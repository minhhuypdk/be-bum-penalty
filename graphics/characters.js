import * as THREE from '../vendor/three.module.js';

export const CHARACTER_PRESETS = Object.freeze({
  'ba-player': { person: 'ba', keeper: false, shirt: 0x176fe5 },
  'bum-player': { person: 'bum', keeper: false, shirt: 0xffb52e },
  'ba-keeper': { person: 'ba', keeper: true, shirt: 0x18b99c },
  'bum-keeper': { person: 'bum', keeper: true, shirt: 0xa06af2 },
});

// Shared geometry and materials keep all four articulated characters inexpensive.
const sphere = new THREE.SphereGeometry(1, 24, 20);
const materials = new Map();
function material(color, roughness = .65) {
  const key = `${color}:${roughness}`;
  if (!materials.has(key)) materials.set(key, new THREE.MeshStandardMaterial({ color, roughness }));
  return materials.get(key);
}
export function createCharacter(id) {
  const preset = CHARACTER_PRESETS[id];
  if (!preset) throw new Error(`Unknown character: ${id}`);
  const root = new THREE.Group();
  root.name = id;
  const skin = preset.person === 'ba' ? 0xe9ac7b : 0xf8c397;
  function part(parent, color, position, scale, roughness) {
    const mesh = new THREE.Mesh(sphere, material(color, roughness));
    mesh.position.set(...position); mesh.scale.set(...scale);
    mesh.castShadow = true; mesh.receiveShadow = true; parent.add(mesh); return mesh;
  }
  part(root, preset.shirt, [0, 1.12, 0], [.35, .43, .23]);
  part(root, 0x182e53, [0, .73, 0], [.32, .18, .22]);
  part(root, 0xffffff, [0, 1.43, .05], [.16, .035, .18]);
  // Raised jersey crest and contrasting side panels.
  part(root, 0xffe48e, [-.14, 1.25, .213], [.055, .065, .018], .35);
  for (const side of [-1, 1]) part(root, 0xffffff, [side * .3, 1.1, 0], [.035, .26, .16]);
  const head = new THREE.Group(); head.position.y = 1.8; root.add(head);
  part(head, skin, [0, 0, 0], [.34, .37, .3]);
  for (const side of [-1, 1]) {
    part(head, skin, [side * .34, -.02, 0], [.07, .105, .07]);
    part(head, 0xffffff, [side * .125, .035, .265], [.09, .105, .035]);
    part(head, 0x263750, [side * .12, .025, .296], [.045, .062, .018], .25);
    part(head, 0xffffff, [side * .12 - .012, .047, .311], [.015, .019, .008]);
    part(head, 0x51352c, [side * .125, .17, .267], [.09, .024, .018]);
    part(head, 0xed947e, [side * .22, -.09, .247], [.065, .035, .012]);
  }
  part(head, skin, [0, -.045, .305], [.065, .07, .06]);
  part(head, 0x793c39, [0, -.16, .269], [.105, .045, .018]);
  part(head, 0xffffff, [0, -.145, .284], [.075, .014, .008]);
  part(head, 0x30251f, [0, .255, -.035], [.35, .17, .29]);
  for (let i = 0; i < 5; i++) {
    const tuft = part(head, 0x30251f, [(i - 2) * .105, .32 + i * .009, .06], [.09, .14, .2]);
    tuft.rotation.z = -.3;
  }
  if (preset.person === 'ba') {
    for (const side of [-1, 1]) part(head, 0x51352c, [side * .065, -.105, .304], [.07, .025, .012]);
  }
  const joints = {};
  for (const side of [-1, 1]) {
    const arm = new THREE.Group(); arm.position.set(side * .36, 1.35, 0); root.add(arm);
    part(arm, preset.shirt, [side * .035, -.1, 0], [.12, .19, .13]);
    part(arm, skin, [side * .07, -.32, .02], [.09, .18, .09]);
    part(arm, preset.keeper ? 0xffefcd : skin, [side * .075, -.49, .045],
      preset.keeper ? [.14, .16, .095] : [.095, .115, .08]);
    if (preset.keeper) part(arm, 0x203459, [side * .075, -.39, .045], [.135, .045, .1]);
    const leg = new THREE.Group(); leg.position.set(side * .17, .72, 0); root.add(leg);
    part(leg, skin, [0, -.17, 0], [.115, .22, .12]);
    part(leg, 0xffffff, [0, -.4, 0], [.11, .16, .11]);
    part(leg, preset.shirt, [0, -.31, 0], [.112, .03, .112]);
    part(leg, 0x203459, [0, -.58, .085], [.14, .09, .23], .38);
    part(leg, 0xffffff, [0, -.62, .09], [.14, .025, .22]);
    joints[side < 0 ? 'leftArm' : 'rightArm'] = arm;
    joints[side < 0 ? 'leftLeg' : 'rightLeg'] = leg;
  }
  if (preset.person === 'bum') root.scale.setScalar(.85);
  root.userData = { preset, joints, head };
  return root;
}

export function poseCharacter(root, time, action = 'idle', progress = 0) {
  const { joints, head, preset } = root.userData;
  const pulse = Math.sin(Math.PI * Math.min(1, Math.max(0, progress)));
  head.rotation.z = Math.sin(time * 1.4) * .025;
  joints.leftArm.rotation.z = -.15 - (preset.keeper ? .25 : 0);
  joints.rightArm.rotation.z = .15 + (preset.keeper ? .25 : 0);
  joints.leftArm.rotation.x = Math.sin(time * 2) * .04;
  joints.rightArm.rotation.x = -Math.sin(time * 2) * .04;
  joints.leftLeg.rotation.x = 0;
  joints.rightLeg.rotation.x = action === 'kick' ? -pulse * 1.3 : 0;
  if (action === 'save') {
    joints.leftArm.rotation.z -= pulse * 1.3;
    joints.rightArm.rotation.z += pulse * 1.3;
  }
  if (action === 'celebrate') {
    joints.leftArm.rotation.z = -2.5; joints.rightArm.rotation.z = 2.5;
  }
}
