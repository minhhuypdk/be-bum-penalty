"""Validate shipped proof integrity, not pretend to rerun Blender or browsers."""
from pathlib import Path
import json,hashlib,sys,struct,zipfile
root=Path(__file__).resolve().parents[1];ev=root/'evidence';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((root/'SHA256SUMS.json').read_text())
for name,h in manifest.items():assert sha(root/name)==h,name
r=json.loads((ev/'build-report.json').read_text());assert r['nativeJoints']==370 and r['jointsRemoved']==0 and r['runtimeSkinInfluences']==4
assert sha(root/'source/scott-original.blend')==r['sourceSha256']=='95b9848fd0c4a1c9ee94a2ae3a9f6136af71c97256ef63ab7a37017470846568'
for name,rec in r['exports'].items():assert sha(root/'assets'/name)==rec['sha256'] and (root/'assets'/name).stat().st_size==rec['bytes']
f=root/'assets/scott-bum07-p41-prototype.glb';b=f.read_bytes();assert struct.unpack_from('<III',b)==(0x46546c67,2,len(b));n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);assert len(d['skins'])==1 and len(d['skins'][0]['joints'])==370
pr=[p for m in d['meshes']for p in m['primitives']];assert len(pr)==21;assert sum(d['accessors'][p['indices']]['count']//3 for p in pr)==103798
assert all('JOINTS_0'in p['attributes'] and 'JOINTS_1'not in p['attributes']for p in pr)
assert not d.get('animations');assert not any(a.startswith('COLOR_')for p in pr for a in p['attributes'])
roundtrip=json.loads((ev/'glb-roundtrip.json').read_text());assert roundtrip['result']=='PASS' and roundtrip['GLBSha256']==sha(f)
assert roundtrip['referenceSha256']==sha(ev/'native-face-reference.npz');assert roundtrip['maxWorldError']<1e-4
for engine in ['chromium','webkit']:
 folder=ev/engine;q=json.loads((folder/'browser-report.json').read_text());assert not q['quick'] and q['result']=='PASS_RENDER_EXECUTION' and not q['errors'] and q['noSupabaseRequests'];assert q['sourceHashes']['P41']==sha(f)
 assert len(q['shots'])==15 and len(q['expressions'])==16 and len(q['eyeID'])==10
 assert not q['physicalIPhone'] and not q['artApproved']
 for x in q['shots']+q['expressions']+q['eyeID']:assert sha(folder/x['file'])==x['sha256']
 assert q['Blink100Gate']==('PASS'if all(x['eyePixels']==0 for x in q['eyeID']if x['value']==1)else'FAIL')
assert json.loads((ev/'webkit/browser-report.json').read_text())['Blink100Gate']=='FAIL' # preserve failure, no accidental greenwashing
assert not r['artApproved'] and not r['gameReplaced']
assert json.loads((ev/'public-pages-check.json').read_text())['unchanged']
out=Path(sys.argv[1]).resolve();assert root not in out.parents;out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for f in sorted(root.rglob('*')):
  if f.is_file() and '__pycache__'not in f.parts:z.write(f,Path('BUM07-P41-Scott-Research')/f.relative_to(root))
Path(str(out)+'.sha256').write_text(sha(out)+'  '+out.name+'\n')
print('PASS EVIDENCE_INTEGRITY / PROTOTYPE_ACCEPTANCE_FAIL',out.stat().st_size)
