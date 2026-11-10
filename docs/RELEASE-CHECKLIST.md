# Test release gate

GitHub Pages currently serves `main` at `/`, over HTTPS:
https://minhhuypdk.github.io/be-bum-penalty/

Old version: `b9e188fd1a51dcec499ca3f0f8c0bb067fb1ba9f`.
Remote recovery branch: `backup/pre-3d-b9e188f`.
Original 3D commit retained: `b968f6590724bc4846a3b113a1ce05c2670ae5b0`.

## Issues found and repaired before release

With the current Supabase SDK, the original top-level `const URL` shadows the
browser URL constructor. Rename it to `SUPABASE_URL` before creating the client.
This fix does not change the endpoint or the game protocol.

After that fix, a live request to the game's table fails with HTTP 401,
Postgres code `42501`, and a hint to grant SELECT to `anon`.
The game uses the publishable key without login, so its database role is `anon`.
The owner granted SELECT/INSERT/UPDATE to anon. Live tests now pass.

Project owner: in Supabase SQL Editor for `zzphvbedtxbhajkpavqp`, run:

```sql
GRANT SELECT, INSERT, UPDATE ON TABLE public.bebum_penalty_rooms TO anon;
```

This restores the privileges needed by the existing shared, account-free game.
It does not disable RLS, create policies, or grant DELETE. Existing RLS policies
still apply. If requests remain blocked, inspect the policies before changing them:

```sql
SELECT policyname, roles, cmd, qual, with_check
FROM pg_policies
WHERE schemaname = 'public' AND tablename = 'bebum_penalty_rooms';
```

## Validation commands

- `python3 -m http.server 4173`
- `node tests/graphics.cjs`
- Download the same SDK used by the page to `/tmp/bebum-supabase.min.js`:
  `curl -fL https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js -o /tmp/bebum-supabase.min.js`
- `MOCK_SUPABASE=1 node tests/multiplayer.cjs`: two independent browser sessions,
  real Supabase SDK with mock REST. This is a regression test, not proof of live
  Realtime connectivity.
- `node tests/multiplayer.cjs`: live integration against a unique `graphics-test-*`
  room. Requires policies permitting that test room. Never accesses room `ba-bum`.
  Live tests retain their own test row and release owned roles; no DELETE privilege
  is needed. Existing family data is never changed.
- `GAME_URL=https://minhhuypdk.github.io/be-bum-penalty/ node tests/multiplayer.cjs`
  repeats the integration against the deployed assets after release.

## Deployment and recovery

Do not merge/deploy while live multiplayer checks fail. After they pass, merge
PR #1 with a merge commit, preserving the original 3D commit in history. Pages
will build from `main`; verify the build commit, HTML and JS asset responses,
WebGL rendering and multiplayer on the public URL.

To restore the old site without rewriting history, change Settings → Pages →
Deploy from a branch to `backup/pre-3d-b9e188f`, folder `/ (root)`, and save.
Wait for Pages to finish and verify the URL. Alternatively revert the release
merge through a new PR and deploy `main` again. Database grants do not repair
the URL constructor bug in the old HTML.

Final acceptance: open the public URL on two iPhones, BA on one and BUM on the
other; check goal/save, alternating roles, synchronized scores and next turn.
The procedural character foundation is a test asset, not the final cinematic
quality target. Continue authored character refinement after this gate passes.

## Verified results before deployment

- Graphics smoke test: PASS in Chromium/SwiftShader at 390×844.
- Two-session regression with mock REST and real Supabase SDK: PASS for
  alternating roles, goal/save, score synchronization, winner, one-time reward
  after reload, restart and leaving. No page errors.
- Live Supabase: PASS with two independent sessions; both channels joined.
- Strict Realtime-only test with 2500ms polling disabled: PASS through six turns,
  winner, reward after reload, restart and leaving. No page errors.
- Rules: PASS for sudden-death fairness, rejecting stale room versions, rejecting
  invalid and duplicate choices, and checking session ownership.
- Test rooms retained: `graphics-test-1794323311365` (first run) and
  `graphics-test-1794323490108` (strict Realtime run). No pre-existing data deleted.
- Version acceptance is monotonic, preventing late fetch responses from rolling
  score or turn backwards. Sudden death waits for an equal number of attempts.
- Physical iPhone Safari and GPU testing remain for the owner after deployment.
