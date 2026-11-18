/* Actual GPU readback using the SAME adapter shader as beauty/ID passes.
 * Float target, real exported vertex attributes, native bone-pose snapshots.
 * Not a visual approximation, CPU-only skin simulation, or iPhone benchmark.
 */
import * as THREE from '../vendor/three.module.js';
const sanitize=n=>THREE.PropertyBinding.sanitizeNodeName(n);
export function applyNativePose(model,fixture,index){
 const p=fixture.poses[index];if(!p)throw Error('Unknown pose '+index);
 for(let i=0;i<fixture.jointNames.length;i++){
  const name=fixture.jointNames[i],b=model.getObjectByName(name)||model.getObjectByName(sanitize(name));if(!b?.isBone)throw Error('Missing native joint '+name);
  b.matrixAutoUpdate=false;b.matrix.fromArray(p.boneLocalMatrices[i]);
 }
 model.updateMatrixWorld(true);return p.name;
}
export function readbackNativeDeformation(model,renderer,camera,fixture,index){
 const p=fixture.poses[index],rows=[],assetInverse=model.matrixWorld.clone().invert(),meshes=[];
 model.traverse(o=>{if(!o.isSkinnedMesh)return;let p=o;while(p&&!p.userData.P41R_skinning)p=p.parent;if(/BodyFaceEyes|Jersey/.test(p?.name||o.name))meshes.push(o);});
 const oldTarget=renderer.getRenderTarget(),shadow=renderer.shadowMap.enabled,clear=renderer.getClearColor(new THREE.Color()),alpha=renderer.getClearAlpha();
 try{
  renderer.shadowMap.enabled=false;renderer.setClearColor(0,0);
  for(const source of meshes){
   let parent=source;while(parent&&!parent.userData.P41R_skinning)parent=parent.parent;const name=Object.keys(p.samples).find(n=>sanitize(n)===(parent?.name||source.name));if(!name)throw Error('Missing fixture samples '+source.name);
   const g=source.geometry.clone();g.setIndex(null);const count=g.attributes.position.count,width=256,height=Math.ceil(count/width),srcID=Object.entries(g.attributes).find(([n])=>n.toLowerCase()==='_p41_source_id')?.[1];if(!srcID)throw Error('Missing explicit source IDs');
   const base=new THREE.ShaderMaterial({uniforms:{probeSize:{value:new THREE.Vector2(width,height)},assetInverse:{value:assetInverse}},vertexShader:`
#include <common>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
uniform vec2 probeSize;uniform mat4 assetInverse;varying vec3 probePoint;
void main(){
#include <skinbase_vertex>
#include <begin_vertex>
#include <morphtarget_vertex>
#include <skinning_vertex>
probePoint=(assetInverse*modelMatrix*vec4(transformed,1.0)).xyz;
vec2 pixel=vec2(mod(p41rVertex,probeSize.x),floor(p41rVertex/probeSize.x));
gl_Position=vec4((pixel+.5)/probeSize*2.-1.,0.,1.);gl_PointSize=1.0;
}`,fragmentShader:'varying vec3 probePoint;void main(){gl_FragColor=vec4(probePoint,1.0);}',depthTest:false,depthWrite:false,toneMapped:false});
   const material=source.userData.p41rSkinMaterial(base),points=new THREE.Points(g,material);points.isSkinnedMesh=true;points.skeleton=source.skeleton;points.bindMatrix=source.bindMatrix;points.bindMatrixInverse=source.bindMatrixInverse;points.matrixAutoUpdate=false;points.matrix.copy(source.matrixWorld);points.frustumCulled=false;points.morphTargetInfluences=source.morphTargetInfluences;points.morphTargetDictionary=source.morphTargetDictionary;points.onBeforeRender=source.onBeforeRender;
   const scene=new THREE.Scene();scene.add(points);const target=new THREE.WebGLRenderTarget(width,height,{type:THREE.FloatType,format:THREE.RGBAFormat,depthBuffer:false,stencilBuffer:false});renderer.setRenderTarget(target);renderer.render(scene,camera);const data=new Float32Array(width*height*4);renderer.readRenderTargetPixels(target,0,0,width,height,data);
   let max=0,sum=0,n=0;for(let v=0;v<count;v++){
    const expected=p.samples[name][String(Math.round(srcID.getX(v)))];if(!expected)continue;
    if(data[v*4+3]<.99)throw Error('GPU sample not rendered '+source.name+' '+v);
    const error=Math.hypot(data[v*4]-expected[0],data[v*4+1]-expected[1],data[v*4+2]-expected[2]);if(!Number.isFinite(error))throw Error('Nonfinite GPU skin');max=Math.max(max,error);sum+=error*error;n++;
   }
   rows.push({pose:p.name,mesh:source.name,method:parent.userData.P41R_skinning,samples:n,maxError:max,rmsError:Math.sqrt(sum/n),floatTarget:true});
   target.dispose();g.dispose();material.dispose();base.dispose();
  }
 }finally{renderer.setRenderTarget(oldTarget);renderer.shadowMap.enabled=shadow;renderer.setClearColor(clear,alpha);}
 return rows;
}
