"""Read native material nodes against immutable P5.2R values, not lit pixels."""
import bpy,json
from pathlib import Path
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r/'bum07-p53ar-refinement.blend'));spec=json.loads((r.parent/'p52r-bum07-design-lock/specification/design-spec.json').read_text());rows=[]
def linear(h):
 v=[int(h[i:i+2],16)/255 for i in (1,3,5)];return [c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in v]
for p in spec['palette']:
 m=bpy.data.materials[p['id']];node=m.node_tree.nodes['Principled BSDF'];actual=list(node.inputs['Base Color'].default_value)[:3];rough=node.inputs['Roughness'].default_value;metal=node.inputs['Metallic'].default_value;ok=all(abs(a-b)<1e-6 for a,b in zip(actual,linear(p['baseColor_sRGB']))) and p['roughnessProposed'][0]<=rough<=p['roughnessProposed'][1] and metal==0
 rows.append({'material':m.name,'P52R_sRGB':p['baseColor_sRGB'],'actual_node_linear_RGB':actual,'actual_roughness':rough,'actual_metallic':metal,'PASS':ok});assert ok,m.name
external=[{'name':img.name,'path':img.filepath,'packed':bool(img.packed_file)} for img in bpy.data.images if img.source=='FILE' and img.users>0]
assert all(x['packed'] for x in external)
(r/'evidence/palette-readback.json').write_text(json.dumps({'palette_materials_PASS':len(rows),'materials':rows,'external_image_dependencies':external,'note':'Values checked from saved native .blend. Lit pixels are transformed by lighting and AgX, not expected to match hex.'},indent=2));print('PASS_NATIVE_PALETTE_10')
