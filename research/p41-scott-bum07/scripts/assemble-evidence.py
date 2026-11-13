"""Copy measured results, build same-camera contact sheets. Never retouch renders."""
import json,sys,shutil,hashlib,html
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
root=Path(__file__).resolve().parents[1];ev=root/'evidence'
for engine,source in zip(['webkit','chromium'],sys.argv[1:]):
 dst=ev/engine;shutil.copytree(Path(source),dst,dirs_exist_ok=True)
 r=json.loads((dst/'browser-report.json').read_text());assert not r['quick'] and len(r['shots'])==15 and len(r['expressions'])==16 and len(r['eyeID'])==10
 assert not r['errors'] and r['noSupabaseRequests'];assert r['sourceHashes']['P41']==json.loads((ev/'build-report.json').read_text())['exports']['scott-bum07-p41-prototype.glb']['sha256']
 for item in r['shots']+r['expressions']+r['eyeID']:assert hashlib.sha256((dst/item['file']).read_bytes()).hexdigest()==item['sha256']
com=root/'comparisons';com.mkdir(exist_ok=True);images=[]
for view in ['front','45','profile','close','body']:
 canvas=Image.new('RGB',(1500,460),'#182636');d=ImageDraw.Draw(canvas)
 for i,(variant,label)in enumerate([('scott-original','Original Scott / Mish7913 CC BY4.0'),('p31r','P3.1R / previous research'),('scott-bum07-p41','Scott-BUM07 P4.1 / NOT ACCEPTED')]):
  im=Image.open(ev/'webkit'/f'{variant}-{view}.png').convert('RGB');im.thumbnail((500,420));canvas.paste(im,(i*500+(500-im.width)//2,35));d.text((i*500+10,10),label,fill='white')
 canvas.save(com/f'{view}.jpg',quality=94);images.append((view,canvas.copy()))
# One unretouched sheet per expression with every measured level and angle.
for mode,levels in [('blink',[0,25,50,75,100]),('smile',[0,50,100])]:
 canvas=Image.new('RGB',(340*len(levels),560),'#182636');d=ImageDraw.Draw(canvas)
 for y,angle in enumerate([0,45]):
  for x,level in enumerate(levels):
   im=Image.open(ev/'webkit'/f'p41-{mode}-{level}-{angle}.png').convert('RGB');im.thumbnail((340,250));canvas.paste(im,(x*340+(340-im.width)//2,y*280+25));d.text((x*340+10,y*280+6),f'{mode} {level}% / {angle}deg',fill='white')
 canvas.save(com/f'{mode}-levels.jpg',quality=94);images.append((mode,canvas.copy()))
images[0][1].save(root/'BUM07-P41-Render-Review.pdf',save_all=True,append_images=[im for _,im in images[1:]],resolution=110)
parts=['<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Scott BUM07 P4.1 — NOT ACCEPTED</title><style>body{font:17px system-ui;background:#142236;color:#fff;margin:24px}img{width:100%;height:auto}a{color:#a7d8ff}section{margin:35px 0}</style><h1>Scott BUM07 P4.1 — nghiên cứu, chưa nghiệm thu</h1><p>Scott của Mish7913 · CC BY 4.0 · có chỉnh sửa. Blink100 FAIL; số07/cổ áo/iris còn lỗi. Không thay nhân vật game. Ảnh WebKit Linux, không phải iPhone.</p><p><a href="REPORT.md">Technical report</a> · <a href="ATTRIBUTION.md">Attribution</a> · <a href="BUM07-P41-Render-Review.pdf">Render PDF</a></p>']
for view,_ in images:parts.append(f'<section><h2>{html.escape(view)}</h2><a href="comparisons/{view}.jpg"><img src="comparisons/{view}.jpg" alt="{view} actual GLB comparison"></a></section>')
parts.append('</html>');(root/'gallery.html').write_text('\n'.join(parts))
print('EVIDENCE_ASSEMBLED')
