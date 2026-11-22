// Particle morph lab: ~14k particles sampled from real meshes, morphing between shapes and pushed around by the pointer.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MeshSurfaceSampler } from 'three/addons/math/MeshSurfaceSampler.js';

const root = document.querySelector('#particles');
const canvas = root.querySelector('canvas');
const N = matchMedia('(max-width: 700px)').matches ? 8000 : 14000;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(42, 1, .1, 100);
camera.position.set(0, 0, 9.5);
const clock = new THREE.Clock();

// ---------------------------------------------------------------- shape targets
function normalise(arr) {
  const box = new THREE.Box3(), v = new THREE.Vector3();
  for (let i = 0; i < N; i++) box.expandByPoint(v.fromArray(arr, i * 3));
  const c = box.getCenter(new THREE.Vector3()), s = 5.2 / Math.max(...box.getSize(new THREE.Vector3()).toArray());
  for (let i = 0; i < N; i++) { arr[i * 3] = (arr[i * 3] - c.x) * s; arr[i * 3 + 1] = (arr[i * 3 + 1] - c.y) * s; arr[i * 3 + 2] = (arr[i * 3 + 2] - c.z) * s; }
  return arr;
}
function fromMesh(object) {
  const meshes = []; object.updateMatrixWorld(true);
  object.traverse(o => { if (o.isMesh) meshes.push(o); });
  const geos = meshes.map(m => { const g = m.geometry.clone(); g.applyMatrix4(m.matrixWorld); return new THREE.Mesh(g); });
  const areas = geos.map(m => { m.geometry.computeBoundingSphere(); return m.geometry.boundingSphere.radius ** 2; });
  const total = areas.reduce((a, b) => a + b, 0);
  const out = new Float32Array(N * 3), p = new THREE.Vector3(); let k = 0;
  geos.forEach((m, i) => {
    const s = new MeshSurfaceSampler(m).build(), n = i === geos.length - 1 ? N - k : Math.round(N * areas[i] / total);
    for (let j = 0; j < n && k < N; j++, k++) { s.sample(p); out.set([p.x, p.y, p.z], k * 3); }
  });
  return normalise(out);
}
function galaxy() {
  const out = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    const arm = i % 3, r = Math.pow(Math.random(), .6) * 3.2, a = r * 1.6 + arm * 2.094 + (Math.random() - .5) * .5;
    out.set([Math.cos(a) * r, (Math.random() - .5) * .35 * (1.2 - r / 3.2), Math.sin(a) * r], i * 3);
  }
  return out;
}
function knot() {
  const g = new THREE.TorusKnotGeometry(1.6, .5, 220, 24, 2, 3);
  return fromMesh(new THREE.Mesh(g));
}

// ---------------------------------------------------------------- points
const geo = new THREE.BufferGeometry();
const pos = new Float32Array(N * 3), target = new Float32Array(N * 3), vel = new Float32Array(N * 3), seed = new Float32Array(N);
for (let i = 0; i < N; i++) { pos.set([(Math.random() - .5) * 12, (Math.random() - .5) * 8, (Math.random() - .5) * 6], i * 3); seed[i] = Math.random(); }
geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
geo.setAttribute('seed', new THREE.BufferAttribute(seed, 1));
const mat = new THREE.ShaderMaterial({
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  uniforms: { uTime: { value: 0 }, uA: { value: new THREE.Color(0x9c8cff) }, uB: { value: new THREE.Color(0xff7ac8) }, uC: { value: new THREE.Color(0xffc86b) }, uPx: { value: renderer.getPixelRatio() } },
  vertexShader: `attribute float seed; uniform float uTime, uPx; varying float vS; varying float vY;
    void main(){ vS = seed; vec4 mv = modelViewMatrix * vec4(position,1.); vY = position.y;
      gl_PointSize = (2.2 + seed * 2.4) * uPx * (9. / -mv.z); gl_Position = projectionMatrix * mv; }`,
  fragmentShader: `uniform vec3 uA, uB, uC; uniform float uTime; varying float vS; varying float vY;
    void main(){ float d = length(gl_PointCoord - .5); if (d > .5) discard;
      vec3 c = mix(mix(uA, uB, smoothstep(-2.5, 2.5, vY)), uC, step(.93, vS) * (.6 + .4 * sin(uTime * 3. + vS * 40.)));
      gl_FragColor = vec4(c, (1. - d * 2.) * .85); }`,
});
const points = new THREE.Points(geo, mat);
scene.add(points);

// ---------------------------------------------------------------- shapes & UI
const shapes = []; let current = 0, lastSwitch = 0, auto = true;
const btns = root.querySelector('[data-shapes]');
function setShape(i, user = false) {
  current = i; target.set(shapes[i].pts); lastSwitch = clock.elapsedTime; if (user) auto = false;
  btns.querySelectorAll('button').forEach((b, k) => b.classList.toggle('on', k === i));
  for (let k = 0; k < N * 3; k++) vel[k] += (Math.random() - .5) * .25; // a little burst on every morph
}
function addShape(name, pts) {
  shapes.push({ name, pts });
  const b = document.createElement('button'); b.textContent = name; b.addEventListener('click', () => setShape(shapes.indexOf(shapes.find(s => s.name === name)), true));
  btns.append(b);
  if (shapes.length === 1) setShape(0);
}
const loader = new GLTFLoader();
loader.load(root.dataset.robot, g => addShape('Robot', fromMesh(g.scene)));
addShape('Galaxy', galaxy());
loader.load(root.dataset.dino, g => addShape('Dino', fromMesh(g.scene)));
addShape('Knot', knot());

// pointer: project onto the z=0 plane in world space
const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(9, 9), hit = new THREE.Vector3(999, 999, 0), plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
canvas.addEventListener('pointermove', e => {
  const r = canvas.getBoundingClientRect(); ndc.set((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1);
});
canvas.addEventListener('pointerleave', () => ndc.set(9, 9));
canvas.addEventListener('click', () => { if (shapes.length) setShape((current + 1) % shapes.length, true); });

function resize() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (canvas.width !== Math.floor(w * renderer.getPixelRatio())) { renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
}

let visible = true;
new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(root);
const local = new THREE.Vector3(), inv = new THREE.Matrix4();
renderer.setAnimationLoop(() => {
  if (!visible) { clock.getDelta(); return; }
  const dt = Math.min(clock.getDelta(), .05), t = clock.elapsedTime;
  resize();
  mat.uniforms.uTime.value = t;
  points.rotation.y += dt * .18; points.rotation.x = Math.sin(t * .2) * .12;
  if (auto && shapes.length > 1 && t - lastSwitch > 5) setShape((current + 1) % shapes.length);

  ray.setFromCamera(ndc, camera);
  if (ndc.x < 2 && ray.ray.intersectPlane(plane, hit)) { inv.copy(points.matrixWorld).invert(); local.copy(hit).applyMatrix4(inv); } else local.set(999, 999, 999);

  for (let i = 0; i < N; i++) {
    const j = i * 3;
    let fx = (target[j] - pos[j]) * 2.2, fy = (target[j + 1] - pos[j + 1]) * 2.2, fz = (target[j + 2] - pos[j + 2]) * 2.2;
    const dx = pos[j] - local.x, dy = pos[j + 1] - local.y, dz = pos[j + 2] - local.z, d2 = dx * dx + dy * dy + dz * dz;
    if (d2 < 1.6) { const f = (1.6 - d2) * 14; fx += dx * f; fy += dy * f; fz += dz * f; }
    vel[j] = (vel[j] + fx * dt) * .9; vel[j + 1] = (vel[j + 1] + fy * dt) * .9; vel[j + 2] = (vel[j + 2] + fz * dt) * .9;
    pos[j] += vel[j] * dt * 6; pos[j + 1] += vel[j + 1] * dt * 6; pos[j + 2] += vel[j + 2] * dt * 6;
  }
  geo.attributes.position.needsUpdate = true;
  renderer.render(scene, camera);
});
