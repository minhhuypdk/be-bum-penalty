import * as THREE from '../vendor/three.module.js';

export const CHARACTER_PRESETS = Object.freeze({
  'ba-player': { person:'ba', keeper:false, shirt:0x226cda, accent:0xffdb78 },
  'bum-player': { person:'bum', keeper:false, shirt:0xf6ac30, accent:0x194d86 },
  'ba-keeper': { person:'ba', keeper:true, shirt:0x149c92, accent:0xc4fff0 },
  'bum-keeper': { person:'bum', keeper:true, shirt:0x8256ca, accent:0xfce5a1 },
});
const sphere = new THREE.SphereGeometry(1, 16, 12);
const materialCache = new Map();
function mat(color, roughness=.6) {
  const key=`${color}:${roughness}`;
  if(!materialCache.has(key)) materialCache.set(key,new THREE.MeshPhysicalMaterial({color,roughness,clearcoat:.08,clearcoatRoughness:.6}));
  return materialCache.get(key);
}

// Authored cross-sections form continuous cheeks, jaw, shoulders and tailored kit.
// Every ring is [height, half-width, half-depth, forward-offset].
function contour(rings, segments=48) {
  const source=rings; rings=[];
  const cubic=(a,b,c,d,t)=>.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t);
  for(let i=0;i<source.length-1;i++)for(let j=0;j<6;j++){
    const ring=[];for(let k=0;k<4;k++)ring.push(cubic(source[Math.max(0,i-1)][k]||0,source[i][k]||0,source[i+1][k]||0,source[Math.min(source.length-1,i+2)][k]||0,j/6));
    ring[1]=Math.max(.002,ring[1]);ring[2]=Math.max(.002,ring[2]);rings.push(ring);
  }
  rings.push(source[source.length-1]);
  const vertices=[], uv=[], indices=[];
  for(let i=0;i<rings.length;i++) {
    const [y,w,d,z=0]=rings[i];
    for(let j=0;j<=segments;j++) {
      const angle=j/segments*Math.PI*2;
      vertices.push(Math.sin(angle)*w,y,Math.cos(angle)*d+z);
      uv.push(j/segments,i/(rings.length-1));
      if(i&&j) { const a=i*(segments+1)+j,b=a-segments-1;indices.push(a,a-1,b,b,a-1,b-1); }
    }
  }
  const geometry=new THREE.BufferGeometry();
  geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));
  geometry.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
  geometry.setIndex(indices);geometry.computeVertexNormals();
  const normals=geometry.attributes.normal;
  for(let i=0;i<rings.length;i++){const a=i*(segments+1),b=a+segments;const n=new THREE.Vector3().fromBufferAttribute(normals,a).add(new THREE.Vector3().fromBufferAttribute(normals,b)).normalize();normals.setXYZ(a,n.x,n.y,n.z);normals.setXYZ(b,n.x,n.y,n.z);}
  return geometry;
}
function curveMesh(points, radius, color, parent, taper=true) {
  const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)));
  const frames=curve.computeFrenetFrames(20,false),positions=[],indices=[];
  for(let i=0;i<=20;i++) {
    const c=curve.getPointAt(i/20),r=radius*(taper ? .02+.98*Math.pow(Math.sin(Math.PI*i/20),.45) : 1);
    for(let j=0;j<=8;j++) {
      const a=j/8*Math.PI*2;
      const p=c.clone().addScaledVector(frames.normals[i],Math.cos(a)*r).addScaledVector(frames.binormals[i],Math.sin(a)*r);
      positions.push(p.x,p.y,p.z);
      if(i&&j){const k=i*9+j;indices.push(k,k-1,k-9,k-9,k-1,k-10);}
    }
  }
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setIndex(indices);g.computeVertexNormals();
  const mesh=new THREE.Mesh(g,mat(color,.52));mesh.castShadow=true;parent.add(mesh);return mesh;
}
const labels=new Map();
function labelTexture(person, back=false) {
  const key=`${person}:${back}`;if(labels.has(key))return labels.get(key);
  const canvas=document.createElement('canvas');canvas.width=256;canvas.height=256;
  const ctx=canvas.getContext('2d');
  ctx.fillStyle='#fff6da';ctx.textAlign='center';ctx.font='800 38px sans-serif';
  ctx.fillText(person.toUpperCase(),128,back?57:70);
  ctx.font='900 140px sans-serif';ctx.fillText(person==='ba'?'10':'7',128,back?205:218);
  const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;labels.set(key,texture);return texture;
}
// Merge parts attached to the same rigid joint, preserving the articulated rig.
function mergeRigidParts(group) {
  for(const child of [...group.children])if(child.isGroup)mergeRigidParts(child);
  const batches=new Map();
  for(const child of group.children)if(child.isMesh&&!child.material.transparent){
    const batch=batches.get(child.material)||[];batch.push(child);batches.set(child.material,batch);
  }
  for(const [material,parts]of batches){
    if(parts.length<2)continue;
    const positions=[],normals=[],uv=[],indices=[];let offset=0;
    for(const part of parts){part.updateMatrix();const g=part.geometry.clone().applyMatrix4(part.matrix);
      positions.push(...g.attributes.position.array);normals.push(...g.attributes.normal.array);if(g.attributes.uv)uv.push(...g.attributes.uv.array);else uv.push(...new Array(g.attributes.position.count*2).fill(0));
      if(g.index)for(const i of g.index.array)indices.push(i+offset);else for(let i=0;i<g.attributes.position.count;i++)indices.push(i+offset);
      offset+=g.attributes.position.count;g.dispose();group.remove(part);
    }
    const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('normal',new THREE.Float32BufferAttribute(normals,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(indices);
    const mesh=new THREE.Mesh(g,material);mesh.castShadow=true;mesh.receiveShadow=true;group.add(mesh);
  }
}
export function createCharacter(id) {
  const preset=CHARACTER_PRESETS[id];if(!preset)throw new Error(`Unknown character: ${id}`);
  const child=preset.person==='bum';
  const root=new THREE.Group();root.name=id;
  const skin=child?0xf4bc91:0xe3a579, hair=child?0x32271f:0x332821;
  function mesh(parent,geometry,color,position=[0,0,0],scale=[1,1,1],roughness=.6) {
    const m=new THREE.Mesh(geometry,mat(color,roughness));m.position.set(...position);m.scale.set(...scale);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
  }
  const oval=(p,c,pos,scale,r)=>mesh(p,sphere,c,pos,scale,r);
  const shirt=mesh(root,contour([[.73,.01,.01],[.75,.25,.19],[.88,.29,.205],[1.08,.315,.21],[1.27,.36,.19],[1.36,.32,.17],[1.42,.17,.14],[1.44,.10,.10]]),preset.shirt);
  // Woven panel seams follow the shirt rather than floating block decorations.
  for(const side of [-1,1]) curveMesh([[side*.25,.82,.14],[side*.285,1.02,.16],[side*.31,1.22,.14],[side*.19,1.39,.12]],.012,preset.accent,root,false);
  const neck=oval(root,skin,[0,1.46,0],[.12,.15,.12]);
  const collar=new THREE.Mesh(new THREE.TorusGeometry(.135,.022,8,40,Math.PI*1.65),mat(preset.accent));
  collar.rotation.x=Math.PI/2;collar.rotation.z=.55;collar.position.set(0,1.415,0);root.add(collar);
  for(const back of [false,true]) {
    const badge=new THREE.Mesh(new THREE.PlaneGeometry(.27,.32),new THREE.MeshStandardMaterial({map:labelTexture(preset.person,back),transparent:true,depthWrite:false,roughness:.85}));
    badge.position.set(0,1.105,back?-.215:.222);if(back)badge.rotation.y=Math.PI;root.add(badge);
  }
  oval(root,preset.accent,[-.19,1.28,.17],[.04,.05,.024],.4);
  for(const side of [-1,1]) mesh(root,contour([[.59,.09,.14],[.62,.15,.18],[.75,.16,.19],[.8,.14,.18]]),0x193653,[side*.155,0,0]);
  const head=new THREE.Group();head.position.set(0,1.79,0);root.add(head);
  const faceRings=[[-.36,.015,.02,.015],[-.33,.14,.14,.02],[-.25,.25,.21,.02],[-.14,.315,.25,.015],[0,.33,.28],[.16,.315,.265],[.29,.245,.22],[.36,.13,.12],[.38,.008,.008]];
  mesh(head,contour(faceRings),skin,[0,0,0],child?[1.06,1,1.05]:[1,1,1],.72);
  const eyes=[];
  for(const side of [-1,1]) {
    oval(head,skin,[side*.325,-.025,-.015],[.075,.11,.07]);
    oval(head,0xce886d,[side*.36,-.025,.035],[.028,.062,.024]);
    // Cheek volumes blend into the jaw; soft blush is a subtle, translucent layer.
    oval(head,skin,[side*.205,-.11,.207],[.10,.075,.043]);
    const blush=oval(head,0xeb927b,[side*.215,-.105,.25],[.049,.025,.006]);blush.material=mat(0xeb927b,.9);
    const eye=new THREE.Group();eye.position.set(side*.124,.045,.258);head.add(eye);eyes.push(eye);
    oval(eye,0xd69776,[0,0,-.005],[.103,.116,.035]);
    oval(eye,0xfff9ed,[0,.002,.014],[.09,.103,.033],.24);
    oval(eye,child?0x654b2e:0x41584f,[0,0,.044],[.051,.069,.018],.2);
    oval(eye,0x172329,[0,-.005,.058],[.028,.046,.012],.18);
    oval(eye,0xffffff,[-.019,.03,.069],[.015,.021,.006],.1);
    oval(eye,0xffffff,[.018,-.025,.068],[.006,.008,.004],.1);
    curveMesh([[side*.20,.16,.238],[side*.13,.188,.272],[side*.06,.16,.269]],.018,hair,head);
  }
  oval(head,skin,[0,-.025,.285],[.065,.09,.075]);
  oval(head,0xd88f6d,[0,-.063,.325],[.047,.029,.027]);
  curveMesh([[-.105,-.17,.252],[-.065,-.204,.27],[0,-.217,.28],[.065,-.204,.27],[.105,-.17,.252]],.018,0x9b4b44,head,false);
  oval(head,0x813f3c,[0,-.185,.269],[.081,.034,.014]);
  oval(head,0xfff8e6,[0,-.17,.28],[.067,.013,.006]);
  if(!child) for(const side of [-1,1]) curveMesh([[side*.018,-.11,.324],[side*.065,-.10,.31],[side*.105,-.12,.285]],.014,0x64402b,head);
  // Sculpted cap plus swept locks. BUM has a softer, tousled silhouette.
  mesh(head,contour([[.13,.26,.25,-.035],[.21,.326,.28,-.035],[.32,.29,.255,-.03],[.41,.19,.18,-.035],[.445,.005,.005,-.04]]),hair);
  for(let i=0;i<7;i++) {
    const x=(i-3)*.08;
    curveMesh(child?[[x,.23+Math.abs(x)*.12,.19],[x-.025,.35,.23],[x+.04,.42-Math.abs(x)*.18,.1],[x+.065,.35,-.08]]:[[x,.2,.215],[x-.065,.31,.26],[x-.11,.40-Math.abs(x)*.2,.09],[x-.07,.34,-.12]],child?.045:.046,hair,head);
  }
  for(const side of [-1,1]) oval(head,hair,[side*.29,.12,-.025],[.04,.15,.19]);
  const joints={}, elbows=[],knees=[];
  for(const side of [-1,1]) {
    const arm=new THREE.Group();arm.position.set(side*.33,1.33,0);root.add(arm);
    mesh(arm,contour([[-.23,.085,.10],[-.20,.115,.12],[-.06,.13,.13],[.04,.08,.09]]),preset.shirt,[side*.035,0,0]);
    const elbow=new THREE.Group();elbow.position.set(side*.045,-.23,0);arm.add(elbow);elbows.push(elbow);
    oval(elbow,skin,[0,-.10,0],[.08,.16,.085]);
    const palm=oval(elbow,preset.keeper?0xffedcc:skin,[0,-.27,.025],preset.keeper?[.115,.13,.08]:[.075,.095,.055]);
    for(let f=0;f<4;f++) oval(elbow,preset.keeper?0xffedcc:skin,[(f-1.5)*.034,-.35,.038],[.021,.064,.036]);
    oval(elbow,preset.keeper?0xffedcc:skin,[side*.085,-.265,.06],[.04,.067,.04]);
    if(preset.keeper) {oval(elbow,0x203c5c,[0,-.19,.02],[.105,.035,.085]);oval(elbow,preset.accent,[0,-.28,.095],[.075,.06,.012]);}
    const leg=new THREE.Group();leg.position.set(side*.155,.71,0);root.add(leg);
    oval(leg,skin,[0,-.12,0],[.108,.18,.12]);
    const knee=new THREE.Group();knee.position.y=-.24;leg.add(knee);knees.push(knee);
    oval(knee,0xfff5df,[0,-.12,0],[.095,.17,.10]);
    oval(knee,preset.accent,[0,-.03,0],[.099,.025,.103]);
    mesh(knee,contour([[-.40,.015,.015,.04],[-.38,.12,.21,.075],[-.31,.125,.23,.09],[-.26,.10,.18,.04],[-.24,.05,.07]]),child?0xf1e3b9:0x26384c);
    oval(knee,0xffffff,[0,-.385,.08],[.12,.018,.21]);
    for(let lace=0;lace<3;lace++) curveMesh([[-.05,-.28,.13+lace*.025],[0,-.274,.14+lace*.025],[.05,-.28,.13+lace*.025]],.007,preset.accent,knee,false);
    joints[side<0?'leftArm':'rightArm']=arm;joints[side<0?'leftLeg':'rightLeg']=leg;
  }
  if(child)root.scale.setScalar(.87);
  root.userData={preset,joints,head,eyes,elbows,knees,shirt,neck};mergeRigidParts(root);return root;
}
export function poseCharacter(root,time,action='idle',progress=0) {
  const {joints,head,preset,eyes,elbows,knees}=root.userData;
  const p=THREE.MathUtils.clamp(progress,0,1), pulse=Math.sin(Math.PI*p);
  head.rotation.set(Math.sin(time*.9)*.015,Math.sin(time*.6)*.035,Math.sin(time*1.3)*.018);
  const blink=Math.pow(Math.max(0,Math.cos(time*1.7+2)),40);
  for(const eye of eyes)eye.scale.y=1-blink*.94;
  joints.leftArm.rotation.set(Math.sin(time*1.8)*.045,0,-.13-(preset.keeper?.25:0));
  joints.rightArm.rotation.set(-Math.sin(time*1.8)*.045,0,.13+(preset.keeper?.25:0));
  joints.leftLeg.rotation.x=0;joints.rightLeg.rotation.x=0;
  for(const elbow of elbows)elbow.rotation.x=-.12;
  for(const knee of knees)knee.rotation.x=0;
  if(action==='kick') {
    joints.rightLeg.rotation.x=-pulse*1.25;
    knees[1].rotation.x=Math.sin(Math.PI*Math.min(1,p*1.8))*.7;
    joints.leftArm.rotation.x=pulse*.4;joints.rightArm.rotation.x=-pulse*.4;
    head.rotation.x=pulse*.18;
  }
  if(action==='save') {
    joints.leftArm.rotation.z-=pulse*1.35;joints.rightArm.rotation.z+=pulse*1.35;
    for(const elbow of elbows)elbow.rotation.x=-pulse*.45;
    for(const knee of knees)knee.rotation.x=pulse*.3;
  }
  if(action==='celebrate') {
    joints.leftArm.rotation.z=-2.5;joints.rightArm.rotation.z=2.5;
    for(const elbow of elbows)elbow.rotation.x=-.45;
  }
}
