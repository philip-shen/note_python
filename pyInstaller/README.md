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
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

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





