"""Integrity and scoped technical checks. Does not approve art."""
from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
r=Path(__file__).resolve().parents[1];base=r.parent/'p53a-bum07-blender-blockout';meta=json.loads((r/'evidence/render-metadata.json').read_text());audit=json.loads((r/'evidence/mesh-camera-audit.json').read_text());lineage=json.loads((r/'evidence/lineage-audit.json').read_text())
assert len(meta['renders'])==6 and meta['before_after_camera_lights_identical']
assert audit['number_surface_PASS'] and audit['static_eye_visibility_PASS']
assert all(x['finite_vertices'] and x['zero_area_faces']==0 for x in audit['geometry'])
assert not audit['hidden_character_objects'] and not audit['hidden_character_collections']
assert audit['armatures']==0 and audit['actions']==0 and audit['shape_keys']==0 and audit['upper_teeth_connected_components']==8
assert json.loads((r/'evidence/palette-readback.json').read_text())['palette_materials_PASS']==10
assert all(value is True for key,value in lineage['checks'].items() if key!='scope')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'bum07-p53ar-refinement.blend')==meta['blend_sha256']==lineage['after']['file_sha256']
assert sha(base/'bum07-p53a-blockout.blend')==lineage['before']['file_sha256']
assert json.loads((r/'evidence/curve-diagnosis-before.json').read_text())['source_sha256']==lineage['before']['file_sha256']
assert json.loads((r/'evidence/curve-diagnosis-after.json').read_text())['source_sha256']==meta['blend_sha256']
rois=json.loads((r/'evidence/iris-projection-sources.json').read_text());assert rois['after']['source_sha256']==meta['blend_sha256'];assert rois['before']['source_sha256']==lineage['before']['file_sha256']
for item in meta['renders']:
 p=r/item['file'];assert sha(p)==item['sha256'];assert item['model_fingerprint_before_and_after']==meta['model_fingerprint'];assert item['lights_unchanged']
 with Image.open(p) as im:assert im.size==(1200,1600);im.verify()
 before=r/'renders/before'/p.name;assert before.read_bytes()==(base/'renders'/p.name).read_bytes()
 with Image.open(before) as im:assert im.size==(1200,1600);im.verify()
optics=json.loads((r/'evidence/optical-clearance-final.json').read_text());assert all(x['PASS_cap_outside_globe'] for x in optics['rows']);assert all(x['source_sha256']==meta['blend_sha256'] for x in optics['rows'] if x['version']=='R')
assert not any(p.suffix.lower() in ['.glb','.gltf'] for p in r.rglob('*'))
info=subprocess.check_output(['pdfinfo',str(r/'BUM07-P53AR-COMPARISON.pdf')],text=True);assert 'A4' in info
out={'files_before_after_pngs_PASS':12,'independent_after_renders':6,'resolution':[1200,1600],'native_blend_sha256_matches':True,'lineage_camera_world_lights_PASS':True,'numeric_zero_face_count':0,'source_P53A_unchanged':True,'pdfinfo':info,'visual_review':'PENDING_READBACK_NOT_ART_APPROVAL','art_approval':'OWNER_PENDING','P53B':'CLOSED'};(r/'evidence/handoff-verification.json').write_text(json.dumps(out,indent=2));print('PASS_HANDOFF_INTEGRITY_NOT_ART_APPROVAL')
