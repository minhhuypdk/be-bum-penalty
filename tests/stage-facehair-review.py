import pathlib
p=pathlib.Path('graphics/showcase.js');s=p.read_text()
old="id.startsWith('bum')?1.9:2.2";assert old in s;s=s.replace(old,'2.2')
old="state.version==='bum07'?record.height*.10:0";assert old in s;s=s.replace(old,"['bum07','local'].includes(state.version)?record.height*.10:0")
api="""  setStudyExpression(mode){active.model.traverse(o=>{if(!o.morphTargetDictionary)return;for(const[n,i]of Object.entries(o.morphTargetDictionary))if(n.startsWith('FH_'))o.morphTargetInfluences[i]=(mode==='smile'&&n==='FH_Smile') ? .6 : (mode==='blink'&&n==='FH_Blink') ? 1 : 0;});needsRender=true;},
  getStudyTargets(){const result=[];active.model.traverse(o=>{if(o.morphTargetDictionary)result.push({name:o.name,names:Object.keys(o.morphTargetDictionary),finite:Object.values(o.geometry.morphAttributes).flat().every(a=>Array.from(a.array).every(Number.isFinite))});});return result;},
"""
assert '  getMetrics:reportBase,' in s;s=s.replace('  getMetrics:reportBase,',api+'  getMetrics:reportBase,');p.write_text(s)
# This patches ONLY the ephemeral CI checkout. It is NOT a shared Showcase commit or deployment.
