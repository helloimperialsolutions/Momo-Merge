# -*- coding: utf-8 -*-
import pathlib
import math
D = pathlib.Path('/home/user/fruit-merge/design/ui-mockups')
ART = 'file:///home/user/fruit-merge/www/assets'

FRUITS = [
 ('Cherry','#ff8299','#e8506a','#c23a54','smile','circle'),
 ('Strawberry','#ff9aa9','#f2697c','#d44e62','happy','berry'),
 ('Grape','#d0a6ff','#a06cd5','#7f4fb5','wink','grape'),
 ('Lemon','#ffe680','#f8d34e','#dcb32c','cat','lemon'),
 ('Orange','#ffc069','#f89b3c','#dd7d1d','smile','circle'),
 ('Apple','#ff7b84','#e8434c','#c22c35','happy','apple'),
 ('Peach','#ffd0bd','#f8b19b','#ea8f76','blush','peach'),
 ('Pear','#d7ef9b','#b7d76a','#93b648','wink','pear'),
 ('Pineapple','#ffe066','#f2c14e','#d09f2c','cat','pineapple'),
 ('Melon','#b9eba9','#95d38e','#6caf66','happy','melon'),
 ('Watermelon','#69cf7d','#43a55c','#2c7f42','big','watermelon'),
]

def face(kind):
    eyes_smile = '<path d="M43 55 Q48 49 53 55" fill="none" stroke="#40222d" stroke-width="3.4" stroke-linecap="round"/><path d="M67 55 Q72 49 77 55" fill="none" stroke="#40222d" stroke-width="3.4" stroke-linecap="round"/>'
    eyes_happy = '<path d="M42 56 Q48 49 54 56" fill="none" stroke="#40222d" stroke-width="3.4" stroke-linecap="round"/><path d="M66 56 Q72 49 78 56" fill="none" stroke="#40222d" stroke-width="3.4" stroke-linecap="round"/>'
    if kind == 'smile':
        return eyes_smile + '<path d="M51 66 Q60 74 69 66" fill="none" stroke="#40222d" stroke-width="3.6" stroke-linecap="round"/>'
    if kind == 'happy':
        return eyes_happy + '<path d="M50 65 Q60 76 70 65 Q60 70 50 65" fill="#40222d"/><circle cx="38" cy="66" r="5" fill="#ff8fab" opacity=".65"/><circle cx="82" cy="66" r="5" fill="#ff8fab" opacity=".65"/>'
    if kind == 'wink':
        return '<circle cx="47" cy="54" r="3.4" fill="#40222d"/><path d="M66 55 Q72 50 78 55" fill="none" stroke="#40222d" stroke-width="3.4" stroke-linecap="round"/><path d="M52 67 Q60 73 69 66" fill="none" stroke="#40222d" stroke-width="3.6" stroke-linecap="round"/><circle cx="82" cy="66" r="5" fill="#ff8fab" opacity=".6"/>'
    if kind == 'cat':
        return eyes_happy + '<path d="M52 66 Q56 61 60 66 Q64 61 68 66 Q64 72 60 69 Q56 72 52 66" fill="none" stroke="#40222d" stroke-width="3.1" stroke-linecap="round" stroke-linejoin="round"/><circle cx="38" cy="65" r="4.6" fill="#ff8fab" opacity=".6"/><circle cx="82" cy="65" r="4.6" fill="#ff8fab" opacity=".6"/>'
    if kind == 'blush':
        return '<path d="M42 56 Q48 51 54 56" fill="none" stroke="#40222d" stroke-width="3.4" stroke-linecap="round"/><path d="M66 56 Q72 51 78 56" fill="none" stroke="#40222d" stroke-width="3.4" stroke-linecap="round"/><path d="M53 67 Q60 72 67 67" fill="none" stroke="#40222d" stroke-width="3.4" stroke-linecap="round"/><circle cx="36" cy="66" r="6" fill="#ff7d9c" opacity=".75"/><circle cx="84" cy="66" r="6" fill="#ff7d9c" opacity=".75"/>'
    return eyes_happy + '<path d="M47 64 Q60 79 73 64 Q60 71 47 64" fill="#40222d"/><circle cx="36" cy="65" r="5.5" fill="#ff8fab" opacity=".65"/><circle cx="84" cy="65" r="5.5" fill="#ff8fab" opacity=".65"/>'

def shape(kind, fill, stroke, sw, extra=''):
    if kind in ('circle','grape','melon','watermelon'):
        return f'<circle cx="60" cy="63" r="38" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    if kind == 'berry':
        return f'<path d="M60 99 C31 82 25 51 39 35 C49 24 71 24 81 35 C95 51 89 82 60 99Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'
    if kind == 'lemon':
        return f'<ellipse cx="60" cy="62" rx="42" ry="31" transform="rotate(-24 60 62)" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    if kind == 'apple':
        return f'<path d="M60 35 C51 24 31 29 27 48 C23 68 38 94 51 96 C56 97 60 94 60 90 C60 94 64 97 69 96 C82 94 97 68 93 48 C89 29 69 24 60 35Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'
    if kind == 'peach':
        return f'<path d="M60 24 C83 24 94 43 91 64 C88 85 74 97 60 97 C46 97 32 85 29 64 C26 43 37 24 60 24Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    if kind == 'pear':
        return f'<path d="M60 22 C70 22 75 31 73 42 C86 50 91 63 86 76 C80 91 68 98 60 98 C52 98 40 91 34 76 C29 63 34 50 47 42 C45 31 50 22 60 22Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'
    if kind == 'pineapple':
        return f'<ellipse cx="60" cy="66" rx="34" ry="38" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    return f'<circle cx="60" cy="63" r="38" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def accessories(kind):
    leaf = '<path d="M61 25 C66 12 82 10 88 13 C85 25 72 31 61 25Z" fill="#43a55c" stroke="#2f6f3e" stroke-width="3" stroke-linejoin="round"/>'
    stem = '<path d="M60 29 C61 21 66 15 72 12" fill="none" stroke="#7a4a21" stroke-width="4" stroke-linecap="round"/>'
    if kind == 'Cherry':
        return '<path d="M62 27 C66 13 79 7 91 8 C87 20 75 28 62 27Z" fill="#43a55c" stroke="#2f6f3e" stroke-width="3"/><path d="M60 38 C62 28 66 18 78 11" fill="none" stroke="#7a4a21" stroke-width="4" stroke-linecap="round"/>'
    if kind == 'Strawberry':
        return '<path d="M60 28 L48 15 L54 30 L60 17 L67 30 L73 15Z" fill="#43a55c" stroke="#2f6f3e" stroke-width="3" stroke-linejoin="round"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="#fff0a6"/>' for x,y in [(45,52),(60,47),(74,53),(50,68),(68,70),(59,82)])
    if kind == 'Grape':
        return leaf + '<circle cx="39" cy="48" r="15" fill="#b889e8"/><circle cx="81" cy="48" r="15" fill="#b889e8"/><circle cx="38" cy="72" r="14" fill="#9a63cf"/><circle cx="82" cy="72" r="14" fill="#9a63cf"/>'
    if kind == 'Apple': return stem + leaf
    if kind == 'Pear': return stem + leaf
    if kind == 'Peach': return '<path d="M62 25 C67 14 80 11 86 14 C83 24 72 29 62 25Z" fill="#5cb85c" stroke="#2f6f3e" stroke-width="3"/><path d="M60 27 C56 43 56 76 61 96" fill="none" stroke="#e58a72" stroke-width="3" opacity=".65"/>'
    if kind == 'Pineapple':
        return '<path d="M60 29 L45 8 L54 27 L60 7 L67 27 L76 8Z" fill="#43a55c" stroke="#2f6f3e" stroke-width="3" stroke-linejoin="round"/><clipPath id="pclip"><ellipse cx="60" cy="66" rx="34" ry="38"/></clipPath><g clip-path="url(#pclip)" stroke="#c98f22" stroke-width="2.4" opacity=".65"><path d="M25 40 L95 105 M25 65 L85 112 M35 30 L100 82 M95 40 L25 105 M95 65 L35 112 M85 30 L20 82"/></g>'
    if kind == 'Melon':
        return '<clipPath id="mclip"><circle cx="60" cy="63" r="38"/></clipPath><g clip-path="url(#mclip)" fill="none" stroke="#dff3c9" stroke-width="5" opacity=".8"><path d="M42 27 C35 55 35 75 43 99 M60 25 C58 55 58 75 60 100 M78 27 C85 55 85 75 77 99"/></g>'
    if kind == 'Watermelon':
        return '<clipPath id="wclip"><circle cx="60" cy="63" r="38"/></clipPath><g clip-path="url(#wclip)" fill="none" stroke="#20713a" stroke-width="7" opacity=".75"><path d="M38 27 C31 55 31 76 39 99 M60 25 C59 53 59 78 60 100 M82 27 C89 55 89 76 81 99"/></g><path d="M60 25 C62 18 68 14 74 14" fill="none" stroke="#2f6f3e" stroke-width="4" stroke-linecap="round"/>'
    return ''

def fruit_svg(i, scale=1.0):
    name, light, c, dark, fkind, skind = FRUITS[i]
    gid = f'g{i}'
    main = shape(skind, f'url(#{gid})', '#3a2b33', 4.2)
    halo = shape(skind, 'white', 'white', 11)
    return f'''<svg viewBox="0 0 120 120" style="width:{120*scale}px;height:{120*scale}px;overflow:visible">
<defs><radialGradient id="{gid}" cx="35%" cy="28%" r="78%"><stop offset="0%" stop-color="{light}"/><stop offset="58%" stop-color="{c}"/><stop offset="100%" stop-color="{dark}"/></radialGradient></defs>
<g>{halo}{main}<ellipse cx="45" cy="43" rx="12" ry="8" fill="white" opacity=".38" transform="rotate(-24 45 43)"/>{accessories(name)}{face(fkind)}</g></svg>'''

# --- Furry round redesign: NO candy/sticker look on characters.
# Every fruit is a round furry ball: lots of soft hair tufts all around,
# a smooth fruit-coloured face in the middle, identity from colour/detail.
def fruit_svg(i, scale=1.0):
    name, light, c, dark, fkind, skind = FRUITS[i]
    gid = 'fur' + str(i)
    rnd = __import__('random').Random(700 + i)
    cx, cy, R = 60, 62, 34
    fur = []
    shades = [light, c, dark]
    # back layer: long soft tufts all the way around
    for a in range(0, 360, 9):
        rad = math.radians(a)
        length = 13 + rnd.random() * 9
        spread = math.radians(7.5)
        x1 = cx + (R - 2) * math.cos(rad - spread); y1 = cy + (R - 2) * math.sin(rad - spread)
        x2 = cx + (R - 2) * math.cos(rad + spread); y2 = cy + (R - 2) * math.sin(rad + spread)
        tx = cx + (R + length) * math.cos(rad); ty = cy + (R + length) * math.sin(rad)
        shade = shades[rnd.randrange(3)]
        fur.append('<path d="M{:.1f} {:.1f} L{:.1f} {:.1f} L{:.1f} {:.1f} Z" fill="{}" stroke="{}" stroke-width="6" stroke-linejoin="round"/>'.format(x1, y1, tx, ty, x2, y2, shade, shade))
    # front layer: loose hair strands sticking out at uneven angles
    for a in range(4, 360, 13):
        rad = math.radians(a + rnd.uniform(-4, 4))
        r1 = R + 2; r2 = R + 15 + rnd.random() * 9
        bend = math.radians(a + 14)
        x1 = cx + r1 * math.cos(rad); y1 = cy + r1 * math.sin(rad)
        x2 = cx + r2 * math.cos(rad); y2 = cy + r2 * math.sin(rad)
        xm = cx + (r2 - 4) * math.cos(bend); ym = cy + (r2 - 4) * math.sin(bend)
        shade = shades[rnd.randrange(2)]
        fur.append('<path d="M{:.1f} {:.1f} Q{:.1f} {:.1f} {:.1f} {:.1f}" fill="none" stroke="{}" stroke-width="3" stroke-linecap="round" opacity=".9"/>'.format(x1, y1, xm, ym, x2, y2, shade))
    clip = '<clipPath id="{}c"><circle cx="60" cy="62" r="34"/></clipPath>'.format(gid)
    detail = ''
    if name == 'Strawberry':
        detail = ''.join('<circle cx="{}" cy="{}" r="2" fill="#fff0a6" opacity=".9"/>'.format(x, y) for x, y in [(45,50),(60,45),(74,51),(48,66),(68,68),(58,80),(76,78)])
    elif name == 'Grape':
        detail = '<g fill="#ffffff" opacity=".25"><circle cx="45" cy="48" r="11"/><circle cx="72" cy="44" r="9"/><circle cx="76" cy="72" r="10"/><circle cx="46" cy="76" r="8"/></g>'
    elif name == 'Pineapple':
        detail = '<g clip-path="url(#{0}c)" stroke="#c98f22" stroke-width="2.2" opacity=".5"><path d="M25 38 L95 104 M25 62 L84 110 M36 28 L100 80 M95 38 L25 104 M95 62 L36 110 M84 28 L20 80"/></g>'.format(gid)
    elif name == 'Melon':
        detail = '<g clip-path="url(#{0}c)" fill="none" stroke="#eef7d2" stroke-width="4.5" opacity=".8"><path d="M43 29 C36 55 36 72 43 95 M60 27 C58 55 58 75 60 97 M77 29 C84 55 84 72 77 95"/></g>'.format(gid)
    elif name == 'Watermelon':
        detail = '<g clip-path="url(#{0}c)" fill="none" stroke="#20713a" stroke-width="6" opacity=".7"><path d="M39 29 C32 55 32 74 39 95 M60 27 C59 54 59 76 60 97 M81 29 C88 55 88 74 81 95"/></g>'.format(gid)
    elif name == 'Peach':
        detail = '<path d="M61 30 C56 46 56 76 62 94" fill="none" stroke="#e58a72" stroke-width="3" opacity=".55"/>'
    elif name == 'Pear':
        detail = '<ellipse cx="60" cy="76" rx="19" ry="15" fill="#ffffff" opacity=".25"/>'
    elif name == 'Orange':
        detail = ''.join('<circle cx="{}" cy="{}" r="1.6" fill="#e07b1f" opacity=".5"/>'.format(x, y) for x, y in [(42,45),(78,50),(50,82),(72,80)])
    # short inner fur strokes near the rim, like combed hair
    inner_fur = []
    for a in range(0, 360, 30):
        rad = math.radians(a + rnd.uniform(-5, 5))
        x1 = cx + 30 * math.cos(rad); y1 = cy + 30 * math.sin(rad)
        x2 = cx + 36 * math.cos(rad + 0.16); y2 = cy + 36 * math.sin(rad + 0.16)
        inner_fur.append('<path d="M{:.1f} {:.1f} Q{:.1f} {:.1f} {:.1f} {:.1f}" fill="none" stroke="{}" stroke-width="2.2" stroke-linecap="round" opacity=".5"/>'.format(x1, y1, (x1+x2)/2, (y1+y2)/2 - 2, x2, y2, light))
    leaf = '<path d="M62 26 C67 12 84 8 91 12 C87 25 73 32 62 26Z" fill="#57bd63" stroke="#2f6f3e" stroke-width="3" stroke-linejoin="round"/>'
    stem = '<path d="M60 28 C61 20 66 14 73 11" fill="none" stroke="#7a4a21" stroke-width="4" stroke-linecap="round"/>'
    top = ''
    if name in ('Apple', 'Pear'):
        top = stem + leaf
    elif name == 'Cherry':
        top = '<path d="M61 27 C64 13 78 5 92 7 C88 20 74 28 61 27Z" fill="#57bd63" stroke="#2f6f3e" stroke-width="3" stroke-linejoin="round"/><path d="M60 33 C62 23 68 14 80 9" fill="none" stroke="#7a4a21" stroke-width="4" stroke-linecap="round"/>'
    elif name == 'Strawberry':
        top = '<path d="M60 29 L47 13 L54 30 L60 15 L67 30 L74 13Z" fill="#57bd63" stroke="#2f6f3e" stroke-width="3" stroke-linejoin="round"/>'
    elif name == 'Pineapple':
        top = '<path d="M60 28 L44 5 L54 26 L60 4 L67 26 L77 5Z" fill="#57bd63" stroke="#2f6f3e" stroke-width="3" stroke-linejoin="round"/>'
    elif name in ('Grape', 'Lemon', 'Orange', 'Peach', 'Melon'):
        top = leaf
    elif name == 'Watermelon':
        top = '<path d="M60 26 C62 18 68 13 75 12" fill="none" stroke="#2f6f3e" stroke-width="4" stroke-linecap="round"/>'
    parts = []
    parts.append('<svg viewBox="0 0 120 120" style="width:{}px;height:{}px;overflow:visible">'.format(int(120*scale), int(120*scale)))
    parts.append('<defs><radialGradient id="{}" cx="38%" cy="28%" r="78%"><stop offset="0%" stop-color="{}"/><stop offset="60%" stop-color="{}"/><stop offset="100%" stop-color="{}"/></radialGradient>{}</defs>'.format(gid, light, c, dark, clip))
    parts.append('<ellipse cx="60" cy="106" rx="27" ry="5.5" fill="#3a2b33" opacity=".16"/>')
    parts.append(''.join(fur))
    parts.append('<circle cx="60" cy="62" r="34" fill="url(#{})"/>'.format(gid))
    parts.append('<g clip-path="url(#{}c)">{}<ellipse cx="60" cy="92" rx="24" ry="8" fill="{}" opacity=".15"/></g>'.format(gid, detail, dark))
    parts.append(''.join(inner_fur))
    parts.append('<ellipse cx="46" cy="43" rx="11" ry="7" fill="#fff" opacity=".38" transform="rotate(-24 46 43)"/>')
    parts.append('<circle cx="39" cy="67" r="5.4" fill="#ff8fab" opacity=".7"/><circle cx="81" cy="67" r="5.4" fill="#ff8fab" opacity=".7"/>')
    parts.append(top)
    parts.append(face(fkind))
    parts.append('</svg>')
    return ''.join(parts)

COMMON = """
@font-face{font-family:Baloo;src:url("file:///tmp/baloo.ttf")}
*{margin:0;box-sizing:border-box;font-family:Baloo,'Trebuchet MS',sans-serif}
body{background:#261d24;display:flex;align-items:center;justify-content:center}
.phone{width:400px;height:720px;border-radius:34px;overflow:hidden;position:relative;background:#ffd9e8;flex:none}
.dots{position:absolute;inset:0;background-image:radial-gradient(#ffabc9 3.2px,transparent 3.7px),radial-gradient(#bfe8ff 3px,transparent 3.5px);background-size:52px 52px,70px 70px;background-position:0 0,25px 28px;opacity:.6}
.art{position:absolute;left:0;right:0;bottom:0;height:330px;background:url("ARTURL/bg-portrait.jpg") center 72%/cover;opacity:.34;mask-image:linear-gradient(transparent,#000 45%)}
.pill{background:#fff;border:3px solid #3a2b33;color:#3a2b33;border-radius:999px;padding:5px 13px;font-weight:800;box-shadow:3.5px 3.5px 0 #3a2b33;font-size:14.5px}
.title h1{font-size:55px;line-height:.95;font-weight:800;color:#ff5d8f;-webkit-text-stroke:2.5px #3a2b33;text-shadow:4.5px 4.5px 0 #3a2b33;letter-spacing:.3px;text-align:center}
.sub{display:inline-block;background:#ffe066;border:3px solid #3a2b33;border-radius:999px;box-shadow:3.5px 3.5px 0 #3a2b33;padding:1px 15px;font-weight:800;color:#3a2b33;transform:rotate(-1.4deg)}
.chipbtn{background:#fff;border:3px solid #3a2b33;color:#3a2b33;border-radius:17px;padding:7px 12px;font-weight:800;box-shadow:4px 4px 0 #3a2b33;font-size:15px;text-align:center}
.playbtn{background:#43d96b;color:white;border:4px solid #3a2b33;border-radius:999px;font-size:32px;font-weight:800;height:76px;padding:0 58px;box-shadow:0 8px 0 #3a2b33;text-shadow:0 2px 0 rgba(0,0,0,.2);display:flex;align-items:center;justify-content:center;line-height:1}
""".replace('ARTURL', ART)

home = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>{COMMON}
.top{{position:absolute;top:14px;left:14px;right:14px;display:flex;justify-content:space-between;z-index:5}}
.title{{position:absolute;top:66px;width:100%;text-align:center;z-index:4}}
.mascot{{position:absolute;left:50%;top:190px;transform:translateX(-50%);width:216px;height:216px;border-radius:42% 58% 55% 45%/48% 42% 58% 52%;border:4.5px solid #3a2b33;background:url('{ART}/bg-portrait.jpg') 62% 96%/335px;box-shadow:8px 9px 0 #3a2b33;z-index:3}}
.mascot:after{{content:'💤';position:absolute;right:-19px;top:-16px;font-size:30px;transform:rotate(10deg)}}
.best{{position:absolute;top:432px;width:100%;display:flex;justify-content:center;z-index:4}}
.play{{position:absolute;top:486px;left:50%;transform:translateX(-50%);z-index:5}}
.row{{position:absolute;top:600px;width:100%;display:flex;justify-content:center;gap:9px;z-index:5}}
.msg{{position:absolute;top:660px;width:100%;text-align:center;color:#3a2b33;font-weight:800;font-size:15px;z-index:4}}
.strip{{position:absolute;bottom:0;left:0;right:0;background:rgba(255,255,255,.58);display:flex;justify-content:center;align-items:center;gap:7px;padding:9px 0 13px;z-index:4}}
.dot{{border-radius:50%;border:2.5px solid #3a2b33}}
</style></head><body><div class='phone'><div class='dots'></div><div class='art'></div>
<div class='top'><div class='pill'>🔥 4 day streak</div><div class='pill' style='border-radius:50%;padding:5px 9px'>🍉</div></div>
<div class='title'><h1>Momo Merge</h1><div class='sub'>Cute Fruit Drop</div></div><div class='mascot'></div>
<div class='best'><div class='pill' style='font-size:16px'>BEST&nbsp; <span style='color:#ff5d8f'>12,480</span> &nbsp;•&nbsp; 🍉 ×3</div></div>
<div class='play'><button class='playbtn'>▶ PLAY</button></div>
<div class='row'><div class='chipbtn' style='transform:rotate(-2deg)'>🎁 Lucky Box</div><div class='chipbtn' style='background:#bfe8ff'>🛒 Shop</div><div class='chipbtn' style='background:#ffe3a3;transform:rotate(2deg)'>🏆 Ranks</div></div>
<div class='msg'>Merge, grow… and make a Watermelon! 🍉</div>
<div class='strip'>{''.join(f"<div class='dot' style='width:{s}px;height:{s}px;background:{c}'></div>" for s,c in [(13,'#e8506a'),(15,'#f27fa5'),(17,'#a06cd5'),(19,'#4aa8d8'),(22,'#43a55c'),(25,'#f2b53c'),(29,'#ff8c42'),(34,'#e8506a')])}</div>
</div></body></html>"""

fruit_positions = [
 (9, 240, 424, 1.16), (8, 193, 458, 1.02), (7, 105, 487, .92),
 (6, 261, 512, .78), (5, 147, 537, .74), (4, 218, 555, .62),
 (3, 91, 566, .54), (2, 292, 573, .55), (1, 168, 591, .48), (0, 250, 601, .42),
]
fruit_divs = ''.join(f"<div style='position:absolute;left:{x}px;top:{y-10}px;z-index:{3+i}'>{fruit_svg(idx, sc)}</div>" for i,(idx,x,y,sc) in enumerate(fruit_positions))
gameplay = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>{COMMON}
.phone{{background:#ffd9e8}}
.topbar{{position:absolute;top:12px;left:12px;right:12px;display:flex;gap:9px;align-items:center;z-index:8}}
.score{{flex:1;background:#fff;border:3.5px solid #3a2b33;border-radius:18px;box-shadow:4px 4px 0 #3a2b33;padding:5px 13px;color:#3a2b33}}
.score small{{display:block;font-size:11px;letter-spacing:1.5px;color:#a26;font-weight:800;line-height:1}} .score b{{font-size:25px;line-height:1;color:#ff5d8f}}
.roundbtn{{width:48px;height:48px;border-radius:50%;background:#fff;border:3.5px solid #3a2b33;box-shadow:3.5px 3.5px 0 #3a2b33;display:flex;align-items:center;justify-content:center;font-size:21px}}
.nextbox{{position:absolute;top:78px;right:12px;z-index:8;background:#fff;border:3px solid #3a2b33;border-radius:16px;box-shadow:3.5px 3.5px 0 #3a2b33;padding:4px 9px;display:flex;align-items:center;gap:4px;color:#3a2b33;font-weight:800;font-size:12px}}
.powers{{position:absolute;top:82px;left:12px;right:176px;display:flex;gap:6px;z-index:8}}
.pbtn{{position:relative;width:48px;height:48px;border-radius:16px;border:3.5px solid #3a2b33;box-shadow:3px 3px 0 #3a2b33;display:flex;align-items:center;justify-content:center;font-size:22px;background:#fff}}
.badge{{position:absolute;right:-6px;top:-7px;background:#ff5d8f;color:white;border:2.5px solid #3a2b33;border-radius:50%;width:21px;height:21px;font-size:11px;display:flex;align-items:center;justify-content:center;font-weight:800}}
.board{{position:absolute;left:16px;right:16px;top:145px;bottom:78px;background:linear-gradient(#fff8e8,#ffedc9);border:4.5px solid #3a2b33;border-radius:25px;box-shadow:7px 8px 0 #3a2b33;overflow:hidden}}
.board:before{{content:'';position:absolute;inset:0;background-image:radial-gradient(#ffd1df 2.4px,transparent 2.8px);background-size:34px 34px;opacity:.7}}
.danger{{position:absolute;left:12px;right:12px;top:48px;border-top:4px dashed #ff5d8f;opacity:.85}}
.guide{{position:absolute;left:50%;top:52px;bottom:110px;border-left:3px dotted rgba(58,43,51,.45)}}
.aim{{position:absolute;left:50%;top:155px;transform:translateX(-50%);z-index:6}}
.mergepop{{position:absolute;left:50%;top:318px;transform:translateX(-50%) rotate(-3deg);z-index:10;background:#ffe066;border:3.5px solid #3a2b33;box-shadow:4px 4px 0 #3a2b33;border-radius:999px;padding:3px 16px;font-weight:800;color:#3a2b33;font-size:19px}}
.floatscore{{position:absolute;left:232px;top:384px;z-index:10;color:#ff8a00;font-size:30px;font-weight:800;text-shadow:2px 2px 0 #fff,-1px -1px 0 #fff}}
.strip{{position:absolute;bottom:0;left:0;right:0;height:66px;background:#fff;border-top:4px solid #3a2b33;display:flex;justify-content:center;align-items:center;gap:5px;z-index:8}}
.minifruit{{display:flex;align-items:center;justify-content:center}}
.combo{{position:absolute;left:24px;top:156px;z-index:9;background:#ff5d8f;color:#fff;border:3px solid #3a2b33;border-radius:999px;box-shadow:3px 3px 0 #3a2b33;padding:1px 11px;font-weight:800}}
</style></head><body><div class='phone'><div class='dots'></div>
<div class='topbar'><div class='score'><small>SCORE</small><b>1,248</b></div><div class='score' style='text-align:right'><small>BEST</small><b style='color:#f2a007'>12,480</b></div><div class='roundbtn'>🏠</div></div>
<div class='powers'><div class='pbtn' style='background:#ffd0d0'>💣<span class='badge'>2</span></div><div class='pbtn' style='background:#ffe3a3'>🧹<span class='badge'>1</span></div><div class='pbtn' style='background:#d8f3ff'>↩️<span class='badge'>1</span></div><div class='pbtn' style='background:#dff3ff'>❄️<span class='badge'>1</span></div><div class='pbtn' style='background:#ffc7dd'>🎈<span class='badge'>3</span></div></div>
<div class='nextbox'>NEXT {fruit_svg(4,.28)}{fruit_svg(2,.23)}</div><div class='combo'>🔥 COMBO ×3</div>
<div class='board'><div class='danger'></div><div class='guide'></div></div>{fruit_divs}<div class='aim'>{fruit_svg(0,.52)}</div><div class='mergepop'>MERGE!</div><div class='floatscore'>+36</div>
<div class='strip'>{''.join(f"<div class='minifruit'>{fruit_svg(i,.22 + i*.018)}</div>" for i in range(11))}</div>
</div></body></html>"""

cards = []
for i, fr in enumerate(FRUITS):
    scale = .92 if i < 10 else 1.08
    cards.append(f"""<div class='card'><div class='num'>{i+1:02d}</div><div class='fruit'>{fruit_svg(i, scale)}</div><h3>{fr[0]}</h3><p>{['Tiny starter','Sweet & speedy','Bouncy bunch','Sour cutie','Round & cheerful','Crisp classic','Soft blusher','Winky fresh','Tropical crown','Gentle giant','GRAND PRIZE!'][i]}</p></div>""")
sheet = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>
@font-face{{font-family:Baloo;src:url('file:///tmp/baloo.ttf')}}*{{margin:0;box-sizing:border-box;font-family:Baloo,'Trebuchet MS',sans-serif}}body{{background:#ffd9e8;background-image:radial-gradient(#ffabc9 3px,transparent 3.5px),radial-gradient(#bfe8ff 3px,transparent 3.5px);background-size:52px 52px,72px 72px;width:1440px;min-height:1000px;padding:34px;color:#3a2b33}}
header{{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:22px}}h1{{font-size:55px;color:#ff5d8f;-webkit-text-stroke:2px #3a2b33;text-shadow:4px 4px 0 #3a2b33}}header p{{font-weight:800;font-size:19px}} .tag{{background:#ffe066;border:3.5px solid #3a2b33;border-radius:999px;box-shadow:4px 4px 0 #3a2b33;padding:7px 16px;font-weight:800;transform:rotate(-1.5deg)}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:17px}}.card{{position:relative;background:#fff;border:4px solid #3a2b33;border-radius:27px;box-shadow:6px 6px 0 #3a2b33;min-height:255px;padding:14px 10px 12px;text-align:center;overflow:hidden}}.card:nth-child(3n+1){{transform:rotate(-.55deg)}}.card:nth-child(3n+2){{transform:rotate(.45deg)}}.num{{position:absolute;left:13px;top:10px;background:#ffe066;border:3px solid #3a2b33;border-radius:50%;width:37px;height:37px;display:flex;align-items:center;justify-content:center;font-weight:800;z-index:3}}.fruit{{height:142px;display:flex;align-items:center;justify-content:center}}h3{{font-size:25px;line-height:1;color:#3a2b33}}.card p{{font-weight:700;color:#8a7480;font-size:15px;margin-top:3px}}.hero{{background:linear-gradient(135deg,#fff,#ffe3ef)}}.footer{{margin-top:20px;display:flex;gap:12px;align-items:center}}.note{{background:#fff;border:3px solid #3a2b33;border-radius:16px;box-shadow:4px 4px 0 #3a2b33;padding:9px 14px;font-weight:800}}
</style></head><body><header><div><h1>Fluffy Fruit Friends</h1><p>Momo Merge · official character lineup</p></div><div class='tag'>11 FRUITS · MERGE TO GROW! 🍉</div></header>
<div class='grid'>{''.join(cards)}</div><div class='footer'><div class='note'>🦁 Style rules: lots of soft fur all around · round smooth faces · fruit colours · sleepy-cute expressions</div><div class='note' style='background:#ffe066'>Same gang — now with fur!</div></div></body></html>"""

(D/'candy-home.html').write_text(home)
(D/'candy-gameplay.html').write_text(gameplay)
(D/'candy-character-sheet.html').write_text(sheet)
print('Candy showcase HTML written')
