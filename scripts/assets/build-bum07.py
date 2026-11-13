"""Original BUM 07 art study, NOT final/9-of-10 art. No Snow geometry used.
blender -b --factory-startup --disable-autoexec -P scripts/assets/build-bum07.py -- /output
The authored surface fields, garment patterns and FK studies are reproducible.
Artist sculpt/retopology, face rig, contact cleanup and approval remain mandatory.
"""
import bpy,math,sys,os,json
from mathutils import Vector
from math import sin,cos,pi,exp,sqrt
OUT=sys.argv[sys.argv.index('--')+1];os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.render.fps=30
objects=[];binding={};mats={}
def mat(name,color,rough=.5):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;mats[name]=m;return m
skin=mat('warm child skin',(.68,.36,.21),.5);hair=mat('soft dark chestnut',(.025,.012,.008),.67)
white=mat('warm sclera',(.88,.85,.77),.2);iris=mat('hazel iris',(.11,.044,.012),.2);pupil=mat('pupil',(.004,.003,.002),.15)
lip=mat('soft lip',(.44,.15,.105),.6);mouth=mat('smile crease',(.13,.035,.02),.7);navy=mat('midnight blue fabric',(.013,.032,.078),.7)
yellow=mat('sunflower knit',(.92,.49,.024),.68);gold=mat('warm gold piping',(.7,.3,.01),.53);sock=mat('ivory socks',(.78,.77,.69),.8)
sole=mat('rubber outsole',(.015,.025,.038),.85);boot=mat('blue football upper',(.025,.07,.13),.44);lace=mat('ivory laces',(.8,.81,.74),.8)
# Actual embedded tangent normal tile, not an unexported Cycles noise shader.
im=bpy.data.images.new('original woven normal tile',width=128,height=128);pixels=[]
for y in range(128):
 for x in range(128):
  a=.028*sin(x*pi/2)*(.6+.4*cos(y*pi/2));b=.028*sin(y*pi/2);pixels.extend([.5+a,.5+b,sqrt(max(0,1-4*a*a-4*b*b))*.5+.5,1])
im.pixels.foreach_set(pixels);im.colorspace_settings.name='Non-Color';im.pack()
for material in [yellow,navy,sock]:
 n=material.node_tree.nodes;t=n.new('ShaderNodeTexImage');t.image=im;uv=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=16;material.node_tree.links.new(uv.outputs['UV'],mapping.inputs[0]);material.node_tree.links.new(mapping.outputs[0],t.inputs['Vector']);normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.24;material.node_tree.links.new(t.outputs['Color'],normal.inputs['Color']);material.node_tree.links.new(normal.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])
def mesh(name,verts,faces,material,bone=None,sub=0):
 data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update();o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);data.materials.append(material)
 for p in data.polygons:p.use_smooth=True
 uv=data.uv_layers.new(name='UVMap')
 # Repeatable surface projection for fine woven tile (no external textures).
 for p in data.polygons:
  for li in p.loop_indices:
   v=data.vertices[data.loops[li].vertex_index].co;uv.data[li].uv=(v.x,v.z)
 if sub:m=o.modifiers.new('surface finish','SUBSURF');m.levels=sub
 objects.append(o);binding[o.name]=bone;return o

def ellipsoid(name,center,radii,material,bone,sculpt=None,nu=48,nv=32):
 verts=[];faces=[]
 for j in range(nv+1):
  v=pi*j/nv
  for i in range(nu):
   u=2*pi*i/nu;x=radii[0]*sin(v)*cos(u);y=-radii[1]*sin(v)*sin(u);z=radii[2]*cos(v)
   if sculpt:x,y,z=sculpt(x,y,z,u,v)
   verts.append((x+center[0],y+center[1],z+center[2]))
 for j in range(nv):
  for i in range(nu):a=j*nu+i;b=j*nu+(i+1)%nu;faces.append((a,b,b+nu,a+nu))
 return mesh(name,verts,faces,material,bone)

def tube(name,centers,radii,material,bone,segments=24,cap=True):
 verts=[];faces=[]
 for j,(c,r) in enumerate(zip(centers,radii)):
  c=Vector(c);t=Vector(centers[min(j+1,len(centers)-1)])-Vector(centers[max(0,j-1)])
  t.normalize();a=t.cross(Vector((0,1,0))).normalized();b=t.cross(a).normalized()
  for i in range(segments):
   u=2*pi*i/segments;rr=1+.012*sin(u*6+j*.8);verts.append(c+a*(cos(u)*r[0]*rr)+b*(sin(u)*r[1]*rr))
 for j in range(len(centers)-1):
  for i in range(segments):a=j*segments+i;b=j*segments+(i+1)%segments;faces.append((a,b,b+segments,a+segments))
 if cap:faces.extend([tuple(reversed(range(segments))),tuple((len(centers)-1)*segments+i for i in range(segments))])
 return mesh(name,verts,faces,material,bone,1)

def ribbon(name,points,widths,material,bone):
 # Flat sculpted strips/seams rather than cylindrical hair or eyebrows.
 verts=[];faces=[]
 for i,p in enumerate(points):
  for s in [-1,1]:verts.append((p[0],p[1],p[2]+s*widths[i]))
 for i in range(len(points)-1):faces.append((2*i,2*i+1,2*i+3,2*i+2))
 return mesh(name,verts,faces,material,bone,1)

def face_y(x,z):
 # Continuous facial volume: cheeks, bridge, tip, philtrum and rounded chin.
 q=max(.001,1-.40*(x/.315)**2-(z/.345)**2);y=-.282*sqrt(q)
 y-=.070*exp(-(x/.052)**2-((z+.018)/.065)**2)
 y-=.014*exp(-(x/.045)**2-((z-.055)/.11)**2)
 y-=.027*(exp(-((x-.19)/.085)**2-((z+.075)/.07)**2)+exp(-((x+.19)/.085)**2-((z+.075)/.07)**2))
 y-=.012*exp(-(x/.12)**2-((z+.25)/.07)**2)
 y-=.018*(exp(-((x-.215)/.055)**2-((z-.065)/.085)**2)+exp(-((x+.215)/.055)**2-((z-.065)/.085)**2))
 y+=.010*(exp(-((x-.137)/.105)**2-((z-.065)/.08)**2)+exp(-((x+.137)/.105)**2-((z-.065)/.08)**2))
 return y

def head_sculpt(x,y,z,u,v):
 if y<0:
  w=min(1,max(0,sin(u))/.75);w=w*w*(3-2*w);y=y*(1-w)+face_y(x,z)*w
 # Lower face deliberately rounded, rather than scaling an adult jaw.
 x*=1+.055*exp(-((z+.15)/.12)**2)
 return x,y,z
head=ellipsoid('BUM independent facial surface',(0,0,1.86),(.315,.282,.345),skin,'Head',head_sculpt,96,64)
colors=head.data.color_attributes.new(name='Complexion',type='FLOAT_COLOR',domain='POINT')
for vertex,item in zip(head.data.vertices,colors.data):
 x,y,z=vertex.co;blush=(exp(-((abs(x)-.18)/.075)**2-((z-1.785)/.07)**2) if y<-.15 else 0);item.color=(.68+.045*blush,.36-.055*blush,.21-.025*blush,1)
n=skin.node_tree.nodes;col=n.new('ShaderNodeVertexColor');col.layer_name='Complexion'
# Only head uses complexion; other skin parts use their original constant material.
headskin=skin.copy();headskin.name='child face complexion';head.data.materials[0]=headskin;col=headskin.node_tree.nodes.get(col.name);headskin.node_tree.links.new(col.outputs['Color'],headskin.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
for side in [-1,1]:
 x=side*.137
 ellipsoid('eye white '+str(side),(x,-.266,1.928),(.087,.024,.070),white,'Head')
 ellipsoid('iris '+str(side),(x-side*.004,-.290,1.93),(.035,.005,.038),iris,'Head',nu=48,nv=24)
 ellipsoid('pupil '+str(side),(x-side*.004,-.295,1.93),(.018,.002,.022),pupil,'Head',nu=32,nv=20)
 ellipsoid('eye glint '+str(side),(x-.011,-.298,1.946),(.008,.002,.009),white,'Head',nu=20,nv=12)
 for upper in [True,False]:
  points=[]
  for i in range(25):
   a=pi*i/24;xx=x+.089*cos(a);zz=1.928+(.071 if upper else -.068)*sin(a);yy=-.266-.003*sin(a);points.append((xx,yy,zz))
  ribbon('soft eyelid '+str(side)+str(upper),points,[.008]*25,skin,'Head')
 points=[]
 for i in range(20):
  t=i/19;xx=x-.095+.19*t;zz=2.038+.025*sin(t*pi)-side*.012*(t-.5);points.append((xx,face_y(xx,zz-1.86)-.008,zz))
 ribbon('tapered brow '+str(side),points,[.003+.009*sin(pi*i/19)**.6 for i in range(20)],hair,'Head')
 ellipsoid('sculpt ear '+str(side),(side*.323,.006,1.85),(.060,.043,.086),skin,'Head',lambda x,y,z,u,v:(x,y+.012*exp(-(z/.04)**2-(x/.03)**2) if y<0 else y,z),32,24)
 # Small nostril marks sit on the integrated nose surface.
 xx=side*.022;zz=1.82;ellipsoid('nostril '+str(side),(xx,face_y(xx,zz-1.86)-.002,zz),(.009,.003,.004),mouth,'Head',nu=20,nv=12)
points=[]
for i in range(33):
 x=-.105+.21*i/32;z=1.724+.023*(x/.105)**2;points.append((x,face_y(x,z-1.86)-.004,z))
ribbon('gentle smile',points,[.002+.004*sin(pi*i/32) for i in range(33)],mouth,'Head')
ribbon('lower lip soft edge',[(x,y-.001,z-.008)for x,y,z in points],[.001+.004*sin(pi*i/32) for i in range(33)],lip,'Head')
# One flowing sculpted hair shell. Broad ridges merge into the cap, no tubes.
verts=[];faces=[];nu=112;nv=40
for j in range(nv+1):
 t=j/nv
 for i in range(nu):
  u=2*pi*i/nu;extent=1.55-.50*sin(u)+.065*cos(3*u+.7);p=t*extent
  groove=(.008*cos(16*u+3.3*p)+.002*cos(43*u+6*p))*(sin(p)**.8)*sin(pi*t)**.35
  rx=.331+groove;ry=.296+groove
  x=rx*sin(p)*cos(u)+.025*(1-t)**2;y=-ry*sin(p)*sin(u);z=1.87+(.366+groove)*cos(p)+.020*exp(-((u-2.1)/.7)**2)*sin(p)
  verts.append((x,y,z))
for j in range(nv):
 for i in range(nu):a=j*nu+i;b=j*nu+(i+1)%nu;faces.append((a,b,b+nu,a+nu))
mesh('original combed sculpt hair cap',verts,faces,hair,'Head',1)
# Skin surfaces connect through a voxel-unified sculpt base, including fingers.
parts=[]
parts.append(tube('torso under kit',[(0,0,1.03),(0,0,1.25),(0,0,1.47),(0,0,1.55)],[(.16,.105),(.17,.105),(.215,.12),(.18,.10)],skin,None))
parts.append(tube('neck',[(0,0,1.49),(0,0,1.64)],[(.085,.078),(.09,.079)],skin,None))
for side,tag in [(-1,'R'),(1,'L')]:
 parts.append(tube('arm '+tag,[(side*.19,0,1.49),(side*.29,0,1.40),(side*.38,0,1.27),(side*.455,0,1.13)],[(.085,.077),(.072,.065),(.057,.052),(.042,.038)],skin,None))
 parts.append(ellipsoid('palm '+tag,(side*.473,-.003,1.075),(.052,.034,.072),skin,None,nu=24,nv=16))
 for i,length in enumerate([.087,.104,.098,.077]):
  xx=side*(.432+i*.026);parts.append(tube('finger '+tag+str(i),[(xx,0,1.048),(xx+side*.005,-.005,1.017),(xx+side*.006,-.012,1.048-length)],[(.015,.014),(.013,.013),(.009,.010)],skin,None,12))
 parts.append(tube('thumb '+tag,[(side*.44,-.012,1.105),(side*.412,-.035,1.067),(side*.406,-.04,1.034)],[(.021,.019),(.017,.016),(.012,.012)],skin,None,16))
 parts.append(tube('leg '+tag,[(side*.10,0,1.08),(side*.115,0,.87),(side*.12,-.012,.64),(side*.12,0,.31),(side*.12,0,.19)],[(.108,.10),(.091,.086),(.070,.064),(.057,.05),(.044,.043)],skin,None))
bpy.ops.object.select_all(action='DESELECT')
for o in parts:
 bpy.context.view_layer.objects.active=o;o.select_set(True)
 # Bake designed surface finish before voxel union.
 for mod in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
remaining=[o for o in objects if o not in parts]
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();body=parts[0];body.name='BUM continuous body and five-finger hands'
remesh=body.modifiers.new('unified sculpt volume','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.008;remesh.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=remesh.name)
smooth=body.modifiers.new('sculpt relax','SMOOTH');smooth.factor=.55;smooth.iterations=3;bpy.ops.object.modifier_apply(modifier=smooth.name)
objects=remaining+[body];binding[body.name]=None
# Jersey: patterned ring surface with small asymmetric drape folds.
centers=[(0,0,z) for z in [1.025,1.045,1.10,1.20,1.32,1.43,1.50,1.525]];radii=[(.178,.12),(.183,.122),(.179,.12),(.178,.118),(.19,.125),(.219,.13),(.227,.125),(.20,.108)]
jersey=tube('yellow jersey tailored shell',centers,radii,yellow,None,64,False)
for v in jersey.data.vertices:
 x,y,z=v.co;v.co.y+=.006*sin(x*42+z*11)*(1-abs(z-1.23)/.3)+.003*sin(z*80+x*10)
# Neck opening and rib collar, anatomical front V.
verts=[];faces=[]
for j in range(5):
 t=j/4
 for i in range(64):
  a=2*pi*i/64;r=.20*(1-t)+.087*t;front=max(0,-sin(a));z=1.525+.050*t-.035*front*t
  verts.append((r*cos(a),r*.55*sin(a),z))
for j in range(4):
 for i in range(64):a=j*64+i;b=j*64+(i+1)%64;faces.append((a,b,b+64,a+64))
mesh('knitted V collar shoulder yoke',verts,faces,yellow,'Chest',1)
for side,tag in [(-1,'R'),(1,'L')]:
 tube('jersey sleeve '+tag,[(side*.18,0,1.48),(side*.25,0,1.435),(side*.30,0,1.37)],[(.102,.092),(.10,.09),(.088,.08)],yellow,'UpperArm.'+tag,40,False)
 tube('navy sleeve rib '+tag,[(side*.294,0,1.379),(side*.309,0,1.355)],[(.09,.081),(.088,.080)],navy,'UpperArm.'+tag,32,False)
 tube('shorts '+tag,[(side*.09,0,1.075),(side*.10,0,.99),(side*.11,0,.85)],[(.116,.128),(.124,.13),(.111,.107)],navy,None,40,False)
 tube('sock '+tag,[(side*.12,0,.18),(side*.12,0,.28),(side*.12,-.003,.43)],[(.052,.053),(.06,.056),(.067,.062)],sock,'Shin.'+tag,32,False)
 tube('sock gold band '+tag,[(side*.12,-.003,.405),(side*.12,-.003,.428)],[(.068,.063),(.067,.062)],gold,'Shin.'+tag,32,False)
 def shoe_sculpt(x,y,z,u,v):return x,y-.045*(1-z/.1),z
 ellipsoid('football boot upper '+tag,(side*.12,-.07,.13),(.083,.166,.092),boot,'Foot.'+tag,shoe_sculpt,48,24)
 ellipsoid('football sole '+tag,(side*.12,-.09,.061),(.087,.19,.022),sole,'Foot.'+tag,nu=48,nv=16)
 for dx in [-.055,.055]:
  for yy in [-.20,-.08,.025]:tube('rounded stud '+tag,[(side*.12+dx,yy,.045),(side*.12+dx,yy,.027)],[(.014,.014),(.011,.011)],gold,'Foot.'+tag,12)
 for k in range(4):
  yy=-.13+k*.024;ribbon('flat lace '+tag,[(side*.12-.038,yy,.201-k*.003),(side*.12+.038,yy,.201-k*.003)],[.004,.004],lace,'Foot.'+tag)
# Own vector 07, no imported font, sponsor or third-party crest.
def number07(back=False):
 yy=.133 if back else -.137;zc=1.26;scale=1.3 if back else 1
 vv=[];ff=[]
 for i in range(48):
  a=2*pi*i/48
  for r in [1,.60]:vv.append(((-.043+.028*cos(a)*r)*scale,yy,zc+.048*sin(a)*r*scale))
 for i in range(48):a=2*i;b=2*((i+1)%48);ff.append((a,b,b+1,a+1))
 mesh('back 0' if back else 'front 0',vv,ff,navy,'Spine')
 p=[(.008,zc+.045),(.070,zc+.045),(.028,zc-.045)]
 # Letter strokes are flat garment applique, not external text geometry.
 for i in range(2):
  (x,z),(xx,zz)=p[i:i+2];o=mesh(('back' if back else 'front')+' 7',[(x*scale,yy,z),(xx*scale,yy,zz),(xx*scale+.010,yy,zz+.004),(x*scale+.010,yy,z+.004)],[(0,1,2,3)],navy,'Spine')
 if back:
  for o in objects[-3:]:
   for v in o.data.vertices:v.co.x*=-1
number07();number07(True)
# Original sun/ball badge and shoulder piping.
v=[(-.105,-.138,1.434)]
for i in range(10):a=2*pi*i/10;r=.023 if i%2==0 else .011;v.append((-.105+r*sin(a),-.14,1.434+r*cos(a)))
mesh('own sun badge',v,[(0,i+1,(i+1)%10+1)for i in range(10)],navy,'Chest')
# A real FK skeleton, including three joints for each of five fingers per hand.
bones={}
def bone(n,h,t,parent=None):bones[n]=(Vector(h),Vector(t),parent)
bone('Root',(0,0,0),(0,0,.18));bone('Hips',(0,0,1.02),(0,0,1.17),'Root');bone('Spine',(0,0,1.17),(0,0,1.37),'Hips');bone('Chest',(0,0,1.37),(0,0,1.52),'Spine');bone('Neck',(0,0,1.52),(0,0,1.64),'Chest');bone('Head',(0,0,1.64),(0,0,2.16),'Neck');bone('Jaw',(0,-.03,1.78),(0,-.15,1.72),'Head')
for side,tag in [(-1,'R'),(1,'L')]:
 bone('UpperArm.'+tag,(side*.19,0,1.49),(side*.38,0,1.27),'Chest');bone('Forearm.'+tag,(side*.38,0,1.27),(side*.455,0,1.13),'UpperArm.'+tag);bone('Hand.'+tag,(side*.455,0,1.13),(side*.475,0,1.045),'Forearm.'+tag)
 for i,length in enumerate([.087,.104,.098,.077]):
  xx=side*(.432+i*.026)
  for j in range(3):bone('Finger%d_%d.%s'%(i,j,tag),(xx,0,1.048-j*length/3),(xx,0,1.048-(j+1)*length/3),'Hand.'+tag if j==0 else 'Finger%d_%d.%s'%(i,j-1,tag))
 for j in range(3):bone('Thumb%d.%s'%(j,tag),(side*(.44-.034*j/3),-.012-.028*j/3,1.105-.071*j/3),(side*(.44-.034*(j+1)/3),-.012-.028*(j+1)/3,1.105-.071*(j+1)/3),'Hand.'+tag if j==0 else 'Thumb%d.%s'%(j-1,tag))
 bone('Thigh.'+tag,(side*.10,0,1.04),(side*.12,-.012,.64),'Hips');bone('Shin.'+tag,(side*.12,-.012,.64),(side*.12,0,.19),'Thigh.'+tag);bone('Foot.'+tag,(side*.12,0,.19),(side*.12,-.20,.08),'Shin.'+tag);bone('Toe.'+tag,(side*.12,-.20,.08),(side*.12,-.26,.07),'Foot.'+tag)
arm=bpy.data.armatures.new('BUM07 FK study skeleton');rig=bpy.data.objects.new('BUM07 original rig study',arm);scene.collection.objects.link(rig)
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
for n,(h,t,parent) in bones.items():b=arm.edit_bones.new(n);b.head=h;b.tail=t
for n,(h,t,parent) in bones.items():
 if parent:arm.edit_bones[n].parent=arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
def distance(p,a,b):
 ab=b-a;t=max(0,min(1,(p-a).dot(ab)/ab.length_squared));return (p-a-t*ab).length
for o in objects:
 if o.name not in bpy.data.objects:continue
 # Apply surface finish once, retaining vertex weights through subsequent LOD.
 bpy.context.view_layer.objects.active=o
 for m in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=m.name)
 fixed=binding.get(o.name)
 if fixed:
  o.vertex_groups.new(name=fixed).add(list(range(len(o.data.vertices))),1,'REPLACE')
 else:
  candidates=[n for n in bones if n not in ['Root','Head','Jaw']]
  groups={n:o.vertex_groups.new(name=n)for n in candidates}
  for v in o.data.vertices:
   closest=sorted([(distance(v.co,bones[n][0],bones[n][1]),n)for n in candidates])[:3];weights=[1/(d+.008)**4 for d,n in closest];total=sum(weights)
   for (d,n),w in zip(closest,weights):groups[n].add([v.index],w/total,'REPLACE')
 m=o.modifiers.new('actual skin deformation','ARMATURE');m.object=rig;o.parent=rig
# Four deliberately labelled FK motion STUDIES. No claim of production sports acting.
def pose(n,angles,frame):
 p=rig.pose.bones[n];p.rotation_mode='XYZ';p.rotation_euler=angles;p.keyframe_insert('rotation_euler',frame=frame,group=n)
for action,duration in [('Idle',120),('Run',30),('Kick',96),('Celebrate',108)]:
 for p in rig.pose.bones:p.rotation_mode='XYZ';p.rotation_euler=(0,0,0);p.location=(0,0,0)
 rig.animation_data_clear()
 for frame in sorted(set(list(range(1,duration+1,3))+[duration])):
  t=(frame-1)/(duration-1);w=sin(t*2*pi)
  values={n:(0,0,0)for n in bones}
  if action=='Idle':values['Chest']=(.013*sin(t*2*pi),0,0);values['Head']=(0,.035*w,0)
  elif action=='Run':
   for s,tag in [(-1,'R'),(1,'L')]:values['Thigh.'+tag]=(s*.65*w,0,0);values['Shin.'+tag]=(.8*max(0,-s*w),0,0);values['UpperArm.'+tag]=(-s*.5*w,0,0);values['Forearm.'+tag]=(-.5,0,0)
   values['Chest']=(.08,0,.025*w)
  elif action=='Kick':
   wind=sin(min(1,t/.36)*pi/2);strike=max(0,sin(min(1,max(0,(t-.32)/.33))*pi/2));recover=1-max(0,min(1,(t-.70)/.30));values['Thigh.R']=((.48*wind-1.6*strike)*recover,0,0);values['Shin.R']=(.65*wind*(1-strike)*recover,0,0);values['UpperArm.L']=(.35*strike*recover,0,-.3*wind*recover);values['UpperArm.R']=(-.3*strike*recover,0,.25*wind*recover);values['Chest']=((.06*wind-.12*strike)*recover,0,0)
  else:
   lift=sin(pi*min(1,t/.24)/2)*(1-max(0,min(1,(t-.78)/.22)));values['UpperArm.L']=(0,0,-1.85*lift);values['UpperArm.R']=(0,0,1.85*lift);values['Forearm.L']=(-.4,0,0);values['Forearm.R']=(-.4,0,0);values['Head']=(0,.12*w,0)
  for n,v in values.items():pose(n,v,frame)
 rig.animation_data.action.name=action
 rig.animation_data.action.use_fake_user=True
# Save editable original source, before creating two export artifacts.
rig.animation_data.action=bpy.data.actions['Idle'];scene.frame_start=1;scene.frame_end=120;scene.frame_set(1)
rig['art_status']='Technical art study, NOT approved final BUM; no 9/10 claim';rig['snow_geometry_used']=False
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'bum07-source.blend'),compress=True)
reports=[]
for lod,ratio in [('portrait',1),('mobile',.55)]:
 clones=[]
 for original in objects:
  if original.name not in bpy.data.objects:continue
  clone=original.copy();clone.data=original.data.copy();scene.collection.objects.link(clone);clones.append(clone)
  if ratio<1 and len(clone.data.polygons)>1500:
   # Keep facial surface more detailed than body/hair at mobile LOD.
   m=clone.modifiers.new('review LOD geometry','DECIMATE');m.ratio=.8 if 'facial surface' in original.name else ratio
   bpy.context.view_layer.objects.active=clone;bpy.ops.object.modifier_apply(modifier=m.name)
 bpy.ops.object.select_all(action='DESELECT')
 for o in clones:o.select_set(True)
 bpy.context.view_layer.objects.active=clones[0];bpy.ops.object.join();export_mesh=clones[0];export_mesh.name='BUM07 skinned mesh '+lod
 rig.select_set(True);bpy.context.view_layer.objects.active=rig
 path=os.path.join(OUT,'bum07-study-'+lod+'.glb')
 bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,use_active_scene=True,export_apply=False,export_animations=True,export_animation_mode='ACTIONS',export_anim_single_armature=True,export_force_sampling=True,export_frame_range=False,export_def_bones=True,export_image_format='AUTO',export_extras=True)
 reports.append({'lod':lod,'bytes':os.path.getsize(path),'geometryRatio':ratio,'status':'original scripted Blender art study; not final child-film character','motions':['Idle','Run','Kick','Celebrate'],'limits':['FK animation studies, no contact/IK/corrective polish','Facial morph/eyelid rig incomplete','Surface fields and sculpted shell are computational, not a professional hand-sculpt']})
 bpy.data.objects.remove(export_mesh,do_unlink=True)
open(os.path.join(OUT,'build-report.json'),'w').write(json.dumps(reports,indent=2)+'\n');print('BUM_BUILD_COMPLETE',reports)
