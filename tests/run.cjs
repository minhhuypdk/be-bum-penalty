const http=require('node:http');
const fs=require('node:fs');
const path=require('node:path');
const {spawn,execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'..'),artifacts=path.join(root,'artifacts');
fs.mkdirSync(artifacts,{recursive:true});
const sdk=path.join(artifacts,'supabase.min.js');
const live=process.argv.includes('--live');
function run(file,env){return new Promise((resolve,reject)=>{
 const child=spawn(process.execPath,[path.join(__dirname,file)],{cwd:root,env:{...process.env,...env},stdio:'inherit'});
 child.on('error',reject);child.on('exit',code=>code===0?resolve():reject(new Error(`${file} exited ${code}`)));
});}
const server=http.createServer((req,res)=>{
 let file;try{file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));}catch{res.writeHead(400).end();return}
 if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403).end();return}
 if(file===root)file=path.join(root,'index.html');
 fs.readFile(file,(error,data)=>{if(error){res.writeHead(404).end();return}
  const mime={'.js':'text/javascript','.html':'text/html; charset=utf-8','.png':'image/png','.json':'application/json'};
  res.writeHead(200,{'content-type':mime[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(data);
 });
});
server.listen(0,'127.0.0.1',async()=>{
 try{
  if(!fs.existsSync(sdk))execFileSync('curl',['-fLsS','--max-time','45','https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js','-o',sdk],{stdio:'inherit'});
  const env={GAME_URL:`http://127.0.0.1:${server.address().port}/`,ARTIFACT_DIR:artifacts,SUPABASE_SDK:sdk};
  for(const test of ['auth-isolation.cjs','diagnostics.cjs','rules.cjs','graphics.cjs','characters.cjs','audio.cjs'])await run(test,env);
  await run('multiplayer.cjs',{...env,MOCK_SUPABASE:live?'0':'1',REQUIRE_REALTIME:live?'1':'0',CONCURRENT_ACTIONS:'1'});
  if(live)await run('session-lifecycle.cjs',env);
  console.log(`ALL CHECKS PASSED (${live?'live Supabase; isolated test row retained':'mock REST; no Supabase writes'}). Artifacts: ${artifacts}`);
 }catch(error){console.error(error.message);process.exitCode=1}
 finally{server.close();}
});
