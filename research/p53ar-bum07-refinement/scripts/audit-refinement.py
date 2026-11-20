"""Read back the saved .blend; evidence for structure/camera only, not art quality."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r/'bum07-p53ar-refinement.blend'));s=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get()
objects=[o for o in s.objects if any(c.name.startswith('BUM07') for c in o.users_collection)]
mesh_objects=[o for o in objects if o.type=='MESH'];surface_objects=[o for o in objects if o.type in ['MESH','CURVE','FONT']]
def vertex_bounds(points):
 return {'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)]}
def bounds(o,evaluated=True):
 # Correct curve bounds: never use evaluated Curve.bound_box in Blender4.3.2.
 e=o.evaluated_get(dg) if evaluated else o;me=e.to_mesh();result=vertex_bounds([e.matrix_world@v.co for v in me.vertices]);e.to_mesh_clear();return result
records=[];tri=0
for o in surface_objects:
 e=o.evaluated_get(dg);me=e.to_mesh();me.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(me)
 rec={'name':o.name,'type':o.type,'evaluated_vertices':len(me.vertices),'triangles':len(me.loop_triangles),'boundary_edges':sum(x.is_boundary for x in bm.edges),'nonmanifold_edges':sum(not x.is_manifold for x in bm.edges),'zero_area_faces':sum(x.calc_area()<1e-12 for x in bm.faces),'finite_vertices':all(math.isfinite(c) for v in me.vertices for c in v.co),'bounds':vertex_bounds([e.matrix_world@v.co for v in me.vertices])}
 records.append(rec);tri+=len(me.loop_triangles);bm.free();e.to_mesh_clear()
arch=bpy.data.objects['UpperDentalArch_SINGLE_8_teeth'];adj={i:set() for i in range(len(arch.data.vertices))}
for edge in arch.data.edges:a,b=edge.vertices;adj[a].add(b);adj[b].add(a)
visited=set();groups=[]
for a in adj:
 if a in visited:continue
 stack=[a];group=[]
 while stack:
  i=stack.pop()
  if i in visited:continue
  visited.add(i);group.append(i);stack.extend(adj[i]-visited)
 groups.append(group)
assert len(groups)==8
cameras=[]
for c in bpy.data.collections['CAMERAS'].objects:
 assert c.data.type=='ORTHO'
 # Translate two1H test points along viewing depth; projected span must stay identical.
 target=Vector(c.data['target']);right=c.rotation_euler.to_matrix()@Vector((1,0,0));forward=c.rotation_euler.to_matrix()@Vector((0,0,-1));spans=[]
 for depth in [-1,1]:
  p=target+forward*depth;u=world_to_camera_view(s,c,p);v=world_to_camera_view(s,c,p+right);spans.append(abs(v.x-u.x)*s.render.resolution_x)
 assert abs(spans[0]-spans[1])<.001
 cameras.append({'name':c.name,'type':c.data.type,'ortho_scale':c.data.ortho_scale,'angle_degrees':c.data['orbit_degrees'],'location':list(c.location),'target':list(c.data['target']),'one_H_projected_pixels_at_two_depths':spans,'depth_independent_scale_PASS':True})
head=bpy.data.objects['Head_NEW_oval_integrated_nose_cheeks'];hb=bounds(head);hair=[bounds(o) for o in objects if any(c.name=='BUM07_HAIR' for c in o.users_collection)];hairmax=max(x['max'][2] for x in hair)
# Fullbody crown/floor ratio uses actual head bounding-box crown/chin; floor is measured studs bottom.
foot=[bounds(o) for o in objects if o.name.startswith('Boot_stud')];floor=min(x['min'][2] for x in foot);H=hb['max'][2]-hb['min'][2]
report={'phase':'P5.3A-R_REFINEMENT','saved_blend_readback':True,'mesh_source':'Existing P5.3A native model refined; no Scott/rebuild/import; actual evaluated vertex bounds used','object_count':len(objects),'surface_objects':len(surface_objects),'mesh_objects':len(mesh_objects),'evaluated_triangles':tri,'materials_used':sorted({m.name for o in surface_objects for m in o.data.materials if m}),'head_bounds':hb,'actual_H_from_head_bbox':H,'actual_skull_to_floor_H':(hb['max'][2]-floor)/H,'actual_floor_z':floor,'actual_hair_to_floor_H':(hairmax-floor)/H,'hair_max_z':hairmax,'design_hair_max_H':5.2,'upper_teeth_connected_components':len(groups),'upper_arch_objects':sum(o.name.startswith('UpperDentalArch') for o in objects),'armatures':sum(o.type=='ARMATURE' for o in s.objects),'actions':len(bpy.data.actions),'shape_keys':sum(bool(o.data.shape_keys) for o in mesh_objects),'camera_checks':cameras,'geometry':records,'limitations':['Separate overlapping blockout components and intentional cloth/hair boundaries; not production connected topology.','Not rigged, not weight tested, not UV unwrapped or game optimized.','Triangle count is Blender evaluated geometry, not GLB triangle budget/drawcalls.','No Blink/Smile animation, no collision/occlusion deformation PASS.','Art approval remains OWNER_PENDING; no9/10 claim.']}
assert abs(report['actual_skull_to_floor_H']-5)<.05
assert report['armatures']==0 and report['actions']==0 and report['shape_keys']==0
assert all(x['finite_vertices'] for x in records)
# Verify number projection onto the evaluated shirt. Distances are scene H, not millimeters.
shirt=bpy.data.objects['Jersey_body_open_neck'];evaluated=shirt.evaluated_get(dg);me=evaluated.to_mesh();verts=[shirt.matrix_world@v.co for v in me.vertices];bvh=BVHTree.FromPolygons(verts,[tuple(p.vertices) for p in me.polygons]);evaluated.to_mesh_clear();numbers=[]
for name,height in [('Front_07',.38),('Back_07',.42),('Front_BUM',.10),('Back_BUM',.13)]:
 o=bpy.data.objects[name];points=[o.matrix_world@v.co for v in o.data.vertices];near=[bvh.find_nearest(p) for p in points];dist=[n[3] for n in near];signed=[(p-n[0]).dot(n[1]) for p,n in zip(points,near)];bb=bounds(o);h=bb['max'][2]-bb['min'][2]
 numbers.append({'object':name,'height_H':h,'target_height_H':height,'min_distance_to_cloth_H':min(dist),'max_distance_to_cloth_H':max(dist),'surface_offset_target_H':.0015,'min_signed_outward_clearance_H':min(signed),'PASS_outside_cloth':min(signed)>0,'PASS_surface_distance_under_003H':max(dist)<.003,'PASS_height_within_005H':abs(h-height)<.005})
report['number_surface_checks']=numbers
report['number_surface_PASS']=all(n['PASS_surface_distance_under_003H'] and n['PASS_height_within_005H'] and n['PASS_outside_cloth'] for n in numbers)
report['hidden_character_objects']=[o.name for o in objects if o.hide_render or o.hide_viewport]
report['hidden_character_collections']=[c.name for c in bpy.data.collections if c.name.startswith('BUM07') and (c.hide_render or c.hide_viewport)]
# Static geometric visibility: orthographic rays through a fixed eye-region grid.
# This does NOT test blink or facial deformation and is not pixel antialiasing evidence.
visibility=[];G=90
for camname in ['Face_front-000','Face_three-quarter-045','Face_profile-090']:
 cam=bpy.data.objects[camname];right=cam.rotation_euler.to_matrix()@Vector((1,0,0));forward=cam.rotation_euler.to_matrix()@Vector((0,0,-1));up=Vector((0,0,1));counts={'camera':camname,'grid_per_eye':[G,G],'grid_step_H':.28/(G-1),'visible_optical_hits':0,'outside_nominal_aperture_hits':0,'outside_aperture_plus_004H_hits':0,'worst_outliers':[]}
 for side,sign in [('R',-1),('L',1)]:
  centre=Vector((sign*.16,-.176,4.54))
  for i in range(G):
   for j in range(G):
    origin=centre+right*(-.14+.28*i/(G-1))+up*(-.14+.28*j/(G-1))-forward*4
    hit,loc,normal,index,obj,matrix=s.ray_cast(dg,origin,forward,distance=8)
    if not hit or not obj.name.startswith(('Eyeball_','Iris_','Pupil_','Corneal_lens_')):continue
    counts['visible_optical_hits']+=1;sgn=1 if obj.name.endswith('_L') else -1;dx=loc.x-sgn*.16;dz=loc.z-4.54-sgn*.005*(dx/.103);h=.055 if dz>=0 else .035
    q=(dx/.103)**2+(dz/h)**2;qt=(dx/.107)**2+(dz/(h+.004))**2
    if q>1.03:counts['outside_nominal_aperture_hits']+=1
    if qt>1:
     counts['outside_aperture_plus_004H_hits']+=1
     if len(counts['worst_outliers'])<8:counts['worst_outliers'].append({'object':obj.name,'location':list(loc),'q':q})
 counts['PASS_no_abnormal_globe_exposure_at_grid_tolerance']=counts['outside_aperture_plus_004H_hits']==0
 visibility.append(counts)
report['static_eye_visibility']=visibility
report['static_eye_visibility_PASS']=all(x['PASS_no_abnormal_globe_exposure_at_grid_tolerance'] for x in visibility)
report['static_eye_visibility_limit']='Geometric ray grid .00315H, aperture tolerance .004H; not per-pixel zero-leak proof, no blink/animation test. Visual0/45/90 render review also required.'
assert not report['hidden_character_objects'] and not report['hidden_character_collections']
(r/'evidence/mesh-camera-audit.json').write_text(json.dumps(report,indent=2));print('AUDIT_NATIVE_BLEND_READBACK',report['actual_skull_to_floor_H'],tri,'TEETH',len(groups))
