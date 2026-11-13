"""Package documentation and an EXISTING P2 workbench. No bpy, mesh build or model write.
prepare -> render PDF with browser -> finalize. All source assets must remain byte-identical.
"""
import argparse,csv,hashlib,html,json,math,pathlib,re,shutil,zipfile,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1];DOC=ROOT/'docs/artist-production/BUM07'
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(pathlib.Path(p).read_text())
def inline(s):
 s=html.escape(s);s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s);s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s);return s

def markdown(text):
 lines=text.splitlines();out=[];para=[];i=0
 def flush():
  if para:out.append('<p>'+inline(' '.join(para))+'</p>');para.clear()
 while i<len(lines):
  line=lines[i].strip()
  if not line:flush();i+=1;continue
  if line.startswith('|'):
   flush();rows=[]
   while i<len(lines)and lines[i].strip().startswith('|'):
    cells=[c.strip()for c in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r'[: -]+',c)for c in cells):rows.append(cells)
    i+=1
   out.append('<table>'+''.join('<tr>'+''.join(('<th>'if j==0 else '<td>')+inline(c)+('</th>'if j==0 else '</td>')for c in row)+'</tr>'for j,row in enumerate(rows))+'</table>');continue
  if line.startswith('#'):
   flush();n=min(4,len(line)-len(line.lstrip('#')));out.append('<h'+str(n)+'>'+inline(line[n:].strip())+'</h'+str(n)+'>')
  elif line.startswith('- '):flush();out.append('<p class="item">• '+inline(line[2:])+'</p>')
  elif re.match(r'^\d+\. ',line):flush();out.append('<p class="step">'+inline(line)+'</p>')
  else:para.append(line)
  i+=1
 flush();return '\n'.join(out)

def check_spec(s):
 t=s['targets'];assert s['changes_geometry'] is False
 assert abs(2*t['eye_center_abs_x_H']-t['eye_inner_gap_H']-t['eye_opening_width_H'])<1e-9
 assert t['eye_center_abs_x_H']+t['eye_opening_width_H']/2<t['head_width_H']/2
 assert 0<t['pupil_diameter_H']<t['iris_diameter_H']<t['eye_opening_height_H']<t['eye_opening_width_H']<t['head_width_H']
 assert t['mouth_seam_height_H']<t['nose_base_height_H']<t['nose_tip_height_H']<t['eye_center_height_H']<t['brow_baseline_height_H']<t['fringe_lowest_height_H']<1
 assert t['fringe_lowest_height_H']<t['fringe_highest_tip_height_H']<t['hair_front_root_height_H']<1
 assert t['hair_primary_masses']==3 and t['hair_secondary_masses']==5

def svg(spec,side=False):
 t=spec['targets'];H=420;C=300;B=650
 X=lambda v:C+v*H;Y=lambda v:B-v*H
 headW=t['head_width_H'];cx=0.0
 tags=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="750" viewBox="0 0 900 750"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto-start-reverse"><path d="M0 0L6 3L0 6" fill="#62748a"/></marker></defs><rect width="900" height="750" fill="#fcfcfa"/><g font-family="DejaVu Sans,sans-serif" fill="#263b50">']
 def text(x,y,s,size=14):tags.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}">{html.escape(s)}</text>')
 def line(x1,y1,x2,y2,color='#b9c3ce',dash=''):
  tags.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-dasharray="{dash}"/>')
 text(28,35,'BUM 07 · '+('PROFILE'if side else'FRONT')+' · MASTER PROPOSAL',23)
 text(28,61,'Sơ đồ tỷ lệ 2D — không phải render, concept art hoặc thiết kế đã duyệt',14)
 for j in range(11):line(70,Y(j/10),540,Y(j/10),'#e6e8ea');text(42,Y(j/10)+4,f'{j/10:.1f}',10)
 if not side:
  w=headW*H/2
  tags.append(f'<path d="M {C} {Y(1)} C {C+w*.87} {Y(1.01)} {C+w} {Y(.82)} {C+w} {Y(.56)} C {C+w} {Y(.34)} {C+w*.73} {Y(.09)} {C} {Y(0)} C {C-w*.73} {Y(.09)} {C-w} {Y(.34)} {C-w} {Y(.56)} C {C-w} {Y(.82)} {C-w*.87} {Y(1.01)} {C} {Y(1)}Z" fill="#f3e9df" stroke="#836f61" stroke-width="2"/>')
  line(C,Y(1.10),C,Y(0),'#aebcca','5 5')
  for sign in [-1,1]:
   ex=X(sign*t['eye_center_abs_x_H']);ey=Y(t['eye_center_height_H'])
   tags.append(f'<ellipse cx="{ex}" cy="{ey}" rx="{H*t["eye_opening_width_H"]/2}" ry="{H*t["eye_opening_height_H"]/2}" fill="white" stroke="#816c61" stroke-width="2"/><circle cx="{ex}" cy="{ey}" r="{H*t["iris_diameter_H"]/2}" fill="#a28a6a"/><circle cx="{ex}" cy="{ey}" r="{H*t["pupil_diameter_H"]/2}" fill="#3d3630"/>')
   bx=H*t['brow_width_H']/2;by=Y(t['brow_baseline_height_H']);peak=Y(t['brow_arch_peak_height_H'])
   tags.append(f'<path d="M{ex-bx} {by}Q{ex} {peak-8} {ex+bx} {by}" fill="none" stroke="#5c4b41" stroke-width="{H*t["brow_max_thickness_H"]}"/>')
   text(X(sign*t['cheek_center_abs_x_H'])-5,Y(t['cheek_center_height_H'])+5,'+',18)
  nw=t['nose_alar_width_H']*H/2
  tags.append(f'<path d="M{C} {Y(t["nose_root_height_H"])}Q{C-6} {Y(t["nose_tip_height_H"])} {C-nw} {Y(t["nose_base_height_H"])}Q{C} {Y(t["nose_base_height_H"])-7} {C+nw} {Y(t["nose_base_height_H"])}" fill="none" stroke="#9a8070" stroke-width="2"/>')
  mw=t['mouth_width_neutral_H']*H/2;my=Y(t['mouth_seam_height_H']);raise_=H*t['mouth_corner_neutral_raise_H']
  tags.append(f'<path d="M{C-mw} {my-raise_}Q{C} {my+raise_} {C+mw} {my-raise_}" fill="none" stroke="#9d7668" stroke-width="3"/>')
  hp=X(t['hair_part_abs_x_H']);hy=Y(t['hair_front_root_height_H'])
  for k in range(3):
   end=X(-.27+k*.16);endY=Y(t['fringe_lowest_height_H']+.025*k)
   tags.append(f'<path d="M{hp-k*21} {hy-35}Q{C+20-k*28} {Y(1.08)} {end} {endY}" fill="none" stroke="{["#7c98aa","#a5b7c5","#bdc9d1"][k]}" stroke-width="21" opacity=".65"/>')
  text(560,210,'Tỷ lệ đề xuất duy nhất',19)
  rows=[('Rộng sọ',t['head_width_H']),('Tâm mắt cao',t['eye_center_height_H']),('Rộng khe mắt',t['eye_opening_width_H']),('Cao khe mắt',t['eye_opening_height_H']),('Khoảng khóe trong',t['eye_inner_gap_H']),('Iris / pupil',f'{t["iris_diameter_H"]} / {t["pupil_diameter_H"]}'),('Đầu mũi cao',t['nose_tip_height_H']),('Đường môi cao',t['mouth_seam_height_H']),('Rộng môi neutral',t['mouth_width_neutral_H']),('Mái thấp nhất',t['fringe_lowest_height_H']),('Tóc thêm trên đỉnh',t['hair_crown_extension_H'])]
  for i,(a,b)in enumerate(rows):text(560,245+i*30,f'{a}: {b}H')
  text(560,600,'Ngôi +X → mái quét -X',14);text(560,623,'3 khối chính + 5 khối phụ',14)
  text(90,700,'+X = trái nhân vật / phải người xem; má là landmark (+), không phải khối cầu',12)
 else:
  F=520;depth=t['skull_depth_H']*H;left=F-depth
  tags.append(f'<path d="M{F-depth/2} {Y(1)}C{left-10} {Y(1)} {left-10} {Y(.44)} {left+45} {Y(.18)}Q{left+95} {Y(0)} {F-55} {Y(0)}Q{F} {Y(.18)} {F} {Y(t["mouth_seam_height_H"])}L{F+t["nose_projection_max_H"]*H} {Y(t["nose_tip_height_H"])}L{F} {Y(t["nose_root_height_H"])}Q{F+5} {Y(.91)} {F-depth/2} {Y(1)}Z" fill="#f3e9df" stroke="#836f61" stroke-width="2"/>')
  line(F,Y(1.07),F,Y(.2),'#a3b0bb','6 5')
  ey=Y(t['eye_center_height_H']);radius=t['hidden_globe_diameter_H']*H/2;ec=F-radius+.02*H
  tags.append(f'<circle cx="{ec}" cy="{ey}" r="{radius}" fill="none" stroke="#547d85" stroke-dasharray="5 4" stroke-width="2"/>')
  text(560,230,'Sọ sâu: '+str(t['skull_depth_H'])+'H',17)
  text(560,280,'Globe ẩn: Ø '+str(t['hidden_globe_diameter_H'])+'H')
  text(560,320,'Apex ≤ '+str(t['cornea_apex_max_ahead_of_orbital_rim_plane_H'])+'H trước rim')
  text(560,360,'Mũi projection ≤ '+str(t['nose_projection_max_H'])+'H')
  text(560,400,'Rim plane được artist xác định')
  text(560,440,'Không đẩy globe ra để làm mắt to')
  tags.append(f'<path d="M{left+30} {Y(.30)}Q{left-35} {Y(1.12)} {F-depth/2} {Y(1.08)}Q{F} {Y(1.06)} {F+10} {Y(.76)}" fill="none" stroke="#7c98aa" stroke-width="15" opacity=".6"/>')
  text(92,700,'Profile schematic: khối lớn/landmark, không phải contour mặt đã được duyệt',12)
 text(28,735,'H = cằm → đỉnh sọ (không tóc/tai). Không áp dụng sơ đồ bằng auto-deform mesh.',12)
 tags.append('</g></svg>');return ''.join(tags)

def prepare(src,out):
 s=load(DOC/'design-spec.json');check_spec(s);assert out!=src and src not in out.parents
 work=src/'artist/bum07-facehair-workbench.blend';expected=s['reference_artifact']['workbench_sha256'];assert sha(work)==expected
 original=load(src/'artist/manifest.json');assert original['workbenchSha256']==expected
 read=load(DOC/'source-read-only-inspection.json');assert read['source_sha256']==expected and read['resaved'] is False
 for f in ['SOURCE','DOCS','REFERENCES','DESIGN']:(out/f).mkdir(parents=True,exist_ok=True)
 shutil.copy2(work,out/'SOURCE'/work.name)
 for p in DOC.iterdir():
  if p.is_file() and p.suffix.lower() != ".pdf":shutil.copy2(p,out/'DOCS'/p.name)
 for name in ['manifest.json','source-audit.json','glb-audit.json']:
  shutil.copy2(src/'artist'/name,out/'SOURCE'/('P2-'+name))
 refs=['c-front.png','c-45.png','c-profile.png','c-close.png','p2-front.png','p2-45.png','p2-profile.png','p2-close.png','p2-neutral.png','p2-smile.png','p2-blink.png','comparison.json']
 comparison=load(src/'comparison.json')
 for shot in comparison['shots']:assert sha(src/shot['file'])==shot['sha256']
 for name in refs:shutil.copy2(src/name,out/'REFERENCES'/name)
 frozen=DOC/'frozen-C-reference'
 if frozen.exists():
  for f in frozen.glob('*.png'):
   assert sha(f)==original['packedCImages'][f.name]
   target=out/'REFERENCES/frozen-C'/f.name;target.parent.mkdir(exist_ok=True);shutil.copy2(f,target)
 for name,side in [('front',False),('profile',True)]:
  data=svg(s,side);ET.fromstring(data);(out/'DESIGN'/('master-'+name+'.svg')).write_text(data)
 (out/'SOURCE'/'SOURCE-SHA256.txt').write_text(expected+'  '+work.name+'\n')
 labels={'head_width_H':'Rộng sọ, không tai','skull_depth_H':'Sâu sọ, không nose projection','eye_center_height_H':'Tâm mắt: cao độ','eye_opening_width_H':'Khe mắt: rộng','eye_opening_height_H':'Khe mắt: cao','eye_inner_gap_H':'Khoảng hai khóe trong','eye_center_abs_x_H':'Tâm mỗi mắt: |x|','iris_diameter_H':'Đường kính iris','pupil_diameter_H':'Đường kính pupil','hidden_globe_diameter_H':'Globe ẩn: đường kính','cornea_apex_max_ahead_of_orbital_rim_plane_H':'Globe: apex tối đa trước rim plane','brow_arch_peak_height_H':'Brow: cao độ peak','brow_width_H':'Brow: bề ngang','brow_max_thickness_H':'Brow: độ dày tối đa','brow_baseline_height_H':'Brow: cao độ baseline','nose_root_height_H':'Nose root: cao độ','nose_base_height_H':'Nose base: cao độ','nose_tip_height_H':'Đầu mũi: cao độ','nose_alar_width_H':'Mũi: bề ngang alar','nose_projection_max_H':'Mũi: projection tối đa','mouth_seam_height_H':'Đường môi: cao độ','mouth_width_neutral_H':'Môi: bề ngang neutral','mouth_total_lip_height_H':'Môi: tổng cao vermillion','cheek_center_abs_x_H':'Má: tâm |x|','cheek_center_height_H':'Má: tâm cao độ','hair_crown_extension_H':'Tóc: thêm trên crown','hair_front_root_height_H':'Tóc: cao độ root trước','fringe_lowest_height_H':'Tóc: tip thấp nhất','fringe_highest_tip_height_H':'Tóc: tip cao nhất'}
 table='<table><tr><th>Landmark / kích thước</th><th>Mục tiêu đề xuất</th></tr>'+''.join('<tr><td>'+v+'</td><td>'+str(s['targets'][k])+'H</td></tr>'for k,v in labels.items())+'</table>'
 intro='<section class="cover"><span class="eyebrow">BÉ BUM PENALTY 3D · HỒ SƠ ARTIST v1.0</span><h1>BUM TIỀN ĐẠO 07</h1><h2>Character Art Production Dossier</h2><p class="notice">P2 CHƯA NGHIỆM THU · HỒ SƠ THIẾT KẾ ĐỀ XUẤT<br>Không tạo P3/P4, không chỉnh mesh tự động, không xác nhận 9/10.</p><p>Gói sử dụng đúng workbench P2 đã bàn giao, nguyên byte. Chỉ mặt/tóc; body/trang phục/animation và ba nhân vật khác ngoài phạm vi.</p><p>Source SHA-256:</p><code>'+expected+'</code><p>Mở SOURCE/bum07-facehair-workbench.blend; xem DOCS, DESIGN và REFERENCES. Bảng tỷ lệ là một đề xuất thống nhất, chờ artist/chủ dự án duyệt direction, không phải form đã được phê duyệt.</p><p>File thật đã mở đọc bằng Blender '+read['blender_version']+', không resave. H sọ hiện tại ≈ '+str(round(read['head_H_scene_units'],6))+' scene units; rộng sọ/H hiện tại ≈ '+str(round(read['head_width_over_H'],4))+'. Đây là số đo P2, không phải mục tiêu đã thực hiện.</p></section>'
 diagrams='<section class="newpage"><h1>Master proportion proposal</h1><p>H = cằm tới đỉnh sọ; không gồm tóc/tai. Không đặt lại tỷ lệ toàn thân. Sơ đồ dưới đây là 2D đo lường, không phải ảnh render hoặc thiết kế final.</p><img class="diagram" src="DESIGN/master-front.svg"><img class="diagram" src="DESIGN/master-profile.svg">'+table+'<p>Dung sai đề xuất: rộng sọ ±0,02H; sâu sọ ±0,03H; feature position ±0,015H. Tóc rộng tối đa 1,06×rộng sọ, ngôi +0,20H phía trái nhân vật và quét sang phải. 3 khối chính + 5 phụ. Các giá trị đầy đủ ở design-spec.json; artist không tự đổi mục tiêu mà không ghi thay đổi/duyệt.</p></section>'
 backlog=list(csv.DictReader((DOC/'issue-backlog.csv').open(encoding='utf-8-sig')))
 bt='<section class="newpage"><h1>Danh sách lỗi và thứ tự xử lý</h1><table><tr><th>ID/Priority</th><th>Lỗi / reference</th><th>Đầu ra để đóng</th></tr>'+''.join('<tr><td>'+r['ID']+'<br>'+r['Priority']+'</td><td>'+html.escape(r['Observed_problem'])+'<br><small>'+html.escape(r['Reference'])+'</small></td><td>'+html.escape(r['Close_condition'])+'</td></tr>'for r in backlog)+'</table><p>Tất cả lỗi art vẫn OPEN hoặc DEFERRED. Technical validation của gói không tự đóng lỗi.</p></section>'
 content='<section class="newpage">'+markdown((DOC/'README.md').read_text())+'</section><section class="newpage">'+markdown((DOC/'SCOPE-AND-RESPONSIBILITY.md').read_text())+'</section>'
 checks=list(csv.DictReader((DOC/'acceptance-checklist.csv').open(encoding='utf-8-sig')))
 ct='<section class="newpage"><h1>Phiếu nghiệm thu — chưa có mục nào được duyệt</h1><table><tr><th>ID / gate</th><th>Tiêu chí</th><th>Người duyệt / trạng thái</th></tr>'+''.join('<tr><td>'+r['ID']+' / '+r['Gate']+'</td><td>'+html.escape(r['Criterion'])+'</td><td>'+html.escape(r['Reviewer'])+'<br>OPEN</td></tr>'for r in checks)+'</table><p>Ghi Evidence và Decision trong CSV, chủ dự án ký quyết định mỹ thuật riêng. Điểm 9/10 không được sinh tự động.</p></section>'
 photos='<section class="newpage"><h1>Ảnh reference P2 hiện có — không chỉnh sửa</h1><p>Ảnh dưới ghi nhận nguồn chưa đạt. Không phải ảnh minh họa cho master đề xuất.</p>'+''.join('<div class="photo-pair"><figure><img src="REFERENCES/c-'+i+'.png"><figcaption>C '+i+'</figcaption></figure><figure><img src="REFERENCES/p2-'+i+'.png"><figcaption>P2 '+i+' · chưa duyệt</figcaption></figure></div>'for i in ['front','45','profile','close'])+'</section>'
 css='''@page{size:A4;margin:15mm 14mm 18mm}*{box-sizing:border-box}body{font:10pt/1.55 "DejaVu Sans",Arial,sans-serif;color:#203247;margin:0;background:#fff}main{max-width:980px;margin:auto;padding:28px}h1{font-size:24pt;color:#163650;line-height:1.2;margin:18px 0}h2{font-size:15pt;color:#234d68;margin:22px 0 10px}h3{font-size:12pt}p{margin:9px 0}code{font:8pt/1.4 monospace;overflow-wrap:anywhere;word-break:break-word}.eyebrow{font-size:10pt;letter-spacing:2px;color:#836414}.notice{border-left:4px solid #c6952c;background:#fbf6e7;padding:12px;font-weight:bold}.cover{min-height:230mm}.newpage{break-before:page}table{border-collapse:collapse;width:100%;margin:14px 0;font-size:8.4pt;table-layout:fixed}th,td{border:1px solid #cfd8df;padding:6px 7px;vertical-align:top;overflow-wrap:anywhere}th{background:#eaf0f5;text-align:left}thead{display:table-header-group}tr{break-inside:avoid}h1,h2,h3{break-after:avoid}.diagram{display:block;width:100%;max-height:235mm;object-fit:contain;break-inside:avoid}.photo-pair{display:flex;gap:8px;break-inside:avoid;margin:12px 0}figure{margin:0;width:50%}figure img{width:100%;height:auto}figcaption{font-size:9pt}.item,.step{padding-left:8px}small{font-size:7.5pt}@media print{main{padding:0;max-width:none}body{print-color-adjust:exact;-webkit-print-color-adjust:exact}}'''
 page='<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>BUM 07 Artist Production Dossier v1.0</title><style>'+css+'</style></head><body><main>'+intro+diagrams+bt+content+ct+photos+'</main></body></html>'
 (out/'production-brief.html').write_text(page)
 (out/'OPEN-FIRST.txt').write_text('BUM 07 ARTIST DOSSIER v1.0\nP2 UNAPPROVED. No new mesh/model generated.\nRead PRODUCTION-BRIEF.pdf or production-brief.html.\nEditable original: SOURCE/bum07-facehair-workbench.blend\nMaster proposal: DOCS/design-spec.json\nChecklists: DOCS/*.csv\nDo not overwrite SOURCE. No body/animation or other characters before owner approval.\n')
 assert sha(work)==expected and sha(out/'SOURCE'/work.name)==expected
 print('PREPARED_DOSSIER',out)

def finalize(src,out,zpath):
 s=load(DOC/'design-spec.json');check_spec(s);expected=s['reference_artifact']['workbench_sha256'];work=out/'SOURCE/bum07-facehair-workbench.blend'
 assert sha(work)==expected and sha(src/'artist/bum07-facehair-workbench.blend')==expected
 pdf=out/'PRODUCTION-BRIEF.pdf';assert pdf.read_bytes().startswith(b'%PDF-') and pdf.stat().st_size>10000
 checks=list(csv.DictReader((out/'DOCS/acceptance-checklist.csv').open(encoding='utf-8-sig')));assert all(r['Status']=='OPEN'for r in checks)
 for f in ['DESIGN/master-front.svg','DESIGN/master-profile.svg']:ET.parse(out/f)
 for path in out.rglob('*'):
  if path.suffix.lower()=='.html':
   for href in re.findall(r'(?:src|href)="([^"]+)"',path.read_text()):
    if not re.match(r'^(https?:|#)',href):assert (path.parent/href).exists(),href
 validation={'result':'PASS','documents_complete':True,'source_model_version':'P2_UNAPPROVED','source_workbench_sha256':expected,'source_file_unchanged':True,'geometry_created':False,'generator_invoked':False,'master_proposal_numeric_consistency':True,'master_proposal_approved':False,'art_approved':False,'quality_9_verified':False,'all_art_checklist_statuses':'OPEN','pdf_header_valid':True,'physical_iPhone_tested':False,'changes_to_game_or_supabase':False}
 (out/'VALIDATION.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
 entries=[]
 for p in sorted(out.rglob('*')):
  if p.is_file()and p.name!='MANIFEST.json':entries.append({'path':p.relative_to(out).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
 manifest={'document_version':'1.0','model_version':'P2_UNCHANGED_UNAPPROVED','source_artifact':s['reference_artifact'],'file_count':len(entries),'files':entries};(out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 zpath.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(out).as_posix())
 with zipfile.ZipFile(zpath)as z:assert z.testzip() is None;assert 'SOURCE/bum07-facehair-workbench.blend' in z.namelist()
 zpath.with_suffix(zpath.suffix+'.sha256').write_text(sha(zpath)+'  '+zpath.name+'\n')
 print(json.dumps({'result':'PASS','zip':str(zpath),'bytes':zpath.stat().st_size,'sha256':sha(zpath),'files':len(entries)+1,'workbench_sha256':expected,'geometry_created':False}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','finalize']);p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--zip',type=pathlib.Path);a=p.parse_args();source=a.source.resolve();out=a.output.resolve()
 if a.command=='prepare':prepare(source,out)
 else:assert a.zip;finalize(source,out,a.zip.resolve())
