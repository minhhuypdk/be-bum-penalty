"""Independent binary glTF skin/morph evaluator vs native Blender reference arrays.
Run with Blender Python for numpy/mathutils; does not execute a donor script."""
import sys,json,struct,hashlib,math
from pathlib import Path
import numpy as np
from mathutils import Matrix,Quaternion,Vector
folder=Path(sys.argv[sys.argv.index('--')+1]);p=folder/'scott-bum07-p41-prototype.glb';b=p.read_bytes();assert struct.unpack_from('<III',b)==(0x46546c67,2,len(b));n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);binary=memoryview(b)[28+n:];cache={}
fmt={5120:np.int8,5121:np.uint8,5122:np.dtype('<i2'),5123:np.dtype('<u2'),5125:np.dtype('<u4'),5126:np.dtype('<f4')};dims={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
def view(vi,offset,count,ctype,width):
 v=d['bufferViews'][vi];dt=np.dtype(fmt[ctype]);stride=v.get('byteStride',dt.itemsize*width);start=v.get('byteOffset',0)+offset;assert offset+max(0,count-1)*stride+dt.itemsize*width<=v['byteLength'];return np.ndarray((count,width),dtype=dt,buffer=binary,offset=start,strides=(stride,dt.itemsize)).copy()
def accessor(i):
 if i in cache:return cache[i]
 a=d['accessors'][i];k=dims[a['type']];v=view(a['bufferView'],a.get('byteOffset',0),a['count'],a['componentType'],k)if'bufferView'in a else np.zeros((a['count'],k),dtype=fmt[a['componentType']])
 if'sparse'in a:
  sp=a['sparse'];ix=sp['indices'];values=sp['values'];ids=view(ix['bufferView'],ix.get('byteOffset',0),sp['count'],ix['componentType'],1).ravel();v[ids]=view(values['bufferView'],values.get('byteOffset',0),sp['count'],a['componentType'],k)
 if a.get('normalized')and a['componentType']!=5126:v=v.astype(np.float64)/np.iinfo(fmt[a['componentType']]).max
 assert np.isfinite(v).all();cache[i]=v;return v
for i in range(len(d['accessors'])):accessor(i)
assert all('uri'not in x for x in d.get('buffers',[])+d.get('images',[]))
parents={child:i for i,node in enumerate(d['nodes'])for child in node.get('children',[])};globalM={}
def nodeM(i):
 if i in globalM:return globalM[i]
 nd=d['nodes'][i]
 if'matrix'in nd:M=Matrix(np.array(nd['matrix']).reshape(4,4).T.tolist())
 else:
  q=nd.get('rotation',[0,0,0,1]);M=Matrix.Translation(Vector(nd.get('translation',[0,0,0])))@Quaternion((q[3],q[0],q[1],q[2])).to_matrix().to_4x4()@Matrix.Diagonal(Vector([*nd.get('scale',[1,1,1]),1]))
 if i in parents:M=nodeM(parents[i])@M
 globalM[i]=M;return M
reference=np.load(folder/'native-face-reference.npz',allow_pickle=False);checks=[];primitiveReport=[];triangles=0
for ni,node in enumerate(d['nodes']):
 if'mesh'not in node:continue
 name=node['name'];mesh=d['meshes'][node['mesh']];keys=mesh.get('extras',{}).get('targetNames',[]);skin=d['skins'][node['skin']];inv=accessor(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1);joint=np.array([np.array(nodeM(j),dtype=float)for j in skin['joints']]);skinM=joint@inv
 for pi,pr in enumerate(mesh['primitives']):
  a=pr['attributes'];positions=accessor(a['POSITION']).astype(float);ids=np.rint(accessor(a['_P41_SOURCE_ID']).ravel()).astype(int);joints=accessor(a['JOINTS_0']).astype(int);weights=accessor(a['WEIGHTS_0']).astype(float);assert np.max(np.abs(weights.sum(axis=1)-1))<1e-5
  M=np.einsum('vi,vijk->vjk',weights,skinM[joints]);indices=accessor(pr['indices']).ravel();assert max(indices)<len(positions);triangles+=len(indices)//3
  for pose in ['Neutral0','Blink25','Blink50','Blink75','Blink100','Smile50','Smile100']:
   points=positions.copy();key=('FH_Blink'if pose=='Blink100'else'FH_'+pose)if pose.startswith('Blink')else('FH_Smile'if pose=='Smile100'else'FH_Smile50')
   if pose!='Neutral0'and key in keys:
    target=pr['targets'][keys.index(key)]
    if'POSITION'in target:points+=accessor(target['POSITION'])
   xyz=np.einsum('vij,vj->vi',M,np.c_[points,np.ones(len(points))])[:,:3];expected=reference[name+'__'+pose][ids];errors=np.linalg.norm(xyz-expected,axis=1)
   checks.append({'node':name,'primitive':pi,'pose':pose,'vertices':len(points),'maxWorldError':float(errors.max()),'rmsWorldError':float(np.sqrt(np.mean(errors**2)))})
  primitiveReport.append({'node':name,'primitive':pi,'material':d['materials'][pr['material']]['name'],'vertices':len(positions),'morphNames':keys,'hasUV':'TEXCOORD_0'in a})
maxError=max(x['maxWorldError']for x in checks);report={'result':'PASS'if maxError<1e-4 else'FAIL','method':'Decode actual GLB node globals+inverse bind+4 weights+sparse morph; match explicit source vertex IDs against full-influence native Blender evaluated world vertices','maxWorldError':maxError,'tolerance':1e-4,'checks':checks,'primitives':primitiveReport,'assetTriangles':triangles,'primitiveCount':len(primitiveReport),'joints':[len(s['joints'])for s in d['skins']],'GLBBytes':len(b),'GLBSha256':hashlib.sha256(b).hexdigest(),'referenceSha256':hashlib.sha256((folder/'native-face-reference.npz').read_bytes()).hexdigest(),'limits':['Tests neutral skeleton and six native facial snapshots only; no arbitrary-pose proof','Body pose skin loss measured separately','Numeric roundtrip does not prove Blink eyelid occlusion or art quality'],'artApproved':False,'physicalIPhone':False}
(folder/'glb-roundtrip.json').write_text(json.dumps(report,indent=2)+'\n');print('GLB_ROUNDTRIP',report['result'],'max',maxError,'triangles',triangles,'primitives',len(primitiveReport))
