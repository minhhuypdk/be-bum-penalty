# Graphics Overhaul: free professional mesh review

This module introduces a real licensed Blender Studio model and an isolated A/B art review. **It does not deliver four finished BA/BUM models or establish a 9/10 art score.** No gameplay, room data, Supabase permissions, main branch or public game deployment is changed in this module.

## Selected source and rights

Selected: [Snow v3, Blender Studio](https://studio.blender.org/characters/snow/v3/), **CC-BY 4.0**, attribution **Snow Rig © Blender Foundation | studio.blender.org**. Modification and redistribution are permitted with attribution, license link and disclosure of changes. `graphics/models/snow/manifest.json` records the exact official download and ZIP SHA-256. `CREDITS.md` accompanies both GLBs and is linked in the viewer. Exported Snow PNGs carry attribution. No paid asset was acquired. This follows the user's preference for free assets with modification and redistribution rights.

The current Snow v4 download returned an origin maintenance/503 page; official v3 downloaded successfully. It provides authored continuous facial anatomy, sculpted hair, fingers, cloth folds, UVs and textures. Its identity, age, body proportions and casual clothing do **not** equal the approved BA/BUM designs.

Rejected as final character sources: Grab3D teen/toddler (publisher says CC0 but also discloses AI-generated mesh and automatic walk/run-only rig without facial/finger control; identities and quality unapproved). Generic paid listings were not purchased. No right to redistribute paid source assets in this public repository has been assumed.

## Real implementation

- Existing four BA/BUM models remain the default A version, with all five existing motions.
- B selects a clearly labelled **Snow art-base candidate**, not a renamed BA/BUM character. The angle, focus and lighting remain comparable. GLB import on the current device remains available separately.
- Two manually selected geometry LODs. The mobile level does not activate silently. Only one candidate LOD remains allocated after switching.
- PBR conversion uses original textures, selects the render UV rather than the tattoo helper UV, and splits skin UDIM tiles into self-contained materials. Geometry is not assembled from new Three.js primitive body parts.
- The evaluated bind mesh retains skin weights. A clean weighted skeleton reconstructs the main anatomical chains. A held standing arm pose and a slight head turn form a minimal real `Idle` clip.
- No CloudRig script, driver, Python text or executable code is embedded in GLB. Blender was invoked with `--disable-autoexec`.
- Original rig controls, B-bone behavior and Cycles facial correction/shading are **not** reproduced completely. Run, Kick, Save and Celebrate are disabled for Snow. The Idle review clip is not a finished natural acting performance.
- A/B load failures preserve A; stale requests cannot override a newer selection. Local GLB files do not upload anywhere. The viewer makes no Supabase request.

## Asset budgets (actual shipped GLBs)

| Level | GLB bytes | Mesh triangles | Render primitives | Estimated RGBA8 textures with mipmaps |
| --- | ---: | ---: | ---: | ---: |
| Portrait | 19,414,844 | 423,990 | 21 | 121.33 MiB |
| Mobile | 5,580,928 | 105,971 | 21 | 50.33 MiB |

Both exports contain one Idle clip and a skin with 278 glTF joints including the generated armature root. Runtime adds the floor/platform/trim: observed 24 draw calls. Portrait face/hair/iris albedo reaches 2K; clothing/body albedo <=1K. Normal maps use half the selected maximum, scalar maps one quarter. Estimates exclude geometry, shadows, environment, browser copies and other allocations. They are not measured device GPU memory. GPU texture compression (KTX2) is a remaining optimization, not implemented or implied by JPEG download size.

## Reproduce and review

Download the official source ZIP recorded in the manifest, verify its SHA-256 and extract it outside the game repository. Do not enable embedded scripts.

```sh
blender -b --disable-autoexec /absolute/source/snow_v03.blend -P scripts/assets/export-snow.py -- /absolute/export
python3 scripts/assets/audit-glb.py
npm test
```

The export script produces both self-contained GLBs and a build report. Copy them to `graphics/models/snow/` before the audit. Blender 4.3.2 was used. Source .blend/107 MB ZIP are not shipped to browsers or committed.

Open `graphics/showcase.html?version=snow&lod=portrait`, choose A/B, compare face/body and rotate, then choose Mobile. B's missing sport clips must remain disabled. Switching A must restore all four original identities and five motions. No live room writes are needed for any art test.

`tests/showcase-asset.cjs` checks the real licensed GLBs, finite geometry, skin animation pixels, A/B retention, actual triangle reduction, unsupported clips, mobile layout, load race/failure handling and zero Supabase requests. `tests/showcase-benchmark.cjs` accepts `SHOWCASE_ASSET=snow`; `tests/showcase-record.cjs` records the actual running WebKit viewer. Browser recordings are not FPS evidence. FPS reports carry asset/source hashes and hardware limits.

## Art gate still open

Missing: distinct BA adult and BUM child sculpts against the supplied visual reference; appropriate eye/eyelid proportions and expressive facial morphs; football kits and keeper gloves; sport footwear; fingers/feet and corrective deformation validated under all five sports actions; natural kick/dive/celebration animation; physical Safari iPhone measurements. No source matching all those approved requirements has been found ready-made and free.

The practical free route is to author those modifications in Blender from this redistributable base, retaining original credit and marking all changes. Snow is an inspection base, not an acceptance shortcut. Do not merge PR #2 or replace the public game's characters before art approval and multiplayer regression checks.

## Verified private publication

Native Sites publication **succeeded**, saved version **2**. Same owner-private project and URL; no new project or audience change:

https://be-bum-character-showcase.jovialmesa21.chatgpt.site/?version=snow&lod=portrait

- Published GitHub code/evidence: `9827450091ec7080d5f3ff1f8edace1310060bee`.
- Exact pushed hosting source: `6d6eb028facc96e4c668d100fafdac1d772a0c85`.
- Hosting saved version and deployment IDs: `showcase/preview-site.json`.
- Root HTML asset/credit links and every allowlisted file were checked against the repository bytes before publication. The packaged mirror contains only the viewer, vendor files, licensed GLBs, credits and render evidence.
- Version 1 remains saved; `rollback_version` in the same JSON preserves its source/version/deployment identifiers. Rollback can redeploy that saved owner-private version without touching GitHub main or Supabase.
- The native successful publication verifies hosting. Browser QA and captures were performed on the identical application source in the GitHub workspace. No extra authenticated production-browser check or physical iPhone test is claimed.
- Remote main remains `c3567aff87ce54adfa251895cecc2247c4d4b705`; public game HTML SHA-256 remains `6477b3465f5ef71ea7ca2632da3856ff3bf282918e69069b775dc57100acf587`.

Three next art priorities: author distinct BA/BUM face/body sculpts from the free licensed source; create football/keeper outfits and corrective sports animation; add compressed-texture delivery and validate on physical Safari iPhones. These remain incomplete and are not hidden behind the source model's professional provenance.
