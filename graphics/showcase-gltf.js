import * as THREE from '../vendor/three.module.js';
import {GLTFLoader} from '../vendor/addons/GLTFLoader.js';

const aliases={idle:['idle','standing','stand'],run:['run','running','jog'],kick:['kick','soccerkick','footballkick'],save:['save','dive','goalkeeperdive','goalkeepersave'],celebrate:['celebrate','celebration','victory','cheer']};
const normalized=s=>s.toLowerCase().replace(/[^a-z]/g,'');
export async function loadLocalGLB(file,height=2.2){
 if(!file.name.toLowerCase().endsWith('.glb'))throw new Error('Hãy chọn GLB có texture nhúng trong file.');
 if(file.size>40*1024*1024)throw new Error('File vượt 40 MB. Hãy tối ưu texture và geometry trước khi duyệt trên iPhone.');
 const buffer=await file.arrayBuffer(),view=new DataView(buffer);
 if(view.byteLength<20||view.getUint32(0,true)!==0x46546c67||view.getUint32(4,true)!==2)throw new Error('File không phải GLB 2.0 hợp lệ.');
 // Reject external URLs: importing an art file never makes requests to other services.
 const jsonLength=view.getUint32(12,true);if(jsonLength>buffer.byteLength-20||view.getUint32(16,true)!==0x4e4f534a)throw new Error('JSON chunk của GLB không hợp lệ.');const json=JSON.parse(new TextDecoder().decode(new Uint8Array(buffer,20,jsonLength)));
 for(const item of [...(json.buffers||[]),...(json.images||[])])if(item.uri&&!item.uri.startsWith('data:'))throw new Error('GLB cần nhúng buffer và texture; không cho phép URL bên ngoài.');
 if((json.extensionsRequired||[]).some(x=>['KHR_draco_mesh_compression','EXT_meshopt_compression','KHR_texture_basisu'].includes(x)))throw new Error('Bản duyệt này cần GLB không nén Draco/Meshopt/KTX2. Hãy xuất bản tương thích hoặc cấu hình decoder trong pipeline asset.');
 const gltf=await new Promise((resolve,reject)=>new GLTFLoader().parse(buffer,'',resolve,reject));
 const object=gltf.scene;
 object.traverse(part=>{if(part.isMesh){part.castShadow=true;part.receiveShadow=true;}});
 const mixer=new THREE.AnimationMixer(object),clips={};
 for(const [action,names]of Object.entries(aliases)){
  const clip=gltf.animations.find(c=>names.some(name=>normalized(c.name)===name))||gltf.animations.find(c=>names.some(name=>normalized(c.name).includes(name)));
  if(clip)clips[action]=mixer.clipAction(clip);
 }
 let current=clips.idle||null;
 // Evaluate the first real pose before measuring/framing the model. This also
 // gives paused review loads a valid stance rather than a transient bind pose.
 if(current){current.reset().setLoop(THREE.LoopRepeat,Infinity).play();mixer.update(0);}
 object.updateMatrixWorld(true);const box=new THREE.Box3().setFromObject(object),size=box.getSize(new THREE.Vector3());
 if(!Number.isFinite(size.y)||size.y<.01)throw new Error('Mô hình không có chiều cao hợp lệ.');
 object.scale.multiplyScalar(height/size.y);
 return {object,mixer,clips,available:Object.keys(clips),name:file.name,
  play(action){if(current===clips[action])return;current?.fadeOut(.18);current=clips[action]||null;if(current)current.reset().setLoop(THREE.LoopRepeat,Infinity).fadeIn(.18).play();},
  dispose(){mixer.stopAllAction();mixer.uncacheRoot(object);object.traverse(p=>{if(p.isMesh){p.geometry.dispose();for(const m of Array.isArray(p.material)?p.material:[p.material]){for(const value of Object.values(m))if(value?.isTexture)value.dispose();m.dispose();}}});}
 };
}
