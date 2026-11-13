"""P3.1 isolated procedural reconstruction. No C/P2 edits, no art approval.
Blender 4.3.2 -b --disable-autoexec BASELINE.blend -P this.py -- OUTPUT
"""
import bpy,bmesh,sys,os,json,math,hashlib,struct
from math import sin,cos,pi,sqrt,exp,atan2,acos
from mathutils import Vector
from pathlib import Path
OUT=Path(sys.argv[sys.argv.index('--')+1]).resolve();OUT.mkdir(parents=True,exist_ok=True)
source=Path(bpy.data.filepath);source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
assert source_hash=='30338d105c61eb206b688d31d74f9a7ccd947607f7ad67a5aff89833a8cb2f4c'
scene=bpy.context.scene;rig=bpy.data.objects['BUM07 original rig study'];rig.animation_data.action=bpy.data.actions['Idle'];scene.frame_set(1)
# Body snapshots include vertex/UV/material/group data; no object is rescaled.
def fingerprint(o):
 h=hashlib.sha256()
 for v in o.data.vertices:
  h.update(struct.pack('<3f',*v.co))
  for g in v.groups:h.update(struct.pack('<If',g.group,g.weight))
 for p in o.data.polygons:h.update(str(tuple(p.vertices)).encode())
 for uv in o.data.uv_layers:
  for d in uv.data:h.update(struct.pack('<2f',*d.uv))
 h.update(str([(m.name,list(m.diffuse_color))for m in o.data.materials]).encode())
 return h.hexdigest()
def rig_state():
 return {'bones':[(b.name,list(b.matrix_local[0]),list(b.matrix_local[1]),list(b.matrix_local[2]),list(b.matrix_local[3]),b.parent.name if b.parent else None)for b in rig.data.bones], 'actions':[(a.name,[(f.data_path,f.array_index,[(list(k.co),k.interpolation)for k in f.keyframe_points])for f in a.fcurves])for a in bpy.data.actions]}
bodycol=bpy.data.collections['03_C_BODY_OUTFIT_LOCKED'];body={o.name:fingerprint(o)for o in bodycol.objects if o.type=='MESH'};before_rig=rig_state()
# Retain all source collections and geometry; hide P2 in NEW file only.
p2=bpy.data.collections['01_P2_FACE_HAIR_EDIT'];p2.hide_render=True;p2.hide_viewport=True
col=bpy.data.collections.new('04_P31_PROCEDURAL_FACE_HAIR');scene.collection.children.link(col)
new=[]
def material(name,rgba,rough):
 m=bpy.data.materials.new('P31 '+name);m.diffuse_color=(*rgba,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgba,1);p.inputs['Roughness'].default_value=rough;return m
skin=material('skin',(.68,.36,.21),.52);hair=material('chestnut',(.025,.012,.008),.57);white=material('sclera',(.88,.85,.77),.26);brown=material('iris',(.11,.044,.012),.28);black=material('pupil',(.004,.003,.002),.23);lip=material('subtle lips',(.53,.235,.16),.58);crease=material('mouth seam',(.24,.075,.042),.7)
def mesh(name,vs,fs,mat,uvcoords=None):
 d=bpy.data.meshes.new('P31 '+name);d.from_pydata(vs,[],fs);d.update();o=bpy.data.objects.new('P31 '+name,d);col.objects.link(o);d.materials.append(mat)
 bm=bmesh.new();bm.from_mesh(d);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(d);bm.free()
 for p in d.polygons:p.use_smooth=True
 uv=d.uv_layers.new(name='UVMap')
 for p in d.polygons:
  for li in p.loop_indices:
   vi=d.loops[li].vertex_index;v=d.vertices[vi].co
   uv.data[li].uv=uvcoords[vi] if uvcoords else ((atan2(v.y,v.x)+pi)/(2*pi),(v.z-1.5)/.8)
 g=o.vertex_groups.new(name='Head');g.add(list(range(len(vs))),1,'REPLACE');m=o.modifiers.new('Original Head skin binding','ARMATURE');m.object=rig;o.parent=rig;new.append(o);return o
# Closed sphere topology: unique poles, quads in rings, triangles only at poles.
def sphere(name,fn,mat,nu=96,nv=64):
 vs=[fn(0,0)];uv=[(.5,0)]
 for j in range(1,nv):
  for i in range(nu):vs.append(fn(2*pi*i/nu,pi*j/nv));uv.append((i/nu,j/nv))
 vs.append(fn(0,pi));uv.append((.5,1));fs=[]
 for i in range(nu):fs.append((0,1+i,1+(i+1)%nu))
 for j in range(nv-2):
  for i in range(nu):a=1+j*nu+i;b=1+j*nu+(i+1)%nu;fs.append((a,a+nu,b+nu,b))
 last=1+(nv-2)*nu;bottom=len(vs)-1
 for i in range(nu):fs.append((last+i,bottom,last+(i+1)%nu))
 return mesh(name,vs,fs,mat,uv)
def ellipsoid(name,c,r,mat,nu=48,nv=32):return sphere(name,lambda u,v:(c[0]+r[0]*sin(v)*cos(u),c[1]-r[1]*sin(v)*sin(u),c[2]+r[2]*cos(v)),mat,nu,nv)
H=.69;zc=1.86;rx=.3174;rz=.345;ry=.276;eyeZ=1.515+.56*H;eyeX=.19*H
# Continuous front-surface field. Gaussian volumes are evaluated on a NEW dense
# parametric topology, not copied P2 vertices. Socket concavities are integral.
def feature(x,z):
 sockets=sum(.044*exp(-((x-s*eyeX)/.075)**2-((z-eyeZ)/.060)**2)for s in [-1,1])
 cheeks=sum(-.013*exp(-((x-s*.19)/.085)**2-((z-1.79)/.09)**2)for s in [-1,1])
 bridge=-.013*exp(-(x/.040)**2-((z-1.872)/.10)**2)
 tip=-.047*exp(-(x/.041)**2-((z-1.812)/.032)**2)
 alar=-.013*sum(exp(-((x-s*.034)/.019)**2-((z-1.794)/.021)**2)for s in [-1,1])
 muzzle=-.009*exp(-(x/.09)**4-((z-1.721)/.040)**2)
 philtrum=.002*exp(-(x/.009)**2-((z-1.748)/.019)**2)
 lips=-.004*exp(-(x/.078)**6-((z-1.712)/.014)**2)
 return sockets+cheeks+bridge+tip+alar+muzzle+philtrum+lips
# Soft jaw reduction; skull/head height and current neck meeting point retained.
def width(z):return rx*(1-.10*exp(-((z-1.60)/.10)**2))
def faceY(x,z):return -ry*sqrt(max(.0001,1-(x/width(z))**2-((z-zc)/rz)**2))+feature(x,z)
def headpoint(u,v):
 z=zc+rz*cos(v);x=width(z)*sin(v)*cos(u);y=-ry*sin(v)*sin(u)
 if sin(u)>0:y+=feature(x,z)
 return (x,y,z)
head=sphere('reconstructed head with orbital recesses',headpoint,skin,192,128)
head.shape_key_add(name='Basis');smile=head.shape_key_add(name='FH_Smile')
for p in smile.data:
 x,y,z=p.co
 if y<-.1:p.co.z+=.009*exp(-((abs(x)-.15)/.09)**2-((z-1.75)/.075)**2)
# Eye globe enclosed by recessed facial field; thick independent annular lids.
for s in [-1,1]:
 cx=s*eyeX;cy=-.156;cz=eyeZ;R=.089
 ellipsoid('globe '+str(s),(cx,cy,cz),(R,R,R),white,64,40)
 ellipsoid('iris '+str(s),(cx,-.2448,cz+.001),(.033,.0025,.033),brown)
 ellipsoid('pupil '+str(s),(cx,-.2473,cz+.001),(.014,.001,.017),black)
 ellipsoid('catchlight '+str(s),(cx-.010,-.2485,cz+.013),(.004,.0008,.004),white,24,16)
 vs=[];uv=[];N=96;J=8
 # Two annuli plus inner/outer walls = closed thick band, not a single patch.
 for back in [False,True]:
  for j in range(J):
   t=j/(J-1)
   for i in range(N):
    a=2*pi*i/N;ix=.079*cos(a);iz=(.045 if sin(a)>=0 else .037)*sin(a)
    x=cx+(1-t)*ix+t*.107*cos(a);z=cz+(1-t)*iz+t*.063*sin(a)
    innerY=cy-sqrt(max(.00002,R*R-ix*ix-iz*iz))-.0015
    y=(1-t)*innerY+t*(faceY(x,z)+.001)-(.003 if sin(a)>0 else .0015)*sin(pi*t)
    globeTerm=R*R-(x-cx)**2-(z-cz)**2
    if globeTerm>0:y=min(y,cy-sqrt(globeTerm)-.0025)
    if back:y+=.004
    vs.append((x,y,z));uv.append((i/N,t*.5+(.5 if back else 0)))
 fs=[];K=N*J
 for layer in [0,1]:
  for j in range(J-1):
   for i in range(N):a=layer*K+j*N+i;b=layer*K+j*N+(i+1)%N;fs.append((a,a+N,b+N,b))
 for row in [0,J-1]:
  for i in range(N):a=row*N+i;b=row*N+(i+1)%N;fs.append((a,b,b+K,a+K))
 lid=mesh('thick orbital lid '+str(s),vs,fs,skin,uv);lid.shape_key_add(name='Basis');key=lid.shape_key_add(name='FH_Blink')
 for i,p in enumerate(key.data):
  t=((i%K)//N)/(J-1);x,y,z=vs[i];p.co.z=z*t+(cz-.002+.0006*sin(2*pi*(i%N)/N))*(1-t)
  p.co.y=y*t+(-.249+(.004 if i>=K else 0))*(1-t)
 # Flattened brow crescent built as a closed lenticular surface, tapered ends.
 def browpoint(u,v):
  t=(cos(v)+1)/2;x=cx+(.5-t)*.170;z=1.515+.675*H+.014*sin(pi*t)
  return (x,faceY(x,z)-.003-.003*sin(v)*sin(u),z+.0048*sin(v)*cos(u))
 sphere('soft brow '+str(s),browpoint,hair,24,40)
 # Ear anatomy remains simple but closed; not a body-scope change.
 ear=ellipsoid('ear '+str(s),(s*.319,.005,1.85),(.042,.031,.067),skin)
 for v in ear.data.vertices:
  if v.co.y<.005:v.co.y+=.010*exp(-((v.co.z-1.85)/.035)**2-((v.co.x-s*.319)/.025)**2)
# Closed thin lip volumes hug integrated muzzle. Full horizontal rings taper at
# the corners. Geometry, not a painted smile; remain separate for rig study.
for upper in [True,False]:
 def lp(u,v):
  t=(cos(v)+1)/2;x=(t-.5)*.172;seam=1.515+.285*H+.003*(abs(x)/.086)**2
  z=seam+(.0035 if upper else -.0045)*sin(pi*t)+.0036*sin(v)*cos(u)
  y=faceY(x,z)-.0025-.0027*sin(v)*sin(u)
  return(x,y,z)
 ob=sphere('upper lip' if upper else 'lower lip',lp,lip,24,64);ob.shape_key_add(name='Basis');key=ob.shape_key_add(name='FH_Smile')
 for p in key.data:p.co.z+=.009*(abs(p.co.x)/.086)**1.5
# Seam is a fine volume, not a wide black graphic stroke.
def seamP(u,v):
 t=(cos(v)+1)/2;x=(t-.5)*.164;z=1.515+.285*H+.003*(abs(x)/.086)**2
 return(x,faceY(x,z)-.006-.0006*sin(v)*sin(u),z+.0007*sin(v)*cos(u))
sphere('subtle mouth contact',seamP,crease,16,64)
# Scalp is a closed, double-layer surface with a shaped hairline. Roots of
# leaf clumps sink into this base, while their midsections rise and separate.
N=96;J=32;vs=[];uv=[]
def scalpPoint(u,t,inside=False):
 front=max(0,sin(u));bound=1.66-.72*front+.028*cos(5*u);p=.01+t*(bound-.01)
 off=-.010 if inside else 0
 return((.326+off)*sin(p)*cos(u),-(.287+off)*sin(p)*sin(u),1.86+(.352+off)*cos(p))
for inside in [False,True]:
 for j in range(J):
  for i in range(N):vs.append(scalpPoint(2*pi*i/N,j/(J-1),inside));uv.append((i/N,j/(J-1)))
fs=[];K=N*J
for layer in [0,1]:
 for j in range(J-1):
  for i in range(N):a=layer*K+j*N+i;b=layer*K+j*N+(i+1)%N;fs.append((a,b,b+N,a+N))
for row in [0,J-1]:
 for i in range(N):a=row*N+i;b=row*N+(i+1)%N;fs.append((a,b,b+K,a+K))
# Tiny central top openings are capped with planar n-gons (non-degenerate).
fs.extend([tuple(reversed(range(N))),tuple(K+i for i in range(N))])
# Top annulus wall would double cap; remove that wall before capping.
fs=fs[:2*(J-1)*N]+fs[2*(J-1)*N+N:]
scalp=mesh('shaped scalp foundation',vs,fs,hair,uv)
def bez(p,t):a,b,c,d=map(Vector,p);return a*(1-t)**3+3*b*(1-t)**2*t+3*c*(1-t)*t*t+d*t**3
paths=[
 ([(.14,.02,2.196),(.13,-.09,2.278),(-.12,-.245,2.175),(-.224,-.245,2.055)],.079,.025),
 ([(.20,.02,2.165),(.24,-.09,2.236),(.10,-.265,2.159),(-.015,-.286,2.059)],.070,.021),
 ([(.045,.08,2.197),(-.05,.035,2.266),(-.24,-.11,2.166),(-.29,-.145,2.035)],.072,.022),
 ([(.14,.10,2.168),(.25,.13,2.19),(.31,-.015,2.06),(.31,-.10,1.959)],.054,.017),
 ([(-.065,.13,2.173),(-.21,.12,2.18),(-.30,-.01,2.05),(-.31,-.075,1.953)],.053,.016),
 ([(.1,.14,2.167),(.23,.21,2.12),(.265,.24,1.995),(.235,.24,1.87)],.060,.018),
 ([(-.07,.16,2.163),(-.18,.23,2.12),(-.24,.25,1.99),(-.21,.24,1.865)],.062,.018),
 ([(0,.18,2.165),(.06,.28,2.10),(.10,.29,1.97),(.08,.27,1.825)],.061,.017)]
for idx,(points,w,d)in enumerate(paths):
 # Leaf surface: explicit convex upper sheet and shallow concave underside,
 # each with broad lateral width, sculpted ridges and naturally tapered tip.
 vs=[];uv=[];L=48;W=16
 for bottom in [False,True]:
  for j in range(L):
   t=j/(L-1);c=bez(points,t);tangent=(bez(points,min(1,t+.001))-bez(points,max(0,t-.001))).normalized();normal=(c-Vector((0,0,1.86))).normalized();side=tangent.cross(normal).normalized();normal=side.cross(tangent).normalized()
   taper=(.18+.82*max(0,sin(pi*t))**.60)*(1-.50*t)
   for i in range(W):
    u=2*i/(W-1)-1;arch=max(0,1-u*u)
    groove=1-.10*cos((u+1)*3*pi+.5*t)*arch
    depth=(-.005 if bottom else d*arch**.7*groove)*taper
    raw=c+side*(u*w*taper);delta=raw-Vector((0,0,1.86))
    # Project each leaf's underside onto scalp ellipsoid: visible roots no
    # longer float on the unbounded Bezier arch. Thickness creates the lift.
    scale=sqrt((delta.x/.326)**2+(delta.y/.287)**2+(delta.z/.352)**2)
    base=Vector((0,0,1.86))+delta/scale;radial=Vector((delta.x/.326**2,delta.y/.287**2,delta.z/.352**2)).normalized()
    p=base+radial*((-.004 if bottom else .003+depth)*taper)
    vs.append(p);uv.append((i/(W-1),t))
 fs=[];K=L*W
 for lay in [0,1]:
  for j in range(L-1):
   for i in range(W-1):a=lay*K+j*W+i;fs.append((a,a+1,a+W+1,a+W))
 for j in range(L-1):
  for i in [0,W-1]:a=j*W+i;b=(j+1)*W+i;fs.append((a,b,b+K,a+K))
 for j in [0,L-1]:
  for i in range(W-1):a=j*W+i;b=a+1;fs.append((a,b,b+K,a+K))
 mesh('layered sculpt leaf %02d'%idx,vs,fs,hair,uv)
# Independent component manifold audit; inter-object overlaps are NOT covered.
report=[]
for o in new:
 bm=bmesh.new();bm.from_mesh(o.data)
 row={'name':o.name,'vertices':len(bm.verts),'faces':len(bm.faces),'quads':sum(len(f.verts)==4 for f in bm.faces),'boundaryEdges':sum(e.is_boundary for e in bm.edges),'nonManifoldEdges':sum(not e.is_manifold for e in bm.edges),'inconsistentNormals':sum(e.is_manifold and not e.is_contiguous for e in bm.edges),'degenerateFaces':sum(f.calc_area()<1e-12 for f in bm.faces),'signedVolume':bm.calc_volume(signed=True),'uvFinite':all(math.isfinite(x)for d in o.data.uv_layers.active.data for x in d.uv),'headWeightComplete':all(len(v.groups)>0 for v in o.data.vertices),'morphs':list(o.data.shape_keys.key_blocks.keys())if o.data.shape_keys else []}
 bm.free();assert row['boundaryEdges']==0 and row['nonManifoldEdges']==0 and row['degenerateFaces']==0 and row['inconsistentNormals']==0,row
 assert row['uvFinite'] and row['headWeightComplete'];report.append(row)
assert body=={n:fingerprint(bpy.data.objects[n])for n in body};assert before_rig==rig_state()
notes=bpy.data.texts.new('P31_README');notes.write('P3.1 unapproved procedural study. New analytic closed head/socket field; thick closed eyelids; eight broad layered leaf clumps. C/P2 collections retained hidden; original body and rig unchanged. Inspect independent overlapping parts: manifold per component is not a watertight unified head, not finished animation retopology. No 9/10 claim, no iPhone FPS. Do not progress to P3.2 without owner approval.')
# Source saves with originals editable and new reconstruction separated.
work=OUT/'bum07-p31-workbench.blend';bpy.ops.wm.save_as_mainfile(filepath=str(work),compress=True)
bpy.ops.object.select_all(action='DESELECT')
for o in new+list(bodycol.objects):
 if o.type=='MESH':o.hide_select=False;o.select_set(True)
rig.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.gltf(filepath=str(OUT/'bum07-p31-experimental.glb'),export_format='GLB',use_selection=True,export_apply=False,export_animations=True,export_animation_mode='ACTIONS',export_anim_single_armature=True,export_force_sampling=True,export_frame_range=False,export_def_bones=True,export_morph=True,export_extras=False,export_cameras=False,export_lights=False)
assert source_hash==hashlib.sha256(source.read_bytes()).hexdigest()
manifest={'version':'P3.1','baselineCommit':'47cfa8c','sourceSha256':source_hash,'sourceUnchanged':True,'bodyFingerprints':body,'rigStateSha256':hashlib.sha256(json.dumps(before_rig,sort_keys=True).encode()).hexdigest(),'newComponents':report,'outsideScopeMeshesUnchanged':len(body),'rigActionsUnchanged':True,'professionalHandSculpt':False,'artApproved':False,'quality9Verified':False,'physicalIPhoneTested':False,'limits':['Individual components are closed but intersect at roots/lids/lips; no inter-object self-intersection certificate','Parametric UVs are finite, not production UDIM or verified nonoverlapping bake layout','Head-weight binding is retained; facial targets are studies, not production facial rig','Body/cloth sports deformation known from C remains outside scope','No P3.2 before owner approval'],'exports':{p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}for p in [work,OUT/'bum07-p31-experimental.glb']}}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('P31_BUILD_PASS',len(new),'new closed meshes; no art approval')
