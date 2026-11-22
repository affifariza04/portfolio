// Character playground: orbit, play animations, set facial expressions, drive with WASD / arrows / on-screen pad.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const root = document.querySelector('#playground');
const canvas = root.querySelector('canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x0b0918, 18, 42);
const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
camera.position.set(8.5, 5.5, 12.5);
const controls = new OrbitControls(camera, canvas);
controls.target.set(0, 1.6, 0); controls.enableDamping = true; controls.minDistance = 5; controls.maxDistance = 22; controls.maxPolarAngle = 1.45;
controls.enablePan = false;

scene.add(new THREE.HemisphereLight(0xc9c0ff, 0x221a3a, 1.4));
const sun = new THREE.DirectionalLight(0xffffff, 2.4); sun.position.set(5, 10, 4); sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024); Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8 }); scene.add(sun);
const rim = new THREE.PointLight(0xff7ac8, 30, 20); rim.position.set(-5, 4, -4); scene.add(rim);

// arena: glowing disc + grid ring
const R = 7;
const floor = new THREE.Mesh(new THREE.CircleGeometry(R, 64), new THREE.MeshStandardMaterial({ color: 0x1a1533, roughness: .85 }));
floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
const ring = new THREE.Mesh(new THREE.TorusGeometry(R, .06, 8, 96), new THREE.MeshBasicMaterial({ color: 0x9c8cff }));
ring.rotation.x = Math.PI / 2; scene.add(ring);
const grid = new THREE.PolarGridHelper(R, 12, 6, 64, 0x3a2f6b, 0x2a2350); grid.position.y = .01; scene.add(grid);
// collectible orbs to make "driving" fun
const orbs = [];
for (let i = 0; i < 6; i++) {
  const o = new THREE.Mesh(new THREE.IcosahedronGeometry(.28, 1), new THREE.MeshStandardMaterial({ color: 0xffc86b, emissive: 0xff9a3c, emissiveIntensity: 1.4 }));
  orbs.push(o); scene.add(o); placeOrb(o);
}
function placeOrb(o) { const a = Math.random() * Math.PI * 2, r = 1.8 + Math.random() * (R - 2.6); o.position.set(Math.cos(a) * r, .6, Math.sin(a) * r); }

let model, mixer, actions = {}, active, face;
const ui = { anims: root.querySelector('[data-anims]'), faces: root.querySelector('[data-faces]'), score: root.querySelector('[data-score]'), hint: root.querySelector('[data-hint]') };
let score = 0;

new GLTFLoader().load(root.dataset.model, gltf => {
  model = gltf.scene; model.scale.setScalar(.9);
  model.traverse(o => { if (o.isMesh) o.castShadow = true; });
  scene.add(model);
  mixer = new THREE.AnimationMixer(model);
  const once = ['Jump', 'Yes', 'No', 'Wave', 'Punch', 'ThumbsUp'];
  gltf.animations.forEach(clip => {
    const a = mixer.clipAction(clip); actions[clip.name] = a;
    if (once.includes(clip.name) || ['Death', 'Sitting', 'Standing'].includes(clip.name)) { a.clampWhenFinished = true; a.loop = THREE.LoopOnce; }
  });
  const show = ['Idle', 'Walking', 'Running', 'Dance', 'Jump', 'Wave', 'ThumbsUp', 'Yes', 'No', 'Punch', 'Sitting', 'Death'];
  ui.anims.innerHTML = show.filter(n => actions[n]).map(n => `<button data-a="${n}">${n.replace('ThumbsUp', 'Thumbs up')}</button>`).join('');
  ui.anims.addEventListener('click', e => { const b = e.target.closest('button'); if (b) play(b.dataset.a, true); });
  face = model.getObjectByName('Head_4');
  if (face?.morphTargetDictionary) {
    ui.faces.innerHTML = Object.keys(face.morphTargetDictionary).map((k, i) =>
      `<label>${k}<input type="range" min="0" max="1" step="0.01" value="0" data-i="${i}"></label>`).join('');
    ui.faces.addEventListener('input', e => { if (e.target.dataset.i) face.morphTargetInfluences[+e.target.dataset.i] = +e.target.value; });
  }
  play('Idle');
  root.classList.add('ready');
  mixer.addEventListener('finished', e => { if (once.includes(e.action.getClip().name)) play(moving ? 'Running' : 'Idle'); });
});

function play(name, user = false) {
  const next = actions[name]; if (!next || next === active) { if (user && next) next.reset().play(); return; }
  next.reset().setEffectiveTimeScale(1).setEffectiveWeight(1).fadeIn(.25).play();
  if (active) active.fadeOut(.25);
  active = next;
  root.querySelectorAll('[data-anims] button').forEach(b => b.classList.toggle('on', b.dataset.a === name));
}

// driving
const keys = new Set();
let moving = false;
const map = { KeyW: 'f', ArrowUp: 'f', KeyS: 'b', ArrowDown: 'b', KeyA: 'l', ArrowLeft: 'l', KeyD: 'r', ArrowRight: 'r' };
addEventListener('keydown', e => {
  if (!map[e.code] || !root.matches(':hover, :focus-within')) return;
  e.preventDefault(); keys.add(map[e.code]);
});
addEventListener('keyup', e => map[e.code] && keys.delete(map[e.code]));
root.querySelectorAll('[data-pad]').forEach(b => {
  const k = b.dataset.pad;
  b.addEventListener('pointerdown', () => keys.add(k)); ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => b.addEventListener(ev, () => keys.delete(k)));
});

function resize() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (canvas.width !== Math.floor(w * renderer.getPixelRatio())) { renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
}

const clock = new THREE.Clock();
const fwd = new THREE.Vector3();
let visible = true;
new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(root);
renderer.setAnimationLoop(() => {
  if (!visible) return;
  const dt = Math.min(clock.getDelta(), .05);
  resize();
  if (model) {
    const turn = (keys.has('l') ? 1 : 0) - (keys.has('r') ? 1 : 0);
    const go = (keys.has('f') ? 1 : 0) - (keys.has('b') ? .6 : 0);
    model.rotation.y += turn * 2.6 * dt;
    const want = go !== 0;
    if (want !== moving) { moving = want; play(moving ? 'Running' : 'Idle'); ui.hint?.classList.add('gone'); }
    if (moving) {
      fwd.set(Math.sin(model.rotation.y), 0, Math.cos(model.rotation.y)).multiplyScalar(go * 4.2 * dt);
      model.position.add(fwd);
      const d = Math.hypot(model.position.x, model.position.z);
      if (d > R - .8) model.position.multiplyScalar((R - .8) / d);
    }
    for (const o of orbs) {
      o.rotation.y += dt * 2; o.position.y = .6 + Math.sin(clock.elapsedTime * 3 + o.id) * .12;
      if (o.position.distanceTo(model.position.clone().setY(.6)) < .9) { placeOrb(o); score++; ui.score.textContent = score; play('Jump'); }
    }
    controls.target.lerp(new THREE.Vector3(model.position.x, 1.6, model.position.z), .08);
  }
  mixer?.update(dt);
  controls.update();
  renderer.render(scene, camera);
});
