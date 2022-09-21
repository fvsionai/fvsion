# -*- mode: python ; coding: utf-8 -*-


from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

# Collect metadata for relevant library that is being checked for dependency 
# https://github.com/huggingface/diffusers/blob/2345481c0e21f1bd84c0d85b866b57d34506d836/src/diffusers/dependency_versions_check.py#L26

datas = collect_data_files('torch')
datas += copy_metadata('torch')
datas += copy_metadata('tqdm')
datas += copy_metadata('regex')
datas += copy_metadata('requests')
datas += copy_metadata('packaging')
datas += copy_metadata('filelock')
datas += copy_metadata('numpy')
datas += copy_metadata('tokenizers')
datas += copy_metadata('importlib_metadata')


block_cipher = None


a = Analysis(
    ['py\\main.py'],
    pathex=['py', '.venv/Lib/site-packages'],
    binaries=[],
    datas=datas,
    hiddenimports=[
         'uvicorn.logging',
                'uvicorn.loops',
                'uvicorn.loops.auto',
                'uvicorn.protocols',
                'uvicorn.protocols.http',
                'uvicorn.protocols.http.auto',
                'uvicorn.protocols.websockets',
                'uvicorn.protocols.websockets.auto',
                'uvicorn.lifespan',
                'uvicorn.lifespan.on',
    ],
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

from PyInstaller.building.datastruct import TOC
x = 'cp310-win_amd64'
datas_upd = TOC()

for d in a.datas:
    if x not in d[0] and x not in d[1]:
        datas_upd.append(d)

a.datas = datas_upd

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

