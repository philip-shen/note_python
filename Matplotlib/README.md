Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Matplotlib](#matplotlib)
   * [[Matplotlib] fill_between](#matplotlib-fill_between)
      * [matplotlib.axes.Axes.axvspan()](#matplotlibaxesaxesaxvspan)
      * [matplotlib.axes.Axes.axhspan()](#matplotlibaxesaxesaxhspan)
      * [matplotlib.axes.Axes.fill_between()](#matplotlibaxesaxesfill_between)
   * [[Matplotlib] FancyBboxPatchクラス](#matplotlib-fancybboxpatchクラス)
   * [[Matplotlib] ヒストグラムの作成](#matplotlib-ヒストグラムの作成)
      * [binの幅を調整する](#binの幅を調整する)
      * [データを正規化して相対度数を表示する](#データを正規化して相対度数を表示する)
   * [Polar_極座標](#polar_極座標)
      * [角度の範囲指定](#角度の範囲指定)
      * [r方向の範囲指定](#r方向の範囲指定)
      * [アルキメデスの渦巻線](#アルキメデスの渦巻線)
   * [spectrogram](#spectrogram)
      * [スペクトログラムを観察する](#スペクトログラムを観察する)
      * [短時間フーリエ変換(STFT)](#短時間フーリエ変換stft)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of Matplotlib

# Matplotlib  
[pythonで最も美しいおっぱいを描いた人が優勝 updated at 2020-07-11](https://qiita.com/samuragouchi-monzaemon/items/aa0f42301733c8bd68aa)  

```
import numpy as np
import matplotlib.pyplot as plt

def oppai(y):
    x_1 = (1.5*np.exp(-0.62*(y-0.16)**2))/(1+np.exp(-20*(5*y-1)))
    x_2 = (1.5+0.8*(y-0.2)**3)*(1+np.exp(20*(5*y-1)))**-1
    x_3 = (1+np.exp(-(100*(y+1)-16)))
    x_4 = (0.2*(np.exp(-(y+1)**2)+1))/(1+np.exp(100*(y+1)-16))
    x_5 = (0.1/np.exp(2*(10*y-1.2)**4))
    x = x_1+(x_2/x_3)+x_4+x_5
    return x

def plot_oppai(x, y):
    plt.title('oppai')
    plt.axes().set_aspect('equal', 'datalim')
    plt.grid()
    plt.plot(x, y, 'black')
    plt.show()

def main():
    y = np.arange(-3, 3 + 0.01, 0.01)
    x = oppai(y)
    plot_oppai(x, y)

if __name__ == '__main__':
    main()
```

```
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def oppai(y):
    x_1 = (1.5*np.exp(-0.62*(y-0.16)**2))/(1+np.exp(-20*(5*y-1)))
    x_2 = (1.5+0.8*(y-0.2)**3)*(1+np.exp(20*(5*y-1)))**-1
    x_3 = (1+np.exp(-(100*(y+1)-16)))
    x_4 = (0.2*(np.exp(-(y+1)**2)+1))/(1+np.exp(100*(y+1)-16))
    x_5 = (0.1/np.exp(2*(10*y-1.2)**4))
    x = x_1+(x_2/x_3)+x_4+x_5
    return x

def plot_oppai(x, y):
    plt.title('oppai')
    plt.axes().set_aspect('equal', 'datalim')
    plt.grid()
    plt.plot(x, y, '#F5D1B7')
    plt.fill_between(x, y, facecolor='#F5D1B7', alpha=0.8)#肌色
    w=patches.Wedge(center=(1.55,0.1),r=0.2,theta1=120,theta2=240,color='#E29577')#乳輪
    ax = plt.axes()
    ax.add_patch(w)
    plt.axvspan(1.52, 1.59, 0.51, 0.53, color = '#C87B6D')#乳首当て
    plt.axvspan(0, 0.18, 0.05, 0.5, color = '#F5D1B7')#下乳補正

    plt.show()

def main():
    y = np.arange(-3, 3 + 0.01, 0.01)
    x = oppai(y)
    plot_oppai(x, y)

if __name__ == '__main__':
    main()
```

# [Matplotlib] fill_between  
[指定範囲を塗り潰す関数](https://python.atelierkobato.com/fill_between/)  
## matplotlib.axes.Axes.axvspan()  
```
　Axes.axvspan(xmin, xmax) を使うと、x = xmin から x = xmax までの範囲を塗り潰すことができます。
```

```
# PYTHON_MATPLOTLIB_FILL_01-2

# FigureとAxesを作成
fig = plt.figure(figsize = (6, 6))
ax = fig.add_subplot(111)

# 軸範囲を設定
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# 0≦x≦6,2≦y≦6の範囲を塗り潰す
ax.axvspan(3, 6, 0.2, 0.6, color = "coral")

plt.show()
```
![alt tag](https://python.atelierkobato.com/wp-content/uploads/2019/02/axvspan_02.png)  


## matplotlib.axes.Axes.axhspan()
```
　Axes.axhspan(ymin, ymax) は y = ymin から y = ymax までの範囲を塗り潰します。
```

```
# PYTHON_MATPLOTLIB_FILL_02-2

# FigureとAxesを作成
fig = plt.figure(figsize = (6, 6))
ax = fig.add_subplot(111)

# 軸範囲を設定
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# 2≦x≦8,4≦y≦8の範囲を塗り潰す
ax.axhspan(4, 8, 0.2, 0.8, color = "olive", alpha = 0.5)

plt.show()
```
![alt tag](https://python.atelierkobato.com/wp-content/uploads/2019/02/axhspan_02.png)  

## matplotlib.axes.Axes.fill_between()  
```
　Axes.fill_between(x, y1, y2) は (x, y1) と (x, y2) の間を塗り潰します。
この関数は 2 つの曲線 y=f(x) と y=g(x) に囲まれた領域を図示する場合などに用いられます。
以下に例として、sinx と cosx に囲まれた領域を図示するコードを掲載します。
```

```
# PYTHON_MATPLOTLIB_FILL_03

import numpy as np
import matplotlib.pyplot as plt

# 円周率を定義
pi = np.pi

# プロットするデータを用意
x = np.arange(0, 3*pi, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)

# FigureとAxesの設定
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlabel("x", fontsize = 14)
ax.set_ylabel("y", fontsize = 14)
ax.set_xlim(0.0, 2 * pi)
ax.set_ylim(-1.5, 1.5)
ax.set_xticks([0, pi/2, pi, 3*pi/2, 2*pi])
ax.set_xticklabels(["0", "$\pi/2$", "$\pi$", "$3\pi/2$", "$2\pi$"],
                   fontsize = 12)

# Axesにグラフをプロット
ax.plot(x, y1, color = "blue")
ax.plot(x, y2, color = "red")

# y1とy1の間をライム色で塗り潰す
ax.fill_between(x, y1, y2, facecolor='lime', alpha=0.5)

plt.show()
```
![alt tag](https://python.atelierkobato.com/wp-content/uploads/2019/02/fill_between.png)  


# [Matplotlib] FancyBboxPatchクラス  
[FancyBboxPatchクラス](https://python.atelierkobato.com/fancy/)  
```
# MATPLOTLIB_FANCY_BBOX_PATCH_01

# Matplotlibをインポート
import matplotlib.pyplot as plt

# Figureを設定
fig = plt.figure(figsize =(8, 6))

# Axesを追加
ax = fig.add_subplot(111)

# 目盛線を描画
ax.grid()

# bbox辞書リストを作成
box_style = [{"boxstyle" : "circle"},
             {"boxstyle" : "darrow"},
             {"boxstyle" : "larrow"},
             {"boxstyle" : "rarrow"},
             {"boxstyle" : "round"},
             {"boxstyle" : "round4"},
             {"boxstyle" : "roundtooth"},
             {"boxstyle" : "sawtooth"},
             {"boxstyle" : "square"}]

ax.text(0.1, 0.8, "Circle", size = 16, bbox = box_style[0])
ax.text(0.4, 0.8, "Darrow", size = 16, bbox = box_style[1])
ax.text(0.7, 0.8, "Larrow", size = 16, bbox = box_style[2])
ax.text(0.1, 0.5, "Rarrow", size = 16, bbox = box_style[3])
ax.text(0.4, 0.5, "Round", size = 16, bbox = box_style[4])
ax.text(0.7, 0.5, "Round4", size = 16, bbox = box_style[5])
ax.text(0.1, 0.2, "Roundtooth", size = 16, bbox = box_style[6])
ax.text(0.4, 0.2, "Sawtooth", size = 16, bbox = box_style[7])
ax.text(0.7, 0.2, "Square", size = 16, bbox = box_style[8])
```
![alt tag](https://python.atelierkobato.com/wp-content/uploads/2018/12/bbox1.png)  

# [Matplotlib] ヒストグラムの作成
[ヒストグラムの作成](https://python.atelierkobato.com/histgram/)  
```
# PYTHON_MATPLOTLIB_HISTOGRAM_01-1

# 男性の身長ヒストグラム

# NumPyとmatplotlib.pyplotをインポート
import numpy as np
import matplotlib.pyplot as plt

# Figureを作成
fig = plt.figure()

# グリッド線の表示
plt.style.use("ggplot")

# FigureにAxesを１つ追加
ax = fig.add_subplot(111)

# Axesのタイトルの設定
ax.set_title("Male Height Distribution", fontsize = 16)

# 軸ラベルの設定
ax.set_xlabel("Height", fontsize = 16)
ax.set_ylabel("Frequency", fontsize = 16)

# 正規分布にしたがうデータ（男性の平均身長）を作成
mu = 171
sigma = 5.7
x = np.random.normal(mu, sigma, size = 1000)

# Axesにヒストグラムを描画
ax.hist(x, color = "blue")

# グラフを描画
plt.show()
```
![alt tag](https://python.atelierkobato.com/wp-content/uploads/2018/10/6fa8ef0bf6bc003cdf876edfeea640ff.png)  

```
　コード HISTOGRAM_01-1 の解説です。疑似データの作成には、
numpy.random の normal()関数を使用しています。normal() は
第 1 引数と第 2 引数で指定した平均値と標準偏差をもつ正規分布にしたがう乱数を返します。
また、size でデータの個数を指定しています。上のサンプルコードでは最初に
```

```
# 平均値と標準偏差の設定
mu = 171
sigma = 5.7
```

```
と記述して平均値と標準偏差の値を明示しています。
値を直接 normal() の引数に記述すればコードの行数は節約できますが、このように書いておけば、
このデータを書き換えることによって異なる分布が描けることがすぐにわかります。
```

## binの幅を調整する  
```
# PYTHON_MATPLOTLIB_HISTOGRAM_01-2

# Axesにヒストグラムを描画
ax.hist(x, rwidth = 0.9, color = "blue")

# グラフを再表示
```
![alt tag](https://python.atelierkobato.com/wp-content/uploads/2018/10/af16f1e14486c710f3f36079efdc8742.png)  

## データを正規化して相対度数を表示する  
```
デフォルト設定ではヒストグラムの縦軸は階級幅に入るデータ数を表しますが、
このままではデータ数の異なる他のデータと比較することができません。
引数 density に True を渡すとデータが正規化され、ヒストグラムの縦軸は相対度数を表すようになります：
```

```
# PYTHON_MATPLOTLIB_HISTOGRAM_01-3

# Axesにヒストグラムを描画
ax.hist(x, rwidth = 0.9, color = "blue", density = True)

# グラフを再表示
display(fig)
```
![alt tag](https://python.atelierkobato.com/wp-content/uploads/2018/10/a87f6597234474ff5e178c47b5c61492.png)  


# Polar_極座標  
## 角度の範囲指定  
[[Python]Matplotlibによる極座標表示の散布図 Sep 18, 2020](https://qiita.com/supersaiakujin/items/34659d94fe377d2b0ab5)  
```
import numpy as np
import matplotlib.pyplot as plt

N = 100
r = np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)


fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='polar')
ax.scatter(theta, r)
ax.set_title('Polar coordinates',fontsize=18)
ax.set_thetamin(0)
ax.set_thetamax(180)
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F100523%2Ff0651eb2-d73c-41d2-6d69-d09079cda63d.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=2ac466ebabf399e33d307279fb7c0304"  width="500" height="500">

## r方向の範囲指定  
```
import numpy as np
import matplotlib.pyplot as plt

N = 100
r = np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='polar')
ax.scatter(theta, r)
ax.set_title('Polar coordinates',fontsize=18)
ax.set_rmin(0)
ax.set_rmax(0.5)
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F100523%2F12621981-5ed7-6873-6d36-9e185cf9fce3.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=7a61961c68bd07dc0a7f93802b6d899a"  width="500" height="500">

## アルキメデスの渦巻線  
[[Pythonによる科学・技術計算] 極座標グラフ，可視化，matplotlib Jul 20, 2017](https://qiita.com/sci_Haru/items/b604083b431849938e26)  

```
import numpy as np
import matplotlib.pyplot as plt
"""
極方程式
例:アルキメデスの渦巻線
"""

theta = np.arange(0.0, 4*2*np.pi, 0.01) #θの範囲を 0-8π ラジアン(4周分)とする
r = 0.5*theta   ## 極方程式を指定する。
plt.polar(theta,r) # 極座標グラフのプロット

plt.show()
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F192457%2F4f59f5b4-a903-cafa-a665-0433b827d483.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=b041080ac16bb4b17bff2ce3028da98f"  width="500" height="500">


# spectrogram  
[Pythonの音声処理ライブラリ【LibROSA】で音声読み込み⇒スペクトログラム変換・表示⇒位相推定して音声復元 Jul 05, 2020](https://qiita.com/lilacs/items/a331a8933ec135f63ab1) 

[matplotlibのspecgram Nov 21, 2018](https://qiita.com/wataoka/items/3f01caaa85ae58ace4b0)  
```
matplotlib.pyplot.specgram(x, NFFT=256, Fs=2, Fc=0, detrend=malab.detrend_none, 
window=mlab.window_hanning, noverlap=128, cmap=None, 
xextent=None, pad_to=None, sides='default', sides='default', 
scale_by_freq=None, mode='default', scale='default', **kwargs)
```

パラメータ名 | データ | 説明
------------------------------------ | --------------------------------------------- | ---------------------------------------------
x | 1次元配列またはシーケンス | データを含む配列またはシーケンス
Fs | スカラー | サンプル周波数(単位時間あたりのサンプル数)。フーリエ周波数freqを単位時間ごとのサイクルで計算するために使用される。デフォルト値は2
window | 長さNFFTの関数またはベクトル | 窓関数。参照窓関数を作成するには、numpy.blackman(), numpy.hamming(), numpy.bartlett(), scipy.signal(), scipy.signal.get_sindow()などを使用。デフォルトはwindow_hamming()。
sides | {'default', 'onesided', 'twosided'} | スペクトルのどちら側を返すかを指定。デフォルトは実際のデータに対しては片面、複雑なデータに対しては両面返す。'onesided'では片側のスペクトル、'twosided'では両側のスペクトル
pad_to | int | FFTを実行するときにデータセグメントが埋められるポイントの数。デフォルトはNone。
NFFT | int | FFTの各ブロックで使用されるデータポイントの数。デフォルト値は256。
detrend | {'default', 'constant', 'mean', 'linear', 'none'} | fft-ingの前に各セグメントに適用され、平均または線形傾向を除去するように設計された関数。
scale_by_freq | bool | 結果の密度値をスケーリング頻度でスケーリングするかどうかを指定する。
mode | {'default', 'psd', 'magnitude', 'angle', 'phase'} | 使用するスペクトルの種類。デフォルトは'psd'でパワースペクトル密度。'magnitude'はマグニチュードスペクトル。'angle'はアンラッピングなしの位相スペクトル。'phase'はアンラッピングを伴う位相スペクトルを返す。
noverlap | int | ブロック間の重複ポイントの数。デフォルト値は128。
scale | {'default', 'linear', 'dB'} | スケーリングスペック。'linear'はスケーリングされない。'dB'はdBスケールで値を返す。
Fc | int | xの中心周波数。デフォルトは0。
cmap | matplotlib.colors.Colomapインスタンス | Noneの場合、rcによって決定されるデフォルトを使用する。
xextent | Noneまたは(xmin, xmax) | x軸に沿った画像範囲。
**kwargs |  | スペクトログラムを

[cmap参数](https://matplotlib.org/examples/color/colormaps_reference.html)  
```
cmaps = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]
```


戻り値名 | データ | 説明
------------------------------------ | --------------------------------------------- | ---------------------------------------------
spectrum | 2次元の配列 | 列は連続するセグメントのピリオドグラム。
freqs | 一次元配列 | スペクトルの行に対応する周波数。
t | 一次元配列 | セグメントの中点に対応する時間。
im | AxesImageクラスのインスタンス | スペクトログラムを含むimshowによって作成された画像。

[Pythonで音声ファイル（モノラル・ステレオ両対応）のスペクトログラム描画 Nov 29, 2020]()  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F156600%2Fb0e86085-d429-b8d7-bb22-6b591a4434a9.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=c530b1ce08bed8d91b8916e7a0f77da3"  width="600" height="900">

[Pythonで長い会議を見える化〜スペクトログラム描画の応用〜 Dec 01, 2020](https://qiita.com/toast-uz/items/2f9fc5a436bd1d9e97a5)  

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F156600%2F9131b3e7-a422-ab3f-9450-6908cc1b2929.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=92a1083d045f5533d1cc8eded91c4c9e"  width="600" height="900">

[numpyでスペクトログラムによる音楽信号の可視化 Dec 08, 2016](https://qiita.com/namaozi/items/dec1575cd455c746f597)  
## スペクトログラムを観察する 
[スペクトログラムを観察する](https://qiita.com/namaozi/items/dec1575cd455c746f597#%E3%82%B9%E3%83%9A%E3%82%AF%E3%83%88%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0%E3%82%92%E8%A6%B3%E5%AF%9F%E3%81%99%E3%82%8B)
```
sox ./audios/harmony1.wav -n trim 0 8 rate 44.1k spectrogram
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F103754%2F529dca72-fce4-d1f7-62a3-a7ee46f5f4f5.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=824aa05cf8c7d0bc1e56c06f1178a21f"  width="400" height="600">

## 短時間フーリエ変換(STFT)  
```
さて、数理的な話をします(飛ばしてもいいです)。観測した信号にどの周波数がどれくらい含まれているのかを調べるには、フーリエ変換が必要になります。しかしこのフーリエ変換は周期信号を仮定しているので、時々刻々と変化する音楽などの信号には不適です。そうした場合に用いるのが短時間フーリエ変換(STFT)です。

短時間フーリエ変換では信号に対して窓関数を徐々にずらしながらかけてフレームに分けていき、各フレームごとに周波数成分を求めるという方法です。

ちなみに高速フーリエ変換(FFT)は計算するアルゴリズムの名前です。

あと離散フーリエ変換(DFT)というのがあって、短時間フーリエ変換の違いはかなり説明が難しいのですが、とりあえず短時間フーリエ変換はスペクトログラムのような解析に使えると考えればいいと思います(筆者もあまりよく分かっていない…)。

短時間フーリエ変換は以下の画像が一番分かりやすいと思うので、こちらから引用しました。
```

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2F1cyjknyddcx62agyb002-web-assets.s3.amazonaws.com%2Fimage1.jpg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=4c50df7019366fc004acfc914dc018a7"  width="500" height="800">

```
1. まず、元の信号をFFT sizeのフレームに分けていきます。(画像の一番上)

2. この際に窓関数をかけるのが重要で、これによって切り出した端点をなめらかにして周期性を仮定します。(画像のwindowed slice of soundというやつ)

3. これにFFT計算をすることによって各フレームの周波数成分が得られます。(画像の赤い波)

4. 短時間フーリエ変換のWikiに書いてあるとおり、STFTの絶対値の2乗をすることでスペクトログラム(パワースペクトルの時間変化)を得ます。
```

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F103754%2F87e6f9f4-3c1f-ff7e-93d9-05eb495cf673.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=3e447e779629d0081654db353c95dbf2"  width="200" height="100">


```

5. 次々に窓をずらしてフレームに分けていくことによって、時間ごとの周波数成分を求めていきます。(画像の点線に対応する赤い波)
```

```
#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import scikits.audiolab as al
#⚠ wave読み込みにはscikits.audiolab.wavreadがオススメです。
#私はwaveというパッケージを先に試しましたが,wave.readframesの挙動がおかしかったので使用をやめました。

import functions as fn

"""
スペクトログラムを計算してプロットします
"""
### 楽曲データ読み込み(scikits.audiolab使用)
# data : ここにwavデータがnumpy.ndarrayとして保持されます。
# sampling_rate : 大半のwav音源のサンプリングレートは44.1kHzです
# fmt : フォーマットはだいたいPCMでしょう
file_path = "audios/harmony1.wav"
data, sampling_rate, fmt = al.wavread(file_path)

# ステレオファイルをモノラル化します
x = fn.monauralize(data)

NFFT = 1024 # フレームの大きさ
OVERLAP = NFFT / 2 # 窓をずらした時のフレームの重なり具合. half shiftが一般的らしい
frame_length = data.shape[0] # wavファイルの全フレーム数
time_song = float(frame_length) / sampling_rate  # 波形長さ(秒)
time_unit = 1 / float(sampling_rate) # 1サンプルの長さ(秒)

# 💥 1.
# FFTのフレームの時間を決めていきます
# time_rulerに各フレームの中心時間が入っています
start = (NFFT / 2) * time_unit
stop = time_song
step =  (NFFT - OVERLAP) * time_unit
time_ruler = np.arange(start, stop, step)

# 💥 2.
# 窓関数は周波数解像度が高いハミング窓を用います
window = np.hamming(NFFT)

spec = np.zeros([len(time_ruler), 1 + (NFFT / 2)]) #転置状態で定義初期化
pos = 0

for fft_index in range(len(time_ruler)):
    # 💥 1.フレームの切り出します
    frame = x[pos:pos+NFFT]
    # フレームが信号から切り出せない時はアウトです
    if len(frame) == NFFT:
        # 💥 2.窓関数をかけます
        windowed = window * frame
        # 💥 3.FFTして周波数成分を求めます
        # rfftだと非負の周波数のみが得られます
        fft_result = np.fft.rfft(windowed)
        # 💥 4.周波数には虚数成分を含むので絶対値をabsで求めてから2乗します
        # グラフで見やすくするために対数をとります
        fft_data = np.log(np.abs(fft_result) ** 2)
        # fft_data = np.log(np.abs(fft_result))
        # fft_data = np.abs(fft_result) ** 2
        # fft_data = np.abs(fft_result)
        # これで求められました。あとはspecに格納するだけです
        for i in range(len(spec[fft_index])):
            spec[fft_index][-i-1] = fft_data[i]

        # 💥 4. 窓をずらして次のフレームへ
        pos += (NFFT - OVERLAP)

### プロットします
# matplotlib.imshowではextentを指定して軸を決められます。aspect="auto"で適切なサイズ比になります
plt.imshow(spec.T, extent=[0, time_song, 0, sampling_rate/2], aspect="auto")
plt.xlabel("time[s]")
plt.ylabel("frequency[Hz]")
plt.colorbar()
plt.show()
```

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F103754%2F5bafc925-95f1-70b9-35fe-b27eb69a320b.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=be00aaccedf624fc0a3a00291d952c22"  width="600" height="400">

# Troubleshooting


# Reference


* []()  
![alt tag]()  

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


<img src=""  width="400" height="500">
