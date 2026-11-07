# Momo Merge — MASTER HANDOFF (8 Nov 2026 banaya gaya; ye SINGLE SOURCE OF TRUTH hai)
> **NAYA SESSION YEH PADHNA SAB SE PEHLE.** Ye doc 7 Nov ke handoff ko bhi absorb karta hai
> (wahan se jo bhi pending tha wo yahan me hai). Purana doc `SESSION-HANDOFF-2026-11-07.md`
> ab reference ke liye hi hai — is file ko follow karo. Baqi purane docs:
> `AUDIT-AND-STATUS.md` (source audit — ab tak valid), `SETUP-GUIDE.md`, `CLOUD-BUILD.md`, `DEPLOY-GUIDE.md`.

---

## 1. Project identity (har session ko yaad rakhna)

- **Game:** Momo Merge: Cute Fruit Drop (Suika/fruit-merge, Matter.js INLINE in `www/index.html`)
- **Package:** `com.isstudios.momomerge` · Capacitor Android · minSdk 24 / compile 36 / target 36
- **Account owner:** helloimperialsolutions@gmail.com — Play developer "IS Studios Official" (Personal/trader declared) · AdMob contact: Imran Sarwar (+92 300 5488049)
- **Repo:** https://github.com/helloimperialsolutions/Momo-Merge (PUBLIC) · **local dir:** `C:\Users\muham\OneDrive\Documents\Default Project`
- **Git (8 Nov tak):** `main` = `efbba55` — poora chain:
  - `67c5673` old handoff → `3a7aa5f` OAuth/Android+refresh → `a7eec07` Continue+resize → `eacbe66` ad-skip+toast → `c183a7b` landing page → `6ab0c2c` handoff notes → `6cfe1b9` **v5/1.3 bump** → `efbba55` audit print fix
- **Tests:** ab **587** (553 → 587; naya Phase N = save/continue/resize/ad-skip). CI **push-to-main par auto "Build Android AAB"** chalata hai; artifacts ka naam `fruitmerge-aab` (andar `app-release.aab`).
- **Current candidate:** versionCode **5** / versionName **1.3** (`android/app/build.gradle`). Play alpha track pe abhi tak sirf v4/1.2 (versionCode 4) upload hua hai.

---

## 2. KAIDAAR RULES — kabhi na toden (audit section 9)

1. `Engine.update(engine, 16.666)` FIXED timestep — physics constants/math KABHI mat chherna
2. Har change ke baad: `npm run check` (587 tests) + `npm run cap:sync` + `python scripts/audit_release.py` → PASS
3. Har milestone pe git commit — **main hi push hota hai** (credentials cached; user ke push me connection tooti thi)
4. `tests/fm_game.js`, `tests/fm_matter.js` GENERATED hain (`scripts/extract.py` unhe deta hai) — manually edit NAHI. `tests/harness.js` aur `scripts/*` = source, edit allowed.
5. `www/index.html` = Source of Truth (single-file game runtime, ~4600+ lines)
6. `window.FM_DEBUG` hook rehna chahiye (test harness ise use karta hai)
7. Secrets/keystore source me NAHI — CI secrets handle karte hain (`KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`)

---

## 3. LIVE infra — current is-waqt state (7 Nov RAT se compare: sab clear ho gaya)

| Hissa | Current state |
|---|---|
| **Supabase** ✅ PUKHTA | `momo-merge` project: url `https://vlkpjngrfkloeszmyypl.supabase.co`, anon key inline in `NET_CONFIG` (index.html) — cloud save + leaderboard ✓ RLS "own row only" ✓. **User ne URL Configuration screenshot bheja: Site URL + teeno Redirect URLs entered (7 Nov raat).** |
| ⚠️ Supabase 2 minute ke reh gaye kaam | 1) Site URL ke neeche **"Save changes" ka button** confirm karke dabana. 2) **Sign In / Providers → Google** — open karke ek dafa baten — Enabled hai na nahi. |
| **Google sign-in (web)** | index.html → `Net.login("google")` → supabase `/auth/v1/authorize?provider=google` → hash me token → `captureAuthHash()` |
| **Google sign-in (APP — ab KAAM KARTA HAI! 3a7aa5f)** | WebView redirect ni hota: app **system browser** me OAuth karata hai → wapsi `com.isstudios.momomerge://callback#access_token=...` → intent-filter `VIEW/BROWSABLE` → `@capacitor/app` ka `appUrlOpen` lifetime listener + cold-start `getLaunchUrl` → `handleAuthCallback()` → token capture + `diaToast("👤 ...")`. **REFRESH-TOKEN rotation: `tryRefreshAuth()` har boot pe 1 POST** (`/auth/v1/token?grant_type=refresh_token`) — warna 1 ghante baad token plugin diya guest ban jata. Keys: `fruitmerge.auth` + `fruitmerge.refresh`. |
| **AdMob** ✅ partial | Real IDs bridge + `initializeForTesting:false`. Account **approved**. GDPR (European) message = **1 active ✓ (7 Nov ko user ne create kar li)**. App pe `Requires review` + `Limited ad serving` — **"Add store" abhi user ne submit karna hai** (plain (auto) review). |
| **Privacy/deletion/ToS Pages** ✓ LIVE | `https://helloimperialsolutions.github.io/Momo-Merge/www/privacy-policy.html` + `-deletion.html` + `-tos.html` — teeno LIVE, `.nojekyll` hai |
| **Pages LANDING (8 Nov tak naya)** ✓ | Root `index.html` commit `c183a7b` — `https://helloimperialsolutions.github.io/Momo-Merge/` ab 404 NAHI. Play Console **"Website" field me ye daal sakte hain** (Pages deploy verify karke). |
| **Play Console** | Closed Alpha **v4/1.2 (versionCode 4)** publish ✓ (7 Nov). Trader status TRADER declared ✓. **12-tester / 14-day production gate chal rahi hai** (12 joine hote hi timer). App content 11/11 complete. **Aa raha naya release: v5/1.3** (upar dekhein "Upload ka kaam"). |

---

## 4. AJ (7/8 Nov ke raat-gheantay) jo HO GAYA — full record

### 4a. ✅ Android OAuth complete (`3a7aa5f`)
- **Reaction code (www/index.html):**
  - `parseAuthFragment(frag)` + `applyAuthParams(q)` refactor — web hash aur app callback same code-path
  - `OAUTH_CALLBACK="com.isstudios.momomerge://callback"`, `handleAuthCallback(url)`, `initOAuthRedirect()` — `Capacitor.isNativePlatform()` guard, `App.addListener("appUrlOpen")` + `App.getLaunchUrl()` (cold start), `diaToast("👤 name, T("welcome")")`
  - `Net.login("google")`: native pe `redirect_to=OAUTH_CALLBACK`, web purane wale page URL
  - `econInit()` me `tryRefreshAuth()` add hota hai — refresh rotation store + UI refresh
- **AndroidManifest.xml:** `MainActivity` ke andar LAUNCHER ke sath **VIEW intent-filter** (`scheme="com.isstudios.momomerge"`, DEFAULT+BROWSABLE), comments included. `singleTask` hai.
- **ab signing future**: `@capacitor/app` pehle hi dependency thi (`^7.0.0`), sirf bridge inject hona chahiye hai.

### 4b. ✅ Save progress / Continue feature (`a7eec07`)
- **Decision:** Local save hi primary hai (audit ne aise hi holda). `fruitmerge.midgame` key, **cloud cross-device board restore NAHI** — tab bar ke geo fark + bug-can ke khul jane ka risk. Player's **account** (diamonds/best/rank) pehle hi cloud me hai.
- **Game flow:**
  - `snapshotBoard()` — sirf `state==="play"|"pause"` aur board non-empty ho; fruit positions **box-ke-relative** store hoti hain (rotation/resize pe bhi graceful), `q` (4-queue), `powers`, `pendingBoost`, `score/drops/uc`
  - **Save triggers:** `goHome()` mid-game (侧 toast `💾 Progress saved` — kabhi kabhi) + `visibilitychange`(hidden) + `pagehide` — **SILENT** auto-save
  - **Clear triggers:** `newRound()` (START PLAY naye se) + `finishGame()` (game over hone par)
  - **Home UI:** Play ke neeche **`#contBtn` (green ▶ CONTINUE)** + `#contHint` ("Score X · Y fruits waiting") — `refreshContinue()` `refreshStartChips()` + `newRound()` ke end se call hoti hai. State play/others me hidden.
  - `continueGame()` — full reset + board rebuild (pos clamp box ke andar), overGraceUntil +1s settle; **deliberately NOT restored:** `lastDrop` (audit rule 4 area — undo ke sath wapsi ka issue), `frozenUntil/goldenUntil/comboCount` (Date.now() timers + "unearned gold"), bomb `fuse` timers. `usedContinue` (ad-flag) restore hota hai — economy safe.
- **Naya CSS:** `#contBtn` green gradient, `#contHint` brown 14px; home markup Play button ke ix neeche ho.
- **i18n strings naye:** `savedNote`, `resumeHint` ("Score {0} · {1} fruits waiting"), `confirmOverwrite`.

### 4c. ✅ Resize bug fix (same commit)
- **Root cause purani:** sirf X remap hoti thi (boxX+Δx), **Y bilkul raw pixels** rehta tha → bade height changes pe pile floor ke neeche/bahar, score HUD stale.
- **Naya layout():** `oldH=geo.boxH` track, `geo._oldBoxY/_oldBoxH` added in geo init + layout ke end me update; kisi bhi `boxW`/`boxH` change pe (s=boxW/oldW): sab bodies **dono axes remap + clamp (r0+2 margin, walls ke andar)** + velocity scale + `aimX=clampAim(aimX)`. render `b.circleRadius` pe chal raha hai jo Body.scale khud update karta hai. Koi physics constant touch nahi hua.

### 4d. ✅ Testers-phase ads skip (`eacbe66`) — ⚠️ **PRODUCTION SE PEHLE FLIP ZARURI**
- **`window.FM_TESTERS_SKIP_ADS=true`** index.html me (`var HOST=detectHost()` section-13b ke top). Ish sath:
  - `requestReward(cb)` → **cb() instant** (no overlay/SDK/no toast) — power ad grabs, +50 💎 ad, sab FREE mil jate hain
  - `showInterstitial(done)` → done() instant (schedule counting chalta rehta hai, future me koi drift nahi hoga)
  - `initBanner()` → no-op
- **`www/admob-bridge.js`:** isme SDK plug-in pe **early `return`** when `window.FM_TESTERS_SKIP_ADS` — **UMP consent form bhi fhi na dikhagi, koi SDK wake-up nahi**
- **Double-garbled toast fix:** `addFloat` ab (a) same-text within 1.2s → in-place refresh; (b) DIFFERENT text <300ms → **y-axis me 26px stagger upar**; koi message blank/smoke nahi hota. (Sab se purane combo/score text wala overlap fix hua.)
- **Flip playbook (PRODUCTION):** index.html se `window.FM_TESTERS_SKIP_ADS=false` + **AdMob → Settings → Test devices** me apna (aur Imran ka) device pehle **register** karna (apni clicks policy flag na ho) + **US state regulations message Create**, phir `npm run check` — CI AAB khud ads ke sath ban jayegi.

### 4e. ✅ Pages landing page (`c183a7b`)
- Root `index.html`: inline-CSS kawai juice design, sections: About / PLAY NOW (button `www/index.html`) / Google Play badge (link kommenden production ke liye blocked) / Policies links. Play "Website" field ka official target.

### 4f. ✅ Version bump + audit (`6cfe1b9`, `efbba55`)
- `versionCode 5 / versionName "1.3"`. `scripts/audit_release.py` ab candidate ki apni version print karta hai (stale hint fix).
- **Play upload ka kaam (USER):** CI run **#22 (`efbba55`)** green → **Artifacts → `fruitmerge-aab`** download → andar `app-release.aab` → **Play Console → Closed testing → New release (v5/1.3)** → release notes chhaape: "• Save your progress & Continue • Fixed: screen-resize issues • Faster & smoother (bug fixes)" → Review → **Start rollout**. Testers ko update kuch ghante me mil jata hai.

---

## 5. Play Console exact answers (re-derivation na ho, ise copy karo)

**Data safety (final config posted):**
- Collect/share: **Yes**; encrypted in transit: **Yes**; account creation: **OAuth** only
- **Deletion URL (dono fields):** `https://helloimperialsolutions.github.io/Momo-Merge/www/account-deletion.html`
- Data tiles: **email + user IDs** (Collected only, Optional, App functionality + Account management); **app interactions + Advertising ID + approximate location** (Collected **and shared**, Required, Advertising)
- Partial deletion (bina account): deletion page ka hi link, **Yes**

**Advertising ID declaration:** Yes + purpose = **Advertising only** ✓
**Content rating:** Everyone · **Target audience:** 13+ ALL, "children appeal"=No · **Financial features:** None · **Sign-in:** No restricted access · **AI asset declaration:** icon+feature graphic AI-labeled tick karna hai (naya art ane per), screenshots REAL device wale
**Store listing:** Name `Momo Merge - Cute Fruit Drop` (28/30) · Short: "Merge cute fruits into a giant watermelon! A cozy drop-puzzle for everyone." · Full desc 1300-char ready · Category Game→Puzzle · contact hello@imperialsolutions.org · **website field ab fill ho sakta hai** (Pages root live)
**Trader:** declared ✓ · app-level ToS URL given ✓

---

## 6. AdMob state (7 Nov late screenshots ke mutabiq)

- Account **APPROVED** ("Your account is approved"), earnings $0 (expected — abhi ads skipped + app review baqi)
- App: `Momo Merge: Cute F...` Android, App ID `ca-app-... 8386435012`, **3 active ad units** (rewarded/interstitial/banner — IDs `www/admob-bridge.js` me + App ID manifest me)
- Status: `Requires review` + `Limited ad serving` → **"Add store" link karna baki (user, 2 min)** — package `com.isstudios.momomerge`; error "not found" aaye to listing index hone ka wait
- GDPR (European) = **1 active ✓**; US state regulations = optional abhi; IDFA = iOS-only (irrelevant)
- **Test devices:** filhal ghair-kari (build ad-free hai). Jab production ads flip hoga tab register karna.
- **app-ads.txt:** later, `imperialsolutions.org/app-ads.txt` pe (root domain crawler rule). Content: `google.com, pub-5002697332409715, DIRECT, f08c47fec0942fa0`
- Home pe "Show hidden tasks (3)" me kya hai — user screenshot ke sath verify karna hai (payee/billing, app settings waghera)

---

## 7. USER-side pending (aapke actions — priority)

1. **Supabase 2-min reh gaye:** Site URL "Save changes" ka button confirm + Sign In / Providers → **Google enabled** check
2. AdMob **"Add store"** submit (store link review)
3. **Play upload v5/1.3:** CI run #22 artifact → Closed testing new release (upar §4f)
4. **12 testers opt-in** — alpha track opt-in link share; 14-day timer 12 joined hote hi
5. **AdMob hidden tasks (3)** kya hain — screenshot一下
6. **Pages landing deploy verify** — open `https://helloimperialsolutions.github.io/Momo-Merge/`, game PLAY button bhi chalana; phir Play listing me **Website field fill**
7. **Phone QA** audit §11 (20+ drops, powers, icons, lag, landscape, sound, **Continue button + login wapas aa jana**) — v4 ya v5 alpha pe
8. **Store screenshots (6)** — power+vol-down, Play listing me daalna
9. **DP trader:** `imperialsolutions.org` pe legal name/profile details page — Naam ka faisla abhi bhi pending (Saqib/Imran vote)
10. **Store listing icon/feature graphic** — naya art kaafi; screenshots REAL device wale

---

## 8. NAYE SESSION KE LIYE — mera kaam (priority order)

### 🥇 1. AI icon + feature graphic (QUOTA WINDOW ~8 NOV NOON)
- Free quota 7 Nov ko exhaust ho chuka tha ("retry in 20h39m" ≈ **8 Nov ~12:20 PM PKT**). **Din ke aghaz pe yehi karna** — pehli cheez:
  - **Icon** `design/icon-512-v3.png` — 512×512: peach+strawberry kawaii mid-merge moment, gold sparkles, cute faces, pastel cream tile bg, thick brown outline, **no text**
  - **Feature graphic** `design/feature-graphic-v3.png` — 1024×500: center wicker basket, falling fruits arc, merge sparkles/heart particles, warm gradient, bold "MOMO MERGE" chunky pink title + "Cute Fruit Drop" subtitle
  - phir exact sizes me resize/crop → root `icon-512.png`/`feature-graphic.png` replace → Play listing ke assets me user upload AI-labeled declare
  - Purane assets: root wale OLD (user ne reject kiye), `design/` me v2 attempts bhi hain
- Agar 8 Nov ko bhi quota fail → backup: local `preview/` dir templates + user ke phone se aane ke hints; bare-minimum iconic art hand-tuned SVG fallback (aakhri resort, user consent lena)

### 🥈 2. CI verify + Play release status check
- `git log -1` + Actions API se run status (gh CLI nahi hai locally, use `Invoke-WebRequest https://api.github.com/repos/helloimperialsolutions/Momo-Merge/actions/runs?per_page=N`)
- Run #22 green → user ko poora §4f ka upload flow yaad karana; agar red → failure log dekh kar fix+push

### 🥉 3. Production ad-flip checklist draft (kis date pe, kis order me)
- Test devices register → `FM_TESTERS_SKIP_ADS=false` → US-state message → check → tag/run → docs
- **Note:** flip AASANI production gate (12 testers/14 din) PASS hone ke BAAD hi karna, warna production track pe ek adn app review phir se prapt ho jayegi

### 4. Chhote polish (agar waqt bache)
- `sendFeedback / support`: WhatsApp/Email support URL public karna — `deletion page` aur Play support contact area me consistent
- Home `loginNudge` message text bhi Continue feature ke sath align ("Login to Cloud-Save & leaderboard")
- `display-name auth` me bug handle: agar user ki google-account name kho gai flow me — `store.profile.name` fallback is already safe; parse further

---

## 9. Tareeqa naseehat (technical knowledge jin modules me azm hai)

- `www/index.html` sections map (approx lines aaj ke tak):
  - ~0-1250: fonts+CSS+boot store (`fruitmerge.v2`)
  - ~1160-1210: STRINGS.en i18n + T()
  - ~1130-1142: store + `save()` + key helpers
  - ~199-215: `.playBig`, `#contBtn`, `#contHint` CSS + glow keyframes
  - ~1500-1660: geometry/layout/makeWalls + **resize remap (bilk line "Uniform remap on ANY geometry change")**
  - ~1680-1750: spawnFruit/removeFruit/processMerges/explodeBomb
  - ~2340-2630: flow: updateHud/pickObj/newRound/**clearSnapshot**/drop/checkGameOver/startFinale/**finishGame (clearSnapshot)**/doContinue
  - ~2415-2605: **10b MIDGAME module**: MID_KEY/snapshotBoard/clearSnapshot/readSnapshot/continueGame/refreshContinue
  - ~2790-3040: ads section: detectHost/**FM_TESTERS_SKIP_ADS + adsSkipped()**/adPause/adResume/rewardFailed/rewardGranted/host funcs/requestReward **(skip first branch)**/interstitial/interstitialDemo/initBanner
  - ~3030-3110: spendPower; bomb/sweep/undo/freeze handlers
  - ~3280-3450: NET_CONFIG/netOn/auth session (AUTH/REFRESH_KEYS, netHeaders, **parseAuthFragment/applyAuthParams/captureAuthHash**, loadAuthTok/clearAuthTok/**tryRefreshAuth**, netFetch)
  - ~3460-3720: store/econDefaults/econInit (loadAuthTok→captureAuthHash→tryRefreshAuth)/dates/period/diamonds/CH_POOL
  - ~3720-3830: lbSubmit/Net facade (native callback branch)/sign/googleSignIn/gisSignIn/applyGoogleProfile
  - OAUTH: OAUTH_CALLBACK/handleAuthCallback/initOAuthRedirect — clearAuthTok ke baad
  - ~4390-4460: boot tail: initWorld → body.inmenu → econInit() → **initOAuthRedirect()** → rollPeriod → wireEcon/initBanner...
  - ~4760-4830: window.FM_DEBUG (naye hooks: `midSnap/midHas/midScore/midFruits/midClear/midRestore/midResume/geoBox/adRequest/adSkip`)
  - file line counts aaj: total ~4700; buildFW the ~588KB.
- **Server (test):** `npx http-server www -p 8081 -c-1` (background me chala diya tha; session band ho to dobara start: `npm start`)
- **Local env:** Node 22.18.0, npm registry sync'd; `py -3` (3.13.5) — `npm run check` cross-platform handles kar leta (`scripts/check.js`)
- **CI:** `.github/workflows/build-android.yml` fail-closed; push to main = auto AAB. `generate-keystore.yml` RUN-ONCE (do NOT run again)
- **tests/harness.js:** sandbox me `els` For IDS mapping (contBtn/contHint added at line ~187-188), `store` = localStorage stub, hermetic fetch (`netCalls[]`), timers stub (`setTimers mode`), `dropMid()`/`pump(n)`/`click(id)` idioms. Phase **N** (N1 restore flow, N2 corrupt-garbage graceful, N5 resize-inside-box, N6 deferred ad-skip — pending after K), sirfm tests pe sand-letters double-check before edit

---

## 10. Agar kuch NOTES/SIDE-ways faadun (marking me)

- 7 Nov handoff doc contains some garbled lines (OCR/mix). Ye file now MASTER hai — only this.
- Old assets: `icon-512.png`, `feature-graphic.png` root, `preview/`, `design/icon-512-v2.png`
- Player pool / fake leaderboard, guest — ID already present (design decision)
- `server/supabase.sql` + `verify_schema.py` imported ✓ — profiles/scores tables live; RLS is "own row only"
- **WhatsApp/Email support** URLs intentionally NOT public yet — user's availability windows seen

---

> **Naya session start instructions (user ke liye):** naya session khol kar bas likhna:
> `SESSION-HANDOFF-2026-11-08.md padho aur wahin se kaam shuru karo` —
> aur agar user-specific note dnasee ho (Play screenshots, AdMob hidden-task screenshots,
> phone QA ke notes) to sath paste kar dena.

— Agla session inshallah icon/graphic + upload + production plan ke bare me hoga. Bas ye yad rakhna: admobb audid `FM_TESTERS_SKIP_ADS` PRODUCTION SE PEHLE OFF.
