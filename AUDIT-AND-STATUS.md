# Momo Merge — mukammal source audit aur project status

**Audit tareekh:** 6 November 2026  
**Source ka snapshot:** `/home/user/fruit-merge/` (is workspace mein maujood project)  
**Agla candidate Android version:** `versionCode 4`, `versionName 1.2`  
**Play par abhi tak nazar aane wala release:** version code 3, Internal testing  
**Faisla:** source-level checks pass hain, lekin app ko abhi “bug-free” ya production-ready kehna durust nahin. Owner ke Android screenshots mein broken game icons aur noticeable lag report hua hai. In-device visual/performance fix abhi verify nahin hui.

---

## 1. Sab se pehle: sachchi scope aur limitations

Yeh audit **workspace ke local source** ka hai. Is assistant ke paas private GitHub repository, us ke `main` branch, Play Console, ya uploaded AAB ka direct access nahin. User ne AAB attach karne ki koshish ki thi, lekin chat uploader `.aab` ko reject karta hai; is liye remote AAB ko khol kar us ke andar ke files compare nahin kiye ja sake.

GitHub Actions ke screenshots mein `main` par commit `3ca48d1` aur successful runs #8/#9 nazar aaye thay. Green check ka matlab workflow complete hua; woh yeh prove nahin karta ke remote source local source jaisa tha, har art file AAB mein thi, game phone par sahi dikha, ya performance theek thi.

Is liye neeche teen qisam ke natayij alag rakhe gaye hain:

- **Local source par verified:** command se check/test kiya.
- **Owner ke phone par report/visible:** screenshots ya user ke gameplay test se pata chala.
- **Remote/Play par unverified:** GitHub/AAB/Console access na hone ki wajah se independently confirm nahin hua.

**“Zero bugs” ki guarantee nahin di ja sakti.** 553 headless checks pass hue, lekin actual phone par reported defects maujood hain. Is package ko **audited source candidate** samjho, certified bug-free release nahin.

---

## 2. Release aur phone test ki current halat

### Play Console (owner ke screenshots se)

- Package: `com.isstudios.momomerge`.
- Console ne version `3 (1.1)`, API levels `24+`, target SDK `36` accept karke Internal testing release ko **Available to internal testers** dikhaya.
- Yeh **Internal testing** hai; Production rollout nahin hua. “Promote release” press nahin karna.
- Tester list `Saqib` mein 5 users dikh rahi thi. Kam az kam do accounts ne `App not available / account hasn't yet been invited` error dekha. Baad mein ek phone par game chalne ke screenshots mile. Tester invite propagation/account eligibility ko abhi final pass nahin maana gaya.
- Console ke upar **Declare your trader status** banner pending tha; declaration owner ko sachai ke mutabiq khud karni hai.

### Android par user-reported QA failures (release blocker)

User ke diye hue phone screenshots/video ke mutabiq:

1. Game version unki umeed ke mutabiq latest nahin lag rahi thi / kuch cheezen missing thin.
2. Gameplay UI mein kai image/icon boxes broken image ki tarah render hue.
3. Fruit drop, collisions, physics aur overall play feel laggy tha.

Yeh defects **abhi resolve/phone par re-test nahin hue**. Jab tak fixed source ka naya internal build isi device par check nahin hota, testers ko link aage na bhejo aur Production par promote na karo.

---

## 3. Missing icons ke liye mila hua concrete cause

Pehle diya gaya `Momo-Merge-GitHub-Overlay.zip` ek **partial overlay** tha, complete source archive nahin. Us ZIP ki file list mein:

- `www/index.html` update tha aur us mein naye `assets/icons/*.png` paths istemal ho rahe thay;
- `www/assets/` ke andar sirf kuch background/basket files thin; `www/assets/icons/` ki mukammal folder aur tamam current runtime assets us overlay mein nahin thin;
- kuch assets `android/app/src/main/assets/public/assets/` mein thay.

Magar GitHub workflow `npx cap sync android` chalata hai. Capacitor ka source `capacitor.config.json` ke mutabiq **`www/`** hai; sync ke waqt Android ka generated `assets/public/` isi web source se copy hota hai. Is liye sirf generated Android copy mein icon hona kaafi nahin—source `www/assets/icons/` mein bhi hona zaroori hai. Agar GitHub `main` ke `www/` mein woh naye icons na thay, sync unhein Android public copy se hata/overwrite kar sakta tha. Yeh phone par broken `<img>` icons ke saath **bohat strong match** hai.

Remote `main` ka poora file tree/AAB yahan directly verify nahin hua; is liye exact AAB mein kaunsa file missing tha, usay final fact nahin kaha ja raha. Is audit ke ZIP mein complete `www/assets/` folder hai; saath CI preflight ab verify karta hai ke `www/` aur Android ki synced public copy byte-for-byte match karte hon. Is se partial overlay wali kami repeat hone ka risk kam hota hai.

**Lag ka root cause abhi alag se diagnose nahin hua.** Fixed-step physics source mein hai, magar headless test FPS ya tumhare phone ke GPU/CPU performance ko measure nahin karta. Physics constants ko andazay se badalna risky hota, is liye is audit mein unhein nahin chheda.

---

## 4. Is audit snapshot mein ki gayi source tabdeeliyan

1. **Partial overlay ke bajaye complete project archive** tayyar kiya gaya; is mein original project ke Android, web, assets, tests, CI, server scaffold, design aur docs sab shamil hain.
2. `www/assets/` ko poora rakha aur Android Capacitor public copy ko `www/` se dobara sync kiya. Local comparison mein sab files barabar hain.
3. User ka pehle se diya rule follow karne ke liye **portrait orientation lock aur “turn your phone upright” blocker hata diya**. Game ab portrait-only overlay se landscape phone/desktop ko block nahin karta. Wake-lock (screen awake while playing) best-effort reh gaya.
4. Aglay Play upload ke liye Android version `versionCode 4`, `versionName 1.2` kiya. Version code 3 internal track par pehle hi upload ho chuka hai; agli upload ko naya code chahiye.
5. GitHub Actions ko fail-closed kiya:
   - `npm ci` hi chalti hai; dependency install error par random `npm install` fallback nahin.
   - Build se pehle `npm run check` chalti hai.
   - `npx cap sync android` ke baad asset/package preflight chalti hai.
   - Chaaron signing secrets lazmi hain; secrets na hon to workflow fail hota hai, unsigned AAB upload nahin karta.
   - AAB artifact upload se pehle JAR signature verify hota hai.
6. `scripts/audit_release.py` add ki: package ID, min/target/compile SDK, next version, fixed timestep/debug hook, landscape/orientation law, required art files, secrets hygiene aur Android asset mirror check.
7. Historical handoff/build docs par current audit ko source-of-truth banane ke notices lagaye; kuch purane test-count/version instructions update kiye.

**Gameplay physics, scoring, merge logic, server/backend aur ad reward logic ko is audit mein modify nahin kiya.** Portrait gate removal UI/platform behaviour ki tabdeeli hai; physics constants nahin badle.

---

## 5. Project ka kaam aur game mein kya maujood hai

### Core game

- Suika/fruit-drop style merge puzzle; Matter.js 0.20 code `www/index.html` mein inline hai.
- 11 fruit stages: Cherry → Strawberry → Grape → Lemon → Orange → Apple → Peach → Pear → Pineapple → Melon → Watermelon.
- Fruit bodies physics mein circle rehte hain; fruit art/sprites sirf rendering ke liye.
- Tap/click se drop, pointer/touch drag se aim; mouse/touch dono ke liye responsive HTML Canvas layout.
- Same-stage fruits merge; score, combo multiplier, floating score, effects aur watermelon milestones.
- Bomb aur golden special drops; watermelon completion par 3 mini-watermelon rain events.
- Game-over finale cascade, final bonus, high score, replay, aur ad callback successful ho to one-time continue.
- NEXT queue mein aglay 3 fruits.
- `window.FM_DEBUG` QA hook production source mein maujood aur test harness use karta hai.

### Powers aur economy

- Sweep: tamam normal stage 0/1/2 fruits clear karta hai; bomb/golden specials nahin.
- Undo: sirf valid `lastDrop` ko reverse karta hai; stale `lastDrop` reuse nahin.
- Freeze: 6 seconds ke liye motion rokta hai; drag-to-arrange support.
- Bomb, Pop/Clear, paid inventory, per-round free powers, shop aur rewarded-ad fallback.
- Diamonds: daily free reward, ad reward quota, challenges/achievements ke claimable rewards.
- Lucky Box/prize wheel, streak, achievements (9), daily/weekly challenges, local profile, stats, shop, ranks screen.
- LocalStorage key `fruitmerge.v2`; guest data isi device par save hota hai.

### Art, UI, sound, controls

- Home screen orchard backgrounds, Momo Merge title, stats, PLAY, profile, Lucky/Shop/Ranks image assets.
- User-approved toolbar icon PNGs, fluffy circular fruit renderings, original woven basket image, fruit strip, background art, Cherry Bomb One/Baloo 2 bundled fonts.
- Home Lucky/Shop/Ranks art user ke cream/brown framed-card direction ko follow karta hai; icon assets ko remove/recolour nahin kiya gaya.
- Sound WebAudio tones se; vibration haptics supported device par best-effort.
- Volume popup slider persists hota hai aur gameplay popup open rehte pause hoti hai.
- Game browser/PC aur mobile ke liye; portrait/landscape layout runtime par actual device par visual test hona baqi hai.

---

## 6. Kya abhi real/live nahin hai ya incomplete hai

| Hissa | Abhi ka asal status | Play/public release se pehle kya chahiye |
|---|---|---|
| Online account / Google sign-in | `NET_CONFIG` URL/key khaali; guest mode aur local save kaam karte hain. | Agar cloud save chahiye to Supabase deploy/configure, OAuth redirect aur policies test. Abhi “Google login ready” claim na karein. |
| Ranks/leaderboard | Server config ke baghair local/simulated rivals; global live leaderboard nahin. | Backend schema, auth, RLS, abuse/rate controls aur real user test. |
| Diamond packs | UI mein demo pricing; real billing nahin. | Google Play Billing products, server-side validation, refunds/restore, tax/policy setup. |
| Ads | AdMob bridge hai; portals ke CrazyGames/GameDistribution/demo paths bhi. Android ad IDs code/manifest mein hain. | Apne account ke IDs aur app association verify; consent/UMP and Data Safety; real-device ad/reward test. Test karte waqt apne live ads par click na karein. |
| Privacy policy | `www/privacy-policy.html` local source mein hai. | Public stable HTTPS URL host karke Play Console listing mein dena; third-party SDK data details match karna. |
| Store listing | 512×512 icon aur 1024×500 feature graphic source mein hain; `preview/` / `design/` images zyada tar mockup/work files hain. | Final store screenshots, descriptions, contact/support URL aur listing text owner se approve/complete. |
| Trader status | Play Console banner screenshot mein pending. | Owner khud sahi legal status choose/declare kare; legal classification hum guess nahin kar sakte. |
| Tester access | List mein 5 accounts nazar aaye; kuch accounts ko invitation error. | Selected list save ho, exact Google accounts verify hon, opt-in link se join test. |
| Device performance / broken icons | Owner ke phone par failure report. | Corrected full-source build ko isi Android device par retest; FPS, missing asset/network console errors aur collision feel inspect. |
| User account production testing gate | Personal developer accounts par Console account-specific test gate aa sakta hai. | Production request ke waqt Console ki exact requirement follow karein; internal testing ko closed-testing requirement na samjhein. |
| Android build/signing | CI workflow source mein harden kiya, lekin is workspace se Android SDK build/sign run nahin hua. | GitHub par full source commit, secret check, CI green + signature verify, phir AAB. |

---

## 7. Android/Play configuration snapshot

- `applicationId` / namespace / Capacitor `appId`: `com.isstudios.momomerge`.
- Current Play internal version observed: `versionCode 3`, `versionName 1.1`.
- Is source candidate ka next version: `versionCode 4`, `versionName 1.2`.
- `minSdkVersion 24` (Android 7.0+; Android 6 devices install nahin kar sakte).
- `compileSdkVersion 36`, `targetSdkVersion 36`.
- App Bundle source: `android/app/build/outputs/bundle/release/app-release.aab` (sirf GitHub workflow ke baad banta hai; is ZIP mein AAB shamil nahin).
- Play App Signing ke liye owner ki upload keystore ki zaroorat; signing secrets ZIP/source mein nahin hain.
- Manifest permissions mein Internet aur Advertising ID permission hain; final Data Safety declarations SDK behavior ke mutabiq honi chahiye.
- Current build type `minifyEnabled false`; is liye Play ka deobfuscation-file warning is build ke liye optional/expected hai.

---

## 8. Test aur static audit ke exact natayij

### Is audit session mein chalaye gaye

- `npm run check`: source ke inline Matter/game blocks dobara extract karke headless test chalaya — **553 passed / 0 failed**.
- New phase J: orientation lock bilkul na ho, rotate-to-portrait overlay na ho, simulated landscape size mein game start/home cycle chale; wake-lock tests bhi retained.
- `python3 scripts/audit_release.py`: **RELEASE PREFLIGHT: PASS**.
  - package ID/namespace match;
  - minSdk24, compile/target36;
  - versionCode kam az kam 4 / versionName1.2;
  - required 30 runtime images/fonts present;
  - 37-file `www/` tree aur Android `assets/public/` copy byte-for-byte same;
  - fixed 16.666ms physics call, `FM_DEBUG`, no orientation lock/rotate gate;
  - source tree mein keystore/signing secrets nahin.
- `python3 -m py_compile` pehle source scripts par pass hua; final package mein asset audit script bhi include hai.
- `node --check`/harness source-extraction path valid. `npm run check` hi recommended regression command.

### Jo **nahin** chal saka

- Chromium/Playwright/Puppeteer available nahin tha: full visual browser smoke test independently nahin hua.
- Android Studio/SDK/device build available nahin: local AAB build/signature nahin banayi gayi.
- Private GitHub `main` aur Play AAB ka file-by-file diff nahin hua.
- Owner ke real phone par lag, collision feel, icon loading, install/update persistence ko is workspace se reproduce nahin kiya ja saka.

**553 tests pass ≠ phone par bug-free.** Harness deterministic 400×800 simulated canvas, JS logic, economy, ads callbacks, fixed-step physics safeguards, UI hooks aur regressions test karta hai; GPU/frame timing, real touch latency, Android WebView cache/asset resolution aur Play Store tester invitation ko nahin.

---

## 9. Game rules / do-not-break audit

| User rule | Current local source/test status |
|---|---|
| Sweep sab stage-0/1/2 normal fruits remove kare | `doSweep()` sab matching bodies filter karta hai; harness sweep regression. |
| `muteBtn` volume popup khole | Source event handler `openVol()`; volume auto-pause/resume tests. |
| `lastDrop` stale object reuse na ho | `lastDrop` validity har use par fruits-list membership se check; removal/merge/sweep/bomb/undo par clear; harness Undo checks. |
| Mini-watermelon rain recursively trigger na kare | `triggerRain()` sirf normal stage-to-watermelon merge branch par call; rain fruits apni max-stage merge path par dobara rain trigger nahin karte. |
| `Engine.update` variable dt kabhi na ho | Runtime loop `Engine.update(engine,16.666)` fixed step; accumulator max 3 steps. CI audit checks fixed call. |
| Bomb/golden ke tests mein sufficient drops | Harness special fruit path/long-run tests hain; current pass summary says specials generated. Detailed statistical frequency on real device is not performance proof. |
| `window.FM_DEBUG` rehne chahiye | Present; harness directly uses it. |
| PC/web + mobile, portrait-only lock na ho | Is audit mein portrait lock/rotate gate remove kiya; landscape logic harness pass. Real landscape visual fit abhi device/browser QA pending. |
| Physics/backend untouched during basket art work | Audit mein physics/scoring/backend edits nahin kiye; sirf orientation gate, version metadata, CI checks aur docs badle. |

---

## 10. Source tree: kis cheez kaun si hai

| Directory/file | Kirdar / audit note |
|---|---|
| `www/index.html` | Actual game runtime: HTML, CSS, Matter.js + game JS inline. Is ko edit karne ke baad `npm run check`. |
| `www/assets/` | Current required fruit PNGs, 11 designed icons, backgrounds, basket images, fonts, preloader. **Current full source mein tamam files included.** |
| `www/admob-bridge.js` | Capacitor native AdMob plugin adapter; real IDs/config and consent setup ko production se pehle verify karna. |
| `www/privacy-policy.html` | Policy page source; public hosting URL abhi confirm nahin. |
| `android/` | Capacitor/Gradle Android project, manifest, package resources, generated `assets/public/`, launcher icons. Build artifacts/keystore excluded. |
| `.github/workflows/build-android.yml` | GitHub cloud AAB build; audit changes tests → sync → asset audit → required signing → signature verify → artifact. GitHub par abhi run nahin hua. |
| `.github/workflows/generate-keystore.yml` | Keystore generation workflow. Isay repeat na karna agar current upload key already established hai; ZIP mein secret/private key nahin. |
| `tests/harness.js` | Headless regression/simulation test runner, 553 passing. |
| `tests/fm_game.js`, `tests/fm_matter.js` | `www/index.html` ke inline blocks se generated test copies. Source-of-truth runtime HTML hai; extract script run kare. |
| `scripts/extract.py` | Inline scripts ko tests mein re-extract karta hai. |
| `scripts/audit_release.py` | Static source/runtime asset/version/package/sync preflight; device test nahin. |
| `scripts/economy.*`, `scripts/adlayer.js` | Historical/development fragments; Android runtime in files ko direct load nahin karta. Runtime game `www/index.html` hai. In fragments ko runtime samajh kar edit na karein jab tak intentional integration na ho. |
| `server/` | Supabase schema/verification scaffolding; deployment credentials/config blank, production backend active nahin. |
| `icon-512.png`, `feature-graphic.png` | Store listing art assets. Icon 512×512 RGBA PNG (opaque alpha channel preserved, no visual redesign); feature graphic 1024×500 PNG. Final upload ke waqt Console preview check karna. |
| `preview/`, `design/` | Design iterations/mockups/screens; runtime mein load nahin. Store-ready screenshots honay ki guarantee nahin. |
| `HANDOFF.md`, `WORKSPACE-NOTES.md`, old merge/readme docs | Historical logs; kuch old version/TODO/orientation statements hain. `AUDIT-AND-STATUS.md` current source-of-truth hai. |

**Inventory:** project archive mein is audit/manifests samet poora current source tree hai; exact file count, byte sizes aur SHA-256 hashes `SOURCE-FILES-MANIFEST.csv` mein. Manifest khud apni hash-list se excluded hai. `node_modules`, Gradle caches/build outputs, `.git` history aur private signing material intentionally included nahin—dependencies CI `npm ci` se install hoti hain.

---

## 11. Release readiness checklist — agla safe rasta

### Source ko GitHub par dalne ke baad

1. Is full source package ko existing `Momo-Merge` repo mein carefully apply/replace karo; `www/` **aur** `.github/workflows/`, `android/`, `tests/`, `scripts/`, `package*.json` sab included hone chahiye. Sirf `android/app/src/main/assets/public/` ko copy karke na rukna.
2. GitHub `main` mein check karo:
   - `www/assets/icons/bomb.png`, `freeze.png`, `home.png`, `lucky.png`, `pop.png`, `ranks.png`, `retry.png`, `shop.png`, `sweep.png`, `undo.png`, `volume.png`;
   - `www/assets/fruits/f0.png` se `f10.png`;
   - `www/assets/index.html` nahin—sahi runtime path `www/index.html` hai;
   - `android/variables.gradle` minSdk24;
   - `android/app/build.gradle` versionCode4/versionName1.2.
3. Existing upload keystore ke **wahi** chaar GitHub Actions secrets rehne chahiye. Nayi keystore generate mat karna; old upload key replace karne se Play updates reject ho sakte hain.
4. GitHub Actions `Build Android AAB` mein npm regression, asset preflight, signature step **sab green** hon. Agar koi step fail ho, artifact upload na karo.
5. Run artifact `fruitmerge-aab` download karke **new internal test** mein upload karo; old version 3 ko replace/update karo. Pehle tester access/account link resolve karo.
6. Kam az kam owner ke Android phone par verify: home all icons; Play→game transition; fruit sprites; top toolbar; 20+ normal drops; collisions/merges; sweep/undo/freeze/bomb/pop; sound; back/home; landscape; 5–10 minute gameplay; no missing assets; lag/framerate acceptable. Is actual device pass ke baghair “fixed” na kaho.
7. Agar icons phir tootay hon: user ke phone par WebView cache/installed build, exact installed `versionCode`, aur main ke file paths verify karo. `scripts/audit_release.py` CI output inspect karo.
8. Production se pehle privacy/data safety/AdMob consent, hosted privacy policy, content/target audience, store listing screenshots, trader status, testers aur Console ki account-specific testing requirement complete karo. Production button abhi nahin.

---

## 12. Final verdict

- **Workspace source checks:** pass (553/0 plus asset preflight pass).
- **Previous partial overlay:** incomplete for guaranteed runtime asset transfer; likely contributing to broken icons after Capacitor sync.
- **New full source candidate:** complete local tree, code4, landscape gate removed, all current web files synced, CI now adds fail-closed tests/assets/signature checks.
- **Phone graphics and lag:** user-reported and still open; no device proof of fix.
- **Remote GitHub source/AAB:** not compared directly.
- **Production readiness:** **NO** until current full-source candidate is built on GitHub and the actual Android phone passes the listed QA, plus Play policy/account requirements are complete.

Is audit ka maqsad har cheez ko sach-sach list karna hai—complete features, demo-only parts, pending kaam, evidence, aur limits. Isay “zero known bugs” claim ya production approval na samjha jaye.
