"""Read-only forensic audit BEFORE any geometry edit. Uses existing P5.3A file."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];base=r.parent/'p53a-bum07-blender-blockout';source=base/'bum07-p53a-blockout.blend';bpy.ops.wm.open_mainfile(filepath=str(source));dg=bpy.context.evaluated_depsgraph_get();old=json.loads((base/'evidence/mesh-camera-audit.json').read_text())
def bbox(points):
 return {'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)]} if points else None
def bbobj(o):return bbox([o.matrix_world@Vector(c) for c in o.bound_box])
rows=[]
for o in bpy.context.scene.objects:
 if o.type!='CURVE':continue
 e=o.evaluated_get(dg);pre=bbobj(e);me=e.to_mesh();actual=bbox([e.matrix_world@v.co for v in me.vertices]);during=bbobj(e);nv=len(me.vertices);e.to_mesh_clear();post=bbobj(e)
 points=[o.matrix_world@p.co for sp in o.data.splines for p in sp.bezier_points];handles=[o.matrix_world@v for sp in o.data.splines for p in sp.bezier_points for v in [p.handle_left,p.handle_right]]
 previous=next((x['bounds'] for x in old['geometry'] if x['name']==o.name),None)
 rows.append({'name':o.name,'matrix_world':[list(row) for row in o.matrix_world],'native_object_bound_box':bbobj(o),'evaluated_bound_box_before_to_mesh':pre,'evaluated_bound_box_during_to_mesh':during,'evaluated_bound_box_after_clear':post,'actual_evaluated_vertex_bounds':actual,'control_bounds':bbox(points),'handle_bounds':bbox(handles),'bevel_depth':o.data.bevel_depth,'vertices':nv,'previous_P53A_report_bounds':previous,'hidden':o.hide_render or o.hide_viewport})
summary={'source_commit':'5dd8744','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'geometry_modified':False,'curves':rows}
(r/'evidence/curve-diagnosis-before.json').write_text(json.dumps(summary,indent=2));print('READ_ONLY_CURVE_AUDIT',len(rows))
for x in rows:
 if x['name'].startswith(('Upper_lid_margin','Ear_helix','Closed_mouth')):print(x['name'],'OLD',x['previous_P53A_report_bounds'],'ACTUAL',x['actual_evaluated_vertex_bounds'],'NATIVE',x['native_object_bound_box'])
