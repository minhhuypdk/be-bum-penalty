# Character Showcase — verified preview

URL: https://be-bum-character-showcase.jovialmesa21.chatgpt.site

Audience: owner-private. Open with the owner's ChatGPT account. No audience
expansion or public sharing was applied. This does not replace the public game.

- Native deployment status: **succeeded**.
- Published version: **1**.
- GitHub source snapshot: `a4e5d7b70e61f163e17b958ba379b3437acd81a9`, PR #2.
- Hosting source snapshot: `9647bd1b03025e277db08133ec89bf7615e8805b`.
- Site: `appgprj_6af3d07f899c819199a4af1ce54673c8`.
- Deployment: `appgdep_6af3da1fc86c81918a0209f2aae94ef7`.
- Saved version: `appgprj_6af3d07f899c819199a4af1ce54673c8~appgver_ab0818efc0188191b9ead1df9652fb63`.

Native saved-version read confirmed the exact hosting commit and archived build
output (31 files, 6,113,280 bytes). The artifact was copied from an explicit source
allowlist; it excludes the game index, Supabase SDK/config, player sessions,
wallets and credentials. Source credentials were passed through hidden stdin,
kept only in process memory/environment, and not stored in Git or deployment.

The deployed artifact contains root `index.html` plus `graphics/showcase.html`,
local modules/vendor dependencies, character portraits, render PNGs and FPS
reports. The root entry rewrites only its local CSS/module paths. Actual source
remains in `minhhuypdk/be-bum-penalty`; hosting is a review snapshot of the same
project, not a replacement game or independent gameplay codebase.

## Verification before publishing

- Chromium: 20 character/motion combinations, camera controls, timeline, local
  GLB/mixer, external-URI blocking, PNG export and mobile layout: PASS.
- WebKit 26.5 (official Playwright binary on Linux with local Debian libraries):
  same functional suite PASS. This is real WebKit, not a physical iPhone test.
- Full `npm test`: all checks PASS, including original game rules, auth/session
  isolation, fallback/context recovery, audio and two-session mock multiplayer.
- Viewer browser runs made zero Supabase requests.
- Final public game HTML checksum remained
  `6477b3465f5ef71ea7ca2632da3856ff3bf282918e69069b775dc57100acf587`.
- GitHub `main` remained `c3567aff87ce54adfa251895cecc2247c4d4b705`.

See `FPS-REPORT.md` for measured software-renderer figures and physical-iPhone
limits. See `../docs/SHOWCASE-ASSET-PIPELINE.md` for professional asset licensing.

PR #2 is still draft. Do not merge without the owner's explicit agreement.
This source/provenance documentation commit changes no deployed app code.
