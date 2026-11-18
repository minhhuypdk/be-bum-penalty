from pathlib import Path
import sys,subprocess,shutil
root=Path(__file__).resolve().parents[3];out=Path(sys.argv[1]).resolve();assets=Path(sys.argv[2]).resolve();original=Path(sys.argv[3]).resolve()
assert root not in out.parents or 'artifacts'in out.parts
subprocess.run([sys.executable,str(root/'research/p4-character-assets/scripts/prepare-preview.py'),str(out),str(original)],cwd=root,check=True)
shutil.copy2(assets/'scott-bum07-p41r-prototype.glb',out/'graphics/models/scott-bum-p41r.glb');p=out/'graphics/showcase.js';s=p.read_text().replace("mode==='body'?1.1:1.80","mode==='body'?1.1:1.78").replace("mode==='close'?1.25:2.0","mode==='close'?1.6:2.0")
api="""  p41Expression(mode,value){active.model.traverse(o=>{if(!o.morphTargetDictionary)return;const d=o.morphTargetDictionary,w=o.morphTargetInfluences;for(const[n,i]of Object.entries(d))if(n.startsWith('FH_'))w[i]=0;const names=mode==='Blink'?['Basis','FH_Blink25','FH_Blink50','FH_Blink75','FH_Blink']:mode==='Smile'?['Basis','FH_Smile50','FH_Smile']:['Basis'];if(names.length===1)return;const pos=Math.min(names.length-1,value*(names.length-1)),lo=Math.min(names.length-2,Math.floor(pos)),t=pos-lo;if(lo>0&&d[names[lo]]!==undefined)w[d[names[lo]]]=1-t;if(d[names[lo+1]]!==undefined)w[d[names[lo+1]]]=t;});needsRender=true;},
  p41EyeID(){const saved=[],shadow=renderer.shadowMap.enabled,red=new THREE.MeshBasicMaterial({color:0xff0000,toneMapped:false,fog:false}),green=new THREE.MeshBasicMaterial({color:0x00ff00,toneMapped:false,fog:false});let eyes=0,skins=0;scene.traverse(o=>{if(!o.isMesh)return;saved.push([o,o.material,o.visible]);if(!active.model.getObjectById(o.id)){o.visible=false;return;}const mats=Array.isArray(o.material)?o.material:[o.material];let visible=false;o.material=mats.map(m=>{const name=m.name.toLowerCase();if(/p41_sclera|p41_iris|p41_pupil/.test(name)){eyes++;visible=true;return red;}if(name.includes('p41_scottskinatlas')){skins++;visible=true;return green;}return m;});if(!Array.isArray(saved[saved.length-1][1]))o.material=o.material[0];o.visible=visible;});try{renderer.shadowMap.enabled=false;renderer.render(scene,camera);const c=document.createElement('canvas');c.width=renderer.domElement.width;c.height=renderer.domElement.height;const x=c.getContext('2d');x.drawImage(renderer.domElement,0,0);let eyePixels=0;const a=x.getImageData(0,0,c.width,c.height).data;for(let i=0;i<a.length;i+=4)if(a[i]>180&&a[i+1]<40&&a[i+2]<40)eyePixels++;return{eyePixels,eyes,skins,png:c.toDataURL('image/png').split(',')[1]};}finally{for(const[o,m,v]of saved){o.material=m;o.visible=v;}renderer.shadowMap.enabled=shadow;red.dispose();green.dispose();renderer.render(scene,camera);needsRender=true;}},
"""
assert '  getMetrics:reportBase,'in s;s=s.replace('  getMetrics:reportBase,',api+'  getMetrics:reportBase,');p.write_text(s);print('P41_ISOLATED_REVIEW_READY')

shutil.copy2(root/'research/p41-scott-bum07/assets/scott-bum07-p41-prototype.glb',out/'graphics/models/scott-bum-p41.glb')
shutil.copy2(root/'research/p41r-scott-bum07/scripts/full-influence-skinning.js',out/'graphics/full-influence-skinning.js')
p=out/'graphics/showcase.js';s=p.read_text();s="import {installFullInfluenceSkinning} from './full-influence-skinning.js';\n"+s
s=s.replace("record=setupRecord(id,asset.object,asset);", "record=setupRecord(id,asset.object,asset);if(file.name.includes('p41r'))installFullInfluenceSkinning(asset.object);")
s=s.replace('return red;', 'return o.userData.p41rSkinMaterial?o.userData.p41rSkinMaterial(red):red;').replace('return green;', 'return o.userData.p41rSkinMaterial?o.userData.p41rSkinMaterial(green):green;')
p.write_text(s)
p=out/'vendor/addons/GLTFLoader.js';s=p.read_text();assert 'mesh.normalizeSkinWeights();'in s;s=s.replace('mesh.normalizeSkinWeights();','/* P41R isolated study: preserve ALL weight-set sums, adapter handles full normalization. */');p.write_text(s)

shutil.copy2(root/'research/p41r-scott-bum07/scripts/gpu-deformation-probe.js',out/'graphics/gpu-deformation-probe.js')
if (assets/'gpu-pose-fixture.json').exists():shutil.copy2(assets/'gpu-pose-fixture.json',out/'graphics/models/gpu-pose-fixture.json')
p=out/'graphics/showcase.js';s=p.read_text();s="import {applyNativePose,readbackNativeDeformation} from './gpu-deformation-probe.js';\n"+s
s=s.replace('  getMetrics:reportBase,',"  p41rApplyPose(fixture,index){const n=applyNativePose(active.model,fixture,index);scene.updateMatrixWorld(true);needsRender=true;return n;},\n  p41rGPU(fixture,index){scene.updateMatrixWorld(true);return readbackNativeDeformation(active.model,renderer,camera,fixture,index);},\n  getMetrics:reportBase,")
p.write_text(s)

p=out/'graphics/showcase.js';s=p.read_text();s=s.replace('for(const[o,m,v]of saved){o.material=m;o.visible=v;}',"for(const[o,m,v]of saved){const old=Array.isArray(m)?m:[m];for(const temp of(Array.isArray(o.material)?o.material:[o.material]))if(temp!==red&&temp!==green&&!old.includes(temp))temp.dispose();o.material=m;o.visible=v;}");p.write_text(s)
p=out/'graphics/showcase-gltf.js';s=p.read_text();s="import {disposeFullInfluenceSkinning} from './full-influence-skinning.js';\n"+s;s=s.replace('dispose(){mixer.stopAllAction();','dispose(){disposeFullInfluenceSkinning(object);mixer.stopAllAction();');p.write_text(s)
