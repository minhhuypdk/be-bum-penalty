import bpy,sys,json,hashlib
from pathlib import Path
src=Path(bpy.data.filepath);before=hashlib.sha256(src.read_bytes()).hexdigest();out=Path(sys.argv[sys.argv.index('--')+1]);out.mkdir(parents=True,exist_ok=True)
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');weighted=set();mesh=[]
for o in bpy.data.objects:
 if o.type!='MESH' or not any(m.type=='ARMATURE'for m in o.modifiers):continue
 mesh.append(o)
 for v in o.data.vertices:
  for g in v.groups:
   if g.weight>0:weighted.add(o.vertex_groups[g.group].name)
report={'sourceSha256':before,'researchOnlyOriginalCharacter':True,'BUMConversion':False,'weightedBoneCount':len(weighted),'weightedBoneNames':sorted(weighted),'rigBoneNames':[b.name for b in rig.data.bones],'materialNodeTypes':{m.name:[n.type for n in m.node_tree.nodes]for m in bpy.data.materials if m.use_nodes}}
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
for obj in bpy.context.scene.objects:obj.select_set(False)
for o in mesh:o.hide_set(False);o.select_set(True)
rig.hide_set(False);rig.select_set(True);bpy.context.view_layer.objects.active=rig
try:
 p=out/'scott-original-probe.glb';bpy.ops.export_scene.gltf(filepath=str(p),export_format='GLB',use_selection=True,export_apply=False,export_animations=False,export_def_bones=True,export_morph=True,export_cameras=False,export_lights=False)
 report['exportStatus']='PASS_STATIC_EXPORT_ONLY';report['GLBBytes']=p.stat().st_size;report['GLBSha256']=hashlib.sha256(p.read_bytes()).hexdigest()
except Exception as e:report['exportStatus']='FAIL';report['error']=str(e)
assert hashlib.sha256(src.read_bytes()).hexdigest()==before;report['sourceUnchanged']=True
(out/'scott-export-probe.json').write_text(json.dumps(report,indent=2)+'\n');print('SCOTT_PROBE',report.get('exportStatus'),report['weightedBoneCount'])
