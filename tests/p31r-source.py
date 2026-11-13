"""Independent topology, preservation, exact triangle-sphere contact and ray audit.
Checks bind-space face geometry; screenshot/ID-pass checks the exported GLB too.
"""
import bpy,bmesh,sys,json,math,hashlib,struct,ast
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import closest_point_on_tri
from mathutils.bvhtree import BVHTree
base,candidate,out=sys.argv[sys.argv.index('--')+1:];before=hashlib.sha256(Path(base).read_bytes()).hexdigest()
mod=ast.parse(Path('scripts/assets/build-bum07-p31.py').read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef)and n.name in ['fingerprint','rig_state']],type_ignores=[]),'audit_helpers','exec'),globals())
def snapshot():return {o.name:fingerprint(o)for o in bpy.data.objects if o.type=='MESH'}
def posed(o,b=0,smile=0):
 values={}
 keys=o.data.shape_keys
 if keys:
  if 'FH_Blink25'in keys.key_blocks:
   labels=['Basis','FH_Blink25','FH_Blink50','FH_Blink75','FH_Blink'];p=min(4,b*4);lo=min(3,int(p));t=p-lo
   if lo>0:values[labels[lo]]=1-t
   values[labels[lo+1]]=t
  elif 'FH_Blink'in keys.key_blocks:values['FH_Blink']=b
  values['FH_Smile']=smile
 vs=[v.co.copy()for v in o.data.vertices]
 if keys:
  for name,w in values.items():
   if name not in keys.key_blocks or w==0:continue
   for i,(p,v)in enumerate(zip(keys.key_blocks[name].data,o.data.vertices)):vs[i]+=(p.co-v.co)*w
 return vs

def face_checks(parts,b):
 coords=[];tri=[]
 for o in parts:
  v=posed(o,b);offset=len(coords);coords+=v;o.data.calc_loop_triangles();tri.extend([tuple(offset+i for i in f.vertices)for f in o.data.loop_triangles])
 bv=BVHTree.FromPolygons(coords,tri,all_triangles=True);r=[]
 for s in [-1,1]:
  center=Vector((s*.19*.69,-.156,1.515+.56*.69));R=.090;near=[];minimum=1
  for t in tri:
   if all((coords[i]-center).length>.22 for i in t):continue
   cp=closest_point_on_tri(center,*(coords[i]for i in t));d=(cp-center).length;minimum=min(minimum,d)
   if d<R-1e-5:near.append(t)
  angles=[]
  for angle in [0,45]:
   a=math.radians(angle);view=Vector((-math.sin(a),-math.cos(a),0));right=Vector((math.cos(a),-math.sin(a),0));up=Vector((0,0,1));visible=0;total=0
   for j in range(-12,13):
    for i in range(-12,13):
     u=i*.089/13;v=j*.089/13
     if u*u+v*v>(.089*.94)**2:continue
     p=center+right*u+up*v+view*math.sqrt(.089**2-u*u-v*v);origin=p+view*.4;hit=bv.ray_cast(origin,-view,.8);total+=1
     if hit[0]is None or hit[3]>.3999:visible+=1
   angles.append({'angle':angle,'globeSamples':total,'visibleGlobeSamples':visible,'fullBlinkOcclusionGate':('PASS'if visible==0 else 'FAIL')if b==1 else 'not-full-closure'})
  r.append({'side':s,'blink':b,'sphereEnvelopeRadius':R,'minimumSkinTriangleDistance':minimum,'skinTrianglesInsideOcularEnvelope':len(near),'views':angles})
 return r

bpy.ops.wm.open_mainfile(filepath=base,use_scripts=False,load_ui=False);rig=bpy.data.objects['BUM07 original rig study'];original=snapshot();rigBase=rig_state()
p31parts=[o for o in bpy.data.collections['04_P31_PROCEDURAL_FACE_HAIR'].objects if 'reconstructed head'in o.name or 'thick orbital lid'in o.name]
control=face_checks(p31parts,1)
bpy.ops.wm.open_mainfile(filepath=candidate,use_scripts=False,load_ui=False);rig=bpy.data.objects['BUM07 original rig study']
for n,h in original.items():assert fingerprint(bpy.data.objects[n])==h,n
assert rigBase==rig_state();parts=list(bpy.data.collections['05_P31R_FACIAL_STRUCTURE'].objects);head=next(o for o in parts if 'unified head'in o.name)
meshReport=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);row={'name':o.name,'vertices':len(bm.verts),'faces':len(bm.faces),'boundary':sum(e.is_boundary for e in bm.edges),'nonManifold':sum(not e.is_manifold for e in bm.edges),'inconsistentNormals':sum(e.is_manifold and not e.is_contiguous for e in bm.edges),'degenerateFaces':sum(f.calc_area()<1e-12 for f in bm.faces),'signedVolume':bm.calc_volume(signed=True),'uvFinite':all(math.isfinite(x)for d in o.data.uv_layers.active.data for x in d.uv)};bm.free();meshReport.append(row)
contact=[];deform=[];selfContact=[]
for b in [0,.125,.25,.375,.5,.625,.75,.875,1]:
 contact+=face_checks([head],b)
 vs=posed(head,b);head.data.calc_loop_triangles();tris=[tuple(t.vertices)for t in head.data.loop_triangles];tree=BVHTree.FromPolygons(vs,tris,all_triangles=True);pairs=[(a,c)for a,c in tree.overlap(tree)if a<c and not set(tris[a]).intersection(tris[c])];selfContact.append({'blink':b,'nonAdjacentTriangleOverlapPairs':len(pairs),'classification':'Unclassified non-adjacent overlap candidates; includes some seam contact but also requires cleanup. Not certified self-intersection-free.'});areas=[(vs[t.vertices[1]]-vs[t.vertices[0]]).cross(vs[t.vertices[2]]-vs[t.vertices[0]]).length/2 for t in head.data.loop_triangles];deform.append({'mode':'Blink','value':b,'finite':all(math.isfinite(x)for v in vs for x in v),'zeroAreaTriangles':sum(a<1e-12 for a in areas),'minTriangleArea':min(areas)})
for value in [0,.5,1]:
 for o in parts:
  if not o.data.shape_keys or 'FH_Smile'not in o.data.shape_keys.key_blocks:continue
  vs=posed(o,smile=value);o.data.calc_loop_triangles();areas=[(vs[t.vertices[1]]-vs[t.vertices[0]]).cross(vs[t.vertices[2]]-vs[t.vertices[0]]).length/2 for t in o.data.loop_triangles];deform.append({'mode':'Smile','object':o.name,'value':value,'finite':all(math.isfinite(x)for v in vs for x in v),'zeroAreaTriangles':sum(a<1e-12 for a in areas),'minTriangleArea':min(areas)})
mouthContact=[]
for val in [0,.5,1]:
 hp=posed(head,smile=val);head.data.calc_loop_triangles();ht=BVHTree.FromPolygons(hp,[tuple(t.vertices)for t in head.data.loop_triangles],all_triangles=True)
 for o in parts:
  if not any(n in o.name for n in ['upper lip','lower lip','oral opening']):continue
  pv=posed(o,smile=val);o.data.calc_loop_triangles();tr=BVHTree.FromPolygons(pv,[tuple(t.vertices)for t in o.data.loop_triangles],all_triangles=True);mouthContact.append({'smile':val,'object':o.name,'headTriangleOverlapPairs':len(ht.overlap(tr)),'classification':'Embedded vermilion/oral insert contacts counted, not certified collision-free','boundsMin':[min(v[i]for v in pv)for i in range(3)],'boundsMax':[max(v[i]for v in pv)for i in range(3)]})
closed=[v for r in contact if r['blink']==1 for v in r['views']];gate='PASS'if all(v['visibleGlobeSamples']==0 for v in closed)else 'FAIL'
report={'result':'PASS_WITH_LIMITATIONS'if gate=='PASS'and all(r['skinTrianglesInsideOcularEnvelope']==0 for r in contact)else 'FAIL_OCULAR_CONTACT_OR_OCCLUSION','independentReadBack':True,'originalMeshesUnchanged':len(original),'originalRigActionsUnchanged':True,'sourceSha256':before,'candidateSha256':hashlib.sha256(Path(candidate).read_bytes()).hexdigest(),'mesh':meshReport,'deformation':deform,'contact':contact,'headSelfContact':selfContact,'mouthContact':mouthContact,'negativeControlP31':control,'blink100RayGate':gate,'ocularTriangleContactGate':'PASS'if all(r['skinTrianglesInsideOcularEnvelope']==0 for r in contact if r['blink']in [0,.25,.5,.75,1])else 'FAIL','interpolationContactGate':'PASS'if all(r['skinTrianglesInsideOcularEnvelope']==0 for r in contact)else 'FAIL','limits':['Exact triangle-sphere envelope test, not arbitrary-object collision certification','Intentional full-closure lid contact overlap is not excluded as global self-intersection-free','Ray coverage uses 25x25 disk grid per eye per view in bind space; exported GLB gets independent ID render gate','No physical iPhone measurements or art approval'],'artApproved':False}
Path(out).write_text(json.dumps(report,indent=2)+'\n');assert before==hashlib.sha256(Path(base).read_bytes()).hexdigest()
print('SOURCE_AUDIT',gate,'mesh issues',[(r['name'],r['boundary'],r['nonManifold'],r['degenerateFaces'])for r in meshReport if any(r[k]for k in ['boundary','nonManifold','degenerateFaces'])]);print('CONTACT',[(r['blink'],r['side'],r['skinTrianglesInsideOcularEnvelope'],[(v['angle'],v['visibleGlobeSamples'])for v in r['views']])for r in contact])
