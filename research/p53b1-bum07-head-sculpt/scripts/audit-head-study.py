"""Head-only native sanity, not an artistic quality certificate."""
import bpy,bmesh,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r/'bum07-p53b1-head-study.blend'));s=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get();rows=[]
for o in s.objects:
 if o.type not in ['MESH','CURVE']:continue
 if not any(c.name.startswith('BUM07') for c in o.users_collection):continue
 e=o.evaluated_get(dg);m=e.to_mesh();m.calc_loop_triangles();pts=[e.matrix_world@v.co for v in m.vertices];bm=bmesh.new();bm.from_mesh(m);rows.append({'object':o.name,'type':o.type,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'min':[min(p[i] for p in pts) for i in range(3)],'max':[max(p[i] for p in pts) for i in range(3)],'finite':all(math.isfinite(c) for p in pts for c in p),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'faces_under_1e12':sum(f.calc_area()<1e-12 for f in bm.faces),'hidden':o.hide_render or o.hide_viewport,'uv_layers':list(m.uv_layers.keys()),'signed_volume_if_closed':bm.calc_volume(signed=True) if all(e.is_manifold for e in bm.edges) else None});bm.free();e.to_mesh_clear()
optics=[]
for side in ['R','L']:
 eye=bpy.data.objects['B1_Eyeball_'+side];centre=eye.matrix_world.translation;rr=max((eye.matrix_world@v.co-centre).length for v in eye.data.vertices)
 for prefix in ['B1_Iris_','B1_Pupil_']:
  o=bpy.data.objects[prefix+side];gaps=[(o.matrix_world@v.co-centre).length-rr for v in o.data.vertices];optics.append({'object':o.name,'min_radial_clearance':min(gaps),'below_globe':sum(g<0 for g in gaps),'PASS':min(gaps)>.0005})
head=next(x for x in rows if x['object'].startswith('B1_HEAD'));hair=next(x for x in rows if x['object'].startswith('B1_HAIR'))
cameras=[]
for name in ['Face_front-000','Face_three-quarter-045','Face_profile-090','B1_back_180']:
 o=bpy.data.objects[name];cameras.append({'name':name,'type':o.data.type,'ortho_scale':o.data.ortho_scale,'location':list(o.location),'rotation':list(o.rotation_euler)});assert o.data.type=='ORTHO'
report={'phase':'P5.3B.1','scope':'Head neck shoulder bust, no full-body model in new study','triangles_total':sum(x['triangles'] for x in rows),'geometry':rows,'head_height_H':head['max'][2]-head['min'][2],'hair_max_Z':hair['max'][2],'optics':optics,'cameras':cameras,'armatures':sum(o.type=='ARMATURE' for o in s.objects),'actions':len(bpy.data.actions),'shape_key_datablocks':len(bpy.data.shape_keys),'linked_libraries':[x.filepath for x in bpy.data.libraries],'unpacked_file_images':[x.filepath for x in bpy.data.images if x.source=='FILE' and x.filepath and not x.packed_file],'unpacked_fonts':[x.filepath for x in bpy.data.fonts if x.filepath and x.filepath!='<builtin>' and not x.packed_file],'source_reference_preserved':hashlib.sha256((r/'reference/bum07-p53ar-preserved.blend').read_bytes()).hexdigest()==hashlib.sha256((r.parent/'p53ar-bum07-refinement/bum07-p53ar-refinement.blend').read_bytes()).hexdigest(),'art_approval':'OWNER_PENDING','artistic_objective':'FAIL_ARTISTIC_OBJECTIVE','limitations':['Triangulated sculpt construction, not production facial topology.','Finite/manifold/cap clearance does not prove natural eye expression or beauty.','5H is retained as design datum; only a1H head/bust is built, no measured full-body B1 ratio.']}
(r/'evidence/native-audit.json').write_text(json.dumps(report,indent=2));print('B1_NATIVE',report['triangles_total'],'HEAD',head['nonmanifold_edges'],head['faces_under_1e12'],'HAIR',hair['nonmanifold_edges'],hair['faces_under_1e12'],'OPTICS',all(x['PASS'] for x in optics))

closed=[x for x in rows if x['object'].startswith(('B1_HEAD','B1_HAIR','B1_ear_sculpt','B1_Eyeball'))]
assert all(x['finite'] and x['nonmanifold_edges']==0 and x['faces_under_1e12']==0 for x in closed)
assert all(x['finite'] and not x['hidden'] for x in rows)
assert all(x['PASS'] for x in optics)
assert report['source_reference_preserved'] and report['armatures']==0 and report['actions']==0
print('SCOPED_NATIVE_ASSERTIONS_PASS_NOT_ART_APPROVAL',flush=True)
assert not report['linked_libraries'] and not report['unpacked_file_images'] and not report['unpacked_fonts']
assert report['shape_key_datablocks']==0
print('EDITABLE_LOCAL_DATA_NO_UNPACKED_DEPENDENCIES_PASS',flush=True)
