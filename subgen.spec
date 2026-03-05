# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for SubGen."""

import sys
import shutil
from pathlib import Path

# Paths
src_path = Path('src')
resources_path = Path('resources')

block_cipher = None

# Platform-specific FFmpeg binary detection
binaries_list = []

def find_ffmpeg_binaries():
    """Locate FFmpeg binaries for the current platform."""
    ffmpeg_path = shutil.which('ffmpeg')
    ffprobe_path = shutil.which('ffprobe')

    if sys.platform == 'win32':
        # Windows
        if ffmpeg_path:
            binaries_list.append((ffmpeg_path, 'ffmpeg'))
        if ffprobe_path:
            binaries_list.append((ffprobe_path, 'ffmpeg'))
    elif sys.platform == 'darwin':
        # macOS
        if ffmpeg_path:
            binaries_list.append((ffmpeg_path, 'ffmpeg'))
        if ffprobe_path:
            binaries_list.append((ffprobe_path, 'ffmpeg'))
    elif sys.platform.startswith('linux'):
        # Linux
        if ffmpeg_path:
            binaries_list.append((ffmpeg_path, 'ffmpeg'))
        if ffprobe_path:
            binaries_list.append((ffprobe_path, 'ffmpeg'))

    if not binaries_list:
        print("WARNING: FFmpeg binaries not found in PATH!")
        print("The built application may not work correctly.")
    else:
        print(f"Found FFmpeg binaries: {binaries_list}")

    return binaries_list

# Find FFmpeg binaries
ffmpeg_binaries = find_ffmpeg_binaries()

# Analysis
a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=ffmpeg_binaries,
    datas=[
        # Resources
        ('resources/languages.json', 'resources'),
        ('resources/styles/main.qss', 'resources/styles'),
        # Add icons if available
        # ('resources/icons/*.png', 'resources/icons'),
    ],
    hiddenimports=[
        'faster_whisper',
        'PyQt6',
        'ffmpeg',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'PIL',
        'numpy.f2py',
        'scipy',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SubGen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window (GUI application)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/app.ico' if Path('resources/icons/app.ico').exists() else None,
)

# COLLECT
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SubGen',
)
