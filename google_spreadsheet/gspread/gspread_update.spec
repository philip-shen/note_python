# -*- mode: python ; coding: utf-8 -*-
# pyinstaller将含有多个py文件的python程序做成exe
# https://blog.csdn.net/djshichaoren/article/details/79801531

block_cipher = None

a = Analysis(['gspread_update.py',
'.\\_Libs\\googleSS.py',
'.\\_Libs\\lib_misc.py',
'.\\_Libs\\logger_setup.py',
'.\\_Libs\\yahooFinance.py'
],
             pathex=['D:\\projects\\note_python\\google_spreadsheet\\gspread','D:\\projects\\note_python\\google_spreadsheet\\gspread\\_libs'],
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
          name='gspread_four_star_yfinanceV0.2.40',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon='iphone4-mini-black-13_76020.ico', 
          console=True)