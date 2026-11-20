"""Render the saved, unchanged blockout. No image generation or retouching.
blender -b -t 8 --python scripts/render-final.py
"""
import bpy,json,hashlib,struct,time,shutil
from pathlib import Path
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r/'bum07-p53ar-refinement.blend'));s=bpy.context.scene
s.cycles.samples=64;s.cycles.use_denoising=False;s.render.resolution_x=1200;s.render.resolution_y=1600;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='8';s.render.filepath='//renders/after/full-front-000.png';s.camera=bpy.data.objects['Full_front-000'];bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(r/'bum07-p53ar-refinement.blend'),compress=True)
print('NATIVE_FINAL_SAVED',flush=True)
objects=sorted([o for o in s.objects if any(c.name.startswith('BUM07') for c in o.users_collection)],key=lambda o:o.name)
def fingerprint():
 h=hashlib.sha256()
 for o in objects:
  h.update(o.name.encode());h.update(str([list(row) for row in o.matrix_world]).encode());h.update(str((o.hide_render,o.hide_viewport)).encode())
  if o.type=='MESH':
   for v in o.data.vertices:h.update(struct.pack('<3f',*v.co))
   for p in o.data.polygons:h.update(struct.pack('<'+'I'*len(p.vertices),*p.vertices))
  elif o.type=='CURVE':
   h.update(str((o.data.bevel_depth,o.data.bevel_resolution)).encode())
   for sp in o.data.splines:
    for p in sp.bezier_points:h.update(str((list(p.co),list(p.handle_left),list(p.handle_right))).encode())
  h.update(str([(m.name,m.type, getattr(m,'levels',None),getattr(m,'thickness',None)) for m in o.modifiers]).encode())
 for m in sorted(bpy.data.materials,key=lambda m:m.name):
  if m.use_nodes:
   p=m.node_tree.nodes.get('Principled BSDF')
   if p:h.update(str((m.name,list(p.inputs['Base Color'].default_value),p.inputs['Roughness'].default_value,p.inputs['Metallic'].default_value)).encode())
 return h.hexdigest()
def lights():return [{'name':o.name,'matrix':[list(row) for row in o.matrix_world],'energy':o.data.energy,'size':o.data.size} for o in sorted(s.objects,key=lambda o:o.name) if o.type=='LIGHT']
fp=fingerprint();lighting=lights()
base=r.parent/'p53a-bum07-blender-blockout';previous=json.loads((base/'evidence/render-metadata.json').read_text())
assert lighting==previous['fixed_lights'], 'Do not change lighting between comparisons'
assert s.view_settings.look==previous['look'] and s.view_settings.view_transform==previous['view_transform']
for item in previous['renders']:
 c=bpy.data.objects[item['camera']];assert list(c.location)==item['location'] and list(c.rotation_euler)==item['rotation_euler'] and c.data.ortho_scale==item['ortho_scale']
meta={'baseline':'5dd8744','phase':'P5.3A-R','source':'Actual Blender4.3.2 CyclesCPU renders; no AI render replacement or postprocessing','resolution':[1200,1600],'samples':64,'denoising':False,'view_transform':s.view_settings.view_transform,'look':s.view_settings.look,'model_fingerprint':fp,'same_model_all_views':True,'fixed_lights':lighting,'art_approval':'OWNER_PENDING','before_images_source':'5dd8744/P5.3A original renders byte-preserved','before_after_camera_lights_identical':True,'renders':[],'aliases':[]}
views=[('Full_front-000','full-front-000'),('Full_three-quarter-045','full-three-quarter-045'),('Full_profile-090','full-profile-090'),('Full_back-180','full-back-180'),('Face_front-000','face-front-000'),('Face_three-quarter-045','face-three-quarter-045')]
for cn,name in views:
 assert fingerprint()==fp and lights()==lighting
 c=bpy.data.objects[cn];assert c.data.type=='ORTHO';s.camera=c;s.render.filepath=str(r/'renders/after'/f'{name}.png');t=time.time();bpy.ops.render.render(write_still=True)
 assert fingerprint()==fp and lights()==lighting
 meta['renders'].append({'file':f'renders/after/{name}.png','camera':cn,'type':'ORTHO','orbit_degrees':c.data['orbit_degrees'],'ortho_scale':c.data.ortho_scale,'target':list(c.data['target']),'location':list(c.location),'rotation_euler':list(c.rotation_euler),'duration_seconds':round(time.time()-t,3),'sha256':hashlib.sha256(Path(s.render.filepath).read_bytes()).hexdigest(),'model_fingerprint_before_and_after':fp,'lights_unchanged':True})
 (r/'evidence/render-metadata.json').write_text(json.dumps(meta,indent=2));print('FINAL_RENDER_READY',name,flush=True)
meta['blend_sha256']=hashlib.sha256((r/'bum07-p53ar-refinement.blend').read_bytes()).hexdigest();(r/'evidence/render-metadata.json').write_text(json.dumps(meta,indent=2));print('FINAL_SET_COMPLETE_6_RENDERS',flush=True)
