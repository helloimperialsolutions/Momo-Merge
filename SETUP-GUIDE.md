# Momo Merge — Sign-in & Ads Setup Guide
*(Ye tumhare accounts banane ke lafzi steps hain. Jo 2 chezen collect hongi, mujhe dena — baqi wiring main karunga.)*

---

## Part 1: Google Sign-in ON karna (`NET_CONFIG`)

### Step 1 — Supabase project banao (free, ~5 min)
1. https://supabase.com pe sign up / login (GitHub se ho sakta hai)
2. **New project** → Name: `momo-merge`, strong DB password save kar lo, region: Singapore (Pakistan ke liye fastest)
3. Project ready hone ke baad: **Project Settings → API**
   - `Project URL` copy karo
   - `anon public` key copy karo (ye secret NAHI hai project id hai, safe hai)

### Step 2 — Database schema import karo
1. Supabase dashboard mein **SQL Editor** kholo → **New query**
2. `server/supabase.sql` file ka poora content paste karo → **Run**
3. 0 errors aiye to done ✅ (verification main khati hai `server/verify_schema.py`)

### Step 3 — Google OAuth credentials banao
1. https://console.cloud.google.com → **New Project**: `Momo Merge`
2. Left menu → **APIs & Services → OAuth consent screen**
   - External → App name `Momo Merge` → support email → Save (scopes skip)
   - **Test users** mein apni Google email add karo
3. **Credentials → Create Credentials → OAuth client ID**
   - Type: **Web application**
   - Authorized redirect URIs mein add karo (Supabase *ka apna* URL hota hai):
     ```
     https://<supabase-project-ref>.supabase.co/auth/v1/callback
     ```
     (exact `<supabase-project-ref>.supabase.co` tumhare Supabase URL se aayega)
   - **Client ID + Client Secret** save karo
4. Supabase → **Authentication → Providers → Google** → ON → Client ID + Secret paste → Save
   - URLs (Redirect URL, Site URL) config main tum se confirm karaunga

### Step 4 — Mujhe ye 2 chezen bhejo
```
SUPABASE_URL     = https://xxxx.supabase.co
SUPABASE_ANONKEY = eyJhb... (anon public key)
```
Main phir: `NET_CONFIG` fill + `verify_schema.py` run + sign-in flow ka full test karunga. Ranks (leaderboard) aur cloud save isi se live ho jayega! 🎯

---

## Part 2: Ads release-ready karna (UMP consent + real IDs)

**STATUS: ✅ DONE (6 Nov 2026)** — real App ID + 3 unit IDs wired & confirmed, UMP consent gate added (fail-closed: bina consent ad request NAHI jayega), `showPrivacyOptions` hook added. Commit `c048bd7`.
**Bacha sirf:** AdMob console → Privacy & messaging → GDPR message create (UMP form tabhi dikhega), device-side QA (list niche), Play Console Data Safety + trader status.

### Mujhe AdMob console se ye 4 values bhejo
1. **App ID** (`ca-app-pub-XXXX~YYYY`) — AdMob → Apps → App settings
   *(agar app registered nahi: AdMob → Apps → Add app → Android → Play link)*
2. **Rewarded unit ID** (`ca-app-pub-XXXX/YYYY`) — AdMob → Ad units → Rewarded
3. **Interstitial unit ID**
4. **Banner unit ID** (Adaptive)

> ⚠️ AdMob App ID AndroidManifest mein jata hai; unit IDs code mein — main dono jagah wire kar dunga. Policy: **apne ads click karna forbidden hai** — phone pe test ke waqt sirf dekho, click mat karo (revenue claim bhi na karna test pe).

### Jo main karunga tumhari IDs aane pe
1. `admob-bridge.js` mein `FM_ADMOB_REWARDED` (test placeholder) → tumhari real ID
2. `AndroidManifest.xml` AdMob **App ID** meta-data verify/update
3. **UMP consent** (GDPR) flow add karna — @capacitor-community/admob ke consent methods se, pehli launch pe consent form
4. `initializeForTesting:false` rehne dunga (already false) aur device build test checklist dunga

### Play Console side (tum karo, main guide doonga)
- Data Safety form: AdMob SDK data collection declare karna
- AdMob ↔ Play app association verify
- Trader status declaration (banner pe pending hai)

---

## Part 3 (baad ka kaam — filhal demo hai)
- [ ] Real Google Play Billing (merchant + products + validation) — fresh session
- [ ] Privacy policy public URL hosting
- [ ] Final store screenshots/listing

*Updated: 6 Nov 2026 — Phase 1/2/3 + audio-bg fix commit ke baad.*
