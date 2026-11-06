# -*- coding: utf-8 -*-
"""5 home-screen UI directions for Momo Merge — mockups only, game untouched.
All directions reuse the game's own painted art (www/assets) + Baloo 2, so
every one of them is realistically buildable in the game's DOM/CSS later."""
import pathlib
D = pathlib.Path(__file__).parent
ART = "../../www/assets"

SKEL = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Baloo;src:url("file:///tmp/baloo.ttf")}}
*{{margin:0;box-sizing:border-box;font-family:Baloo,'Trebuchet MS',sans-serif}}
body{{background:#26221f;display:flex;flex-direction:column;align-items:center;padding:26px 0}}
.cap{{color:#f5ead6;font-size:25px;font-weight:800;margin-bottom:14px;letter-spacing:.4px}}
.cap small{{display:block;text-align:center;color:#bfae94;font-size:15.5px;font-weight:600;margin-top:3px}}
.phone{{width:400px;height:720px;border-radius:36px;overflow:hidden;position:relative;flex:none}}
.bg{{position:absolute;inset:0;background:url("{art}/bg-portrait.jpg") center 62%/cover}}
.top{{position:absolute;top:14px;left:14px;right:14px;display:flex;justify-content:space-between;z-index:5}}
.title{{position:absolute;top:64px;width:100%;text-align:center;z-index:4}}
.mascot{{position:absolute;left:50%;top:196px;transform:translateX(-50%);width:212px;height:212px;z-index:3}}
.best{{position:absolute;top:428px;width:100%;display:flex;justify-content:center;z-index:4}}
.play{{position:absolute;left:50%;top:478px;transform:translateX(-50%);z-index:5;white-space:nowrap}}
.row3{{position:absolute;top:600px;width:100%;display:flex;justify-content:center;gap:9px;z-index:5}}
.msg{{position:absolute;top:662px;width:100%;text-align:center;z-index:4}}
.strip{{position:absolute;bottom:0;width:100%;display:flex;justify-content:center;align-items:center;gap:7px;padding:10px 0 14px;z-index:4}}
.dot{{border-radius:50%;flex:none}}
{css}
</style></head><body>
<div class="cap">{cap}<small>{sub}</small></div>
<div class="phone {cls}">
 <div class="bg"></div>
 <div class="top"><div class="pill">🔥 4 day streak</div><div class="pill round">🐑</div></div>
 <div class="title"><h1>Momo Merge</h1><p>Cute Fruit Drop</p></div>
 <div class="mascot"></div>
 <div class="best"><div class="bestIn">BEST&nbsp; <b>12,480</b> &nbsp;•&nbsp; 🍉 × 3</div></div>
 <button class="play">▶ PLAY</button>
 <div class="row3"><div class="chip">🎁 Lucky Box</div><div class="chip">🛒 Shop</div><div class="chip">🏆 Ranks</div></div>
 <div class="msg">Merge, grow… and make a Watermelon! 🍉</div>
 <div class="strip">{dots}</div>
</div></body></html>"""

DOTS = "".join(
    f'<div class="dot" style="width:{s}px;height:{s}px;background:radial-gradient(circle at 35% 30%,{l},{c})"></div>'
    for s, l, c in [(12,"#ffb3ab","#e8506a"),(14,"#ffc4d6","#f27fa5"),(16,"#d9b8ff","#8b5cf6"),
                    (18,"#bfe3ff","#4aa8d8"),(21,"#c8f2c0","#43a55c"),(24,"#fff3a6","#f2b53c"),
                    (28,"#ffd9a1","#ff8c42"),(33,"#ff9d9d","#e8506a")])

def mk(name, cap, sub, cls, css):
    (D / f"{name}.html").write_text(SKEL.format(art=ART, css=css, cap=cap, sub=sub, cls=cls, dots=DOTS))

# ---------- 1 · Storybook Paper ----------
mk("opt1-storybook", "Style 1 · Storybook Paper", "mojooda art hi, lekin kagaz + tankay (stitch) wali UI", "s1", """
.s1 .pill{background:rgba(255,248,234,.92);border:2px dashed #b08954;color:#7a5230;border-radius:999px;padding:5px 13px;font-weight:800;font-size:14.5px;box-shadow:0 2px 0 rgba(122,82,48,.35)}
.s1 .round{border-radius:50%;padding:5px 9px}
.s1 h1{font-size:52px;font-weight:800;color:#fff8ea;text-shadow:0 3px 0 #b0713a,0 6px 14px rgba(90,50,20,.45);letter-spacing:.5px}
.s1 .title p{color:#8a5a2b;font-weight:800;font-size:17px;background:rgba(255,248,234,.85);display:inline-block;padding:1px 14px;border-radius:999px;margin-top:2px}
.s1 .mascot{border-radius:50%;border:5px solid #fff3da;outline:3px dashed #b08954;outline-offset:3px;background:url("../../www/assets/bg-portrait.jpg") 62% 96%/330px;box-shadow:0 10px 24px rgba(90,50,20,.35)}
.s1 .bestIn{background:rgba(255,248,234,.94);border:2px solid #d9b77c;color:#7a5230;border-radius:14px;padding:5px 18px;font-weight:700;font-size:16.5px;box-shadow:0 3px 0 rgba(122,82,48,.3)}
.s1 .bestIn b{color:#d2691e;font-size:19px}
.s1 .play{background:linear-gradient(#b07a3e,#8a5a2b);color:#fff3da;border:3px solid #6e4520;border-bottom:8px solid #5d3a1c;border-radius:20px;font-size:31px;font-weight:800;padding:10px 58px 12px;box-shadow:0 8px 18px rgba(70,40,10,.4);text-shadow:0 2px 0 rgba(0,0,0,.25);cursor:pointer}
.s1 .chip{background:rgba(255,248,234,.95);border:2px solid #d9b77c;border-bottom:5px solid #c9a45c;color:#7a5230;border-radius:14px;padding:7px 13px;font-weight:800;font-size:15px}
.s1 .chip:nth-child(2){transform:rotate(-1.2deg)} .s1 .chip:nth-child(3){transform:rotate(1deg)}
.s1 .msg{color:#7a5230;font-weight:700;font-size:15px;text-shadow:0 1px 0 rgba(255,248,234,.8)}
.s1 .strip{background:linear-gradient(transparent,rgba(255,244,214,.65))}
.s1 .dot{border:2px solid rgba(122,82,48,.45)}
""")

# ---------- 2 · Candy Sticker Pop ----------
mk("opt2-sticker", "Style 2 · Candy Sticker Pop", "sab se zyada cute — chunky stickers, sakht saaye, uchhalti rangat", "s2", """
.s2 .bg{background:#ffd9e8}
.s2 .bg::after{content:"";position:absolute;inset:0;background-image:radial-gradient(#ffb7d1 3.2px,transparent 3.6px),radial-gradient(#bfe8ff 3.2px,transparent 3.6px);background-size:52px 52px,68px 68px;background-position:0 0,26px 30px;opacity:.55}
.s2 .pill{background:#fff;border:3px solid #3a2b33;color:#3a2b33;border-radius:999px;padding:4px 13px;font-weight:800;font-size:14.5px;box-shadow:3px 3px 0 #3a2b33}
.s2 .round{border-radius:50%;padding:4px 8px}
.s2 h1{font-size:54px;font-weight:800;color:#ff5d8f;-webkit-text-stroke:2.5px #3a2b33;text-shadow:4px 4px 0 #3a2b33;letter-spacing:.5px}
.s2 .title p{color:#3a2b33;font-weight:800;font-size:16.5px;background:#ffe066;border:3px solid #3a2b33;display:inline-block;padding:0 14px;border-radius:999px;box-shadow:3px 3px 0 #3a2b33;transform:rotate(-1.5deg);margin-top:5px}
.s2 .mascot{border-radius:38% 62% 60% 40%/45% 42% 58% 55%;border:4px solid #3a2b33;background:url("../../www/assets/bg-portrait.jpg") 62% 96%/330px;box-shadow:7px 8px 0 #3a2b33}
.s2 .bestIn{background:#fff;border:3px solid #3a2b33;color:#3a2b33;border-radius:999px;padding:4px 18px;font-weight:800;font-size:16px;box-shadow:3px 3px 0 #3a2b33}
.s2 .bestIn b{color:#ff5d8f}
.s2 .play{background:#43d96b;color:#fff;border:4px solid #3a2b33;border-radius:999px;font-size:32px;font-weight:800;padding:9px 58px 11px;box-shadow:0 7px 0 #3a2b33;text-shadow:0 2px 0 rgba(0,0,0,.18);cursor:pointer}
.s2 .chip{background:#fff;border:3px solid #3a2b33;color:#3a2b33;border-radius:16px;padding:6px 13px;font-weight:800;font-size:15px;box-shadow:3.5px 3.5px 0 #3a2b33}
.s2 .chip:nth-child(1){transform:rotate(-2deg)} .s2 .chip:nth-child(2){background:#bfe8ff} .s2 .chip:nth-child(3){transform:rotate(2deg);background:#ffe3a3}
.s2 .msg{color:#3a2b33;font-weight:800;font-size:15px}
.s2 .strip{background:rgba(255,255,255,.55)}
.s2 .dot{border:2.5px solid #3a2b33}
""")

# ---------- 3 · Orchard Wood Signs ----------
mk("opt3-wood", "Style 3 · Orchard Wood Signs", "khet/farm stand — lakri ke board, rassi, haath ki likhai", "s3", """
.s3 .bg{background:url("../../www/assets/bg-landscape.jpg") center/cover}
.s3 .pill{background:repeating-linear-gradient(0deg,#9c6b34 0 7px,#96652f 7px 14px);border:2.5px solid #5d3a1c;color:#ffeec9;border-radius:9px;padding:4px 12px;font-weight:800;font-size:14px;box-shadow:0 3px 0 rgba(40,22,5,.55);text-shadow:0 1px 0 rgba(0,0,0,.4)}
.s3 .round{border-radius:50%;padding:4px 8px}
.s3 h1{font-size:50px;font-weight:800;color:#ffeec9;text-shadow:0 3px 0 #7c4f1e,0 5px 0 rgba(60,35,8,.55),0 9px 16px rgba(50,30,5,.5)}
.s3 .title p{color:#5d3a1c;font-weight:800;font-size:16px;background:#f3dfae;border:2.5px solid #7c4f1e;display:inline-block;padding:0 14px;border-radius:6px;transform:rotate(-1deg);box-shadow:0 3px 0 rgba(60,35,8,.5);margin-top:4px}
.s3 .mascot{border-radius:18px;border:6px solid #7c4f1e;background:url("../../www/assets/bg-portrait.jpg") 62% 96%/330px;box-shadow:0 10px 0 rgba(60,35,8,.35),0 16px 26px rgba(50,30,5,.4)}
.s3 .bestIn{background:repeating-linear-gradient(0deg,#9c6b34 0 8px,#92622e 8px 16px);border:2.5px solid #5d3a1c;color:#ffeec9;border-radius:9px;padding:5px 18px;font-weight:700;font-size:16px;box-shadow:0 3px 0 rgba(40,22,5,.5);text-shadow:0 1px 0 rgba(0,0,0,.35)}
.s3 .bestIn b{color:#ffd76e;font-size:19px}
.s3 .play{background:repeating-linear-gradient(0deg,#a5713a 0 10px,#9c6b34 10px 20px);color:#ffeec9;border:3.5px solid #5d3a1c;border-radius:14px;font-size:31px;font-weight:800;padding:11px 54px;box-shadow:0 7px 0 #41260e,0 12px 20px rgba(50,30,5,.45);text-shadow:0 2px 0 rgba(0,0,0,.4);letter-spacing:2px;cursor:pointer}
.s3 .chip{background:#f3dfae;border:2.5px solid #7c4f1e;border-bottom:5px solid #7c4f1e;color:#5d3a1c;border-radius:9px;padding:6px 12px;font-weight:800;font-size:14.5px}
.s3 .msg{color:#fff3d0;font-weight:800;font-size:15px;text-shadow:0 2px 3px rgba(60,35,8,.6)}
.s3 .strip{background:linear-gradient(transparent,rgba(63,38,12,.45))}
.s3 .dot{border:2px solid rgba(60,35,8,.55)}
""")

# ---------- 4 · Cozy Night Glow ----------
mk("opt4-night", "Style 4 · Cozy Night Glow", "raat wala sukoon — gehri neeli sham, jalti roshniyan, premium glow", "s4", """
.s4 .bg{background:radial-gradient(420px 300px at 78% 18%,#5a4a8a 0,transparent 60%),radial-gradient(300px 220px at 12% 30%,#3c5a7d 0,transparent 55%),linear-gradient(#1d2440 0%,#2c2a52 46%,#57406b 78%,#8a5f7d 100%)}
.s4 .bg::after{content:"✦ ✧ · ✦ · ✧ ✦ · ✧ · ✦ ✧ · ✦ · ✧ ✦ · · ✦ ✧ ✦";position:absolute;top:8px;left:0;width:100%;color:#ffeec9;font-size:15px;letter-spacing:14px;opacity:.75;text-align:center}
.s4 .pill{background:rgba(24,26,52,.72);border:2px solid rgba(255,220,150,.55);color:#ffe6b0;border-radius:999px;padding:4px 13px;font-weight:800;font-size:14px;box-shadow:0 0 14px rgba(255,190,90,.35)}
.s4 .round{border-radius:50%;padding:4px 8px}
.s4 h1{font-size:52px;font-weight:800;color:#fff2cf;text-shadow:0 0 22px rgba(255,190,90,.75),0 3px 0 #b0713a}
.s4 .title p{color:#ffd98f;font-weight:800;font-size:16.5px;text-shadow:0 0 12px rgba(255,190,90,.8)}
.s4 .mascot{border-radius:50%;border:4px solid rgba(255,220,150,.75);background:url("../../www/assets/bg-portrait.jpg") 62% 96%/330px;box-shadow:0 0 42px rgba(255,180,90,.5),inset 0 0 30px rgba(20,16,50,.45)}
.s4 .bestIn{background:rgba(24,26,52,.72);border:2px solid rgba(255,220,150,.5);color:#ffe6b0;border-radius:999px;padding:4px 18px;font-weight:700;font-size:16px;box-shadow:0 0 16px rgba(255,190,90,.3)}
.s4 .bestIn b{color:#ffd76e}
.s4 .play{background:linear-gradient(#ffb84d,#ff7b3d);color:#fff;border:3px solid #ffd9a0;border-radius:999px;font-size:31px;font-weight:800;padding:10px 58px 12px;box-shadow:0 0 34px rgba(255,150,60,.75),0 6px 0 #b34a1d;text-shadow:0 2px 0 rgba(120,40,0,.35);cursor:pointer}
.s4 .chip{background:rgba(24,26,52,.72);border:2px solid rgba(255,220,150,.5);color:#ffe6b0;border-radius:14px;padding:6px 13px;font-weight:800;font-size:14.5px;box-shadow:0 0 12px rgba(255,190,90,.25)}
.s4 .msg{color:#ffdf9e;font-weight:700;font-size:15px;text-shadow:0 0 10px rgba(255,190,90,.6)}
.s4 .strip{background:linear-gradient(transparent,rgba(16,14,38,.6))}
.s4 .dot{border:2px solid rgba(255,220,150,.5);box-shadow:0 0 8px rgba(255,190,90,.45)}
""")

# ---------- 5 · Vintage Fruit Label ----------
mk("opt5-vintage", "Style 5 · Vintage Fruit Label", "purani peti ke label jaisa poster — chapay hue rang, stamp wali shan", "s5", """
.s5 .bg{background:#f4e7c8}
.s5 .bg::after{content:"";position:absolute;inset:10px;border:3px double #b3402a;border-radius:6px;pointer-events:none}
.s5 .pill{background:#fbf3da;border:2px solid #b3402a;color:#b3402a;border-radius:4px;padding:3px 11px;font-weight:800;font-size:13.5px;letter-spacing:.6px;box-shadow:2px 2px 0 rgba(179,64,42,.4)}
.s5 .round{border-radius:50%;padding:3px 7px}
.s5 h1{font-size:49px;font-weight:800;color:#b3402a;letter-spacing:1px;text-shadow:2.5px 2.5px 0 #e8b64c}
.s5 .title p{color:#4a7c3a;font-weight:800;font-size:15.5px;letter-spacing:3.5px;text-transform:uppercase}
.s5 .title p::before,.s5 .title p::after{content:" ★ "}
.s5 .mascot{border-radius:12px;border:3px solid #4a7c3a;outline:2px solid #b3402a;outline-offset:3px;background:url("../../www/assets/bg-portrait.jpg") 62% 96%/330px;box-shadow:5px 6px 0 rgba(74,124,58,.35)}
.s5 .bestIn{background:#fbf3da;border:2.5px solid #4a7c3a;color:#7a3b2e;border-radius:4px;padding:4px 18px;font-weight:800;font-size:15.5px;letter-spacing:.8px;box-shadow:3px 3px 0 rgba(74,124,58,.35)}
.s5 .bestIn b{color:#b3402a;font-size:18px}
.s5 .play{background:#b3402a;color:#fbf3da;border:3px solid #7e2a1c;border-radius:8px;font-size:30px;font-weight:800;padding:10px 56px 12px;box-shadow:0 6px 0 #7e2a1c;letter-spacing:2.5px;cursor:pointer}
.s5 .chip{background:#fbf3da;border:2.5px solid #b3402a;color:#7a3b2e;border-radius:6px;padding:6px 12px;font-weight:800;font-size:14.5px;box-shadow:2.5px 2.5px 0 rgba(179,64,42,.4)}
.s5 .chip:nth-child(2){transform:rotate(-1.6deg);border-color:#4a7c3a;color:#4a7c3a;box-shadow:2.5px 2.5px 0 rgba(74,124,58,.4)}
.s5 .msg{color:#7a3b2e;font-weight:700;font-size:14.5px;letter-spacing:.4px}
.s5 .strip{background:#eeddB4}
.s5 .dot{border:2px solid rgba(126,42,28,.5)}
""")
print("5 mockup HTML files written:", ", ".join(sorted(x.name for x in D.glob('opt*.html'))))
