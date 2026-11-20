import bpy
from pathlib import Path
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r/'bum07-p53b1-head-study.blend'));s=bpy.context.scene;s.cycles.samples=12;s.cycles.use_denoising=False;s.render.resolution_x=720;s.render.resolution_y=960;s.render.resolution_percentage=100
for camera in ['Face_front-000','Face_three-quarter-045','Face_profile-090','B1_back_180']:
 s.camera=bpy.data.objects[camera];s.render.filepath=str(r/'evidence/previews'/(camera+'.png'));bpy.ops.render.render(write_still=True);print('B1_PREVIEW_READY',camera,flush=True)
