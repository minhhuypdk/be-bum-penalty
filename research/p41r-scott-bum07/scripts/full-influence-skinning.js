/* P4.1R research-only Three.js adapter. ALL glTF JOINTS_n/WEIGHTS_n kept.
 * No extra joints, rigid binding, weight truncation or corrective test-pose bake.
 * Original Three.js weight0 normalization is disabled ONLY in isolated staging.
 */
import * as THREE from '../vendor/three.module.js';
export function installFullInfluenceSkinning(model){
 const report=[];const boneCache=new Map(),ownedTextures=new Set();
 function nativeBoneDQ(skeleton){
  if(boneCache.has(skeleton))return boneCache.get(skeleton);
  const width=1024,height=Math.ceil(skeleton.bones.length*6/width),data=new Float32Array(width*height*4),texture=new THREE.DataTexture(data,width,height,THREE.RGBAFormat,THREE.FloatType);texture.magFilter=texture.minFilter=THREE.NearestFilter;texture.generateMipmaps=false;ownedTextures.add(texture);
  const bases=skeleton.boneInverses.map(m=>m.clone().invert());let frame=-1;
  const update=renderer=>{
   if(frame===renderer.info.render.frame)return;frame=renderer.info.render.frame;
   for(let i=0;i<skeleton.bones.length;i++){
    const pose=new THREE.Matrix4().multiplyMatrices(model.matrixWorld.clone().invert(),skeleton.bones[i].matrixWorld),e=pose.elements,y=new THREE.Vector3(e[4],e[5],e[6]).normalize(),x=new THREE.Vector3(e[0],e[1],e[2]);x.addScaledVector(y,-x.dot(y)).normalize();const z=x.clone().cross(y).normalize();x.copy(y).cross(z).normalize();
    const rigid=new THREE.Matrix4().makeBasis(x,y,z);rigid.setPosition(e[12],e[13],e[14]);
    const diff=rigid.clone().multiply(skeleton.boneInverses[i]),q=new THREE.Quaternion().setFromRotationMatrix(diff).normalize(),t=new THREE.Vector3().setFromMatrixPosition(diff),dual=new THREE.Quaternion(t.x,t.y,t.z,0).multiply(q);
    const residual=bases[i].clone().multiply(rigid.clone().invert()).multiply(pose).multiply(skeleton.boneInverses[i]);
    const at=i*24;data.set([q.x,q.y,q.z,q.w,dual.x*.5,dual.y*.5,dual.z*.5,dual.w*.5],at);data.set(residual.elements,at+8);
   }
   texture.needsUpdate=true;
  };const rec={texture,width,height,update};boneCache.set(skeleton,rec);return rec;
 }

 model.traverse(o=>{
  if(!o.isSkinnedMesh)return;
  const g=o.geometry,attrs=g.attributes,sets=[];
  for(let i=0;;i++){
   const j=attrs[i===0?'skinIndex':'joints_'+i],w=attrs[i===0?'skinWeight':'weights_'+i];
   if(!j||!w)break;sets.push([j,w]);
  }
  if(!sets.length)throw Error('Missing skin attributes: '+o.name);
  let parent=o;while(parent&&!parent.userData.P41R_skinning)parent=parent.parent;const dqs=parent?.userData.P41R_skinning==='DUAL_QUATERNION',dqInfo=dqs?nativeBoneDQ(o.skeleton):null;
  const count=attrs.position.count,N=sets.length,width=1024,height=Math.ceil(count*N*2/width),data=new Float32Array(width*height*4),idx=new Float32Array(count);
  let maxSumError=0,maxInfluences=0;
  for(let v=0;v<count;v++){
   idx[v]=v;let total=0,inf=0;
   for(let s=0;s<N;s++)for(let c=0;c<4;c++){
    const read=(a)=>[a.getX,a.getY,a.getZ,a.getW][c].call(a,v),weight=read(sets[s][1]);total+=weight;if(weight>0)inf++;
    data[(v*N*2+s*2)*4+c]=read(sets[s][0]);data[(v*N*2+s*2+1)*4+c]=weight;
   }
   maxSumError=Math.max(maxSumError,Math.abs(total-1));maxInfluences=Math.max(maxInfluences,inf);
  }
  if(maxSumError>1e-5)throw Error('Full weights not normalized '+o.name+' '+maxSumError);
  const tex=new THREE.DataTexture(data,width,height,THREE.RGBAFormat,THREE.FloatType);tex.needsUpdate=true;tex.magFilter=tex.minFilter=THREE.NearestFilter;tex.generateMipmaps=false;ownedTextures.add(tex);
  g.setAttribute('p41rVertex',new THREE.BufferAttribute(idx,1));
  // Extra weights live in texture, avoiding >16 vertex-attribute slots on Safari.
  for(let s=1;s<N;s++){g.deleteAttribute('joints_'+s);g.deleteAttribute('weights_'+s);}
  let decl=`uniform highp sampler2D p41rWeights;uniform vec2 p41rTexSize;attribute float p41rVertex;
vec4 p41rRead(float t){float yy=floor(t/p41rTexSize.x);return texture2D(p41rWeights,(vec2(t-yy*p41rTexSize.x,yy)+.5)/p41rTexSize);}\n`;
  let blend='mat4 p41rSkin=mat4(0.0);';
  for(let s=0;s<N;s++){
   blend+=`{vec4 jj=p41rRead(p41rVertex*${N*2}.0+${s*2}.0);vec4 ww=p41rRead(p41rVertex*${N*2}.0+${s*2+1}.0);`;
   for(const c of ['x','y','z','w'])blend+=`if(ww.${c}>0.0)p41rSkin+=getBoneMatrix(jj.${c})*ww.${c};`;
   blend+='}';
  }
  if(dqs){
   decl+=`uniform highp sampler2D p41rBoneDQ;uniform mat4 p41rAssetWorld;uniform vec2 p41rBoneSize;
vec4 p41rDQRead(float f){float y=floor(f/p41rBoneSize.x);return texture2D(p41rBoneDQ,(vec2(f-y*p41rBoneSize.x,y)+.5)/p41rBoneSize);}
vec4 p41rMulQ(vec4 a,vec4 b){return vec4(a.w*b.xyz+b.w*a.xyz+cross(a.xyz,b.xyz),a.w*b.w-dot(a.xyz,b.xyz));}
mat4 p41rQuatMat(vec4 q){float x=q.x,y=q.y,z=q.z,w=q.w;return mat4(1.-2.*(y*y+z*z),2.*(x*y+w*z),2.*(x*z-w*y),0.,2.*(x*y-w*z),1.-2.*(x*x+z*z),2.*(y*z+w*x),0.,2.*(x*z+w*y),2.*(y*z-w*x),1.-2.*(x*x+y*y),0.,0.,0.,0.,1.);}
`;
   blend='vec4 p41rQ=vec4(0.0),p41rD=vec4(0.0);mat4 p41rS=mat4(0.0);';
   for(let set=0;set<N;set++){
    blend+=`{vec4 jj=p41rRead(p41rVertex*${N*2}.0+${set*2}.0),ww=p41rRead(p41rVertex*${N*2}.0+${set*2+1}.0);`;
    for(const c of ['x','y','z','w'])blend+=`if(ww.${c}>0.0){float p=jj.${c}*6.0;vec4 q=p41rDQRead(p),d=p41rDQRead(p+1.0);float s=dot(p41rQ,q)<0.0?-1.0:1.0;p41rQ+=q*(ww.${c}*s);p41rD+=d*(ww.${c}*s);p41rS+=mat4(p41rDQRead(p+2.0),p41rDQRead(p+3.0),p41rDQRead(p+4.0),p41rDQRead(p+5.0))*ww.${c};}`;
    blend+='}';
   }
   blend+='float p41rLen=length(p41rQ);p41rQ/=p41rLen;p41rD/=p41rLen;mat4 p41rSkin=p41rQuatMat(p41rQ);p41rSkin[3].xyz=2.0*p41rMulQ(p41rD,vec4(-p41rQ.xyz,p41rQ.w)).xyz;p41rSkin=p41rAssetWorld*p41rSkin*p41rS;';
   const oldShadow=o.onBeforeShadow;o.userData.p41rPreviousBeforeShadow=oldShadow;o.onBeforeShadow=function(renderer,...args){dqInfo.update(renderer);if(oldShadow)oldShadow.call(this,renderer,...args);};const prev=o.onBeforeRender;o.userData.p41rPreviousBeforeRender=prev;o.onBeforeRender=function(renderer,...args){dqInfo.update(renderer);if(prev)prev.call(this,renderer,...args);};
  }
  const patch=base=>{
   const m=base.clone();m.onBeforeCompile=shader=>{
    if(dqs){shader.uniforms.p41rAssetWorld={value:model.matrixWorld};shader.uniforms.p41rBoneDQ={value:dqInfo.texture};shader.uniforms.p41rBoneSize={value:new THREE.Vector2(dqInfo.width,dqInfo.height)};}
    shader.uniforms.p41rWeights={value:tex};shader.uniforms.p41rTexSize={value:new THREE.Vector2(width,height)};
    shader.vertexShader=decl+shader.vertexShader;
    shader.vertexShader=shader.vertexShader.replace('#include <skinbase_vertex>',blend)
      .replace('#include <skinnormal_vertex>',`mat4 p41rNormal=bindMatrixInverse*p41rSkin*bindMatrix;objectNormal=(p41rNormal*vec4(objectNormal,0.0)).xyz;\n#ifdef USE_TANGENT\nobjectTangent=(p41rNormal*vec4(objectTangent,0.0)).xyz;\n#endif`)
      .replace('#include <skinning_vertex>','transformed=(bindMatrixInverse*p41rSkin*bindMatrix*vec4(transformed,1.0)).xyz;');
   };m.customProgramCacheKey=()=>`P41R_ALL_SKIN_${N}_${dqs}`;m.needsUpdate=true;return m;
  };
  o.userData.p41rSkinMaterial=patch;o.material=Array.isArray(o.material)?o.material.map(patch):patch(o.material);
  o.customDepthMaterial=patch(new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking}));o.customDistanceMaterial=patch(new THREE.MeshDistanceMaterial());
  report.push({mesh:o.name,method:dqs?'DQS':'LBS',vertices:count,sets:N,maxInfluences,maxSumError,textureBytes:data.byteLength});
 });
 model.userData.p41rDispose=()=>{
  ownedTextures.forEach(t=>t.dispose());ownedTextures.clear();
  model.traverse(o=>{if(!o.isMesh)return;o.customDepthMaterial?.dispose();o.customDistanceMaterial?.dispose();if(o.userData.p41rPreviousBeforeRender)o.onBeforeRender=o.userData.p41rPreviousBeforeRender;if(o.userData.p41rPreviousBeforeShadow)o.onBeforeShadow=o.userData.p41rPreviousBeforeShadow;delete o.userData.p41rSkinMaterial;});
 };
 window.__p41rSkinReport=report;return report;
}

export function disposeFullInfluenceSkinning(model){model.userData.p41rDispose?.();delete model.userData.p41rDispose;}
