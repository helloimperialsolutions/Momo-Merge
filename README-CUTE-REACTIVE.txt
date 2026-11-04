MOMO MERGE — CUTE REACTIVE ORCHARD (COMPLETE PROJECT)
====================================================

This is the complete game project, not the tiny basket browser-test ZIP.
The original game, corrected original wicker basket, physics, scoring,
shop/economy, ads, achievement system, Android wrapper, and assets are preserved.

WHAT'S NEW
----------
* Original custom-designed storybook orchard gameplay backgrounds:
  www/assets/bg-landscape.jpg and www/assets/bg-portrait.jpg
* Fluffy fruit companions use the game's existing fruit sprite artwork.
* Wide desktop gameplay: up to six floating plush friends at the sides.
* Phone portrait: two small, responsive companions near the side edges.
* Very short landscape: two side friends with no overlapping characters.
* Friends gently bob, wiggle, jump and react with stickers / speech bubbles.
* Tap a friend to pet it; petting will NOT also drop a fruit.
* Gameplay reactions include merges, combo streaks, golden fruit,
  watermelon creation, watermelon rain, bombs, sweep, undo, freeze, thaw,
  pop, score milestones, overflow warning, game over and new record,
  as well as periodic friendly cheers and tap-to-pet dialogues.
* All new rendering happens on the existing gameplay canvas; it does not
  replace the basket, game UI, click/touch controls or game physics.

HOW TO PLAY IN A BROWSER
------------------------
Extract this ZIP. Open fruit-merge/www/index.html in Chrome or another
modern browser. For local-host testing, you can serve the www folder with
python3 -m http.server 8081 (then visit http://localhost:8081).

ANDROID
-------
The bundled android/app/src/main/assets/public directory includes the
same UPDATED index.html, fruit sprites, wicker basket and backgrounds.
This archive contains Android SOURCE, not a signed/installable APK.
You need a working Android/Gradle environment to build the APK or AAB.

TEST RESULTS
------------
* JS syntax: node --check: passed
* Automated existing game harness: 554 passed / 0 failed
* Chromium rendering: desktop 1730x870, phone portrait 430x932,
  short-landscape 850x470: rendered, loaded backgrounds and basket,
  no JavaScript page errors during smoke test
* Real browser pointer input: tapping a companion did not drop fruit
* Real gameplay physics: touching seeded fruit pair merges and scores
* Web and Android bundled index.html / key assets are byte-identical

Note: Automated tests and browser smoke tests reduce defects but cannot
promise that no bugs will ever occur on every device or Android version.
