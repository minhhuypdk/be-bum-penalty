"""Independent read-back + evaluated geometry tests; never saves a .blend."""
import bpy,bmesh,sys,json,hashlib,math,ast,struct
from pathlib import Path
base,candidate,out=sys.argv[sys.argv.index('--')+1:];src=Path(base);before=hashlib.sha256(src.read_bytes()).hexdigest()
module=ast.parse(Path('scripts/assets/build-bum07-p31.py').read_text());defs=[n for n in module.body if isinstance(n,ast.FunctionDef)and n.name in ['fingerprint','rig_state']];exec(compile(ast.Module(body=defs,type_ignores=[]),'audit_helpers','exec'),globals())
def snapshot():
 return {o.name:fingerprint(o)for o in bpy.data.objects if o.type=='MESH'}
bpy.ops.wm.open_mainfile(filepath=base,use_scripts=False,load_ui=False);rig=bpy.data.objects['BUM07 original rig study'];original=snapshot();r=rig_state()
bpy.ops.wm.open_mainfile(filepath=candidate,use_scripts=False,load_ui=False);rig=bpy.data.objects['BUM07 original rig study'];actual=snapshot()
for n,h in original.items():assert actual[n]==h,n
assert r==rig_state();parts=list(bpy.data.collections['04_P31_PROCEDURAL_FACE_HAIR'].objects);neutral={o.name:[v.co.copy()for v in o.data.vertices]for o in parts}
mesh=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);mesh.append({'name':o.name,'boundary':sum(e.is_boundary for e in bm.edges),'nonManifold':sum(not e.is_manifold for e in bm.edges),'inconsistentNormals':sum(e.is_manifold and not e.is_contiguous for e in bm.edges),'degenerateFaces':sum(f.calc_area()<1e-12 for f in bm.faces),'volume':bm.calc_volume(signed=True),'quads':sum(len(f.verts)==4 for f in bm.faces),'faces':len(bm.faces)});bm.free()
 assert all(mesh[-1][k]==0 for k in ['boundary','nonManifold','inconsistentNormals','degenerateFaces']);assert mesh[-1]['volume']>0
morph=[]
for o in parts:
 if not o.data.shape_keys:continue
 for key in o.data.shape_keys.key_blocks[1:]:
  for t in [0,.5,1]:
   key.value=t;bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());d=ev.to_mesh();d.calc_loop_triangles()
   areas=[(d.vertices[b].co-d.vertices[a].co).cross(d.vertices[c].co-d.vertices[a].co).length/2 for a,b,c in [tri.vertices for tri in d.loop_triangles]]
   finite=all(math.isfinite(x)for v in d.vertices for x in v.co);assert finite
   morph.append({'object':o.name,'key':key.name,'value':t,'finite':finite,'zeroAreaTriangles':sum(a<1e-12 for a in areas),'minTriangleArea':min(areas)})
   ev.to_mesh_clear()
  key.value=0
motion=[]
for action in ['Idle','Run','Kick','Celebrate']:
 a=bpy.data.actions.get(action);assert a,action;rig.animation_data.action=a
 for f in [a.frame_range[0],sum(a.frame_range)/2,a.frame_range[1]]:
  bpy.context.scene.frame_set(int(f));dep=bpy.context.evaluated_depsgraph_get();maxDisp=0
  for o in parts:
   ev=o.evaluated_get(dep);m=ev.to_mesh();assert all(math.isfinite(x)for v in m.vertices for x in v.co)
   maxDisp=max(maxDisp,max((v.co-neutral[o.name][i]).length for i,v in enumerate(m.vertices)));ev.to_mesh_clear()
  motion.append({'action':action,'frame':f,'finite':True,'maxLocalDisplacement':maxDisp})
assert max(x['maxLocalDisplacement']for x in motion)>.01
assert before==hashlib.sha256(src.read_bytes()).hexdigest()
report={'result':'PASS_WITH_LIMITATIONS','independentReadBack':True,'originalMeshesPreserved':len(original),'originalRigActionsPreserved':True,'sourceSha256':before,'newMeshes':mesh,'morphDeformation':morph,'motion':motion,'limits':['Manifold per component only; intentional intersections between lids/head/hair roots not a welded production surface','Finite deformation is not proof of collision-free poses or good facial anatomy','UV availability/finite values checked by build; overlaps/seam distortion not production certified','Morph zero-area triangles are reported explicitly, not hidden'],'artApproved':False,'physicalIPhone':False}
Path(out).write_text(json.dumps(report,indent=2));print('READBACK_PASS',len(original),'unchanged original meshes; morph degeneracy count',sum(x['zeroAreaTriangles']for x in morph))
