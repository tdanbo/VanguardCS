# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

data_list = []

for file in os.listdir("src/.icons"):
    icon_path = os.path.join("src/.icons", file)
    data_list.append((icon_path, ".icons"))

for file in os.listdir("src/.sounds"):
    icon_path = os.path.join("src/.sounds", file)
    data_list.append((icon_path, ".sounds"))

a = Analysis(
    ['src/main.py'],
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
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
