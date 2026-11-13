"""Validate actual P3.1R evidence; auto-FAIL full blink if skin penetrates eyes or ID pass leaks.
Packaging success is separate from art/production-rig acceptance.
"""
from pathlib import Path
import json,hashlib,sys,zipfile
root=Path(__file__).resolve().parents[1];p=root/'research/bum07-p31r';load=lambda f:json.loads(f.read_text());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
manifest=load(p/'assets/manifest.json');base=root/'research/bum07-p31/assets/bum07-p31-workbench.blend';assert manifest['sourceSha256']==sha(base)and manifest['sourceUnchanged']
for f,meta in manifest['exports'].items():assert sha(p/'assets'/f)==meta['sha256']
s=load(p/'assets/source-audit.json');assert s['originalMeshesUnchanged']==122 and s['originalRigActionsUnchanged']and s['candidateSha256']==sha(p/'assets/bum07-p31r-workbench.blend')and s['sourceSha256']==sha(base)
assert all(all(r[k]==0 for k in ['boundary','nonManifold','inconsistentNormals','degenerateFaces'])and r['uvFinite']for r in s['mesh'])
assert all(r['finite']and r['zeroAreaTriangles']==0 for r in s['deformation'])
g=load(p/'assets/glb-audit.json');assert g['result']=='PASS'and g['sha256']==sha(p/'assets/bum07-p31r-experimental.glb')and len(g['newNormals'])>=11
expected={'graphics/models/p31.glb':sha(root/'research/bum07-p31/assets/bum07-p31-experimental.glb'),'graphics/models/p31r/bum07-p31r-experimental.glb':sha(p/'assets/bum07-p31r-experimental.glb')};reports={};budget=[];full=[]
for engine in ['chromium','webkit']:
 r=load(p/'renders'/engine/'browser-report.json');assert r['result']=='BROWSER_RENDER_PASS'and r['sourceHashes']==expected and r['engine']==engine and not r['physicalIPhone']and not r['errors']and r['noSupabaseRequests'];reports[engine]=r
 assert len(r['shots'])==38 and len(r['eyeID'])==20
 for shot in r['shots']+r['eyeID']:assert sha(p/'renders'/engine/shot['file'])==shot['sha256']
 for angle in [0,45]:
  for variant in ['P3.1','P3.1R']:
   assert {x['value']for x in r['shots']if x['variant']==variant and x['mode']=='Blink'and x['angle']==angle}=={0,.25,.5,.75,1}
   assert {x['value']for x in r['shots']if x['variant']==variant and x['mode']=='Smile'and x['angle']==angle}=={0,.5,1}
 for angle in [0,45,90]:
  group=[x for x in r['shots']if x['mode']=='neutral'and x['angle']==angle];assert len(group)==2
  for k in ['camera','target']:assert all(abs(a-b)<1e-6 for a,b in zip(group[0]['view'][k],group[1]['view'][k]))
  for x in group:budget.append({'engine':engine,'variant':x['variant'],'angle':angle,'drawCalls':x['metrics']['drawCalls'],'renderedTriangles':x['metrics']['triangles'],'viewport':x['metrics']['renderPixels']})
 full += [x for x in r['eyeID']if x['variant']=='P3.1R'and x['value']==1]
 assert all(x['redPixels']>0 for x in r['eyeID']if x['variant']=='P3.1'and x['value']==1)
sourceFull=[x for x in s['contact']if x['blink']==1]
blink='PASS'if all(x['skinTrianglesInsideOcularEnvelope']==0 and all(v['visibleGlobeSamples']==0 for v in x['views'])for x in sourceFull)and all(x['redPixels']==0 for x in full)else 'FAIL'
# Do NOT silently convert render success into deformation/art approval.
gates={'version':'P3.1R','blink100Gate':blink,'requestedBlinkOcularContact':s['ocularTriangleContactGate'],'sampledInterpolationContact':s['interpolationContactGate'],'globalFacialDeformation':'FAIL_VISIBLE_FOLDS_AND_UNCLASSIFIED_SELF_CONTACTS','socketSurfaceForm':'FAIL_VISIBLE_FOLDS','hairArt':'PARTIAL_STILL_CAP_LIKE','artAcceptance':'PENDING_OWNER_NOT_9_OF_10','noNextPhaseAuthorized':True,'physicalIPhone':False,'fullBlinkEyeRedPixels':[{k:x[k]for k in ['angle','redPixels']}|{'engine':engine}for engine,r in reports.items()for x in r['eyeID']if x['variant']=='P3.1R'and x['value']==1],'limits':['Unclassified head self-contact candidates and mouth root contacts remain','Finite sampled poses and full-closure occlusion do not certify all continuous expressions or quality9']}
(p/'GATES.json').write_text(json.dumps(gates,indent=2)+'\n')
old=load(root/'research/bum07-p31/assets/glb-audit.json');b={'assetTotals':{'P3.1':{k:old[k]for k in ['triangles','primitives','bytes']},'P3.1R':{k:g[k]for k in ['triangles','primitives','bytes']}},'renderedFrames':budget,'note':'Primitives are potential draw units; measured drawCalls differ with culling and studio. No FPS/iPhone inference.'};(p/'BUDGET.json').write_text(json.dumps(b,indent=2)+'\n')
# Human-readable machine results, with failures/limits preserved.
lines=['# Kết quả kiểm chứng P3.1R', '', 'Blink100: **'+blink+'**. Tổng thể Facial Structure Repair: **chưa đạt** vì còn nếp gấp và self-contact chưa xử lý. Không phải duyệt9/10.', '', 'Đọc lại:122 mesh gốc và rig/action giữ nguyên. Source candidate SHA-256: `'+s['candidateSha256']+'`.', '', '## Va chạm và deformation', '', '| Blink | Tam giác da xuyên envelope hai mắt | Khoảng cách min | Self-overlap candidates |','| --- | ---: | ---: | ---: |']
for c in s['headSelfContact']:
 rows=[r for r in s['contact']if r['blink']==c['blink']];lines.append('| '+str(c['blink']*100)+'% | '+str(sum(r['skinTrianglesInsideOcularEnvelope']for r in rows))+' | '+str(round(min(r['minimumSkinTriangleDistance']for r in rows),6))+' | '+str(c['nonAdjacentTriangleOverlapPairs'])+' |')
lines+=['', 'Envelope radius0.090; distances scene units. Self-overlap là candidates chưa phân loại, không tự coi là contact hợp lệ. Finite/no-zero-area triangles không bảo đảm tạo hình tự nhiên.', '', '## GLB full-blink ID gate', '', '| Engine | Variant | Góc | Pixel mắt đỏ |','| --- | --- | ---: | ---: |']
for engine,r in reports.items():
 for v in r['eyeID']:
  if v['value']==1:lines.append('| '+engine+' | '+v['variant']+' | '+str(v['angle'])+' | '+str(v['redPixels'])+' |')
lines+=['', 'P3.1 là negative control phải lộ mắt; R yêu cầu0 pixel. Camera/studio khớp; ảnh ID unlit tách riêng beauty.', '', '## Ngân sách', '', '| Engine | Variant | Góc | Draw calls thực đo | Rendered triangles |','| --- | --- | ---: | ---: | ---: |']
for v in budget:lines.append('| '+v['engine']+' | '+v['variant']+' | '+str(v['angle'])+' | '+str(v['drawCalls'])+' | '+str(v['renderedTriangles'])+' |')
lines+=['', 'Tổng asset P3.1:225446 triangles/71 primitives; P3.1R:206034/59. Không đồng nhất primitives với measured draw calls. GLB R có corrective data lớn hơn; không suy ra FPS iPhone. Xem BUDGET.json cho bytes.', '', 'Smile0/50/100 và Blink đủ năm mức có ảnh0°/45°. Shader/decoder và finite geometry đạt kiểm tra hẹp; các nếp gấp, mouth contacts và tóc dạng cap vẫn cần xử lý/nghiệm thu. Không chuyển P3.2.']
(p/'CHECK-RESULTS.md').write_text('\n'.join(lines)+'\n')
assert all((p/'comparison'/name).exists()for name in ['neutral.png','blink-0.png','blink-45.png','smile-0.png','smile-45.png'])
entries=[{'path':f.relative_to(p).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)}for f in sorted(p.rglob('*'))if f.is_file()and f.name!='HANDOFF-MANIFEST.json'];(p/'HANDOFF-MANIFEST.json').write_text(json.dumps({'version':'P3.1R','blink100Gate':blink,'artApproved':False,'files':entries},indent=2)+'\n')
out=Path(sys.argv[1])if len(sys.argv)>1 else root/'artifacts/BUM07-P3.1R-Handoff.zip';out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for f in sorted(p.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(p).as_posix())
with zipfile.ZipFile(out)as z:assert z.testzip()is None
out.with_suffix('.zip.sha256').write_text(sha(out)+'  '+out.name+'\n');print(json.dumps({'packageResult':'PASS','blink100Gate':blink,'artApproved':False,'bytes':out.stat().st_size,'sha256':sha(out)}))
