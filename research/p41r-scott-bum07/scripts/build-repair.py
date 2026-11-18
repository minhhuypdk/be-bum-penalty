"""Scott→BUM07 P4.1R, isolated final-repair prototype. Source: Mish7913, CC BY4.0.
Retains370native joints. Full-influence bind compensation and native facial
pose baking are validated separately; not a claim of global deformation equality.
"""
import bpy,bmesh,sys,math,json,hashlib,struct
import numpy as np
from pathlib import Path
from math import sin,cos,pi,exp,sqrt
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent));from dq_math import bone_parts,blended_matrix
OUT=Path(sys.argv[sys.argv.index('--')+1]).resolve();OUT.mkdir(parents=True,exist_ok=True);src=Path(bpy.data.filepath);sourceHash=hashlib.sha256(src.read_bytes()).hexdigest()
expected=json.loads(Path('research/p4-character-assets/audits/scott-audit.json').read_text())['sourceSha256'];assert sourceHash==expected and src.parent!=OUT
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
scene=bpy.context.scene;scene.frame_set(1);native=bpy.data.objects['Boy'];scene.tool_settings.use_keyframe_insert_auto=False
ref=bpy.data.collections.new('00_SCOTT_ORIGINAL_REFERENCE');scene.collection.children.link(ref);ref.hide_render=True;ref.hide_viewport=True
col=bpy.data.collections.new('01_SCOTT_BUM07_P41');scene.collection.children.link(col)
sourceMeshes=[o for o in bpy.data.objects if o.type=='MESH'and any(m.type=='ARMATURE'for m in o.modifiers)]
for o in [native]+sourceMeshes:
 for c in list(o.users_collection):c.objects.unlink(o)
 ref.objects.link(o)
rig=native.copy();rig.data=native.data.copy();rig.name='P41_ScottRig_370';col.objects.link(rig);rig.hide_set(False)
def remap_animation(ad):
 if not ad:return
 for f in ad.drivers:
  for v in f.driver.variables:
   for t in v.targets:
    if t.id==native:t.id=rig
remap_animation(rig.animation_data)
for pb in rig.pose.bones:
 for c in pb.constraints:
  for key in ['target','pole_target']:
   if hasattr(c,key)and getattr(c,key)==native:setattr(c,key,rig)
  if c.type=='ARMATURE':
   for t in c.targets:
    if t.target==native:t.target=rig
new=[];copies={}
for o in sourceMeshes:
 if o.name=='Circle':continue # Source bandana: remove it, not recolor it.
 c=o.copy();c.data=o.data.copy();c.name='P41_'+o.name;c.parent=rig;col.objects.link(c);c.hide_set(False)
 for m in c.modifiers:
  if m.type=='ARMATURE':m.object=rig
 remap_animation(c.animation_data);new.append(c);copies[o.name]=c
body=copies['Plane'];shirt=copies['Plane.002'];shorts=copies['Plane.001'];hair=copies['Plane.003'];boots=copies['Plane.004']
body.name='P41_BodyFaceEyes';shirt.name='P41_Jersey';shorts.name='P41_Shorts';hair.name='P41_SculptedHair';boots.name='P41_FootballBoots'
# Each new material belongs to the prototype. Source material/atlas unmodified.
oldmat=bpy.data.materials['Material'];skin=oldmat.copy();skin.name='P41_ScottSkinAtlas';skin.use_nodes=True
if skin.node_tree.nodes.get('Principled BSDF'):skin.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.53
body.data.materials.clear();body.data.materials.append(skin)
for o in [copies['Cube'],copies['Circle.001']]:o.data.materials.clear();o.data.materials.append(skin)
def mat(name,color,rough=.55):
 m=bpy.data.materials.new('P41_'+name);m.use_nodes=True;m.diffuse_color=(*color,1);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;return m
white=mat('Sclera',(.88,.87,.81),.24);irisMat=mat('Iris',(.13,.055,.019),.27);pupilMat=mat('Pupil',(.003,.002,.001),.17)
yellow=mat('YellowFootballFabric',(.95,.57,.025),.73);navy=mat('NavyFootballFabric',(.012,.030,.075),.76);ivory=mat('Socks',(.83,.84,.79),.85);sole=mat('BootRubber',(.015,.021,.03),.8);upper=mat('BootUpper',(.022,.07,.14),.48);hairMat=mat('ChestnutHair',(.055,.022,.012),.52);trim=mat('KitPiping',(.13,.21,.32),.7)
# Embedded fabric normal tile shared by kit, rather than nonportable noise nodes.
im=bpy.data.images.new('P41_woven_normal',width=128,height=128);pixels=[]
for y in range(128):
 for x in range(128):
  a=.025*sin(x*pi/2);b=.025*sin(y*pi/2);pixels.extend((.5+a,.5+b,sqrt(max(0,1-4*a*a-4*b*b))*.5+.5,1))
im.pixels.foreach_set(pixels);im.colorspace_settings.name='Non-Color';im.pack()
for m in [yellow,navy,ivory]:
 ns=m.node_tree.nodes;t=ns.new('ShaderNodeTexImage');t.image=im;n=ns.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.16;m.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);m.node_tree.links.new(n.outputs['Normal'],ns.get('Principled BSDF').inputs['Normal'])
for o,m in [(shirt,yellow),(shorts,navy),(hair,hairMat),(boots,upper)]:o.data.materials.clear();o.data.materials.append(m)
# Reveal source anatomical legs formerly hidden beneath long pants.
for m in list(body.modifiers):
 if m.type=='MASK':body.modifiers.remove(m)
# Identify source eye spheres by connected-component topology, before subdivision.
adj=[set()for _ in body.data.vertices]
for e in body.data.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
seen=set();eyes=[]
for i in range(len(adj)):
 if i in seen:continue
 stack=[i];seen.add(i);ids=[]
 while stack:
  j=stack.pop();ids.append(j)
  for k in adj[j]:
   if k not in seen:seen.add(k);stack.append(k)
 if 300<len(ids)<800 and min(body.data.vertices[j].co.z for j in ids)>3.3:eyes.append(set(ids))
assert len(eyes)==2
body.data.materials.append(white)
for p in body.data.polygons:
 if any(all(v in ids for v in p.vertices)for ids in eyes):p.material_index=1
# Actual face/hair form edits plus subdivided donor topology, not recolor only.
allEye=set.union(*eyes)
for v in body.data.vertices:
 if v.index not in allEye and v.co.y<-.25 and 3.2<v.co.z<4.2:
  x,y,z=v.co;v.co.y+=.027*exp(-(x/.11)**2-((z-3.60)/.15)**2);v.co.x*=1+.012*exp(-((z-3.50)/.20)**2)
for v in hair.data.vertices:
 x,y,z=v.co;t=max(0,min(1,(z-4.1)/.72));v.co.z-=.12*t*t;v.co.x-=.07*t;v.co.y+=.018*sin(x*8)*t
# Cut full-length trousers into shorts, preserving interpolated native weights.
bm=bmesh.new();bm.from_mesh(shorts.data);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,1.68),plane_no=(0,0,1),clear_inner=True,clear_outer=False);bm.to_mesh(shorts.data);bm.free();shorts.data.update()
for v in shorts.data.vertices:
 if v.co.z<2.25:
  s=1 if v.co.x>0 else -1;cx=s*(.19+.14*max(0,(2.10-v.co.z)/.87));v.co.x=cx+(v.co.x-cx)*.82;v.co.y*=.93
for v in boots.data.vertices:
 if v.co.z>.20:v.co.z=.20+(v.co.z-.20)*.33
boots.data.materials.append(sole)
for p in boots.data.polygons:
 if sum(boots.data.vertices[i].co.z for i in p.vertices)/len(p.vertices)<.065:p.material_index=1
# P4.1R: replace the laced donor garment entirely with a donor-torso-based
# football shirt. No old lacing polygons survive in this edited object.
oldshirt=shirt
shirt=body.copy();shirt.data=body.data.copy();shirt.name='P41_Jersey';col.objects.link(shirt)
shirt.data.materials.clear();shirt.data.materials.append(yellow)
for f in shirt.data.polygons:f.material_index=0
bm=bmesh.new();bm.from_mesh(shirt.data)
for point,normal,inner in [((0,0,2.18),(0,0,1),True),((0,0,3.12),(0,0,1),False),((.53,0,0),(1,0,0),False),((-.53,0,0),(1,0,0),True)]:
 bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=point,plane_no=normal,clear_inner=inner,clear_outer=not inner)
# Distinguish intentional cut openings from inherited anatomical torso holes.
boundary=set(e for e in bm.edges if e.is_boundary);shirtOpeningAudit=[]
while boundary:
 seed=boundary.pop();group={seed};stack=[seed]
 while stack:
  edge=stack.pop()
  for v in edge.verts:
   for other in v.link_edges:
    if other in boundary:boundary.remove(other);group.add(other);stack.append(other)
 points={v for e in group for v in e.verts}
 intentional=any(all(abs(v.co[axis]-plane)<2e-5 for v in points)for axis,plane in [(2,2.18),(2,3.12),(0,.53),(0,-.53)])
 shirtOpeningAudit.append({'edges':len(group),'intentionalCutOpening':intentional})
 if not intentional:bmesh.ops.holes_fill(bm,edges=list(group),sides=0)
bm.normal_update()
for v in bm.verts:
 v.co+=v.normal*.034
 # small broad cloth folds by hem, not a resolution-only edit
 z=v.co.z;v.co+=v.normal*(.006*sin(v.co.x*24+z*5)*exp(-((z-2.27)/.20)**2))
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(shirt.data);bm.free()
new=[shirt if o==oldshirt else o for o in new];bpy.data.objects.remove(oldshirt,do_unlink=True)
# Voxel manifold reconstruction only for non-deforming hair and boot surfaces;
# native nearest-surface weights are transferred, not replaced by a single bone.
from mathutils.kdtree import KDTree
remeshStats=[]
def remesh_preserving_weights(o,voxel):
 old=[(v.co.copy(),[(o.vertex_groups[g.group].name,g.weight)for g in v.groups])for v in o.data.vertices]
 kd=KDTree(len(old))
 for i,(co,w)in enumerate(old):kd.insert(co,i)
 kd.balance();bpy.context.view_layer.objects.active=o
 for ob in scene.objects:ob.select_set(False)
 o.select_set(True)
 # Suppress Armature during voxelization: remesh is in the original bind space.
 arm=[m for m in o.modifiers if m.type=='ARMATURE']
 for m in arm:m.show_viewport=False
 m=o.modifiers.new('P41R seal donor shell','SOLIDIFY');m.thickness=.032 if o==hair else .020;m.offset=0;
 bpy.ops.object.modifier_apply(modifier=m.name)
 m=o.modifiers.new('P41R manifold reconstruction','REMESH');m.mode='VOXEL';m.voxel_size=voxel;m.use_smooth_shade=True
 bpy.ops.object.modifier_apply(modifier=m.name)
 m=o.modifiers.new('P41R soften sculpt transitions','SMOOTH');m.factor=.32;m.iterations=3;bpy.ops.object.modifier_apply(modifier=m.name)
 m=o.modifiers.new('P41R surface budget','DECIMATE');m.ratio=.24 if o==hair else .18;bpy.ops.object.modifier_apply(modifier=m.name)
 for g in list(o.vertex_groups):o.vertex_groups.remove(g)
 groups={};maxDistance=0
 for v in o.data.vertices:
  _,i,dist=kd.find(v.co);maxDistance=max(maxDistance,dist)
  for name,w in old[i][1]:
   if name not in groups:groups[name]=o.vertex_groups.new(name=name)
   groups[name].add([v.index],w,'REPLACE')
 for m in arm:m.show_viewport=True
 remeshStats.append({'object':o.name,'voxel':voxel,'maxNearestBindDistance':maxDistance,'beforeVertices':len(old),'afterVertices':len(o.data.vertices),'transfer':'nearest original native bind vertex, ALL weights retained; sampled deformation tested after transfer'})
remesh_preserving_weights(hair,.016)
remesh_preserving_weights(boots,.009)
# Smooth topology is applied before facial samples so every sample has same IDs.
for o in [body,shirt,shorts]:
 bpy.context.view_layer.objects.active=o;m=o.modifiers.new('P41_surface_refinement','SUBSURF');m.levels=1;m.render_levels=1
 bpy.ops.object.modifier_move_up(modifier=m.name)
 while list(o.modifiers).index(m)>0:bpy.ops.object.modifier_move_up(modifier=m.name)
 bpy.ops.object.modifier_apply(modifier=m.name)
 for p in o.data.polygons:p.use_smooth=True

# Ensure the new football shirt clears the donor body after subdivision.
# Same bind space for body and shirt; only cloth vertices move, never body/rig.
body.data.calc_loop_triangles();clearanceTree=BVHTree.FromPolygons([v.co for v in body.data.vertices],[tuple(t.vertices)for t in body.data.loop_triangles],all_triangles=True);clothClearance=[]
for iteration in range(5):
 changed=0;minimum=100
 for v in shirt.data.vertices:
  co,n,_,dist=clearanceTree.find_nearest(v.co);signed=(v.co-co).dot(n);minimum=min(minimum,signed)
  if signed<.020:v.co+=n*(.021-signed);changed+=1
 shirt.data.update();clothClearance.append({'iteration':iteration,'verticesMoved':changed,'minimumSignedDistanceBefore':minimum})
 if not changed:break

# The waistband is a separate donor garment; the shirt must also clear it.
shorts.data.calc_loop_triangles();pantsTree=BVHTree.FromPolygons([v.co for v in shorts.data.vertices],[tuple(t.vertices)for t in shorts.data.loop_triangles],all_triangles=True)
for iteration in range(5):
 changed=0;minimum=100
 for v in shirt.data.vertices:
  if v.co.z>2.43:continue
  co,n,_,dist=pantsTree.find_nearest(v.co);signed=(v.co-co).dot(n);minimum=min(minimum,signed)
  if dist<.18 and signed<.018:v.co+=n*(.019-signed);changed+=1
 shirt.data.update();clothClearance.append({'target':'shorts waistband','iteration':iteration,'verticesMoved':changed,'minimumSignedDistanceBefore':minimum})
 if not changed:break

def mesh(name,vs,fs,material,bone=None):
 d=bpy.data.meshes.new(name);d.from_pydata(vs,[],fs);d.update();o=bpy.data.objects.new('P41_'+name,d);col.objects.link(o);d.materials.append(material)
 for f in d.polygons:f.use_smooth=True
 uv=d.uv_layers.new(name='UVMap')
 for f in d.polygons:
  for li in f.loop_indices:v=d.vertices[d.loops[li].vertex_index].co;uv.data[li].uv=(v.x*6,v.z*6)
 if bone:o.vertex_groups.new(name=bone).add(list(range(len(vs))),1,'REPLACE')
 o.parent=rig;m=o.modifiers.new('Scott native armature','ARMATURE');m.object=rig;new.append(o);return o

def tube(name,centers,radii,material,bone,segments=32):
 vs=[];fs=[]
 for j,c in enumerate(centers):
  for i in range(segments):a=2*pi*i/segments;vs.append((c[0]+radii[j][0]*cos(a),c[1]+radii[j][1]*sin(a),c[2]))
 for j in range(len(centers)-1):
  for i in range(segments):a=j*segments+i;b=j*segments+(i+1)%segments;fs.append((a,b,b+segments,a+segments))
 fs.extend([tuple(reversed(range(segments))),tuple((len(centers)-1)*segments+i for i in range(segments))]);return mesh(name,vs,fs,material,bone)
# Knee socks follow native anatomical shin line in the source A stance.
for side,sign in [('L',1),('R',-1)]:
 centers=[];radii=[]
 for j in range(13):
  z=.30+.82*j/12;fac=(z-.24)/(1.235-.24);centers.append((sign*(.472+(.331-.472)*fac),.071+(-.044-.071)*fac,z));radii.append((.108+.028*sin(pi*j/12),.111+.022*sin(pi*j/12)))
 tube('FootballSock_'+side,centers,radii,ivory,'Bone.Leg.007.'+side)
 tube('SockTop_'+side,centers[-2:],[(r[0]+.005,r[1]+.005)for r in radii[-2:]],navy,'Bone.Leg.007.'+side)
# P4.1R: football round collar follows the new shirt's actual neck opening.
# Read the top boundary in bind space and form a continuous cloth band.
bm=bmesh.new();bm.from_mesh(shirt.data);bm.normal_update()
ring=[v for v in bm.verts if any(e.is_boundary for e in v.link_edges)and v.co.z>3.10]
center=Vector((sum(v.co.x for v in ring)/len(ring),sum(v.co.y for v in ring)/len(ring),0))
ring.sort(key=lambda v:math.atan2(v.co.y-center.y,v.co.x-center.x))
vs=[];fs=[]
for row in range(4):
 for v in ring:
  radial=Vector((v.co.x-center.x,v.co.y-center.y,0)).normalized();co=v.co+radial*(.007 if row in [0,1]else .013);co.z-=.032 if row in [1,2]else 0;vs.append(tuple(co))
N=len(ring)
for j in range(4):
 for i in range(N):fs.append((j*N+i,j*N+(i+1)%N,((j+1)%4)*N+(i+1)%N,((j+1)%4)*N+i))
collar=mesh('FootballCollar',vs,fs,navy)
for g in shirt.vertex_groups:collar.vertex_groups.new(name=g.name)
for v in collar.data.vertices:
 nearest=min(shirt.data.vertices,key=lambda p:(p.co-v.co).length_squared)
 for g in nearest.groups:collar.vertex_groups[g.group].add([v.index],g.weight,'REPLACE')
# Shirt object carries the source body's world offset; collar shares it.
collar.matrix_world=shirt.matrix_world.copy();bm.free()
# Correct projection in a single WORLD space and preserve label sidewall depth.
shirt.data.calc_loop_triangles();verts=[shirt.matrix_world@v.co for v in shirt.data.vertices]
tree=BVHTree.FromPolygons(verts,[tuple(t.vertices)for t in shirt.data.loop_triangles],all_triangles=True)
for name,text,size,z,x in [('Shirt07','07',.36,2.56,0),('BUMBadge','BUM',.085,2.94,-.16)]:
 bpy.ops.object.text_add(location=(x,-.5,z),rotation=(pi/2,0,0));o=bpy.context.object;o.name='P41_'+name;o.data.body=text;o.data.align_x='CENTER';o.data.size=size;o.data.extrude=.002;o.data.bevel_depth=.0006;bpy.ops.object.convert(target='MESH');bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.data.materials.append(navy)
 for g in shirt.vertex_groups:o.vertex_groups.new(name=g.name)
 for v in o.data.vertices:
  world=v.co.copy();depth=world.y+.5;hit=tree.ray_cast(Vector((world.x,-2,world.z)),Vector((0,1,0)),4);assert hit[0]is not None,('label misses jersey',name,tuple(world))
  world.y=hit[0].y-.012+depth;v.co=world
  nearest=min(shirt.data.vertices,key=lambda p:((shirt.matrix_world@p.co)-world).length_squared)
  for g in nearest.groups:o.vertex_groups[g.group].add([v.index],g.weight,'REPLACE')
 o.parent=rig;m=o.modifiers.new('Scott kit skin','ARMATURE');m.object=rig;m.use_deform_preserve_volume=True;new.append(o)
# Actual studs/cleats, merged later by material in runtime export if useful.
for side,sign in [('L',1),('R',-1)]:
 for i,(dx,y)in enumerate([(-.07,-.25),(.07,-.25),(-.07,-.08),(.07,-.08),(-.06,.10),(.06,.10)]):
  tube('BootStud_'+side+str(i),[(sign*.472+dx,y,-.015),(sign*.472+dx,y,.025)],[(.022,.022),(.03,.03)],sole,'Bone.Leg.004.'+side,12)

# Project real laces onto the donor boot surface, then batch small details.
boots.data.calc_loop_triangles();bt=BVHTree.FromPolygons([v.co for v in boots.data.vertices],[tuple(t.vertices)for t in boots.data.loop_triangles],all_triangles=True);laces=[];laceMat=mat('LaceWhite',(.84,.86,.82),.8)
for side,sign in [('L',1),('R',-1)]:
 for j in range(4):
  points=[]
  for k in range(7):
   x=sign*.472-.08+.16*k/6;y=-.235+.065*j+.006*sin(pi*k/6);hit=bt.ray_cast(Vector((x,y,1)),Vector((0,0,-1)),2)
   if hit[0]is not None:points.append((x,y,hit[0].z+.012))
  if len(points)<2:continue
  cv=bpy.data.curves.new('lace','CURVE');cv.dimensions='3D';cv.use_fill_caps=True;cv.bevel_depth=.006;cv.bevel_resolution=2;sp=cv.splines.new('POLY');sp.points.add(len(points)-1)
  for q,pt in zip(sp.points,points):q.co=(*pt,1)
  ob=bpy.data.objects.new('P41_Lace_'+side+str(j),cv);col.objects.link(ob);bpy.context.view_layer.objects.active=ob
  for obj in scene.objects:obj.select_set(False)
  ob.select_set(True);bpy.ops.object.convert(target='MESH');ob=bpy.context.object;ob.data.materials.append(laceMat);ob.vertex_groups.new(name='Bone.Leg.004.'+side).add(list(range(len(ob.data.vertices))),1,'REPLACE');ob.parent=rig;mm=ob.modifiers.new('Scott shoe binding','ARMATURE');mm.object=rig;laces.append(ob)
def join_objects(objects,active):
 for obj in scene.objects:obj.select_set(False)
 for obj in objects:obj.select_set(True)
 bpy.context.view_layer.objects.active=active;bpy.ops.object.join();return active
studs=[o for o in new if 'BootStud_'in o.name];new=[o for o in new if o not in studs];join_objects([boots]+studs,boots)
if laces:lace=join_objects(laces,laces[0]);lace.name='P41_ProjectedBootLaces';new.append(lace)
for prefix in ['Iris','Pupil']:
 parts=[o for o in new if o.name.startswith('P41_'+prefix+'_')]
 if len(parts)>1:
  new=[o for o in new if o not in parts];merged=join_objects(parts,parts[0]);merged.name='P41_'+prefix+'_BothEyes';new.append(merged)

# Neutral native-pose sampling, including full influences. Runtime keys bake
# these evaluated shapes before skin; native reference rig remains editable.
neutralBasis={b.name:b.matrix_basis.copy()for b in rig.pose.bones};dqCache={}
def pose(mode='Neutral',value=0):
 for b in rig.pose.bones:b.matrix_basis=neutralBasis[b.name]
 if mode=='Blink':
  for s in ['L','R']:rig.pose.bones['Bone.Eyes.Close-Open.'+s].location.z=.176827*value
 if mode=='Smile':
  for s,sign in [('L',1),('R',-1)]:
   b=rig.pose.bones['Bone.Face.016.'+s+'.002'];b.location.z+=.065*value;b.location.x+=sign*.018*value
  rig.pose.bones['Bone.Face.014'].location.z=.015*value
 if mode=='HeadTurn':rig.pose.bones['Bone.Head'].matrix_basis=neutralBasis['Bone.Head']@Matrix.Rotation(.25*value,4,'Z')
 if mode=='ArmRaise':rig.pose.bones['Bone.Hand.L'].location.z+=.25*value;rig.pose.bones['Bone.Hand.L'].location.y-=.15*value
 if mode=='FootForward':rig.pose.bones['Bone.Leg.004.L.001'].location.y-=.35*value
 rig.update_tag(refresh={'OBJECT'});bpy.context.view_layer.update();dqCache.clear()
def evaluated(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();vs=[v.co.copy()for v in m.vertices];e.to_mesh_clear();assert len(vs)==len(o.data.vertices),(o.name,len(vs),len(o.data.vertices));return vs
def skin_matrix(o,v):
 rows=[(o.vertex_groups[g.group].name,g.weight)for g in v.groups if g.weight>0 and o.vertex_groups[g.group].name in rig.pose.bones];rows.sort(key=lambda p:p[1],reverse=True);total=sum(w for n,w in rows);assert total>1e-10,(o.name,v.index)
 preserve=any(m.type=='ARMATURE'and m.use_deform_preserve_volume for m in o.modifiers)
 if preserve:
  if not dqCache:
   dqCache.update({b.name:bone_parts(b.matrix,b.bone.matrix_local)for b in rig.pose.bones})
  M=blended_matrix(dqCache,[(n,w/total)for n,w in rows])
 else:
  M=Matrix(((0,0,0,0),)*4)
  for name,w in rows:
   b=rig.pose.bones[name];D=b.matrix@b.bone.matrix_local.inverted()
   for j in range(4):
    for k in range(4):M[j][k]+=D[j][k]*(w/total)
 return o.matrix_world.inverted()@rig.matrix_world@M@rig.matrix_world.inverted()@o.matrix_world,rows

pose();neutral={o.name:evaluated(o)for o in new}
# P4.1R: iris/pupil are UV artwork ON the actual donor globe; no overlapping
# spheres, curved patches or eye hiding. Lighting still acts on real globe mesh.
E=1024;im=bpy.data.images.new('P41R_own_brown_iris_sclera',width=E,height=E);pix=[]
for yy in range(E):
 phi=((yy+.5)/E-.5)*pi
 for xx in range(E):
  theta=((xx+.5)/E-.5)*2*pi;dx=cos(phi)*sin(theta);dz=sin(phi);front=cos(theta)>0;rr=sqrt(dx*dx+dz*dz)
  if front and rr<.445:
   angle=math.atan2(dz,dx);grain=.5+.5*sin(angle*67+rr*75);t=rr/.445
   color=(.25+.11*grain,.105+.065*grain,.035+.020*grain)
   if t>.92:color=(.055,.027,.013)
   if rr<.205:color=(.008,.005,.004)
  else:color=(.90,.88,.82)
  pix.extend((*color,1))
im.pixels.foreach_set(pix);im.pack();white.use_nodes=True;white.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.27
tex=white.node_tree.nodes.new('ShaderNodeTexImage');tex.image=im;white.node_tree.links.new(tex.outputs['Color'],white.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
body.data.calc_loop_triangles();eyeVerts=set(i for p in body.data.polygons if p.material_index==1 for i in p.vertices)
uv=body.data.uv_layers.active
for sign in [1,-1]:
 ids=[i for i in eyeVerts if sign*neutral[body.name][i].x>0];points=[neutral[body.name][i]for i in ids];center=Vector(tuple((min(v[k]for v in points)+max(v[k]for v in points))/2 for k in range(3)))
 # Ellipsoid-correct UV uses actual globe axis extents, not a guessed spherical patch.
 radii=Vector(tuple((max(v[k]for v in points)-min(v[k]for v in points))/2 for k in range(3)))
 for p in body.data.polygons:
  if p.material_index!=1 or not all(i in ids for i in p.vertices):continue
  coords=[]
  for li in p.loop_indices:
   v=neutral[body.name][body.data.loops[li].vertex_index]-center;v=Vector(tuple(v[k]/radii[k]for k in range(3)));u=.5+math.atan2(v.x,-v.y)/(2*pi);vv=.5+math.asin(max(-1,min(1,v.z)))/pi;coords.append((li,u,vv))
  if max(t[1]for t in coords)-min(t[1]for t in coords)>.5:coords=[(li,u+1 if u<.5 else u,vv)for li,u,vv in coords]
  for li,u,vv in coords:uv.data[li].uv=(u,vv)
# Finish mesh topology: triangulate generated n-gons, remove zero geometry,
# and generate nondegenerate per-triangle UVs for new clothing/hair/boots.
for o in new:
 bm=bmesh.new();bm.from_mesh(o.data)
 if o.name in ['P41_Shirt07','P41_BUMBadge','P41_ProjectedBootLaces']:bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 bmesh.ops.dissolve_degenerate(bm,dist=1e-7,edges=list(bm.edges))
 bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 if o not in [body,copies['Cube'],copies['Circle.001']]:
  uv=o.data.uv_layers.active or o.data.uv_layers.new(name='UVMap')
  for p in o.data.polygons:
   axis=max(range(3),key=lambda k:abs(p.normal[k]));axes=[k for k in range(3)if k!=axis]
   for li in p.loop_indices:
    co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*3,co[axes[1]]*3)
# P4.1R inner-canthus closure corrective acts on the EXISTING eyelid mesh.
# Locate exposed globe rays in native Blink100; expand lid contact depth locally.
# Eyeballs stay visible, full size, same topology and material; no culling trick.
pose('Blink',1);closed=evaluated(body);body.data.calc_loop_triangles()
skinTris=[tuple(t.vertices)for t in body.data.loop_triangles if body.data.polygons[t.polygon_index].material_index==0]
eyeTris=[tuple(t.vertices)for t in body.data.loop_triangles if body.data.polygons[t.polygon_index].material_index==1]
skinTree=BVHTree.FromPolygons(closed,skinTris,all_triangles=True);eyeTree=BVHTree.FromPolygons(closed,eyeTris,all_triangles=True)
leaks={1:[],-1:[]}
for sign in [1,-1]:
 ids=[i for i in eyeVerts if sign*closed[i].x>0];xmin=min(closed[i].x for i in ids);xmax=max(closed[i].x for i in ids);zmin=min(closed[i].z for i in ids);zmax=max(closed[i].z for i in ids)
 for ix in range(260):
  x=xmin+(xmax-xmin)*(ix+.5)/260
  for iz in range(260):
   z=zmin+(zmax-zmin)*(iz+.5)/260;origin=Vector((x,-2,z));e=eyeTree.ray_cast(origin,Vector((0,1,0)),4)
   if e[0]is None:continue
   k=skinTree.ray_cast(origin,Vector((0,1,0)),4)
   if k[0]is None or k[3]>e[3]+1e-6:leaks[sign].append(e[0])
body.shape_key_add(name='Basis');closureAudit=[]
skinIDs=set(v for tri in skinTris for v in tri)
for sign,side in [(1,'L'),(-1,'R')]:
 key=body.shape_key_add(name='P41R_CanthusContact_'+side);points=leaks[sign]
 if not points:continue
 kd=KDTree(len(points))
 for j,co in enumerate(points):kd.insert(co,j)
 kd.balance();count=0
 for v in body.data.vertices:
  if v.index not in skinIDs or sign*closed[v.index].x<0:continue
  _,idx,dist=kd.find(closed[v.index])
  if dist>.055:continue
  # Smooth local forward contact; millimeters in source units, no decorative mesh.
  f=exp(-(dist/.025)**2);delta=Vector((0,-.010*f,0));target=closed[v.index]+delta
  key.data[v.index].co=skin_matrix(body,v)[0].inverted_safe()@target;count+=1
 driver=key.driver_add('value').driver;driver.type='SCRIPTED';var=driver.variables.new();var.name='blink';var.type='SINGLE_PROP';var.targets[0].id=rig;var.targets[0].data_path='pose.bones["Bone.Eyes.Close-Open.'+side+'"].location.z'
 driver.expression='min(1,max(0,(blink/0.176827-0.65)/0.35))**2*(3-2*min(1,max(0,(blink/0.176827-0.65)/0.35)))'
 closureAudit.append({'side':side,'nativeFrontalExposedProbeRays':len(points),'existingLidVerticesCorrected':count,'maxForwardContactDepth':.010,'supportRadius':.055})
pose()
pose();neutral={o.name:evaluated(o)for o in new};faceSamples={}
for mode,levels in [('Blink',[.25,.5,.75,1]),('Smile',[.5,1])]:
 for value in levels:pose(mode,value);faceSamples[(mode,value)]={o.name:evaluated(o)for o in new}
pose()
# Independent audit fixtures are native evaluated WORLD vertices, converted
# to glTF axes, before runtime skin compensation. glTF parser checks them later.
expected={};expectedIndex={}
for label,samples in [('Neutral0',neutral)]+[(mode+str(round(value*100)),samples)for (mode,value),samples in faceSamples.items()]:
 for o in new:
  key=o.name+'_Runtime__'+label;points=[o.matrix_world@v for v in samples[o.name]];expected[key]=np.array([(v.x,v.z,-v.y)for v in points],dtype=np.float32);expectedIndex[key]={'object':o.name+'_Runtime','pose':label,'count':len(points)}
np.savez_compressed(OUT/'native-face-reference.npz',**expected)
(OUT/'native-face-reference-index.json').write_text(json.dumps(expectedIndex,indent=2)+'\n')
# Full-influence matrix per vertex, after native bone constraint evaluation.
compensated={};weightStats=[]
for o in new:
 mats=[skin_matrix(o,v)for v in o.data.vertices];compensated[o.name]=[M.inverted_safe()@v for (M,rows),v in zip(mats,neutral[o.name])];weightStats.append({'object':o.name,'maxSourceInfluences':max(len([g for g in v.groups if g.weight>0])for v in o.data.vertices),'vertices':len(o.data.vertices)})
# Body deformation audit compares same prototype full native skin against
# full DQS/LBS matrices + compensated bind, WITHOUT claiming arbitrary-pose equality.
poseErrors=[]
for mode in ['Neutral','HeadTurn','ArmRaise','FootForward']:
 pose(mode,1)
 for o in new:
  full=evaluated(o);errors=[(skin_matrix(o,v)[0]@compensated[o.name][v.index]-full[v.index]).length for v in o.data.vertices];poseErrors.append({'pose':mode,'object':o.name,'maxError':max(errors),'rmsError':sqrt(sum(e*e for e in errors)/len(errors)),'maxNativeDisplacement':max((p-q).length for p,q in zip(full,neutral[o.name]))})
pose()
# Store native editable meshes and a separate runtime-compensated export set.
text=bpy.data.texts.new('P41_SOURCE_AND_LIMITS');text.write('Scott by Mish7913 /3DMish, CC BY4.0. Source preserved byte-for-byte separately. P4.1 removes bandana, modifies face/hair, football kit07/navy/socks/cleats, adds brown iris and native facial pose bakes. Native370joint rig kept. Runtime full-influence compensation only validated for sampled neutral/expression/body poses; see errors and actual GLB gates. No9/10 or iPhone claims. No game replacement.')
work=OUT/'scott-bum07-p41r-editable.blend'
runtime=[];exportcol=bpy.data.collections.new('02_RUNTIME_COMPENSATED');scene.collection.children.link(exportcol)
for o in new:
 c=o.copy();c.data=o.data.copy();c.name=o.name+'_Runtime';c['P41R_skinning']='DUAL_QUATERNION'if any(m.type=='ARMATURE'and m.use_deform_preserve_volume for m in o.modifiers)else'LINEAR';exportcol.objects.link(c)
 for v,p in zip(c.data.vertices,compensated[o.name]):v.co=p
 c.shape_key_clear();c.shape_key_add(name='Basis')
 for (mode,value),sample in faceSamples.items():
  name=('FH_Blink'if value==1 else'FH_Blink'+str(round(value*100)))if mode=='Blink'else('FH_Smile'if value==1 else'FH_Smile50')
  delta=max((p-q).length for p,q in zip(sample[o.name],neutral[o.name]))
  if delta<1e-7:continue
  k=c.shape_key_add(name=name)
  for v,p in zip(c.data.vertices,sample[o.name]):k.data[v.index].co=skin_matrix(o,v)[0].inverted_safe()@p
 # Keep ALL native weights. Export JOINTS_n/WEIGHTS_n, never truncate.
 rows=[skin_matrix(o,v)[1]for v in o.data.vertices]
 for g in list(c.vertex_groups):c.vertex_groups.remove(g)
 groups={}
 for i,row in enumerate(rows):
  total=sum(w for n,w in row)
  for name,w in row:
   if name not in groups:groups[name]=c.vertex_groups.new(name=name)
   groups[name].add([i],w/total,'REPLACE')
 for m in list(c.modifiers):
  if m.type!='ARMATURE':c.modifiers.remove(m)
 for color in list(c.data.color_attributes):c.data.color_attributes.remove(color)
 attr=c.data.attributes.new(name='_P41_SOURCE_ID',type='FLOAT',domain='POINT')
 for v in c.data.vertices:attr.data[v.index].value=float(v.index)
 runtime.append(c)
# Store both editable native meshes and the exact baked runtime morph set.
for o in new:o.hide_set(True);o.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(work),compress=True)
for o in scene.objects:o.select_set(False)
for o in runtime:o.select_set(True)
rig.select_set(True);bpy.context.view_layer.objects.active=rig
asset=OUT/'scott-bum07-p41r-prototype.glb';bpy.ops.export_scene.gltf(filepath=str(asset),export_format='GLB',use_selection=True,export_apply=False,export_animations=False,export_def_bones=True,export_morph=True,export_attributes=True,export_cameras=False,export_lights=False,export_all_influences=True,export_rest_position_armature=False,export_extras=True)
assert hashlib.sha256(src.read_bytes()).hexdigest()==sourceHash
report={'phase':'P4.1R','sourceAuthor':'Mish7913 /3DMish','sourceLicense':'CC-BY-4.0','sourceSha256':sourceHash,'sourceUnchanged':True,'nativeJoints':len(rig.data.bones),'jointsRemoved':0,'nativeWeightStats':weightStats,'runtimeSkinInfluences':'ALL','nativePreserveVolumeKept':True,'runtimeSkinning':'per-mesh native DQS or LBS; custom research adapter required','bodyPoseToleranceHeightRatio':.002,'faceReferenceSha256':hashlib.sha256((OUT/'native-face-reference.npz').read_bytes()).hexdigest(),'neutralCompensation':'inverse full-weight native bone matrix applied to full native evaluated neutral; facial samples transformed by same inverse','poseErrors':poseErrors,'faceSampleMaxDisplacements':{mode+str(value):max((p-q).length for name,vs in sample.items()for p,q in zip(vs,neutral[name]))for (mode,value),sample in faceSamples.items()},'clothClearance':clothClearance,'closureAudit':closureAudit,'shirtOpeningAudit':shirtOpeningAudit,'remeshStats':remeshStats,'artApproved':False,'physicalIPhone':False,'gameReplaced':False,'exports':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [work,asset]},'limits':['Retains370joints; no claim rig is mobile optimized','All influences retained. Desktop/research Three.js needs provided full-weight adapter; stock loader alone truncates','Native facial rig samples baked to morphs; must check exported GLB visibility and shape roundtrip','No sports animation clips in this prototypeGLB','Original source and C/P2/P3.1/P3.1R not overwritten']}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n');print('P41_BUILD_COMPLETE',len(new),'meshes',len(rig.data.bones),'joints')
