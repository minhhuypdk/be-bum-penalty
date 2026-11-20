"""P5.4 evaluation only. Disable autoexec. No bpy save/export/generation operations."""
import bpy,bmesh,hashlib,json,math
from pathlib import Path
r=Path(__file__).resolve().parents[1]
specs=[('B1',r.parent/'p53b1-bum07-head-sculpt/bum07-p53b1-head-study.blend'),('R',r.parent/'p53ar-bum07-refinement/bum07-p53ar-refinement.blend'),('Tiby',Path('/tmp/p54-tiby-original/TIBY.blend'))]
results=[]
for label,p in specs:
 before=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False);rows=[];dg=bpy.context.evaluated_depsgraph_get()
 for o in bpy.context.scene.objects:
  if o.type!='MESH':continue
  if label in ['B1','R'] and not any(c.name.startswith('BUM07') for c in o.users_collection):continue
  m=o.data;bm=bmesh.new();bm.from_mesh(m);weights=[sum(g.weight>1e-6 for g in v.groups) for v in m.vertices];e=o.evaluated_get(dg);em=e.to_mesh();em.calc_loop_triangles()
  rows.append({'name':o.name,'vertices_raw':len(m.vertices),'polygons_raw':len(m.polygons),'tri_faces_raw':sum(len(f.vertices)==3 for f in m.polygons),'quad_faces_raw':sum(len(f.vertices)==4 for f in m.polygons),'ngons_raw':sum(len(f.vertices)>4 for f in m.polygons),'triangles_evaluated':len(em.loop_triangles),'uv_layers':list(m.uv_layers.keys()),'shape_keys':[k.name for k in m.shape_keys.key_blocks] if m.shape_keys else [],'modifiers':[{'name':x.name,'type':x.type,'levels':getattr(x,'levels',None),'viewport':x.show_viewport,'render':x.show_render} for x in o.modifiers],'boundary_edges_raw':sum(x.is_boundary for x in bm.edges),'nonmanifold_edges_raw':sum(not x.is_manifold for x in bm.edges),'material_slots':len(o.material_slots),'max_vertex_groups_weight_gt_1e_minus6':max(weights,default=0),'vertices_over_4_influences':sum(x>4 for x in weights),'vertex_group_count':len(o.vertex_groups),'finite':all(math.isfinite(c) for v in m.vertices for c in v.co)});bm.free();e.to_mesh_clear()
 arms=[{'name':o.name,'bones':len(o.data.bones),'deform_bones':sum(b.use_deform for b in o.data.bones),'constraints':sum(len(b.constraints) for b in o.pose.bones),'custom_shape_objects':sorted({b.custom_shape.name for b in o.pose.bones if b.custom_shape})} for o in bpy.context.scene.objects if o.type=='ARMATURE']
 keys=[k for m in bpy.data.meshes if m.shape_keys for k in m.shape_keys.key_blocks]
 results.append({'label':label,'source':str(p.relative_to(r.parent)) if label!='Tiby' else 'temporary TIBY.blend from author CC0 ZIP','source_sha256':before,'source_sha256_after':hashlib.sha256(p.read_bytes()).hexdigest(),'source_bytes_unchanged':before==hashlib.sha256(p.read_bytes()).hexdigest(),'autoexec':False,'saved_or_exported':False,'blender':bpy.app.version_string,'meshes':rows,'armatures':arms,'actions':len(bpy.data.actions),'shape_key_total_including_basis':len(keys),'limitations':['Read-only structure inspection, not deformation playback or art approval.','Evaluated triangle count uses current dependency graph/viewport modifier evaluation, not an exported GLB.','Material slots and Blender bones do not equal runtime draw calls/export joints.']});print('READ_ONLY_INSPECTED',label,len(rows),'meshes',arms,flush=True)
(r/'evidence/read-only-mesh-audit.json').write_text(json.dumps(results,indent=2));assert all(x['source_bytes_unchanged'] for x in results)
