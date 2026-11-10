# BÉ BUM PENALTY 3D — session handoff, 2026-11-10

## Released and verified

Game: https://minhhuypdk.github.io/be-bum-penalty/

PR #1 merged with commit `c3567aff87ce54adfa251895cecc2247c4d4b705`.
GitHub Pages reports build `built` for that exact commit. Two independent browser
sessions on the public URL passed a full six-turn game, synchronized scoring,
winner, reward-once after reload, restart and leaving, with polling disabled.
Both Supabase Realtime channels reported `joined`; no page errors.

The deployed fixes cover the browser URL constructor collision, stale room
updates, equal-attempt sudden death and session ownership/input validation.
Original `b968f65` remains in history. Exact historical branch: `backup/pre-3d-b9e188f`.
Tested recovery branch: `backup/2d-compatible`, commit `068baf5`.
It retains the old 2D pitch plus the connection/gameplay fixes; its live Realtime
and simultaneous-action test passed. Choose it in Pages settings to recover.

## Development branch: graphics/cinematic-pass

- `fcc1125`: four smooth character variants, faces, hair, kits and articulated
  elbows/knees; character review viewer and mobile screenshots.
- `56b8145`: curved stadium, 300 instanced spectators, banners, flags, light
  structures, closer camera, approach and goal celebration staging.
- `aee1ae2`: original generated opt-in music/effects and optional Vietnamese voice
  encouragement; volume/mute and stable direction controls.
- `433a0ec`: woven fabric bump/sheen and optimized character verification.
- Test tooling and WebGL context-loss recovery are committed separately after
  final verification. The development render loop is capped at 30 frames/second
  with 512px mobile shadow maps to reduce load; real iPhone profiling is pending. `npm test` runs the suite without touching live Supabase.

The new development scene also passed a separate two-session Supabase
Realtime-only test, without polling. The public game deliberately remains on
the verified baseline while the more detailed graphics await physical iPhone
performance and art-quality review.

## Data preservation

No existing room, scores, schema or family progress was deleted. Tests create
only isolated `graphics-test-*` rows. Live rows retained in this session:

- `graphics-test-1794323311365` — initial live test, delete denied; retained.
- `graphics-test-1794323490108` — strict local Realtime test.
- `graphics-test-1794323852322` — deployed Pages Realtime test.
- `graphics-test-1794324481203` — development graphics Realtime test.
- `graphics-test-1794325160689` — compatible 2D recovery, concurrent Realtime test.

Later live tests return roles they own without deleting the row. The earliest
test row may still contain its test-session BA token, which has no effect on
the separate family room `ba-bum`. No extra DELETE grant is required.

## Verification and limits

- Graphics and all four models: PASS in Chromium, mobile 390×844 / 430×900.
- Character topology finite, knee/elbow poses, reduced motion: PASS.
- Audio unlock, no autoplay before gesture, volume and mute: PASS.
- Regulation/sudden-death, stale state, session/input validation: PASS.
- Simultaneous choices and simultaneous next-turn requests with mock REST: PASS.
- Intentional WebGL loss shows the CSS fallback and restores the canvas: PASS.
- WebKit download succeeded, but launch is blocked by missing host libraries.
  Chromium emulation is not a physical iPhone/Safari test.
- Premium cinematic quality is still incomplete: facial joins, profile shapes,
  materials and motion need further art direction; custom GLB assets may be needed.
- Vietnamese speech depends on device voices; recorded chants are not included.

## Next three priorities

1. Validate the public baseline on two physical iPhones: BA/BUM, reconnect,
   synchronized score/turn, full match, long sessions and battery/thermal behavior.
2. Review the development characters close-up and in motion; refine face/profile,
   skin/hair/cloth, run-up, foot contact and dive/ground recovery before art approval.
3. Profile and tune the development stadium/character scene on iPhone Safari,
   verify sound/voice unlock, then release the next graphics PR after checks pass.
