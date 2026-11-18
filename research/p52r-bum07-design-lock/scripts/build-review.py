from pathlib import Path
import json,base64
r=Path(__file__).resolve().parents[1];b='../p52-bum07-design-spec/'
head='''<!doctype html><html lang="vi"><meta charset="utf-8"><title>BUM07 P5.2R</title><style>@page{size:A4 landscape;margin:10mm}body{font:11pt 'DejaVu Sans',sans-serif;color:#182b45}section{break-after:page}h1{font-size:25pt}h2{font-size:17pt;margin:0 0 3mm}p{margin:2mm 0}.pair{display:flex;justify-content:center;gap:8mm;height:145mm}figure{margin:0;text-align:center}img{height:138mm;max-width:250mm;object-fit:contain}figcaption{font-size:9pt}.notice{background:#fff1b8;padding:5mm}html[data-book=turnaround] .expressions{display:none}html[data-book=expressions] .turnaround{display:none}</style><script>document.documentElement.dataset.book=new URLSearchParams(location.search).get('book')||'all'</script><body>'''
p=[]
def page(book,body):p.append(f'<section class="{book}">{body}</section>')
def pair(book,title,files,note):
 page(book,f'<h2>{title}</h2><p>{note}</p><div class="pair">'+''.join(f'<figure><img src="{f}"><figcaption>{label}</figcaption></figure>' for f,label in files)+'</div>')
for book,title in [('turnaround','Turnaround / design lock'),('expressions','Expression sheet / design lock')]:
 page(book,f'<h1>BUM07 · P5.2R<br>{title}</h1><p>B — Gió Sân Cỏ / Field Breeze. Baseline 8529f6b. Nhánh research/p52r-bum07-design-lock.</p><p class="notice">CHỜ CHỦ DỰ ÁN NGHIỆM THU. Chưa cho phép dựng Blender.<br>Ảnh AI concept, không phải render Blender; không chứng minh camera orthographic 3D hoặc cùng mesh. Không công bố 9/10.</p><h2>Phạm vi khóa đề xuất</h2><p>Ngôi trái giải phẫu, mái quét thấp, gáy ngắn mềm. Mặt oval trẻ em; tai sát đầu, mũi/cằm mềm. Cổ V trước, cổ bo navy sau, số 07 và đường vai nhất quán về ý đồ thiết kế.</p><p>Giữ nguyên bảng 5H, mốc đo và màu P5.2. H = sọ–cằm không tính tóc; tóc tối đa 5,2H là đề xuất, không phải số đo từ mesh.</p><p>Focused bình tĩnh, tự tin; Celebration mở mắt hơn. Một mẫu cung răng trên, không khe răng chủ ý. Ảnh AI vẫn có sai khác độ rộng răng, crop và hướng tóc; xem báo cáo FAIL/NOT_VERIFIED.</p><p>PNG gốc 1024×1536. Không sửa game, main, Pages, Supabase, PR #2 hoặc các bản lịch sử.</p>')
angles=[('01-front-000','Chính diện 0°'),('02-three-quarter-045','Góc 45°'),('03-profile-090','Nghiêng 90°'),('04-back-180','Sau lưng 180°'),('05-a-pose-000','Toàn thân A-pose'),('06-neutral-face-000','Cận mặt neutral')]
for name,title in angles:pair('turnaround',title,[(b+'turnaround/'+name+'.png','P5.2'),('turnaround/'+name+'.png','P5.2R')],'Trước / sau. Nhãn góc là ý đồ minh họa 2D, không phải camera 3D đã đo.')
for file,title in [('turnaround-measurement-layout.svg','Mốc 5H giữ nguyên — đường đo đề xuất'),('face-construction-guide.svg','Cấu trúc khuôn mặt đề xuất'),('material-palette.svg','Bảng màu / vật liệu giữ nguyên')]:pair('turnaround',title,[('specification/'+file,'Chưa xác minh bằng mesh')],'Các con số là thông số thiết kế đề xuất; ảnh không bảo đảm khớp tuyệt đối với lưới.')
states=[('01-neutral','Neutral'),('02-happy','Happy'),('03-big-smile','Big Smile'),('04-blink-100','Blink 100%'),('05-focused','Focused'),('06-surprised','Surprised'),('07-disappointed','Disappointed'),('08-celebration','Celebration')]
for n,title in states:pair('expressions',title,[('expressions/'+n+'-000.png','0°'),('expressions/'+n+'-045.png','45°')],'Cùng định hướng B; hình minh họa không chứng minh deformation hoặc occlusion 3D.')
for n,title in [('05-focused','Focused'),('08-celebration','Celebration'),('03-big-smile','Big Smile')]:
 for angle in ['000','045']:pair('expressions',title+' '+angle+' · P5.2 / P5.2R',[(b+'expressions/'+n+'-'+angle+'.png','P5.2'),('expressions/'+n+'-'+angle+'.png','P5.2R')],'So sánh trực tiếp; crop/đường nét có trôi nhẹ giữa ảnh AI, không khẳng định camera giống nhau chính xác.')
pair('expressions','Một cung răng trên — chuẩn 2D đề xuất',[('specification/upper-dental-arch.svg','Chưa có mesh răng')],'Big Smile/Celebration phải dùng cùng mẫu. Ảnh AI hiện chưa khớp tuyệt đối: giữ FAIL cho khóa hình học răng.')
doc=head+'\n'.join(p)+'</body></html>'
for old in (r.parent/'p52-bum07-design-spec').glob('*/*.png'):
 token=b+str(old.relative_to(r.parent/'p52-bum07-design-spec'))
 if token in doc:doc=doc.replace(token,'data:image/png;base64,'+base64.b64encode(old.read_bytes()).decode())
(r/'review.html').write_text(doc);print('SECTIONS',len(p))
