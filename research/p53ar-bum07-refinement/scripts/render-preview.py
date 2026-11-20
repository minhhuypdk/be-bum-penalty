"""Diagnostic Blender renders only, never save preview settings into native file."""
import bpy
from pathlib import Path
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r/'bum07-p53ar-refinement.blend'));s=bpy.context.scene;s.cycles.samples=12;s.cycles.use_denoising=False;s.render.resolution_x=640;s.render.resolution_y=853;s.render.resolution_percentage=100
for name in ['Face_front-000','Face_three-quarter-045','Face_profile-090','Full_back-180']:
 s.camera=bpy.data.objects[name];s.render.filepath=str(r/'evidence/previews'/(name+'.png'));bpy.ops.render.render(write_still=True);print('PREVIEW_READY',name,flush=True)
