import bpy,json,sys,math,hashlib
from pathlib import Path
src=Path(bpy.data.filepath);h=hashlib.sha256(src.read_bytes()).hexdigest();report={'sourceFile':src.name,'sourceSha256':h,'readOnly':True,'autoExecDisabled':True,'blender':bpy.app.version_string,'objects':[],'armatures':[],'images':[],'texts':[],'actions':[]}
for o in bpy.data.objects:
 if o.type=='ARMATURE':report['armatures'].append({'name':o.name,'bones':len(o.data.bones),'deformBones':sum(b.use_deform for b in o.data.bones),'constraints':sum(len(b.constraints)for b in o.pose.bones),'drivers':len(o.animation_data.drivers)if o.animation_data else 0})
 if o.type=='MESH':
  o.data.calc_loop_triangles();report['objects'].append({'name':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'triangles':len(o.data.loop_triangles),'quads':sum(len(f.vertices)==4 for f in o.data.polygons),'uvLayers':len(o.data.uv_layers),'materials':[m.name if m else None for m in o.data.materials],'shapeKeys':list(o.data.shape_keys.key_blocks.keys())if o.data.shape_keys else [],'modifiers':[{'type':m.type,'name':m.name,'levels':getattr(m,'levels',None),'renderLevels':getattr(m,'render_levels',None)}for m in o.modifiers],'armatureModifiers':sum(m.type=='ARMATURE'for m in o.modifiers),'drivers':len(o.data.shape_keys.animation_data.drivers)if o.data.shape_keys and o.data.shape_keys.animation_data else 0})
for im in bpy.data.images:report['images'].append({'name':im.name,'size':list(im.size),'packed':bool(im.packed_file),'path':im.filepath})
for text in bpy.data.texts:report['texts'].append({'name':text.name,'bytes':len(text.as_string()),'autoRun':text.use_module})
for a in bpy.data.actions:report['actions'].append({'name':a.name,'frames':list(a.frame_range)})
report['totals']={'meshes':len(report['objects']),'baseTriangles':sum(o['triangles']for o in report['objects']),'materialSlots':sum(len(o['materials'])for o in report['objects']),'shapeKeys':sum(max(0,len(o['shapeKeys'])-1)for o in report['objects'])};assert hashlib.sha256(src.read_bytes()).hexdigest()==h
Path(sys.argv[sys.argv.index('--')+1]).write_text(json.dumps(report,indent=2)+'\n');print('READ_ONLY_ASSET_AUDIT',report['totals'])
