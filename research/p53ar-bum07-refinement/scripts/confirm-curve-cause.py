"""Controlled in-memory copies only; never save or alter baseline .blend."""
import bpy,json
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r.parent/'p53a-bum07-blender-blockout/bum07-p53a-blockout.blend'));source=bpy.data.objects['Upper_lid_margin_R'];rows=[]
def bounds(points):return {'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)]}
for radius,bevel in [(1,.0025),(.1,.0025),(1,.01)]:
 o=source.copy();o.data=source.data.copy();bpy.context.scene.collection.objects.link(o)
 for sp in o.data.splines:
  for p in sp.bezier_points:p.radius=radius
 o.data.bevel_depth=bevel;bpy.context.view_layer.update();e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());reported=bounds([e.matrix_world@Vector(c) for c in e.bound_box]);m=e.to_mesh();actual=bounds([e.matrix_world@v.co for v in m.vertices]);e.to_mesh_clear();rows.append({'point_radius':radius,'bevel_depth':bevel,'reported_evaluated_bbox':reported,'actual_vertex_bbox':actual});bpy.data.objects.remove(o,do_unlink=True)
(r/'evidence/curve-cause-controlled-test.json').write_text(json.dumps({'baseline_saved':False,'geometry_changes_in_delivery':False,'temporary_copies_only':True,'tests':rows},indent=2));print(json.dumps(rows))
