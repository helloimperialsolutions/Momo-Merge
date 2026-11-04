MOMO MERGE — COMPLETE MERGED GAME PROJECT
30 October 2026

BASE: fruit-merge.rar (entire original project retained)
FIXES: Momo-Merge-Basket-Corrected-Test.zip (browser basket correction)

This is the full project, NOT a minimal browser demo. All existing
Android source files, web game, economy, ads bridge, artwork, preview
images, server scripts, design work, project configs and tests remain.

MERGED INTO THE ORIGINAL PROJECT
--------------------------------
1. www/index.html — replaced by the tested basket-corrected version;
   retains all other original game logic and features.
2. www/assets/basket-original.png — added original full basket photo
   (736 x 931). Original artwork is rendered without cropping.
3. Android offline/public assets — game HTML and current www/assets
   synchronized into android/app/src/main/assets/public/ for Android.
   Existing Android-specific project files are preserved.
4. tests/fm_game.js — regenerated from the merged HTML.
5. tests/harness.js — updated ONLY the obsolete basket assertions to
   verify the corrected intact basket photo, scaling and U-walls.

HOW TO PLAY IN A BROWSER
------------------------
Open fruit-merge/www/index.html in Chrome or Edge, or (recommended)
open a terminal in fruit-merge/www and run:

    python -m http.server 8000

Then open http://localhost:8000/

HOW TO RUN PROJECT TESTS
------------------------
In the fruit-merge root, with Node.js installed:

    npm run check

Validation on the merged project: 554 passed, 0 failed.
Browser smoke tests also passed in Chromium at mobile, desktop, and
short-landscape viewports; game started, basket loaded and fruit dropped.

ANDROID PROJECT
---------------
This archive includes Android/Capacitor SOURCE, not an APK.
To generate a build in your own Android/Java/Node environment:

    npm install
    npm run cap:sync
    npm run build:apk

See the project's existing DEPLOY-GUIDE.md and CLOUD-BUILD.md for setup.
Ad monetization, online sign-in and production services may need their
own production credentials/configuration.

Note: All old sliced basket assets are kept for source/project continuity,
but the game now displays the new untouched basket-original.png image.
