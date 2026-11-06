#!/usr/bin/env python3
"""Basket/board UI mockups (2026-10-29). Fruits are the REAL game sprites
and NEVER change -- only the crate/basket/board + chrome varies.
Five directions, same layout, so the user compares style, not content."""
import pathlib

ROOT = pathlib.Path("/home/user/fruit-merge")
OUT = ROOT / "design/ui-mockups/basket"
OUT.mkdir(parents=True, exist_ok=True)
FRUIT = "../../../www/assets/fruits"
FONT = "../../../www/assets/fonts/cherry-bomb-one.woff2"

FRUITS_PILE = [  # (stage, x, y, diameter) inside a 392x420 board
    (10, 92, 258, 158), (9, 238, 282, 132), (8, 18, 300, 108),
    (6, 268, 196, 96), (5, 176, 318, 84), (4, 132, 226, 70),
    (2, 236, 148, 58), (3, 300, 306, 56), (1, 96, 196, 46), (0, 60, 250, 36),
]
STRIP_D = [30, 32, 34, 36, 38, 42, 46, 50, 56, 62, 70]

def fruits_html():
    s = ""
    for st, x, y, d in FRUITS_PILE:
        s += f'<img class="fr" src="{FRUIT}/f{st}.png" style="left:{x}px;top:{y}px;width:{d}px">\n'
    s += f'<img class="fr aim" src="{FRUIT}/f4.png" style="left:168px;top:-24px;width:58px">\n'
    return s

def strip_html():
    s = ""
    for i, d in enumerate(STRIP_D):
        ring = ' ring' if i == 4 else ''
        s += f'<span class="slot{ring}"><img src="{FRUIT}/f{i}.png" style="width:{d}px"></span>\n'
    return s

BASE_CSS = """
*{margin:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
@font-face{font-family:"Cherry Bomb One";src:url("__FONT__") format("woff2")}
body{font-family:"Trebuchet MS",sans-serif;display:flex;justify-content:center}
.phone{width:460px;height:800px;position:relative;overflow:hidden;background:var(--page)}
.top{position:absolute;top:14px;left:12px;right:12px;display:flex;gap:8px;align-items:flex-start}
.icobtn{width:52px;height:52px;border-radius:50%;background:var(--card);border:3px solid var(--edge);
  display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 3px 0 var(--shadow)}
.scorecard{flex:1;background:var(--card);border:3px solid var(--edge);border-radius:18px;text-align:center;
  padding:5px 2px;box-shadow:0 3px 0 var(--shadow)}
.scorecard .lab{font-size:11px;font-weight:900;letter-spacing:1px;color:var(--ink2)}
.scorecard .val{font-family:"Cherry Bomb One";font-size:26px;color:var(--accent);line-height:1}
.powers{position:absolute;top:96px;left:12px;right:12px;display:flex;gap:7px;align-items:center}
.pw{width:54px;height:54px;border-radius:16px;background:var(--card);border:3px solid var(--edge);
  display:flex;align-items:center;justify-content:center;font-size:22px;position:relative;box-shadow:0 3px 0 var(--shadow)}
.pw .bdg{position:absolute;top:-7px;right:-7px;background:var(--accent);color:#fff;font-size:11px;font-weight:900;
  min-width:19px;height:19px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:2px solid #fff}
.nextpill{margin-left:auto;background:var(--card);border:3px solid var(--edge);border-radius:999px;
  display:flex;align-items:center;gap:5px;padding:7px 10px;box-shadow:0 3px 0 var(--shadow)}
.nextpill .lab{font-size:11px;font-weight:900;color:var(--ink2);letter-spacing:.5px}
.nextpill img{width:26px}
.board{position:absolute;top:168px;left:14px;right:14px;height:452px;border-radius:20px}
.board .inner{position:absolute;inset:0;border-radius:20px;overflow:hidden;background:var(--board)}
.board .inner::after{content:"";position:absolute;inset:0;background:var(--boardfx)}
.wall{position:absolute;background:var(--wall);z-index:3}
.wall.l{left:0;top:0;bottom:0;width:16px;border-radius:20px 0 0 20px}
.wall.r{right:0;top:0;bottom:0;width:16px;border-radius:0 20px 20px 0}
.wall.b{left:0;right:0;bottom:0;height:16px;border-radius:0 0 20px 20px}
.danger{position:absolute;left:22px;right:22px;top:52px;border-top:4px dashed var(--danger);opacity:.75;z-index:2}
.guide{position:absolute;left:50%;top:8px;bottom:14px;border-left:3px dotted var(--guide);opacity:.55;z-index:1}
.fr{position:absolute;z-index:2}
.strip{position:absolute;left:14px;right:14px;bottom:56px;height:64px;background:var(--card);
  border:3px solid var(--edge);border-radius:999px;display:flex;align-items:center;justify-content:space-evenly;
  box-shadow:0 3px 0 var(--shadow);padding:0 6px}
.slot{display:flex;align-items:center;justify-content:center;width:38px;height:52px;position:relative}
.slot.ring::before{content:"";position:absolute;width:44px;height:44px;border:3.5px solid var(--accent);border-radius:50%}
.tag{position:absolute;left:14px;bottom:16px;font-family:"Cherry Bomb One";font-size:19px;color:var(--ink)}
.credit{position:absolute;right:14px;bottom:20px;font-size:11px;font-weight:800;color:var(--ink2)}
"""

THEMES = {
"v1-crate": """
:root{--page:#f7e3c2;--card:#fff7e8;--edge:#c98d54;--shadow:rgba(122,72,20,.45);--ink:#5b3a1e;--ink2:#a97c50;
--accent:#e8506a;--board:#f2d5a7;--wall:linear-gradient(180deg,#c98a4b,#a96f35);--danger:#e8506a;--guide:#b5763f}
.board .inner{background:repeating-linear-gradient(90deg,#f4d8ab 0 62px,#e9c48c 62px 65px)}
.board .inner::after{background:repeating-linear-gradient(0deg,rgba(160,110,50,.05) 0 3px,transparent 3px 26px)}
""",
"v2-wicker": """
:root{--page:#f3e0bd;--card:#fff6e3;--edge:#b57e3e;--shadow:rgba(110,66,18,.45);--ink:#5f3d1c;--ink2:#a8793f;
--accent:#e8506a;--board:#d9a860;--wall:linear-gradient(180deg,#b57e3e,#96622a);--danger:#fff0d0;--guide:#8a5a24}
.board .inner{background-color:#d9a860;background-image:
 linear-gradient(45deg,rgba(255,235,190,.20) 25%,transparent 25%,transparent 75%,rgba(255,235,190,.20) 75%),
 linear-gradient(45deg,rgba(120,72,20,.16) 25%,transparent 25%,transparent 75%,rgba(120,72,20,.16) 75%);
 background-size:30px 30px;background-position:0 0,15px 15px}
.wall{background:repeating-linear-gradient(45deg,#c08b45 0 10px,#a5712f 10px 20px)!important}
""",
"v3-felt": """
:root{--page:#fdf3e0;--card:#ffffff;--edge:#57b894;--shadow:rgba(31,110,79,.35);--ink:#20503d;--ink2:#6fae97;
--accent:#ff5d7e;--board:#cdeeda;--wall:linear-gradient(180deg,#6cc79f,#4cab82);--danger:#ff5d7e;--guide:#3f9c74}
.board .inner::before{content:"";position:absolute;inset:9px;border:2.5px dashed rgba(255,255,255,.85);border-radius:14px;z-index:1}
.scorecard,.pw,.nextpill,.strip,.icobtn{border-style:solid}
.board .inner{background:#cdeeda}
""",
"v4-whitewash": """
:root{--page:#fbf1e6;--card:#ffffff;--edge:#eec3cf;--shadow:rgba(190,120,140,.35);--ink:#6d4252;--ink2:#c49aa9;
--accent:#ff5d7e;--board:#f8ecdb;--wall:linear-gradient(180deg,#f3ccd9,#eab2c6);--danger:#ff5d7e;--guide:#d99cae}
.board .inner{background:repeating-linear-gradient(90deg,#faefdf 0 62px,#f1decb 62px 65px)}
.board .inner::after{background:repeating-linear-gradient(0deg,rgba(190,150,110,.06) 0 3px,transparent 3px 26px)}
""",
"v5-pinkwood": """
:root{--page:#fde7ee;--card:#fff8fa;--edge:#e79fb4;--shadow:rgba(190,90,120,.40);--ink:#70324a;--ink2:#c4839b;
--accent:#e83e6b;--board:#f7ccd9;--wall:linear-gradient(180deg,#e58aa6,#d96b8a);--danger:#fff2f6;--guide:#c25b7c}
.board .inner{background:repeating-linear-gradient(90deg,#f8d2de 0 62px,#f0bccb 62px 65px)}
.board .inner::after{background:repeating-linear-gradient(0deg,rgba(190,90,120,.06) 0 3px,transparent 3px 26px)}
""",
}
TITLES = {"v1-crate":"V1 · Wooden Crate (reference jaisa)","v2-wicker":"V2 · Wicker Basket (buni tokri)",
"v3-felt":"V3 · Felt Toy Box","v4-whitewash":"V4 · Whitewash Wood","v5-pinkwood":"V5 · Pink Wood"}

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>__CSS__</style></head>
<body><div class="phone">
  <div class="top">
    <div class="icobtn">🏠</div><div class="icobtn">🔊</div>
    <div class="scorecard"><div class="lab">SCORE</div><div class="val">1821</div></div>
    <div class="scorecard"><div class="lab">BEST</div><div class="val">2400</div></div>
    <div class="icobtn">↩</div>
  </div>
  <div class="powers">
    <div class="pw">💣<span class="bdg">1</span></div><div class="pw">🧹<span class="bdg">1</span></div>
    <div class="pw">↩️<span class="bdg">1</span></div><div class="pw">❄️<span class="bdg">1</span></div>
    <div class="pw">🎈<span class="bdg">2</span></div>
    <div class="nextpill"><span class="lab">NEXT</span><img src="__FRUIT__/f3.png"><img src="__FRUIT__/f1.png" style="width:21px;opacity:.75"></div>
  </div>
  <div class="board"><div class="inner">
    <div class="danger"></div><div class="guide"></div>
    __FRUITS__
  </div><div class="wall l"></div><div class="wall r"></div><div class="wall b"></div></div>
  <div class="strip">__STRIP__</div>
  <div class="tag">__TITLE__</div><div class="credit">Momo Merge · mockup</div>
</div></body></html>"""

for name, theme in THEMES.items():
    css = (BASE_CSS + theme).replace("__FONT__", FONT)
    html = (HTML.replace("__CSS__", css).replace("__FRUIT__", FRUIT)
                .replace("__FRUITS__", fruits_html()).replace("__STRIP__", strip_html())
                .replace("__TITLE__", TITLES[name]))
    (OUT / f"{name}.html").write_text(html)
    print("wrote", name)
