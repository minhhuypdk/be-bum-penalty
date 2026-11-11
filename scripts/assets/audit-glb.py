"""Static, offline audit of shipped self-contained review GLBs (no execution)."""
import json,struct,hashlib,pathlib
root=pathlib.Path(__file__).resolve().parents[2];reports=[]
def size(data):
 if data.startswith(b'\x89PNG'):return struct.unpack('>II',data[16:24])
 assert data[:2]==b'\xff\xd8','Unsupported embedded image'
 i=2
 while i<len(data):
  if data[i]!=255:i+=1;continue
  marker=data[i+1];i+=2
  if marker in [0xd8,0xd9]:continue
  length=struct.unpack('>H',data[i:i+2])[0]
  if marker in [0xc0,0xc1,0xc2]:
   height,width=struct.unpack('>HH',data[i+3:i+7]);return width,height
  i+=length
 raise ValueError('No JPEG dimensions')
for path in sorted((root/'graphics/models/snow').glob('*.glb')):
 b=path.read_bytes();magic,version,total=struct.unpack_from('<III',b);assert magic==0x46546c67 and version==2 and total==len(b)
 length=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+length]);offset=28+length
 assert all('uri' not in x for x in d.get('images',[])+d.get('buffers',[]))
 assert not d.get('extensionsRequired')
 textures=[]
 for im in d.get('images',[]):
  view=d['bufferViews'][im['bufferView']];start=offset+view.get('byteOffset',0);w,h=size(b[start:start+view['byteLength']]);textures.append({'name':im.get('name'),'width':w,'height':h,'encodedBytes':view['byteLength']})
 reports.append({'file':str(path.relative_to(root)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'triangles':sum(d['accessors'][p['indices']]['count']//3 for m in d['meshes']for p in m['primitives']),'meshPrimitives':sum(len(m['primitives'])for m in d['meshes']),'materials':len(d['materials']),'skinJointCounts':[len(s['joints'])for s in d.get('skins',[])],'clips':[a.get('name')for a in d.get('animations',[])],'textures':textures,'estimatedRGBA8TextureMiBWithMipmaps':round(sum(t['width']*t['height']*4*4/3 for t in textures)/1024**2,2),'warning':'Texture estimate excludes geometry, shadows, environment, browser copies and other renderer allocations; actual GPU memory is device-dependent.'})
p=root/'graphics/models/snow/glb-audit.json';p.write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps([{k:v for k,v in r.items()if k!='textures'}for r in reports],indent=2))
