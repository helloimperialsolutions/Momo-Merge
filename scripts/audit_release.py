#!/usr/bin/env python3
"""Fail-closed static preflight for Momo Merge's Cloud AAB build.

Checks source identity, Play API levels/version monotonicity, the user-visible
orientation requirement, core runtime assets, and the post-Capacitor Android
asset mirror. This is not a substitute for browser/device QA.
"""
from __future__ import annotations
import json
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WWW = ROOT / "www"
PUBLIC = ROOT / "android/app/src/main/assets/public"
errors: list[str] = []
notes: list[str] = []

def need(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

html_path = WWW / "index.html"
html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
need(bool(html), "www/index.html missing or empty")
need("window.FM_DEBUG" in html, "FM_DEBUG hook missing from runtime HTML")
need("Engine.update(engine,16.666)" in html, "fixed 16.666ms Engine.update call missing")
need("screen.orientation.lock" not in html, "portrait orientation lock must not ship")
need("rotateOv" not in html, "portrait-only rotate overlay must not ship")

# The app has user-designed toolbar/home artwork plus fruit sprites/backgrounds.
required = [
    "assets/basket-original.png", "assets/bg-landscape.jpg", "assets/bg-portrait.jpg",
    "assets/home-bg-mobile.jpg", "assets/home-bg-wide.jpg", "assets/preloader.jpg",
    "assets/fonts/baloo2.woff2", "assets/fonts/cherry-bomb-one.woff2",
]
required += [f"assets/fruits/f{i}.png" for i in range(11)]
required += [f"assets/icons/{n}.png" for n in (
    "bomb", "freeze", "home", "lucky", "pop", "ranks", "retry", "shop",
    "sweep", "undo", "volume")]
for rel in required:
    p = WWW / rel
    need(p.is_file() and p.stat().st_size > 0, f"required web asset missing/empty: www/{rel}")

class LocalAssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs: list[str] = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"src", "href"} and value:
                self.refs.append(value)

if html:
    parser = LocalAssetParser()
    parser.feed(html)
    for ref in parser.refs:
        parsed = urlparse(ref)
        if parsed.scheme or ref.startswith(("//", "#", "data:", "javascript:", "mailto:")):
            continue
        local = (parsed.path or "").lstrip("/")
        if local and Path(local).suffix and not (WWW / local).is_file():
            errors.append(f"static local HTML asset reference missing: {ref}")
    # CSS background/font references are checked separately from src/href.
    for raw in re.findall(r"url\(\s*['\\\"]?([^)'\"]+)", html, re.I):
        ref = raw.strip()
        parsed = urlparse(ref)
        if parsed.scheme or ref.startswith(("//", "#", "data:", "var(")):
            continue
        local = (parsed.path or "").lstrip("/")
        if local and Path(local).suffix and not (WWW / local).is_file():
            errors.append(f"static local CSS asset reference missing: {ref}")

# Capacitor's sync step must have copied the whole web directory into Android.
need(PUBLIC.is_dir(), "Android Capacitor public assets directory missing; run npx cap sync android")
if PUBLIC.is_dir() and WWW.is_dir():
    for src in sorted(p for p in WWW.rglob("*") if p.is_file()):
        rel = src.relative_to(WWW)
        dst = PUBLIC / rel
        if not dst.is_file():
            errors.append(f"Android public copy missing: {rel.as_posix()}")
        elif src.read_bytes() != dst.read_bytes():
            errors.append(f"Android public copy differs from www/: {rel.as_posix()}")

# Identity/version must match in Capacitor and Android Gradle.
config_path = ROOT / "capacitor.config.json"
try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception as exc:
    config = {}
    errors.append(f"capacitor.config.json invalid: {exc}")
app_id = "com.isstudios.momomerge"
need(config.get("appId") == app_id, f"Capacitor appId must be {app_id}")
gradle = (ROOT / "android/app/build.gradle").read_text(encoding="utf-8")
variables = (ROOT / "android/variables.gradle").read_text(encoding="utf-8")
for pattern, expected, label, text in [
    (r'namespace\s+[\"\']([^\"\']+)', app_id, "Android namespace", gradle),
    (r'applicationId\s+[\"\']([^\"\']+)', app_id, "Android applicationId", gradle),
    (r'compileSdkVersion\s*=\s*(\d+)', "36", "compileSdk", variables),
    (r'targetSdkVersion\s*=\s*(\d+)', "36", "targetSdk", variables),
    (r'minSdkVersion\s*=\s*(\d+)', "24", "minSdk", variables),
    (r'versionCode\s+(\d+)', None, "versionCode", gradle),
    (r'versionName\s+[\"\']([^\"\']+)', None, "versionName", gradle),
]:
    m = re.search(pattern, text)
    if not m:
        errors.append(f"{label} not found")
    elif label == "versionCode":
        try:
            need(int(m.group(1)) >= 4, "versionCode must be >= 4; Play already received versionCode 3")
        except ValueError:
            errors.append("versionCode is not an integer")
    elif label == "versionName":
        need(bool(re.fullmatch(r"\d+\.\d+(?:\.\d+)?", m.group(1))),
             f"versionName must be numeric major.minor[.patch], found {m.group(1)}")
    else:
        need(m.group(1) == expected, f"{label} must be {expected}, found {m.group(1)}")

# Keep accidental signing material out of source archives/repository.
for pattern in ("*.keystore", "*.jks", "SECRETS.txt", "google-services.json"):
    found = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob(pattern)
             if not any(part in {"node_modules", ".git", ".gradle", "build"} for part in p.parts)]
    if found:
        errors.append(f"sensitive/release-only file present in source: {', '.join(found)}")

if errors:
    print("RELEASE PREFLIGHT: FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("RELEASE PREFLIGHT: PASS")
print(f" - package: {app_id}")
print(" - Android: minSdk 24 / compileSdk 36 / targetSdk 36; next Play versionCode >= 4, versionName 1.2 for this candidate")
print(f" - required runtime assets present: {len(required)}; www/ and Android public copies match byte-for-byte")
print(" - fixed timestep / FM_DEBUG present; no portrait lock or rotate gate")
print(" - no keystore or signing-secret file in source tree")
print("NOTE: static preflight does not prove device visuals, performance, signing, policy compliance, or a bug-free release.")
