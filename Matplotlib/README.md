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


