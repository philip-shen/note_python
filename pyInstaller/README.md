Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [pyinstaller matplotlib](#pyinstaller-matplotlib)
      * [Matplotlib](#matplotlib)
      * [過剰にパッケージを取り込んでしまう場合がある](#過剰にパッケージを取り込んでしまう場合がある)
      * [Multiprocessing対応](#multiprocessing対応)
      * [UPXでexeファイルが少し圧縮できる](#upxでexeファイルが少し圧縮できる)
   * [Anaconda環境](#anaconda環境)
   * [python code 打包 - pyinstaller](#python-code-打包---pyinstaller)
      * [.spec](#spec)
   * [Python 打包成 exe，太大了该怎么解决？](#python-打包成-exe太大了该怎么解决)
      * [1. Python: Excluding Modules Pyinstaller](#1-python-excluding-modules-pyinstaller)
      * [2. Importing Python modules from a select location](#2-importing-python-modules-from-a-select-location)
      * [3. How can I create the minimum size executable with pyinstaller?](#3-how-can-i-create-the-minimum-size-executable-with-pyinstaller)
         * [1) Install a new version of python independently from anaconda.](#1-install-a-new-version-of-python-independently-from-anaconda)
         * [2) Create and activate the environment, from CMD](#2-create-and-activate-the-environment-from-cmd)
         * [3) Install in the environment all the modules needed in the script](#3-install-in-the-environment-all-the-modules-needed-in-the-script)
         * [4) Create/modify the .spec file (when you run pyinstaller it creates a .spec file, you can rename).](#4-createmodify-the-spec-file-when-you-run-pyinstaller-it-creates-a-spec-file-you-can-rename)
         * [5) Finally make the executable with the command](#5-finally-make-the-executable-with-the-command)
      * [4. the Ultimate Packer for eXecutables](#4-the-ultimate-packer-for-executables)
      * [5. python-embedded](#5-python-embedded)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose
Take note of pyInstaller

# pyinstaller matplotlib 
[TkinterとMatplotlibが含まれるpythonプログラムをpyinstallerでexeを生成 Jun 29, 2018](https://qiita.com/john256/items/8865754569c8261e8425)

## Matplotlib
[Python3でGUI(WxPython)実行ファイル(pyInstaller)[Windows] Jun 02, 2017](https://qiita.com/mm_sys/items/a7690dface9727704143) 
```
MatplotlibをPyInstallerに登録してもそのままではQtのリンク関係で動作しないことが多いです。
対応策としては、import matplotlibの直後に別のバックエンドにすると通るはずです。
```

```
import matplotlib
matplotlib.use('TkAgg')
# 以下略
```
[https://github.com/pyinstaller/pyinstaller/issues/2857](https://github.com/pyinstaller/pyinstaller/issues/2857)
[http://chick.g.hatena.ne.jp/allegro/20091009/p3]()

[Pyinstaller によるPython 3.6スクリプトのexeファイル化  Jan 07, 2018](https://qiita.com/jun365/items/4020ee85056f3a21c11b) 

## 過剰にパッケージを取り込んでしまう場合がある
```
上の記事にあるように、matplotlib.pyplotを取り込むだけでPyQtなどが取り込まれて大きなサイズになります。
dist配下が140MBほどになりました。--onefileを指定すると１ファイルにまとまり、60MBほどでした。
自分はconda createで環境を分けてます（virtualenvのようなもの）が、matplotlibがPyQt等に依存しているようなので切り離すのは難しそうです。
```

## Multiprocessing対応  
問題  
```
Error: no such option: --multiprocessing-fork
```

対処方法
```
    UPX化 のDisable
    Myprog.py に multiprocessing.freeze_support() を追加（下記まとめ myprog.py 参照）。

※ 参考サイトでは onefileの場合は上記対処だけでは無理と記述があったが、手元ではできた。
```

[PyInstaller-built Windows EXE fails with multiprocessing Jul 24 '14](https://stackoverflow.com/questions/24944558/pyinstaller-built-windows-exe-fails-with-multiprocessing)



[Pyinstaller で Python スクリプトを Windows で実行可能な .exe にする 2015-07-21](https://qiita.com/kounoike/items/128f3294362a229005d7#exe-%E3%81%AE%E4%BD%9C%E6%88%90)  

## UPXでexeファイルが少し圧縮できる
[Pythonのexe化、Pyinstaller使用メモ May 04, 2016](https://qiita.com/ymdymd/items/f9f5587f0f3128285e25) 

[Python matplotlibでグラフを作る-5（Pythonプログラムをスタンドアロンの実行可能ファイルにする） Jul 29, 2018](https://qiita.com/ty21ky/items/baec82726c492ca4fd5f)  

[Ubuntuでショートカットを作成する（初心者向け） 2018-03-19](https://qiita.com/ty21ky/items/c2357b6cf24fda49280e)  

# Anaconda環境
[Anaconda環境で作成したPythonプログラムをexe化した話。 Oct 01, 2018](https://qiita.com/shikasama/items/d0418fa4a604cfc00337)  

[python3のpyinstallerを使用したexe化について 2018/09/26](https://teratail.com/questions/148542)  
```
c:\users\user\anaconda3\lib\site-packages\PyInstaller\compat.py の370行目

out = out.decode(encoding)
↓ 変更
out = out.decode(encoding, errors='ignore')

```



[超軽量、超高速な配布用Python「embeddable python」2020-11-21](https://qiita.com/mm_sys/items/1fd3a50a930dac3db299) 


```
#! env python
# -*- coding: utf-8 -*-

from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

import wx

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)


if __name__ == "__main__":
    app = wx.PySimpleApp()
    fr = wx.Frame(None, title='test')
    panel = CanvasPanel(fr)
    panel.draw()
    fr.Show()
    app.MainLoop()
```
[python - Embedding a matplotlib figure inside a WxPython panel - Stack Overflow](https://stackoverflow.com/questions/10737459/embedding-a-matplotlib-figure-inside-a-wxpython-panel) 


# python code 打包 - pyinstaller  
[將你的python code 打包 - pyinstaller Sep 26, 2019](https://peaceful0907.medium.com/%E5%B0%87%E4%BD%A0%E7%9A%84python-code-%E6%89%93%E5%8C%85-pyinstaller-6777d0e06f58)  

## .spec  
```
pyinstaller -D XXX.spec
```

<img src="https://miro.medium.com/max/875/1*uj8kicInRq-UNZtiIRZSSg.png"  width="500" height="500">

```
當你程式不是那麼簡單時，打包時很可能遇到很多error，
尤其像是”no module names XXX”這種，這時候就需要一直google。

我目前的經驗，spec 裡 [‘cython’, ‘sklearn’, ‘sklearn.ensemble’, 
‘sklearn.neighbors.typedefs’, ‘sklearn.neighbors.quad_tree’, ‘sklearn.tree._utils’,
’sklearn.utils._cython_blas’] 這些都給他設定在hiddenimport 裡應該可以擋掉大部分。

datas的寫法為(路徑，名稱)，
如: [(‘mtcnn-model\\*’, ‘mtcnn-model’), (‘img_for_registed\\*’, ‘img_for_registed’)]，這樣他就會把這些folder給打包進dist。

如果你是使用 -D 的模式，你也可以不寫在datas裡，當他包好後在自己手動拉到dist 資料夾內也行。
另外有些module像是mxnet好像也無法直接自動幫你包進去，
所以你需要自己到你python 的site-package裡找mxnet的資料夾，把它整個複製到dist裡就可以了~
```


# Python 打包成 exe，太大了该怎么解决？  
[Python 打包成 exe，太大了该怎么解决？ 2020-07-21](https://www.zhihu.com/question/281858271)  

*先说结论:在virtualenv下用upx压缩打包出来的exe最小*

*还不满意就上python-embed env 最下面有教程链接*

## 1. Python: Excluding Modules Pyinstaller 
[Python: Excluding Modules Pyinstaller Feb 3 '11](https://stackoverflow.com/questions/4890159/python-excluding-modules-pyinstaller/17595149#17595149)

<img src="https://pic4.zhimg.com/80/v2-013f0d8112528151bf98443f5392f023_720w.jpg?source=1940ef5c"  width="500" height="300">

```
然后就可以愉快的在第13行的"[]"里面输入自己不需要的库啦
```

## 2. Importing Python modules from a select location  
[Importing Python modules from a select location  Dec 2 '17](https://stackoverflow.com/questions/47610050/importing-python-modules-from-a-select-location)  

[package multiple exe(s) sharing the same dependencies:Multipackage Bundles](https://pyinstaller.readthedocs.io/en/stable/spec-files.html#multipackage-bundles)


## 3. How can I create the minimum size executable with pyinstaller?  
[How can I create the minimum size executable with pyinstaller? Feb 5 '18](https://stackoverflow.com/questions/48629486/how-can-i-create-the-minimum-size-executable-with-pyinstaller?noredirect=1)

### 1) Install a new version of python independently from anaconda.  

### 2) Create and activate the environment, from CMD  

### 3) Install in the environment all the modules needed in the script  

### 4) Create/modify the .spec file (when you run pyinstaller it creates a .spec file, you can rename).  
```
Initially I got a lot of ImportError: DLL load failed (especially for scipy) and missing module error which I solved thanks to these posts:
```

[What is the recommended way to persist (pickle) custom sklearn pipelines? Oct 31 '17](https://stackoverflow.com/questions/47040099/what-is-the-recommended-way-to-persist-pickle-custom-sklearn-pipelines?answertab=active#tab-top)  
[Pyinstaller with scipy.signal ImportError: DLL load failed edited Feb 24 '20](https://stackoverflow.com/questions/47065295/pyinstaller-with-scipy-signal-importerror-dll-load-failed?answertab=active#tab-top)  

```
# -*- mode: python -*-
options = [ ('v', None, 'OPTION')]
block_cipher = None


a = Analysis(['test1.py'],
             pathex=['D:\\py36envtest', 'D:\\py36envtest\\venv_py36\\Lib\\site-packages\\scipy\\extra-dll' ],
             binaries=[],
             datas=[],
             hiddenimports=['scipy._lib.messagestream',
                            'pandas._libs.tslibs.timedeltas'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='test1',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
```

### 5) Finally make the executable with the command  
```
(venv_py36) D:\py36envtest>pyinstaller -F --clean inputtest1.spec
```

## 4. the Ultimate Packer for eXecutables   
[the Ultimate Packer for eXecutables](https://upx.github.io/)

<img src="https://pic3.zhimg.com/80/v2-c105b04a0bbb288d98ca825f8a7faeab_720w.jpg?source=1940ef5c"  width="500" height="400">  

## 5. python-embedded  
<img src="https://pic2.zhimg.com/80/v2-a78211b5f37e9a21cc5b6e0d837475ea_720w.jpg?source=1940ef5c"  width="700" height="400">

[pyinstaller打包的exe太大？你需要嵌入式python玄学 前提篇](https://zhuanlan.zhihu.com/p/76974787)  

[pyinstaller打包的exe太大？你需要嵌入式python玄学 惊喜篇 2020-04-20](https://zhuanlan.zhihu.com/p/77028265)  

[pyinstaller打包的exe太大？你需要嵌入式python玄学 拓展篇 ](https://zhuanlan.zhihu.com/p/77317765) 
[pip with embedded python Mar 8 '17](https://stackoverflow.com/questions/42666121/pip-with-embedded-python)

[pyinstaller打包的exe太大？你需要嵌入式python玄学 探索篇 03-30](https://zhuanlan.zhihu.com/p/77338198)

[pyinstaller打包的exe太大？你需要嵌入式python玄学 充实篇 2019-09-20](https://zhuanlan.zhihu.com/p/83302212)
[Creating independent process! Mar 3 '11](https://stackoverflow.com/questions/5177140/creating-independent-process)

# Troubleshooting



# Reference


* []()  
![alt tag]()  
<img src=""  width="300" height="400">

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3

