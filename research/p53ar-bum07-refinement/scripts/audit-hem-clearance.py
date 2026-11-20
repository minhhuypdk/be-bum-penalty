import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];before='--before' in sys.argv;source=r.parent/'p53a-bum07-blender-blockout/bum07-p53a-blockout.blend' if before else r/'bum07-p53ar-refinement.blend';bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get();rows=[]
for z in [2.442,2.47,2.49,2.51]:
 counts={};hits=[]
 for i in range(41):
  x=-.44+i*.88/40;hit,loc,n,index,o,mat=s.ray_cast(dg,Vector((x,-2,z)),Vector((0,1,0)),distance=4)
  if hit:counts[o.name]=counts.get(o.name,0)+1;hits.append({'x':x,'first_surface':o.name,'Y':loc.y})
 rows.append({'z':z,'counts':counts,'rays':hits})
(r/'evidence'/('hem-baseline.json' if before else 'hem-after.json')).write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source':'5dd8744' if before else 'P5.3A-R','method':'41 front orthographic rays at each Z, X from-.44 to+.44, first opaque surface. Static clearance sample, not all intersections.','rows':rows},indent=2));print([(row['z'],row['counts']) for row in rows])
