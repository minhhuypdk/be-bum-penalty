"""Convert official CC-BY Snow v3 to self-contained review GLBs.
Run: blender -b --disable-autoexec /path/to/snow_v03.blend -P scripts/assets/export-snow.py -- /output/directory
Original embedded Python is NEVER enabled. This is an art-base review asset,
not a BA/BUM redesign. Control rig, Cycles shaders and corrective behavior are
not equivalent in glTF; export a frozen evaluated bind pose + skin weights.
"""
import bpy,sys,os,json,math
from mathutils import Matrix
out=sys.argv[sys.argv.index('--')+1];os.makedirs(out,exist_ok=True)
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
source=bpy.data.objects['RIG-Snow'];bpy.context.scene.render.use_simplify=False;bpy.context.scene.frame_set(1)
# Use the textured render eyes, not the viewport animator proxy.
names=['body','head','hair_base','eyebrows','eyes','eye_dots','shirt','pants','shoes_base','shoes_bottom','shoes_parts','teeth_upper','teeth_lower','gums_upper','gums_lower','tongue']
objects=[bpy.data.objects['GEO-snow_'+n]for n in names]
for o in objects:
 o.hide_viewport=False;o.hide_set(False)
 # The source rig drives viewport subdivision to zero. Explicit export LODs
 # must remove only this driver before setting levels.
 for mod in o.modifiers:
  if mod.type=='SUBSURF':o.driver_remove('modifiers["'+mod.name+'"].levels')
# Build simple glTF-compatible PBR from the original published baked maps.
maproot=os.path.join(os.path.dirname(bpy.data.filepath),'maps','bake')
report=[]
for lod,level,texture_max in [('portrait',2,2048),('mobile',1,1024)]:
 mats={};textures={};created=[]
 def image(filename,color=True):
  key=(filename,color)
  if key in textures:return textures[key]
  im=bpy.data.images.load(os.path.join(maproot,filename),check_existing=False)
  im.colorspace_settings.name='sRGB' if color else 'Non-Color'
  w,h=im.size
  limit=texture_max if color and filename in ['skin_diffuse.1001.png','hair_diffuse.png','eyes_diffuse.png'] else min(texture_max,1024) if color else min(texture_max//2,1024) if 'normal' in filename else max(256,texture_max//4)
  if max(w,h)>limit:im.scale(round(w*limit/max(w,h)),round(h*limit/max(w,h)))
  im.pack();textures[key]=im;return im
 def material(key,skin_tile=1001):
  cache=(key,skin_tile)
  if cache in mats:return mats[cache]
  m=bpy.data.materials.new('Review-'+key+'-'+str(skin_tile));m.use_nodes=True
  n=m.node_tree.nodes;n.clear();p=n.new('ShaderNodeBsdfPrincipled');p.inputs['Roughness'].default_value=.48
  output=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(p.outputs['BSDF'],output.inputs['Surface'])
  maps={'snow.skin':('skin_diffuse.%s.png'%skin_tile,'skin_roughness.%s.png'%skin_tile,None),'snow.hair':('hair_diffuse.png','hair_roughness.png',None),'snow.eyes':('eyes_diffuse.png',None,'eyes_normal.png'),'snow.shirt':('shirt_diffuse.png','shirt_roughness.png','shirt_normal.png'),'snow.pants':('pants_diffuse.png','pants_roughness.png','pants_normal.png'),'snow.shoe':('shoes_diffuse.png','shoes_roughness.png','shoes_normal.png')}
  if key.startswith('snow.skin'):maps[key]=maps['snow.skin']
  if key in maps:
   color,rough,normal=maps[key]
   for fname,socket,cs in [(color,'Base Color',True),(rough,'Roughness',False)]:
    if fname:
     tex=n.new('ShaderNodeTexImage');tex.image=image(fname,cs);m.node_tree.links.new(tex.outputs['Color'],p.inputs[socket])
   if normal:
    tex=n.new('ShaderNodeTexImage');tex.image=image(normal,False);normalnode=n.new('ShaderNodeNormalMap');m.node_tree.links.new(tex.outputs['Color'],normalnode.inputs['Color']);m.node_tree.links.new(normalnode.outputs['Normal'],p.inputs['Normal'])
   if key=='snow.eyes':p.inputs['Roughness'].default_value=.16
  else:
   colors={'snow.skin_darker':(.43,.20,.14,1),'snow.skin_upper_lip':(.40,.13,.12,1),'snow.skin_lower_lip':(.55,.22,.20,1),'snow.teeth':(.85,.82,.72,1),'snow.gums':(.37,.08,.09,1),'snow.tongue':(.5,.12,.15,1),'snow.eye_dot':(1,1,1,1)}
   p.inputs['Base Color'].default_value=colors.get(key,(.5,.25,.15,1))
  mats[cache]=m;return m
 # Evaluate existing sculpt/cloth/subdivision and bind to a clean pose skeleton.
 for o in objects:
  for mod in o.modifiers:
   if mod.type=='SUBSURF':
    detail=level if o.name in ['GEO-snow_head','GEO-snow_hair_base','GEO-snow_eyes','GEO-snow_eyebrows'] else max(0,level-1)
    mod.levels=detail;mod.render_levels=detail
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 mesh_objects=[];used=set()
 for original in objects:
  ev=original.evaluated_get(dg);mesh=bpy.data.meshes.new_from_object(ev,preserve_all_data_layers=True,depsgraph=dg)
  obj=bpy.data.objects.new('Snow-'+original.name.removeprefix('GEO-snow_'),mesh);bpy.context.collection.objects.link(obj);obj.matrix_world=original.matrix_world.copy();created.append(obj);mesh_objects.append(obj)
  for group in original.vertex_groups:obj.vertex_groups.new(name=group.name)
  if not any(v.groups for v in mesh.vertices):
   group=obj.vertex_groups.new(name='DEF-Jaw' if any(w in original.name for w in ['lower','tongue']) else 'DEF-Head');group.add(list(range(len(mesh.vertices))),1,'REPLACE')
  for v in mesh.vertices:
   for g in v.groups:
    if g.weight>0:used.add(obj.vertex_groups[g.group].name)
  # Select correct UDIM tile per polygon; glTF has no UDIM sampling.
  original_materials=[s.material.name if s.material else 'snow.skin'for s in original.material_slots]
  original_indices=[p.material_index for p in mesh.polygons]
  mesh.materials.clear();slots={}
  uv=next((u for u in mesh.uv_layers if u.active_render),mesh.uv_layers.active)
  # Blender's selected UV can be the tattoo helper; glTF needs the render UV.
  uv_name=uv.name if uv else None
  for other_name in [layer.name for layer in mesh.uv_layers]:
   if other_name!=uv_name:mesh.uv_layers.remove(mesh.uv_layers[other_name])
  uv=mesh.uv_layers.get(uv_name) if uv_name else None
  for poly in mesh.polygons:
   key=original_materials[min(original_indices[poly.index],len(original_materials)-1)]
   tile=1001
   if key=='snow.skin' and uv:
    u=sum(uv.data[i].uv.x for i in poly.loop_indices)/len(poly.loop_indices);v=sum(uv.data[i].uv.y for i in poly.loop_indices)/len(poly.loop_indices);tile=1001+math.floor(u)+10*math.floor(v)
    if tile not in [1001,1002,1003]:tile=1001
    for i in poly.loop_indices:uv.data[i].uv.x-=tile-1001
   slot=(key,tile)
   if slot not in slots:slots[slot]=len(mesh.materials);mesh.materials.append(material(key,tile))
   poly.material_index=slots[slot];poly.use_smooth=True
 # Retain only weighted joints; bake bind matrices, discard Blender controls.
 weighted={n for n in used if n in source.pose.bones};data=bpy.data.armatures.new('Snow-review-skin');rig=bpy.data.objects.new('Snow-review-rig',data);bpy.context.collection.objects.link(rig);created.append(rig)
 bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
 for name in sorted(weighted):
  p=source.pose.bones[name];b=data.edit_bones.new(name);b.matrix=p.matrix.copy();b.length=max(p.length,.001)
 # Source controls are siblings of DEF joints; keeping only the nearest DEF
 # ancestor loses the anatomical hierarchy. Reconstruct main chains, then
 # attach facial/finger detail while preserving each world-space bind matrix.
 chains=[['DEF-Hips','DEF-Spine','DEF-Chest','DEF-RibCage','DEF-Neck','DEF-Head']]
 for side in ['L','R']:
  chains += [[n+'.'+side for n in ['DEF-RibCage','DEF-Shoulder','DEF-UpperArm1','DEF-UpperArm2','DEF-Forearm1','DEF-Forearm2','DEF-Wrist']][1:]]
  chains += [['DEF-Hips','DEF-Hips.'+side]+[n+'.'+side for n in ['DEF-Thigh1','DEF-Thigh2','DEF-Knee1','DEF-Knee2','DEF-Foot']]]
 parents={}
 for chain in chains:
  filtered=[n for n in chain if n in weighted]
  for parent,child in zip(filtered,filtered[1:]):parents[child]=parent
 for side in ['L','R']:
  if 'DEF-Shoulder.'+side in weighted:parents['DEF-Shoulder.'+side]='DEF-RibCage'
 for name in sorted(weighted):
  if name=='DEF-Hips':continue
  if name not in parents:
   ancestor=source.data.bones[name].parent
   while ancestor and ancestor.name not in weighted:ancestor=ancestor.parent
   if ancestor:parents[name]=ancestor.name
   elif 'Finger' in name:parents[name]='DEF-Wrist.'+name[-1]
   elif 'Toe' in name:parents[name]='DEF-Foot.'+name[-1]
   elif 'Hip' in name:parents[name]='DEF-Hips'
   else:parents[name]='DEF-Head'
 for name,parent in parents.items():
  if parent in weighted and parent!=name:data.edit_bones[name].parent=data.edit_bones[parent]
 bpy.ops.object.mode_set(mode='OBJECT')
 for obj in mesh_objects:
  mod=obj.modifiers.new('Review skin','ARMATURE');mod.object=rig;obj.parent=rig
 # A restrained standing review pose, not finished sports animation.
 # Lower the upper arms around world Y; the anatomical chains move hands too.
 from mathutils import Vector
 for side,angle in [('L',1.15),('R',-1.15)]:
  name='DEF-UpperArm1.'+side
  if name in rig.pose.bones:
   p=rig.pose.bones[name];pivot=p.head.copy();p.matrix=Matrix.Translation(pivot) @ Matrix.Rotation(angle,4,'Y') @ Matrix.Translation(-pivot) @ p.matrix
   p.rotation_mode='QUATERNION'
   for frame in [1,121]:p.keyframe_insert('rotation_quaternion',frame=frame,group='Standing arms')
 if 'DEF-Head' in rig.pose.bones:
  bone=rig.pose.bones['DEF-Head'];bone.rotation_mode='XYZ'
  for frame,angle in [(1,0),(31,.045),(61,0),(91,-.045),(121,0)]:
   bone.rotation_euler[1]=angle;bone.keyframe_insert('rotation_euler',frame=frame,group='Head review')
  rig.animation_data.action.name='Idle';bpy.context.scene.frame_set(1);bpy.context.scene.frame_end=121
 original_scene=bpy.context.scene;review_scene=bpy.data.scenes.new('Isolated Snow GLB');review_scene.frame_end=121
 for obj in created:review_scene.collection.objects.link(obj)
 bpy.context.window.scene=review_scene
 for obj in created:obj.select_set(True)
 bpy.context.view_layer.objects.active=rig
 path=os.path.join(out,'snow-review-'+lod+'.glb')
 bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,use_active_scene=True,export_apply=False,export_animations=True,export_anim_single_armature=False,export_animation_mode='ACTIVE_ACTIONS',export_nla_strips_merged_animation_name='Idle',export_frame_range=True,export_force_sampling=True,export_image_format='JPEG',export_jpeg_quality=92,export_extras=False,export_def_bones=True)
 report.append({'lod':lod,'subdivision':level,'maxTexture':texture_max,'texturePolicy':'Face, hair and iris albedo up to selected maximum; cloth/body albedo <=1K; normals <=half selected maximum; scalar roughness <=quarter selected maximum','bytes':os.path.getsize(path),'weightedJoints':len(weighted),'baseMeshVertices':sum(len(o.data.vertices)for o in mesh_objects),'note':'Frozen evaluated source bind pose; clean weighted skeleton; only authored Idle head-turn clip; no original CloudRig controls or sports clips.'})
 bpy.context.window.scene=original_scene
 for o in created:bpy.data.objects.remove(o,do_unlink=True)
 bpy.data.scenes.remove(review_scene)
 for m in mats.values():bpy.data.materials.remove(m)
 for im in textures.values():bpy.data.images.remove(im)
open(os.path.join(out,'build-report.json'),'w').write(json.dumps(report,indent=2)+'\n')
print('SNOW_EXPORT_COMPLETE',report)
