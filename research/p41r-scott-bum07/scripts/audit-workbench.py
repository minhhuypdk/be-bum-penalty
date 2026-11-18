"""Read back the saved workbench; no edits or saving. Native rig remains editable."""
import bpy,json,sys,hashlib
from pathlib import Path
out=Path(sys.argv[sys.argv.index('--')+1]);rig=bpy.data.objects['P41_ScottRig_370'];body=bpy.data.objects['P41_BodyFaceEyes'];run=bpy.data.objects['P41_BodyFaceEyes_Runtime']
keys=lambda o:list(o.data.shape_keys.key_blocks.keys())
native=keys(body);runtime=keys(run)
assert len(rig.data.bones)==370
assert all('P41R_CanthusContact_'+s in native for s in ['L','R'])
assert all(k in runtime for k in ['Basis','FH_Blink25','FH_Blink50','FH_Blink75','FH_Blink','FH_Smile50','FH_Smile'])
assert not any(k.startswith('P41R_Canthus')for k in runtime)
assert any(m.type=='ARMATURE'and m.use_deform_preserve_volume for m in body.modifiers)
source=Path('research/p41-scott-bum07/source/scott-original.blend');assert hashlib.sha256(source.read_bytes()).hexdigest()=='95b9848fd0c4a1c9ee94a2ae3a9f6136af71c97256ef63ab7a37017470846568'
r={'result':'PASS','savedBlenderOpened':True,'nativeJoints':len(rig.data.bones),'nativeBodyKeys':native,'runtimeBodyKeys':runtime,'nativeCorrectiveDrivers':len(body.data.shape_keys.animation_data.drivers),'nativePreserveVolume':True,'sourceUnchanged':True,'fileSha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'scope':'Saved native rig/correctives and exact runtime keys verified; no editing or saving'}
(out/'workbench-audit.json').write_text(json.dumps(r,indent=2)+'\n');print('WORKBENCH_PASS')
