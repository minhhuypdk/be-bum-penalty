"""Physical radial clearance of cap surfaces to the spherical globe; read-only."""
import bpy,json,hashlib,sys
from pathlib import Path
r=Path(__file__).resolve().parents[1];rows=[];pre='--pre-repair' in sys.argv
for version,path in [('baseline',r.parent/'p53a-bum07-blender-blockout/bum07-p53a-blockout.blend'),('R',r/'bum07-p53ar-refinement.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(path))
 for side in ['R','L']:
  eye=bpy.data.objects['Eyeball_'+side];centre=eye.matrix_world.translation;rad=[(eye.matrix_world@v.co-centre).length for v in eye.data.vertices];radius=max(rad);assert max(rad)-min(rad)<1e-6
  for prefix in ['Iris_','Pupil_']:
   o=bpy.data.objects[prefix+side];clearance=[(o.matrix_world@v.co-centre).length-radius for v in o.data.vertices];rows.append({'version':version,'object':o.name,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'globe_center':list(centre),'globe_radius':radius,'min_radial_clearance_H':min(clearance),'max_radial_clearance_H':max(clearance),'vertices_below_globe':sum(d<0 for d in clearance),'PASS_cap_outside_globe':min(clearance)>.0005})
name='optical-clearance-pre-repair.json' if pre else 'optical-clearance-final.json';(r/'evidence'/name).write_text(json.dumps({'stage':'PRE_REPAIR_DIAGNOSTIC' if pre else 'FINAL','method':'Distance of each cap vertex from centre minus maximum globe radius. Positive everywhere plus500microunit margin required; sphere verified. Not a full rig/animation test.','rows':rows},indent=2));print([(x['version'],x['object'],x['min_radial_clearance_H'],x['vertices_below_globe']) for x in rows])
if not pre:assert all(x['PASS_cap_outside_globe'] for x in rows)
