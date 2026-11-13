"""Create isolated review checkout. Never patch tracked Showcase or C/P2 files."""
import pathlib,shutil,sys
root=pathlib.Path(__file__).resolve().parents[1];out=pathlib.Path(sys.argv[1]).resolve();assets=pathlib.Path(sys.argv[2]).resolve()
assert root not in out.parents or 'artifacts' in out.parts
out.mkdir(parents=True,exist_ok=True)
for name in ['graphics','vendor']:shutil.copytree(root/name,out/name,dirs_exist_ok=True)
shutil.copytree(assets,out/'graphics/models/bum07-p31',dirs_exist_ok=True)
s=(root/'graphics/showcase.js').read_text().replace(' updateFollowing();controls.update();',' if(!window.__p31LockView)updateFollowing();controls.update();').replace("id.startsWith('bum')?1.9:2.2",'2.2').replace("state.version==='bum07'?record.height*.10:0","['bum07','local'].includes(state.version)?record.height*.10:0")
api="""  setMatchedView(v){window.__p31LockView=true;controls.enableDamping=false;turntable.rotation.y=v.angle;controls.target.fromArray(v.target);camera.position.fromArray(v.camera);controls.update();needsRender=true;},
  setStudyExpression(mode,value=1){active.model.traverse(o=>{if(!o.morphTargetDictionary)return;for(const[n,i]of Object.entries(o.morphTargetDictionary))if(n.startsWith('FH_'))o.morphTargetInfluences[i]=n===('FH_'+mode)?value:0;});needsRender=true;},
  getStudyTargets(){const result=[];active.model.traverse(o=>{if(o.morphTargetDictionary)result.push({name:o.name,names:Object.keys(o.morphTargetDictionary),finite:Object.values(o.geometry.morphAttributes).flat().every(a=>Array.from(a.array).every(Number.isFinite))});});return result;},
"""
assert '  getMetrics:reportBase,' in s;s=s.replace('  getMetrics:reportBase,',api+'  getMetrics:reportBase,');(out/'graphics/showcase.js').write_text(s)
# Canonical P2 GLB path provided separately, byte verified by test.
if len(sys.argv)>3:
 dest=out/'graphics/models/p2-original.glb';shutil.copy2(sys.argv[3],dest)
print('ISOLATED_REVIEW_STAGED',out)
