> CURRENT STATUS (2026-11-06): This is a historical implementation log. Some TODOs and orientation notes are obsolete. Read `AUDIT-AND-STATUS.md` first; it is the authoritative current audit/status.

# Workspace Notes — Fruit Merge (2026-10-08)

> **Current update (2026-11-04):** user supplied the AI-update assets and approved
> `com.isstudios.momomerge` as the new package ID. User confirmed no AAB was uploaded
> under the legacy package. See `PACKAGE-ID-MIGRATION.md`; dated notes below may describe
> the earlier project state.

Project transfer se pehla session. Ye file sirf un cheezon ka record hai jo is
workspace mein **nayi** maloom hui — HANDOFF.md waisa hi authoritative hai.

---

## Jo files aayin, jo nahi aayin

| File | Status |
|---|---|
| `www/index.html` | ✅ aayi (143,357 chars) |
| `HANDOFF.md` | ✅ aayi (510 lines) |
| `tests/harness.js` | ❌ **nahi aayi** — is workspace mein dobara likha gaya |
| `tests/fm_matter.js`, `fm_game.js` | ❌ nahi aayin — `scripts/extract.py` se banaye |
| `package.json` | ❌ nahi aaya — dobara likha |
| `capacitor.config.json` | ❌ nahi aaya — dobara likha |

---

## Finding 1 — index.html mein Cloudflare beacon inject tha (hata diya)

File mein **3 script blocks** thay, HANDOFF ke mutabiq 2 hone chahiye thay.

Teesra block (921 chars) game ka hissa nahi tha — ye Cloudflare ka
challenge-platform beacon tha:

```js
window.__CF$cv$params={r:'a472fb845f04c4c3',t:'MTc5MTQzOTgyNg=='}
// -> loads /cdn-cgi/challenge-platform/scripts/jsd/main.js
```

`t` decode hota hai **2026-10-08T06:10:26Z** — yaani jis waqt file browser se
copy ki gayi, us waqt. Ye Cloudflare ne serve karte waqt inject kiya, game ke
code mein nahi tha.

**Nateeja:** `window.__CF$cv$params` ki wajah se game "100% offline" nahi raha
tha — browser har baar `/cdn-cgi/...` se script mangta. Play Store ke WebView
mein ye unnecessary network call hoti. **Hata diya gaya** (938 chars kam).

Verify: ab sirf 2 script blocks, aur file mein koi external URL nahi bacha
siwaye matter.js ke header comment ke.

---

## ⚠️ Finding 2 — HANDOFF ka extract command ab galat hai

HANDOFF §1 mein ye likha hai:

```python
open('fruit-merge/tests/fm_game.js','w').write(b[-1])    # game code
```

`b[-1]` = **aakhri** block. Jab tak beacon maujood tha, `b[-1]` game ki jagah
**Cloudflare beacon** extract karta — yaani test suite galat code test karti.

Beacon hata diya gaya hai to `b[-1]` ab dobara sahi kaam karta hai, **lekin**
ye future-proof nahi. Is liye:

```bash
python3 scripts/extract.py     # b[0] aur b[1] explicitly, aur 2-block assert
```

Ye script **fail ho jati hai** agar block count 2 na ho — taake agli dafa koi
beacon ya analytics snippet chupke se na ghus jaye.

---

## Finding 3 — `// PRODUCTION:` marker maujood hai, lekin block comment hai

HANDOFF kehta hai `// PRODUCTION:` comment hai jahan AdMob call jani hai.
Grep se `// PRODUCTION:` nahi milta kyunke wo `/* ... */` block comment hai,
**line 958** pe (extracted `fm_game.js` mein):

```js
function requestReward(cb){
  var ov=document.getElementById("adOv"), cnt=document.getElementById("adCount");
  ov.classList.remove("hide");
  var n=3; cnt.textContent=n;
  var iv=setInterval(function(){
    n--;
    if(n<=0){ clearInterval(iv); ov.classList.add("hide"); sfxCoin(); buzz(20); cb(); }
    else cnt.textContent=n;
  },800);
  /* PRODUCTION: AdMob.prepareRewardVideoAd({adId:'ca-app-pub-XXXX/YYYY'})
     .then(()=>AdMob.showRewardVideoAd()).then(()=>cb()); */
}
```

TODO #1 (real AdMob) yahin se shuru hoga.

---

## Test harness — is workspace ka version

`tests/harness.js` transfer mein nahi aaya tha, to HANDOFF §8 ki spec se
**dobara likha** gaya. Wahi 9 phases A–I, wahi stub strategy:

- `simT` har frame +16.7 ms
- `setTimeout` instant, `setInterval` fn 5×
- `FakeDate` real constructor (matter.js `+new Date` chalata hai, game
  `new Date()` ke instance methods use karta hai daily seed ke liye)
- `Math = Object.create(Math)`
- overlays (`adOv`, `pauseOv`, `overOv`, `volOv`) pe `hide` class seeded
- `document.body` stub
- **`this` element pe bind** — `volMute` aur `volRange` handlers `this` use
  karte hain, warna crash

Naye additions jo original spec mein nahi thay:
- volume slider `input` event test (`this.value` → `store.vol`)
- `lastDrop` cleared after undo
- rAF queue leak check (phase F)

**Result: 60 assertions, sab pass, phases A–I green.**

Ek reference run: finale score 12,087, bonus +483.

### Do bugs jo harness likhte waqt mile (dono harness ke, game ke nahi)

1. **`this` bind** — `dispatch()` handlers ko bina `this` ke call kar raha tha.
   `volMute` ka handler `this.textContent` set karta hai → TypeError. Asli
   browser mein `this` element hota hai. Fix: `fn.call(el, e)`.
2. **Undo test flaky tha** — sweep ke baad bache hue fruits drop ke baad merge
   ho rahe thay, is liye count 2 kam hota tha (1 undo + 1 merge). Test ab
   clean board pe chalta hai: ek fruit, koi merge partner nahi → delta exactly 1.

**Game ka koi bug nahi mila.** `doUndo()` sirf `lastDrop.body` hatata hai, jo
sahi hai.

---

## Workflow rule (HANDOFF se, ab automated)

```bash
cd fruit-merge
python3 scripts/extract.py && node tests/harness.js
# ya: npm run check
```

Har index.html edit ke baad. **A–I green hone se pehle result nahi dikhaya
jaye ga.**

---

## TODO #2 DONE — orientation lock + wake lock (2026-10-08)

`index.html` mein section **16b** add hua (+2,603 chars):

- `screen.orientation.lock("portrait")` — best-effort, `.catch()` ke sath. Browser
  fullscreen/installed context ke bahar reject karta hai, is liye fail hona normal hai.
- `#rotateOv` — agar device landscape mein ho to Roman Urdu hint ke sath overlay.
  `orientation.type` na mile to `innerWidth > innerHeight` fallback.
- `navigator.wakeLock.request("screen")` PLAY pe, `release()` goHome pe aur
  `visibilitychange` pe. Safari mein `wakeLock` hi nahi — guard se skip ho jata hai.
- Koi call gameplay ko touch nahi karta; sab try/catch mein.

**Phase J** harness mein add hua. Ye zaroori tha: pehli baar tests bina screen
stub ke pass ho rahe thay, yaani guards chup-chaap fail ho rahe thay aur feature
"kaam kar raha hai" lag raha tha jabke kuch nahi ho raha tha. Ab harness
`orientation.lock()` aur `wakeLock.request()` ko **track** karta hai aur prove
karta hai ke dono actually call huay.

Ek asli cheez jo test mein nikli: `requestWake()` ka `.then()` microtask hai, to
`wkSentinel` synchronously assign nahi hota. Harness ko `await flush()` chahiye
tha warna release hamesha fail hota. Browser mein ye masla nahi (wahan frames ke
dauraan microtasks drain ho jate hain) — lekin is se ek real edge case samne aaya:
agar player PLAY daba kar **foran** Home chala jaye, wake lock leak ho sakta hai
kyunke tab tak `wkSentinel` set nahi hua hota. Agle browser playtest mein dekhna.

**Result (Phase J ke baad): 71 assertions, phases A–J, sab pass.**

---

## Phase K — multi-host ad layer (133 assertions, sab pass)

Ek hi `index.html`, chaar ad hosts (CrazyGames v3 / GameDistribution / AdMob /
demo), koi fork nahi. Tests likhte waqt **4 asli game bugs** aur **3 harness bugs**
nikle — tafseel `HANDOFF.md` §8 mein. Sab se ahem: GameDistribution ka
`settle()` ulta condition use kar raha tha, jis se **har poori dekhi gayi ad pe
player ko reward hi nahi milta tha**. Ye production mein tab tak pakda nahi jata
jab tak koi asli GD ad na chalti.

Wake-lock leak wala TODO ab **fix ho gaya** (`requestWake` synchronous release +
`wkGen` generation counter) aur Phase K mein regression test bhi hai — browser
playtest ka intezar nahi karna parega.

`scripts/adlayer.js` ab verified build se regenerate hota hai; us se dobara patch
karo, HTML ka ad section haath se edit mat karo.

---

## UI overhaul + i18n + physics tuning (174 assertions, phases A–L)

User ke 8 items, sab land kiye:

1. **Portrait overlay** ab sirf touch handheld pe aata hai (`isHandheld()` =
   `maxTouchPoints>1 && (pointer:coarse)`). Desktop/PC pe kabhi nahi — wahan
   layout fluid hai aur landscape theek chalta hai.
2. **"Breathing" home dock** fix: `playBig` ki `scale()` animation hata kar
   `box-shadow` glow laga di (flex column mein scale siblings ko hilata tha),
   aur achievements ab apne `#achOv` panel mein hain — pehle 9 achievements ek
   `<p>` mein dump hoti thin jo 6 lines ban kar PLAY button uchhal deti thi.
   `#homeMsg` ki CSS height fixed hai + `.homeBottom` pe `contain:layout style`.
3. **Bara UI**: base font sizes ~25% upar, buttons 44→52 px, score 24→34 px.
4. **NEXT 3**: `q2`/`q3` slots, drop pe rotate + refill, undo sab restore karta
   hai. Canvas 30→104 px chaura (CSS fixed, to reflow nahi).
5. **English + i18n**: poora game English. `STRINGS` table + `T(key, args)` +
   `data-i18n` markup + language button (8 locales listed, sirf `en` translated —
   baqi fallback). `setLang` sab kuch ek call mein repaint karta hai aur
   localStorage mein yaad rakhta hai. RTL (`ar`) ka `dir` bhi set hota hai.
6. **Naya look**: candy-arcade theme — animated gradient backdrop, gradient
   bubbly title, chunky 3px-border buttons hard shadow ke saath.
7. **Achievements panel**: 3×3 tile grid, progress bar, unlocked tiles gold +
   pop animation, locked grayscale.
8. **Physics**: fruit friction `0.55→0.05`, static `0.9→0.12` (chipakne ka asli
   sabab), walls `0.4→0.25`, restitution `0.12→0.2`, speed clamp `15→24`, aur
   render pe sub-step interpolation (`physAlpha`) — 90/120 Hz pe smooth.

**Qaim rakha:** fixed-timestep accumulator, `positionIterations=10`, moti 60 px
deewarein, safety net. Tunnelling (phase E) aur 100-drop stability (phase F)
abhi bhi green — clamp 24 pe bhi koi phal deewar se bahar nahi gaya.

**Naya FM_DEBUG:** `pos()` (sab phal x/y/r), `lang()`, `nlang()`.

---

## Economy system (diamonds / challenges / shop / ranks)

**Source of truth:** `scripts/economy.js` + `scripts/economy.html` +
`scripts/economy.css`. Ye teeno `www/index.html` mein **inject** hote hain —
section `13c` (JS), body markup, aur `<style>` ke andar CSS. Kabhi bhi change
pehle in files mein karo, phir inject; seedha `index.html` pe patch karne se
agli injection use mita deti hai (ye galti `rollPeriod` ke saath ho chuki hai).

**Kya bana:**

| Piece | Detail |
|---|---|
| Currency | **Diamonds** (`store.diamonds`). `addDiamonds(n,why)` / `spendDiamonds(n)` — dono `save()` + `refreshEcon()` karte hain |
| Free daily | **10/day**, `takeDailyFree()`, calendar-day key pe reset |
| Ads | **50 per ad**, **5 ads/day** (250 max). `grantAdDiamonds()` → `requestReward()` se wrapped, to har portal host pe chalta hai |
| Achievements | Har unlock pe **15 diamonds**, `store.ach[k]` flag once-guard hai |
| Daily challenges | **3**, 7-type pool se day-key seeded |
| Weekly challenges | **6**, week-key seeded, **target 3–12× bara** aur **reward 2.5×** |
| Shop | bomb 60 · sweep 40 · undo 30 · freeze 45 — **sab `store.inv` (persistent)** mein credit hote hain |
| Spending order | `spendPower(k,fn)`: **free per-round → paid inventory → ad**. Isliye khareedari kabhi bekaar nahi jati |
| Bomb button | `#bombBtn` toolbar mein — aim slot ke phal ko `{st:2,sp:1}` banata hai (wahi shape jo random queue banata hai) |
| Diamond packs | 4 tiers, **demo only** — koi billing wired nahi |
| Profile | Naam 2–16 chars, **haftay mein ek baar** change (`NAME_COOLDOWN_DAYS=7`) |
| Leaderboard | daily / weekly / all-time, **20 rows per page**, up/down arrows, **hard cap 500** |
| Home pill | `#diaPill` — live balance + `+`, tap pe diamonds panel khulta hai |
| Sign-in invitation | `#signIn` home screen pe — **sirf tab jab `netOn()` true ho** (warna Google login mumkin hi nahi, button jhoot bolta). Dismissible, `store.siDismissed` persist hota hai |

**Server seam:** `NET_CONFIG = {url:"",key:""}`. Khaali = **guest mode**
(default): sab kuch `localStorage` pe, leaderboard sirf player ka apna score.
Supabase URL/key bharne pe `Net.login()` / `lbFetch()` live ho jate hain —
**game ka koi code branch nahi karta**, sirf `netOn()` dekhta hai. Isliye
portal build (CrazyGames/GD) aur APK build dono ek hi file se bante hain.

**Period peaks:** `store.periodBest` / `periodCombo` / `weekBest` week-key
change pe `rollPeriod()` se zero hote hain — warna pichle hafte ka 9,000 score
is hafte ki challenge free mein claim ho jati.

**Naya FM_DEBUG:** `econ()`, `chProg(kind,id)`, `chList()`, `setDia(n)`,
`claim(kind,id)`, `buy(id)`, `watchAd()`, `takeFree()`, `setName(n)`,
`rollPeriod()`, `achCount()`, `checkAchNow()`, `lbSeed(rows)`, `lbGo(dir)`,
`lbRefresh()`, `mergeTwo()`, `achReset()`, `over()`.

**Phase M = 42 test groups (M1–M42)**, total suite **405 assertions green**.
(Runtime count, na ke static `ok()` count — kuch assertions loops ke andar hain
to source grep se number kam aata hai.) Sabse bara sabak HANDOFF §8 mein hai:
economy inject hone ke baad suite **174/0 green** thi aur wo **jhoot** tha —
34 naye ids harness ke `IDS` list mein nahi thay, to har null-guarded call site
chup-chaap skip ho rahi thi. Ids add karte hi 17 failures nikle (15 meri test
bugs, **2 asli product bugs**).

---

## Server side (Supabase) — `server/`

Do files, dono **optional**. Inke baghair game poora chalta hai (guest mode).

| File | Kya hai |
|---|---|
| `server/supabase.sql` | `scores` table + RLS policies + indexes + trigger. Supabase SQL editor mein paste karke Run |
| `server/README.md` | Poora setup: project → schema → Google OAuth → `NET_CONFIG` |

**Contract** (schema aur client bilkul match karte hain — programmatically
verify kiya gaya):

```
POST /rest/v1/scores   {name, score_all, score_day, score_week, day_key, week_key}
                       Prefer: resolution=merge-duplicates
GET  /rest/v1/scores?select=name,<col>&order=<col>.desc&limit=500
                       [&day_key=eq.<k>&<col>=gt.0 | &week_key=eq.<k>&<col>=gt.0]
```

**Do design decisions jo bhoolne layak nahi:**

1. **`name` pe UNIQUE constraint mat lagana.** Client `resolution=merge-duplicates`
   bhejta hai bina `on_conflict` ke, to PostgREST table ke **ek** unique
   constraint se target infer karta hai. Doosra unique index lagaya to har
   score write HTTP 400 dega. Aur ek player doosre ka naam block kar dega.

2. **`day_key`/`week_key` filter columns hain, cron job nahi.** Server pe
   counters kabhi zero nahi hote — har row us period ki mohar rakhti hai jis
   mein wo set hui. Purani row bas aaj ke filter se match karna band kar deti
   hai. Isliye koi scheduled job nahi chahiye jo chup-chaap fail ho sake.

**Auth:** `apikey` = anon key (project ki pehchan), `Authorization: Bearer` =
player ka apna token. Detail HANDOFF §8 "Auth ka sabak" mein.

**Verify nahi hua** (yahan Postgres aur real Google credentials nahi hain):
SQL syntax · RLS ka forged write rokna · OAuth round trip. `server/README.md`
ke aakhir mein teen manual test likhe hain jo Supabase pe chalane hain.

---

## Storage

Workspace cap 128 MB. Ye project ~460 KB hai. Koi masla nahi.

## [2026-10-10] Storybook redesign
- `design/` = approved mockups (mock-home, mock-board). `www/index.html` me "STORYBOOK SKIN" override layer + wooden-crate board.
- Warm tokens: paper #faf3e1, ink #54371f, coral #ee7a5c. Revert point `/tmp/pressyle.html`.

## [2026-10-10] Mobile conversion + deployment docs
- Capacitor Android platform generated: `android/` (appId com.sukoonstudio.fruitmerge). targetSdk/compileSdk bumped 35→36 (Play mandatory since 31 Aug 2026).
- AdMob: @capacitor-community/admob@7.2.0 installed+registered; `www/admob-bridge.js` maps plugin→window.AdMob (game already had adAdMob branch). TEST IDs by default; replace before prod. Bridge inert on web → harness unaffected (405/0).
- `www/privacy-policy.html` template added. `DEPLOY-GUIDE.md` = full step-by-step (web/mobile/Play/portals/checklist).
- Cannot verify here: live AdMob ad (needs device), AAB build (needs Android Studio). Both documented.
