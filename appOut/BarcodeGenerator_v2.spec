# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['G:\\programming\\PycharmProjects\\iconsBarCodeGen\\iconsBarcodeGeneratorGUI.py'],
             pathex=['G:\\programming\\PycharmProjects\\iconsBarCodeGen\\appOut'],
             binaries=[],
             datas=[('G:\\programming\\PycharmProjects\\iconsBarCodeGen\\Resource\\DejaVuSansMono.ttf', 'Resource'), ('G:\\programming\\PycharmProjects\\iconsBarCodeGen\\Resource\\generator-icon.png', 'Resource')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='BarcodeGeneratorv2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='G:\\programming\\PycharmProjects\\iconsBarCodeGen\\Resource\\generator-icon.ico')
