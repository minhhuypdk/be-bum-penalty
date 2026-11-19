"""Verify saved evidence and PNG/PDF files; does not approve visual quality."""
from pathlib import Path
from PIL import Image
import hashlib,json,subprocess
r=Path(__file__).resolve().parents[1];meta=json.loads((r/'evidence/render-metadata.json').read_text());audit=json.loads((r/'evidence/mesh-camera-audit.json').read_text())
assert json.loads((r/'evidence/palette-readback.json').read_text())['palette_materials_PASS']==10
assert len(meta['renders'])==7 and len(meta['aliases'])==1
assert audit['number_surface_PASS'] and audit['static_eye_visibility_PASS']
assert audit['armatures']==0 and audit['actions']==0 and audit['shape_keys']==0
assert audit['upper_teeth_connected_components']==8 and audit['upper_arch_objects']==1
assert not audit['hidden_character_objects'] and not audit['hidden_character_collections']
for record in meta['renders']:
 p=r/record['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'];assert record['model_fingerprint_before_and_after']==meta['model_fingerprint'];assert record['lights_unchanged']
 with Image.open(p) as im:assert im.size==(1200,1600);im.verify()
assert (r/'renders/full-a-pose-000.png').read_bytes()==(r/'renders/full-front-000.png').read_bytes()
assert hashlib.sha256((r/'bum07-p53a-blockout.blend').read_bytes()).hexdigest()==meta['blend_sha256']
assert not any(p.suffix.lower() in ['.glb','.gltf'] for p in r.rglob('*'))
info=subprocess.check_output(['pdfinfo',str(r/'BUM07-P53A-BLOCKOUT-COMPARISON.pdf')],text=True)
assert 'A4' in info
readback={'png_decode_PASS':8,'independent_renders':7,'explicit_A_pose_alias':1,'resolution':[1200,1600],'model_fingerprint_consistent':True,'lights_fixed':True,'native_blend_sha256_matches':True,'pdfinfo':info,'visual_review':'PENDING_MANUAL_READBACK; file integrity does not approve art.','art_finish':'FAIL / NOT_APPROVED','future_phase_authorization':'CLOSED'}
(r/'evidence/handoff-verification.json').write_text(json.dumps(readback,ensure_ascii=False,indent=2))
print('PASS_HANDOFF_INTEGRITY_NOT_ART_APPROVAL')
