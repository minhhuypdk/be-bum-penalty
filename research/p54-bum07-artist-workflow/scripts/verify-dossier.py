"""Offline evidence/document integrity. No service writes or model edits."""
from pathlib import Path
import ast,json,hashlib,re
r=Path(__file__).resolve().parents[1]
c=json.loads((r/'candidates.json').read_text());assert c['baseline'].startswith('928d212') and len(c['candidates'])==5
assert not c['production_sculpt_started'] and not c['artist_hired'] and c['purchases']==0 and c['owner_choice']=='PENDING'
assert all(not x['game_model_replaced'] and not x['BUM_adaptation_created'] and not x['art_approved'] for x in c['candidates'])
a=json.loads((r/'evidence/read-only-mesh-audit.json').read_text());assert {x['label'] for x in a}=={'R','B1','Tiby'};assert all(x['source_bytes_unchanged'] and not x['saved_or_exported'] and not x['autoexec'] for x in a)
h=json.loads((r/'evidence/human-bundle-audit.json').read_text());assert h['source_unchanged'] and not h['saved_or_exported'] and not h['autoexec']
g=next(x for x in h['head_eye_jaw_meshes'] if x['name']=='Head - Generic Topology');assert (g['vertices_raw'],g['quad_faces_raw'],g['triangles_base'])==(318,316,632);assert 'Real_Kid' in g['shape_keys']
m=next(x for x in h['asset_metadata'] if x['name']=='Head - Generic Topology');assert m['author']=='Paul Kotelevets' and m['license']=='CC0'
assert any('Rain Rig' in x['text'] and 'Attribution 4.0' in x['text'] for x in h['embedded_notices'])
assert any('All provided assets are public domain under the CC0 license.' in x['text'] for x in h['embedded_notices'])
assert not h['armatures']
for x in c['candidates']:
 assert x['commercial_game_use'] and x['modification'] and x['raw_mesh_redistribution'] and x['measured_5H_match'] is None
assert (r/'BUM07-P54-WORKFLOW-EVALUATION.pdf').read_bytes().startswith(b'%PDF-')
for p in r.rglob('*'):
 if p.is_file():assert p.suffix.lower() not in ['.blend','.blend1','.glb','.gltf','.fbx','.zip'],str(p)
for p in (r/'scripts').glob('*.py'):ast.parse(p.read_text())
for n in ['read-only-mesh-audit.py','inspect-human-bundle.py']:
 s=(r/'scripts'/n).read_text();assert 'use_scripts=False' in s
 assert not any(k in s for k in ['save_as_mainfile','bpy.ops.export','bpy.ops.sculpt','bpy.ops.mesh.primitive'])
for name,expected in json.loads((r/'SHA256SUMS.json').read_text()).items():assert hashlib.sha256((r/name).read_bytes()).hexdigest()==expected,name
print('P54_DOSSIER_INTEGRITY_PASS;5CANDIDATES;READ_ONLY_NATIVE_PROOFS;NO_ART_OR_IPHONE_APPROVAL')
