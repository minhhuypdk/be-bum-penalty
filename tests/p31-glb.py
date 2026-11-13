"""Offline GLB structure/accessor audit, not a substitute for Khronos validator."""
import sys,struct,json,math,hashlib
from pathlib import Path
p=Path(sys.argv[1]);b=p.read_bytes();magic,ver,total=struct.unpack_from('<III',b);assert magic==0x46546c67 and ver==2 and total==len(b)
n,typ=struct.unpack_from('<II',b,12);assert typ==0x4e4f534a;d=json.loads(b[20:20+n]);binstart=28+n
assert all('uri'not in v for v in d.get('buffers',[])+d.get('images',[]));assert not d.get('extensionsRequired')
fmt={5120:('b',1),5121:('B',1),5122:('h',2),5123:('H',2),5125:('I',4),5126:('f',4)};dims={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16};cache={}
def read_view(view_index,offset,count,ctype,k):
 view=d['bufferViews'][view_index];f,size=fmt[ctype];stride=view.get('byteStride',k*size);start=binstart+view.get('byteOffset',0)+offset
 assert offset+(count-1)*stride+k*size<=view['byteLength']
 return [struct.unpack_from('<'+f*k,b,start+j*stride)for j in range(count)]
def values(i):
 if i in cache:return cache[i]
 a=d['accessors'][i];k=dims[a['type']]
 v=read_view(a['bufferView'],a.get('byteOffset',0),a['count'],a['componentType'],k)if 'bufferView'in a else [(0,)*k for _ in range(a['count'])]
 if 'sparse'in a:
  sp=a['sparse'];si=sp['indices'];sv=sp['values'];indices=read_view(si['bufferView'],si.get('byteOffset',0),sp['count'],si['componentType'],1);patch=read_view(sv['bufferView'],sv.get('byteOffset',0),sp['count'],a['componentType'],k)
  assert all(0<=ind[0]<a['count']for ind in indices);assert all(indices[j][0]<indices[j+1][0]for j in range(len(indices)-1))
  for ind,row in zip(indices,patch):v[ind[0]]=row
 assert all(math.isfinite(x)for row in v for x in row);cache[i]=v;return v
for i in range(len(d['accessors'])):values(i)
triangles=0;prims=0;newNormals=[];weightMax=0
for m in d['meshes']:
 for prim in m['primitives']:
  prims+=1;a=prim['attributes'];pos=values(a['POSITION']);idx=values(prim['indices']);assert max(x[0]for x in idx)<len(pos);triangles+=len(idx)//3
  assert 'NORMAL'in a and 'JOINTS_0'in a and 'WEIGHTS_0'in a
  if m['name'].startswith('P31 '):assert 'TEXCOORD_0'in a
  weightMax=max(weightMax,max(abs(sum(w)-1)for w in values(a['WEIGHTS_0'])))
  if m['name'].startswith('P31 '):
   normalError=max(abs(sum(x*x for x in row)-1)for row in values(a['NORMAL']));assert normalError<.001;newNormals.append({'mesh':m['name'],'normalLengthSquaredMaxError':normalError})
  for target in prim.get('targets',[]):
   for ai in target.values():assert len(values(ai))==len(pos)
assert weightMax<.001
names=[a.get('name')for a in d.get('animations',[])];assert all(n in names for n in ['Idle','Run','Kick','Celebrate'])
r={'result':'PASS','auditType':'Custom offline structure + all-accessor finite + normal/UV/skin/morph checks; not Khronos certification','file':p.name,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'triangles':triangles,'primitives':prims,'materials':len(d['materials']),'skins':len(d['skins']),'clips':names,'accessorsFinite':len(cache),'maxWeightSumError':weightMax,'newNormals':newNormals,'embeddedImages':len(d.get('images',[])),'legacyMeshesWithoutUV':[m['name']for m in d['meshes']if any('TEXCOORD_0'not in p['attributes']for p in m['primitives'])],'uvOverlapCertified':False,'intersectionsCertified':False,'physicalIPhone':False}
p.with_name('glb-audit.json').write_text(json.dumps(r,indent=2));print('GLB_AUDIT_PASS',triangles,'triangles;',prims,'primitives; all accessor values finite')
