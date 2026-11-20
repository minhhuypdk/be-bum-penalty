"""P5.3B.1 bounded artistic head study. Load R, retain only a shoulder bust,
replace head/ear/hair topology, never invoke the full-character builder.
All reference/history files are read-only. No body refinement, rig or GLB.
"""
import bpy,bmesh,math,json,hashlib,shutil
import numpy as np
from mathutils import Vector,Matrix,geometry
from pathlib import Path
from math import sin,cos,pi,sqrt,exp,atan2
R=Path(__file__).resolve().parents[1];BASE=R.parent/'p53ar-bum07-refinement';SOURCE=BASE/'bum07-p53ar-refinement.blend';(R/'reference').mkdir(exist_ok=True)
shutil.copy2(SOURCE,R/'reference/bum07-p53ar-preserved.blend');source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(SOURCE));s=bpy.context.scene
# Only the existing neck and upper jersey are retained as context, not finished.
retain={'Neck_blockout','Jersey_body_open_neck','Front_V_back_round_collar','Front_raglan_R','Front_raglan_L','Back_raglan_R','Back_raglan_L','Front_BUM'}
removed=[]
for o in list(s.objects):
 if any(c.name.startswith('BUM07') for c in o.users_collection) and o.name not in retain:removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
for name in ['Jersey_body_open_neck','Front_raglan_R','Front_raglan_L','Back_raglan_R','Back_raglan_L']:
 o=bpy.data.objects.get(name)
 if not o:continue
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 for mod in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
 bm=bmesh.new();bm.from_mesh(o.data);ret=bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,3.40),plane_no=(0,0,1),clear_inner=True,clear_outer=False);bm.to_mesh(o.data);bm.free();o.data.update()
# No full-body geometry exists in this new study; the exact old file remains preserved separately.
C=bpy.data.collections.new('BUM07_B1_HEAD_SCULPT');s.collection.children.link(C);H=bpy.data.collections.new('BUM07_B1_HAIR_SCULPT');s.collection.children.link(H)
def put(o,col=C):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);return o
def srgb(h):
 cs=[int(h[i:i+2],16)/255 for i in (1,3,5)];return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in cs)+(1,)
def mat(n,hex,rough=.55):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=srgb(hex);m.diffuse_color=srgb(hex);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=0;m['palette_anchor']=hex;return m
skin=mat('B1_skin_palette_anchor','#D9A078',.56);p=skin.node_tree.nodes['Principled BSDF'];p.inputs['Subsurface Weight'].default_value=.09;p.inputs['Subsurface Radius'].default_value=(1,.45,.25);p.inputs['Subsurface Scale'].default_value=.018;p.inputs['Specular IOR Level'].default_value=.25
# Micro-normal is secondary; facial forms and topology below are rebuilt explicitly.
noise=skin.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=180;noise.inputs['Detail'].default_value=2
bump=skin.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.10;bump.inputs['Distance'].default_value=.00018;skin.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);skin.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
headmat=skin.copy();headmat.name='B1_head_skin_with_soft_lip_cheek_tint';attr=headmat.node_tree.nodes.new('ShaderNodeVertexColor');attr.layer_name='BUM_SkinTint';headmat.node_tree.links.new(attr.outputs['Color'],headmat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
white=mat('B1_sclera','#EFE7DA',.28);white.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value=.18
iris=mat('B1_brown_iris_palette_anchor','#4E331D',.28);p=iris.node_tree.nodes['Principled BSDF'];p.inputs['Specular IOR Level'].default_value=.18;p.inputs['Coat Weight'].default_value=.12;p.inputs['Coat Roughness'].default_value=.07
uv=iris.node_tree.nodes.new('ShaderNodeTexCoord');dist=iris.node_tree.nodes.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=(.5,.5,0);iris.node_tree.links.new(uv.outputs['UV'],dist.inputs[0]);ramp=iris.node_tree.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1]);e=ramp.color_ramp.elements[0];e.position=.16;e.color=srgb('#61432A')
for pos,color in [(.32,'#574026'),(.45,'#4E331D'),(.50,'#38271D')]:e=ramp.color_ramp.elements.new(pos);e.color=srgb(color)
iris.node_tree.links.new(dist.outputs['Value'],ramp.inputs['Fac']);tex=iris.node_tree.nodes.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=28;tex.inputs['Detail'].default_value=2;iris.node_tree.links.new(uv.outputs['UV'],tex.inputs['Vector']);nr=iris.node_tree.nodes.new('ShaderNodeMapRange');nr.inputs['To Min'].default_value=.89;nr.inputs['To Max'].default_value=1.05;iris.node_tree.links.new(tex.outputs['Fac'],nr.inputs['Value']);mix=iris.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;iris.node_tree.links.new(ramp.outputs['Color'],mix.inputs[1]);iris.node_tree.links.new(nr.outputs['Result'],mix.inputs[2]);iris.node_tree.links.new(mix.outputs[0],p.inputs['Base Color'])
pupil=mat('B1_pupil','#100E0C',.25);pupil.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value=.2
hairmat=mat('B1_hair_palette_anchor','#241D1A',.58);p=hairmat.node_tree.nodes['Principled BSDF'];p.inputs['Specular IOR Level'].default_value=.18;
if 'Anisotropic' in p.inputs:p.inputs['Anisotropic'].default_value=.2
browmat=mat('B1_brow','#30221A',.70);seammat=mat('B1_lip_seam','#815544',.65);tear=mat('B1_tear_corner','#C68E73',.42)
def mesh(name,v,f,ma,col=C):
 d=bpy.data.meshes.new(name);d.from_pydata(v,[],f);d.update();o=bpy.data.objects.new(name,d);col.objects.link(o);d.materials.append(ma)
 for p in d.polygons:p.use_smooth=True
 return o
def sphere(name,loc,r,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=40,location=loc);o=put(bpy.context.object);o.name=name;o.scale=(r,r,r);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma)
 for p in o.data.polygons:p.use_smooth=True
 return o
def curve(name,points,r,ma):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=12;d.bevel_depth=r;d.bevel_resolution=3;sp=d.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,d);C.objects.link(o);d.materials.append(ma);return o
W=[(4,.055),(4.035,.14),(4.10,.225),(4.22,.285),(4.36,.344),(4.50,.369),(4.66,.370),(4.82,.33),(4.93,.22),(5,.001)]
FD=[(4,.005),(4.06,.095),(4.22,.274),(4.36,.307),(4.54,.330),(4.73,.305),(4.9,.22),(5,.001)]
BD=[(4,.12),(4.15,.23),(4.40,.355),(4.65,.39),(4.85,.32),(4.96,.15),(5,.001)]
def interp(z,knots):
 if z<=knots[0][0]:return knots[0][1]
 for i,((a,va),(b,vb)) in enumerate(zip(knots,knots[1:])):
  if z<=b:
   t=(z-a)/(b-a);left=knots[max(0,i-1)];right=knots[min(len(knots)-1,i+2)];ma=(vb-left[1])/(b-left[0]);mb=(right[1]-va)/(right[0]-a)
   return max(.001,(2*t**3-3*t*t+1)*va+(t**3-2*t*t+t)*(b-a)*ma+(-2*t**3+3*t*t)*vb+(t**3-t*t)*(b-a)*mb)
 return knots[-1][1]
def ga(x,z,cx,cz,sx,sz):return exp(-((x-cx)/sx)**2-((z-cz)/sz)**2)
def seamz(x):return 4.205+.024*(min(1,abs(x)/.18))**1.65
def seam_y(z):return -.16*exp(-((z-4.0)/.060)**2)
def fy(x,z):
 w=interp(z,W);edge=max(0,1-(abs(x)/w)**3.1)**.52;depth=interp(z,FD);y=seam_y(z)-depth*edge
 y-=edge*(.054*ga(x,z,0,4.355,.060,.052)+.014*ga(x,z,0,4.44,.038,.105)+.010*(ga(x,z,-.049,4.338,.027,.028)+ga(x,z,.049,4.338,.027,.028)))
 y-=edge*(.018*(ga(x,z,-.205,4.335,.12,.105)+ga(x,z,.205,4.335,.12,.105))+.016*ga(x,z,0,4.22,.17,.08)+.005*ga(x,z,0,4.085,.14,.07))
 y+=edge*.008*(ga(x,z,-.155,4.545,.115,.075)+ga(x,z,.155,4.545,.115,.075))
 # Sculpt lips directly into head, with soft corners and a restrained cupid bow.
 width=max(0,1-(x/.18)**2);line=seamz(x);y-=edge*.0075*width*exp(-((z-line-.010)/.014)**2);y-=edge*.009*width*exp(-((z-line+.012)/.016)**2)
 y+=edge*.003*(ga(x,z,-.174,4.227,.013,.014)+ga(x,z,.174,4.227,.013,.014))
 y+=edge*.007*(ga(x,z,-.042,4.327,.011,.006)+ga(x,z,.042,4.327,.011,.006))
 return y
CENTRES=[(-.155,'R',-1),(.155,'L',1)];EY=4.545;CY=-.205;RAD=.112;N=128
# New front surface constrained around two dedicated orbital patches.
outline=[(interp(4+j/140,W),4+j/140) for j in range(141)]+[(-interp(4+j/140,W),4+j/140) for j in range(140,-1,-1)]
def outer_eye(x,sign,a):return (x+.133*cos(a),EY+(.100 if sin(a)>=0 else .097)*sin(a)+sign*.006*cos(a))
holes=[[outer_eye(x,sign,2*pi*i/N) for i in range(N)] for x,side,sign in CENTRES]
def within_hole(x,z):return any(((x-c)/.137)**2+((z-EY)/.108)**2<1.04 for c,side,sgn in CENTRES)
def triangulate(front):
 verts=list(outline);edges=[];loops=[list(range(len(outline)))]
 if front:
  for hole in holes:start=len(verts);verts+=hole;loops.append(list(range(start,len(verts))))
 for loop in loops:edges += [(loop[i],loop[(i+1)%len(loop)]) for i in range(len(loop))]
 # Face-specific density around nose/lips, not uniform added subdivision.
 for j in range(1,125):
  z=4+j*.008
  if z>=5:continue
  w=interp(z,W)
  for i in range(-47,48):
   x=i*.008
   if abs(x)>w-.004 or (front and within_hole(x,z)):continue
   verts.append((x,z))
 if front:
  for j in range(60):
   z=4.17+j*.004
   for i in range(-49,50):
    x=i*.004
    if ((abs(x)<.20 and 4.17<z<4.255) or (abs(x)<.095 and 4.30<z<4.41)) and not within_hole(x,z):verts.append((x,z))
 v,e,f,ov,oe,of=geometry.delaunay_2d_cdt([Vector(v) for v in verts],edges,[loops[0]],1,1e-7)
 faces=[]
 for poly in f:
  x=sum(v[k].x for k in poly)/len(poly);z=sum(v[k].y for k in poly)/len(poly)
  # Hole constraints prevent crossing; remove only the inside of each orbital loop.
  if front:
   inside=False
   for hole in holes:
    odd=False
    for (ax,az),(bx,bz) in zip(hole,hole[1:]+hole[:1]):
     if (az>z)!=(bz>z) and x<(bx-ax)*(z-az)/(bz-az)+ax:odd=not odd
    inside|=odd
   if inside:continue
  faces.append(tuple(poly) if front else tuple(reversed(poly)))
 # CDT stores float32 coordinates. Preserve explicit contour identity so fractional
 # powers do not create unequal front/back seam depths from rounding noise.
 coords=[]
 for i,p in enumerate(v):
  is_contour=any(j<len(outline) for j in ov[i])
  yy=seam_y(p.y) if is_contour else (fy(p.x,p.y) if front else seam_y(p.y)+interp(p.y,BD)*sqrt(max(0,1-(p.x/interp(p.y,W))**2)))
  coords.append((p.x,yy,p.y))
 return coords,faces
fv,ff=triangulate(True);bv,bf=triangulate(False);verts=fv+bv;faces=ff+[tuple(i+len(fv) for i in p) for p in bf]
for x,side,sign in CENTRES:
 start=len(verts);K=14
 for k in range(K+1):
  t=k/K;blend=t*t*(3-2*t)
  for i in range(N):
   a=2*pi*i/N;dx=(.096 if sign*cos(a)>0 else .089)*cos(a);dz=(.046 if sin(a)>=0 else .026)*sin(a)+sign*.006*cos(a);xi=x+dx;zi=EY+dz;xo,zo=outer_eye(x,sign,a);xx=xo*(1-t)+xi*t;zz=zo*(1-t)+zi*t
   inner=CY-sqrt(max(.00001,RAD**2-dx*dx-dz*dz))-.0025;yy=fy(xx,zz)+(inner-fy(xi,zi))*blend-.003*sin(pi*t)*(1 if sin(a)>0 else .40)
   d2=(xx-x)**2+(zz-EY)**2
   if d2<RAD**2:yy=min(yy,CY-sqrt(RAD**2-d2)-.0025)
   verts.append((xx,yy,zz))
 for k in range(K):
  for i in range(N):a=start+k*N+i;b=start+k*N+(i+1)%N;faces.append((a,b,b+N,a+N))
 # Thin waterline transitions into a closed orbital cup behind the eyeball.
 wall=len(verts)
 for i in range(N):a=2*pi*i/N;dx=(.096 if sign*cos(a)>0 else .089)*cos(a);dz=(.046 if sin(a)>=0 else .026)*sin(a)+sign*.006*cos(a);verts.append((x+dx,-.065,EY+dz))
 for i in range(N):a=start+K*N+i;b=start+K*N+(i+1)%N;faces.append((a,b,wall+(i+1)%N,wall+i))
 faces.append(tuple(wall+i for i in reversed(range(N))))
head=mesh('B1_HEAD_new_orbital_topology_and_face_forms',verts,faces,headmat)
bm=bmesh.new();bm.from_mesh(head.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=2e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(head.data);bm.free();head.data.update()
# Vertex tint follows actual sculpted lip/cheek forms. No painted render edits.
attr=head.data.color_attributes.new(name='BUM_SkinTint',type='FLOAT_COLOR',domain='POINT');base=np.array(srgb('#D9A078')[:3]);lip=np.array(srgb('#B97465')[:3]);nost=np.array(srgb('#8D5C45')[:3])
for v,c in zip(head.data.vertices,attr.data):
 x,y,z=v.co;front=max(0,min(1,(-y-.04)/.12));blush=.035*(ga(x,z,-.205,4.335,.12,.10)+ga(x,z,.205,4.335,.12,.10));wid=max(0,1-(x/.18)**2);dz=z-seamz(x);lm=.48*wid*exp(-(abs(dz)/.021)**6) if abs(x)<.18 else 0;nm=.42*(ga(x,z,-.042,4.327,.011,.006)+ga(x,z,.042,4.327,.011,.006));color=base*(1-front*(lm+blush))+lip*front*(lm+blush);color=color*(1-front*nm)+nost*front*nm;c.color=(*color,1)
curve('B1_closed_relaxed_smile',[(x,fy(x,seamz(x))-.0010,seamz(x)) for x in [-.18+i*.36/64 for i in range(65)]],.0007,seammat)
# Eyeballs and cap surfaces are new, kept outside the sphere under rigid gaze rotations.
for x,side,sign in CENTRES:
 sphere('B1_Eyeball_'+side,(x,CY,EY),RAD,white)
 rot=Matrix.Rotation(-sign*.0194,3,'Z')@Matrix.Rotation(-.0044,3,'X')
 for prefix,radius,offset,ma in [('Iris',.051,.0013,iris),('Pupil',.021,.0027,pupil)]:
  coords=[(0,-RAD-offset-.003,0)];uvs=[(.5,.5)];fs=[]
  for k in range(1,13):
   rr=radius*k/12
   for i in range(96):
    a=2*pi*i/96;dx=rr*cos(a);dz=rr*sin(a);dome=.003*max(0,1-(rr/.051)**2)**2;coords.append((dx,-sqrt(RAD**2-rr*rr)-offset-dome,dz));uvs.append((.5+dx/(2*radius),.5+dz/(2*radius)))
  for i in range(96):fs.append((0,1+i,1+(i+1)%96))
  for k in range(11):
   for i in range(96):a=1+k*96+i;b=1+k*96+(i+1)%96;fs.append((a,a+96,b+96,b))
  o=mesh('B1_'+prefix+'_'+side,[Vector((x,CY,EY))+rot@Vector(p) for p in coords],fs,ma);uvl=o.data.uv_layers.new(name='IrisRadialUV')
  for poly in o.data.polygons:
   for li,vi in zip(poly.loop_indices,poly.vertices):uvl.data[li].uv=uvs[vi]
 # Thin anatomical upper margin, not a thick black eyeliner ring.
 pts=[]
 for i in range(49):
  a=pi*i/48;dx=(.096 if sign*cos(a)>0 else .089)*cos(a);dz=.046*sin(a)+sign*.006*cos(a);pts.append((x+dx,CY-sqrt(RAD**2-dx*dx-dz*dz)-.0033,EY+dz))
 curve('B1_upper_waterline_'+side,pts,.0009,seammat)
 # Tapered brows and brow form already supported by the cranial surface.
 vs=[];fs=[]
 for i in range(49):
  t=i/48;xx=x+.105*(2*t-1);zz=4.65+.010*sin(pi*t)-sign*.003*(2*t-1);width=.008*sin(pi*t)**.65
  for dz in [-width,width]:vs.append((xx,fy(xx,zz+dz)-.003,zz+dz))
 for i in range(48):fs.append((2*i,2*i+1,2*i+3,2*i+2))
 mesh('B1_brow_'+side,vs,fs,browmat)
 # Ear sculpt: front concha/helix relief on one shell, no separate wire curves.
 vs=[];fs=[];NC=96;KR=24
 for face in [0,1]:
  for k in range(KR+1):
   rr=max(.0001,k/KR)
   for i in range(NC):
    a=2*pi*i/NC;dx=.074*rr*cos(a);dz=.145*rr*sin(a);px=sign*.375+sign*dx;pz=4.405+dz
    py=.010+(.044*sqrt(max(0,1-rr*rr)) if face else -.043*sqrt(max(0,1-rr*rr))-.011*exp(-((rr-.80)/.12)**2)+.017*exp(-((dx+.006)/.036)**2-(dz/.077)**2)-.006*exp(-((dx+.020)/.014)**2-((dz+.012)/.045)**2))
    if k==KR:py=.010
    vs.append((px,py,pz))
  off=face*(KR+1)*NC
  for k in range(KR):
   for i in range(NC):a=off+k*NC+i;b=off+k*NC+(i+1)%NC;fs.append((a,b,b+NC,a+NC) if face else (a,a+NC,b+NC,b))
 fs.extend([tuple(reversed(range(NC))),tuple((KR+1)*NC+i for i in range(NC))])
 o=mesh('B1_ear_sculpt_'+side,vs,fs,skin);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=2e-5);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# New hair volume: scalp height fields with curved growth directions, plus four irregular fringe tips.
def cat(points,t):
 ps=[Vector(points[0])]+[Vector(p) for p in points]+[Vector(points[-1])];u=t*(len(points)-1);i=min(len(points)-2,int(u));q=u-i;p0,p1,p2,p3=ps[i:i+4];return .5*(2*p1+(-p0+p2)*q+(2*p0-5*p1+4*p2-p3)*q*q+(-p0+3*p1-3*p2+p3)*q*q*q)
def scalp(p):
 q=Vector((p[0]/.382,(p[1]-.015)/.405,(p[2]-4.58)/.555));q.normalize();return Vector((q.x*.382,q.y*.405+.015,q.z*.555+4.58))
paths=[[(.18,-.26,5.00),(.05,-.37,4.94),(-.15,-.36,4.83),(-.29,-.23,4.75)],[(.18,-.14,5.09),(-.01,-.24,5.11),(-.24,-.25,4.98),(-.36,-.06,4.82)],[(.12,.015,5.12),(-.06,-.05,5.14),(-.29,-.08,5.03),(-.36,.17,4.84)],[(.16,.13,5.09),(-.04,.17,5.13),(-.25,.23,4.98),(-.30,.28,4.66)],[(.20,.20,4.99),(.12,.34,4.94),(-.02,.39,4.76),(-.16,.32,4.46)],[(.28,.15,4.96),(.32,.27,4.85),(.23,.35,4.63),(.07,.35,4.43)],[(.23,-.24,4.97),(.34,-.17,4.86),(.37,-.03,4.70),(.32,.12,4.57)],[(.23,-.07,5.08),(.35,.01,4.97),(.37,.18,4.77),(.27,.28,4.62)], [(-.18,.23,4.98),(-.28,.29,4.83),(-.20,.37,4.64),(-.03,.35,4.44)]]
samples=[np.array([scalp(cat(path,i/36)) for i in range(37)]) for path in paths]
vs=[];fs=[];NT=192;KP=72
for k in range(KP+1):
 for i in range(NT):
  a=2*pi*i/NT;front=max(0,cos(a));side=abs(sin(a));back=max(0,-cos(a));boundary=4.42+.31*front+.13*side-.024*sin(3*a+.6)*front+.018*sin(2*a+.3)*back;pmax=math.acos(max(-1,min(1,(boundary-4.58)/.555)));p=.0005+(pmax-.0005)*k/KP
  pos=Vector((.382*sin(p)*sin(a),-.405*sin(p)*cos(a)+.015,4.58+.555*cos(p)));nn=Vector((pos.x/.382**2,(pos.y-.015)/.405**2,(pos.z-4.58)/.555**2)).normalized();q=np.array(pos);height=0
  for j,ss in enumerate(samples):d2=np.sum((ss-q)**2,axis=1);idx=int(np.argmin(d2));t=idx/36;height+=.010*(.25+.75*sin(pi*t)**.6)*exp(-float(d2[idx])/(.045+(j%3)*.008)**2)
  height=min(.027,height);pos+=nn*height;vs.append(pos)
for k in range(KP):
 for i in range(NT):a=k*NT+i;b=k*NT+(i+1)%NT;fs.append((a,a+NT,b+NT,b))
fs += [tuple(reversed(range(NT))),tuple(KP*NT+i for i in range(NT))]
cap=mesh('B1_hair_new_growth_volume',vs,fs,hairmat,H)
fringes=[([( .18,-.29,4.98),(.07,-.39,4.88),(-.10,-.38,4.78),(-.26,-.29,4.705)],.105),([(.20,-.21,5.04),(.04,-.34,4.99),(-.19,-.34,4.88),(-.34,-.18,4.745)],.090),([(.19,-.08,5.11),(-.02,-.23,5.08),(-.23,-.27,4.98),(-.35,-.07,4.83)],.105),([(.24,-.22,4.98),(.33,-.18,4.87),(.36,-.06,4.73),(.32,.05,4.60)],.078)]
for n,(path,width) in enumerate(fringes):
 v=[];f=[];L=48;NC=16
 for k in range(L+1):
  t=k/L;raw=cat(path,t);on=scalp(raw);blend=max(0,min(1,(t-.84)/.16));c=on.lerp(raw,blend);normal=Vector((c.x/.382**2,(c.y-.015)/.405**2,(c.z-4.58)/.555**2)).normalized();c+=normal*.012*(1-blend);tangent=(cat(path,min(1,t+.002))-cat(path,max(0,t-.002))).normalized();axis=tangent.cross(normal).normalized();normal=axis.cross(tangent).normalized();taper=max(.02,sin(pi*t)**.55)
  for i in range(NC):a=2*pi*i/NC;v.append(c+axis*(width*.5*taper*cos(a))+normal*(.013*taper*sin(a)))
 for k in range(L):
  for i in range(NC):a=k*NC+i;b=k*NC+(i+1)%NC;f.append((a,b,b+NC,a+NC))
 f.extend([tuple(reversed(range(NC))),tuple(L*NC+i for i in range(NC))]);mesh('B1_fringe_sculpt_'+str(n),v,f,hairmat,H)
# Voxel sculpt union is intentionally allowed for head/hair research; old ridges are gone.
bpy.ops.object.select_all(action='DESELECT')
for o in H.objects:o.select_set(True)
bpy.context.view_layer.objects.active=cap;bpy.ops.object.join();cap=bpy.context.object;cap.name='B1_HAIR_REDESIGNED_sculpt_volume';cap.data.remesh_voxel_size=.0035;bpy.ops.object.voxel_remesh();mod=cap.modifiers.new('Soften sculpt union junctions','SMOOTH');mod.factor=.35;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
for p in cap.data.polygons:p.use_smooth=True
# Camera/back inspection uses the same actual orthographic system as R close-ups.
cam=bpy.data.cameras.new('B1_back_180');cam.type='ORTHO';cam.ortho_scale=1.5;o=bpy.data.objects.new('B1_back_180',cam);bpy.data.collections['CAMERAS'].objects.link(o);o.location=(0,12,4.53);o.rotation_euler=(Vector((0,-.01,4.53))-o.location).to_track_quat('-Z','Y').to_euler()
s.camera=bpy.data.objects['Face_front-000'];s['phase']='P5.3B.1 HEAD ONLY ART RESEARCH / OWNER_PENDING';s['baseline']='cebfbe1';s['scope']='New head/ear/orbit/hair topology; cropped existing neck/shoulder context; no full-body work/rig/animation/GLB';s['H_unit']='Skull-chin1H atZ4..5, same5H design coordinate system; no full-body B1 measurement claimed.';s.cycles.samples=48;s.cycles.use_denoising=False;s.render.resolution_x=1200;s.render.resolution_y=1600;s.render.resolution_percentage=100;s.render.filepath='//renders/head-front-000.png'
# Purge unused full-body/old head data in NEW file only, not the preserved baseline.
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=False,do_recursive=True);bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'bum07-p53b1-head-study.blend'),compress=True)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
(R/'evidence/build-provenance.json').write_text(json.dumps({'baseline':'cebfbe1','source_sha256':source_hash,'preserved_reference_sha256':hashlib.sha256((R/'reference/bum07-p53ar-preserved.blend').read_bytes()).hexdigest(),'source_unchanged':True,'study_scope':'head neck shoulder bust','removed_from_NEW_study_only':removed,'new_head_topology':True,'new_hair_design':True,'no_full_body_refinement':True,'no_rig_animation_GLB':True,'art_approval':'OWNER_PENDING','method':'One bounded procedural sculpt construction; results must be judged visually, not by export success.'},indent=2));print('B1_HEAD_STUDY_SAVED',flush=True)
