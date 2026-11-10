# Compatible 2D recovery version

This branch restores the original CSS/emoji pitch while retaining the verified
Supabase URL-constructor fix, monotonic room versions, sudden-death fairness and
session/input checks from the released 3D baseline. No source assets were deleted;
the 3D modules remain in the repository but are not loaded by index.html.

Two independent browser sessions with real Supabase, polling disabled and
concurrent choices/advance requests passed: score synchronization, winner,
reward once after reload, restart and leaving. Both Realtime channels joined;
no page errors. Test row graphics-test-1794325160689 is retained with test roles
released. No pre-existing family data was changed or deleted.

Recovery: repository Settings → Pages → Deploy from a branch →
backup/2d-compatible → / (root) → Save. Verify the finished Pages build and URL.
To return to 3D, select main again. The exact original is also retained at
backup/pre-3d-b9e188f, but that historical HTML still has the URL naming bug.
