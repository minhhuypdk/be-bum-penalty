import * as THREE from '../vendor/three.module.js';

export function createStadium(scene) {
 const group=new THREE.Group();group.name='Bé Bum family stadium';scene.add(group);
 const material=(color)=>new THREE.MeshStandardMaterial({color,roughness:.83});
 const add=(geometry,color,position,rotation)=>{const m=new THREE.Mesh(geometry,material(color));m.position.set(...position);if(rotation)m.rotation.set(...rotation);m.receiveShadow=true;group.add(m);return m;};
 // Horseshoe stands leave the camera side open, with curved tiers behind the goal.
 for(let row=0;row<5;row++) {
  const tier=add(new THREE.RingGeometry(11+row*.85,11.85+row*.85,64,1,Math.PI*.07,Math.PI*.86),row%2?0x244d6a:0x335d76,[0,.65+row*.48,-1],[-Math.PI/2,0,0]);
  const radius=11.85+row*.85;
  const riser=add(new THREE.CylinderGeometry(radius,radius,.48,64,1,true,Math.PI*.57,Math.PI*.86),0x24465e,[0,.41+row*.48,-1]);
  riser.material.side=THREE.DoubleSide;
 }
 const bodies=new THREE.InstancedMesh(new THREE.CapsuleGeometry(.115,.22,3,6),material(0xffffff),300);
 const heads=new THREE.InstancedMesh(new THREE.SphereGeometry(.105,8,6),material(0xffffff),300);
 const matrix=new THREE.Object3D(),color=new THREE.Color();
 const shirts=[0xf3bd4d,0x4d8cce,0xe97978,0x8ecbbc,0xaf8be0];
 for(let i=0;i<300;i++) {
  const row=Math.floor(i/60),a=Math.PI*.09+(i%60)/59*Math.PI*.82,r=11.45+row*.85;
  const x=Math.cos(a)*r,z=-1-Math.sin(a)*r,y=.9+row*.48;
  matrix.position.set(x,y,z);matrix.rotation.set(0,Math.PI-a,0);matrix.scale.setScalar(.9+(i%7)*.035);matrix.updateMatrix();bodies.setMatrixAt(i,matrix.matrix);bodies.setColorAt(i,color.setHex(shirts[i%shirts.length]));
  matrix.position.y=y+.32;matrix.updateMatrix();heads.setMatrixAt(i,matrix.matrix);heads.setColorAt(i,color.setHex([0xf2c8a1,0xca926b,0x986848][i%3]));
 }
 group.add(bodies,heads);
 const bannerTextures=[];
 function banner(text,x,z,width=7,color='#ffc855') {
  const canvas=document.createElement('canvas');canvas.width=1024;canvas.height=160;const ctx=canvas.getContext('2d');
  ctx.fillStyle='#183b57';ctx.fillRect(0,0,1024,160);ctx.fillStyle=color;ctx.fillRect(0,0,1024,7);ctx.fillRect(0,153,1024,7);ctx.font='800 49px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(text,512,80,980);
  const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;bannerTextures.push(texture);
  const mesh=new THREE.Mesh(new THREE.PlaneGeometry(width,1.1),new THREE.MeshStandardMaterial({map:texture,roughness:.9,side:THREE.DoubleSide}));mesh.position.set(x,.67,z);group.add(mesh);return mesh;
 }
 banner('BÉ BUM · CÙNG NHAU TỎA SÁNG',0,-9,9);
 const left=banner('BA ƠI! CỐ LÊN!',-8,-7,5,'#bceadf');left.rotation.y=.5;
 const right=banner('BUM ƠI! CỐ LÊN!',8,-7,5,'#f9d59e');right.rotation.y=-.5;
 // Field markings: penalty area, spot and curved penalty arc.
 const points=[];const line=(a,b)=>points.push(...a,...b);
 line([-5,.012,-2.5],[-5,.012,4.8]);line([5,.012,-2.5],[5,.012,4.8]);line([-5,.012,4.8],[5,.012,4.8]);
 for(let i=0;i<48;i++){const a=i/48*Math.PI,b=(i+1)/48*Math.PI;line([Math.cos(a)*2.4,.012,4.8+Math.sin(a)*2.4],[Math.cos(b)*2.4,.012,4.8+Math.sin(b)*2.4]);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(points,3));group.add(new THREE.LineSegments(g,new THREE.LineBasicMaterial({color:0xe7f0d8,transparent:true,opacity:.8})));
 add(new THREE.CircleGeometry(.07,20),0xffffff,[0,.016,2],[-Math.PI/2,0,0]);
 for(const side of [-1,1]) {
  add(new THREE.CylinderGeometry(.05,.09,7,10),0x67808b,[side*10,3.4,-8]);
  const housing=add(new THREE.BoxGeometry(1.4,.45,.2),0x25465d,[side*10,6.8,-8]);housing.rotation.y=-side*.25;
  for(let i=0;i<4;i++) {const lamp=new THREE.Mesh(new THREE.CircleGeometry(.13,12),new THREE.MeshBasicMaterial({color:0xfff3d3}));lamp.position.set(side*10+(i-1.5)*.3,6.8,-7.88);group.add(lamp);}
 }
 const flags=[];
 for(const side of [-1,1]) {
  add(new THREE.CylinderGeometry(.018,.018,2,8),0xffffff,[side*5,1,4.8]);
  const flag=add(new THREE.PlaneGeometry(.5,.33),0xffce66,[side*5+.24,1.8,4.8]);flag.material.side=THREE.DoubleSide;flags.push(flag);
 }
 return {group,update(time){for(let i=0;i<flags.length;i++)flags[i].rotation.y=Math.sin(time*2+i)*.22;}};
}
