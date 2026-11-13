"""Evidence packaging only: no asset generation, purchase, database or deployment."""
from pathlib import Path
import json,hashlib,zipfile,sys,re
p=Path(__file__).resolve().parents[1];repo=p.parents[1];load=lambda f:json.loads(f.read_text());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=load(p/'candidates.json');assets=d['candidates'];assert len(assets)>=3 and len({a['id']for a in assets})==len(assets)
assert d['ownerAcceptance']=={'P31R_Blink100':True,'P31R_OverallArt':False};assert not d['assetChoiceApproved']and not d['BUMAdaptationCreated']and not d['gameReplacementAllowed']
for a in assets:
 assert a['source'].startswith('https://')and a['previewURL'].startswith('https://')and a['license']in ['CC-BY-4.0','CC0-1.0']
 if a['previewLocal']:assert (p/a['previewLocal']).exists()
 if not a['inspectedBinary']:assert all(a[k]is None for k in ['baseTrianglesMeasured','GLBBytesMeasured','GLBPrimitivesMeasured','GLBJointsMeasured','blendshapesMeasured'])
assert not any(f.suffix.lower()in ['.blend','.glb','.fbx']for f in p.rglob('*')if f.is_file()),'No raw donor/game assets in this first research handoff'
scott=next(a for a in assets if a['id']=='scott');audit=load(p/'audits/scott-audit.json');probe=load(p/'audits/scott-export-probe.json');glb=load(p/'audits/scott-glb-audit.json');preview=load(p/'renders/original-asset-preview.json')
assert audit['readOnly']and audit['autoExecDisabled']and probe['sourceUnchanged'];assert audit['sourceSha256']==probe['sourceSha256'];assert audit['totals']['baseTriangles']==scott['baseTrianglesMeasured']==glb['triangles'];assert audit['totals']['shapeKeys']==0==scott['blendshapesMeasured'];assert glb['bytes']==probe['GLBBytes']==scott['GLBBytesMeasured'];assert glb['primitives']==scott['GLBPrimitivesMeasured'];assert glb['joints']==[scott['GLBJointsMeasured']]
assert preview['result']=='PASS_STATIC_PREVIEW_ONLY'and not preview['BUMAdaptation']and not preview['physicalIPhone']and not preview['ownerAssetApproval'];assert preview['noSupabaseRequests']and not preview['errors'];assert preview['sourceHashes']['Scott']==probe['GLBSha256']
assert preview['sourceHashes']['P31R']==sha(repo/'research/bum07-p31r/assets/bum07-p31r-experimental.glb')
assert len(preview['shots'])==10
for shot in preview['shots']:assert sha(p/'renders'/shot['file'])==shot['sha256']
for sid in ['front','45','profile','close','body']:
 rows=[s for s in preview['shots']if s['id']==sid];assert len(rows)==2
 for k in ['camera','target']:assert all(abs(a-b)<1e-6 for a,b in zip(rows[0]['view'][k],rows[1]['view'][k]))
 assert (p/'comparison'/(sid+'.png')).exists()
assert (p/'ASSET-CANDIDATES-P4.pdf').read_bytes().startswith(b'%PDF-')
for f in p.rglob('*.html'):
 for href in re.findall(r'(?:href|src)="([^"]+)"',f.read_text()):
  if not href.startswith(('http','#')):assert(f.parent/href).exists(),href
validation={'result':'PASS_RESEARCH_EVIDENCE_ONLY','candidates':len(assets),'localPublisherPreviews':sum(bool(a['previewLocal'])for a in assets),'publisherPreviewLinksOnly':['spring','storm'],'nativeBinaryInspected':['scott'],'originalAssetPreviewEngine':'WebKit WPE Linux','ScottStaticGLBExport':'PASS_WITH_SKIN_INFLUENCE_WARNING','ScottAnimatedEquivalence':'NOT_VERIFIED','physicalIPhone':False,'ownerApprovedP31RBlinkOnly':True,'ownerApprovedOverallArt':False,'donorApproved':False,'BUMDonorTrialCreated':False,'gameReplacement':False,'purchaseOrSubscription':False,'protectedP31RGLBHashMatches':True,'noSupabaseRequestsInPreview':True,'quality9Verified':False,'unmeasuredCandidateMetricsRemainNull':True}
(p/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
entries=[{'path':f.relative_to(p).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)}for f in sorted(p.rglob('*'))if f.is_file()and f.name!='MANIFEST.json'and '__pycache__'not in f.parts];(p/'MANIFEST.json').write_text(json.dumps({'phase':'P4_RESEARCH','ownerApprovalRequiredBeforeAdaptation':True,'files':entries},indent=2)+'\n')
out=Path(sys.argv[1])if len(sys.argv)>1 else repo/'artifacts/BUM07-P4-Asset-Research.zip';out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for f in sorted(p.rglob('*')):
  if f.is_file()and '__pycache__'not in f.parts:z.write(f,f.relative_to(p).as_posix())
with zipfile.ZipFile(out)as z:assert z.testzip()is None
out.with_suffix('.zip.sha256').write_text(sha(out)+'  '+out.name+'\n');print(json.dumps({'result':validation['result'],'zip':str(out),'bytes':out.stat().st_size,'sha256':sha(out)}))
