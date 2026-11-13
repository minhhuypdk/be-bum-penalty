import * as THREE from '../vendor/three.module.js';
import {poseCharacter} from './characters.js';

export const CLIPS=Object.freeze({idle:{name:'Đứng',duration:4},run:{name:'Chạy',duration:1},kick:{name:'Sút bóng',duration:3.2},save:{name:'Bay người bắt bóng',duration:4.8},celebrate:{name:'Ăn mừng',duration:3.6}});
const clamp=THREE.MathUtils.clamp;
const ease=t=>{t=clamp(t,0,1);return t*t*(3-2*t)};
const span=(p,a,b)=>ease((p-a)/(b-a));

// Showcase-only staging: the multiplayer pose/state code is never called here.
export function animateShowcase(actor,rig,action,time,centerHeight,ball){
 const duration=CLIPS[action]?.duration||4,p=(time%duration)/duration;
 rig.position.set(0,centerHeight,0);rig.rotation.set(0,0,0);ball.visible=false;
 poseCharacter(actor,time,action==='save'?'save':action==='celebrate'?'celebrate':action==='kick'?'kick':'idle',p);
 const {joints:j,knees,elbows,head}=actor.userData;
 if(action==='idle'){rig.position.y+=Math.sin(time*1.65)*.005;return p}
 if(action==='run'){
  const phase=p*Math.PI*2,step=Math.sin(phase);
  j.leftLeg.rotation.x=step*.72;j.rightLeg.rotation.x=-step*.72;
  knees[0].rotation.x=Math.max(0,-step)*1.05;knees[1].rotation.x=Math.max(0,step)*1.05;
  j.leftArm.rotation.x=-step*.6;j.rightArm.rotation.x=step*.6;
  elbows[0].rotation.x=elbows[1].rotation.x=-.65;
  rig.position.y+=.025+Math.abs(Math.sin(phase))*.065;rig.rotation.x=.11;rig.rotation.z=step*.025;head.rotation.x=-.06;
 }else if(action==='kick'){
  const back=span(p,.08,.27),strike=span(p,.28,.46),recover=span(p,.57,.88);
  j.rightLeg.rotation.x=(.62*back-2.05*strike)*(1-recover);
  knees[1].rotation.x=(.8*back*(1-strike)+.2*strike)*(1-recover);
  knees[0].rotation.x=.10*Math.sin(Math.PI*p);
  j.leftArm.rotation.x=.55*strike*(1-recover);j.rightArm.rotation.x=-.55*strike*(1-recover);
  j.leftArm.rotation.z=-.25-.4*back*(1-recover);j.rightArm.rotation.z=.25+.25*strike*(1-recover);
  rig.position.z=.18*(back-strike)*(1-recover);rig.rotation.x=.08*back-.13*strike*(1-recover);
  const scale=actor.scale.x,flight=span(p,.43,.78);
  ball.visible=p<.9;ball.position.set(.155*scale,.165+Math.sin(flight*Math.PI)*.5,.43*scale+flight*2.1);ball.rotation.set(flight*9,flight*2,0);
 }else if(action==='save'){
  const direction=Math.floor(time/duration)%2?-1:1,launch=span(p,.12,.37),landing=span(p,.48,.67),recover=span(p,.74,.98);
  const reach=launch*(1-recover),roll=direction*-1.24*reach;
  rig.position.x=direction*1.45*reach;
  const floor=Math.abs(Math.cos(roll))*centerHeight+Math.abs(Math.sin(roll))*.53+.018;
  rig.position.y=Math.max(floor,centerHeight+Math.sin(Math.PI*launch)*.45-.36*landing*(1-recover));rig.rotation.z=roll;
  j.leftArm.rotation.z=direction<0?-2.1*reach-.35:1.4*reach-.35;
  j.rightArm.rotation.z=direction>0?2.1*reach+.35:-1.4*reach+.35;
  elbows[0].rotation.x=elbows[1].rotation.x=-.18;
  knees[0].rotation.x=.50*reach;knees[1].rotation.x=.70*reach;j.leftLeg.rotation.x=-.15*reach;j.rightLeg.rotation.x=.3*reach;
  head.rotation.z=-direction*.1*reach;
 }else if(action==='celebrate'){
  rig.position.y+=Math.abs(Math.sin(time*5.2))*.12;
  rig.rotation.y=Math.sin(time*2)*.12;
  j.leftArm.rotation.z=-2.45+Math.sin(time*6)*.12;j.rightArm.rotation.z=2.45-Math.sin(time*6)*.12;
  knees[0].rotation.x=knees[1].rotation.x=.08*Math.abs(Math.sin(time*5.2));
 }
 return p;
}
