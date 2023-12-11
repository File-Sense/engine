# -*- mode: python ; coding: utf-8 -*-

from distutils.dir_util import copy_tree

a = Analysis(
    ['main.py'],
    pathex=['../venv/Lib/site-packages'],
    binaries=[],
    datas=[],
    hiddenimports=['psutil'],
    hookspath=['extra-hooks'],
    hooksconfig={},
    runtime_hooks=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='engine-x86_64-unknown-linux-gnu',
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

# copy_tree("data", "../backend/bin/python/data")