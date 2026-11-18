# Scott → BUM07 P4.1 attribution / changes

Original **Scott** by **Mish7913 (3DMish)**.
- Author release: https://blenderartists.org/t/boy-scott-free-3d-character-mish7913/1510925
- Author source: https://projects.blender.org/3DMish/M7s-Assets-Library/raw/branch/main/data/characters/scott-3d-model.blend
- License: **Creative Commons Attribution 4.0 International**: https://creativecommons.org/licenses/by/4.0/
- Legal text: https://creativecommons.org/licenses/by/4.0/legalcode
- Preserved donor: `../p41-scott-bum07/source/scott-original.blend`, SHA256 `95b9848fd0c4a1c9ee94a2ae3a9f6136af71c97256ef63ab7a37017470846568`.

CC BY 4.0 allows game use, adaptation and redistribution, including commercial use, subject to attribution, license link, indication of changes and no implication of endorsement. Do not impose legal/technical restrictions on recipients' licensed rights. No endorsement by Mish7913 is implied. This dossier records the author's linked license; it is not a claim to additional third-party trademark rights.

Changes by the BÉ BUM PENALTY research pipeline, November 2026:
- Duplicate donor mesh/rig; remove bandana from duplicate only. Retain original bytes and native rig reference.
- Reshape nose/cheeks and hair silhouette; subdivide selected donor surfaces once. These are procedural edits, not a professional manual sculpt or an independently authored character.
- Split sclera material; add curved brown iris and pupil geometry. Current exported eyes have visible striping defects.
- Replace duplicate clothing materials with yellow/navy woven-normal fabric; cut trousers to shorts; reveal existing donor legs; add socks, collar, projected number07/BUM label, boot soles, cleats and laces. Current number/badge projection and collar fail visual acceptance.
- Retain 370 joints. Compensate neutral bind for four runtime weights; bake full native facial rig samples into six facial morph snapshots. Non-neutral body deformation is NOT lossless.
- Export experimental GLB, keep native editable controls plus runtime shapes in new Blender workbench. No source texture or donor source file overwritten.

The inherited donor geometry, UVs, atlas, rig and their modifications remain credited to Mish7913 under CC BY 4.0. Retain this file with redistributed Blender/GLB derivatives. New scripts are research tooling within this repository. Comparison images also show earlier project P3.1R; their presence does not change the donor's license.

## Additional P4.1R modifications — 2026-11-18

P4.1R is derived from project commit `ea273ab94459525c34af07f4022d6ef52ff2e904`. The preceding P4.1 changes remain documented above; defects stated there describe P4.1, not the repaired export. Original Scott is still at `../p41-scott-bum07/source/scott-original.blend`, unchanged.

- Replace overlapping iris/pupil patches with original procedural brown-iris/sclera artwork on the **same donor eye surface**; ellipsoid-aware UV mapping. No eye visibility toggle or eye shrink.
- Existing inner-canthus eyelid mesh gets two editable, driver-controlled contact correctives. Face expressions remain native Scott rig samples, baked into runtime facial keys.
- Reconstruct softened hair and boot shells with solidification/voxel remeshing, smooth/decimate, and transfer **all** original nearby weights. Repair normals and triangulation, regenerate nondegenerate material-tile UVs.
- Remove the edited copy of Scott's original laced shirt entirely; build football shirt from donor torso topology. New continuous neck band, correct world-space number07/BUM projections, real label depth, welded caps, capped shoe laces and body/waistband clearance. Donor source garment is retained in the original reference.
- Keep all370 joints and native Preserve Volume modifiers. Export all influence sets, with per-mesh `P41R_skinning` extras; isolated research adapter implements full-weight DQS/LBS. Blender's constraints/drivers/Bendy Bones are not a native glTF feature.
- New independent CPU/GLB checks and actual browser GPU float readbacks; no ownership approval or quality9/10 claim.

The iris/fabric artwork and pipeline scripts are created for this prototype. The mathematical skinning code is independently expressed using normalized dual-quaternion blending and affine scale residuals; see Kavan et al., *Skinning with Dual Quaternions* (2007), https://users.cs.utah.edu/~ladislav/kavan07skinning/kavan07skinning.pdf . No third-party shader implementation is copied. Blender and Three.js remain their respective upstream tools; their binaries are not redistributed in the asset-only bundle.

Scott-derived mesh, atlas, rig and modifications remain attributed to **Mish7913 /3DMish, CC BY4.0**. Keep attribution, license link and change descriptions with redistributed derivatives. No endorsement is implied. This research does not claim rights to any unrelated asset or trademark.
