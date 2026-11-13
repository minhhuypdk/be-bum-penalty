# BUM07 P4.1 — Scott prototype (NOT ACCEPTED)

Research branch `research/p41-scott-bum07`, baseline `7c2c676`. This is a reproducible failed/limited prototype for review, not a replacement for the game. Overall art approval remains with the owner. No 9/10 claim.

## Files

- `source/scott-original.blend`: immutable Scott donor; [source/license/changes](ATTRIBUTION.md).
- `assets/scott-bum07-p41-editable.blend`: native reference, edited native rig/meshes, four-weight runtime shapes.
- `assets/scott-bum07-p41-prototype.glb`: actual experimental export.
- `evidence/`: native reference arrays, binary GLB roundtrip, topology audit, browser results and images.
- `REPORT.md` and `gallery.html`: technical outcome and visual comparisons.

## Reproduce (Blender 4.3.2; run from repository root)

Use a NEW output directory outside tracked source folders. Do not save over donor or historical C/P2/P3.1/P3.1R.

```bash
blender -b research/p41-scott-bum07/source/scott-original.blend --disable-autoexec -P research/p41-scott-bum07/scripts/build-prototype.py -- /tmp/bum07-p41
blender -b /tmp/bum07-p41/scott-bum07-p41-editable.blend --disable-autoexec -P research/p41-scott-bum07/scripts/finalize-export.py -- /tmp/bum07-p41
blender -b --factory-startup --disable-autoexec -P research/p41-scott-bum07/scripts/check-glb-roundtrip.py -- /tmp/bum07-p41
blender -b /tmp/bum07-p41/scott-bum07-p41-editable.blend --disable-autoexec -P research/p41-scott-bum07/scripts/audit-geometry.py -- /tmp/bum07-p41
```

The finalize step is required: exports explicit pose bind, exact vertex provenance and removes unused runtime color channels. Binary Blender export can differ across runs; compare decoded geometry and assertions, not an expectation of byte-identical generated binaries. The immutable donor SHA must match.

Browser evidence uses the *unchanged P4 original-Scott probe GLB* (see P4 dossier) as argument3:

```bash
python3 research/p41-scott-bum07/scripts/stage-review.py /tmp/p41-review /tmp/bum07-p41 /path/to/scott-original-probe.glb
WEBKIT_PATH=/path/to/working-webkit-launcher node research/p41-scott-bum07/scripts/browser-review.cjs /tmp/p41-review /tmp/p41-webkit webkit
BROWSER_EXECUTABLE=/usr/bin/chromium node research/p41-scott-bum07/scripts/browser-review.cjs /tmp/p41-review /tmp/p41-chromium chromium
```

Requires Playwright and working browser runtimes; Linux WebKit is not physical Safari iPhone. Viewer modifications affect the isolated review copy only. It imports local GLBs and must make zero Supabase requests.

## Edit workbench

`00_SCOTT_ORIGINAL_REFERENCE` is hidden donor reference. `01_SCOTT_BUM07_P41` has native edited meshes/370-joint constrained rig; meshes hidden while runtime is displayed. `02_RUNTIME_COMPENSATED` contains visible runtime meshes. Unhide native meshes and hide runtime for native rig work. Do not display both overlapping.

Native blink controls: `Bone.Eyes.Close-Open.L/R` location.z from0 to0.176827. Smile controls and reset logic are in `build-prototype.py:pose`. Runtime facial keys: `FH_Blink25`, `FH_Blink50`, `FH_Blink75`, `FH_Blink`, `FH_Smile50`, `FH_Smile` on meshes. Keep facial skeleton neutral when using baked morphs: driving both doubles deformation. Facial snapshots are not a complete facial animation system.

## Protection

No tracked game code, main, Pages, Supabase, PR2 or other three characters is modified. No sports animation clips or production LOD provided. This branch must not be merged as a game upgrade. Review images first; follow-up repairs require another measured revision, not an acceptance claim.
