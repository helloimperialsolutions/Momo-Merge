# Fruit Merge — server setup (Supabase)

Ye **optional** hai. Iske baghair game poora chalta hai — guest mode mein sab kuch
`localStorage` pe save hota hai, leaderboard player ka apna score dikhata hai, aur
challenges/shop/diamonds sab kaam karte hain. Portals (CrazyGames, GameDistribution,
itch.io) pe isi guest mode mein ship karo — wahan Google login chahiye hi nahi.

Server sirf apni site / APK ke liye chahiye, jahan aap chahte ho ke player ka
progress device badalne pe bhi saath jaye.

Free tier kaafi hai: 500 MB database, 50,000 monthly active users.

---

## 1. Supabase project

1. [supabase.com](https://supabase.com) → **New project**
2. Region: jo aapke players ke qareeb ho (Europe/West ya Southeast Asia)
3. Database password: strong, kahin save kar lo

Do cheezein note karo — **Project Settings → API**:

| Kya | Kahan se | Kya karna hai |
|---|---|---|
| Project URL | `https://xyzcompany.supabase.co` | `NET_CONFIG.url` |
| **anon** public key | `eyJhbGciOi...` (lamba) | `NET_CONFIG.key` |

> ⚠️ **service_role key kabhi mat daalo.** Wo RLS ko poora bypass karta hai.
> Client mein sirf **anon** key jati hai — wo public hone ke liye bani hai,
> kyunke asli protection RLS policies hain, key nahi.

## 2. Schema

Dashboard → **SQL Editor** → New query → `server/supabase.sql` ka poora content
paste → **Run**.

Phir wahi file ke §5 ke verification queries chalao. Do cheezein zaroori hain:
- `relrowsecurity` = `true`
- `pg_constraint` se **sirf ek** unique constraint (primary key) nikle

Ek se zyada unique constraint hue to client ka upsert HTTP 400 dega — wajah
`supabase.sql` ke header comment mein likhi hai.

## 3. Google OAuth

1. [console.cloud.google.com](https://console.cloud.google.com) → naya project
2. **APIs & Services → OAuth consent screen** → External → app ka naam bharo
3. **Credentials → Create credentials → OAuth client ID**
   - Application type: **Web application**
   - Authorized JavaScript origins: `https://xyzcompany.supabase.co`
   - Authorized redirect URIs: `https://xyzcompany.supabase.co/auth/v1/callback`
4. Client ID aur Client secret copy karo
5. Supabase → **Authentication → Providers → Google** → paste karke **Enable**
6. **Authentication → URL Configuration** → Site URL = apni game ki URL
   (jahan `index.html` host hai), aur us domain ko **Redirect URLs** mein add karo

Step 6 chhoot gaya to login redirect ke baad player wapas game pe nahi aayega.

## 4. Game mein wire karo

`www/index.html` mein `NET_CONFIG` dhoondo (section 13c ke shuru mein):

```js
var NET_CONFIG={ url:"", key:"" };
```

Bhar do:

```js
var NET_CONFIG={ url:"https://xyzcompany.supabase.co",
                 key:"eyJhbGciOi...anon-key..." };
```

Bas. Game ka koi aur code branch nahi karta — `netOn()` true hote hi:

- Sign-in invitation home screen pe aane lagta hai
- 🔑 button Supabase ke Google OAuth pe redirect karta hai
- Wapas aane pe token URL hash se capture hota hai aur hash **saaf** kar diya jata hai
  (taake reload ya share kiya gaya URL live credential na le jaye)
- Leaderboard asli 500 players dikhata hai, daily/weekly boards current period ke
- Score har game-over pe upsert hota hai

`NET_CONFIG` khaali chhodne se sab kuch wapas guest mode.

---

## Kaise kaam karta hai (security)

`NET_CONFIG.key` **anon** key hai — ye project ki pehchan hai, player ki nahi.
Isliye:

- `apikey` header mein **hamesha** anon key jati hai
- `Authorization: Bearer` mein **player ka apna token** jata hai (login ke baad)

Agar anon key ko Bearer bana diya jaye to har request `anon` role mein chalti
hai, `auth.uid()` null hota hai, aur RLS do players mein farq nahi kar sakta —
koi bhi kisi ka bhi score overwrite kar sakta. Phase M ke tests M30–M32 isi
cheez ko lock karte hain.

RLS policies (`supabase.sql` §3):
- **select**: sab ke liye khula — leaderboard public hai
- **insert/update**: sirf `auth.uid() = id`, yaani apni row
- **delete**: koi policy nahi = deny

Signed-out client likh hi nahi sakta, aur `lbSubmit()` signed-out hone par
request bhejta hi nahi (bewajah round trip se bachne ke liye).

## Imandari ke saath: kya verify hua, kya nahi

| Cheez | Status |
|---|---|
| Client contract (columns, queries, token handling) | ✅ 337 harness assertions, phases A–M |
| Schema column names client se match | ✅ programmatically checked |
| SQL syntax | ✅ **asli PostgreSQL parser** (pglast / libpg_query) se parse — 16 statements, 0 errors |
| Schema invariants (PK, RLS, policies, indexes, trigger) | ✅ `python3 server/verify_schema.py` — 21 checks green |
| RLS policies actually block a forged write | ⚠️ **structurally verified, not executed** — policies `auth.uid() = id` pe hain ye AST se confirm hai, lekin asli 401/403 dekhne ke liye live Supabase chahiye |
| Google OAuth round trip | ❌ **unverified** — real Google credentials chahiye |

Schema check khud chalane ke liye:

```bash
pip install pglast
python3 server/verify_schema.py
```

Supabase pe schema chalane ke baad ye teen cheezein khud test karo:

1. Do browser (ek incognito) mein alag naam se login karo, dono khelo —
   dono leaderboard pe aane chahiye
2. Browser ke devtools se `fetch()` chalao aur kisi **doosre** player ki row
   update karne ki koshish karo — 401/403 aana chahiye
3. Sign out ke baad leaderboard padha ja sake, likha na ja sake
