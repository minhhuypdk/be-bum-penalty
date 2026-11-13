"""Reproduce the isolated original-asset preview checkout, never patch repository runtime."""
from pathlib import Path
import sys,shutil,subprocess
root=Path(__file__).resolve().parents[3];out=Path(sys.argv[1]).resolve();scott=Path(sys.argv[2]).resolve();assert out!=root and (root not in out.parents or 'artifacts'in out.parts)
subprocess.run([sys.executable,str(root/'tests/stage-p31r-review.py'),str(out),str(root/'research/bum07-p31r/assets')],cwd=root,check=True)
shutil.copy2(scott,out/'graphics/models/scott-original.glb');p=out/'graphics/showcase.js';s=p.read_text();api="""  p4Frame(angle,mode){window.__repairViewLock=true;controls.enableDamping=false;turntable.rotation.y=angle*Math.PI/180;controls.target.set(0,mode==='body'?1.1:1.80,0);camera.position.set(0,controls.target.y,mode==='body'?5.2:mode==='close'?1.25:2.0);controls.update();needsRender=true;},
""";assert '  getMetrics:reportBase,'in s;p.write_text(s.replace('  getMetrics:reportBase,',api+'  getMetrics:reportBase,'));print('PREVIEW_COPY_READY',out)
