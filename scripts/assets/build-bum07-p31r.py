"""P3.1R only: stitched socket/lid/cavity, contact-corrective blink, coordinated smile,
and a single sculpted hair volume. Never save over C/P2/P3.1. Blender 4.3.2."""
import bpy,bmesh,sys,math,json,hashlib,ast,struct
from pathlib import Path
from math import sin,cos,pi,sqrt,exp,atan2,asin
from mathutils import Vector
OUT=Path(sys.argv[sys.argv.index('--')+1]).resolve();OUT.mkdir(parents=True,exist_ok=True)
source=Path(bpy.data.filepath);sourceSha=hashlib.sha256(source.read_bytes()).hexdigest()
expected=json.loads(Path('research/bum07-p31/assets/manifest.json').read_text())['exports']['bum07-p31-workbench.blend']['sha256'];assert sourceSha==expected
assert OUT!=source.parent
scene=bpy.context.scene;rig=bpy.data.objects['BUM07 original rig study'];rig.animation_data.action=bpy.data.actions['Idle'];scene.frame_set(1)
# Trusted helper definitions only. Never executes P3.1 build or overwrites it.
mod=ast.parse(Path('scripts/assets/build-bum07-p31.py').read_text());defs=[n for n in mod.body if isinstance(n,ast.FunctionDef)and n.name in ['fingerprint','rig_state']];exec(compile(ast.Module(body=defs,type_ignores=[]),'fingerprint_helpers','exec'),globals())
original={o.name:fingerprint(o)for o in bpy.data.objects if o.type=='MESH'};rigBefore=rig_state()
old=bpy.data.collections['04_P31_PROCEDURAL_FACE_HAIR'];old.hide_render=True;old.hide_viewport=True
col=bpy.data.collections.new('05_P31R_FACIAL_STRUCTURE');scene.collection.children.link(col);new=[]
material=lambda n:bpy.data.materials['P31 '+n]
skin=material('skin');hair=material('chestnut');white=material('sclera');brown=material('iris');black=material('pupil');lip=material('subtle lips');crease=material('mouth seam')
# Same materials and studio as P3.1, no light/texture masking.
def mesh(name,vs,fs,mat,uvs=None):
 d=bpy.data.meshes.new('P31R '+name);d.from_pydata(vs,[],fs);d.update();o=bpy.data.objects.new('P31R '+name,d);col.objects.link(o);d.materials.append(mat)
 bm=bmesh.new();bm.from_mesh(d);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(d);bm.free()
 for f in d.polygons:f.use_smooth=True
 uv=d.uv_layers.new(name='UVMap')
 for f in d.polygons:
  for li in f.loop_indices:
   vi=d.loops[li].vertex_index;v=d.vertices[vi].co;uv.data[li].uv=uvs[vi]if uvs else((atan2(v.y,v.x)+pi)/(2*pi),(v.z-1.5)/.8)
 o.vertex_groups.new(name='Head').add(list(range(len(d.vertices))),1,'REPLACE');m=o.modifiers.new('unchanged Head binding','ARMATURE');m.object=rig;o.parent=rig;new.append(o);return o

def sphere(name,fn,mat,nu=48,nv=32):
 vs=[fn(0,0)];uv=[(.5,0)]
 for j in range(1,nv):
  for i in range(nu):vs.append(fn(2*pi*i/nu,pi*j/nv));uv.append((i/nu,j/nv))
 vs.append(fn(0,pi));uv.append((.5,1));fs=[]
 for i in range(nu):fs.append((0,1+i,1+(i+1)%nu))
 for j in range(nv-2):
  for i in range(nu):a=1+j*nu+i;b=1+j*nu+(i+1)%nu;fs.append((a,a+nu,b+nu,b))
 last=1+(nv-2)*nu
 for i in range(nu):fs.append((last+i,len(vs)-1,last+(i+1)%nu))
 return mesh(name,vs,fs,mat,uv)
# Keep actual ear/brow meshes unchanged in this facial-only repair.
for o in old.objects:
 if o.name.startswith(('P31 ear ','P31 soft brow ')):
  c=o.copy();c.data=o.data.copy();c.name=o.name.replace('P31 ','P31R ');col.objects.link(c);new.append(c)
H=.69;EX=.19*H;EZ=1.515+.56*H;CY=-.156;GLOBE=.089;CONTACT=.100
# Rebuild iris/pupil as curved patches seated on globe, no protruding flat lenses.
for s in [-1,1]:
 cx=s*EX;sphere('globe '+str(s),lambda u,v,cx=cx:(cx+GLOBE*sin(v)*cos(u),CY-GLOBE*sin(v)*sin(u),EZ+GLOBE*cos(v)),white,64,40)
 for name,rad,mat,depth in [('iris',.032,brown,.00025),('pupil',.014,black,.00055)]:
  # Closed thin disk with curved front/back and unique pole centers.
  def disk(u,v,cx=cx,rad=rad,depth=depth):
   r=rad*sin(v);x=r*cos(u);z=r*sin(u);front=sqrt(max(.0001,GLOBE*GLOBE-r*r));y=CY-front-depth+(.0005 if cos(v)<0 else 0)
   return(cx+x,y,EZ+z)
  # Rings run outward then inward on opposite thin hemisphere; pole is center.
  sphere(name+' '+str(s),disk,mat,48,24)
# Use original P3.1 head vertices/topology outside eyes; stitch every eyelid ring
# into the SAME mesh using original boundary indices. No overlapping lid overlay.
oldHead=bpy.data.objects['P31 reconstructed head with orbital recesses'];bm=bmesh.new();bm.from_mesh(oldHead.data)
remove=[f for f in bm.faces if f.calc_center_median().y<-.1 and any(((f.calc_center_median().x-s*EX)/.105)**2+((f.calc_center_median().z-EZ)/.078)**2<1 for s in [-1,1])]
bmesh.ops.delete(bm,geom=remove,context='FACES');bm.verts.ensure_lookup_table();bm.verts.index_update()
# Remove loose remnants, then each connected boundary is a single eye loop.
bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.verts.ensure_lookup_table();bm.verts.index_update()
vs=[tuple(v.co)for v in bm.verts];fs=[tuple(v.index for v in f.verts)for f in bm.faces];boundary={s:[]for s in [-1,1]}
for v in bm.verts:
 if any(e.is_boundary for e in v.link_edges):boundary[1 if v.co.x>0 else -1].append(v.index)
assert all(len(b)>32 for b in boundary.values());bm.free()
# Original analytic face surface without eyelid patch seams.
def faceY(x,z):
 rx=.3174*(1-.1*exp(-((z-1.60)/.10)**2));y=-.276*sqrt(max(.0001,1-(x/rx)**2-((z-1.86)/.345)**2))
 y+=sum(.044*exp(-((x-s*EX)/.075)**2-((z-EZ)/.060)**2)-.013*exp(-((x-s*.19)/.085)**2-((z-1.79)/.09)**2)for s in [-1,1])
 y-=.013*exp(-(x/.040)**2-((z-1.872)/.10)**2)+.047*exp(-(x/.041)**2-((z-1.812)/.032)**2)
 y-=.013*sum(exp(-((x-s*.034)/.019)**2-((z-1.794)/.021)**2)for s in [-1,1])+.009*exp(-(x/.09)**4-((z-1.721)/.040)**2)
 return y
# Records encode every appended ring vertex so all blink states can be solved
# from the same anatomy/contact equations rather than independent offsets.
records=[];socketInfo=[];OUTER={}
for s,ids in boundary.items():
 cx=s*EX;ids.sort(key=lambda i:atan2(vs[i][2]-EZ,vs[i][0]-cx));N=len(ids)
 angles=[atan2(vs[i][2]-EZ,vs[i][0]-cx)for i in ids]
 for idx,a in zip(ids,angles):
  # Preserve the actual cut boundary: pushing it past adjacent face rows
  # caused folded transition triangles in the first diagnostic build.
  OUTER[(s,a)]=vs[idx]
 rings=[ids];J=10;Q=18
 # Outer facial transition plus margin thickness on globe contact shell.
 for j in range(1,J+1):
  ring=[]
  for a in angles:
   ring.append(len(vs));vs.append((0,0,0));records.append((len(vs)-1,s,a,'lid',j/J))
  rings.append(ring)
 for j in range(1,Q):
  ring=[]
  for a in angles:
   ring.append(len(vs));vs.append((0,0,0));records.append((len(vs)-1,s,a,'cup',j/Q))
  rings.append(ring)
 for prev,nxt in zip(rings,rings[1:]):
  for i in range(N):fs.append((prev[i],prev[(i+1)%N],nxt[(i+1)%N],nxt[i]))
 pole=len(vs);vs.append((cx,CY+CONTACT,EZ))
 for i in range(N):fs.append((rings[-1][i],rings[-1][(i+1)%N],pole))
 socketInfo.append({'side':s,'boundaryVertices':N,'stitchedToHead':True,'contactRadius':CONTACT,'eyeballRadius':GLOBE})
def solve_record(rec,b):
 idx,s,a,kind,t=rec;cx=s*EX;contact=CONTACT+.006*b**8
 # Upper lid contributes 65%, lower 35%, contact seam 0.0008 overlap only
 # at full closure. Negative final aperture height is intentional lid contact.
 h=(.046 if sin(a)>=0 else .038)*(1-b)-.0008*b
 # Radial ellipse parameter keeps posterior cup azimuth well distributed
 # as aperture narrows, preventing long chords through the ocular volume.
 apertureR=1/sqrt((cos(a)/.079)**2+(sin(a)/max(abs(h),.00005))**2)
 ix=apertureR*cos(a);iz=apertureR*sin(a)*(1 if h>=0 else -1)-.006*b
 rr=sqrt(ix*ix+iz*iz);theta0=asin(min(.999,rr/contact));qy=CY-sqrt(max(.00001,contact*contact-rr*rr))
 if kind=='lid':
  outer=OUTER[(s,a)];x=outer[0]*(1-t)+(cx+ix)*t;z=outer[2]*(1-t)+(EZ+iz)*t
  radial=contact*contact-(x-cx)**2-(z-EZ)**2
  y=(1-t)*OUTER[(s,a)][1]+t*qy-.0015*sin(pi*t)
  if radial>0:y=min(y,CY-sqrt(radial)-.001)
  return(x,y,z)
 # Orbital lining remains behind the eyelid. Interpolate on the contact
 # sphere toward its NEUTRAL posterior direction, rather than everting the
 # whole cup with the contracting aperture (which created visible fins).
 nh=.046 if sin(a)>=0 else .038
 nr=1/sqrt((cos(a)/.079)**2+(sin(a)/nh)**2)
 nt=asin(min(.999,nr/CONTACT))+(pi-asin(min(.999,nr/CONTACT)))*t
 rest=Vector((cos(a)*sin(nt),-cos(nt),sin(a)*sin(nt)))
 rim=Vector((ix,qy-CY,iz)).normalized();k=min(1,t*4);k=k*k*(3-2*k)
 direction=(rim*(1-k)+rest*k).normalized();radius=contact*(1-k)+CONTACT*k
 return tuple(Vector((cx,CY,EZ))+direction*radius)
for rec in records:vs[rec[0]]=solve_record(rec,0)
head=mesh('unified head socket eyelid and orbital lining',vs,fs,skin);head.shape_key_add(name='Basis')
for b,label in [(.25,'FH_Blink25'),(.5,'FH_Blink50'),(.75,'FH_Blink75'),(1,'FH_Blink')]:
 k=head.shape_key_add(name=label)
 for rec in records:k.data[rec[0]].co=solve_record(rec,b)
# New vermilion volumes and a real mouth interior follow one smile map.
mouth=[];MZ=1.515+.285*H
for upper in [True,False]:
 def lp(u,v,upper=upper):
  t=(1+cos(v))/2;x=(t-.5)*.182;corner=.004*(abs(x)/.091)**2;cupid=.0015*cos(2*pi*t)*sin(pi*t)
  z=MZ+corner+((.006+cupid)if upper else -.008)*sin(pi*t)+.0045*sin(v)*cos(u)
  return(x,faceY(x,z)-.004-.004*sin(v)*sin(u),z)
 o=sphere('upper lip'if upper else 'lower lip',lp,lip,32,56);mouth.append(o)
def inner(u,v):
 t=(1+cos(v))/2;x=(t-.5)*.170;z=MZ+.004*(abs(x)/.091)**2+.0012*sin(v)*cos(u)
 return(x,faceY(x,z)-.0035-.0008*sin(v)*sin(u),z)
mouth.append(sphere('oral opening interior',inner,crease,32,56))
def smile_map(p,kind='head'):
 x,y,z=p;front=1 if y<-.12 else 0;w=front*exp(-((z-MZ)/.065)**2-(x/.145)**6);cheek=front*exp(-((abs(x)-.165)/.085)**2-((z-1.78)/.075)**2)
 xx=x*(1+.085*w);zz=z+.021*(min(abs(x)/.091,1.4))**1.8*w+.012*cheek;yy=y-.005*cheek
 if kind=='upper':zz+=.0035*max(0,1-(x/.091)**2)
 if kind=='lower':zz-=.005*max(0,1-(x/.091)**2)
 if kind=='inner':zz+=.006*sin(atan2(z-MZ,x)) if abs(z-MZ)>.0001 else 0
 return(xx,yy,zz)
head.shape_key_add(name='FH_Smile')
for p,v in zip(head.data.shape_keys.key_blocks['FH_Smile'].data,head.data.vertices):p.co=smile_map(v.co)
for o in mouth:
 o.shape_key_add(name='Basis');k=o.shape_key_add(name='FH_Smile');kind='upper'if 'upper' in o.name else 'lower'if 'lower' in o.name else 'inner'
 for p,v in zip(k.data,o.data.vertices):p.co=smile_map(v.co,kind)
# A SINGLE closed sculpted mass: volumetric lobes change the silhouette and
# scalloped hairline itself; no leaf strips laid onto a uniform cap.
N=112;J=40;hv=[];uv=[]
def hairpoint(u,t,inside):
 front=max(0,sin(u));limit=1.70-.70*front+front*(.12*cos(u)+.09*cos(3*u+.8)+.04*cos(7*u+.3))+.02*sin(3*u)
 phi=.008+t*(limit-.008);twist=.55*(1-t)*front;uu=u+twist
 lobes=0
 for center,amp,spread in [(.55,.025,.40),(1.3,.033,.42),(2.10,.026,.42),(2.85,.020,.48),(3.7,.015,.5),(4.7,.019,.6),(5.6,.016,.4)]:
  du=atan2(sin(uu-center),cos(uu-center));lobes+=amp*exp(-(du/spread)**2)*sin(pi*min(1,t*1.12))**.65
 groove=.0035*cos(8*uu+2*t)*sin(pi*t)**2
 for seam in [.72,1.38,2.15,2.90,3.8,4.8,5.7]:
  du=atan2(sin(uu-seam-.13*t),cos(uu-seam-.13*t));groove-=.012*exp(-(du/.055)**2)*max(0,sin(pi*t))**.45
 offset=max(.002,(lobes+groove)*(1 if not inside else .20))
 rX=.323+offset-(.006 if inside else 0);rY=.283+offset-(.006 if inside else 0);rZ=.349+offset-(.006 if inside else 0)
 return(rX*sin(phi)*cos(uu),-rY*sin(phi)*sin(uu),1.86+rZ*cos(phi))
for inside in [False,True]:
 for j in range(J):
  for i in range(N):hv.append(hairpoint(2*pi*i/N,j/(J-1),inside));uv.append((i/N,j/(J-1)))
hf=[];K=N*J
for layer in [0,1]:
 for j in range(J-1):
  for i in range(N):a=layer*K+j*N+i;b=layer*K+j*N+(i+1)%N;hf.append((a,b,b+N,a+N))
for i in range(N):a=(J-1)*N+i;b=(J-1)*N+(i+1)%N;hf.append((a,b,b+K,a+K))
hf.extend([tuple(reversed(range(N))),tuple(K+i for i in range(N))]);mesh('continuous lobed hair with scalloped hairline',hv,hf,hair,uv)
# Retain new meshes only; keep every original mesh in its original collection.
for n,h in original.items():assert fingerprint(bpy.data.objects[n])==h,n
assert rigBefore==rig_state()
text=bpy.data.texts.new('P31R_README');text.write('P3.1R Facial Structure Repair only. Original C/P2/P3.1 intact hidden. Socket/lid/orbital lining stitched to a single head mesh. Blink knots 0/25/50/75/100 use piecewise mapping; FH_Blink is 100. Smile coordinates head cheeks lips and oral interior. Full closure uses 0.0016 contact overlap at lid seam, not globally intersection-free. Hair is one sculpted lobed volume. No art approval or iPhone claims. See contact audit before claiming Blink PASS. No P3.2.')
work=OUT/'bum07-p31r-workbench.blend';bpy.ops.wm.save_as_mainfile(filepath=str(work),compress=True)
bpy.ops.object.select_all(action='DESELECT')
for o in new+list(bpy.data.collections['03_C_BODY_OUTFIT_LOCKED'].objects):
 if o.type=='MESH':o.hide_select=False;o.select_set(True)
rig.select_set(True);bpy.context.view_layer.objects.active=rig
asset=OUT/'bum07-p31r-experimental.glb'
bpy.ops.export_scene.gltf(filepath=str(asset),export_format='GLB',use_selection=True,export_apply=False,export_animations=True,export_animation_mode='ACTIONS',export_anim_single_armature=True,export_force_sampling=True,export_frame_range=False,export_def_bones=True,export_morph=True,export_extras=False,export_cameras=False,export_lights=False)
assert sourceSha==hashlib.sha256(source.read_bytes()).hexdigest()
report={'version':'P3.1R','baselineCommit':'def4314','sourceSha256':sourceSha,'sourceUnchanged':True,'originalMeshCount':len(original),'originalMeshesUnchanged':True,'rigActionsUnchanged':True,'sockets':socketInfo,'originalFingerprints':original,'newObjects':[o.name for o in new],'blinkMapping':{'knots':[0,.25,.5,.75,1],'keys':['Basis','FH_Blink25','FH_Blink50','FH_Blink75','FH_Blink'],'interpolation':'linear between adjacent absolute-pose morphs; Basis at0'},'artApproved':False,'physicalIPhone':False,'nextPhase':'blocked until owner review','limits':['Intentional lid-seam contact overlap at full closure; no global self-intersection-free certificate','Analytic shared-eye contact model must be checked on exported GLB too','Parametric UVs are not certified production bake layout'],'exports':{p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}for p in [work,asset]}}
(OUT/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('P31R_BUILD_COMPLETE',len(new),'objects; no art approval')
