"""Manifest this dossier only. No API, Git or protected-file writes."""
from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parents[1]
files=[p for p in r.rglob('*') if p.is_file() and p.name not in ['SHA256SUMS.json','review.html'] and '__pycache__' not in p.parts and not p.name.endswith('.blend1')]
(r/'SHA256SUMS.json').write_text(json.dumps({str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2)+'\n')
print('MANIFEST_CREATED',len(files))
