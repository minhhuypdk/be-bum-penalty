"""Read original PNGs and projected iris hulls. No image retouching or output image.
Fixed white/highlight proxy thresholds, not an aesthetic or gaze-quality test.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json
r=Path(__file__).resolve().parents[1];rois=json.loads((r/'evidence/iris-projection-rois.json').read_text())
def hull(points):
 pts=sorted(set(tuple(p) for p in points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lo=[];hi=[]
 for p in pts:
  while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
  lo.append(p)
 for p in reversed(pts):
  while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
  hi.append(p)
 return lo[:-1]+hi[:-1]
rows=[]
for version,items in rois.items():
 for item in items:
  polygon=hull(item['projected_iris_vertices_pixels']);poly=np.array(polygon);x0=max(0,int(np.floor(poly[:,0].min())));x1=min(1200,int(np.ceil(poly[:,0].max()))+1);y0=max(0,int(np.floor(poly[:,1].min())));y1=min(1600,int(np.ceil(poly[:,1].max()))+1)
  xx,yy=np.meshgrid(np.arange(x0,x1)+.5,np.arange(y0,y1)+.5);inside=np.ones(xx.shape,dtype=bool)
  for a,b in zip(poly,np.roll(poly,-1,axis=0)):inside&=((b[0]-a[0])*(yy-a[1])-(b[1]-a[1])*(xx-a[0]))>=-1e-7
  image=np.asarray(Image.open(r/item['file']).convert('RGB'),dtype=np.float32)/255;pixels=image[y0:y1,x0:x1][inside];bright=(pixels.min(axis=1)>.70)&((pixels.max(axis=1)-pixels.min(axis=1))<.20)
  rows.append({'version':version,'camera':item['camera'],'eye':item['eye'],'roi_pixels':len(pixels),'bright_neutral_pixels':int(bright.sum()),'bright_neutral_fraction':float(bright.mean()),'mean_RGB_sRGB':pixels.mean(axis=0).tolist()})
pairs=[]
for b in [x for x in rows if x['version']=='before']:
 a=next(x for x in rows if x['version']=='after' and x['camera']==b['camera'] and x['eye']==b['eye']);pairs.append({'camera':b['camera'],'eye':b['eye'],'before_fraction':b['bright_neutral_fraction'],'after_fraction':a['bright_neutral_fraction'],'fraction_reduced':a['bright_neutral_fraction']<b['bright_neutral_fraction']})
report={'method':'Projected convex hull of iris vertices on same orthographic camera. Read source beauty PNG, minRGB>.70 and RGB range<.20. Same fixed thresholds for both versions, not tuned per-eye/version.','limitations':['Proxy includes hull occlusion by lids; not a semantic specular pass.','Does not prove natural gaze, attractiveness, or performance. Owner review required.','No pixels edited; original Blender PNGs preserved.'],'rows':rows,'comparisons':pairs};(r/'evidence/glare-proxy.json').write_text(json.dumps(report,indent=2));print('GLARE_PROXY',pairs)
