# BÉ BUM PENALTY 3D — Graphics Overhaul

## Audit

Base: `main`, commit `b9e188f`. The existing single HTML game uses the Supabase
`bebum_penalty_rooms` table, room `ba-bum`, version-based optimistic updates,
Realtime subscriptions and polling. BA and BUM alternate shooting and keeping.
Coins and purchases live in localStorage. There was no 3D engine or asset pipeline.

## Module 1: articulated characters — implemented foundation

`graphics/characters.js` provides BA player, BUM player, BA keeper, BUM keeper.
Shared meshes/materials, facial features, hair, kit colors, keeper gloves,
articulated limbs and idle/kick/save/celebration poses are implemented in code.
`graphics/scene.js` renders the active pair, pitch, goal, shadows and ball flight.
Three.js 0.170.0 is vendored with its MIT license. The HTML dispatches a read-only
`penalty:state` event; the graphics module never writes to Supabase.
The original CSS pitch remains the fallback when WebGL cannot initialize.

This is a procedural character foundation, **not a finished cinematic asset pack**.
The four presets share a base rig; they are not four independently sculpted models.

## Next modules

1. Art direction: review close-up turntables for all four presets, refine silhouettes,
   clothing, facial expressions and anatomy. Produce authored, optimized GLB models
   and textures if the procedural style does not meet the approved target.
2. Animation: anticipation, run-up, foot/ball contact, directional dives, recovery,
   outcome-specific celebration and disappointment. Current save motion is stylized;
   ball contact and full-body ground contact still need refinement.
3. Presentation: stadium, crowd, cinematic cameras, restrained effects and sound.
4. Release validation: real mobile GPU performance, context loss handling,
   two independent devices on Supabase, reconnection and complete matches.
5. Deploy using the repository's verified hosting configuration; confirm the public
   URL and repeat the two-device smoke test before reporting a released game.

## Local verification

Serve the repository root with `python3 -m http.server 4173`, then open
`http://localhost:4173`. Use two separate browser sessions/devices and choose
different BA/BUM roles for a real multiplayer test. This accesses the existing
shared room; coordinate with the family before testing live play.

Automated graphics smoke test (requires Node, Playwright and Chromium):
`node tests/graphics.cjs`. The test blocks Supabase traffic, loads all four rigs,
exercises the two roles and five directions, checks JavaScript errors and saves
`tests/graphics-mobile.png`. It does not establish live multiplayer correctness,
visual quality approval, or physical mobile GPU performance.

## Validation performed

- Chromium/SwiftShader, 390×844: PASS, canvas rendered, four rigs with four limb
  joints each, both role variants and five directions, no page errors.
- Mobile screenshot inspected: pitch, goal, player, keeper and shadows visible.
- Existing Supabase mutation/gameplay code retained; no schema changes.
- No production deployment performed in this module.
