#!/bin/bash
# build_mac_app.sh - baut ne native Python Learner.app + .dmg auf
# apple silicon. aus dem build-kit-ordner raus starten
set -euo pipefail
cd "$(dirname "$0")" || exit 1

STEP="start"
trap 'echo ""; echo "BUILD FAILED at step: $STEP" >&2' ERR

VERSION=$(sed -n 's/^VERSION = "\(.*\)"$/\1/p' app/version.py)
[ -n "$VERSION" ] || { echo "could not read VERSION from app/version.py"; exit 1; }
echo "==> Building Python Learner $VERSION for macOS (arm64)"

# ---------- 1. erstmal checken ob alles da is ----------
STEP="preflight"
echo "==> preflight"
if [ "$(uname -m)" != "arm64" ]; then
    echo "This kit builds for Apple Silicon only (uname -m: $(uname -m))."
    exit 1
fi

PYTHON=""
for c in /Library/Frameworks/Python.framework/Versions/3.1[0-9]/bin/python3 \
         /opt/homebrew/bin/python3 python3; do
    for cc in $c; do
        [ -x "$cc" ] || command -v "$cc" >/dev/null 2>&1 || continue
        if "$cc" -c 'import sys; sys.exit(sys.version_info < (3,10))' \
                >/dev/null 2>&1; then
            PYTHON="$cc"; break 2
        fi
    done
done
if [ -z "$PYTHON" ]; then
    echo "Python 3.10+ was not found."
    echo "Install Python 3.12 from https://www.python.org/downloads/macos/ then run this again."
    exit 1
fi
echo "    python: $PYTHON ($("$PYTHON" -c 'import platform; print(platform.python_version())'))"
xcode-select -p >/dev/null 2>&1 || \
    echo "    note: Xcode command-line tools not installed - NOT needed for this" \
         "build; only the stock /usr/bin/python3 stub would require them."

# ---------- 2. venv fürs bauen ----------
STEP="venv"
echo "==> creating build venv"
PYI_VER=$(sed -n 's/^pyinstaller==\(.*\)$/\1/p' requirements-build.txt)
WV_VER=$(sed -n 's/^pywebview==\(.*\)$/\1/p' requirements.txt)
"$PYTHON" -m venv .build-venv
PY="./.build-venv/bin/python"
"$PY" -m pip install --quiet --upgrade pip
"$PY" -m pip install --quiet "pywebview==${WV_VER:-*}" \
    "pyinstaller${PYI_VER:+==$PYI_VER}" pillow
if ! "$PY" -c "import webview, objc, WebKit" >/dev/null 2>&1; then
    echo "==> installing pyobjc bindings"
    "$PY" -m pip install --quiet pyobjc-core pyobjc-framework-Cocoa \
        pyobjc-framework-WebKit pyobjc-framework-Quartz \
        pyobjc-framework-Security
fi
"$PY" -c "import webview, objc, WebKit; print('    webview+pyobjc ok')"

# ---------- 3. learner-runtime (python-build-standalone) ----------
STEP="runtime"
echo "==> fetching standalone Python runtime (aarch64)"
mkdir -p build
RUNTIME_TGZ="build/pbs.tar.gz"
RT_URL=""
echo "    resolving latest python-build-standalone release..."
RT_URL=$("$PY" - <<'PYEOF' 2>/dev/null || true
import json, urllib.request
api = ("https://api.github.com/repos/astral-sh/python-build-standalone"
       "/releases/latest")
data = json.load(urllib.request.urlopen(api, timeout=20))
for a in data["assets"]:
    n = a["name"]
    if ("cpython-3.12." in n and "aarch64-apple-darwin" in n
            and n.endswith("install_only.tar.gz")):
        print(a["browser_download_url"])
        break
PYEOF
)
# falls die github api nicht geht oder rate-limit, hardcoded fallback urls
for u in $RT_URL \
  "https://github.com/astral-sh/python-build-standalone/releases/download/20250612/cpython-3.12.11+20250612-aarch64-apple-darwin-install_only.tar.gz" \
  "https://github.com/astral-sh/python-build-standalone/releases/download/20250517/cpython-3.12.10+20250517-aarch64-apple-darwin-install_only.tar.gz"; do
    [ -n "$u" ] || continue
    echo "    trying $u"
    if curl -fL --retry 2 -o "$RUNTIME_TGZ" "$u"; then
        RT_URL="$u"; break
    fi
    u=""
done
[ -n "$RT_URL" ] || { echo "could not download a runtime - check your connection"; exit 1; }

rm -rf build/runtime build/pbs_tmp
mkdir -p build/pbs_tmp
tar -xzf "$RUNTIME_TGZ" -C build/pbs_tmp
mv build/pbs_tmp/python build/runtime
rm -rf build/pbs_tmp "$RUNTIME_TGZ"
rm -rf build/runtime/lib/python3.12/test
find build/runtime -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
build/runtime/bin/python3 -I -X utf8 -c \
    "import json, math, random, itertools, datetime, string; print('    runtime ok')"

# ---------- 4. icon (optional, geht auch ohne) ----------
STEP="icon"
echo "==> building icon (optional)"
ICON=""
if "$PY" tools/make_icon.py >/dev/null 2>&1 \
        && "$PY" -c "from PIL import Image; Image.open('build/icon.ico').save('build/icon.png')" >/dev/null 2>&1; then
    mkdir -p build/icon.iconset
    sips -s format png -z 16 16     build/icon.png --out build/icon.iconset/icon_16x16.png      >/dev/null 2>&1 || true
    sips -s format png -z 32 32     build/icon.png --out build/icon.iconset/icon_16x16@2x.png   >/dev/null 2>&1 || true
    sips -s format png -z 32 32     build/icon.png --out build/icon.iconset/icon_32x32.png      >/dev/null 2>&1 || true
    sips -s format png -z 64 64     build/icon.png --out build/icon.iconset/icon_32x32@2x.png   >/dev/null 2>&1 || true
    sips -s format png -z 128 128   build/icon.png --out build/icon.iconset/icon_128x128.png    >/dev/null 2>&1 || true
    sips -s format png -z 256 256   build/icon.png --out build/icon.iconset/icon_128x128@2x.png >/dev/null 2>&1 || true
    sips -s format png -z 256 256   build/icon.png --out build/icon.iconset/icon_256x256.png    >/dev/null 2>&1 || true
    sips -s format png -z 512 512   build/icon.png --out build/icon.iconset/icon_256x256@2x.png >/dev/null 2>&1 || true
    sips -s format png -z 512 512   build/icon.png --out build/icon.iconset/icon_512x512.png    >/dev/null 2>&1 || true
    sips -s format png -z 1024 1024 build/icon.png --out build/icon.iconset/icon_512x512@2x.png >/dev/null 2>&1 || true
    iconutil -c icns build/icon.iconset -o build/icon.icns && ICON="build/icon.icns" || true
fi
[ -n "$ICON" ] && echo "    icon: $ICON" || echo "    icon skipped"

# ---------- 5. pyinstaller-spec + build ----------
STEP="pyinstaller"
echo "==> generating spec and running PyInstaller"
HIDDEN=$("$PY" - <<'PYEOF'
import glob, os
mods = sorted("app.content." + os.path.splitext(os.path.basename(p))[0]
              for p in glob.glob("app/content/ch*.py"))
print(" ".join(mods))
PYEOF
)
echo "    hidden imports: $HIDDEN"

ROOT_ABS="$(pwd)"
ICON_LINE=""
[ -n "$ICON" ] && ICON_LINE="    icon=\"$ROOT_ABS/$ICON\","
cat > build/mac_app.spec <<SPECEOF
# wird von build_mac_app.sh generiert, nicht von hand ändern
from PyInstaller.utils.hooks import collect_all

DATAS = [
    ("$ROOT_ABS/app/ui", "app/ui"),
    ("$ROOT_ABS/app/content/data", "app/content/data"),
    ("$ROOT_ABS/build/runtime", "runtime"),
]
HIDDEN = """$HIDDEN""".split()
wv_datas, wv_binaries, wv_hidden = collect_all("webview")

a_gui = Analysis(
    ["$ROOT_ABS/app/main.py"], pathex=["$ROOT_ABS"],
    binaries=wv_binaries, datas=DATAS + wv_datas,
    hiddenimports=HIDDEN + wv_hidden,
)
pyz_gui = PYZ(a_gui.pure)
exe_gui = EXE(
    pyz_gui, a_gui.scripts, [], exclude_binaries=True,
    name="Python Learner", console=False,
)

a_srv = Analysis(
    ["$ROOT_ABS/tools/entry_server.py"], pathex=["$ROOT_ABS"],
    binaries=[], datas=DATAS, hiddenimports=HIDDEN,
)
pyz_srv = PYZ(a_srv.pure)
exe_srv = EXE(
    pyz_srv, a_srv.scripts, [], exclude_binaries=True,
    name="Python Learner Server", console=True,
)

coll = COLLECT(
    exe_gui, a_gui.binaries, a_gui.datas,
    exe_srv, a_srv.binaries, a_srv.datas,
    name="Python Learner",
)

app = BUNDLE(
    coll,
    name="Python Learner.app",
    bundle_identifier="de.pythonlearner.app",
$ICON_LINE
)
SPECEOF

"$PY" -m PyInstaller --noconfirm --clean build/mac_app.spec | tail -5
APP="dist/Python Learner.app"
[ -d "$APP" ] || { echo "PyInstaller did not produce $APP"; exit 1; }

# runtime muss da liegen wo app/pyexe.py danach sucht, sonst fallback auf PATH
FW="$APP/Contents/Frameworks"
if [ ! -x "$FW/runtime/bin/python3" ]; then
    if [ -d "$APP/Contents/Resources/runtime" ]; then
        mkdir -p "$FW"
        ln -s ../Resources/runtime "$FW/runtime" 2>/dev/null || \
            cp -R "$APP/Contents/Resources/runtime" "$FW/runtime"
    elif [ -d "$APP/Contents/MacOS/runtime" ]; then
        mkdir -p "$FW"
        cp -R "$APP/Contents/MacOS/runtime" "$FW/runtime"
    fi
fi
[ -x "$FW/runtime/bin/python3" ] && echo "    bundled runtime in place" \
    || echo "    WARNING: runtime not found under Frameworks (PATH fallback will be used)"

# ---------- 6. ad-hoc signieren + quarantäne weg ----------
STEP="sign"
echo "==> ad-hoc signing the bundle"
xattr -cr "$APP" 2>/dev/null || true
codesign --force --deep --sign - "$APP"

# ---------- 7. smoke test über den gebündelten server ----------
STEP="smoke test"
echo "==> smoke test (server exe inside the .app)"
SRV="$APP/Contents/MacOS/Python Learner Server"
"$SRV" >/tmp/plsrv.log 2>&1 &
SRVPID=$!
sleep 3
ok=""
for _ in $(seq 1 15); do
    if curl -sf -X POST -H "Content-Type: application/json" \
        -d '{}' http://127.0.0.1:8765/api/get_content | \
        grep -q "\"version\": \"$VERSION\""; then ok=1; break; fi
    sleep 1
done
if [ -z "$ok" ]; then
    kill $SRVPID 2>/dev/null || true
    echo "server did not answer or wrong version; log:"; cat /tmp/plsrv.log
    exit 1
fi
RC=$(curl -sf -X POST -H "Content-Type: application/json" \
    -d '{"code":"print(6*7)","stdin_text":""}' \
    http://127.0.0.1:8765/api/run_code)
echo "    run_code: $RC"
echo "$RC" | grep -q '"stdout": "42' || { kill $SRVPID; exit 1; }
CT=$(curl -sf -X POST -H "Content-Type: application/json" \
    -d '{"task_id":"ch00-task-1","code":"print(\"Hello, world!\")"}' \
    http://127.0.0.1:8765/api/check_task)
echo "$CT" | grep -q '"passed": *true' || { kill $SRVPID; echo "$CT"; exit 1; }
echo "    check_task passed"
kill $SRVPID 2>/dev/null || true
rm -f "$HOME/Library/Application Support/PythonLearner/progress.json"

echo "==> launch test: opening the app for 5 seconds"
open "$APP"
sleep 5
pgrep -f "Python Learner" >/dev/null && echo "    app process running" \
    || echo "    WARNING: app process not found"
osascript -e 'quit app "Python Learner"' 2>/dev/null || true

# ---------- 8. dmg bauen ----------
STEP="dmg"
echo "==> building DMG"
rm -rf build/dmg_staging
mkdir -p build/dmg_staging
cp -R "$APP" build/dmg_staging/
ln -s /Applications build/dmg_staging/Applications
DMG="dist/Python Learner-$VERSION.dmg"
hdiutil create -volname "Python Learner" -srcfolder build/dmg_staging \
    -ov -format UDZO "$DMG"
hdiutil verify "$DMG" | tail -2
cp "$DMG" "../Python Learner-$VERSION.dmg"
SHA=$(shasum -a 256 "$DMG" | awk '{print $1}')
SIZE=$(du -h "$DMG" | cut -f1)
echo ""
echo "======================================================"
echo " DONE: $DMG  ($SIZE)"
echo " SHA256: $SHA"
echo " Copied next to the kit as: ../Python Learner-$VERSION.dmg"
echo " Copy Python Learner-$VERSION.dmg to the USB: MAC Releases/ver-$VERSION-mac/"
echo "======================================================"
