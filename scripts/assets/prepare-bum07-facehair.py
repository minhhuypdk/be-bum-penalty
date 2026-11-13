"""Face/hair ONLY. Computational mesh study; NOT professional hand-sculpt or approved 9/10."""
import bpy,bmesh,ast,os,sys,json,hashlib,struct,math
from math import sin,cos,pi,exp,sqrt,atan2
from mathutils import Vector
from mathutils.kdtree import KDTree
args=sys.argv[sys.argv.index('--')+1:];OUT=os.path.abspath(args[0]);os.makedirs(OUT,exist_ok=True)
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
scene=bpy.context.scene;source=bpy.data.filepath;source_sha=hashlib.sha256(open(source,'rb').read()).hexdigest()
assert OUT!=os.path.dirname(source)
rig=bpy.data.objects['BUM07 original rig study'];rig.animation_data.action=bpy.data.actions['Idle'];scene.frame_set(1)
def is_face(n):return n=='BUM independent facial surface' or n.startswith(('eye white','iris ','pupil ','eye glint','soft eyelid','tapered brow','sculpt ear','nostril ','gentle smile','lower lip','original combed'))
def fp(o):
 h=hashlib.sha256()
 for v in o.data.vertices:
  h.update(struct.pack('<3f',*v.co))
  for g in v.groups:h.update(struct.pack('<If',g.group,g.weight))
 for p in o.data.polygons:h.update(str(tuple(p.vertices)).encode())
 for uv in o.data.uv_layers:
  h.update(uv.name.encode())
  for d in uv.data:h.update(struct.pack('<2f',*d.uv))
 h.update(str([(m.name,list(m.diffuse_color),m.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value if m.use_nodes else None)for m in o.data.materials]).encode());return h.hexdigest()
def rig_data():
 return {'bones':[(b.name,list(b.head_local),list(b.tail_local),b.parent.name if b.parent else None)for b in rig.data.bones],'actions':[(a.name,[(f.data_path,f.array_index,[(list(k.co),k.interpolation)for k in f.keyframe_points])for f in a.fcurves])for a in bpy.data.actions]}
body={o.name:fp(o)for o in bpy.data.objects if o.type=='MESH' and not is_face(o.name)};before_rig=rig_data()
face=[o for o in bpy.data.objects if o.type=='MESH' and is_face(o.name)]
ref=bpy.data.collections.new('00_C_LOCKED_FACE_REFERENCE');scene.collection.children.link(ref);ref.hide_render=True;ref.hide_viewport=True
for o in face:
 c=o.copy();c.data=o.data.copy();c.name='C_REFERENCE__'+o.name;ref.objects.link(c);c.hide_select=True
head=bpy.data.objects['BUM independent facial surface'];head.name='P2 facial surface'
for v in head.data.vertices:
 x,y,z=v.co
 if y<-.1:
  v.co.y+=.026*exp(-(x/.060)**2-((z-1.842)/.075)**2)-.008*exp(-(x/.082)**2-((z-1.875)/.075)**2)
  v.co.z+=.006*exp(-(x/.11)**2-((z-1.61)/.10)**2)
bm=bmesh.new();bm.from_mesh(head.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001)
remove=[f for f in bm.faces if f.calc_center_median().y<-.15 and any(((f.calc_center_median().x-s*.137)/.076)**2+((f.calc_center_median().z-1.925)/.054)**2<1 for s in [-1,1])]
bmesh.ops.delete(bm,geom=remove,context='FACES')
for v in bm.verts:
 if any(e.is_boundary for e in v.link_edges) and v.co.y<-.12 and 1.84<v.co.z<2.02:
  cx=.137 if v.co.x>0 else -.137;a=atan2((v.co.z-1.925)/.054,(v.co.x-cx)/.076);v.co.x=cx+.076*cos(a);v.co.z=1.925+(.054 if sin(a)>0 else .047)*sin(a)
bm.to_mesh(head.data);bm.free();head.data.update()
front=[v.co.copy()for v in head.data.vertices if v.co.y<-.1];tree=KDTree(len(front))
for i,v in enumerate(front):tree.insert(Vector((v.x,v.z,0)),i)
tree.balance()
def surface_y(x,z):
 near=tree.find_n(Vector((x,z,0)),6);ws=[1/(d+.003)**2 for v,i,d in near];return sum(front[i].y*w for (v,i,d),w in zip(near,ws))/sum(ws)
# Reuse ONLY trusted project helper function definitions, never execute its scene reset/build.
objects=[];binding={}
tree_ast=ast.parse(open('scripts/assets/build-bum07.py').read())
defs=[n for n in tree_ast.body if isinstance(n,ast.FunctionDef) and n.name in ['mesh','ellipsoid']]
exec(compile(ast.Module(body=defs,type_ignores=[]),'project_mesh_helpers','exec'),globals())
def copy_mat(n,label):m=bpy.data.materials[n].copy();m.name=label;return m
headmat=head.data.materials[0].copy();headmat.name='P2 complexion';head.data.materials[0]=headmat
skin=copy_mat('warm child skin','P2 skin');white=copy_mat('warm sclera','P2 sclera');iris=copy_mat('hazel iris','P2 iris');pupil=copy_mat('pupil','P2 pupil');lip=copy_mat('soft lip','P2 lips');dark=copy_mat('smile crease','P2 seam');hair=copy_mat('soft dark chestnut','P2 chestnut')
for p in hair.node_tree.nodes:
 if p.type=='BSDF_PRINCIPLED':p.inputs['Roughness'].default_value=.57
for o in face:
 if o!=head:bpy.data.objects.remove(o,do_unlink=True)
for s in [-1,1]:
 cx=s*.137;cy=-.234;cz=1.925
 ellipsoid('P2 sclera '+str(s),(cx,cy,cz),(.082,.057,.067),white,'Head',nu=48,nv=24)
 ellipsoid('P2 iris '+str(s),(cx-s*.002,-.290,cz+.002),(.030,.004,.034),iris,'Head',nu=48,nv=24)
 ellipsoid('P2 pupil '+str(s),(cx-s*.002,-.294,cz+.002),(.013,.0015,.018),pupil,'Head',nu=32,nv=20)
 ellipsoid('P2 glint '+str(s),(cx-.009,-.296,cz+.014),(.005,.001,.006),white,'Head',nu=24,nv=16)
 vs=[];fs=[];N=64;R=5
 for j in range(R):
  t=j/(R-1)
  for i in range(N):
   a=2*pi*i/N;rx=.076*(1-t)+.096*t;rz=(.054 if sin(a)>0 else .047)*(1-t)+.077*t;x=cx+rx*cos(a);z=cz+rz*sin(a)
   iy=cy-.057*sqrt(max(.02,1-(.076*cos(a)/.082)**2-((.054 if sin(a)>0 else .047)*sin(a)/.067)**2))-.001
   y=iy*(1-t)+(surface_y(x,z)+.002)*t-(.005 if sin(a)>0 else .0025)*sin(pi*t);vs.append((x,y,z))
 for j in range(R-1):
  for i in range(N):
   a=j*N+i;b=j*N+(i+1)%N;fs.append((a,a+N,b+N,b))
 o=mesh('P2 volumetric eyelids '+str(s),vs,fs,headmat,'Head');col=o.data.color_attributes.new(name='Complexion',type='FLOAT_COLOR',domain='POINT')
 for c in col.data:c.color=(.68,.36,.21,1)
 o.shape_key_add(name='Basis');key=o.shape_key_add(name='FH_Blink')
 for i,p in enumerate(key.data):
  t=(i//N)/(R-1);p.co.z=vs[i][2]*t+(cz-.004)*(1-t);p.co.y=vs[i][1]*t-.300*(1-t)
 vs=[];fs=[]
 for j in range(25):
  t=j/24;x=cx-.079+.158*t;z=2.024+.012*sin(pi*t)-s*.007*(t-.5);y=surface_y(x,z)-.004;w=.001+.005*sin(pi*t)**.6
  for i in range(10):
   a=2*pi*i/10;vs.append((x,y-.003*sin(a),z+w*cos(a)))
 for j in range(24):
  for i in range(10):
   a=j*10+i;b=j*10+(i+1)%10;fs.append((a,b,b+10,a+10))
 mesh('P2 brow '+str(s),vs,fs,hair,'Head')
 ear=ellipsoid('P2 ear '+str(s),(s*.322,.008,1.85),(.053,.038,.077),skin,'Head')
 for v in ear.data.vertices:
  x,y,z=v.co
  if y<.008:v.co.y+=.013*exp(-((z-1.85)/.035)**2-((x-s*.322)/.026)**2)
vs=[];fs=[];N=33;R=7
for j in range(R):
 t=j/(R-1)*2-1
 for i in range(N):
  u=i/(N-1);x=-.077+.154*u;z=1.736+.011*(x/.077)**2+t*.010*sin(pi*u)**.55;vs.append((x,surface_y(x,z)-.003-.004*(1-t*t)*sin(pi*u),z))
for j in range(R-1):
 for i in range(N-1):
  a=j*N+i;fs.append((a,a+1,a+N+1,a+N))
o=mesh('P2 lip volume',vs,fs,lip,'Head');o.shape_key_add(name='Basis');key=o.shape_key_add(name='FH_Smile')
for p in key.data:p.co.z+=.011*(abs(p.co.x)/.077)**1.7;p.co.y-=.001
vs=[];fs=[]
for i in range(33):
 u=i/32;x=-.074+.148*u;z=1.736+.011*(x/.077)**2
 for sign in [-1,1]:vs.append((x,surface_y(x,z)-.0075,z+sign*.0015*sin(pi*u)))
for i in range(32):fs.append((2*i,2*i+1,2*i+3,2*i+2))
o=mesh('P2 lip seam',vs,fs,dark,'Head');o.shape_key_add(name='Basis');key=o.shape_key_add(name='FH_Smile')
for p in key.data:p.co.z+=.011*(abs(p.co.x)/.077)**1.7
head.shape_key_add(name='Basis');key=head.shape_key_add(name='FH_Smile')
for p in key.data:
 x,y,z=p.co
 if y<-.15:p.co.z+=.004*exp(-((abs(x)-.17)/.08)**2-((z-1.78)/.08)**2)

# Layered hair guides, then a closed sculpt blockout to clean intersections.
vs=[];fs=[];NU=80;NV=28
for j in range(NV+1):
 t=j/NV
 for i in range(NU):
  u=2*pi*i/NU;p=t*(1.55-.51*sin(u)+.035*cos(3*u));vs.append((.323*sin(p)*cos(u),-.290*sin(p)*sin(u),1.865+.352*cos(p)))
for j in range(NV):
 for i in range(NU):
  a=j*NU+i;b=j*NU+(i+1)%NU;fs.append((a,b,b+NU,a+NU))
scalp=mesh('P2 scalp foundation',vs,fs,hair,'Head')
def bezier(points,t):
 a,b,c,d=[Vector(p)for p in points];return (1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d
locks=[
 ([(.13,.03,2.174),(.12,-.09,2.227),(-.08,-.235,2.153),(-.21,-.259,2.042)],.070,.022),
 ([(.22,.025,2.137),(.24,-.13,2.180),(.115,-.27,2.133),(-.015,-.304,2.064)],.064,.022),
 ([(.03,.09,2.187),(-.015,.015,2.224),(-.18,-.13,2.16),(-.27,-.19,2.044)],.062,.020),
 ([(.04,.15,2.165),(.17,.16,2.18),(.28,.04,2.115),(.31,-.10,1.974)],.053,.017),
 ([(-.09,.16,2.163),(-.20,.12,2.18),(-.29,-.015,2.095),(-.31,-.10,1.97)],.051,.016),
 ([(.12,.12,2.17),(.23,.22,2.12),(.27,.24,2.00),(.23,.26,1.90)],.055,.018),
 ([(-.05,.18,2.166),(-.12,.28,2.13),(-.20,.285,2.01),(-.20,.26,1.88)],.058,.019),
 ([(.01,.18,2.18),(.08,.30,2.12),(.10,.30,2.01),(.08,.294,1.90)],.058,.019),
 ([(.27,-.04,2.07),(.32,-.09,2.04),(.33,-.09,1.96),(.315,-.07,1.90)],.037,.012),
 ([(-.27,-.02,2.08),(-.32,-.07,2.02),(-.33,-.07,1.96),(-.314,-.055,1.90)],.037,.012)]
for index,(path,width,depth)in enumerate(locks):
 vs=[];fs=[];N=32;K=16
 for j in range(N+1):
  t=j/N;c=bezier(path,t)
  if c.y<0:
   w=min(1,max(0,-c.y/.10))*min(1,max(0,(2.205-c.z)/.05));w=w*w*(3-2*w);c.y=c.y*(1-w)+(surface_y(c.x,c.z)-.014)*w
  tangent=(bezier(path,min(1,t+.002))-bezier(path,max(0,t-.002))).normalized();normal=(c-Vector((0,0,1.86))).normalized();side=tangent.cross(normal).normalized();normal=side.cross(tangent).normalized();taper=(.25+.75*sin(pi*t)**.65)*(1-t)**.45+.002
  for i in range(K):
   a=2*pi*i/K;p=c+side*(cos(a)*width*taper)+normal*(sin(a)*depth*.5*taper*(1+.05*cos(3*a+3*t)));p.z=min(p.z,2.236);vs.append(p)
 for j in range(N):
  for i in range(K):
   a=j*K+i;b=j*K+(i+1)%K;fs.append((a,a+K,b+K,b))
 fs.extend([tuple(reversed(range(K))),tuple(N*K+i for i in range(K))]);mesh('P2 swept hair clump %02d'%index,vs,fs,hair,'Head')
guides=bpy.data.collections.new('02_P2_HAIR_RAW_GUIDES');scene.collection.children.link(guides);guides.hide_render=True;guides.hide_viewport=True
parts=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('P2 scalp foundation','P2 swept hair clump'))]
for o in parts:
 c=o.copy();c.data=o.data.copy();c.name='P2_GUIDE__'+o.name;guides.objects.link(c)
bpy.context.view_layer.objects.active=scalp
m=scalp.modifiers.new('scalp volume','SOLIDIFY');m.thickness=.008;m.offset=0;bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=scalp;bpy.ops.object.join();scalp.name='P2 layered hair sculpt blockout'
m=scalp.modifiers.new('clean layered intersections','REMESH');m.mode='VOXEL';m.voxel_size=.0035;m.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=m.name)
m=scalp.modifiers.new('sculpt relax','SMOOTH');m.factor=.35;m.iterations=3;bpy.ops.object.modifier_apply(modifier=m.name)
study=bpy.data.collections.new('01_P2_FACE_HAIR_EDIT');scene.collection.children.link(study)
for o in list(bpy.data.objects):
 if o.type=='MESH' and o.name.startswith('P2 ') and not o.name.startswith('P2_GUIDE__'):
  for c in list(o.users_collection):c.objects.unlink(o)
  study.objects.link(o)
  if 'Head' not in o.vertex_groups:o.vertex_groups.new(name='Head')
  o.vertex_groups['Head'].add(list(range(len(o.data.vertices))),1,'REPLACE')
  if not any(m.type=='ARMATURE'for m in o.modifiers):
   m=o.modifiers.new('unchanged Head binding','ARMATURE');m.object=rig
  o.parent=rig
locked=bpy.data.collections.new('03_C_BODY_OUTFIT_LOCKED');scene.collection.children.link(locked)
for n,h in body.items():
 o=bpy.data.objects[n];assert fp(o)==h,n
 for c in list(o.users_collection):c.objects.unlink(o)
 locked.objects.link(o);o.hide_select=True
assert rig_data()==before_rig
packed={}
for n in ['approval-front.png','approval-45.png','approval-profile.png','approval-back.png','approval-face.png','approval-kick.png']:
 p=os.path.join(args[1],n);assert os.path.isfile(p),p
 im=bpy.data.images.load(p,check_existing=False);im.name='C_REFERENCE_'+n;im.use_fake_user=True;im.pack();packed[n]=hashlib.sha256(open(p,'rb').read()).hexdigest()
text=bpy.data.texts.new('READ_ME_PHASE2_ARTIST.txt');text.write('Computed FACE/HAIR mesh study, not a professional hand-sculpt or approved 9/10 result. C reference and body/outfit are locked. 10 raw hair guides are hidden. P2 editable collection only. Original body, materials, skin weights, rig and action curves unchanged. Clean lid/lip loops and seams by hand; sculpt hair silhouette and retopology. FH_Blink/FH_Smile are static studies, not finished facial animation. No body/animation production before owner image approval.')
for name,pos in [('ART_Front',(0,-3.7,1.87)),('ART_45',(2.6,-2.6,1.87)),('ART_Profile',(3.7,0,1.87))]:
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,1.87))-o.location).to_track_quat('-Z','Y').to_euler();d.lens=55
scene.camera=bpy.data.objects['ART_Front']
for n,loc,power,size in [('ART_Key',(-2,-3,4),500,3),('ART_Fill',(3,-2,2.8),180,3),('ART_Rim',(1,2,3.5),400,2)]:
 d=bpy.data.lights.new(n,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(n,d);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,1.8))-o.location).to_track_quat('-Z','Y').to_euler()
scene.world=scene.world or bpy.data.worlds.new('ART world');scene.world.color=(.12,.12,.12)
bpy.ops.object.select_all(action='DESELECT');head.select_set(True);bpy.context.view_layer.objects.active=head
workbench=os.path.join(OUT,'bum07-facehair-workbench.blend');bpy.ops.wm.save_as_mainfile(filepath=workbench,compress=True)
live=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith(('C_REFERENCE__','P2_GUIDE__'))]
reports=[]
for lod,ratio in [('portrait',1),('mobile',.68)]:
 plain=[];morph=[]
 for o in live:
  c=o.copy();c.data=o.data.copy();c.hide_select=False;scene.collection.objects.link(c)
  if c.data.shape_keys:morph.append(c)
  else:
   if 'layered hair sculpt blockout' in o.name or (ratio<1 and len(c.data.polygons)>1500):
    tris=sum(max(0,len(p.vertices)-2)for p in c.data.polygons);budget=90000 if lod=='portrait' else 45000
    m=c.modifiers.new('runtime silhouette budget','DECIMATE');m.ratio=min(1,budget/max(1,tris)) if 'layered hair sculpt blockout' in o.name else ratio;bpy.context.view_layer.objects.active=c;bpy.ops.object.modifier_apply(modifier=m.name)
   plain.append(c)
 bpy.ops.object.select_all(action='DESELECT')
 for o in plain:o.select_set(True)
 bpy.context.view_layer.objects.active=plain[0];bpy.ops.object.join();merged=plain[0];merged.name='P2 combined body and details '+lod
 for o in morph:o.select_set(True)
 rig.select_set(True);bpy.context.view_layer.objects.active=rig
 dest=os.path.join(OUT,'bum07-facehair-'+lod+'.glb')
 bpy.ops.export_scene.gltf(filepath=dest,export_format='GLB',use_selection=True,use_active_scene=True,export_apply=False,export_animations=True,export_animation_mode='ACTIONS',export_anim_single_armature=True,export_force_sampling=True,export_frame_range=False,export_def_bones=True,export_morph=True,export_image_format='AUTO',export_extras=False,export_cameras=False,export_lights=False)
 reports.append({'lod':lod,'bytes':os.path.getsize(dest),'sha256':hashlib.sha256(open(dest,'rb').read()).hexdigest()})
 bpy.data.objects.remove(merged,do_unlink=True)
 for o in morph:bpy.data.objects.remove(o,do_unlink=True)
assert hashlib.sha256(open(source,'rb').read()).hexdigest()==source_sha
manifest={'phase':'2 face/hair only','artApproval':False,'score9Verified':False,'professionalHandSculpt':False,'originalCSourceSha256':source_sha,'workbenchSha256':hashlib.sha256(open(workbench,'rb').read()).hexdigest(),'bodyFingerprints':body,'rigAndActionsUnchanged':True,'packedCImages':packed,'hairGuides':10,'exports':reports,'limits':['Lid/lip seam topology and expression need artist cleanup','Hair sculpt blockout needs manual silhouette/roots/retopology','No body/outfit/animation production or physical iPhone approval']}
open(os.path.join(OUT,'manifest.json'),'w').write(json.dumps(manifest,indent=2)+'\n')
print('PHASE2_BUILD_COMPLETE',reports)
