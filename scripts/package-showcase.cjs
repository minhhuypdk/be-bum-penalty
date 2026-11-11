const fs=require('node:fs'),path=require('node:path');
const {execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'..'),destination=path.resolve(process.argv[2]||'/workspace/sites/be-bum-character-showcase');
const identity=JSON.parse(fs.readFileSync(path.join(root,'showcase/preview-site.json'),'utf8'));
if(destination===root||destination.startsWith(root+path.sep))throw new Error('Use a separate deployment artifact directory, never the game checkout.');
const config=path.join(destination,'.openai/hosting.json');
if(fs.existsSync(config)&&JSON.parse(fs.readFileSync(config)).project_id!==identity.project_id)throw new Error('Refusing to overwrite another Site identity.');
fs.mkdirSync(path.dirname(config),{recursive:true});
fs.writeFileSync(config,JSON.stringify({project_id:identity.project_id,static:{directory:'dist'}},null,2)+'\n');
const files=['graphics/showcase.html','graphics/showcase.css','graphics/showcase.js','graphics/showcase-motion.js','graphics/showcase-gltf.js','graphics/characters.js','vendor/three.module.js','vendor/THREE-LICENSE.txt','vendor/addons/OrbitControls.js','vendor/addons/GLTFLoader.js','vendor/addons/BufferGeometryUtils.js'];
for(const name of ['snow-review-portrait.glb','snow-review-mobile.glb','manifest.json','build-report.json','glb-audit.json','CREDITS.md'])files.push('graphics/models/snow/'+name);
for(const id of ['ba-player','ba-keeper','bum-player','bum-keeper'])files.push(`graphics/showcase-assets/${id}.png`);
for(const file of files){const target=path.join(destination,'dist',file);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(root,file),target);}
const html=fs.readFileSync(path.join(root,'graphics/showcase.html'),'utf8').replace('href="./showcase.css"','href="./graphics/showcase.css"').replace('src="./showcase.js"','src="./graphics/showcase.js"').replace('href="./models/snow/CREDITS.md"','href="./graphics/models/snow/CREDITS.md"');
fs.writeFileSync(path.join(destination,'dist/index.html'),html);
const reports=['showcase/fps-report.json','showcase/FPS-REPORT.md'];
for(const report of reports)if(fs.existsSync(path.join(root,report))){const target=path.join(destination,'dist/reports',path.basename(report));fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(root,report),target);}
const renders=path.join(root,'showcase/renders');
if(fs.existsSync(renders))for(const name of fs.readdirSync(renders))if(name.endsWith('.png')){const target=path.join(destination,'dist/renders',name);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(renders,name),target);}
const review=path.join(root,'showcase/asset-review');if(fs.existsSync(review))for(const name of fs.readdirSync(review))if(/\.(png|json|webm|md)$/.test(name)){const target=path.join(destination,'dist/asset-review',name);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(review,name),target);}
fs.writeFileSync(path.join(destination,'SOURCE-PROVENANCE.json'),JSON.stringify({github:identity.source_repository,branch:identity.source_branch,source_commit:execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),files,excludes:['game index.html','Supabase SDK/config','rooms','wallets','sessions','credentials','third-party purchased assets']},null,2)+'\n');
console.log(JSON.stringify({destination,project_id:identity.project_id,files:files.length,noSupabase:true}));
