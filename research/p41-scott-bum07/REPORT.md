# P4.1 — Scott BUM07 prototype: NOT ACCEPTED

Baseline `7c2c676`; separate branch `research/p41-scott-bum07`. Scope: BUM striker only, isolated assets. Scott by Mish7913 /3DMish, CC BY4.0; [full provenance/changes](ATTRIBUTION.md). Original donor preserved byte-for-byte. This report separates a successful export from failed production gates.

## Outcome

A real editable Blender file and experimental GLB exist. The donor gives a more coherent connected face, hands and hair foundation than P3.1R, but this adaptation has **not demonstrated a sufficiently improved final appearance**. Iris striping, collar artifacts, clothing projection and rig limitations make it unsuitable for game replacement. Overall technical acceptance is **FAIL / research only**, and art approval is **pending owner review**. No9/10 claim; no next phase started.

## What changed

Actual duplicate donor geometry was edited: nose/cheek form; hair height/sweep; trousers cut to shorts; existing donor legs revealed; added football socks/cleats/laces/collar/07 geometry. Bandana removed. Eye faces get a separate sclera material plus curved iris/pupil geometry. Yellow/navy fabric has an embedded woven normal tile. Native facial bone samples were converted into morphs with neutral-bind compensation for the runtime's four weights.

This is not a professional manual face sculpt, hair groom or final football garment. The 07 and BUM label objects exist in the Blender/GLB but **fail visibility/projection in the delivered render**. Do not describe the kit as visually complete. Existing donor lacing/neckline geometry was insufficiently rebuilt and remains visible as collar artifacts. Added iris geometry intersects the donor eye surface, causing concentric striping. These are outstanding geometry defects, not lighting issues.

## Technical evidence

| Check | Result | Evidence / practical limit |
|---|---|---|
| Immutable donor | PASS | SHA256 `95b9848fd0c4a1c9ee94a2ae3a9f6136af71c97256ef63ab7a37017470846568` |
| GLB parsing/export | PASS | 103,798 triangles;21 primitives;370 joints;7,167,624bytes (~6.84MiB) |
| Native→GLB facial coordinates | PASS sampled only | `evidence/glb-roundtrip.json`: exact source vertex IDs, decoded skin matrices and sparse morphs; maximum world error1.47236e-6 below1e-4 |
| Actual Blink100 visibility | **FAIL** | Linux WebKit:1 exposed eye pixel at0°,0 at45°; Chromium:0/0. Aggregate FAIL under the strict zero rule. No P3.1R result reused |
| Smile | Animated, visual acceptance pending | Actual GLB samples0/50/100 at0°/45°, native maximum displacement0.052461; mouth corner/teeth still need art review |
| Four-weight body skin | **FAIL acceptance / lossy** | ArmRaise maxerror0.00969271 exceeds0.2%characterheight budget; see all permesh errors |
| Full production topology/UV | **FAIL** | Open garment boundaries,18 non-manifold non-boundary edges,301 zero-area faces,1094 zero-UV-area faces; normal vectors finite, not proof of outward winding |
| Sports animation | NOT PROVIDED | No run/kick/celebration clips exported; source pose library is not a sports animation set |
| Physical iPhone FPS | NOT MEASURED | Linux Chromium/WebKit compatibility evidence cannot establish Safari hardware performance |
| Art target9/10 | NOT ACCEPTED | Owner must review actual renders; currently obvious defects |

GLB roundtrip validates the neutral skeleton plus Blink25/50/75/100 and Smile50/100 snapshots from **this Scott-derived model's native full-influence rig**. It does not prove hidden-surface occlusion, correct eyelid anatomy, arbitrary facial combinations, normals or arbitrary-pose skin equivalence. Blink diagnostic paints the actual exported sclera/iris/pupil red and face green with depth testing; no geometry removed or eye hidden to pass. Raw diagnostics and beauty images are included.

### Skin/370 joints

All370 native joints are retained; **zero joints removed**. Therefore there is no rig-pruning preservation claim. The donor's native mesh has up to16 nonzero weights; subdivision/interpolation raises the measured maximum on the edited body to27. Simply truncating donor weights to4 could discard about38.9%weight on some vertices. The prototype uses full-native neutral evaluation and inverse four-weight skin compensation, and separately bakes native facial snapshots. This preserves sampled neutral/expression coordinates but not arbitrary body motion.

| Nontrivial native pose | Maximum runtime4 deviation (scene units) |
|---|---:|
| Neutral |0.000000492|
| HeadTurn, native displacement~0.6045 |0.00674848|
| ArmRaise via handIK, displacement~0.3165 |0.00969271|
| FootForward, displacement~0.35 |0.00376529|

`build-report.json` contains permesh deviations and nonzero-displacement controls so inactive constraints cannot masquerade as successful tests. Facial production rig still requires bone/morph coordination, combination testing and expression transitions; single pose keys are not a complete facial controller.

### Geometry / collision scope

`geometry-audit.json` inspects all19 editable runtime meshes:1938 boundary edges,18 other non-manifold edges,301 zero-area faces,0 non-finite normals,1094 zero-UV-area faces. Clothing openings alone need not be errors, but label sidewalls collapse during projection and are not production topology. Runtime meshes have UV layers; this does not imply good packing or texel density. The actual rendered Blink ID tests reveal residual exposure. No exhaustive triangle/triangle self-intersection certificate is claimed for face, fingers, kit or arbitrary animations. Those remain unverified.

### Draw budget and iPhone feasibility

Same studio, each character normalized toheight2.2; identical cameras within each view. Full asset triangle totals differ from current frame counts because close cameras cull meshes and the studio adds geometry/draws.

| Full-body frame, Linux WebKit | Rendered triangles incl. studio | Draw calls incl. studio |
|---|---:|---:|
| Original Scott |25,239|11|
| P3.1R |207,572|62|
| Scott-BUM07 prototype |105,336|24|

Prototype asset alone has103,798 triangles/21 material primitives. Compared with original Scott23,701triangles/8primitives, this is a substantial cost increase. The new GLB includes embedded atlas/fabric textures and facial morphs, retains370bones, and has no production LOD or texture compression. Export/load is feasible in the tested desktop runtimes; stable iPhone FPS, memory, heat, context recovery and multiplayer/game integration remain **unverified**. No GPU-string or browser-user-agent result is presented as physical iPhone evidence. No multiplayer behavior was modified or retested as part of isolated art research.

## Deliverables and inspection

Open `gallery.html` locally with the accompanying comparisons folder or `BUM07-P41-Render-Review.pdf`. Five side-by-side views: **original Scott / P3.1R / P4.1**, front,45°,profile,close,fullbody. Raw PNGs from both browsers and Blink0/25/50/75/100 plus Smile0/50/100 at0°/45° are in `evidence/{webkit,chromium}`. No postprocessing of beauty renders beyond scaling/captioning contact sheets. Original Scott is the unchanged P4 probe export; its donor skin-weight export limitation is documented in P4, not treated as a perfect native-deformation reference.

See README for reproducible Blender/browser commands and how to unhide the native rig in the editable workbench. Do not drive native facial bones and baked facial keys simultaneously. Scripts, original blend, exported blend/GLB and native reference arrays are included.

## Next repairs, within P4.1 only

1. Fit iris/pupil to the actual donor globe surface; correct lid closure anatomically and repeat both browser Blink gates. Current1pixel FAIL must not be waived.
2. Rebuild neckline, remove inherited lace geometry, project07 in a consistent evaluated world space, preserve text sidewall depth, and retest kit deformation. Repair degenerate/non-manifold geometry and UVs.
3. Solve body skin budget through measured weight transfer/rig reduction or higher-influence runtime support, then sports poses and actual iPhone profiling. Do not silently prune370joints or claim equivalent deformation from three samples.

No main/Pages/Supabase modification, no PR2 merge, no other character edits and no game model replacement. C/P2/P3.1/P3.1R remain intact. No purchase, subscription, external artist contact or unlicensed asset used. Public hash/main/PR2 state evidence is recorded separately.
