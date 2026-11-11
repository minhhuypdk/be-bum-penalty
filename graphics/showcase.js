import * as THREE from '../vendor/three.module.js';
import {OrbitControls} from '../vendor/addons/OrbitControls.js';
import {createCharacter} from './characters.js';
import {CLIPS,animateShowcase} from './showcase-motion.js';
import {loadLocalGLB} from './showcase-gltf.js';

const $=id=>document.getElementById(id),host=$('stage');
const presets={
 'ba-player':{person:'BA',role:'CẦU THỦ SÚT PHẠT',number:'10'},'ba-keeper':{person:'BA',role:'THỦ MÔN',number:'10'},
 'bum-player':{person:'BUM',role:'CẦU THỦ SÚT PHẠT',number:'07'},'bum-keeper':{person:'BUM',role:'THỦ MÔN',number:'07'},
};
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const state={character:'ba-player',action:'idle',focus:'body',quality:'cinema',paused:reduced,autoRotate:false,time:0};
const records=new Map(),overrides=new Map();
let renderer,controls,active,previous=0,needsRender=true,lastToast,benchmark=null,lastReport=null,frameTimes=[],draws=0,lastFps=0;
const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(35,1,.03,60),turntable=new THREE.Group();
scene.background=new THREE.Color(0x14263b);scene.fog=new THREE.FogExp2(0x14263b,.045);scene.add(turntable);
const target=new THREE.Vector3(),oldTarget=new THREE.Vector3(),deltaTarget=new THREE.Vector3();
function toast(message){$('toast').textContent=message;$('toast').classList.add('visible');clearTimeout(lastToast);lastToast=setTimeout(()=>$('toast').classList.remove('visible'),3500)}
function makeEnvironment(){
 const canvas=document.createElement('canvas');canvas.width=512;canvas.height=256;const c=canvas.getContext('2d');
 const base=c.createLinearGradient(0,0,0,256);base.addColorStop(0,'#b8c8dc');base.addColorStop(.48,'#2a3b51');base.addColorStop(1,'#122033');c.fillStyle=base;c.fillRect(0,0,512,256);
 for(const[x,y,w,h,color]of[[90,25,65,110,'#fff1d9'],[330,50,28,140,'#c4e4ff'],[190,15,110,35,'#ffffff']]){c.fillStyle=color;c.fillRect(x,y,w,h)}
 const texture=new THREE.CanvasTexture(canvas);texture.mapping=THREE.EquirectangularReflectionMapping;texture.colorSpace=THREE.SRGBColorSpace;
 const pmrem=new THREE.PMREMGenerator(renderer),environment=pmrem.fromEquirectangular(texture);scene.environment=environment.texture;scene.environmentIntensity=.48;texture.dispose();pmrem.dispose();
}
const key=new THREE.DirectionalLight(0xffe5c5,3.2);key.position.set(-3.4,5,4.5);key.castShadow=true;key.shadow.normalBias=.025;key.shadow.bias=-.0001;key.shadow.radius=3;
Object.assign(key.shadow.camera,{near:.1,far:18,left:-4,right:4,top:4,bottom:-2});scene.add(key);
scene.add(new THREE.HemisphereLight(0xdbefff,0x56494b,.9));
const rim=new THREE.DirectionalLight(0x9ecbff,2);rim.position.set(3,3.5,-3);scene.add(rim);
const fill=new THREE.DirectionalLight(0xffeed8,.5);fill.position.set(4,2,4);scene.add(fill);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(60,60),new THREE.MeshStandardMaterial({color:0x1b3046,roughness:.87}));floor.rotation.x=-Math.PI/2;floor.position.y=-.07;floor.receiveShadow=true;scene.add(floor);
const platform=new THREE.Mesh(new THREE.CylinderGeometry(2.5,2.58,.1,96),new THREE.MeshStandardMaterial({color:0x253d54,metalness:.15,roughness:.6}));platform.position.y=-.06;platform.receiveShadow=true;scene.add(platform);
const trim=new THREE.Mesh(new THREE.TorusGeometry(2.52,.008,6,96),new THREE.MeshStandardMaterial({color:0xb98d4b,metalness:.6,roughness:.35}));trim.rotation.x=Math.PI/2;trim.position.y=-.035;scene.add(trim);
function ballTexture(){const canvas=document.createElement('canvas');canvas.width=512;canvas.height=256;const c=canvas.getContext('2d');c.fillStyle='#f8f5e9';c.fillRect(0,0,512,256);c.strokeStyle='#b7bdbe';c.lineWidth=1.5;
 for(let y=0;y<4;y++)for(let x=0;x<8;x++){const cx=x*64+(y%2?32:0),cy=y*64+32;c.beginPath();for(let i=0;i<5;i++){const a=i*Math.PI*2/5-Math.PI/2;c.lineTo(cx+Math.cos(a)*17,cy+Math.sin(a)*17)}c.closePath();c.fillStyle='#203343';c.fill();c.stroke()}
 const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;return texture;}
const ball=new THREE.Mesh(new THREE.SphereGeometry(.155,28,20),new THREE.MeshStandardMaterial({map:ballTexture(),roughness:.45}));ball.castShadow=true;ball.visible=false;turntable.add(ball);

function setupRecord(id,model,asset=null){
 model.updateMatrixWorld(true);const box=new THREE.Box3().setFromObject(model),size=box.getSize(new THREE.Vector3()),center=box.getCenter(new THREE.Vector3());
 const rig=new THREE.Group(),centered=new THREE.Group(),pivot=size.y/2;
 centered.position.set(-center.x,-box.min.y-pivot,-center.z);centered.add(model);rig.position.y=pivot;rig.add(centered);turntable.add(rig);rig.visible=false;
 return{id,model,asset,rig,centered,height:size.y,width:size.x,depth:size.z,pivot};
}
function getRecord(id){if(overrides.has(id))return overrides.get(id);if(!records.has(id))records.set(id,setupRecord(id,createCharacter(id,{detail:'showcase'})));return records.get(id)}
function headTarget(record,out){
 if(record.model.userData.head)return record.model.userData.head.getWorldPosition(out).add(new THREE.Vector3(0,record.height*.018,0));
 let head=null;record.model.traverse(p=>{if(!head&&/(^head$|mixamorighead|bip.*head)/i.test(p.name))head=p});
 return head?head.getWorldPosition(out):record.rig.localToWorld(out.set(0,record.height*.32,0));
}
function getTarget(){
 active.rig.updateWorldMatrix(true,true);
 if(state.focus==='face')headTarget(active,target);
 else{active.rig.getWorldPosition(target);target.y=active.height*.43;}
 return target;
}
function updateFollowing(){
 oldTarget.copy(controls.target);getTarget();deltaTarget.copy(target).sub(oldTarget);
 controls.target.copy(target);camera.position.add(deltaTarget);
}
function frame(mode=state.focus){
 state.focus=mode;getTarget();const v=THREE.MathUtils.degToRad(camera.fov),h=2*Math.atan(Math.tan(v/2)*camera.aspect),angle=Math.min(v,h);
 const radius=mode==='face'?active.height*.23:Math.max(active.height,active.width,active.depth)*.64;
 const distance=radius/Math.sin(angle/2)*(mode==='face'?1.03:1);
 const direction=camera.position.clone().sub(controls.target).normalize();if(!Number.isFinite(direction.x)||direction.lengthSq()<.1)direction.set(.12,.07,1).normalize();
 controls.target.copy(target);camera.position.copy(target).addScaledVector(direction,distance);controls.update();needsRender=true;
 $('full-body').classList.toggle('active',mode==='body');$('full-body').setAttribute('aria-pressed',String(mode==='body'));$('face').classList.toggle('active',mode==='face');$('face').setAttribute('aria-pressed',String(mode==='face'));
}
function cancelBenchmark(reason){if(!benchmark)return;const b=benchmark;benchmark=null;b.reject(new Error(reason));$('benchmark-status').textContent=reason;}
function refreshMotionOptions(){
 for(const option of $('pose').options){option.disabled=!!active.asset&&!active.asset.available.includes(option.value);option.textContent=(option.index+1).toString().padStart(2,'0')+' · '+CLIPS[option.value].name+(option.disabled?' (chưa có clip)':'')}
 if(active.asset&&!active.asset.available.includes(state.action)){state.action=active.asset.available[0]||'idle';$('pose').value=state.action}
}
function selectCharacter(id){
 if(!presets[id])return;cancelBenchmark('Đã đổi nhân vật; hãy đo lại.');if(active)active.rig.visible=false;
 state.character=id;state.time=0;active=getRecord(id);active.rig.visible=true;ball.visible=false;
 $('character').value=id;const p=presets[id];$('character-name').innerHTML=p.person+' <span>/ '+p.number+'</span>';$('role-label').textContent=p.role;
 for(const button of document.querySelectorAll('[data-character]')){const selected=button.dataset.character===id;button.classList.toggle('selected',selected);button.setAttribute('aria-pressed',String(selected))}
 refreshMotionOptions();if(active.asset)active.asset.play(state.action);frame(state.focus);needsRender=true;
}
function setAction(action){if(!CLIPS[action])return;if(active.asset&&!active.asset.available.includes(action)){toast('Mô hình này chưa có clip '+CLIPS[action].name);return}
 cancelBenchmark('Đã đổi chuyển động; hãy đo lại.');state.action=action;state.time=0;$('pose').value=action;active.asset?.play(action);needsRender=true;
}
function setPaused(paused){state.paused=paused;$('pause').textContent=paused?'▶':'Ⅱ';$('pause').setAttribute('aria-pressed',String(paused));$('pause').setAttribute('aria-label',paused?'Phát chuyển động':'Tạm dừng chuyển động');needsRender=true;}
function setQuality(quality){
 cancelBenchmark('Đã đổi chất lượng; hãy đo lại.');state.quality=quality;$('quality').value=quality;
 renderer.setPixelRatio(Math.min(devicePixelRatio,quality==='cinema'?3:2));const size=quality==='cinema'?2048:1024;
 key.shadow.mapSize.set(size,size);if(key.shadow.map){key.shadow.map.dispose();key.shadow.map=null;}resize();needsRender=true;
}
function resize(){const width=host.clientWidth,height=host.clientHeight;if(!width||!height)return;renderer.setSize(width,height);camera.aspect=width/height;camera.updateProjectionMatrix();needsRender=true;}
function gpuInfo(){const gl=renderer.getContext(),extension=gl.getExtension('WEBGL_debug_renderer_info');return extension?gl.getParameter(extension.UNMASKED_RENDERER_WEBGL):'Không có thông tin GPU công khai'}
function reportBase(){const size=renderer.getDrawingBufferSize(new THREE.Vector2());return{character:state.character,action:state.action,source:active.asset?'local GLB':'BA/BUM authored procedural model',quality:state.quality,focus:state.focus,paused:state.paused,viewport:{width:host.clientWidth,height:host.clientHeight},renderPixels:{width:size.x,height:size.y},devicePixelRatio,pixelRatio:renderer.getPixelRatio(),shadowMap:key.shadow.mapSize.x,userAgent:navigator.userAgent,gpu:gpuInfo(),triangles:renderer.info.render.triangles,drawCalls:renderer.info.render.calls,measuredOnPhysicalIPhone:/iPhone/.test(navigator.userAgent)&&!/(Headless|Playwright)/i.test(navigator.userAgent)?'user agent only; hardware not independently verified':false};}
function measure(seconds=8){
 if(benchmark)return Promise.reject(new Error('Đang có phép đo.'));if(document.hidden)return Promise.reject(new Error('Hãy mở tab để đo FPS.'));
 return new Promise((resolve,reject)=>{benchmark={start:performance.now(),warmup:1000,duration:seconds*1000,frames:[],last:0,resolve,reject,config:reportBase()};$('benchmark-status').textContent='Đang làm nóng rồi đo '+seconds+' giây…';needsRender=true;});
}
function tickBenchmark(now){
 if(!benchmark)return;const b=benchmark;if(now-b.start<b.warmup)return;
 if(!b.last)b.sampleStart=now;else b.frames.push(now-b.last);b.last=now;
 if(now-b.sampleStart<b.duration||!b.frames.length)return;
 const ms=b.frames.reduce((a,v)=>a+v,0),sorted=[...b.frames].sort((a,c)=>a-c),percentile=q=>sorted[Math.min(sorted.length-1,Math.floor(sorted.length*q))]||0;
 const report={...b.config,measuredAt:new Date().toISOString(),durationSeconds:Number((ms/1000).toFixed(3)),renderedFrames:b.frames.length,averageFps:Number((b.frames.length*1000/ms).toFixed(2)),medianFrameMs:Number(percentile(.5).toFixed(2)),p95FrameMs:Number(percentile(.95).toFixed(2)),note:'FPS thực đo trên môi trường ghi ở userAgent/GPU. Không dùng số desktop/emulator làm cam kết FPS Safari iPhone.'};
 benchmark=null;lastReport=report;$('performance-report').textContent=JSON.stringify(report,null,2);$('benchmark-status').textContent='Đã đo xong · '+report.averageFps+' FPS';b.resolve(report);
}
async function capture(download=true){renderer.render(scene,camera);const blob=await new Promise(resolve=>renderer.domElement.toBlob(resolve,'image/png'));if(!blob)throw new Error('Chưa xuất được render.');if(download){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`be-bum-${state.character}-${state.action}-${state.focus}.png`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1500);toast('Đã xuất ảnh render 3D.')}return blob;}
function animate(now){
 if(!previous)previous=now;const dt=Math.min(.25,(now-previous)/1000);previous=now;
 if(document.hidden||renderer.getContext().isContextLost()||!active)return;
 if(!state.paused)state.time+=dt;
 if(active.asset){if(!state.paused)active.asset.mixer.update(dt);ball.visible=false;}else animateShowcase(active.model,active.rig,state.action,state.time,active.pivot,ball);
 if(state.autoRotate&&!state.paused){turntable.rotation.y+=dt*.23;needsRender=true;}
 updateFollowing();controls.update();
 const duration=CLIPS[state.action].duration;$('timeline').value=String(Math.floor((state.time%duration)/duration*1000));
 if(!state.paused||needsRender||benchmark){renderer.render(scene,camera);draws++;frameTimes.push(now);if(frameTimes.length>240)frameTimes.shift();tickBenchmark(now);needsRender=false;}
 if(now-lastFps>1000){const recent=frameTimes.filter(t=>t>=now-1000);$('live-fps').textContent=state.paused&&!benchmark?'TẠM DỪNG':recent.length+' FPS';lastFps=now;}
}
async function importGLB(file){
 $('asset-status').textContent='Đang đọc mô hình…';const id=state.character;
 try{const asset=await loadLocalGLB(file,id.startsWith('bum')?1.9:2.2),record=setupRecord(id,asset.object,asset);if(overrides.has(id)){const old=overrides.get(id);turntable.remove(old.rig);old.asset.dispose();}
  overrides.set(id,record);selectCharacter(id);$('asset-status').textContent=file.name+' · '+(asset.available.map(a=>CLIPS[a].name).join(', ')||'Chưa có animation clip');toast('Đã mở GLB trên thiết bị này.');
 }catch(error){$('asset-status').textContent=error.message;throw error}
}
function resetGLB(){const record=overrides.get(state.character);if(!record)return;turntable.remove(record.rig);record.asset.dispose();overrides.delete(state.character);selectCharacter(state.character);$('asset-status').textContent='Đã trở lại tạo hình BA/BUM.';}
function bind(){
 $('character').onchange=e=>selectCharacter(e.target.value);for(const button of document.querySelectorAll('[data-character]'))button.onclick=()=>selectCharacter(button.dataset.character);
 $('pose').onchange=e=>setAction(e.target.value);$('pause').onclick=()=>setPaused(!state.paused);
 $('full-body').onclick=()=>frame('body');$('face').onclick=()=>frame('face');
 const zoom=factor=>{cancelBenchmark('Đã đổi mức phóng; hãy đo lại.');camera.position.sub(controls.target).multiplyScalar(factor).add(controls.target);controls.update();needsRender=true;};
 $('zoom-in').onclick=()=>zoom(.84);$('zoom-out').onclick=()=>zoom(1.19);
 $('rotate').onclick=()=>{state.autoRotate=!state.autoRotate;$('rotate').setAttribute('aria-pressed',String(state.autoRotate));$('rotate').textContent=state.autoRotate?'↻ Dừng xoay':'↻ Xoay 360°';needsRender=true;};
 $('quality').onchange=e=>setQuality(e.target.value);
 $('timeline').oninput=e=>{setPaused(true);state.time=Number(e.target.value)/1000*CLIPS[state.action].duration;if(active.asset)active.asset.mixer.setTime(state.time);needsRender=true;};
 $('capture').onclick=()=>capture().catch(e=>toast(e.message));
 $('performance').onclick=()=>{$('performance-dialog').showModal();$('performance-report').textContent='';measure().catch(e=>$('benchmark-status').textContent=e.message)};
 $('copy-performance').onclick=async()=>{if(!lastReport)return;try{await navigator.clipboard.writeText(JSON.stringify(lastReport,null,2));toast('Đã sao chép số đo FPS.')}catch{toast('Hãy chọn và sao chép nội dung báo cáo.')}};
 $('asset-open').onclick=()=>$('asset-dialog').showModal();$('asset-file').onchange=e=>{if(e.target.files[0])importGLB(e.target.files[0]).catch(()=>{});};$('asset-reset').onclick=resetGLB;
 for(const button of document.querySelectorAll('[data-close]'))button.onclick=()=>$(button.dataset.close).close();
 renderer.domElement.tabIndex=0;renderer.domElement.setAttribute('aria-label','Nhân vật 3D. Kéo để xoay, chụm hai ngón để phóng to.');
 renderer.domElement.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();camera.position.sub(controls.target).applyAxisAngle(new THREE.Vector3(0,1,0),e.key==='ArrowLeft'?-.18:.18).add(controls.target);controls.update();needsRender=true;}if(e.key==='+')zoom(.84);if(e.key==='-')zoom(1.19);});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)cancelBenchmark('Phép đo dừng vì tab đã ẩn.');previous=0;needsRender=true;});
}
try{
 renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,powerPreference:'high-performance'});renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.08;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 host.append(renderer.domElement);camera.position.set(.6,1.45,5.4);controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.09;controls.enablePan=false;controls.minDistance=.55;controls.maxDistance=14;controls.minPolarAngle=.2;controls.maxPolarAngle=Math.PI*.53;controls.addEventListener('change',()=>needsRender=true);
 makeEnvironment();setQuality('cinema');selectCharacter('ba-player');setPaused(state.paused);bind();
 new ResizeObserver(()=>{resize();frame(state.focus)}).observe(host);
 renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();cancelBenchmark('WebGL đã mất ngữ cảnh; hãy đo lại sau khi phục hồi.');$('unavailable').hidden=false;});
 renderer.domElement.addEventListener('webglcontextrestored',()=>{$('unavailable').hidden=true;needsRender=true;});
 renderer.setAnimationLoop(animate);$('loading').hidden=true;document.body.dataset.ready='true';
 for(const el of document.querySelectorAll('[data-portrait]')){const img=new Image();img.alt='';img.src=new URL('./showcase-assets/'+el.dataset.portrait+'.png',import.meta.url);img.onload=()=>el.replaceChildren(img);img.onerror=()=>{};}
 window.showcase={state,selectCharacter,setAction,setPaused,setQuality,frame,measure,capture,importGLB,resetGLB,
  setAngle(angle){turntable.rotation.y=angle;needsRender=true;},
  getMetrics:reportBase,
  getModelSummary(){return{height:active.height,source:active.asset?'glb':'procedural',available:active.asset?active.asset.available:Object.keys(CLIPS),position:active.rig.position.toArray(),rotation:active.rig.rotation.toArray().slice(0,3),geometryFinite:(()=>{let finite=true;active.model.traverse(p=>{if(p.isMesh)for(const v of p.geometry.attributes.position.array)if(!Number.isFinite(v))finite=false;});return finite;})()};}
 };
}catch(error){$('loading').hidden=true;$('unavailable').hidden=false;$('unavailable').textContent='Không khởi tạo được phòng trưng bày: '+error.message;document.body.dataset.error=error.message;console.error(error);}
