# Momo Merge — Cute Fruit Drop 🍑

A cozy Suika-style fruit merge drop puzzle. Drop cute fruits, merge them into
bigger ones, climb the daily / weekly / all-time leaderboards.

- **Play the web build:** https://games.imperialsolutions.org/
- **Android app:** shipped via Google Play (closed alpha / production)
- **Policies:** [Privacy](https://games.imperialsolutions.org/www/privacy-policy.html)
  · [Account deletion](https://games.imperialsolutions.org/www/account-deletion.html)
  · [Terms](https://games.imperialsolutions.org/www/tos.html)

## Tech

- Single-file HTML5 game (`www/index.html`): Matter.js physics, canvas rendering
- Capacitor 7 Android wrapper (`android/`)
- Supabase backend: Google OAuth + cloud save + leaderboards (RLS enforced,
  own-row-only policies — see `server/supabase.sql`)
- AdMob ads with UMP consent flow

## Development

```bash
npm install
npm run check     # extract + full test harness (must pass)
npm run start     # local server on :8081
npm run cap:sync  # refresh native android assets
```

Rules for contributors: never edit `tests/fm_game.js` / `tests/fm_matter.js`
(generated), keep the fixed physics timestep untouched, and never commit
secrets — CI owns signing material via GitHub Actions secrets.

© IS Studios. Contact: hello@imperialsolutions.org
