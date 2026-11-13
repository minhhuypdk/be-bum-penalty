# BA/BUM session lifecycle — verified fixes, 2026-11-11

The public Pages deployment and Supabase permissions remain unchanged. All fixes
in this document belong to the unmerged development PR #2.

## Defects reproduced on public code

With two/three independent browser sessions on an isolated room and real
Supabase, polling disabled:

- A failed claim of an occupied role still saved that role in sessionStorage.
- If the release PATCH failed, `leave()` had already forgotten the local role,
  although the server still held the token. The user could not retry normally.
- A replacement browser session could not resume a role left by its old tab.

The baseline test verified these defects without touching the family room.
Room `session-test-1794361394828` is retained; test roles were released.

## Fixes

Only save the selected role after the server confirms the claim. Keep local
ownership when a release fails, allowing retry. Refresh local state even when
an optimistic mutation correctly decides it should not change the room.

After a successful claim, store a recovery marker scoped to project/room/role on
the same device. A new tab/session can explicitly select "Tiếp tục BA/BUM trên
máy này" if that marker still matches the server's role token. The new session
rotates ownership to its own token, preserving turn, shots, history and scores.
The old token can no longer submit choices. A device without a matching marker
cannot use this recovery path. A single token cannot hold both roles.

No lease, automatic kicking, schema migration, extra privileges, policy changes
or deletion is introduced. Recovery requires a role previously saved by the new
version and retained device storage. A legacy abandoned role or erased storage
cannot be silently reclaimed; the game never takes a different device's role
just because a browser tab seems absent.

## Auth isolation

This account-free game now uses an in-memory Auth client with persistence,
token auto-refresh and URL session detection disabled. Existing login records
from the same origin remain untouched. A controlled SDK test reproduced the
old default choosing a stored authenticated JWT and displaying 42501; the new
client uses the public key and leaves that saved session byte-for-byte intact.
This mechanism is proven, but the owner's original iPhone error is not attributed
to it without the affected-device report. Effective anon access is confirmed by
the owner's SQL test and current HTTP tests, so no GRANT/RLS change is justified.

## Verified against the new implementation

`tests/session-lifecycle.cjs` with real Supabase and no polling passed:

- two devices simultaneously claim BA: exactly one wins;
- an occupied role cannot be taken by another device;
- failed join does not save a selected role;
- reload preserves token/ownership;
- failed release retains ownership; retry frees the role;
- another device can claim a role after successful release;
- a replacement session with the matching local marker resumes the role;
- the old session cannot shoot or release the new owner after transfer;
- a stale recovery marker cannot take the role back;
- recovery preserves the match and score;
- no page errors.

Successful test room: `session-test-1794361637618`; retained with test roles released.
No existing room or user progress was changed or deleted.
