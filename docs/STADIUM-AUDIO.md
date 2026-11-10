# Stadium, movement and sound module

The scene now includes a curved five-tier stand, 300 instanced spectators,
family-friendly BA/BUM banners, floodlight structures, corner flags and penalty
markings. Spectator heads and bodies each use one instanced draw call. Sunlight
and a cool rim light support the character silhouettes. Flag movement respects
reduced motion. The camera is closer, and the player approaches the ball before
the kick and turns to celebrate after scoring. Detailed foot contact and grounded
dive recovery remain open animation work.

Audio is off by default. The button unlocks AudioContext after a user gesture,
as required on mobile Safari. Original generated melody, ball impact and filtered
crowd-like noise require no external sound files. Volume is adjustable, mute
suspends the audio context and stops the music timer, and hidden pages suspend
audio. No licensed songs or recorded crowd voices are included.

Player name encouragement uses an installed Vietnamese speech synthesis voice
only when available. Availability and pronunciation vary by iPhone/browser. This
is not a recorded crowd chant and cannot yet be promised on every device.

## Verified

- `node tests/audio.cjs`: no AudioContext before gesture; playback unlocks; goal
  effects play; volume works; mute suspends and stops the music timer. PASS.
- `GAME_URL=http://127.0.0.1:4180/ node tests/graphics.cjs`: mobile WebGL and no
  JavaScript errors. PASS. Mobile screenshot visually inspected.
- Live two-session Supabase Realtime-only regression on the new scene: PASS;
  channels joined, synchronized scoring, match/reload/restart/leave verified.
- Four character geometry and motion tests: PASS, approximately 46–49k triangles
  per character after reducing sphere subdivisions and merging rigid parts.
- WebKit was downloaded, but launch is blocked by missing host libraries:
  libgtk-4, libgraphene, libharfbuzz-icu, libmanette, libhyphen and libGLESv2.
  Chromium emulation does not establish real iPhone Safari or GPU performance.

## Remaining quality work

Replace synthesized crowd noise with art-directed, licensed recordings if desired;
verify Vietnamese name calls on physical iPhones; refine stadium materials,
supporters' gestures and facial/cloth/hair rendering. This module is development
work, not a claim of final premium cinematic quality.
