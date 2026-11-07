# Momo Merge — Session Handoff (7 Nov 2026, evening)
> **NEXT SESSION YEH PADHNA SAB SE PEHLE.** Ye doc pichle sessions ka poora record + agle session ka kaam hai.
> Purane docs: `AUDIT-AND-STATUS.md` (source audit, abhi tak valid), `SETUP-GUIDE.md` (backend setup steps).

---

## 0. AGLA SESSION (8 Nov, raat ~noon ke baad image window khulegi)
**Aaj (7 Nov raat) ho gaya — commits:**
- `3a7aa5f` **OAuth Android complete**: app-scheme callback (`com.isstudios.momomerge://callback`), `appUrlOpen` + cold-start `getLaunchUrl` (index.html → `handleAuthCallback`/`initOAuthRedirect`), `Net.login` native redirect_to, intent-filter manifest me, web flow refactor (`parseAuthFragment`/`applyAuthParams`), **refresh-token boot rotation** (`tryRefreshAuth` — 1h token expire hone par player guest me na gire; REFRESH_KEY `fruitmerge.refresh`)
- `a7eec07` **Continue feature + resize fix**: mid-game snapshot `fruitmerge.midgame` (`snapshotBoard`/`readSnapshot`/`continueGame`/`refreshContinue`), home pe green **CONTINUE** btn + hint ("Score X · Y fruits waiting"), auto-save on goHome (toast 💾) + visibilitychange/pagehide; `newRound`/`finishGame` clear karte hain; **lastDrop/frozen/golden/combo JAAN-BUJH ke restore nahi hote** (audit rule 4); resize remap ab dono axes (y-drift fix) + clamp box ke andar + velocity scale — fruits ab kabhi bahar nahi jate
- `eacbe66` **Testers-phase ad skip** (⚠️ production pe lautana hai): `window.FM_TESTERS_SKIP_ADS=true` index.html me — requestReward → instant grant (koi ad/overlay/toast nahi), interstitial skip, banner skip, admob-bridge SDK/UMP interruptively guardoff. **PRODUCTION RELEASE SE PEHLE `false` karna** (single switch). Saath me `addFloat` dedupe/stagger — double garbled toast bug fix
- `c183a7b` **Pages landing page** — root `index.html` live: game, Play badge, privacy/deletion/ToS/contact links. Play "Website" field me ab `https://helloimperialsolutions.github.io/Momo-Merge/` daal sakte ho (Pages deploy ke baad — 404 check karna)
- Tests: **587 (553 → 587)** — Phase N (save/continue, corrupt-save graceful reset, resize remap N1–N6) + N6 ad-skip assertions. CI push ke sath green hona chahiye (verify: poora check pass tha)
- **AI quota ne abhi bhi block kiya** (dono icon/feature-graphic attempts, free tier daily limit) — **retry 8 Nov ~noon** ke baad pehla kaam; prompts design me likhi thi: icon (peach+strawberry kawaii merge sparkles, no text) + feature graphic (basket + falling fruits + "MOMO MERGE" title) → `design/icon-512-v3.png`, `design/feature-graphic-v3.png` beds, exact 512×512 + 1024×500 me resize karke Play listing me replace

**USER-side pending (same list, upar section 4 me):** Supabase URL Configuration (pehla table neeche section 5.1), 12 testers opt-in, GDPR message create, Search Console, phone QA, screenshots, DP name, suppress: ab sirf PageS deploy verify + Supabase entries.

**Supabase dashboard exact values (user ke paste karne ke liye — COMPLETE):**
- Site URL: `https://helloimperialsolutions.github.io/Momo-Merge/`
- Redirect URLs (teen no ek ek karke): `https://helloimperialsolutions.github.io/Momo-Merge/**` · `http://localhost:8081/**` · `com.isstudios.momomerge://callback` (app ke liye ZARURI — warna Android login wapas nahi aayega)

---

## 1. Project identity (har session yaad rakhne wale)

- **Game:** Momo Merge: Cute Fruit Drop (Suika/fruit-merge, Matter.js inline in `www/index.html`)
- **Package:** `com.isstudios.momomerge` · Capacitor Android · minSdk 24 / target 36
- **Account owner:** helloimperialsolutions@gmail.com — Play developer "IS Studios Official" (Personal account)
- **Repo:** https://github.com/helloimperialsolutions/Momo-Merge (**PUBLIC hai ab**)
- **Local working dir:** `C:\Users\muham\OneDrive\Documents\Default Project`
- **Git state (7 Nov evening):** `main` = `3623493` (TOS page push). CI green pass wale builds: #11 (`b0794cb`), #12 (`e6b8cf7`).
- **Owner user:** Saqib (helloimperialsolutions@gmail.com). Contact: hello@imperialsolutions.org (verified on Play), phone verified, website imperialsolutions.org (LIVE — abhi Search Console ownership verification pending).

---

## 2. KAIDAAR RULES — kabhi na toden (audit section 9 se)

1. `Engine.update(engine, 16.666)` FIXED timestep — physics constants/math KABHI mat chherna
2. Har change ke baad: `npm run check` (553 tests) + `npm run cap:sync` + `python3 scripts/audit_release.py` → PASS
3. Har milestone pe git commit — main hi push hota hai (credentials cached, user ke push me connection toot'ti thi)
4. `tests/fm_game.js`, `tests/fm_matter.js` GENERATED hen (`scripts/extract.py` inhi ko deta hai) — manually edit NAHI
5. `www/index.html` = Source of Truth (game runtime)
6. `window.FM_DEBUG` hook rehna chahiye (test harness ise use karta hai)
7. Secrets/keystore source mein NAHI — CI secrets handle karta hai

---

## 3. Live infra (yehi config is waqt)

| Bahut hissa | Current state |
|---|---|
| **Supabase** | Project `momo-merge` LIVE: url `https://vlkpjngrfkloeszmyypl.supabase.co`, anon (publishable) key inline in `NET_CONFIG` (index.html mein fill ho chuka — cloud save + leaderboard ✓) Notes: anon key hi app mein hotha hai; RLS "own row only" ka rule ✓ |
| **Google sign-in flow (game-side)** | index.html → `Net.login("google")` → `window.location.href = supabase>/auth/v1/authorize?provider=google&redirect_to=<current#-less url>` → token URL hash mein wapsi pe aata hai → `captureAuthHash()` |
| **⚠️ Supabase SHA—BUG** | Site URL = `http://192.168.100.184:8081/` (LAN IP — barik network pe NAHI milega). Redirect URLs khali hain. **Isliye Google login ke baad user wapas app/web pe pahunch hi nahi raha.** Fix unlike below (section 5) |
| **AdMob** | Real app ID + 4 unit IDs wired in `admob-bridge.js` + UMP consent hook. initializeForTesting=false |
| **Privacy policy / deletion / ToS URLs (Pages)** | `https://helloimperialsolutions.github.io/Momo-Merge/www/privacy-policy.html` (+ `/account-deletion.html`, `/tos.html`) — teeno PUBLIC LIVE.  `.nojekyll` hai, Pages turbo deploys karte hain |
| **Play Console** | Closed Alpha track (v4/1.2) publish ✓ (Nov 7). Trading status: TRADER, declared ✓. 12-testers / 14-day production gate ab chalni hai |

---

## 4. New session KE LIYE — pending + user ke poochay ke kaam (priority order)

### 🚧 USER ka kaha khud ko bhi jo bug + tayyar new features (ye session chahiye) 🚧

**4a. Supabase site/redirect URLs FIX (first thing!).**
- Dashboard → Auth → URL Configuration open (user ke screen mein jo LAN IP dikh raha hai):
  - `Site URL` = `https://helloimperialsolutions.github.io/Momo-Merge/` — root of Pages app (game is at `/` root after Pages serve at Momo-Merge). NOTE: runtime www/index.html game via Pages top level + `/www/` html paths (flash needed — check).
  - **Redirect URLs** add (kyonki asli app mein OAuth not browser native hai):
    - `https://helloimperialisionsolutions.github.io/Momo-Merge/**`
    - `http://localhost:8081/**` (web dev)
    - `https://vlkpjngrfkloeszmyypl.supabase.co/**`? (holder redirect keep)
  - **Real Android app redirect:** Capacitor WebView ke redirect "com.isstudios.momomerge://" custom scheme via intent-filter + `@capacitor/app` `appUrlOpen` plugin handler. Abhi game ye Front-end part NAHI karta. Ye next session main kaam hoga.
    Plan-of-record: play store/Android intent `e.g. appUrlOpen` capture token → code change in `www/index.html` around `Net.login` and `captureAuthHash`. **in CHECK ke sath + backward-compatible web flow.**
  - Also OAuth session persistence via Capacitor login loop — Confirm they use `@capacitor/app` package and `App.addListener("appUrlOpen")` in app context only, guard if `Capacitor.isNativePlatform()`.

**4b. "Save your progress / Continue" feature (user request!).** User ka logic:
- Users bore hote hain 1–2 ghante khelte khelte, chahte hain break le kar wapas aayen and uski saving progress ho na
- Hamare ranking/leaderboard > score dikhaye — yehi motivation backbone chahiye
- Plan: **Local save hi priamry enti hui**: `fruitmerge.v2` localStorage default (already!). **Cloud save (Supabase `profiles`/`scores`)** = jab browser handle oplus sign-in kiya jayé
- Game flow additions:
  - Home menu pe **"Continue"** button — jab last session ki state (mid-game board) machine saved ho
  - **Auto-save on Quit/Home (CLOSE CLOSING)** — store(game state) mid-board snapshot before exit (fruit positions, score, current index, characters). Add format/data trailer on state
  - Sign-in on different device (cloud save + `lastPlay` resuming allowed)
  - Stale board (pure app close, force restart, corrupted save) gracefully se reset
  - Scope kya kya hoga: pata nahi local vs. supabase — **next session decide karna hai** aur kai UI copy. fat priority ke kaam
- **Careful:** power inventory/bomb/undo/lastDrop state bhi save ho to `lastDrop` invalid bug wala area (audit rule!) — futurepadded

**4c. Resize bug (reported).** Window/viewport resize karo (desktop browser chota-bara karo):
- Fruits first **positions kho** dete, phir basket ke bahar gir jatay, score stuck purana
- Likely cause: Matter.js canvas/`bounds/positions` ko window resize par board geometry update nahi kiye — bodies fixed px coords hote!
- Next session fix: `resize` listener → canvas/ canvas resize, Matter `engine.Bounds/` bodies, wall/floor bodies reposition, positioning scorepark **scale-based clamp**. Physics to fixed timestep rule respect

**4d. Testers phase ads skip (user request).** Khabre ye: ads ko test build meछी EXCLUDE:
- Users double toast aur rough falon na milei, testers ko full game achi chaiye!
- `admob-bridge.js` mein e.g. `FM_TEST_SKIP_ADS=true` / constant bakas skip — har advert skip flag ho, no toast, no reward-blocking — **safi turn on in its release**
- `window.FM_DEBUG` jaisa — sifr dev/test phase mein ON, release build OFF (this destructive phase par Working)
- Alternatives: Play Console "internal test build" diye jaayen separate — direct switch ya seياs ke 45+ minute ka ઘરka plan; don't ---
- Check consistent single toast waghera — never double, exact 1.

### ❌ Pending user-side (Play/AdMob) — INFORM karna is session mein
1. **12 testers opt-in** — Alpha track (v4) ka opt-in link bhulo. **14-day clock jo 12 joined hote hi shuru hoga (12 count)** — 20 nahi, Play ne 12 kiya hai
2. **AdMob → Privacy & messaging → GDPR message Create/Publish** (user ne confirm kiya tha baaki hai)
3. **imperialsolutions.org Search Console ownership** (Play dev profile "website" ka verification request)
4. **Phone QA** — Audit §11 (20+ drops, powers, icons, lag, landscape, sound) — **v4 closed Alpha pe bhi kar sakte hain**
5. **Store screenshots (6)** — power+vol-down se lena and Play listing pe add — ye bhi pending
6. **DP:** `Trader status declared ✓` — new `imperialsolutions.org` web page + Get started ke details (Name decision is legal name/profile) — **USER ne decide nahi kiya hai abhi; daran** saqib ya imram vote pending, optional se waliba
7. **Naya cute/updated icon & feature graphic** — user NE PURANE assets purani bol diya, NEW ART chahiye (AI image gen). **Google Free quota 7 Nov raat khatam had** — retry window next session lasting 13 hrs… **next session pehla image work WITH new prompts!** (icon: merge ka sparkles moment / feature graphic: basket + falling fruits + title "Momo Merge"). Files → exact 512×512 + 1024×500 → Play listing assets replace
8. **GitHub Pages landing page** (root/ to `index.html`) — Play Store "Website" field ka official target (abhi 404 hona hoga!) aur imperialsolutions.org ka match

### ✅ Kitna ho gaya (aaj tak ka, short)
- Local: 9→14 commits total; `main` = `3623493`. All local used phases covered
- CI Run #11 (b0794cb) = **green** with fail-close pipeline (tests→sync→preflight→keystore→AAB artifact verify `fruitmerge-aab` 16MB)
- Pages: `.nojekyll` added — Pages turbo deploys always works (build ne #3 fail kiya tha a lusi, is testi)
- Privacy/deletion/ToS teeno pages insta up ho gaye
- Play Console: App content 11/11 complete (privacy policy, sign-in "No", ads "Yes", content rating, target aud 13+, **data safety** fully declared (email, user ID, ad interactions, GAID, approximate location), financial → "None" (real billing baad ka kaam), health → "No", ads → **Advertising ID declaration "Yes" = required!**, category=Puzzle, contact email=hello@imperialsolutions.org)
- App-level trader: **Yes applies to app** + **Terms of Service URL provided** — submitted
- Account: **trader** declared (Feb 2027 deadline tha, ab kar liya)
- ToS + AI page live

---

## 5. Play Console exact answers (re-derivation na ho, ise copy karo)

**Data safety (final config posted):**
- Collect/share: **Yes**; encrypted in transit: **Yes**; account creation: **OAuth** only
- **Deletion URL** (both fields): `https://helloimperialsolutions.github.io/Momo-Merge/www/account-deletion.html` (404 warning ek bar aaya, 9 min — Pages deploy ke baad clean!)
- Data tiles: **email + user IDs** (Collected only, Optional, App functionality + Account management); **app interactions + Advertising ID + approximate location** (Collected **and shared**, Required, Advertising)
- Partial deletion (without account): link same deletion page, **Yes**

**Advertising ID declaration:** Yes pura + purpose = **Advertising only** ✓ (double ≠ 2 separate declarations)

**Content rating:** questionnaire = Everyone
**Target audience:** 13+ ALL selected; "children appeal" = No
**Financial features:** My app doesn't provide any financial features (diamond packs sirf demo hai)
**Sign-in:** No restricted access ("no part of app is restricted") — core game guest mode full access, koi payment gate nahi
**AI asset declaration:** label "AI-asset made" NEXT step tick — **icon + feature graphic AI-labeled**; screenshots techy REAL device wale (AI-labeled nahi)
**Store listing:** Name: `Momo Merge - Cute Fruit Drop` (28/30). Short desc: "Merge cute fruits into a giant watermelon! A cozy drop-puzzle for everyone." Full desc: 1300-char version written (store desktop, cheez description) — ready copy doc mile
**Category:** Game → Puzzle; contact email: hello@imperialsolutions.org; website: **abhi khali** (Pages root 404 — TRY na karo)

---

## 6. Olt technical implementations — kya-existing indexes mil chuke

- `scripts/check.js` NEW — cross-platform python launcher (python3/python/py -3) + `--extract-only` flag; `npm run check` ✔ dono OS pe (Windows + CI), **Python 3.13.5 window install hai, `py -3` alias**
- `tests/harness.js`: sandbox me **hermetic `fetch` stub** (netCalls[] record karte, `json()` returns []), sab NET_CONFIG paths ko clean, no real network, tests offline se secure
- `scripts/extract.py`: game block pe **NET_CONFIG masking rule** (`re.subn` guard) test copies me URL/key "" ho jate
- 553 tests pass in'saahil local on Python & JS side, might run with CI same pass against local after `npm run check`
- `.nojekyll` root dir — GitHub Pages no-jekyll (bare HTML) build, HYS deploy per Pages
- WhatsApp/Email support URL: not public (user ka ahem ahtee inhi hours windows) — improper flows counter watch

---

## 7. Naye files/dirs health (folders main bhi careful)

| Kya thaya | Kahan |
|---|---|
| Main game runtime | `www/index.html` |
| AdMob bridge | `www/admob-bridge.js` — REWARDED/interstitial ad unit IDs + UMP hooks |
| Privacy / deletion / ToS | `www/privacy-policy.html`, `www/account-deletion.html`, `www/tos.html` |
| Gauss Art assets | `icon-512.png`, `feature-graphic.png` root (+ preview/ dir) — **PURANE, user ne naya mango (AI gen)** |
| Pre-back/ design art | `design/icon-512-v2.png` niche file pending |
| Test harness | `tests/harness.js` (source!) + `tests/fm_*.js` (generated) |
| Extraction + audit scripts | `scripts/extract.py`, `scripts/audit_release.py`, `scripts/check.js` (new) |
| CI Workflow | `.github/workflows/build-android.yml` (fail-closed steps), plus `generate-keystore.yml` (RUN ONCE — do not repeat) |
| Backend schema | `server/supabase.sql` imported ✓ (`server/verify_schema.py` verify auchen) |

---

## 8. Known credentials / environment (non-secret, cabhi)

- Local npm deps: `npm install` ka **sorted** use karo (cap:sync, http-server). **CI uses `npm ci` fail-closed** — **`npx cap sync android` (no build!)** aur local `npm install` na chalana jab kasak break ho
- Node 22.18.0 local, npm registry sync done
- Python: `py -3` works (3.13.5), NO python3 alias local wala alias — `scripts/check.js` this damen handles
- Play pipeline is in the handoff which important plays **developer "IS Studios Official" kholia** muqt jawab

---

## 9. Release status & NEXT steps summary

**Play flow aise hoga:**
```
v4 closed Alpha ✅ (published — 12/12 testers opt-in → 14 day timer → Production apply)
```

**Isa nye session mein pending ka kaam (tumharaأو version):**
1. **Supabase URL Configuration** fix (dashboard, user side 2 min) — **pehla priority**
2. **Android OAuth redirect** app wapas (appUrlOpen + intent-filter) — code
3. **Save progress / Continue button** — code + UI
4. **Resize bug** — Matter.js canvas/bounds — code
5. **Ads skip flag for testers** — code (release pe off!)
6. Naya **cute icon + feature graphic** — AI quota (13h!) timely
7. Pages landing page (`index.html`) for Play website field
8. Sources **imax** `npm run check` before commit + kahn kadaid rules commit sabki

> **Next session — substance bhi lo: Play Console per new status screenshot le ao, aur `git log -5` bhi, code + Play state sath compare karke better effort plan hoga.**

— Har kuch decide hum nakary. Baqi kisi phase sawal khatam ke seypo puche.
