# Character Showcase — professional asset route

The current four models are an authored procedural art iteration, not final
cinematic assets. The earlier reference image is not attached in the current
context, so visual parity has not been established. Do not mark that gate passed.

## Sources and rights

1. **Preferred: commission two custom BA/BUM characters and four kits.** Request
   Blender source, skinned GLB 2.0, blend shapes, PBR textures, and written rights
   for modification, commercial game use, rendered images, and browser delivery
   of compiled assets in both the game and this standalone showcase. Keep source
   art private unless the contract explicitly permits public redistribution.
2. **Fab artist assets as a starting point:** https://www.fab.com/ . Check the
   exact product, artist, formats, rig, texture maps and license before purchase.
   The official Standard License permits modification and incorporation into a
   Project but forbids standalone asset redistribution. Do not commit purchased
   GLB/FBX files to this public GitHub repo or assume a standalone viewer is covered.
   Obtain explicit browser/showcase delivery permission when needed.
   Official terms checked: https://www.fab.com/eula .
3. **Adobe Mixamo for animation/retargeting:**
   https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html . The official FAQ
   allows royalty-free character/animation use in personal, commercial and
   non-profit projects including games. Review all applicable restrictions before
   distribution; do not redistribute raw library files as an asset pack. Retarget
   animation onto the approved BA/BUM rig and bake the licensed result as allowed.
4. **Quaternius** https://quaternius.com/ offers useful base/rig prototyping
   resources. Verify the individual pack's license. A low-poly base alone does
   not meet this project's final art target.

No paid assets have been purchased or silently copied. All default render art is
generated from this repository's models. Local GLB import uploads nothing.

## Artist handoff specification

- Four exports: BA player, BA keeper, BUM player, BUM keeper; same underlying
  identity across the two kits. +Y up, +Z forward, meters; neutral floor at Y=0.
- Continuous face/jaw/ears and eyelid topology; iris/cornea layers; detailed swept
  hair forms; UV-mapped cloth normal/roughness; embroidered crest/name/number.
- Skeleton with spine, neck, head, shoulder/elbow/wrist, fingers, hip/knee/ankle.
  Facial blend shapes for blink, smile, focused brows and gentle reaction.
- Five **in-place**, looping or cleanly loopable clips named `Idle`, `Run`, `Kick`,
  `Dive`/`Save`, `Celebrate`/`Victory`. Preserve foot contact, planted support foot,
  anticipation, follow-through, dive recovery and root height. No fake idle
  substitution for missing clips.
- Prefer one high-quality main LOD around 80–140k triangles for this one-character
  showcase, plus an artist-approved gameplay LOD. Optimize hidden faces, duplicate
  materials and texture reuse rather than automatically reducing visual quality.
- Embedded GLB textures; initially 2K skin/kit maps and selective 4K only if the
  close-up warrants it. Audit memory on a physical iPhone before acceptance.

## Implemented integration

`graphics/showcase-gltf.js` uses the official, vendored Three.js GLTFLoader.
The UI accepts a local embedded GLB, normalizes height, applies mesh shadows,
loads the actual AnimationMixer clips, and marks missing clips unavailable.
All four model slots can be replaced independently during a review session.
Changing back disposes that GLB's GPU resources. No model file is uploaded.

External URIs are rejected before parsing. Current adapter accepts uncompressed
GLB 2.0; Draco/Meshopt/KTX2 require a deliberately configured decoder pipeline.
This is stated in the UI instead of silently failing or requesting foreign URLs.

Once an asset is legally approved for web delivery, host it on the same origin
and load it with the existing adapter:

```js
const response = await fetch('./approved/ba-player.glb');
await window.showcase.importGLB(new File(
  [await response.arrayBuffer()], 'ba-player.glb', {type:'model/gltf-binary'}
));
```

Production asset registration and licensing records must be committed before
enabling automatic hosted GLB loading. The current local-file route is working
and tested with an embedded GLB animation fixture; that test triangle is not
included in the preview or presented as character art.
