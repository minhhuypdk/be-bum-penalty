"""Actual WebKit beauty renders, native pixels, labels outside render. No retouch."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]/'research/bum07-p31r';src=root/'renders/webkit';out=root/'comparison';out.mkdir(exist_ok=True);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
def sheet(name,rows):
 ims=[[Image.open(src/(v+'-'+suffix+'.png')).convert('RGB')for v in ['p31','p31r']]for suffix,label in rows];w,h=ims[0][0].size;assert all(im.size==(w,h)for row in ims for im in row)
 d=Image.new('RGB',(w*2,(h+65)*len(rows)),(16,29,46));draw=ImageDraw.Draw(d)
 for j,((suffix,label),row)in enumerate(zip(rows,ims)):
  for i,(v,im)in enumerate(zip(['P3.1 - NOT APPROVED','P3.1R - OWNER REVIEW PENDING'],row)):d.paste(im,(i*w,j*(h+65)+65));draw.text((i*w+14,j*(h+65)+18),label+' | '+v,font=font,fill=(245,205,101))
 d.save(out/(name+'.png'))
sheet('neutral',[('neutral-'+str(a),'Neutral '+str(a)+' deg')for a in [0,45,90]])
for a in [0,45]:
 sheet('blink-'+str(a),[('blink-'+str(v)+'-'+str(a),'Blink '+str(v)+'% / '+str(a)+' deg')for v in [0,25,50,75,100]])
 sheet('smile-'+str(a),[('smile-'+str(v)+'-'+str(a),'Smile '+str(v)+'% / '+str(a)+' deg')for v in [0,50,100]])
sections=''.join('<section><h2>'+label+'</h2><a href="comparison/'+name+'.png"><img src="comparison/'+name+'.png" loading="lazy" alt="'+label+'"></a></section>'for name,label in [('neutral','Tóc/mặt: 0°, 45°, 90°'),('blink-0','Blink 0/25/50/75/100% · chính diện'),('blink-45','Blink 0/25/50/75/100% · 45°'),('smile-0','Smile 0/50/100% · chính diện'),('smile-45','Smile 0/50/100% · 45°')])
(root/'index.html').write_text('''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BUM07 P3.1R — Facial Structure Repair</title><style>body{margin:0;background:#101d2e;color:#e7edf5;font:16px/1.6 system-ui}main{max-width:1500px;padding:24px;margin:auto}a{color:#f5cd65}img{width:100%;height:auto}aside{border-left:4px solid #f5cd65;padding:14px}section{margin:32px 0}</style><main><h1>BUM07 · P3.1 / P3.1R</h1><aside>P3.1R chưa đạt tổng thể: còn nếp gấp vùng mí. Chờ chủ dự án nghiệm thu; không tự chấm9/10. Cổng che mắt không thay cổng mỹ thuật hoặc rig production. Xem GATES/contact report: các self-contact và head–lip overlap vẫn mở. Không chuyển P3.2.</aside><p><a href="assets/bum07-p31r-workbench.blend">Blender</a> · <a href="assets/bum07-p31r-experimental.glb">GLB</a> · <a href="TECHNICAL-REPORT.md">Báo cáo</a> · <a href="GATES.json">Gates</a> · <a href="BUDGET.json">Ngân sách</a></p>'''+sections+'''<p>Ảnh thật từ GLB dưới studio/camera cố định. PNG ghép giữ nguyên pixel từng ảnh; mở ảnh để zoom. ID diagnostic ở renders/webkit, không dùng làm beauty render hoặc hiệu năng iPhone.</p></main></html>''')
print('P31R_FIVE_NATIVE_COMPARISON_SHEETS')
