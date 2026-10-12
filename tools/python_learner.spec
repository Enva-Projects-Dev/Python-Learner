# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller-spec für Python Learner (Windows, onedir).

Baut zwei exe's in einem COLLECT-ordner:
  - "Python Learner"        windowed gui (pywebview)
  - "Python Learner Server" console dev/browser-server
"""
from pathlib import Path

from PyInstaller.utils.hooks import collect_all

ROOT = Path(SPECPATH).parent

CONTENT_MODS = sorted(
    p.stem for p in (ROOT / "app" / "content").glob("ch*.py"))
HIDDEN = [f"app.content.{m}" for m in CONTENT_MODS]

DATAS = [
    (str(ROOT / "app" / "ui"), "app/ui"),
    (str(ROOT / "app" / "content" / "data"), "app/content/data"),
]

wv_datas, wv_binaries, wv_hidden = collect_all("webview")

ICON = str(ROOT / "build" / "icon.ico")

a_gui = Analysis(
    [str(ROOT / "app" / "main.py")],
    pathex=[str(ROOT)],
    binaries=wv_binaries,
    datas=DATAS + wv_datas,
    hiddenimports=HIDDEN + wv_hidden,
)
pyz_gui = PYZ(a_gui.pure)
exe_gui = EXE(
    pyz_gui, a_gui.scripts, [],
    exclude_binaries=True,
    name="Python Learner",
    console=False,
    icon=ICON,
)

a_srv = Analysis(
    [str(ROOT / "tools" / "entry_server.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=DATAS,
    hiddenimports=HIDDEN,
)
pyz_srv = PYZ(a_srv.pure)
exe_srv = EXE(
    pyz_srv, a_srv.scripts, [],
    exclude_binaries=True,
    name="Python Learner Server",
    console=True,
    icon=ICON,
)

coll = COLLECT(
    exe_gui, a_gui.binaries, a_gui.datas,
    exe_srv, a_srv.binaries, a_srv.datas,
    name="Python Learner",
)
