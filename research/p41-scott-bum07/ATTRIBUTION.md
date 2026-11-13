# Scott → BUM07 P4.1 attribution / changes

Original **Scott** by **Mish7913 (3DMish)**.
- Author release: https://blenderartists.org/t/boy-scott-free-3d-character-mish7913/1510925
- Author source: https://projects.blender.org/3DMish/M7s-Assets-Library/raw/branch/main/data/characters/scott-3d-model.blend
- License: **Creative Commons Attribution 4.0 International**: https://creativecommons.org/licenses/by/4.0/
- Legal text: https://creativecommons.org/licenses/by/4.0/legalcode
- Preserved donor: `source/scott-original.blend`, SHA256 `95b9848fd0c4a1c9ee94a2ae3a9f6136af71c97256ef63ab7a37017470846568`.

CC BY 4.0 allows game use, adaptation and redistribution, including commercial use, subject to attribution, license link, indication of changes and no implication of endorsement. Do not impose legal/technical restrictions on recipients' licensed rights. No endorsement by Mish7913 is implied. This dossier records the author's linked license; it is not a claim to additional third-party trademark rights.

Changes by the BÉ BUM PENALTY research pipeline, November 2026:
- Duplicate donor mesh/rig; remove bandana from duplicate only. Retain original bytes and native rig reference.
- Reshape nose/cheeks and hair silhouette; subdivide selected donor surfaces once. These are procedural edits, not a professional manual sculpt or an independently authored character.
- Split sclera material; add curved brown iris and pupil geometry. Current exported eyes have visible striping defects.
- Replace duplicate clothing materials with yellow/navy woven-normal fabric; cut trousers to shorts; reveal existing donor legs; add socks, collar, projected number07/BUM label, boot soles, cleats and laces. Current number/badge projection and collar fail visual acceptance.
- Retain 370 joints. Compensate neutral bind for four runtime weights; bake full native facial rig samples into six facial morph snapshots. Non-neutral body deformation is NOT lossless.
- Export experimental GLB, keep native editable controls plus runtime shapes in new Blender workbench. No source texture or donor source file overwritten.

The inherited donor geometry, UVs, atlas, rig and their modifications remain credited to Mish7913 under CC BY 4.0. Retain this file with redistributed Blender/GLB derivatives. New scripts are research tooling within this repository. Comparison images also show earlier project P3.1R; their presence does not change the donor's license.
