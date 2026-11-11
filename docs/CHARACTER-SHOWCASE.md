# BÉ BUM Character Showcase

Entry: `graphics/showcase.html`. This is a separate, static character-review room
in PR #2. It does not load the game, Supabase SDK, auth, wallet or room state.
No gameplay/data/permissions change is needed to use or publish this viewer.

## Implemented

- Four independently selectable variants: BA kicker, BA keeper, BUM kicker,
  BUM keeper. Only the selected model is drawn; others are cached lazily.
- OrbitControls: full azimuth orbit, elevation, wheel/pinch zoom, keyboard arrows,
  zoom buttons, full-body framing and a head-following facial close-up.
- Five showcase motions with their own staging: idle, run, kick/ball flight,
  dive/landing/recovery, celebration. Pause/play and scrub the timeline.
- Cinematic studio environment, key/fill/rim lighting, cloth PBR detail, contact
  shadows, PNG canvas export and actual-render character portraits.
- A separate high-detail option for facial spheres, head contours and hair/lip
  curves in the showcase. The game's default character geometry is unchanged.
- Quality defaults to full device DPR up to 3 and 2048px shadows. The viewer
  never automatically lowers quality to make an FPS report look better.
- Local embedded GLB import with actual AnimationMixer clips. Missing clips are
  disabled; external asset URLs are rejected; reset disposes imported resources.

## Browser and art verification

`tests/showcase.cjs` covers all 20 character/action combinations, finite geometry,
rotation/zoom, face/body controls, timeline, PNG export, GLB loading/clip mapping,
external-URI rejection, portrait layout and no Supabase traffic.

The suite passed in Chromium and WebKit. WebKit was run from the official
Playwright binary using dependencies extracted from official Debian packages
into a separate workspace runtime. The browser engine actually launched and
rendered WebGL; this is not a claim of physical iPhone/Safari hardware testing.

`tests/showcase-benchmark.cjs` measures actual rendered frames over at least eight
seconds after warmup. Reports include viewport, DPR, shadow size, GPU, browser,
triangle/draw counts and exact source hashes. Software GPU figures are not iPhone
FPS. Users can run the same measurement with the **Đo FPS** button on their phone.

## Hosting isolation

`scripts/package-showcase.cjs` copies an allowlist into a separate static Site
artifact. It excludes the game index, Supabase SDK/config, sessions and private
runtime data. The source remains `minhhuypdk/be-bum-penalty`, PR #2; the Site is a
review snapshot, not another game or a replacement repository. The game on
GitHub Pages and `main` remain unchanged. The preview is owner-private by default.

## Quality gate

The earlier supplied reference image is absent from this conversation's visible
attachments. No claim of visual parity or final cinematic approval is made.
These are detailed procedural art candidates, not final approved character assets.
See `SHOWCASE-ASSET-PIPELINE.md` for legitimate professional asset sources,
contract requirements and the working GLB integration path. Final acceptance
still needs the reference, art review and physical iPhone performance checks.
