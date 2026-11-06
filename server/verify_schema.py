#!/usr/bin/env python3
"""
Verify server/supabase.sql against the invariants the client depends on.

Uses pglast, which wraps libpg_query -- the REAL PostgreSQL parser -- so this
catches genuine syntax errors, not just what a hand-rolled regex tolerates.

    pip install pglast
    python3 server/verify_schema.py

Three AST gotchas this script works around (all three produced false failures
before they were understood):

  1. auth.uid() parses to FuncCall(funcname=('auth','uid')) -- two separate
     String nodes. A substring search for "auth.uid" can therefore NEVER match.
     The expression must be walked structurally.
  2. A plpgsql body lives in options['as'], not sql_body. sql_body is only
     populated for SQL-language functions with an inline body.
  3. That option's arg is a 1-element TUPLE of String, not a String.
"""
import pathlib
import sys

try:
    import pglast
    from pglast import ast, enums
except ImportError:
    sys.exit("pglast is required:  pip install pglast")

HERE = pathlib.Path(__file__).resolve().parent
SQL = (HERE / "supabase.sql").read_text()

CT, ATT = enums.ConstrType, enums.AlterTableType
fails = []


def check(label, cond, detail=""):
    mark = "\u2713" if cond else "\u2717"
    print(f"  {mark}  {label}" + (f"  [{detail}]" if detail else ""))
    if not cond:
        fails.append(label)


def sval_tuple(node):
    """Extract ('auth','uid') from a FuncCall's funcname / ColumnRef's fields."""
    return tuple(getattr(s, "sval", None) for s in (node or ()))


def is_auth_uid_eq_id(node):
    """True when the expression is exactly  auth.uid() = id."""
    if not isinstance(node, ast.A_Expr):
        return False
    if tuple(getattr(s, "sval", None) for s in (node.name or ())) != ("=",):
        return False
    fn, col = node.lexpr, node.rexpr
    return (
        isinstance(fn, ast.FuncCall) and sval_tuple(fn.funcname) == ("auth", "uid")
        and isinstance(col, ast.ColumnRef) and sval_tuple(col.fields) == ("id",)
    )


def option_text(arg):
    """DefElem.arg may be a String node or a tuple of them (plpgsql bodies)."""
    if hasattr(arg, "sval"):
        return arg.sval
    if isinstance(arg, (tuple, list)):
        return "".join(getattr(x, "sval", "") for x in arg)
    return ""


# --- parse with the real PostgreSQL grammar --------------------------------
try:
    stmts = [s.stmt for s in pglast.parse_sql(SQL)]
except pglast.parser.ParseError as e:
    sys.exit(f"  \u2717  SQL SYNTAX ERROR: {e}")
print(f"  \u2713  parsed {len(stmts)} statements, 0 syntax errors\n")

# --- table -----------------------------------------------------------------
tbl = next(s for s in stmts if isinstance(s, ast.CreateStmt))
cols = [e.colname for e in tbl.tableElts if isinstance(e, ast.ColumnDef)]
want = ["id", "name", "score_all", "score_day", "score_week",
        "day_key", "week_key", "updated_at"]
check("8 contract columns, exact match", sorted(cols) == sorted(want))

pk, uniq = [], []
for e in tbl.tableElts:
    if not isinstance(e, ast.ColumnDef):
        continue
    for c in (e.constraints or []):
        k = CT(c.contype).name
        if k == "CONSTR_PRIMARY":
            pk.append(e.colname)
        elif k == "CONSTR_UNIQUE":
            uniq.append(e.colname)
check("exactly one PRIMARY KEY (id)", pk == ["id"], ",".join(pk))
# The client upserts with Prefer: resolution=merge-duplicates and sends no
# on_conflict, so PostgREST infers the target from the ONE unique constraint.
check("zero UNIQUE constraints (upsert inference depends on it)", not uniq,
      ",".join(uniq) or "none")
check("no UNIQUE index either",
      not [s for s in stmts if isinstance(s, ast.IndexStmt) and s.unique])

# --- RLS -------------------------------------------------------------------
check("row level security ENABLED", any(
    isinstance(s, ast.AlterTableStmt)
    and any(c.subtype == ATT.AT_EnableRowSecurity for c in s.cmds)
    for s in stmts))

pols = [s for s in stmts if isinstance(s, ast.CreatePolicyStmt)]
check("3 policies created", len(pols) == 3,
      "; ".join(f"{p.policy_name}={p.cmd_name}" for p in pols))
check("  SELECT policy", sum(1 for p in pols if p.cmd_name == "select") == 1)
check("  INSERT policy", sum(1 for p in pols if p.cmd_name == "insert") == 1)
check("  UPDATE policy", sum(1 for p in pols if p.cmd_name == "update") == 1)
check("  no DELETE policy (absence = deny)",
      not any(p.cmd_name == "delete" for p in pols))

ins = next(p for p in pols if p.cmd_name == "insert")
upd = next(p for p in pols if p.cmd_name == "update")
sel = next(p for p in pols if p.cmd_name == "select")
check("  INSERT with_check is auth.uid() = id", is_auth_uid_eq_id(ins.with_check))
check("  UPDATE using is auth.uid() = id", is_auth_uid_eq_id(upd.qual))
check("  UPDATE with_check is auth.uid() = id", is_auth_uid_eq_id(upd.with_check))
check("  SELECT is world-readable (bare TRUE)",
      isinstance(sel.qual, ast.A_Const) and getattr(sel.qual.val, "boolval", False) is True)


def is_public(p):
    return any(getattr(r, "roletype", None) == enums.RoleSpecType.ROLESPEC_PUBLIC
               for r in (p.roles or ()))


check("  write policies NOT open to PUBLIC role",
      not any(is_public(p) for p in (ins, upd)))

# --- indexes + trigger -----------------------------------------------------
idxs = [s for s in stmts if isinstance(s, ast.IndexStmt)]
check("3 indexes, one per board", len(idxs) == 3,
      ", ".join(x.idxname for x in idxs))
check("updated_at trigger present",
      sum(1 for s in stmts if isinstance(s, ast.CreateTrigStmt)) == 1)

fn = next(s for s in stmts if isinstance(s, ast.CreateFunctionStmt))
opts = {getattr(o, "defname", None): option_text(o.arg) for o in (fn.options or ())}
body = opts.get("as", "")
check("trigger fn is plpgsql", opts.get("language") == "plpgsql")
check("trigger fn sets new.updated_at := now()", "new.updated_at := now()" in body)
check("trigger fn returns new", "return new" in body)

print()
if fails:
    print(f"  \u274c  {len(fails)} INVARIANT(S) FAILED:")
    for f in fails:
        print(f"      - {f}")
    sys.exit(1)
print("  \u2705  ALL SCHEMA INVARIANTS HOLD (real PostgreSQL parser)")
