"""Read original CC0 bundle only; no saving, appending or sculpting."""
import bpy,json,hashlib,bmesh
from pathlib import Path
r=Path(__file__).resolve().parents[1];p=Path('/tmp/p54-human-base-original/human-base-meshes-bundle-v1.4.1/human_base_meshes_bundle.blend');h=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False);rows=[]
for o in list(bpy.data.objects)+list(bpy.data.collections):
 if o.asset_data:
  a=o.asset_data;meta={'name':o.name,'type':getattr(o,'type','COLLECTION'),'author':a.author,'description':a.description,'license':getattr(a,'license',None),'copyright':getattr(a,'copyright',None),'tags':[t.name for t in a.tags]}
  rows.append(meta)
meshes=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 if not any(k in o.name.lower() for k in ['head','eye','jaw']):continue
 m=o.data;bm=bmesh.new();bm.from_mesh(m);meshes.append({'name':o.name,'vertices_raw':len(m.vertices),'polygons_raw':len(m.polygons),'quad_faces_raw':sum(len(x.vertices)==4 for x in m.polygons),'triangles_base':sum(len(x.vertices)-2 for x in m.polygons),'uv_layers':list(m.uv_layers.keys()),'shape_keys':[x.name for x in m.shape_keys.key_blocks] if m.shape_keys else [],'modifiers':[{'type':x.type,'levels':getattr(x,'levels',None),'total_levels':getattr(x,'total_levels',None)} for x in o.modifiers],'boundary_edges_raw':sum(x.is_boundary for x in bm.edges),'nonmanifold_edges_raw':sum(not x.is_manifold for x in bm.edges)});bm.free()
texts=[{'name':x.name,'text':x.as_string()} for x in bpy.data.texts if any(k in x.name.lower()+' '+x.as_string().lower() for k in ['license','cc0','copyright','readme'])]
result={'source':'Official Human Base Meshes bundle1.4.1, exact unmodified native','sha256':h,'source_unchanged':hashlib.sha256(p.read_bytes()).hexdigest()==h,'autoexec':False,'saved_or_exported':False,'asset_metadata':rows,'head_eye_jaw_meshes':meshes,'embedded_notices':texts,'armatures':[{'name':o.name,'bones':len(o.data.bones)} for o in bpy.data.objects if o.type=='ARMATURE'],'actions':len(bpy.data.actions),'limitations':['Original bundle inspection only; no BUM adaptation or art approval.','Base topology counts are not evaluated render tris or GLB counts.','No deformation or export test performed.']};(r/'evidence/human-bundle-audit.json').write_text(json.dumps(result,indent=2));print('ASSET_METADATA',json.dumps(rows));print('NOTICES',[x['name'] for x in texts]);print('HEAD_MESHES',json.dumps(meshes))
