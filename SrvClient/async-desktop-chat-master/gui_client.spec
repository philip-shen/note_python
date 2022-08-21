# -*- mode: python ; coding: utf-8 -*-
# pyinstaller将含有多个py文件的python程序做成exe
# https://blog.csdn.net/djshichaoren/article/details/79801531

block_cipher = None

a = Analysis(['client.py',
'D:\\projects\\async-desktop-chat-master\\libs\\lib_files.py'
],
             pathex=['D:\\projects\\async-desktop-chat-master'],
             #binaries=[('Debussy_API\\HIF\\lib\\windows\\64bit\\Ginkgo_Driver.dll','.'),('C:\\Windows\\System32\\libusb0.dll','.')],
             datas=[],
             #hiddenimports=['usb'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['jedi'],
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
          name='global_toolkits_server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon='D:\\projects\\gointelligo\\AIBF\\S_Logo_M1.ico', 
          console=False)