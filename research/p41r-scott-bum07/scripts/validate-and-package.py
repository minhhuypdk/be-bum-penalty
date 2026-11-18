"""Integrity/acceptance-boundary checks of shipped evidence, not a CI rerender.
Must never change failure/approval flags merely to turn the packaging job green.
"""
from pathlib import Path
import json,sys,struct,hashlib,zipfile,subprocess,tempfile
root=Path(__file__).resolve().parents[1];repo=root.parents[1];ev=root/'evidence';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
for f,h in read(root/'SHA256SUMS.json').items():assert sha(root/f)==h,f
r=read(ev/'build-report.json');assert r['phase']=='P4.1R'and r['nativeJoints']==370 and r['jointsRemoved']==0 and r['runtimeSkinInfluences']=='ALL'and r['nativePreserveVolumeKept']
for n,x in r['exports'].items():assert sha(root/'assets'/n)==x['sha256']and(root/'assets'/n).stat().st_size==x['bytes']
f=root/'assets/scott-bum07-p41r-prototype.glb';raw=f.read_bytes();assert struct.unpack_from('<III',raw)==(0x46546c67,2,len(raw));n=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+n]);assert len(d['skins'])==1 and len(d['skins'][0]['joints'])==370
base=repo/'research/p41-scott-bum07';b=(base/'assets/scott-bum07-p41-prototype.glb').read_bytes();old=json.loads(b[20:20+struct.unpack_from('<I',b,12)[0]]);names=lambda a:{a['nodes'][i]['name']for i in a['skins'][0]['joints']};assert names(d)==names(old)
source=base/'source/scott-original.blend';assert sha(source)==r['sourceSha256']=='95b9848fd0c4a1c9ee94a2ae3a9f6136af71c97256ef63ab7a37017470846568'
assert sha(base/'assets/scott-bum07-p41-prototype.glb')=='5ae2bac2f706364c7a6133b45e35534df0728d942ac01dbad976ff89bea0ee4b'
pr=[p for m in d['meshes']for p in m['primitives']];assert len(pr)==17 and sum(d['accessors'][p['indices']]['count']//3 for p in pr)==104791
assert max(sum(k.startswith('JOINTS_')for k in p['attributes'])for p in pr)==7
assert not any('uri'in x for x in d.get('images',[])+d.get('buffers',[]));assert not d.get('animations')
rr=read(ev/'glb-roundtrip.json');assert rr['GLBSha256']==sha(f)and rr['result']=='PASS'and rr['maxWorldError']<1e-4
assert rr['referenceSha256']==sha(ev/'native-face-reference.npz');assert rr['globeIntegrity']and all(x['maxBlinkDisplacement']==0 and x['noAddedIrisGeometry']for x in rr['globeIntegrity'])
native=read(ev/'native-deformation.json');assert native['GLBSha256']==sha(f)and native['result']=='PASS'and native['poses']==12 and native['maxError']<1e-4
assert read(ev/'gpu-pose-fixture.json')['GLBSha256']==sha(f)
work=read(ev/'workbench-audit.json');assert work['result']=='PASS'and work['fileSha256']==sha(root/'assets/scott-bum07-p41r-editable.blend')and work['nativeCorrectiveDrivers']==2
geo=read(ev/'geometry-audit.json');assert geo['result']=='PASS_SCOPED'
for x in geo['meshes']:
 assert not any(x[k]for k in ['nonManifoldNonBoundaryEdges','zeroAreaFaces','nonFiniteNormals','zeroUVAreaFaces','inconsistentWindingEdges'])
 assert all(p['classification']!='UNCLASSIFIED'for p in x['boundaryComponents'])
for engine in ['webkit','chromium']:
 folder=ev/engine;q=read(folder/'browser-report.json');assert not q['quick']and q['result']=='PASS_RENDER_EXECUTION'and not q['errors']and q['noSupabaseRequests'];assert q['sourceHashes']['P41R']==sha(f)
 assert len(q['shots'])==10 and len(q['expressions'])==16 and len(q['eyeID'])==10 and len(q['mobileViewport'])==4
 for x in q['shots']+q['expressions']+q['eyeID']+q['mobileViewport']+q['poseShots']:assert sha(folder/x['file'])==x['sha256']
 for angle in [0,45]:
  ids=[x for x in q['eyeID']if x['angle']==angle];assert ids[0]['eyePixels']>100 and ids[-1]['eyePixels']==0;assert all(a['eyePixels']>=b['eyePixels']for a,b in zip(ids,ids[1:]))
 assert q['Blink100Gate']=='PASS'and all(x['eyePixels']==0 for x in q['mobileViewport']if x['value']==1)
 gpu=q['gpuDeformation'];assert gpu['result']=='PASS'and len(gpu['checks'])==36 and all(x['samples']>0 and x['maxError']<1e-4 for x in gpu['checks']);assert len({x['pose']for x in gpu['checks']})==12
 assert not q['physicalIPhone']and not q['artApproved']
 for view in ['front','45','profile','close','body']:
  a,b=[x for x in q['shots']if x['id']==view];assert a['view']['camera']==b['view']['camera']and a['view']['target']==b['view']['target']and abs(a['view']['angle']-b['view']['angle'])<1e-8
summary=read(ev/'summary.json');assert summary['artApproval']=='PENDING_OWNER'and not summary['quality9of10Claimed']and not summary['gameReady']and not summary['physicalIPhoneTested']and summary['stopAfterHandoff']and summary['requiresCustomDQSAdapter']
assert read(ev/'protection.json')['pagesUnchanged']
out=Path(sys.argv[1]).resolve();assert root not in out.parents;out.parent.mkdir(parents=True,exist_ok=True)
# A staged viewer is built for inspection, not deployed. It retains original A/B/C.
with tempfile.TemporaryDirectory(prefix='p41r-package-')as tmp:
 viewer=Path(tmp)/'viewer';subprocess.run([sys.executable,str(root/'scripts/stage-review.py'),str(viewer),str(root/'assets'),str(base/'source/scott-original-probe.glb')],cwd=repo,check=True)
 # stage-review needs only the GLB for manual import; include native pose fixture too.
 (viewer/'graphics/models/gpu-pose-fixture.json').write_bytes((ev/'gpu-pose-fixture.json').read_bytes())
 for p,h in read(ev/'viewer-source-hashes.json').items():assert sha(viewer/p)==h,p
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
  prefix=Path('BUM07-P41R-Scott-Research')
  for p in sorted(root.rglob('*')):
   if p.is_file()and'__pycache__'not in p.parts:z.write(p,prefix/p.relative_to(root))
  for p in sorted(viewer.rglob('*')):
   if p.is_file():z.write(p,prefix/'viewer'/p.relative_to(viewer))
  for p,name in [(source,'scott-original.blend'),(base/'assets/scott-bum07-p41-prototype.glb','scott-bum07-p41-prototype.glb'),(base/'ATTRIBUTION.md','P41-ATTRIBUTION.md')]:z.write(p,prefix/'reference'/name)
Path(str(out)+'.sha256').write_text(sha(out)+'  '+out.name+'\n');print('PASS_EVIDENCE_INTEGRITY_AND_SCOPED_QA / ART_PENDING / CUSTOM_ADAPTER_REQUIRED',out.stat().st_size)
