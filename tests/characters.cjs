const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.GAME_URL||'http://127.0.0.1:4180/';
(async()=>{
 const browser=await chromium.launch({executablePath:require('./browser.cjs').executablePath,args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try {
  const page=await browser.newPage({viewport:{width:430,height:900},reducedMotion:'reduce'}), errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(new URL('graphics/review.html',base).href);await page.waitForSelector('body[data-ready=true]');
  const contracts=await page.evaluate(async base=>{
   const {createCharacter,poseCharacter,CHARACTER_PRESETS}=await import(new URL('graphics/characters.js',base).href);
   return Object.keys(CHARACTER_PRESETS).map(id=>{
    const c=createCharacter(id);let finite=true,triangles=0;
    c.traverse(o=>{if(o.isMesh){for(const value of o.geometry.attributes.position.array)if(!Number.isFinite(value))finite=false;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;}});
    poseCharacter(c,0,'idle',0);const openEye=c.userData.eyes[0].scale.y;
    poseCharacter(c,1,'kick',.5);const leg=c.userData.joints.rightLeg.rotation.x;
    poseCharacter(c,1,'save',.5);const arm=c.userData.joints.leftArm.rotation.z;
    return{id,finite,triangles,openEye,leg,arm};
   });
  },base);
  assert.equal(contracts.length,4);assert(contracts.every(c=>c.finite&&c.triangles>10000&&c.openEye>.9&&c.leg<-.5&&c.arm<-1));
  for(const id of ['ba-player','bum-player','ba-keeper','bum-keeper']){
   await page.selectOption('#character',id);await page.waitForTimeout(100);
   await page.screenshot({path:`${process.env.ARTIFACT_DIR||'tests'}/${id}-v2.png`});
  }
  for(const pose of ['kick','save','celebrate']){await page.selectOption('#pose',pose);await page.waitForTimeout(100);}
  assert.deepEqual(errors,[]);console.log('PASS: four continuous-surface characters, finite geometry, articulation, reduced motion, mobile review screenshots.',JSON.stringify(contracts));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
