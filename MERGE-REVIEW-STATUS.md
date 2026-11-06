# Merge review follow-up — 2026-11-04

- Read the user-provided `MERGE-README.txt`, `README-CUTE-REACTIVE.txt`, and game screenshot `image-11.png`.
- The README describes a whole-photo basket build and reports 554 passing tests plus Chromium smoke tests. The referenced archive/browser run was not in this workspace, so only the source and tests now present here are claimed as verified.
- Applied the README's intended full, uncropped `basket-original.png` render. The photo's measured inner cavity drives the visible playfield bounds; the top flower/rim stay behind fruit, while only side/bottom wicker receives a foreground pass. The evolution strip is positioned below the full photo.
- Matter engine, fixed timestep, fruit merge/scoring rules, ads and backend code are unchanged. The collision-box dimensions now follow the basket cavity measurements so the art and walls align; this changes the playable area to fit the supplied image.
- The previous screenshot's flower-over-fruit and lower-strip/basket-fit issues are addressed in the source. Full visual confirmation is available in the live Momo Merge preview.
- `android/app/src/main/assets/public/` is synchronized byte-for-byte from `www/`; the original basket photo and new backgrounds are included in both.
- `node --check tests/fm_game.js`: passed. Current workspace harness: **554 passed / 0 failed** (includes five additional photo/cavity/strip regressions, not a copied test result).
- Chromium was not installed in this workspace, so the README's separate browser smoke-test claim was not independently rerun here.


## Play Console min-SDK rejection — 2026-11-04

- Play Console rejected the attempted AAB because its manifest minSdk is 23 and automatic protection requires 24+.
- Updated `android/variables.gradle` to minSdk 24 and `android/app/build.gradle` to versionCode 3 (versionCode 2 had already been attempted).
- Rebuild is required; the existing AAB cannot be repaired. Re-run the signed GitHub Actions workflow and upload the new AAB to the same Internal testing track.

## Comprehensive source audit and corrected candidate — 2026-11-06

- Added `AUDIT-AND-STATUS.md` as the current source of truth; older HANDOFF/workspace notes contain historical/superseded claims.
- Root-cause analysis of broken icons: the earlier partial overlay contained updated `www/index.html` and some generated Android public assets, but did not contain the full current `www/assets/` source tree. Since CI runs `npx cap sync android` from `www/`, a stale/missing `www/assets/icons/` in GitHub could be copied over the Android assets. This strongly matches the user's broken toolbar image screenshots; remote AAB was not directly inspectable here, so the exact remote bundle contents remain unverified.
- The new full-source package includes the complete `www/` runtime assets and an asset-mirror preflight. It also bumps the next Play candidate to code 4/name 1.2 (code 3 is already in Internal testing).
- Removed the portrait orientation lock and blocking rotate overlay to obey the user's no-portrait-only rule. Physics/scoring/backend were not modified.
- Hardened CI: locked `npm ci`, 553 regression checks, Capacitor sync, identity/asset preflight, required signing secrets, and signature verification before artifact upload.
- Locally verified: `npm run check` = **553 passed / 0 failed**; `npm run audit:release` = **PASS**; Android public runtime copy matches `www/` byte-for-byte.
- Not verified: GitHub main equality, AAB content/signature from the user's prior run, Chromium visual test, Android build in this workspace, tester link delivery, and reported phone lag. Do NOT call production-ready until real-device QA passes.
