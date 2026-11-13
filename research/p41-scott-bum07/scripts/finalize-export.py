"""Add exact source-vertex provenance and save runtime morphs for independent GLB checks.
Only touches new P4.1 workbench/export, never Scott's source file."""
import bpy,json,hashlib,sys
from pathlib import Path
out=Path(sys.argv[sys.argv.index('--')+1]);r=json.loads((out/'build-report.json').read_text());rig=bpy.data.objects['P41_ScottRig_370'];runtime=list(bpy.data.collections['02_RUNTIME_COMPENSATED'].objects)
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
for o in bpy.context.scene.objects:o.select_set(False)
for o in runtime:
 for color in list(o.data.color_attributes):o.data.color_attributes.remove(color)
 attr=o.data.attributes.get('_P41_SOURCE_ID')or o.data.attributes.new(name='_P41_SOURCE_ID',type='FLOAT',domain='POINT')
 for v in o.data.vertices:attr.data[v.index].value=float(v.index)
 o.select_set(True)
rig.select_set(True);bpy.context.view_layer.objects.active=rig
props=bpy.ops.export_scene.gltf.get_rna_type().properties;extra={}
if 'export_rest_position_armature'in props:extra['export_rest_position_armature']=False
print('EXPORT_EXPLICIT_OPTIONS',extra)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scott-bum07-p41-editable.blend'),compress=True)
bpy.ops.export_scene.gltf(filepath=str(out/'scott-bum07-p41-prototype.glb'),export_format='GLB',use_selection=True,export_apply=False,export_animations=False,export_def_bones=True,export_morph=True,export_attributes=True,export_cameras=False,export_lights=False,**extra)
for n in r['exports']:
 p=out/n;r['exports'][n]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
r['runtimeVertexIDsExported']=True;r['exportExplicitOptions']=extra
(out/'build-report.json').write_text(json.dumps(r,indent=2)+'\n')
