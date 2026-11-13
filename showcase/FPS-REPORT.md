# Character Showcase — measured FPS

All measurements below use Linux software rendering, **not physical iPhone hardware**.
Quality preset: Cinema, 2048px shadows, no automatic quality reduction.
Each row contains at least eight seconds after warmup. Rendered frame counts are intentionally disclosed.

| Engine | Profile | Pixels | Frames / seconds | FPS | P95 frame time |
|---|---|---|---|---|---|
| chromium | desktop-software | 1012×666 | 8 / 9.8 | 0.82 | 2383.3 ms |
| chromium | portrait-retina-emulation | 1170×1320 | 7 / 9.283 | 0.75 | 2349.9 ms |
| webkit | desktop-software | 1012×657 | 38 / 8.053 | 4.72 | 243 ms |
| webkit | portrait-retina-emulation | 1170×1320 | 21 / 8.461 | 2.48 | 493 ms |

These low software-GPU figures are real and are not advertised as smooth iPhone performance.
WebKit reports a masked `Apple GPU` string even though this test ran in Linux WPE with software rendering forced.
The renderer handles roughly 103k triangles and 50 draw calls for one high-detail character and studio.
Physical Safari/iPhone FPS remains unverified. Open the private preview on the phone and use **Đo FPS** to obtain a device-local report.
The report records viewport, DPR, shadow size, animation, browser/GPU strings and source-file SHA-256 hashes.
The original reference image is still required to evaluate visual parity; FPS alone does not establish art quality.
