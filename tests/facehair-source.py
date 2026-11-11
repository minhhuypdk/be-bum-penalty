import bpy,bmesh,ast,sys,hashlib,json,struct
args=sys.argv[sys.argv.index('--')+1:];base,candidate,out=args
module=ast.parse(open('scripts/assets/prepare-bum07-facehair.py').read())
defs=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name in ['is_face','fp','rig_data']]
exec(compile(ast.Module(body=defs,type_ignores=[]),'audit_helpers','exec'),globals())
bpy.ops.wm.open_mainfile(filepath=base,use_scripts=False,load_ui=False);rig=bpy.data.objects['BUM07 original rig study']
body={o.name:fp(o)for o in bpy.data.objects if o.type=='MESH' and not is_face(o.name)};h=fp(bpy.data.objects['BUM independent facial surface']);r=rig_data()
bpy.ops.wm.open_mainfile(filepath=candidate,use_scripts=False,load_ui=False);rig=bpy.data.objects['BUM07 original rig study']
for n,v in body.items():assert fp(bpy.data.objects[n])==v,n+' outside-scope data changed'
assert r==rig_data(),'Rig/action curves changed'
assert h==fp(bpy.data.objects['C_REFERENCE__BUM independent facial surface'])
assert h!=fp(bpy.data.objects['P2 facial surface'])
assert len([im for im in bpy.data.images if im.name.startswith('C_REFERENCE_')])==6
assert len([o for o in bpy.data.objects if o.name.startswith('P2_GUIDE__P2 swept hair clump')])==10
bm=bmesh.new();bm.from_mesh(bpy.data.objects['P2 layered hair sculpt blockout'].data);edges=sum(e.is_boundary for e in bm.edges);bm.free();assert edges==0
report={'result':'PASS','independentReadBack':True,'outsideScopeMeshesUnchanged':len(body),'rigAndActionCurvesUnchanged':True,'CHeadReferenceUnchanged':True,'actualHeadGeometryChanged':True,'bodyLocked':all(bpy.data.objects[n].hide_select for n in body),'hairOpenBoundaryEdges':edges,'hairGuides':10,'packedReferenceImages':6,'artApproval':False,'professionalHandSculpt':False}
open(out,'w').write(json.dumps(report,indent=2)+'\n');print('INDEPENDENT_READBACK_PASS',report)
