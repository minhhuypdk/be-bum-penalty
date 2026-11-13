# Snow A/B art-base review — evidence

This folder contains **real Three.js/WebKit/Chromium renders**, not image-generated concept art. Snow is a licensed base asset, not the final four BA/BUM characters and not a verified 9/10 result.

- `snow-portrait-full.png`, `snow-portrait-face.png`: real high-detail GLB, original source anatomy/hair, converted PBR and held standing pose.
- `baseline-face.png`: preserved prior BA/BUM source for A/B.
- `snow-idle-start.png`, `snow-idle-motion.png`: sampled frames of the actual skinned Idle head turn; automated test verifies changed pixels. Other sports clips do not exist in the Snow candidate.
- `snow-mobile-face.png`, `snow-mobile-ui.png`: actual mobile LOD and 390 × 844 browser viewport. These are not photographs or physical iPhone measurements.
- `asset-functional-chromium.json`, `webkit/asset-functional-webkit.json`: real asset tests, two LODs, baseline retention, stale/failing load checks and zero Supabase requests.
- `fps-webkit.json`, `fps-chromium.json`: >=8-second runtime measurements, source and asset hashes, actual viewport/DPR/renderer information. Software Linux measurements, **not physical iPhone FPS**. WebKit's masked Apple GPU string does not identify physical Apple hardware in this executor.
- `snow-idle-runtime.webm`, `motion-recording.json`: recording of the actual running WebKit viewer, including startup and face/body framing. Movie playback FPS is not render FPS.

Attribution: **Snow Rig © Blender Foundation | studio.blender.org**, [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: glTF PBR/UV conversion, evaluated bind mesh, reconstructed review skin, standing arm pose, slight Idle head turn, LOD/texture sizing. See `graphics/models/snow/manifest.json`, `CREDITS.md`, `glb-audit.json` and `docs/GRAPHICS-OVERHAUL-ASSET-REVIEW.md`.

No current module edits the public game, multiplayer source, Supabase rights or data. The full regression suite uses a mock room for two independent BA/BUM sessions. Its test-row cleanup affects the mock only, not Supabase.

## Recorded FPS on this Linux executor

| Engine | Portrait LOD desktop | Mobile LOD, 390-wide / DPR 3 |
| --- | ---: | ---: |
| webkit | 1.85 FPS (15 intervals) | 2.16 FPS (18 intervals) |
| chromium | 0.36 FPS (3 intervals) | 0.63 FPS (6 intervals) |

Each sample covers >=8 seconds after warmup. Small sample counts reflect very slow software rendering and are not a reliable predictor of phone hardware. No smoothness or iPhone FPS claim is made. Measured runtime draws 24 calls: 425,528 portrait / 107,509 mobile triangles including the studio floor/platform.

Validation: the full npm regression suite passed with mock REST and no live DB writes. A/B asset tests passed on Chromium and WebKit. A subsequent fix refreshes renderer statistics before collecting a report; both final benchmark runs assert candidate geometry and 24 calls, and the source/asset hashes match the committed runtime files. The runtime video was verified as a 19.12-second WebM with ffprobe.
