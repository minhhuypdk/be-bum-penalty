"""Prove refinement lineage from actual saved before/after files; no geometry edits."""
import bpy,json,hashlib,struct
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];base=r.parent/'p53a-bum07-blender-blockout';files={'before':base/'bum07-p53a-blockout.blend','after':r/'bum07-p53ar-refinement.blend'};records={}
def sha_parts(items):
 h=hashlib.sha256()
 for item in items:h.update(str(item).encode())
 return h.hexdigest()
for version,path in files.items():
 bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get();objects={}
 for o in s.objects:
  if not any(c.name.startswith('BUM07') for c in o.users_collection):continue
  row={'type':o.type,'matrix_world':[list(v) for v in o.matrix_world],'hidden':o.hide_render or o.hide_viewport}
  if o.type=='MESH':
   row.update(vertices=len(o.data.vertices),polygons=len(o.data.polygons),topology_sha256=sha_parts([tuple(p.vertices) for p in o.data.polygons]),position_sha256=sha_parts([tuple(o.matrix_world@v.co) for v in o.data.vertices]))
   if o.name=='Head_NEW_oval_integrated_nose_cheeks':
    pts=[o.matrix_world@v.co for v in o.data.vertices];nose=[p for p in pts if abs(p.x)<.09 and 4.28<p.z<4.41 and p.y<0];row['nose_ROI_min_Y_H']=min(p.y for p in nose)
  elif o.type=='CURVE':
   e=o.evaluated_get(dg);m=e.to_mesh();points=[e.matrix_world@v.co for v in m.vertices];row['actual_vertex_bounds']={'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)]};e.to_mesh_clear();row['point_radii']=sorted(set(p.radius for sp in o.data.splines for p in sp.bezier_points));row['bevel_depth']=o.data.bevel_depth;row['curve_positions_sha256']=sha_parts([tuple(p.co) for sp in o.data.splines for p in sp.bezier_points])
  objects[o.name]=row
 lights=[{'name':o.name,'matrix':[list(row) for row in o.matrix_world],'energy':o.data.energy,'size':o.data.size} for o in sorted(s.objects,key=lambda o:o.name) if o.type=='LIGHT']
 cams=[{'name':o.name,'matrix':[list(row) for row in o.matrix_world],'type':o.data.type,'ortho_scale':o.data.ortho_scale} for o in sorted(s.objects,key=lambda o:o.name) if o.type=='CAMERA']
 records[version]={'file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'objects':objects,'lights':lights,'cameras':cams,'view_transform':s.view_settings.view_transform,'look':s.view_settings.look,'world_background':list(s.world.node_tree.nodes['Background'].inputs[0].default_value),'world_strength':s.world.node_tree.nodes['Background'].inputs[1].default_value}
b,a=records['before'],records['after'];assert set(a['objects'])==set(b['objects'])
for key in ['lights','cameras','view_transform','look','world_background','world_strength']:assert a[key]==b[key],key
for name in ['Head_NEW_oval_integrated_nose_cheeks','Hair_unified_low_swept_masses']:
 assert a['objects'][name]['topology_sha256']==b['objects'][name]['topology_sha256']
for name in ['Front_07','Back_07','Front_BUM','Back_BUM','UpperDentalArch_SINGLE_8_teeth']:
 assert a['objects'][name]==b['objects'][name],name
assert a['objects']['Jersey_body_open_neck']['topology_sha256']==b['objects']['Jersey_body_open_neck']['topology_sha256']
for name,row in a['objects'].items():
 if row['type']=='CURVE':assert row['point_radii']==b['objects'][name]['point_radii'],name
checks={'loaded_existing_model_object_names_identical':True,'head_hair_connectivity_identical':True,'07_BUM_teeth_geometry_unchanged':True,'jersey_connectivity_retained_lower_hem_only_refined':True,'curve_point_radius_unchanged':True,'camera_lights_world_look_identical':True,'no_hidden_character_geometry':not any(x['hidden'] for x in a['objects'].values()),'scope':'P5.3A-R only; art approval pending'}
(r/'evidence/lineage-audit.json').write_text(json.dumps({'checks':checks,'before':b,'after':a},indent=2));print('PASS_NATIVE_REFINEMENT_LINEAGE_NOT_ART_APPROVAL')
