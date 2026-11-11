# Supabase investigation — 2026-11-11

No grants, RLS policies, schema, existing room data or public deployment changed.

## Verified production configuration

- Project URL: `https://zzphvbedtxbhajkpavqp.supabase.co`.
- Publishable key: `sb_publishable_vSE-W8kCzOD5oKwwu6iAKg_nJ_AgucT` (public client key).
- Key SHA-256: `48bf5efc37765edc42c34a4ebbe200510a4ea4e9ec8d7096aa6b232d15300ec5`.
- Pages HTML SHA-256: `6477b3465f5ef71ea7ca2632da3856ff3bf282918e69069b775dc57100acf587`.
- Normal Pages URL, cache-busting URL and `origin/main:index.html` matched byte
  for byte. Pages build is `built` at `c3567aff87ce54adfa251895cecc2247c4d4b705`.
- PR #2 uses the same project URL/key; its newer graphics are not deployed.

## Live evidence

GET `public.bebum_penalty_rooms`, both `limit=0` and the exact game query
`select=*&room_id=eq.ba-bum`, returned HTTP 200 with the public key. The exact
query returned one row; family state/tokens were not printed in diagnostics.
Response `sb-project-ref` matched `zzphvbedtxbhajkpavqp`.

A clean Chromium session on the public URL sent the public key as bearer,
had no saved Auth session, loaded the room and joined Realtime without errors.
The owner also ran the SQL audit's final `SET LOCAL ROLE anon` read and obtained
`ba-bum`. This confirms effective anon access; there is no evidence warranting
additional GRANTs or disabling RLS. Exact catalog flags/policy expressions are
not inferred from successful HTTP requests; they require the audit output.

Two independent sessions on the public assets passed a full match, score/turn
synchronization, one-time reward after reload, restart and leaving. Polling was
disabled; both Realtime channels joined. Simultaneous choice/advance requests
also passed. Only isolated test room `graphics-test-1794361048142` was created
and retained, with owned test roles released.

## Cached Auth mechanism reproduced, iPhone cause not yet confirmed

The production code uses SDK defaults that restore Auth sessions from localStorage.
With a controlled `authenticated` fixture session and mocked API, the actual
Supabase SDK used that stored JWT instead of the publishable key. The mock
returned code `42501`, reproducing the same displayed permission-denied message.
The session remained stored. This proves the mechanism, not the state of the
owner's affected iPhone. A real device report is needed to establish that cause.

`diagnostics.html` is a read-only investigation page on the development branch.
It compares anon credentials with a saved token, if present, and reports role
claims plus detailed API errors without printing tokens or family state.
`tests/diagnostics.cjs` verifies both branches and redaction with fixtures.
The page is not published until the owner approves a merge.
