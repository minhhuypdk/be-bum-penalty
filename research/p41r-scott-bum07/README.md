# BUM07 P4.1R — Scott Final Repair Prototype

**Research only; owner has NOT approved art. STOP after this handoff.**

Separate branch `research/p41r-scott-bum07`, exact baseline `ea273ab94459525c34af07f4022d6ef52ff2e904`. No main/Pages/Supabase/game/PR2 changes. Historical C/P2/P3.1/P3.1R/P4.1 and original Scott are preserved.

- [Report](REPORT.md): scoped technical gates, measured budgets and remaining limits.
- [Render review PDF](BUM07-P41R-Render-Review.pdf) / [gallery](gallery.html): **P4.1 left, P4.1R right**, same camera/studio, five views; raw facial and skin test renders included.
- `assets/scott-bum07-p41r-editable.blend`: real editable donor/native/runtime workbench.
- `assets/scott-bum07-p41r-prototype.glb`: real export with embedded textures and facial morphs.
- [Attribution and full change log](ATTRIBUTION.md): Scott by Mish7913, CC BY4.0.

## Important GLB compatibility boundary

Core glTF uses linear skinning. Scott's native Preserve Volume uses DQS. This export retains ALL weights (up to27 influences after subdivision) and370 joints; `extras.P41R_skinning` flags the donor method on each mesh. **The included research adapter is required to reproduce the tested native DQS deformation.** A stock four-weight Three.js loader or a generic viewer that ignores these extras is NOT a validated native-motion consumer. Static geometry/facial morphs can be inspected separately; that is not proof of full rig compatibility. No generic glTF extension support is claimed for the custom extras.

Blender retains the native controls/constraints/drivers. glTF does not carry those editor controls or arbitrary Bendy-Bone segment behavior. The supplied12 skeleton poses and facial snapshots are test fixtures, not a complete sports-animation set or proof of every possible rig motion. No joints were deleted to pass tests.

## Rebuild (Blender4.3.2, from repository root)

Create a fresh output outside the tracked historical asset directories. This pipeline is numerical, with generated geometry, not a manual artist sculpt.

```bash
blender -b research/p41-scott-bum07/source/scott-original.blend --disable-autoexec -P research/p41r-scott-bum07/scripts/build-repair.py -- /tmp/bum07-p41r
blender -b --factory-startup --disable-autoexec -P research/p41r-scott-bum07/scripts/check-glb-roundtrip.py -- /tmp/bum07-p41r
blender -b /tmp/bum07-p41r/scott-bum07-p41r-editable.blend --disable-autoexec -P research/p41r-scott-bum07/scripts/audit-native-deformation.py -- /tmp/bum07-p41r
blender -b /tmp/bum07-p41r/scott-bum07-p41r-editable.blend --disable-autoexec -P research/p41r-scott-bum07/scripts/audit-geometry.py -- /tmp/bum07-p41r
```

Original SHA must match. Voxel/triangulation/export binaries can vary with tool version/order; compare decoded geometry and measured thresholds, not an assumption of byte-identical regenerated files. SHA manifest validates the exact shipped evidence.

## Reproduce isolated browser review

Requires Playwright and working Chromium/WebKit runtimes. Stage makes a disposable copy and patches ONLY that copy's loader/viewer:

```bash
python3 research/p41r-scott-bum07/scripts/stage-review.py /tmp/p41r-review /tmp/bum07-p41r research/p41-scott-bum07/source/scott-original-probe.glb
WEBKIT_PATH=/path/to/working-webkit-launcher node research/p41r-scott-bum07/scripts/browser-review.cjs /tmp/p41r-review /tmp/p41r-webkit webkit
BROWSER_EXECUTABLE=/usr/bin/chromium node research/p41r-scott-bum07/scripts/browser-review.cjs /tmp/p41r-review /tmp/p41r-chromium chromium
```

The adapter preserves all JOINTS_n/WEIGHTS_n via high-precision lookup textures. The staged loader's weight0-only normalization is disabled; DQS is computed in asset space before applying viewer normalization. Beauty, depth, eye-ID and GPU diagnostic shaders use the same skinning adapter. Texture/material cleanup is included. This is NOT patched into the real game.

The review archive includes a `viewer/` staged copy. Serve it over HTTP, for example `python3 -m http.server 8000 --directory viewer`, open `/graphics/showcase.html`, then use GLB import to select `graphics/models/scott-bum-p41r.glb`. The filename triggers the scoped adapter. P4.1 is `graphics/models/scott-bum-p41.glb`. Do not upload this viewer to the production Pages site. Offline `file://` is not a supported module/GLB loading mode.

## Edit the Blender workbench

- `00_SCOTT_ORIGINAL_REFERENCE`: hidden original donor reference. Do not edit/save over the separate source file.
- `01_SCOTT_BUM07_P41`: native edited rig/meshes; unhide native meshes and hide runtime to work on the rig.
- `02_RUNTIME_COMPENSATED`: visible export set, complete weights and native DQS/LBS flags.
- Native body shape keys `P41R_CanthusContact_L/R` have blink-control drivers; `Basis` preserves neutral geometry. Correctives move existing eyelid skin; globes retain the same vertices and positions across Blink.
- Runtime expression keys: `FH_Blink25`, `FH_Blink50`, `FH_Blink75`, `FH_Blink`, `FH_Smile50`, `FH_Smile`. Use the supplied interpolation across snapshots. Keep native facial bones neutral when driving baked facial keys, avoiding double deformation.
- Native blink controls: `Bone.Eyes.Close-Open.L/R` location.z0→0.176827. Bone-control logic and reset are in `build-repair.py:pose`.

No animation production, other characters, next phase, merge or public deployment is authorized by this handoff. Wait for owner image approval.
