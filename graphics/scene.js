import * as THREE from '../vendor/three.module.js';
import { createCharacter, poseCharacter } from './characters.js';

const host = document.querySelector('.goal');
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.25;
  renderer.domElement.setAttribute('aria-label', 'Sân 3D: cầu thủ và thủ môn BA, BUM');
  host.append(renderer.domElement);
  host.classList.add('ready-3d');
} catch (error) {
  console.warn('Sân 3D chưa khả dụng; giữ sân hiện tại.', error);
}
if (renderer) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x99d9f5);
  scene.fog = new THREE.Fog(0x99d9f5, 18, 45);
  const camera = new THREE.PerspectiveCamera(42, 1, .1, 60);
  camera.position.set(5.1, 3.6, 9.5); camera.lookAt(0, 1, 0);
  scene.add(new THREE.HemisphereLight(0xe2f5ff, 0x4d7953, 2.4));
  const sun = new THREE.DirectionalLight(0xffefd4, 3.2);
  sun.position.set(-4, 8, 5); sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  Object.assign(sun.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9 });
  sun.shadow.normalBias = .03; scene.add(sun);
  function box(size, position, color) {
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(...size), new THREE.MeshStandardMaterial({ color, roughness: .8 }));
    mesh.position.set(...position); mesh.receiveShadow = true; mesh.castShadow = true; scene.add(mesh); return mesh;
  }
  box([30, .1, 40], [0, -.12, 0], 0x4baf71);
  for (let i = -5; i < 5; i++) box([14, .012, 1.5], [0, -.06, i * 3], 0x55b879);
  box([6.3, .025, .045], [0, 0, -2.5], 0xffffff);
  for (const x of [-3, 3]) box([.1, 2.65, .1], [x, 1.3, -2.5], 0xffffff);
  box([6.1, .1, .1], [0, 2.6, -2.5], 0xffffff);
  const lines = [];
  for (let x = -3; x <= 3.01; x += .25) lines.push(x, 0, -3.15, x, 2.6, -3.15);
  for (let y = 0; y <= 2.61; y += .25) lines.push(-3, y, -3.15, 3, y, -3.15);
  const net = new THREE.BufferGeometry(); net.setAttribute('position', new THREE.Float32BufferAttribute(lines, 3));
  scene.add(new THREE.LineSegments(net, new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: .4 })));
  const characters = {};
  for (const id of ['ba-player', 'bum-player', 'ba-keeper', 'bum-keeper']) {
    characters[id] = createCharacter(id); scene.add(characters[id]);
  }
  const ball = new THREE.Mesh(new THREE.IcosahedronGeometry(.17, 1), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .35, flatShading: true }));
  ball.castShadow = true; scene.add(ball);
  const seams = new THREE.LineSegments(new THREE.EdgesGeometry(ball.geometry), new THREE.LineBasicMaterial({ color: 0x28405b })); ball.add(seams);
  let state = null, resultKey = '', start = -10;
  window.addEventListener('penalty:state', event => {
    state = event.detail;
    const key = `${state.matchId}:${state.turn}:${state.stage}`;
    if (state.stage === 'result' && key !== resultKey) { start = performance.now() / 1000; resultKey = key; }
  });
  const resize = new ResizeObserver(() => {
    const { width, height } = host.getBoundingClientRect();
    if (!width || !height) return;
    renderer.setSize(width, height); camera.aspect = width / height; camera.updateProjectionMatrix();
  }); resize.observe(host);
  const targets = [[-2.15, 2.15], [0, 2.2], [2.15, 2.15], [-2.15, .45], [2.15, .45]];
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  renderer.setAnimationLoop(() => {
    if (document.hidden || !host.clientHeight) return;
    const now = performance.now() / 1000;
    const shooting = (state?.turn || 0) % 2 === 0 ? 'ba' : 'bum';
    const elapsed = now - start;
    const active = state?.stage === 'result';
    const t = active ? (reducedMotion ? 1 : THREE.MathUtils.clamp((elapsed - .2) / .85, 0, 1)) : 0;
    for (const [id, character] of Object.entries(characters)) {
      const isKeeper = character.userData.preset.keeper;
      character.visible = id === `${shooting}-player` || id === `${shooting === 'ba' ? 'bum' : 'ba'}-keeper`;
      character.position.set(isKeeper ? 0 : -.7, 0, isKeeper ? -2.05 : 2.2);
      character.rotation.set(0, isKeeper ? 0 : Math.PI, 0);
      poseCharacter(character, reducedMotion ? 0 : now, active ? (isKeeper ? 'save' : 'kick') : 'idle', t);
      if (isKeeper && active) {
        const target = targets[state.dive] || targets[1];
        character.position.x = target[0] * t * .85;
        character.position.y = target[1] > 1 ? Math.sin(t * Math.PI) * .5 : 0;
        character.rotation.z = -Math.sign(target[0]) * t * .65;
      }
    }
    const target = targets[state?.shot] || targets[1];
    const saved = state?.shot === state?.dive;
    ball.position.set(target[0] * t, .18 + (target[1] - .18) * t + Math.sin(t * Math.PI) * .5, 2 - (saved ? 3.8 : 5) * t);
    ball.rotation.x = t * 12; ball.rotation.z = t * 5;
    renderer.render(scene, camera);
  });
  host.dataset.graphics = 'ready';
}
