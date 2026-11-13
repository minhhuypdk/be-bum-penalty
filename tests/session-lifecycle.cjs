const assert=require('node:assert/strict');
const {openHarness}=require('./room-harness.cjs');
const baseline=process.argv.includes('--baseline');
(async()=>{
 const h=await openHarness(process.env.GAME_URL||'http://127.0.0.1:4180/'),checks={};
 try{
  const first=await h.open(),second=await h.open();
  await Promise.all([first.evaluate(()=>join('ba')),second.evaluate(()=>join('ba'))]);
  const roles=await Promise.all([first.evaluate(()=>role),second.evaluate(()=>role)]);
  checks.onlyOneDeviceWinsClaimRace=roles.filter(r=>r==='ba').length===1;
  assert(checks.onlyOneDeviceWinsClaimRace);
  const a=roles[0]==='ba'?first:second,b=a===first?second:first;
  await b.evaluate(()=>join('bum'));
  for(const p of [a,b])await p.waitForFunction(()=>room.state.players.ba&&room.state.players.bum);
  const aToken=await a.evaluate(()=>token);
  const outsider=await h.open();await outsider.evaluate(()=>join('ba'));
  checks.occupiedRoleDenied=await outsider.evaluate(()=>role===null);
  checks.failedJoinDoesNotSaveRole=await outsider.evaluate(()=>sessionStorage.getItem('bbpenalty-role')===null);
  await a.reload({waitUntil:'domcontentloaded'});await a.waitForFunction(()=>role==='ba'&&room?.state?.players.ba===token);
  checks.reloadKeepsOwnership=(await a.evaluate(()=>token))===aToken;
  h.failNextWrite();await a.evaluate(()=>leave());await a.waitForFunction(()=>!busy);
  checks.failedReleaseKeepsOwnership=await a.evaluate(()=>role==='ba'&&sessionStorage.getItem('bbpenalty-role')==='ba'&&room.state.players.ba===token);
  // Restore only the isolated test client's local role to continue auditing v1.
  if(baseline&&!checks.failedReleaseKeepsOwnership)await a.evaluate(()=>{role='ba';sessionStorage.setItem('bbpenalty-role','ba')});
  await a.evaluate(()=>leave());await a.waitForFunction(()=>!busy);
  await b.waitForFunction(()=>room.state.players.ba===null);
  checks.releaseFreesRole=await a.evaluate(()=>role===null&&room.state.players.ba===null);
  await outsider.evaluate(()=>join('ba'));await outsider.waitForFunction(()=>room.state.players.ba===token);
  checks.otherDeviceCanClaimReleasedRole=true;
  const saved=await outsider.context().storageState(),oldToken=await outsider.evaluate(()=>token);
  const replacement=await h.open(saved);
  const supportsRecovery=await replacement.evaluate(()=>typeof recoverRole==='function');
  if(supportsRecovery){
   await replacement.getByRole('button',{name:'Tiếp tục BA trên máy này',exact:true}).click();
   await replacement.waitForFunction(()=>role==='ba'&&room.state.players.ba===token);
   checks.sameDeviceCanRecoverOldSession=(await replacement.evaluate(()=>token))!==oldToken;
   await outsider.waitForFunction(()=>room.state.players.ba!==token);
   await outsider.evaluate(()=>choose(0));
   checks.oldSessionCannotShoot=await replacement.evaluate(()=>room.state.shot===null);
   await outsider.evaluate(()=>recoverRole('ba'));await replacement.evaluate(()=>fetchRoom());
   checks.staleRecoveryCannotTakeRoleBack=await replacement.evaluate(()=>room.state.players.ba===token);
   await outsider.evaluate(()=>leave());await replacement.evaluate(()=>fetchRoom());
   checks.oldSessionCannotReleaseNewOwner=await replacement.evaluate(()=>room.state.players.ba===token);
   checks.recoveryPreservesMatch=await replacement.evaluate(()=>room.state.turn===0&&room.state.history.length===0&&room.state.score.ba===0&&room.state.score.bum===0);
  }else{
   await replacement.evaluate(()=>join('ba'));
   checks.sameDeviceCanRecoverOldSession=await replacement.evaluate(()=>role==='ba');
  }
  if(!baseline)assert(Object.values(checks).every(Boolean),JSON.stringify(checks));
  else {assert(checks.occupiedRoleDenied&&checks.reloadKeepsOwnership&&checks.releaseFreesRole);assert(!checks.failedReleaseKeepsOwnership&&!checks.sameDeviceCanRecoverOldSession);}
  assert.deepEqual(h.errors,[]);
  console.log(JSON.stringify({mode:baseline?'baseline defects reproduced':'PASS',checks,errors:h.errors}));
 }finally{await h.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
