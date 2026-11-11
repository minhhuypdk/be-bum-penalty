const{chromium,webkit}=require('playwright');
const fs=require('node:fs');
const assert=require('node:assert/strict'),crypto=require('node:crypto');
const base=process.env.GAME_URL||'http://127.0.0.1:4180/';
const engine=process.env.SHOWCASE_ENGINE||'chromium';
(async()=>{
 const browser=engine==='webkit'?await webkit.launch({executablePath:process.env.WEBKIT_PATH,headless:true}):await chromium.launch({executablePath:require('./browser.cjs').executablePath,headless:true,args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const results=[];
 try{
  for(const profile of [{name:'desktop-software',width:1300,height:900,dpr:1},{name:'portrait-retina-emulation',width:390,height:844,dpr:3}]){
   const context=await browser.newContext({viewport:{width:profile.width,height:profile.height},deviceScaleFactor:profile.dpr,isMobile:profile.dpr===3,hasTouch:profile.dpr===3});
   const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(new URL('graphics/showcase.html',base).href,{waitUntil:'domcontentloaded'});await page.waitForSelector('body[data-ready=true]',{timeout:60000});
   for(const [character,action]of profile.dpr===3?[['bum-keeper','save']]:[['ba-player','run']]){
    const result=await page.evaluate(async({character,action})=>{showcase.selectCharacter(character);showcase.setAction(action);showcase.setPaused(false);showcase.frame('body');return await showcase.measure(8);},{character,action});
    assert(result.durationSeconds>=8&&Number.isFinite(result.averageFps)&&result.averageFps>0,'FPS sample must cover a full eight seconds');assert.deepEqual(errors,[]);results.push({profile:profile.name,engine,...result,errors});console.log(JSON.stringify(results[results.length-1]));
   }
   await context.close();
  }
 }finally{await browser.close();}
 fs.mkdirSync('showcase',{recursive:true});const file=process.env.FPS_REPORT||`showcase/fps-${engine}.json`;fs.writeFileSync(file,JSON.stringify({measuredHardware:'Codex Linux browser rendering, not a physical iPhone',sourceFilesSha256:Object.fromEntries(['graphics/showcase.js','graphics/showcase-motion.js','graphics/characters.js'].map(p=>[p,crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')])),results},null,2)+'\n');
})().catch(e=>{console.error(e);process.exitCode=1});
