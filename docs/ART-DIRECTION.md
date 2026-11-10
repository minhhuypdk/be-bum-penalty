# Character refinement pass 2

Implemented four variants with authored, smooth contour topology for cheeks,
jaw, cranium, tailored shirt, shorts and boots. BA has swept hair and a mustache;
BUM has softer proportions, tousled hair and a smaller silhouette. Both have
irises, pupils, catchlights, blink motion, eyebrows, nose, smile and ears.
Woven bump detail and cloth sheen add material separation.
Named/numbered jerseys, piping, collars, laces, gloves with fingers and wrist
bands distinguish the four kits. Elbows and knees extend the original limb rig.
The original model source is retained as `graphics/characters-v1.js`.

Open `graphics/review.html` on a local server to inspect any variant, rotate it,
and select idle, kick, save or celebration. The viewer is an art-review page;
it does not replace the multiplayer game or touch Supabase.

## Verification

`node tests/characters.cjs` (default local port 4180) validates all four models,
finite geometry, articulated kick/save poses, open eyes under reduced motion,
and captures four 430×900 screenshots. All four variants were visually inspected.
The original graphics smoke test also passes against this module.

## Quality gate still open

This is a stronger procedural art pass, not approved final cinematic quality.
Remaining: integrate refined skin/cloth/hair materials, improve the facial
silhouette from profile, replace visible intersections with authored topology,
and refine run-up/foot contact/dive recovery. A professionally authored, rigged
GLB asset pipeline may still be needed to meet the final target. Physical iPhone
GPU and Safari validation remains required. No claim of cinematic completion.
