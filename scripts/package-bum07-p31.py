"""Validate shipped P3.1 evidence and package. Does not generate/edit meshes."""
from pathlib import Path
import json,hashlib,sys,zipfile,struct
root=Path(__file__).resolve().parents[1];p=root/'research/bum07-p31';load=lambda f:json.loads(f.read_text());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
base=root/'docs/artist-production/BUM07/BASELINE-P2/artist/bum07-facehair-workbench.blend';assert sha(base)=='30338d105c61eb206b688d31d74f9a7ccd947607f7ad67a5aff89833a8cb2f4c'
manifest=load(p/'assets/manifest.json')
for f,meta in manifest['exports'].items():assert sha(p/'assets'/f)==meta['sha256']
assert manifest['sourceSha256']==sha(base)and manifest['rigActionsUnchanged']and not manifest['artApproved']
audit=load(p/'assets/source-audit.json');assert audit['result']=='PASS_WITH_LIMITATIONS'and audit['originalMeshesPreserved']==95 and audit['originalRigActionsPreserved']
assert all(x['zeroAreaTriangles']==0 for x in audit['morphDeformation'])
glb=load(p/'assets/glb-audit.json');assert glb['result']=='PASS'and glb['sha256']==sha(p/'assets/bum07-p31-experimental.glb')
canonicalP2=load(root/'docs/artist-production/BUM07/BASELINE-P2/artist/manifest.json');assert any(x['sha256']==sha(p/'reference/p2-original.glb')for x in canonicalP2['exports'])
expected={'graphics/models/bum07/bum07-study-portrait.glb':sha(root/'graphics/models/bum07/bum07-study-portrait.glb'),'graphics/models/p2-original.glb':sha(p/'reference/p2-original.glb'),'graphics/models/bum07-p31/bum07-p31-experimental.glb':sha(p/'assets/bum07-p31-experimental.glb')}
for engine in ['chromium','webkit']:
 report=load(p/'renders'/engine/'browser-report.json');assert report['result']=='PASS'and report['engine']==engine and report['noSupabaseRequests']and not report['errors']and not report['physicalIPhone'];assert report['sourceHashes']==expected
 shots=report['shots'];assert len(shots)==12 and {s['variant']for s in shots}=={'C','P2','P3.1'}
 for s in shots+report['motion']:assert sha(p/'renders'/engine/s['file'])==s['sha256']
 for sid in ['front','45','profile','close']:
  rows=[s for s in shots if s['id']==sid]
  for s in rows:
   for k in ['camera','target']:assert all(abs(a-b)<1e-6 for a,b in zip(s['view'][k],rows[0]['view'][k]))
  assert (p/'comparison'/(sid+'.png')).exists()
review=load(p/'visual-review.json');assert review['result']=='FAIL_ART_TARGET'and not review['ownerApproval']and not review['score9Verified']and not review['nextPhaseAuthorized']
validation={'result':'EVIDENCE_PACKAGE_PASS_ART_GATE_FAIL','geometryDataChecks':'PASS_WITH_LIMITATIONS','visualArtGate':review['result'],'facialRigGate':review['facialDeformation'],'browserLoadRender':{'chromium':'PASS','webkit':'PASS'},'physicalIPhone':False,'sourceP2Unchanged':True,'artApproved':False,'nextPhaseAuthorized':False,'noSupabaseRequestsInBrowserTests':True}
(p/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
entries=[{'path':f.relative_to(p).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)}for f in sorted(p.rglob('*'))if f.is_file()and f.name!='HANDOFF-MANIFEST.json']
(p/'HANDOFF-MANIFEST.json').write_text(json.dumps({'version':'P3.1','sourceBaseline':'47cfa8c','files':entries,'artGate':'FAIL_ART_TARGET'},indent=2)+'\n')
out=Path(sys.argv[1])if len(sys.argv)>1 else root/'artifacts/BUM07-P3.1-Handoff.zip';out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for f in sorted(p.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(p).as_posix())
with zipfile.ZipFile(out)as z:assert z.testzip()is None
out.with_suffix('.zip.sha256').write_text(sha(out)+'  '+out.name+'\n');print(json.dumps({'result':validation['result'],'zip':str(out),'sha256':sha(out),'bytes':out.stat().st_size}))
