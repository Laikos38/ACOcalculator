# -*- mode: python ; coding: utf-8 -*-
"""
Archivo de configuración de PyInstaller para ACOCalculator.
Genera ejecutables standalone para Windows, macOS y Linux.
"""

block_cipher = None

import os
import sys

# Incluir config.ini solo si existe (opcional)
datas_list = [('src', 'src')]  # Siempre incluir el paquete src
if os.path.exists('config.ini'):
    datas_list.append(('config.ini', '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas_list,
    hiddenimports=[
        'xlwt',
        'configparser',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pytest',
        'faker',
        'factory',
        '_pytest',
        'tests',
    ],
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
    name='ACOCalculator',
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
    icon=None,  # Windows: icon.ico, macOS: icon.icns
)

# Para macOS, crear bundle .app (solo se genera en macOS)
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='ACOCalculator.app',
        icon=None,
        bundle_identifier='com.acocalculator.app',
        info_plist={
            'CFBundleName': 'ACOCalculator',
            'CFBundleDisplayName': 'ACO Calculator',
            'CFBundleGetInfoString': 'Sistema de Gestión de Calificaciones de Moodle',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHumanReadableCopyright': 'Copyright © 2025',
            'NSHighResolutionCapable': True,
        },
    )

