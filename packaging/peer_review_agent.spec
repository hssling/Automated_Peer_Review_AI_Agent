# -*- mode: python ; coding: utf-8 -*-

"""PyInstaller spec file to build a standalone peer-review-agent executable."""

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

project_root = Path(__file__).resolve().parents[1]
source_path = project_root / "src"

hidden_imports = []
hidden_imports += collect_submodules("pptx")
hidden_imports += collect_submodules("docx")

a = Analysis(
    ["src/peer_review_agent/cli.py"],
    pathex=[str(project_root), str(source_path)],
    binaries=[],
    datas=[],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="peer-review-agent",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="peer-review-agent",
)
