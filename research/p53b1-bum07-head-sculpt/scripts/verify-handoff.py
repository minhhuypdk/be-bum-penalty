"""Offline dossier integrity and scope checks. Never approves art or touches services."""
from pathlib import Path
import hashlib,json,subprocess,struct
r=Path(__file__).resolve().parents[1];repo=r.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((r/'evidence/native-audit.json').read_text());m=json.loads((r/'evidence/render-metadata.json').read_text())
assert len(m['renders'])==4 and m['same_model_all_views']
assert m['blend_sha256']==sha(r/'bum07-p53b1-head-study.blend')
assert a['source_reference_preserved'] and a['actions']==0 and a['armatures']==0
assert all(x['PASS'] for x in a['optics'])
for x in m['renders']:
 p=r/x['file'];b=p.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';assert struct.unpack('>II',b[16:24])==(1200,1600);assert sha(p)==x['sha256'];assert x['model_fingerprint_before_and_after']==m['model_fingerprint'] and x['lights_unchanged'] and x['type']=='ORTHO' and x['ortho_scale']==1.5
for name in ['face-front-000.png','face-three-quarter-045.png']:assert sha(r/'renders/before'/name)==sha(r.parent/'p53ar-bum07-refinement/renders/after'/name)
assert sha(r/'reference/bum07-p53ar-preserved.blend')==sha(r.parent/'p53ar-bum07-refinement/bum07-p53ar-refinement.blend')
assert (r/'BUM07-P53B1-HEAD-REVIEW.pdf').read_bytes().startswith(b'%PDF-')
assert m['art_result']=='FAIL_ARTISTIC_OBJECTIVE'
for file,expected in json.loads((r/'SHA256SUMS.json').read_text()).items():assert sha(r/file)==expected,file
print('HANDOFF_INTEGRITY_PASS; ARTISTIC_OBJECTIVE_FAIL; NO_RUNTIME_OR_IPHONE_CLAIM')
