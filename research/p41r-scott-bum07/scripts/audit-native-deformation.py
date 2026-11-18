"""Native Preserve Volume vs decoded GLB at real non-neutral bone poses.
No pose corrective or sports-clip claims. Keeps all370 bones and all weights.
Exports deterministic sample fixtures for actual GPU shader readback in browsers.
"""
import sys,json,runpy,hashlib,math
from pathlib import Path
import bpy,numpy as np
from mathutils import Matrix,Vector
out=Path(sys.argv[sys.argv.index('--')+1]);sys.path.insert(0,str(Path(__file__).resolve().parent))
from dq_math import bone_parts
# The independent binary reader validates the GLB/morph snapshots first.
lib=runpy.run_path(str(Path(__file__).with_name('check-glb-roundtrip.py')));d=lib['d'];accessor=lib['accessor'];nodeM=lib['nodeM']
rig=bpy.data.objects['P41_ScottRig_370'];native=list(bpy.data.collections['01_SCOTT_BUM07_P41'].objects)
for o in native:o.hide_set(False);o.hide_render=False
for o in bpy.data.collections['02_RUNTIME_COMPENSATED'].objects:o.hide_set(True)
basis={b.name:b.matrix_basis.copy()for b in rig.pose.bones};N0={b.name:rig.matrix_world@b.matrix.copy()for b in rig.pose.bones};C=Matrix(((1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)))
skin=d['skins'][0];jointNames=[d['nodes'][i]['name']for i in skin['joints']];G0=[nodeM(i).copy()for i in skin['joints']];inv=accessor(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1).astype(float)
poses=[('Neutral',{}),('ArmL_15',{'L':(.15,-.08)}),('ArmL_35',{'L':(.35,-.18)}),('ArmL_55',{'L':(.55,-.25)}),('ArmR_35',{'R':(.35,-.18)}),('ArmsBoth',{'L':(.4,-.2),'R':(.4,-.2)}),('FootL',{'foot':'L'}),('FootR',{'foot':'R'}),('HeadLeft',{'head':-.35}),('HeadRight',{'head':.35}),('HeadArm',{'head':.25,'L':(.35,-.2)}),('ArmAcross',{'L':(.2,-.4)})]
def posed(params):
 for b in rig.pose.bones:b.matrix_basis=basis[b.name]
 for side in ['L','R']:
  if side in params:
   z,y=params[side];rig.pose.bones['Bone.Hand.'+side].location.z+=z;rig.pose.bones['Bone.Hand.'+side].location.y+=y
 if'foot'in params:rig.pose.bones['Bone.Leg.004.'+params['foot']+'.001'].location.y-=.35
 if'head'in params:rig.pose.bones['Bone.Head'].matrix_basis=basis['Bone.Head']@Matrix.Rotation(params['head'],4,'Z')
 rig.update_tag(refresh={'OBJECT'});bpy.context.view_layer.update()
def fast_dqs(jointM,joints,weights):
 # Vectorized implementation independent of the scalar builder evaluator.
 parts=[bone_parts(Matrix(m.tolist()),Matrix(rest.tolist()).inverted())for m,rest in zip(jointM,inv)]
 Q=np.array([tuple(p[0])for p in parts]);D=np.array([tuple(p[1])for p in parts]);K=np.array([np.array(p[2])for p in parts])
 qi=Q[joints];di=D[joints];sign=np.where(np.einsum('vnc,vc->vn',qi,qi[:,0])<0,-1,1)
 q=np.einsum('vn,vnc->vc',weights*sign,qi);dual=np.einsum('vn,vnc->vc',weights*sign,di);length=np.linalg.norm(q,axis=1);q/=length[:,None];dual/=length[:,None]
 w,x,y,z=q.T;R=np.zeros((len(q),4,4));R[:,0,0]=1-2*(y*y+z*z);R[:,0,1]=2*(x*y-w*z);R[:,0,2]=2*(x*z+w*y);R[:,1,0]=2*(x*y+w*z);R[:,1,1]=1-2*(x*x+z*z);R[:,1,2]=2*(y*z-w*x);R[:,2,0]=2*(x*z-w*y);R[:,2,1]=2*(y*z+w*x);R[:,2,2]=1-2*(x*x+y*y);R[:,3,3]=1
 # translation = 2 * (dual * conjugate(real)).xyz
 R[:,:3,3]=2*(-dual[:,0,None]*q[:,1:]+q[:,0,None]*dual[:,1:]-np.cross(dual[:,1:],q[:,1:]))
 S=np.einsum('vn,vnij->vij',weights,K[joints]);return R@S
primitives=[]
for ni,node in enumerate(d['nodes']):
 if'mesh'not in node:continue
 nativeName=node['name'].removesuffix('_Runtime');o=bpy.data.objects[nativeName]
 for pi,pr in enumerate(d['meshes'][node['mesh']]['primitives']):
  a=pr['attributes'];sets=sorted(int(k.split('_')[1])for k in a if k.startswith('JOINTS_'));pos=accessor(a['POSITION']).astype(float);ids=np.rint(accessor(a['_P41_SOURCE_ID']).ravel()).astype(int);js=np.concatenate([accessor(a['JOINTS_'+str(i)])for i in sets],axis=1).astype(int);ws=np.concatenate([accessor(a['WEIGHTS_'+str(i)])for i in sets],axis=1).astype(float)
  primitives.append((node,o,pi,pos,ids,js,ws))
fixture={'GLBSha256':hashlib.sha256((out/'scott-bum07-p41r-prototype.glb').read_bytes()).hexdigest(),'jointNames':jointNames,'poses':[],'scope':'Native bone-world delta snapshots and vertex samples; not animation clips or arbitrary-pose certification'};checks=[];neutral=None
for label,params in poses:
 posed(params);nativePoints={}
 for o in native:
  if o.type!='MESH':continue
  e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();P=np.array([tuple(C@o.matrix_world@v.co)for v in m.vertices]);e.to_mesh_clear();nativePoints[o.name]=P
 if neutral is None:neutral=nativePoints
 jointM=np.array([np.array(C@(rig.matrix_world@rig.pose.bones[n].matrix)@N0[n].inverted()@C.inverted()@g)for n,g in zip(jointNames,G0)])
 boneLocal=[];byNode={node:jointM[i]for i,node in enumerate(skin['joints'])};parents=lib['parents']
 for i,nodeID in enumerate(skin['joints']):
  parent=parents.get(nodeID);pg=byNode.get(parent,np.array(nodeM(parent))if parent is not None else np.eye(4));boneLocal.append((np.linalg.inv(pg)@jointM[i]).flatten(order='F').tolist())
 row={'name':label,'params':params,'boneLocalMatrices':boneLocal,'samples':{}}
 for node,o,pi,pos,ids,js,ws in primitives:
  dq=node.get('extras',{}).get('P41R_skinning')=='DUAL_QUATERNION';M=fast_dqs(jointM,js,ws)if dq else np.einsum('vn,vnij->vij',ws,(jointM@inv)[js]);xyz=np.einsum('vij,vj->vi',M,np.c_[pos,np.ones(len(pos))])[:,:3];expected=nativePoints[o.name][ids];err=np.linalg.norm(xyz-expected,axis=1);disp=np.linalg.norm(nativePoints[o.name]-neutral[o.name],axis=1)
  checks.append({'pose':label,'mesh':node['name'],'primitive':pi,'method':'DQS'if dq else'LBS','maxError':float(err.max()),'rmsError':float(np.sqrt(np.mean(err**2))),'maxNativeDisplacement':float(disp.max())})
  # Systematic whole-surface samples plus worst-error vertices. Shared IDs avoid UV seam ambiguity.
  pick=np.unique(np.r_[np.arange(0,len(ids),max(1,len(ids)//128)),np.argsort(err)[-8:]])
  samples=row['samples'].setdefault(node['name'],{})
  for k in pick:samples[str(int(ids[k]))]=expected[k].tolist()
 fixture['poses'].append(row);print('POSE',label,'max',max(x['maxError']for x in checks if x['pose']==label),flush=True)
posed({});maxErr=max(x['maxError']for x in checks);report={'GLBSha256':fixture['GLBSha256'],'result':'PASS'if maxErr<1e-4 else'FAIL','tolerance':1e-4,'maxError':maxErr,'jointCount':len(jointNames),'poses':len(poses),'checks':checks,'nativePreserveVolumeKept':True,'allInfluencesKept':True,'scope':'Decoded actual GLB + native evaluated bone poses. No pose morph corrections used. Requires DQS adapter for flagged meshes; vanilla glTF uses LBS.'}
(out/'native-deformation.json').write_text(json.dumps(report,indent=2)+'\n');(out/'gpu-pose-fixture.json').write_text(json.dumps(fixture,separators=(',',':'))+'\n');print('NATIVE_GL B_DEFORMATION',report['result'],maxErr)
