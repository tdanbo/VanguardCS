# -*- mode: python ; coding: utf-8 -*-
import os
import sys

site_packages = next(p for p in sys.path if "site-packages" in p)
print(site_packages)
block_cipher = None

# SCRIPTNAME
scriptname = os.path.basename(os.getcwd())

data_list = []

# WILL ORGANISE ICONS TO DIST FOLDER
icon_root = "src\\.icons"

for data_root in ["src\\.icons", "src\\gui_functions", "src\\gui_windows", "src\\template"]:
    for root, dirs, files in os.walk(data_root, topdown=False):
        for name in files:
            icon_path = os.path.join(root, name)
            data_list.append((icon_path, os.path.basename(data_root)))

a = Analysis(
    ["src\\run.pyw"],
    pathex=[],
    binaries=[],
    datas=data_list,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=scriptname,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon="src\\.icons\\app_icon.ico",
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
