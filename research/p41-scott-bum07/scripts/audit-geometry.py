import bpy,json,bmesh,sys,math
from pathlib import Path
out=Path(sys.argv[sys.argv.index('--')+1]);rows=[]
for o in bpy.data.collections['02_RUNTIME_COMPENSATED'].objects:
 m=o.data;bm=bmesh.new();bm.from_mesh(m);uv=m.uv_layers.active;bad=0
 if uv:
  for p in m.polygons:
   a=[uv.data[i].uv for i in p.loop_indices];area=sum(a[i].x*a[(i+1)%len(a)].y-a[(i+1)%len(a)].x*a[i].y for i in range(len(a)))/2
   if abs(area)<1e-12:bad+=1
 rows.append(dict(object=o.name,vertices=len(m.vertices),faces=len(m.polygons),boundaryEdges=sum(e.is_boundary for e in bm.edges),nonManifoldNonBoundaryEdges=sum(not e.is_manifold and not e.is_boundary for e in bm.edges),zeroAreaFaces=sum(f.calc_area()<1e-12 for f in bm.faces),nonFiniteNormals=sum(not all(math.isfinite(x)for x in p.normal)for p in m.polygons),uvLayers=len(m.uv_layers),zeroUVAreaFaces=bad,worldBounds=[[min((o.matrix_world@v.co)[k]for v in m.vertices),max((o.matrix_world@v.co)[k]for v in m.vertices)]for k in range(3)]));bm.free()
r={'meshes':rows,'scope':'Runtime editable mesh data, pre-skin; separate open clothing boundaries expected. Not a self-intersection or manifold certification. UV degeneracy includes sidewalls/soles/projected labels.','facialMorphNames':list(bpy.data.objects['P41_BodyFaceEyes_Runtime'].data.shape_keys.key_blocks.keys())}
(out/'geometry-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps([x for x in rows if any(n in x['object']for n in ['Shirt07','Jersey','BUMBadge'])],indent=2))
