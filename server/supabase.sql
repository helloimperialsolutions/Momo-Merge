-- ============================================================================
--  Fruit Merge — Supabase schema
--  Run this ONCE in the Supabase SQL editor (Dashboard -> SQL -> New query).
--
--  IMPORTANT — do not add a UNIQUE constraint on `name`.
--  The client upserts with `Prefer: resolution=merge-duplicates` and sends no
--  `on_conflict` parameter, so PostgREST infers the conflict target from the
--  table's single unique constraint. A second unique index (e.g. on name)
--  makes that inference ambiguous and every score write starts failing with
--  400. It would also let one player permanently block a name for everyone.
--
--  Columns below mirror scripts/economy.js exactly:
--    lbSubmit()  -> POST /rest/v1/scores  {name, score_all, score_day,
--                                          score_week, day_key, week_key}
--    lbFetch()   -> GET  /rest/v1/scores?select=name,<col>
--                        &order=<col>.desc&limit=500
--                        [&day_key=eq.<k>&<col>=gt.0 | &week_key=eq.<k>&<col>=gt.0]
--  Rename a column here and you must rename it there.
-- ============================================================================

create extension if not exists pgcrypto;

-- ---------------------------------------------------------------------------
-- 1. the leaderboard table
-- ---------------------------------------------------------------------------
create table if not exists public.scores (
  -- Defaults to the caller's own uid, so the client never sends an id and
  -- cannot aim a write at somebody else's row.
  id          uuid primary key default auth.uid(),

  -- Display name only. 2..16 chars matches NAME_MIN/NAME_MAX in economy.js.
  -- <> & " ' are stripped client-side; length is enforced here too because a
  -- modified client can send anything it likes.
  name        text not null
              check (char_length(name) between 2 and 16),

  score_all   integer not null default 0 check (score_all  between 0 and 99999999),
  score_day   integer not null default 0 check (score_day  between 0 and 99999999),
  score_week  integer not null default 0 check (score_week between 0 and 99999999),

  -- Which period the day/week scores were set in. Format is produced by
  -- dayKey()/weekKey():  "2026-10-9"  and  "2026-W41".
  -- These are filter columns, not derived ones — the server never has to know
  -- how the client computes a week boundary, and no cron job is needed to
  -- clear stale rows: an old row simply stops matching today's filter.
  day_key     text,
  week_key    text,

  updated_at  timestamptz not null default now()
);

comment on table public.scores is
  'One row per player. Upserted on every game over and on every rename.';

-- ---------------------------------------------------------------------------
-- 2. indexes for the three boards
--    Each board is `order by <col> desc limit 500`, two of them filtered by a
--    period key. Without these, every board load is a full table sort.
-- ---------------------------------------------------------------------------
create index if not exists scores_all_idx
  on public.scores (score_all desc);

create index if not exists scores_day_idx
  on public.scores (day_key, score_day desc);

create index if not exists scores_week_idx
  on public.scores (week_key, score_week desc);

-- ---------------------------------------------------------------------------
-- 3. row level security
--    This is the whole reason the player's own token is the Bearer and the
--    anon key only goes in `apikey`. Under the anon role auth.uid() is null,
--    so the write policies below cannot match and a signed-out client cannot
--    write at all.
-- ---------------------------------------------------------------------------
alter table public.scores enable row level security;

-- The leaderboard is public: a signed-out visitor should still see the board.
drop policy if exists "scores are world-readable" on public.scores;
create policy "scores are world-readable"
  on public.scores for select
  using (true);

-- A player may create exactly one row, and it must be their own.
drop policy if exists "players insert their own row" on public.scores;
create policy "players insert their own row"
  on public.scores for insert
  to authenticated
  with check (auth.uid() = id);

-- A player may update exactly one row, and it must be their own.
-- Both clauses matter: `using` gates which row is found, `with check` gates
-- what it may become. Omitting `with check` would let a client try to rewrite
-- the row's id.
drop policy if exists "players update their own row" on public.scores;
create policy "players update their own row"
  on public.scores for update
  to authenticated
  using (auth.uid() = id)
  with check (auth.uid() = id);

-- No delete policy: rows are never removed by the game, and the absence of a
-- policy is itself the deny rule.

-- ---------------------------------------------------------------------------
-- 4. keep updated_at honest
--    A client could post an updated_at of its own choosing; this overwrites it.
-- ---------------------------------------------------------------------------
create or replace function public.touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

drop trigger if exists scores_touch on public.scores;
create trigger scores_touch
  before insert or update on public.scores
  for each row execute function public.touch_updated_at();

-- ---------------------------------------------------------------------------
-- 5. verification queries (run these after applying, expect the noted results)
-- ---------------------------------------------------------------------------
-- Should list exactly 4 policies:
--   select policy names from pg_policies where tablename = 'scores';
--
-- Should return exactly ONE row (the primary key). More than one unique
-- constraint and the client's upsert will fail with HTTP 400:
--   select conname from pg_constraint
--    where conrelid = 'public.scores'::regclass and contype in ('p','u');
--
-- RLS must be on:
--   select relrowsecurity from pg_class where oid = 'public.scores'::regclass;
