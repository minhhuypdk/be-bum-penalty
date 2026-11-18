"""Assemble verified final evidence and unretouched render contact sheets."""
from pathlib import Path
import json,sys,shutil,hashlib,html
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];ev=root/'evidence';ev.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
asset=root/'assets/scott-bum07-p41r-prototype.glb';reports={}
for engine,folder in zip(['webkit','chromium'],sys.argv[1:3]):
 dst=ev/engine;shutil.copytree(folder,dst,dirs_exist_ok=True);r=json.loads((dst/'browser-report.json').read_text());reports[engine]=r
 assert not r['quick'] and r['sourceHashes']['P41R']==sha(asset)
 assert r['Blink100Gate']=='PASS'and r['gpuDeformation']['result']=='PASS'
 assert len(r['shots'])==10 and len(r['expressions'])==16 and len(r['eyeID'])==10 and len(r['mobileViewport'])==4 and len(r['gpuDeformation']['checks'])==36
 assert not r['errors']and r['noSupabaseRequests']and not r['physicalIPhone']and not r['artApproved']
 for x in r['shots']+r['expressions']+r['eyeID']+r['poseShots']+r['mobileViewport']:assert sha(dst/x['file'])==x['sha256']
viewer=Path(sys.argv[3]);files=['graphics/showcase.js','graphics/showcase-gltf.js','graphics/full-influence-skinning.js','graphics/gpu-deformation-probe.js','vendor/addons/GLTFLoader.js','vendor/three.module.js']
(ev/'viewer-source-hashes.json').write_text(json.dumps({p:sha(viewer/p)for p in files},indent=2)+'\n')
com=root/'comparisons';com.mkdir(exist_ok=True);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16);pages=[];names=[]
def label(d,xy,text):d.text(xy,text,font=small,fill='white')
for view in ['front','45','profile','close','body']:
 canvas=Image.new('RGB',(1600,660),'#182636');d=ImageDraw.Draw(canvas)
 for i,(variant,title)in enumerate([('scott-bum07-p41','P4.1 — chưa nghiệm thu'),('scott-bum07-p41r','P4.1R — chờ chủ dự án duyệt mỹ thuật')]):
  im=Image.open(ev/'webkit'/f'{variant}-{view}.png').convert('RGB');im.thumbnail((800,610));canvas.paste(im,(i*800+(800-im.width)//2,45));label(d,(i*800+18,14),title)
 canvas.save(com/f'{view}.jpg',quality=96);pages.append(canvas);names.append(view)
for mode,levels in [('blink',[0,25,50,75,100]),('smile',[0,50,100])]:
 canvas=Image.new('RGB',(360*len(levels),590),'#182636');d=ImageDraw.Draw(canvas)
 for y,angle in enumerate([0,45]):
  for x,level in enumerate(levels):
   im=Image.open(ev/'webkit'/f'p41-{mode}-{level}-{angle}.png').convert('RGB');im.thumbnail((360,260));canvas.paste(im,(x*360+(360-im.width)//2,y*295+30));label(d,(x*360+10,y*295+7),f'{mode} {level}% / {angle}°')
 canvas.save(com/f'{mode}-levels.jpg',quality=96);pages.append(canvas);names.append(mode+'-levels')
poses=reports['webkit']['poseShots'];canvas=Image.new('RGB',(400*len(poses),365),'#182636');d=ImageDraw.Draw(canvas)
for i,s in enumerate(poses):
 im=Image.open(ev/'webkit'/s['file']).convert('RGB');im.thumbnail((400,320));canvas.paste(im,(i*400+(400-im.width)//2,35));label(d,(i*400+10,10),s['pose'])
canvas.save(com/'skin-poses.jpg',quality=96);pages.append(canvas);names.append('skin-poses')
summary=Image.new('RGB',(1600,950),'#182636');d=ImageDraw.Draw(summary)
lines=['BUM07 P4.1R — Scott Final Repair Prototype','NỀN: ea273ab · Scott / Mish7913 · CC BY 4.0','CHƯA NGHIỆM THU MỸ THUẬT — KHÔNG TỰ CHẤM 9/10','Blink100: Chromium/WebKit 0 pixel lộ, góc0°/45°, DPR1 và viewport390×844 DPR2.','12 tư thế: GPU đối chiếu Blender; ngưỡng1e-4, sai lệch tối đa~2.27e-5.','370 joints; giữ toàn bộ influences và Preserve Volume. Adapter DQS đi kèm là bắt buộc.','104.791 tam giác;17 primitives;GLB11.857.720bytes. Không triển khai vào game.','Các viewer glTF chỉ dùng linear skinning chưa được xác nhận đúng biến dạng gốc.','FPS Linux software không phải FPS Safari iPhone. Chưa có thiết bị thật.','Ảnh P4.1 bên trái / P4.1R bên phải: camera, ánh sáng, chiều cao chuẩn hóa giống nhau.','Ảnh rawPNG và phép đo có SHA256 trong evidence/. Contact sheet chỉ ghép/thu nhỏ.','Dừng tại P4.1R, chờ chủ dự án nghiệm thu ảnh. Main/Pages/PR2/Supabase giữ nguyên.']
for i,line in enumerate(lines):d.text((45,45+i*65),line,font=font,fill='white')
summary.save(root/'BUM07-P41R-Render-Review.pdf',save_all=True,append_images=pages,resolution=130)
head='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>BUM07 P4.1R — chờ nghiệm thu</title><style>body{font:17px system-ui;background:#142236;color:#fff;margin:24px}img{width:100%;height:auto}a{color:#a7d8ff}section{margin:32px 0}</style><h1>BUM07 P4.1R — chờ nghiệm thu mỹ thuật</h1><p>Scott / Mish7913 · CC BY4.0 · có chỉnh sửa. P4.1 bên trái, P4.1R bên phải; cùng camera và ánh sáng. Đây là renderGLB thực tế, không phải ảnh AI.</p><p><a href="REPORT.md">Báo cáo</a> · <a href="BUM07-P41R-Render-Review.pdf">PDF ảnh</a> · <a href="ATTRIBUTION.md">Nguồn / giấy phép / thay đổi</a></p><p>Giữ370joints, đầy đủweights và DQS qua adapter nghiên cứu. Không tự công bố9/10. Linux WebKit/Chromium không phải iPhone thật.</p>'''
(root/'gallery.html').write_text(head+'\n'.join(f'<section><h2>{html.escape(n)}</h2><a href="comparisons/{n}.jpg"><img src="comparisons/{n}.jpg" alt="{n}"></a></section>'for n in names)+'</html>')
metrics=json.loads((ev/'glb-roundtrip.json').read_text());native=json.loads((ev/'native-deformation.json').read_text());geo=json.loads((ev/'geometry-audit.json').read_text())
summary={'baseline':'ea273ab94459525c34af07f4022d6ef52ff2e904','phase':'P4.1R','GLBSha256':sha(asset),'technicalScope':'PASS_NATIVE_CPU_AND_RESEARCH_ADAPTER_GPU','artApproval':'PENDING_OWNER','quality9of10Claimed':False,'gameReady':False,'physicalIPhoneTested':False,'requiresCustomDQSAdapter':True,'joints':370,'triangles':metrics['assetTriangles'],'primitives':metrics['primitiveCount'],'GLBBytes':metrics['GLBBytes'],'maxNativeError':native['maxError'],'geometry':geo['result'],'browserResults':{k:{'Blink100':r['Blink100Gate'],'GPU':r['gpuDeformation']['result'],'maxGPUError':max(x['maxError']for x in r['gpuDeformation']['checks']),'poses':12,'desktopSoftwareFpsUnderConcurrentTestLoad':r['desktopBenchmark']['averageFps'],'weightLookupTextureBytes':sum(x['textureBytes']for x in r['skinAdapter'])}for k,r in reports.items()},'stopAfterHandoff':True}
(ev/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print('P41R_EVIDENCE_ASSEMBLED')
