# Build the Android app WITHOUT Android Studio (zero extra storage)

**Your problem:** Android Studio + the Android SDK need **10–15 GB** of free disk space, and
your laptop doesn't have it.

**The fix:** you don't have to build on your laptop at all. Build in the **cloud** — GitHub
runs the build on *its* computers (which already have Java + the Android SDK), and hands you
back the finished `.aab` file to download. **Free, and it uses ~0 storage on your machine.**

This project is **already set up** for it:
- `.github/workflows/build-android.yml` — builds the signed AAB in the cloud.
- `.github/workflows/generate-keystore.yml` — creates your signing key in the cloud (so you
  don't need Java locally either).
- `android/app/build.gradle` — already reads the signing key from CI secrets.
- `.gitignore` — keeps `node_modules` and your keystore off GitHub.

---

## Your options, ranked

| # | Option | Storage on your PC | Cost | Best for |
|---|---|---|---|---|
| **1** | **GitHub Actions** (this guide) | **~0 GB** (just Git, ~50 MB) | Free | **You — recommended** |
| 2 | GitHub Codespaces | ~0 GB (cloud PC in browser) | Free hours/month | If you want to click around a cloud Android Studio |
| 3 | Command-line only (no Android Studio) | ~3 GB (JDK 17 + SDK tools) | Free | If you can free a few GB and like terminals |
| 4 | Borrow any PC once | 0 on yours | Free | A friend's laptop with Android Studio, one time |

---

## Recommended path: GitHub Actions (step by step)

### Step 0 — Make a free GitHub account
Go to **github.com** → sign up (free). Remember your username + password.

### Step 1 — Put the project on GitHub
The `node_modules` folder is huge but is **ignored automatically** by `.gitignore`, so the
upload stays small (~6 MB).

**Easiest (no command line): GitHub Desktop**
1. Install **GitHub Desktop** (desktop.github.com, ~150 MB), sign in.
2. **File → Add Local Repository** → pick the `fruit-merge` folder.
   (If it says "not a repository", click **create a repository**.)
3. Write a summary like "first commit" → **Commit to main**.
4. **Publish repository** → keep it **Private** → Publish.

**Or with Git commands** (Git is only ~50 MB):
```bash
cd fruit-merge
git init
git add .
git commit -m "Momo Merge: game + Android project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/fruit-merge.git
git push -u origin main
```
(First create the empty repo `fruit-merge` on github.com, **Private**, don't add a README.)

> **Private vs public:** Actions is free for both. Keep it **Private** so your game code and
> keystore secrets stay yours. (Private gets ~2000 free build-minutes/month — far more than
> enough; each build is ~5 minutes.)

### Step 2 — Create your signing keystore (RUN ONCE)
Play needs a **keystore** to sign the app. You have no Java locally, so let GitHub make it:
1. On your repo page → **Actions** tab.
2. Click **"Generate signing keystore (run ONCE)"** → **Run workflow** → run it.
3. Wait for the green ✔ (about a minute). Click the run → **Artifacts** → download
   **`keystore`**.
4. Unzip it. You get `fruitmerge-release.keystore` + `SECRETS.txt`.
   - **Back up `fruitmerge-release.keystore` FOREVER** (password manager + Google Drive).
     Lose it = you can never update the app.
   - **Delete the artifact from GitHub** afterwards (it contains your private key).

> ⚠️ **Run this generator only ONCE.** Running it again makes a *different* key that Play will
> reject for updates.

### Step 3 — Add the 4 secrets to the repo
Open `SECRETS.txt`. For each of the 4 values:
- Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
- Add these names exactly (paste each value):
  - `KEY_ALIAS`
  - `KEYSTORE_PASSWORD`
  - `KEY_PASSWORD`
  - `KEYSTORE_BASE64`  ← one very long line; copy all of it.

### Step 4 — Build the AAB in the cloud
1. **Actions** tab → **"Build Android AAB"** → **Run workflow**.
2. Wait ~5 minutes for the green ✔.
3. Click the run → **Artifacts** → download **`fruitmerge-aab`**.
4. Unzip → you have **`app-release.aab`** — this is the file you upload to Play Console.

That's it — **no Android Studio, no SDK, no storage used on your laptop.**

### Step 5 — Upload to Play Console
Follow **DEPLOY-GUIDE.md → PART D** (store listing, content rating, privacy policy, the
**12-testers-for-14-days** rule, then upload the AAB to a track).

---

## Shipping an update later (v1.1, v1.2…)
1. Edit `www/index.html`, run `npm run check` (405/0).
2. Bump the version in `android/app/build.gradle`: `versionCode 2`, `versionName "1.1"`
   (**versionCode must increase every upload**).
3. Commit + push (or GitHub Desktop → Commit → Push). The build runs automatically, or run
   **"Build Android AAB"** manually.
4. Download the new `app-release.aab`, upload to Play.

---

## 💡 Strategy note: you can go live on PORTALS *today* — zero storage, zero cost
The Play Store path needs the $25 fee **and** the 12-testers-14-days wait **and** an Android
build. The **portals need none of that** — they just take a ZIP of your `www/` folder:

```bash
cd www
zip -r fruitmerge-web.zip index.html assets admob-bridge.js privacy-policy.html
```

Upload that ZIP to **itch.io** (easiest), **CrazyGames**, and **GameDistribution** and you can
be live and earning **without Android Studio, without the $25, and without any extra storage**
(see DEPLOY-GUIDE.md → PART F). Do the portals now, and do the Play Store build whenever you're
ready — the cloud build above means storage is no longer a blocker.

Also, two things you said you were waiting on:
- **AdMob does NOT require Play Console.** You can create the AdMob app now with just the
  package name `com.isstudios.momomerge`; link the Play listing later.
- **The $25 is only charged when you actually create the Play developer account** — you can
  finish everything else (build, AdMob, listing text, screenshots) first and pay at the end.
