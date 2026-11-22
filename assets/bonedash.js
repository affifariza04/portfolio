// Bone Dash: a browser prototype of the core loop of my Roblox game "Revive & Steal a Dino".
// Run around the island, collect glowing bones before time runs out; every 4 bones revives a dino with a random mutation.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const root = document.querySelector('#bonedash');
const canvas = root.querySelector('canvas');
const $ = s => root.querySelector(s);
const ui = { time: $('[data-time]'), bones: $('[data-bones]'), revived: $('[data-revived]'), toast: $('[data-toast]'), start: $('[data-start]'),
  over: $('[data-over]'), result: $('[data-result]'), best: $('[data-best]'), stick: $('[data-stick]'), knob: $('[data-knob]') };

// ---------------------------------------------------------------- renderer, scene, post
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(48, 1, 0.1, 300);

// gradient sky dome (purple → peach horizon), matches the key art
const sky = new THREE.Mesh(new THREE.SphereGeometry(150, 32, 16), new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false,
  uniforms: { top: { value: new THREE.Color(0x6e5bd6) }, mid: { value: new THREE.Color(0xc79be6) }, low: { value: new THREE.Color(0xffc9a3) } },
  vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }',
  fragmentShader: `uniform vec3 top, mid, low; varying vec3 vP;
    void main(){ float h = vP.y; vec3 c = h > .18 ? mix(mid, top, smoothstep(.18,.75,h)) : mix(low, mid, smoothstep(-.05,.18,h)); gl_FragColor = vec4(c,1.); }`,
}));
scene.add(sky);
scene.fog = new THREE.Fog(0xe2b3d9, 38, 120);

scene.add(new THREE.HemisphereLight(0xffe7f2, 0x5a4a7a, 1.15));
const sun = new THREE.DirectionalLight(0xffd2a1, 2.6);
sun.position.set(-18, 26, 14); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -26, right: 26, top: 26, bottom: -26, near: 1, far: 90 }); sun.shadow.bias = -0.0006;
scene.add(sun, sun.target);

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.55, 0.5, 0.86);
composer.addPass(bloom); composer.addPass(new OutputPass());

// ---------------------------------------------------------------- world (procedural low-poly island)
const R = 22; // walkable radius
const flat = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, flatShading: true, roughness: .9, ...extra });
function jitter(geo, amt, seed = 1) {
  const p = geo.attributes.position, v = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i);
    const n = Math.sin(v.x * 1.7 + seed) * Math.cos(v.z * 1.3 + seed * 2) * Math.sin(v.y * 2.1 + seed);
    p.setXYZ(i, v.x + n * amt, v.y + n * amt * .6, v.z + n * amt);
  }
  geo.computeVertexNormals(); return geo;
}
const island = new THREE.Group(); scene.add(island);
const sand = new THREE.Mesh(jitter(new THREE.CylinderGeometry(R + 2, R + 7, 3, 28, 2), .45), flat(0xf2c98f));
sand.position.y = -1.5; sand.receiveShadow = true; island.add(sand);
const grass = new THREE.Mesh(jitter(new THREE.CylinderGeometry(R - 7, R - 4.5, .5, 20, 1), .3, 3), flat(0x8fc46a));
grass.position.set(-2, .2, -3); grass.receiveShadow = true; island.add(grass);

// animated low-poly water
const waterGeo = new THREE.PlaneGeometry(260, 260, 70, 70); waterGeo.rotateX(-Math.PI / 2);
const water = new THREE.Mesh(waterGeo, new THREE.MeshStandardMaterial({ color: 0x5fb8d8, flatShading: true, roughness: .35, metalness: .1, transparent: true, opacity: .92 }));
water.position.y = -1.1; water.receiveShadow = true; scene.add(water);
const wBase = waterGeo.attributes.position.array.slice();

const colliders = []; // {x, z, r}
function palm(x, z, s = 1, lean = .25) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = Math.random() * 6.28;
  let px = 0, py = 0;
  for (let i = 0; i < 7; i++) {
    const seg = new THREE.Mesh(new THREE.CylinderGeometry(.22 * s, .3 * s, .9 * s, 6), flat(i % 2 ? 0x9a6b45 : 0xab7a4f));
    px += lean * .22 * i * s; py += .82 * s; seg.position.set(px, py, 0); seg.rotation.z = -lean * .35 * (i / 7);
    seg.castShadow = true; g.add(seg);
  }
  for (let k = 0; k < 7; k++) {
    const leaf = new THREE.Mesh(new THREE.ConeGeometry(.55 * s, 3.4 * s, 4, 1), flat(k % 2 ? 0x5fae4e : 0x79c25a));
    leaf.geometry.translate(0, 1.7 * s, 0); leaf.scale.z = .25;
    leaf.position.set(px, py + .3 * s, 0); leaf.rotation.set(1.15 + Math.random() * .25, (k / 7) * 6.28, 0, 'YXZ');
    leaf.castShadow = true; g.add(leaf);
  }
  island.add(g); colliders.push({ x, z, r: .8 * s });
}
function rock(x, z, s) {
  const m = new THREE.Mesh(jitter(new THREE.DodecahedronGeometry(s, 0), s * .12, x), flat(0x9b8fb0));
  m.position.set(x, s * .35, z); m.rotation.set(Math.random(), Math.random() * 6, 0); m.castShadow = m.receiveShadow = true;
  island.add(m); colliders.push({ x, z, r: s * .9 });
}
function bush(x, z) {
  const m = new THREE.Mesh(jitter(new THREE.IcosahedronGeometry(.9, 0), .12, z), flat([0x4f9a55, 0x6db35a, 0xc85fa0][Math.floor(Math.random() * 3)]));
  m.position.set(x, .45, z); m.castShadow = true; island.add(m);
}
[[-10, 6, 1.15], [9, -11, 1], [14, 7, .95], [-15, -9, 1.1], [3, 14, .9], [-4, -16, 1]].forEach(([x, z, s]) => palm(x, z, s));
[[6, 3, 1.3], [-7, -2, 1], [12, -3, .8], [-12, 12, 1.4], [16, 14, 1.1], [-17, 3, .9], [2, -9, .7]].forEach(([x, z, s]) => rock(x, z, s));
for (let i = 0; i < 16; i++) { const a = Math.random() * 6.28, r = 5 + Math.random() * (R - 7); bush(Math.cos(a) * r, Math.sin(a) * r); }

// ---------------------------------------------------------------- bones
function boneMesh() {
  const g = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({ color: 0xfff1c9, emissive: 0xffb84d, emissiveIntensity: 1.6, roughness: .4, flatShading: true });
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(.12, .12, 1, 8), mat); shaft.rotation.z = Math.PI / 2; g.add(shaft);
  for (const sx of [-.5, .5]) for (const sz of [-.13, .13]) {
    const k = new THREE.Mesh(new THREE.IcosahedronGeometry(.2, 0), mat); k.position.set(sx, 0, sz); g.add(k);
  }
  const halo = new THREE.Mesh(new THREE.RingGeometry(.55, .75, 24), new THREE.MeshBasicMaterial({ color: 0xffd27a, transparent: true, opacity: .5, side: THREE.DoubleSide }));
  halo.rotation.x = -Math.PI / 2; halo.position.y = -.75; g.add(halo);
  g.userData.halo = halo;
  return g;
}
const bones = [];
function placeBone(b) {
  for (let tries = 0; tries < 40; tries++) {
    const a = Math.random() * 6.28, r = 3 + Math.random() * (R - 5);
    const x = Math.cos(a) * r, z = Math.sin(a) * r;
    if (colliders.every(c => Math.hypot(c.x - x, c.z - z) > c.r + 1) && (!player || Math.hypot(player.position.x - x, player.position.z - z) > 6)) {
      b.position.set(x, 1, z); b.userData.phase = Math.random() * 6; return;
    }
  }
}
let player;
for (let i = 0; i < 7; i++) { const b = boneMesh(); scene.add(b); bones.push(b); }

// sparkle burst particles
const sparkGeo = new THREE.BufferGeometry(), SP = 160;
const sPos = new Float32Array(SP * 3), sVel = new Float32Array(SP * 3), sLife = new Float32Array(SP);
sparkGeo.setAttribute('position', new THREE.BufferAttribute(sPos, 3));
const sparks = new THREE.Points(sparkGeo, new THREE.PointsMaterial({ color: 0xffe08a, size: .22, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
scene.add(sparks);
function burst(p, n = 40, color) {
  if (color) sparks.material.color.set(color);
  for (let i = 0, k = 0; i < SP && k < n; i++) if (sLife[i] <= 0) {
    sPos.set([p.x, p.y, p.z], i * 3);
    const a = Math.random() * 6.28, u = Math.random() * 2 - 1, s = 3 + Math.random() * 4;
    sVel.set([Math.cos(a) * Math.sqrt(1 - u * u) * s, Math.abs(u) * s + 2, Math.sin(a) * Math.sqrt(1 - u * u) * s], i * 3);
    sLife[i] = .7 + Math.random() * .5; k++;
  }
}

// ---------------------------------------------------------------- player (CC0 frilled dino, idle/walk/run)
let mixer, acts = {}, current;
const tex = new THREE.TextureLoader().load(root.dataset.tex); tex.colorSpace = THREE.SRGBColorSpace; tex.flipY = false;
new GLTFLoader().load(root.dataset.model, gltf => {
  const model = gltf.scene;
  model.traverse(o => { if (o.isMesh) { o.castShadow = true; o.material = new THREE.MeshStandardMaterial({ map: tex, roughness: .75 }); } });
  const box = new THREE.Box3().setFromObject(model), size = box.getSize(new THREE.Vector3());
  const s = 3.4 / Math.max(size.x, size.y, size.z); model.scale.setScalar(s);
  box.setFromObject(model); model.position.y -= box.min.y;
  // the model's nose points along -Z; wrap it so +Z is "forward" for movement maths
  player = new THREE.Group(); const holder = new THREE.Group(); holder.rotation.y = Math.PI; holder.add(model); player.add(holder);
  scene.add(player);
  mixer = new THREE.AnimationMixer(model);
  gltf.animations.forEach(c => { acts[c.name.replace('-loop', '')] = mixer.clipAction(c); });
  play('idle');
  bones.forEach(placeBone);
  root.classList.add('ready');
});
function play(name, speed = 1) {
  const a = acts[name]; if (!a) return;
  a.timeScale = speed;
  if (a === current) return;
  a.reset().fadeIn(.2).play(); current?.fadeOut(.2); current = a;
}

// ---------------------------------------------------------------- input
const keys = new Set();
const KM = { KeyW: 'f', ArrowUp: 'f', KeyS: 'b', ArrowDown: 'b', KeyA: 'l', ArrowLeft: 'l', KeyD: 'r', ArrowRight: 'r', ShiftLeft: 'run', ShiftRight: 'run' };
addEventListener('keydown', e => { if (state === 'play' && KM[e.code]) { keys.add(KM[e.code]); e.preventDefault(); } });
addEventListener('keyup', e => { if (KM[e.code]) keys.delete(KM[e.code]); });
const stick = { x: 0, y: 0, id: null };
ui.stick.addEventListener('pointerdown', e => { stick.id = e.pointerId; ui.stick.setPointerCapture(e.pointerId); moveStick(e); });
ui.stick.addEventListener('pointermove', e => { if (e.pointerId === stick.id) moveStick(e); });
const release = () => { stick.id = null; stick.x = stick.y = 0; ui.knob.style.transform = ''; };
ui.stick.addEventListener('pointerup', release); ui.stick.addEventListener('pointercancel', release);
function moveStick(e) {
  const r = ui.stick.getBoundingClientRect(), dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
  const m = Math.min(1, Math.hypot(dx, dy) / (r.width / 2)), a = Math.atan2(dy, dx);
  stick.x = Math.cos(a) * m; stick.y = Math.sin(a) * m;
  ui.knob.style.transform = `translate(${stick.x * 34}px, ${stick.y * 34}px)`;
}

// ---------------------------------------------------------------- game state
const ROUND = 60, MUT = [['Golden', '#ffc94d'], ['Lava', '#ff6a3d'], ['Galaxy', '#a68bff'], ['Rainbow', '#7df0c8'], ['Classic', '#ffffff']];
let state = 'menu', timeLeft = ROUND, collected = 0, revived = 0, camYaw = 0;
const best = () => { try { return +localStorage.getItem('bonedash.best') || 0; } catch { return 0; } };
ui.best.textContent = best();
root.querySelectorAll('[data-play]').forEach(b => b.addEventListener('click', start));
function start() {
  if (!player) return;
  state = 'play'; timeLeft = ROUND; collected = 0; revived = 0;
  player.position.set(0, 0, 0); bones.forEach(placeBone);
  ui.start.hidden = true; ui.over.hidden = true; hud(); root.focus({ preventScroll: true });
}
function end() {
  state = 'over'; keys.clear(); play('idle');
  const score = collected;
  try { if (score > best()) localStorage.setItem('bonedash.best', score); } catch { /* private mode */ }
  ui.result.textContent = `${score} bones · ${revived} dino${revived === 1 ? '' : 's'} revived`;
  ui.best.textContent = best(); ui.over.hidden = false;
}
function hud() {
  ui.time.textContent = Math.ceil(timeLeft); ui.bones.textContent = `${collected % 4}/4`; ui.revived.textContent = revived;
  root.classList.toggle('hurry', state === 'play' && timeLeft < 10);
}
let toastT;
function toast(text, color) {
  ui.toast.textContent = text; ui.toast.style.setProperty('--c', color); ui.toast.classList.remove('on'); void ui.toast.offsetWidth; ui.toast.classList.add('on');
  clearTimeout(toastT); toastT = setTimeout(() => ui.toast.classList.remove('on'), 1600);
}

// ---------------------------------------------------------------- loop
const clock = new THREE.Clock(), tmp = new THREE.Vector3(), camPos = new THREE.Vector3(0, 9, 16), look = new THREE.Vector3();
let visible = true, speed = 0;
new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(root);
function resize() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (canvas.width !== Math.floor(w * renderer.getPixelRatio()) || canvas.height !== Math.floor(h * renderer.getPixelRatio())) {
    renderer.setSize(w, h, false); composer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix();
  }
}
renderer.setAnimationLoop(() => {
  if (!visible) { clock.getDelta(); return; }
  const dt = Math.min(clock.getDelta(), .05), t = clock.elapsedTime;
  resize();

  // water waves
  const wp = waterGeo.attributes.position;
  for (let i = 0; i < wp.count; i++) {
    const x = wBase[i * 3], z = wBase[i * 3 + 2];
    wp.array[i * 3 + 1] = Math.sin(x * .25 + t * 1.2) * .18 + Math.cos(z * .3 + t * .9) * .15;
  }
  wp.needsUpdate = true; waterGeo.computeVertexNormals();

  // bones bob + spin
  for (const b of bones) {
    b.rotation.y += dt * 1.6; b.position.y = 1 + Math.sin(t * 2.4 + b.userData.phase) * .18;
    b.userData.halo.scale.setScalar(1 + Math.sin(t * 3 + b.userData.phase) * .12);
  }

  if (player) {
    if (state === 'play') {
      timeLeft -= dt; if (timeLeft <= 0) { timeLeft = 0; end(); }
      // input → camera-relative direction
      let ix = (keys.has('r') ? 1 : 0) - (keys.has('l') ? 1 : 0) + stick.x;
      let iz = (keys.has('b') ? 1 : 0) - (keys.has('f') ? 1 : 0) + stick.y;
      const mag = Math.min(1, Math.hypot(ix, iz));
      const run = keys.has('run') || Math.hypot(stick.x, stick.y) > .85;
      const target = mag > .1 ? (run ? 9.5 : 5.2) * mag : 0;
      speed += (target - speed) * Math.min(1, dt * 8);
      if (mag > .1) {
        const ang = Math.atan2(ix, iz) + camYaw;
        let d = ang - player.rotation.y; d = Math.atan2(Math.sin(d), Math.cos(d));
        player.rotation.y += d * Math.min(1, dt * 10);
      }
      tmp.set(Math.sin(player.rotation.y), 0, Math.cos(player.rotation.y)).multiplyScalar(speed * dt);
      player.position.add(tmp);
      for (const c of colliders) {
        const dx = player.position.x - c.x, dz = player.position.z - c.z, dd = Math.hypot(dx, dz), min = c.r + .7;
        if (dd < min) player.position.x = c.x + dx / dd * min, player.position.z = c.z + dz / dd * min;
      }
      const dc = Math.hypot(player.position.x, player.position.z);
      if (dc > R) player.position.multiplyScalar(R / dc);
      play(speed > 6.5 ? 'run' : speed > .6 ? 'walk' : 'idle', speed > 6.5 ? speed / 8 : Math.max(.6, speed / 4));

      for (const b of bones) if (b.position.distanceTo(tmp.copy(player.position).setY(1)) < 1.9) {
        burst(b.position, 36, 0xffe08a); collected++; placeBone(b);
        if (collected % 4 === 0) {
          revived++; const [name, color] = MUT[Math.floor(Math.random() * MUT.length)];
          toast(`${name} dino revived!`, color); burst(tmp.copy(player.position).setY(2), 90, color); timeLeft = Math.min(ROUND, timeLeft + 5);
        }
      }
      hud();
    } else {
      play('idle'); player.rotation.y += dt * .3;
    }
    // follow camera: behind and above, smoothed; slowly aligns with travel direction
    if (state === 'play' && speed > 1) { let d = player.rotation.y - camYaw; d = Math.atan2(Math.sin(d), Math.cos(d)); camYaw += d * dt * .8; }
    const off = new THREE.Vector3(Math.sin(camYaw + Math.PI) * 8.5, 5.2, Math.cos(camYaw + Math.PI) * 8.5);
    const desired = state === 'play' ? tmp.copy(player.position).add(off) : new THREE.Vector3(Math.sin(t * .1) * 26, 13, Math.cos(t * .1) * 26);
    camPos.lerp(desired, Math.min(1, dt * (state === 'play' ? 4 : 1.2)));
    camera.position.copy(camPos);
    look.lerp(state === 'play' ? tmp.copy(player.position).setY(1.4) : new THREE.Vector3(0, 1, 0), Math.min(1, dt * 5));
    camera.lookAt(look);
    sun.position.set(player.position.x - 18, 26, player.position.z + 14); sun.target.position.copy(player.position);
    mixer.update(dt);
  } else {
    camera.position.set(Math.sin(t * .1) * 26, 13, Math.cos(t * .1) * 26); camera.lookAt(0, 1, 0);
  }

  // particles
  for (let i = 0; i < SP; i++) if (sLife[i] > 0) {
    sLife[i] -= dt; sVel[i * 3 + 1] -= 9 * dt;
    sPos[i * 3] += sVel[i * 3] * dt; sPos[i * 3 + 1] += sVel[i * 3 + 1] * dt; sPos[i * 3 + 2] += sVel[i * 3 + 2] * dt;
    if (sLife[i] <= 0) sPos[i * 3 + 1] = -99;
  }
  sparkGeo.attributes.position.needsUpdate = true;

  composer.render();
});
