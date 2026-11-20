"""Geometric ROI projection for read-only pixel glare proxy, not image editing."""
import bpy,json,hashlib
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
r=Path(__file__).resolve().parents[1];result={};sources={}
for version,path in [('before',r.parent/'p53a-bum07-blender-blockout/bum07-p53a-blockout.blend'),('after',r/'bum07-p53ar-refinement.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene;rows=[];sources[version]={'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'resolution':[1200,1600]}
 for camname,file in [('Face_front-000','face-front-000.png'),('Face_three-quarter-045','face-three-quarter-045.png')]:
  c=bpy.data.objects[camname]
  for side in ['R','L']:
   o=bpy.data.objects['Iris_'+side];points=[]
   for v in o.data.vertices:
    p=world_to_camera_view(s,c,o.matrix_world@v.co);points.append([p.x*1200,(1-p.y)*1600])
   rows.append({'camera':camname,'file':f'renders/{version}/{file}','eye':side,'projected_iris_vertices_pixels':points})
 result[version]=rows
(r/'evidence/iris-projection-sources.json').write_text(json.dumps(sources,indent=2));(r/'evidence/iris-projection-rois.json').write_text(json.dumps(result));print('IRIS_ROIS_EXPORTED_NOT_ART_APPROVAL')
