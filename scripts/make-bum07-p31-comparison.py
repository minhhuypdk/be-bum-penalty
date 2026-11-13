"""Assemble actual PNG renders without retouch/crop/rescale; labels outside render."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import html,json
root=Path(__file__).resolve().parents[1]/'research/bum07-p31';out=root/'comparison';out.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
for sid in ['front','45','profile','close']:
 ims=[Image.open(root/'renders/chromium'/(v+'-'+sid+'.png')).convert('RGB')for v in ['c','p2','p31']];assert len({im.size for im in ims})==1
 w,h=ims[0].size;dest=Image.new('RGB',(w*3,h+60),(16,29,46));d=ImageDraw.Draw(dest)
 for i,(im,label)in enumerate(zip(ims,['C - baseline unchanged','P2 - original GLB unchanged','P3.1 - unapproved / art gate FAIL'])):dest.paste(im,(i*w,60));d.text((i*w+18,15),label,font=font,fill=(245,205,101))
 dest.save(out/(sid+'.png'))
rows=''.join('<section><h2>'+sid+'</h2><div class="row">'+''.join('<figure><a href="renders/chromium/'+v+'-'+sid+'.png"><img src="renders/chromium/'+v+'-'+sid+'.png"></a><figcaption>'+label+'</figcaption></figure>'for v,label in [('c','C'),('p2','P2'),('p31','P3.1 · chưa nghiệm thu')])+'</div></section>'for sid in ['front','45','profile','close'])
page='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BUM 07 P3.1 — C/P2/P3.1</title><style>body{background:#101d2e;color:#e7edf5;font:16px/1.6 system-ui;margin:0}main{max-width:1600px;margin:auto;padding:24px}a{color:#f5cd65}aside{border-left:4px solid #f5cd65;padding:12px}.row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}figure{margin:0}img{width:100%;height:auto}figcaption{padding:8px} @media(max-width:700px){.row{grid-template-columns:1fr}}</style><main><h1>BUM 07 · C / P2 / P3.1</h1><aside>FAIL_ART_TARGET · chưa nghiệm thu, không xác nhận 9/10. Có cải thiện cục bộ; mí/tóc/biểu cảm vẫn chưa đạt. Blink 100% còn xuyên iris/sclera. Không chuyển P3.2. Ảnh thật từ GLB, cùng studio/camera trong Chromium Linux; không phải ảnh concept hoặc hiệu năng iPhone.</aside><p><a href="README.md">Hướng dẫn</a> · <a href="TECHNICAL-REPORT.md">Báo cáo kỹ thuật</a> · <a href="assets/bum07-p31-workbench.blend">Blender</a> · <a href="assets/bum07-p31-experimental.glb">GLB</a> · <a href="renders/webkit/browser-report.json">WebKit report</a></p>'''+rows+'''<h2>Lỗi deformation được giữ để kiểm tra</h2><p><a href="renders/webkit/p31-blink-1.png">Ảnh Blink 100% — FAIL</a>. PASS của browser chỉ xác nhận import/render và luồng kiểm thử; không phải nghiệm thu mỹ thuật.</p></main></html>'''
(root/'index.html').write_text(page)
print('FOUR_ACTUAL_RENDER_TRIPTYCHS_WRITTEN_NO_RESCALE')
