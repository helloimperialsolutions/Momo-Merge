#!/usr/bin/env python3
"""
Re-extract the two script blocks from www/index.html into tests/.

Run after EVERY edit to index.html, then:  node tests/harness.js

NOTE: this uses b[0] and b[1] explicitly, NOT b[-1]. HANDOFF.md §1 originally
showed b[-1] for the game block, which was correct only while index.html had
exactly two <script> tags. See WORKSPACE-NOTES.md finding #1.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "www" / "index.html"
TESTS = ROOT / "tests"

s = HTML.read_text(encoding="utf-8")
blocks = re.findall(r"<script>(.*?)</script>", s, re.S)

if len(blocks) != 2:
    sys.exit(
        f"ERROR: expected exactly 2 <script> blocks, found {len(blocks)}.\n"
        f"  sizes: {[len(b) for b in blocks]}\n"
        f"Something was injected into index.html (a third-party beacon, an\n"
        f"analytics snippet, a CDN loader). Remove it before extracting --\n"
        f"the game must stay fully self-contained and offline."
    )

matter, game = blocks

# Mask the build's NET_CONFIG in the test copies. index.html now ships the
# LIVE backend url/key inline (cloud save + leaderboard), so the raw copy
# would make netOn() true from boot and the guest-mode milestones would all
# see a cloud this build does not have. Tests that exercise the net paths
# configure their own endpoints via FM_DEBUG.setNet(), so every phase stays
# hermetic and readable whatever the shipped config happens to be.
game, n_masked = re.subn(r"NET_CONFIG=\{[^{}]*\}", 'NET_CONFIG={ url:"", key:"" }', game)
assert n_masked == 1, (
    f"expected exactly 1 NET_CONFIG literal, found {n_masked} -- "
    "extract.py's masking rule no longer matches the source" 
)

# sanity anchors -- fail loudly rather than writing junk into tests/
assert "matter-js" in matter[:400], "block[0] does not look like matter.js"
assert "FM_DEBUG" in game, "block[1] does not look like the game code"
assert "fruitmerge.v2" in game, "game block is missing the save key"

(TESTS / "fm_matter.js").write_text(matter, encoding="utf-8")
(TESTS / "fm_game.js").write_text(game, encoding="utf-8")

print(f"extracted: fm_matter.js ({len(matter)} chars), fm_game.js ({len(game)} chars)")
