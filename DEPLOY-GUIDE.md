# Momo Merge: Cute Fruit Drop — Complete Build & Publish Guide

A single, self-contained HTML5 game that ships to **three places from one codebase**:
your **website/browser**, the **Google Play Store** (via Capacitor → Android APK/AAB), and
**HTML5 portals** (CrazyGames, GameDistribution, itch.io).

> **Roman-Urdu TL;DR (quick map):**
> 1. **Web chalana:** `npm install` → `npm start` → browser me `http://localhost:8081`. Test: `npm run check` (405 tests green hone chahiye).
> 2. **Mobile (Play Store):** project pehle se Capacitor ke saath ready hai (`android/` folder bana hua hai, AdMob plugin laga hua hai). Android Studio me `android/` kholo → phone par chalao → signed **AAB** banao → Play Console par upload.
> 3. **Portals:** `www/` folder ka zip banao, CrazyGames/GD par upload karo, aur unka SDK `<script>` tag add karo (guide me exact line hai).
> 4. **Zaroori cheezein jo log bhool jate hain:** Privacy Policy, Data-Safety form, Content Rating, **12 testers × 14 din** (naye personal Play accounts), signing **keystore ka backup**, aur AdMob ke **real IDs** (abhi test IDs lage hain). Sab neeche detail me hai.

---

## Table of contents
1. [What's in the box (project map)](#1-whats-in-the-box)
2. [The golden rule (edit → extract → test)](#2-the-golden-rule)
3. [Prerequisites — install once](#3-prerequisites--install-once)
4. [PART A — Run & test the WEB version](#part-a--web)
5. [PART B — Convert to MOBILE (Capacitor)](#part-b--mobile-capacitor)
6. [PART C — Build the signed AAB](#part-c--build-the-signed-aab)
7. [PART D — Publish on Google Play](#part-d--publish-on-google-play)
8. [PART E — Ads (AdMob on mobile, SDKs on portals)](#part-e--ads)
9. [PART F — Publish on portals](#part-f--publish-on-portals)
10. [PART G — Master checklist (things people forget)](#part-g--master-checklist)
11. [Shipping an update (v1.1, v1.2…)](#11-shipping-an-update)
12. [Troubleshooting](#12-troubleshooting)
13. [Reference (commands, economy, ad hooks)](#13-reference)

---

<a name="1-whats-in-the-box"></a>
## 1. What's in the box (project map)

```
fruit-merge/
├─ www/                      ← THE GAME (this exact folder ships everywhere)
│  ├─ index.html             ← the whole game: UI + physics + economy (single file)
│  ├─ admob-bridge.js        ← AdMob adapter, ONLY active in the Android build
│  ├─ privacy-policy.html    ← your privacy policy (fill in the [BRACKETS])
│  └─ assets/                ← background art (bg-portrait / bg-landscape)
├─ android/                  ← the native Android app (Capacitor). Open in Android Studio.
│  └─ app/src/main/
│     ├─ AndroidManifest.xml ← permissions + AdMob App ID live here
│     └─ assets/public/      ← a COPY of www/ (refreshed by `npx cap sync android`)
├─ capacitor.config.json     ← app id, name, splash/status-bar colours
├─ package.json              ← scripts + Capacitor/AdMob dependencies
├─ scripts/                  ← source pieces + the extractor (see §2)
├─ tests/harness.js          ← the 405-check test suite
├─ server/supabase.sql       ← OPTIONAL backend (leaderboard/login). NOT required.
├─ design/                   ← the approved storybook mockups
└─ HANDOFF.md                ← engineering notes (what/why of the code)
```

**Key idea:** the game is one file — `www/index.html`. It contains everything and needs
**no server and no internet** to play. The `android/` app is just a thin native shell
(a WebView) that loads that same file. So when you fix the game, you fix it once, then
"push" it to the app with one command (`npx cap sync android`).

The optional `server/supabase.sql` is a schema for a cloud leaderboard/login. **The
shipped build does NOT use it** — scores and progress are stored locally on the device.
Ignore it unless you later want a global online leaderboard.

---

<a name="2-the-golden-rule"></a>
## 2. The golden rule (edit → extract → test)

`www/index.html` is the real source. The test suite runs against an **extracted** copy of
the game logic (`tests/fm_game.js`), produced by `scripts/extract.py`.

**Any time you change `www/index.html`, run this before you trust it:**

```bash
cd fruit-merge
python3 scripts/extract.py        # re-extract the game logic from index.html
node tests/harness.js             # run all 405 checks
# shortcut that does both:
npm run check
```

You want to see:

```
PASSED: 405   FAILED: 0
```

If you skip the extract step, the tests run the **old** logic and lie to you. This is the
single most common mistake on this project.

---

<a name="3-prerequisites--install-once"></a>
## 3. Prerequisites — install once

| Tool | Needed for | Get it |
|---|---|---|
| **Node.js 18+** (you have v20) | running tools, Capacitor | nodejs.org |
| **Python 3** | the extractor / test harness | already installed |
| **Android Studio** (latest) | building the Android app | developer.android.com/studio |
| **Android SDK Platform 36** | required by Play (see below) | inside Android Studio → SDK Manager |
| **A Google account + $25** | Play Console (one-time) | play.google.com/console |
| **AdMob account** (free) | mobile ads / revenue | admob.google.com |
| **JDK 17+** | Gradle builds | bundled with Android Studio |

**Inside Android Studio → Tools → SDK Manager**, install:
- **Android SDK Platform 36**
- **Android SDK Build-Tools** (latest)
- **Android SDK Command-line Tools**

> **Why API 36?** Since **31 August 2026**, Google Play requires every **new app and update**
> to **target Android 16 (API level 36)**. A build targeting API 35 or lower is **rejected on
> upload**. This project is already set to `compileSdk = 36` and `targetSdk = 36`
> (`android/variables.gradle`), so you are compliant out of the box.

---

<a name="part-a--web"></a>
## PART A — Run & test the WEB version

### A1. Run it locally
```bash
cd fruit-merge
npm install          # first time only
npm start            # serves www/ at http://localhost:8081
```
Open **http://localhost:8081** in your browser. (No internet needed to play — only to show
portal ads, which are replaced by a built-in demo ad when no portal is present.)

### A2. Test it
```bash
npm run check        # → PASSED: 405   FAILED: 0
```

### A3. Test on your phone (same Wi-Fi)
Find your PC's local IP (`ipconfig` on Windows, `ip addr` on Linux/Mac), then on your phone
visit `http://YOUR-PC-IP:8081`. This checks the mobile/portrait layout without building an app.

### A4. Publish the web version (free hosting)
The `www/` folder is a static site — host it anywhere free:

- **GitHub Pages:** push `www/` to a repo → Settings → Pages → deploy from branch. Your
  `privacy-policy.html` is then live at `https://you.github.io/repo/privacy-policy.html`.
- **Netlify / Cloudflare Pages / Vercel:** drag-and-drop the `www/` folder, or connect the repo.
- **Your own domain:** upload `www/` to any web host / cPanel `public_html`.

That's it — the web version is just the folder.

---

<a name="part-b--mobile-capacitor"></a>
## PART B — Convert to MOBILE (Capacitor)

**Good news: this is already done for you.** The `android/` project exists, the AdMob plugin
is installed and registered, the web assets are copied in, and the manifest is configured.
You mainly need to *open* it and *build* it.

### How it works (30-second mental model)
[Capacitor](https://capacitorjs.com) wraps your web game in a native Android **WebView** and
exposes native features (ads, haptics, status bar) to the JavaScript. One game, native app.

### B1. What is already configured
- **App ID:** `com.sukoonstudio.fruitmerge` (change it in `capacitor.config.json` **before your
  first build** if you want a different package name — you **cannot** change it after publishing).
- **App name:** "Momo Merge: Cute Fruit Drop".
- **targetSdk / compileSdk:** 36 (Play-compliant).
- **minSdk:** 23 (Android 6.0+) — covers ~99% of devices.
- **Orientation:** unlocked — works in **portrait and landscape** (never portrait-only).
- **AdMob plugin:** installed; the app shows **test ads** until you add real IDs (see PART E).

### B2. Refresh the app with your latest game
Whenever you edit `www/`, push it into the Android project:
```bash
cd fruit-merge
npx cap sync android      # copies www/ → android, updates plugins
```

### B3. Open in Android Studio
```bash
npx cap open android
```
(Or open Android Studio → **Open** → select the `fruit-merge/android` folder.)

The first open downloads Gradle + dependencies — let it finish (a few minutes, one time).

> **If Android Studio prompts to "Upgrade Android Gradle Plugin" or "Gradle":** click
> **Accept / Upgrade Assistant**. Compiling against SDK 36 sometimes wants a newer plugin than
> the bundled 8.7.2. Accepting is safe.

### B4. Run it on a real phone (recommended) or emulator
- **Real phone (best):** enable **Developer options → USB debugging**, plug in via USB,
  select your device in Android Studio's toolbar, press **Run ▶**.
- **Emulator:** Android Studio → **Device Manager** → create a Pixel device → Run ▶.

Play a full game: check both portrait and landscape, the shop, the lucky spinner, and that a
**test ad** appears when you tap a "watch ad" button.

### B5. App icon & splash screen (do this before publishing)
Capacitor put a default icon in. Replace it with your own:
1. Make a **1024×1024 PNG** icon (and optionally a 2732×2732 splash) — put them in
   `fruit-merge/assets/` as `icon.png` / `splash.png`.
2. Run:
   ```bash
   npx @capacitor/assets generate --android
   ```
   This regenerates every icon density + splash automatically. Then `npx cap sync android`.

---

<a name="part-c--build-the-signed-aab"></a>
## PART C — Build the signed AAB

Google Play needs a **signed Android App Bundle (.aab)**. Signing needs a **keystore** —
**treat it like a bank key: if you lose it, you can never update the app.**

### C1. Create your keystore (once, keep it safe)
```bash
keytool -genkey -v -keystore fruitmerge-release.keystore -alias fruitmerge \
  -keyalg RSA -keysize 2048 -validity 10000
```
Answer the prompts. **Back up `fruitmerge-release.keystore` + its password somewhere safe
(password manager + cloud).** Never commit it to a public repo.

### C2. Build the AAB in Android Studio (easiest)
1. **Build → Generate Signed App Bundle / APK…**
2. Choose **Android App Bundle** → Next.
3. Select your keystore, enter the passwords, alias `fruitmerge`.
4. Build variant: **release** → **Create**.
5. The `.aab` is at `android/app/release/app-release.aab`.

### C3. Or build from the command line
Add your signing details to `android/app/build.gradle` (or use a `keystore.properties` file),
then:
```bash
cd android
./gradlew bundleRelease
# output: android/app/build/outputs/bundle/release/app-release.aab
```

> Prefer **Play App Signing** (Google manages a second key) — enable it in Play Console. Then
> even if you lose your upload key you can recover via Google.

---

<a name="part-d--publish-on-google-play"></a>
## PART D — Publish on Google Play

### D1. Create the developer account (one-time, $25)
1. Go to **play.google.com/console**, sign in with a Google account.
2. Choose a **Personal** account, pay the **US$25** one-time fee, complete identity verification.

> **⚠️ The 12-tester rule (personal accounts).** For personal accounts created **after
> 13 Nov 2023**, before your app can go to **Production** you must run a **closed test with at
> least 12 testers who have continuously opted-in for 14 days.** Plan for this — recruit 12
> friends/family with Google accounts, add them as testers, and wait out the 14 days. This is
> the #1 thing that stalls first-time publishers.

### D2. Create the app
**Create app** → Name: *Momo Merge: Cute Fruit Drop* → Default language → **App** → **Free**.

### D3. Fill in the store listing
Under **Grow → Store presence → Main store listing**:
- **App name** (≤30 chars), **Short description** (≤80), **Full description** (≤4000).
- **App icon:** 512×512 PNG (32-bit, ≤1 MB).
- **Feature graphic:** 1024×500 PNG/JPG.
- **Screenshots:** at least 2 phone screenshots (16:9 or 9:16, ≤8 each). Add a 7" and 10"
  tablet screenshot too if you can.
- (Optional) Promo video URL.

### D4. Required declarations (App content) — do NOT skip
Under **Policy → App content**, complete every card:
1. **Privacy policy** — paste your hosted URL (from `privacy-policy.html`, §Part A4).
2. **Data safety** — declare what the app collects. For this game:
   - App functionality data: **none sent to your servers** (progress is local-only).
   - **Advertising ID** — *collected* (for ads via AdMob), not shared with you personally.
   - Answer the "is data encrypted / can users request deletion" questions honestly
     (local storage = nothing leaves the device; ads are handled by Google).
3. **Content rating** — complete the IARC questionnaire. A cute, non-violent merge puzzle
   will typically rate **Everyone / PEGI 3**. Answer truthfully.
4. **Target audience & content** — pick your age groups. **Important decision:**
   - If you include **children** (under 13), you must follow the **Families** policy: use only
     Families-certified ad SDKs and serve **non-personalized** ads to kids. Configure AdMob
     accordingly (PART E).
   - If it's a **general/teen+** audience, declare that instead. Either is fine — just be
     consistent across Data safety, Content rating, and AdMob settings.
5. **Ads** — declare **"Yes, my app contains ads."**
6. **App access** — if reviewers need anything special, say so. (This game needs nothing.)

### D5. Upload & test (the track ladder)
1. **Testing → Internal testing** → create a release → upload your `.aab` → roll out to
   yourself first. Install via the opt-in link and smoke-test on a real phone.
2. **Testing → Closed testing** → add your **12 testers** → let it run **14 days** (the rule above).
3. **Production** → create release → promote the tested build → **Send for review**.

Review usually takes **a few hours to ~7 days**. Watch **Policy status** for any warning
(e.g. the target-API warning means an old AAB is still in a track — deactivate it).

### D6. After it's live
- **Monetization → set up AdMob** linkage (PART E) so revenue starts.
- Check **Android vitals** (crashes/ANRs) after a few days.

---

<a name="part-e--ads"></a>
## PART E — Ads

The game has a **single ad switch** (`detectHost()` in `index.html`). It automatically picks
the right provider for where it's running:

```
1. window.FM_HOST override  → forced (used by tests)
2. CrazyGames SDK present   → CrazyGames rewarded ads      (portal)
3. gdsdk present            → GameDistribution rewarded    (portal)
4. Capacitor + window.AdMob → AdMob rewarded ads           (Play Store)
5. otherwise                → built-in "demo" ad           (safe fallback, never blocks)
```

Rewards are **only** granted on the correct success callback for each provider, and the game
always survives a failed/blocked ad. **This logic is already written and tested** — you only
supply IDs.

### E1. Mobile (AdMob) — already wired, just add real IDs
The Android app already includes the **@capacitor-community/admob** plugin and a bridge
(`www/admob-bridge.js`) that connects it to the game. Right now it uses **Google's official
TEST IDs**, so a debug build shows test ads. **Before a production release:**

1. In **AdMob**, create an **App** (Android) → copy the **App ID**.
   Paste it into `android/app/src/main/AndroidManifest.xml`:
   ```xml
   <meta-data
       android:name="com.google.android.gms.ads.APPLICATION_ID"
       android:value="ca-app-pub-YOUR-REAL-APP-ID" />
   ```
2. In AdMob, create **three** ad units (the game uses all three formats):
   - **Rewarded** → powers / diamonds / continue (`FM_ADMOB_REWARDED` — already set: `.../7199766849`)
   - **Interstitial** → shown at game over (1st game, then every 3rd) (`FM_ADMOB_INTERSTITIAL`)
   - **Banner** → always-on strip at the very bottom (`FM_ADMOB_BANNER`)

   Put each ID in `www/admob-bridge.js` (replace the defaults) or set them in `index.html`:
   ```js
   window.FM_ADMOB_REWARDED     = "ca-app-pub-XXXX/YYYY";   // your rewarded unit
   window.FM_ADMOB_INTERSTITIAL = "ca-app-pub-XXXX/YYYY";   // your interstitial unit
   window.FM_ADMOB_BANNER       = "ca-app-pub-XXXX/YYYY";   // your banner unit
   ```
   **Done (17 Oct 2026):** all three real units are already set in `www/admob-bridge.js` —
   Rewarded `.../7199766849`, Interstitial `.../5362484723`, Banner `.../4472074881`.
3. `npx cap sync android`, rebuild the AAB (PART C), upload.

> **AdMob payments:** to actually get paid, in AdMob add your **payment profile**, complete the
> **W-8BEN** tax form (otherwise 30% US withholding), and expect a **PIN postcard** to verify
> your address (3–6 weeks) before payout. Payout threshold is **US$100**.

> **Testing note:** the bridge is verified against plugin **v7.2.0** (correct method + event
> names), but a live ad can only be confirmed **on a real device** — the headless test harness
> can't show ads. Test with the TEST IDs first, then swap to real ones.

### E1b. Google Sign-In (free, ~5 minutes)

The game already contains the full login scene (official "Sign in with Google"
buttons, session, sign-out). It switches on with one free value:

**Website / own domain (works today):**
1. Go to https://console.cloud.google.com -> create a project (e.g. "Momo Merge").
2. **APIs & Services -> OAuth consent screen** -> External -> app name "Momo Merge"
   -> save (no scopes needed beyond the defaults).
3. **APIs & Services -> Credentials -> Create Credentials -> OAuth client ID**
   -> **Web application**.
4. Under **Authorized JavaScript origins** add your site (and `http://localhost`
   if you test locally).
5. Copy the **Client ID** and paste it into `www/index.html`:
   `var GOOGLE_CLIENT_ID = "...apps.googleusercontent.com";`
   **Done (17 Oct 2026):** Client ID `317257394408-...03p8lj.apps.googleusercontent.com`
   is already set as the shipped default.
6. Re-upload the site (or `npx cap sync` + rebuild for the app). Done — the
   Google buttons now open the real Google sign-in, the profile takes the
   player's Google name, renaming unlocks, and the session survives reloads.
   ⚠️ The origin serving the game (your website domain, `http://localhost`
   for testing) must be listed under **Authorized JavaScript origins** for
   that Client ID, or Google refuses the sign-in on that origin.

**Android app (at AAB build time):** Google blocks OAuth inside WebViews, so the
app uses Firebase Authentication instead — the game already calls the plugin
when a build ships it:
1. https://console.firebase.google.com -> Add project -> add an **Android app**
   with package `com.sukoonstudio.fruitmerge`.
2. Add the SHA-1 fingerprint (Play Console -> App signing, or your release
   keystore) and download **google-services.json** into `android/app/`.
3. In Firebase -> Authentication -> enable the **Google** provider.
4. `npm i @capacitor-firebase/authentication firebase` then `npx cap sync android`.

Portals (CrazyGames / GameDistribution) give players portal accounts instead —
the Google buttons simply stay in guest mode there.

### E2. Web portals — add the portal's SDK `<script>`
The game **detects** a portal SDK but does **not** ship the SDK (each portal wants its own).
For a portal build, add the portal's script **before the game script** in `index.html`.

- **CrazyGames** (the game already calls `gameplayStart/Stop` + rewarded correctly):
  ```html
  <script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>
  ```
- **GameDistribution** — set your gameId, then load their SDK:
  ```html
  <script>
    window.GD_OPTIONS = { gameId: "YOUR_GD_GAME_ID", onEvent: function(){} };
  </script>
  <script src="https://html5.api.gamedistribution.com/main.min.js"
          id="gamedistribution-jssdk"></script>
  ```

Make a **separate copy** of `index.html` per portal (or keep the SDK tags in the portal zip
only) so your own website stays SDK-free.

---

<a name="part-f--publish-on-portals"></a>
## PART F — Publish on portals

Portals want a **ZIP** of the web build. From inside `www/`:
```bash
zip -r fruitmerge-web.zip index.html assets admob-bridge.js privacy-policy.html
```
(`admob-bridge.js` is harmless on portals — it stays inert without Capacitor.)

### F1. CrazyGames — developer.crazygames.com
1. Create a **developer account** (free).
2. **Upload** the ZIP; it auto-detects `index.html`.
3. Add the CrazyGames SDK tag (§E2) to the uploaded build.
4. Fill the listing (title, description, tags, thumbnails).
5. Submit for **QA** (usually 1–2 days). New games start in **Basic Launch** (no ads/revenue)
   and graduate to **Full Launch** after they meet playtime/retention thresholds.
- **Limits:** 50 MB initial download, 250 MB total, ≤1500 files. **No exclusivity** required.
- **Payout:** via Tipalti, €100 monthly minimum.

### F2. GameDistribution — gamedistribution.com
1. Register as a developer, **create a game** → get a **gameId**.
2. Turn on the **rewarded** flag for the game (else no ad fill).
3. Add the GD SDK tag + your gameId (§E2), upload the ZIP.
4. GD distributes to 4000+ portals; you earn **~33% of net**, €100 threshold.

### F3. itch.io — itch.io (easiest, also good for a portfolio link)
1. Create an account → **Upload new project**.
2. Kind of project: **HTML**. Upload the ZIP, mark `index.html` as the entry.
3. Set **embedding** on, choose a viewport size, publish (free or "name your price").
4. You set the revenue cut (default 10% to itch).

### F4. Also worth it (free, later)
**Poki** (curated, invite/apply — strict 8 MB initial download), **Playgama**, **Y8**,
**Newgrounds**. Same ZIP approach.

---

<a name="part-g--master-checklist"></a>
## PART G — Master checklist (things people forget)

**Before you upload to Play:**
- [ ] App ID (`com.sukoonstudio.fruitmerge`) is final — **cannot change after publishing**.
- [ ] Custom **app icon + splash** (not the Capacitor default).
- [ ] `privacy-policy.html` filled in **and hosted** at a real URL.
- [ ] **Data safety** form completed (Advertising ID declared).
- [ ] **Content rating** questionnaire completed.
- [ ] **Target audience** chosen (and AdMob family/non-personalized set if kids are included).
- [ ] **Ads declaration** = "contains ads".
- [ ] Real **AdMob App ID** in manifest + real **rewarded unit** id (not the test IDs).
- [ ] **Keystore backed up** (+ password). Enable **Play App Signing**.
- [ ] Build **targets API 36** (already set — just don't downgrade it).
- [ ] **12 testers lined up** for the 14-day closed test.
- [ ] Smoke-tested a full game on a **real phone** (portrait + landscape + one ad).
- [ ] `npm run check` → **405 / 0**.

**Before you upload to a portal:**
- [ ] Portal **SDK `<script>`** added with the correct gameId.
- [ ] ZIP built from the current `www/`.
- [ ] Runs cleanly with an **ad-blocker** and with the **SDK missing** (the demo ad covers this).

---

<a name="11-shipping-an-update"></a>
## 11. Shipping an update (v1.1, v1.2…)

```bash
# 1. edit www/index.html
# 2. verify
npm run check                       # 405 / 0

# 3. push to the app
npx cap sync android

# 4. bump the version (Play requires a HIGHER versionCode every upload)
#    android/app/build.gradle → versionCode 2, versionName "1.1"

# 5. build a new signed AAB (PART C) and upload to a track
```
For the **web/portals**, just redeploy `www/` (and re-upload the ZIP to each portal).

> **versionCode** must strictly increase with every Play upload, or the upload is rejected.

---

<a name="12-troubleshooting"></a>
## 12. Troubleshooting

| Problem | Fix |
|---|---|
| Tests show old behaviour after an edit | You forgot `python3 scripts/extract.py`. Run `npm run check`. |
| "App must target Android 16 (API 36)" warning on Play | An old AAB is still in a track. Deactivate it, upload the API-36 build. |
| Android Studio: "compileSdk 36 requires newer AGP" | Accept the **AGP/Gradle upgrade** prompt. |
| Gradle build fails first time | Let Android Studio finish downloading Gradle; check SDK Platform 36 is installed. |
| Ads don't show in the app | You're still on TEST IDs (fine for testing), or the real App ID isn't in the manifest, or no network. Test IDs always fill. |
| AdMob "no fill" on production | New ad units take a few hours–days to start filling. |
| Portal shows no ads | SDK `<script>` missing or wrong gameId; or you're in Basic Launch (CrazyGames). |
| App icon looks wrong | Re-run `npx @capacitor/assets generate --android` then `npx cap sync android`. |
| Screen stuck in one orientation | It shouldn't be — orientation is unlocked. Check you didn't add `screenOrientation` to the manifest. |

---

<a name="13-reference"></a>
## 13. Reference

**Everyday commands**
```bash
npm install                 # first time
npm start                   # run web at :8081
npm run check               # extract + run all 405 tests
npx cap sync android        # push www/ into the Android app
npx cap open android        # open in Android Studio
```

**Key files to edit**
| To change… | Edit |
|---|---|
| App name / package id / colours | `capacitor.config.json` (+ `android/.../strings.xml`) |
| AdMob App ID | `android/app/src/main/AndroidManifest.xml` |
| Rewarded ad unit id | `www/admob-bridge.js` |
| target/compile/min SDK | `android/variables.gradle` |
| version for Play | `android/app/build.gradle` (`versionCode` / `versionName`) |
| The game itself | `www/index.html` (then `npm run check`) |

**Current economy numbers** (in `www/index.html`): shop bomb 60 / sweep 40 / undo 30 /
freeze 45 diamonds; daily free 10; rewarded ad = 50 diamonds; leaderboard page 20, max 500.

**Portal economics (for planning):** CrazyGames ≈ 60% ad share, no exclusivity, €100 payout
minimum. GameDistribution ≈ 33% of net. itch.io = you set the cut (default 10%). A typical
casual portal game earns roughly **$200–$2,000/month** if it finds an audience.

**One codebase, three destinations** — web, Play Store, portals. Fix the game once in
`www/index.html`, test it (`npm run check`), then `cap sync` for the app and redeploy the
folder for the web.
