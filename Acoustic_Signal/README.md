Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Pythonで音圧のデシベル(dB)変換式と逆変換式!](#pythonで音圧のデシベルdb変換式と逆変換式)
      * [dBを使う理由](#dbを使う理由)
      * [dB変換式](#db変換式)
      * [dB逆変換式](#db逆変換式)
      * [Pythonで実装しよう！](#pythonで実装しよう)
   * [Pythonでwav波形を切り出す!NumPyの配列処理](#pythonでwav波形を切り出すnumpyの配列処理)
      * [使用する波形](#使用する波形)
      * [波形の情報取得](#波形の情報取得)
      * [波形情報の図解](#波形情報の図解)
      * [配列から要素を抽出するコード](#配列から要素を抽出するコード)
   * [Pythonでヒルベルト変換!時間波形の包絡線を求める方法](#pythonでヒルベルト変換時間波形の包絡線を求める方法)
   * [Pythonで学ぶ信号処理!振幅変調のサイドバンドを観察してみる](#pythonで学ぶ信号処理振幅変調のサイドバンドを観察してみる)
      * [参考の記事は以下にリンクしておきますので、是非ご覧下さい。](#参考の記事は以下にリンクしておきますので是非ご覧下さい)
   * [PythonでFFTやスペクトログラムからバンド計算をする方法](#pythonでfftやスペクトログラムからバンド計算をする方法)
      * [バンド計算とは？](#バンド計算とは)
      * [FFT波形の場合](#fft波形の場合)
      * [スペクトログラムの場合](#スペクトログラムの場合)
   * [Pythonでスペクトログラムからピーク値を任意数抽出する方法](#pythonでスペクトログラムからピーク値を任意数抽出する方法)
      * [ピーク自動検出のメリット](#ピーク自動検出のメリット)
      * [スペクトログラムのピーク検出方針(大きい順に抽出する方法）](#スペクトログラムのピーク検出方針大きい順に抽出する方法)
      * [ピーク検出の関数](#ピーク検出の関数)
      * [全コード（コピペ用：単一ピークを検出）](#全コードコピペ用単一ピークを検出)
      * [複数ピークを検出する方法](#複数ピークを検出する方法)
      * [録音データからピーク検出するコード](#録音データからピーク検出するコード)
   * [Acoustic Process by Python](#acoustic-process-by-python)
      * [使用言語・モジュール](#使用言語モジュール)
      * [音を式で表現せねば…](#音を式で表現せねば)
      * [プログラムで表現した音を.wavに出力しましょ。そうしましょ。](#プログラムで表現した音をwavに出力しましょそうしましょ)
         * [1.バイナリ化](#1バイナリ化)
         * [2.waveモジュールで.wavファイルを出力](#2waveモジュールでwavファイルを出力)
      * [めんどいからプログラム上で音鳴らしたいよな！](#めんどいからプログラム上で音鳴らしたいよな)
      * [波形の表示](#波形の表示)
   * [pythonで音声処理](#pythonで音声処理)
      * [pydubを使う](#pydubを使う)
         * [音声を読み込む](#音声を読み込む)
         * [１部分を切り出す](#１部分を切り出す)
         * [音を結合する](#音を結合する)
         * [効果音をつける（音声を重ねる）](#効果音をつける音声を重ねる)
         * [音量を変える](#音量を変える)
         * [RMSレベル](#rmsレベル)
      * [wav音频文件：音频信息，读取内容，获取时长，切割音频，波形图，pcm与wav互转](#wav音频文件音频信息读取内容获取时长切割音频波形图pcm与wav互转)
   * [LibROSA](#librosa)
      * [Wavの読み込み](#wavの読み込み)
      * [Fourier transform](#fourier-transform)
      * [LibROSAで音声読み込み⇒スペクトログラム変換・表示⇒位相推定して音声復元](#librosaで音声読み込みスペクトログラム変換表示位相推定して音声復元)
   * [Beginner's Guide to Audio Data](#beginners-guide-to-audio-data)
      * [1. データの分析](#1-データの分析)
      * [2. Raw波形を使ったモデルの構築](#2-raw波形を使ったモデルの構築)
         * [Raw波形を使ったKerasモデル](#raw波形を使ったkerasモデル)
      * [3.3. MFCCの紹介](#33-mfccの紹介)
         * [Librosaを使ったMFCCの生成](#librosaを使ったmfccの生成)
   * [Pythonで音響信号処理](#pythonで音響信号処理)
      * [周波数応答を表示したい](#周波数応答を表示したい)
   * [Pythonで音響信号処理(2)](#pythonで音響信号処理2)
      * [サンプリングレートを変換したい](#サンプリングレートを変換したい)
      * [waveモジュールで24bitの音声ファイルを読みたい](#waveモジュールで24bitの音声ファイルを読みたい)
      * [TSP信号を生成したい](#tsp信号を生成したい)
   * [サンプリング周波数変換(SamplingRateConversion)](#サンプリング周波数変換samplingrateconversion)
      * [Upsampling](#upsampling)
      * [Downsampling](#downsampling)
      * [Wavファイルの読み込み処理](#wavファイルの読み込み処理)
      * [Upsampling処理](#upsampling処理)
      * [Downsampling処理](#downsampling処理)
      * [Wavファイルの書き出し処理](#wavファイルの書き出し処理)
      * [Mainスクリプト](#mainスクリプト)
      * [wave.Error: unknown format:3](#waveerror-unknown-format3)
         * [SoXのインストール](#soxのインストール)
         * [実際に使うには](#実際に使うには)
   * [From Stereo to Mono](#from-stereo-to-mono)
   * [Build an Audio Spectrum Analyzer](#build-an-audio-spectrum-analyzer)
      * [Reading Audio Files](#reading-audio-files)
      * [Fourier Transform (FT)](#fourier-transform-ft)
      * [Fast Fourier Transform (FFT)](#fast-fourier-transform-fft)
      * [Spectrogram](#spectrogram)
      * [Speech Recognition using Spectrogram Features](#speech-recognition-using-spectrogram-features)
      * [Conclusion](#conclusion)
   * [Sound by Python](#sound-by-python)
      * [Comparison of Audio Libraries](#comparison-of-audio-libraries)
      * [Play](#play)
      * [Record](#record)
      * [Devices](#devices)
   * [RaspberryPi   Python3でPyaudio](#raspberrypi--python3でpyaudio)
      * [マイクとスピーカーの接続と録音の確認](#マイクとスピーカーの接続と録音の確認)
   * [Return value of scipy.io.wavfile.read](#return-value-of-scipyiowavfileread)
      * [What do the bytes in a .wav file represent?](#what-do-the-bytes-in-a-wav-file-represent)
   * [speech_process_exercise](#speech_process_exercise)
      * [ディジタル信号処理の基礎](#ディジタル信号処理の基礎)
   * [音楽のデジタル信号での各ビットの役割。](#音楽のデジタル信号での各ビットの役割)
   * [DSP (digital signal processing ) functionality](#dsp-digital-signal-processing--functionality)
      * [Loading a wave file and saving a normalized version of the sound](#loading-a-wave-file-and-saving-a-normalized-version-of-the-sound)
   * [Polar Response](#polar-response)
   * [Kaldi](#kaldi)
      * [Kaldiインストール](#kaldiインストール)
      * [Simple Guide To “KALDI”](#simple-guide-to-kaldi)
   * [Progress Bar](#progress-bar)
      * [light-progress](#light-progress)
      * [Download Large Files with Tqdm Progress Bar](#download-large-files-with-tqdm-progress-bar)
   * [【Scipy】 FFT, STFT and wavelet](#scipy-fft-stft-and-wavelet)
      * [STFT変換の例題](#stft変換の例題)
      * [FFT変換の例](#fft変換の例)
      * [FFT変換・逆変換](#fft変換逆変換)
      * [STFT変換・逆変換](#stft変換逆変換)
      * [wavelet変換・逆変換](#wavelet変換逆変換)
   * [ディープラーニング (Deep learning)声質変換環境構築](#ディープラーニング-deep-learning声質変換環境構築)
   * [音声を並列で再生する方法](#音声を並列で再生する方法)
   * [combine-multiple-channels-of-audio-files](#combine-multiple-channels-of-audio-files)
      * [Usage](#usage)
      * [Example](#example)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of Acoustic Process by Python  

# Pythonで音圧のデシベル(dB)変換式と逆変換式!  
[Pythonで音圧のデシベル(dB)変換式と逆変換式! 2019.04.25](https://watlab-blog.com/2019/04/25/db/)  

## dBを使う理由  
```
音を分析するために精密騒音計で音圧を測定すると、騒音計の表示はデシベル(dB)で表現されています。

マイクで計測しているのは「音圧」で単位はパスカル[Pa]です。そのままPaで計測値を表示しないのは理由があります。

人間は耳で音を聞き、その音の大きさをレベルとして感じることができます。
人間が聞くことのできる最小可聴値は20[μPa]、最大可聴値は200[Pa]とされており、その範囲には1000万倍もの開きがあります。

騒音計では音圧[Pa]を測定していますが、これをそのままディスプレイに表示してしまうと、必要な桁数が多すぎてしまいますね。

dBを使うとこの20[μPa]～200[Pa]は0[dB]～140[dB]で扱えることになり表示に関しては非常に効率が良くなります。

そしてdBは人間の感覚と近いというのも、広く使われている理由にあります。

人は0.1[Pa]から1[Pa]の音圧の変化と、1[Pa]から10[Pa]への変化は同じように音量が増加したと感じることがわかっています。
つまり人の耳は物理量を差としてではなく倍率で評価しているということになります。

dBで表示すると0.1[Pa]から1[Pa]は20[dB], 1[Pa]から10[Pa]も20[dB]と同じ量になるため、変化量も単純に捉えやすいという利点があります。
```

## dB変換式  
```
dBへの変換は非常に簡単です。以下の式を使います。

SPLdB=20log10(SPLin/dBref)

ここでSPLdB（Sound Pressure Level）がデシベル値で、SPLin（Sound Pressure）が実際の物理値である音圧[Pa]を意味しています。
dBに変換する前の物理値のことを、一般には「リニア値」と読んだりします。

式中のdBrefはデシベル基準値（デシベルリファレンス）のことで、0[dB]の時の物理値のことを意味しており、音圧の場合は最小可聴値と設定されている20[μPa]になります。
```

## dB逆変換式  
```
次に逆変換式を示します。この式はdB値をリニア値に変換する式として使います。

SPLin=dBref⋅10^(SPLdB/20)
```

## Pythonで実装しよう！
```
import numpy as np

#リニア値からdBへ変換
def db(x, dBref):
    y = 20 * np.log10(x / dBref)     #変換式
    return y                         #dB値を返す

#dB値からリニア値へ変換
def idb(x, dBref):
    y = dBref * np.power(10, x / 20) #変換式
    return y                         #リニア値を返す
```

```
import db_function as dbf

x = 1
dBref = 2e-5
y_db = dbf.db(x, dBref)
y_lin = dbf.idb(y_db, dBref)

print(y_db)
print(y_lin)

>>93.97940008672037
>>0.9999999999999999
```

# Pythonでwav波形を切り出す!NumPyの配列処理  
[Pythonでwav波形を切り出す!NumPyの配列処理 2019.04.15](2019.04.15)

## 使用する波形  

## 波形の情報取得  

## 波形情報の図解 
<img src="https://watlab-blog.com/wp-content/uploads/2019/04/sampling_theory.png" width="600" height="300">  

## 配列から要素を抽出するコード  

```
配列から任意の位置のデータを抽出するために、以下の構文を使います。

開始指標とは、配列のどの位置から抽出を開始するかを設定する項目です。この値は秒で指定するのではなく、何番目かを指定します。

終了指標は配列のどの位置まで抽出するかを設定する項目です。開始指標と同様に何番目かを指定します。

ステップは1を設定すると開始指標から終了指標までの全てのデータを抽出します。2であれば一つずつ飛ばしながら抽出と、間引き間隔を指定可能です。
```

```
#配列から任意位置のデータを抽出
配列[開始指標:終了指標:ステップ]
```

```
以下に例として、今回の波形の抽出設定を示します。波形からは「〇秒から〇秒」を切り出したいので、最初にt_startとt_endで設定します。

4, 5行目は指標を算出しています。秒数を時間刻み幅で除すれば、その秒の指標が得られます。
しかし除した結果は小数点を含む型ですので、int()文にて強制的に整数にしています（intはintegerの意味）。
```

```
dt = 1/samplerate              #dt:時間刻み幅
t_start = 1.2                  #開始時間
t_end = 7                      #終了時間
index_start = int(t_start/dt)  #開始時間の指標
index_end = int(t_end/dt)      #終了時間の指標
 
data = data[index_start:index_end:1]  #波形切り出し
```
<img src="https://watlab-blog.com/wp-content/uploads/2019/04/wav-subset.png" width="600" height="300">  


# Pythonでヒルベルト変換!時間波形の包絡線を求める方法  
[Pythonでヒルベルト変換!時間波形の包絡線を求める方法 2019.10.13](https://watlab-blog.com/2019/10/13/hilbert-envelope/)

# Pythonで学ぶ信号処理!振幅変調のサイドバンドを観察してみる  
[Pythonで学ぶ信号処理!振幅変調のサイドバンドを観察してみる 2021.01.10](https://watlab-blog.com/2021/01/10/amplitude-modulation/)

## 参考の記事は以下にリンクしておきますので、是非ご覧下さい。
[PythonでFFT実装!SciPyのフーリエ変換まとめ](https://watlab-blog.com/2019/04/21/python-fft/) 
[Pythonでヒルベルト変換!時間波形の包絡線を求める方法](https://watlab-blog.com/2019/10/13/hilbert-envelope/) 
[PythonでFFT波形から任意個数のピークを自動検出する方法](https://watlab-blog.com/2020/09/26/fft-find-peaks/) 


# PythonでFFTやスペクトログラムからバンド計算をする方法 
[PythonでFFTやスペクトログラムからバンド計算をする方法 2021.01.06](https://watlab-blog.com/2021/01/06/fft-band-calculation/)

## バンド計算とは？
```
バンド計算を説明する前に、まずは上記FFTから得られる情報をみてみましょう。

時間波形に対しFFTをかけると、以下のような周波数波形（ここでは振幅を例にしています）を得ます。この波形を見ると、まず目に入ってくるのは図中に示したピークの情報です。
```

<img src="https://watlab-blog.com/wp-content/uploads/2021/01/fft-band-example.png" width="600" height="300">  

```
ピークの値を定量的に求める場合は
```
[PythonでFFT波形から任意個数のピークを自動検出する方法](https://watlab-blog.com/2020/09/26/fft-find-peaks/)

```
で紹介した方法があります。

しかし、単純にピークの値を知りたいわけではなく、○[Hz]-○[Hz]の範囲の統計量（平均・分散・標準偏差等）を知りたい時もよくあります。
```
<img src="https://watlab-blog.com/wp-content/uploads/2021/01/fft-band-example2-1024x482.png" width="600" height="300">  


```
この周波数領域の任意範囲というのがバンド（Band：帯域）と呼ばれるものです。
統計量の他に音や振動の場合は全バンドのオーバーオール値や部分バンドのパーシャルオーバーオール値といった振幅レベルの指標を求めるというのも、製品開発の中では頻繁に行われています。

この記事ではバンド毎の計算を行う事をバンド計算と呼んでいますが、特に一般用語ではないと思われるので使用の際はご注意下さい。

ちなみに、スペクトログラムに対して任意のバンドを設定して統計量を計算すると、下図のような時間によって統計量が変化する結果を得ます。
```
<img src="https://watlab-blog.com/wp-content/uploads/2021/01/spectrogram-band-example-1024x498.png" width="600" height="300">  

## FFT波形の場合

<img src="https://watlab-blog.com/wp-content/uploads/2021/01/fft-band-result.png" width="600" height="300">  

## スペクトログラムの場合
[PythonでFFT波形から任意個数のピークを自動検出する方法](https://watlab-blog.com/2020/09/26/fft-find-peaks/)

<img src="https://watlab-blog.com/wp-content/uploads/2021/01/spectrogram-band-result-1024x307.png" width="600" height="300">  


# Pythonでスペクトログラムからピーク値を任意数抽出する方法 
[Pythonでスペクトログラムからピーク値を任意数抽出する方法  2020.09.29](https://watlab-blog.com/2020/09/29/findpeaks-spectrogram/)

## ピーク自動検出のメリット 
<img src="https://watlab-blog.com/wp-content/uploads/2020/09/fft-peak-ideal-768x534.png" width="400" height="300">  

## スペクトログラムのピーク検出方針(大きい順に抽出する方法）  
<img src="https://watlab-blog.com/wp-content/uploads/2020/09/2d-findpeaks-orientation-1024x618.png" width="600" height="300">  
  
## ピーク検出の関数  

## 全コード（コピペ用：単一ピークを検出）
[Pythonで音のSTFT計算を自作!スペクトログラム表示する方法](https://watlab-blog.com/2019/05/19/python-spectrogram/)
<img src="https://watlab-blog.com/wp-content/uploads/2020/09/2d-findpeaks-max.png" width="600" height="300">  


## 複数ピークを検出する方法  
<img src="https://watlab-blog.com/wp-content/uploads/2020/09/2d-findpeaks-maxpeaks-1024x466.png" width="600" height="300">  

## 録音データからピーク検出するコード
<img src="https://watlab-blog.com/wp-content/uploads/2021/05/original_spectrogram_peaks.png" width="600" height="500">  


# Acoustic Process by Python  
[pythonで音を鳴らす方法を詳しめに解説 updated at 2020-04-17](https://qiita.com/ShijiMi-Soup/items/3bbf34911f6e43ee14a3)  

## 使用言語・モジュール  

* 言語：Python
* モジュール
  * numpy（sinやπをつかうので）
  * matplotlib（波形を描画したいなら）
  * wave（.wavファイルの入出力に）
  * struct(waveで.wavファイルにする際に波形のデータをバイナリ化するのに使います）
  * pyaudio（音を鳴らすのに使いますが、Python3.7だとインストールがめんどくさいので最悪使わなくても全然大丈夫）

```
import numpy as np
import matplotlib.pyplot as pl
import wave
import struct
import pyaudio
```

## 音を式で表現せねば…  
```
sec = 1 #1秒
note_hz = 440 #ラの音の周波数
sample_hz = 44100 #サンプリング周波数
t = np.arange(0, sample_hz * sec) #1秒分の時間の配列を確保
wv = np.sin(2 * np.pi * note_hz * t/sample_hz)
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F528997%2Ff221a586-d308-84b9-6027-10a59c485114.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=8e44d274fd721649bab0552f665271b0)  

```
tは１秒間の時間を表現していて、上の場合44100個の要素の1次元配列です。

私たちの住む世界の情報は連続値（アナログ）ですが、
残念ながらパソコンでは離散的（デジタル）なデータしか扱えません。

なので、1秒を44100個に分割して表現するのです。
```

```
（ちなみに44100hzというサンプリング周波数は、CDのサンプリング周波数の規格で、
人の可聴域の約二倍の数字にしてあります。なぜ二倍かというのはナイキスト周波数とググりましょう。）
```

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F528997%2Fb18d66b2-6895-7af3-ff4c-ee4604cd0a61.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=3cc2b5a2e8adfeb888ade269bf8db3fb)  


## プログラムで表現した音を.wavに出力しましょ。そうしましょ。  
```

1 作った音を.wavファイルとして出力する。
    1. 音のデータをstructモジュールでバイナリ化する。
    2. バイナリ化されたデータを、waveモジュールで.wavファイルとして出力。
2 作った音をプログラム上で鳴らす。（任意）
    1.  作った.wavファイルをwaveモジュールで開く
    2.  pyaudioモジュールで鳴らす。
3 音の波形をmatplotlib.pyplotモジュールでグラフとして表示する。（任意）

3.に関しては波形が気にならない人はやんなくていいです全然。

2.は、pyaudioというモジュールを使うんですが、Python3.7系だとインストールがめんどくさい
（インストールしたい場合は、このページの最後の参考サイトを参照してください）ので、
1.で作成した.wavファイルをWindows Media Playerなどで鳴らせばいいです。
```

### 1.バイナリ化  
```
max_num = 32767.0 / max(wv) #バイナリ化の下準備の下準備
wv16 = [int(x * max_num) for x in wv] #バイナリ化の下準備
bi_wv = struct.pack("h" * len(wv16), *wv16) #バイナリ化
```

```
32767って何の数字だよ！って思いますよね、わかります。
これは、16bitのデータ(16桁の2進数で表現されたデータ)のとりうる値が、
-32768～32767であることからきています。（2の16乗が65536で、その半分の数が32768だから……うっ頭がっっっ）

w/max(W)がとりうる値は-1～1、それに32767をかけることで* 32767・
(w/max(W)) は *-32767～32767 の値をとり、
音の波形データを16bitの中にまんべんなく（というよりピッタリ？）収まるようにしています。
そうしてできるのがwv16です。ふぅ…。

そしてバイナリ化のコードbi_wv = struct.pack("h" * len(wv16), *wv16)。
正直僕はこれについて全然わかっていません。コピペです。
とりあえず、structバイナリのstruct.packはバイナリ形式への変換を行ってくれるもので、
第一引数の"h"は、2byte（16bit）整数のフォーマットらしい。へぇ。
```

### 2.waveモジュールで.wavファイルを出力  
```
file = wave.open('sin_wave.wav', mode='wb') #sin_wave.wavを書き込みモードで開く。（ファイルが存在しなければ新しく作成する。）
param = (1,2,sample_hz,len(bi_wv),'NONE','not compressed') #パラメータ
file.setparams(param) #パラメータの設定
file.writeframes(bi_wv) #データの書き込み
file.close #ファイルを閉じる
```

```
wave.setparams()で.wavファイルのパラメータを設定します。
パラメータ(param）は左から順に、

    チャンネル数（ ステレオ→2、モノラル→1 ）
    サンプルサイズ〔byte〕（今回は2byte）
    サンプリング周波数　
    フレーム数（今回でいえばt配列の個数と同じ）
    圧縮形式（'NONE'だけがサポートされている。それって存在意義あるんか…？）
    圧縮形式を人に判読可能にしたもの（圧縮形式'NONE'に対して'not compressed'が返される。）  
```

## めんどいからプログラム上で音鳴らしたいよな！  
```
file = wave.open('sin_wave.wav', mode='rb')
```

```
p = pyaudio.PyAudio() #pyaudioのインスタンス化
stream = p.open(
    format = p.get_format_from_width(file.getsampwidth()),
    channels = wr.getnchannels(),
    rate = wr.getframerate(),
    output = True
    ) #音を録音したり再生したりするためのストリームを作る。
file.rewind() #ポインタを先頭に戻す。
chunk = 1024 #よくわかりませんが公式ドキュメントがこうしてました。
data = file.readframes(chunk) #chunk分（1024個分）のフレーム（音の波形のデータ）を読み込む。
while data:
    stream.write(data) #ストリームにデータを書き込むことで音を鳴らす。
    data = file.readframes(chunk) #新しくchunk分のフレームを読み込む。
stream.close() #ストリームを閉じる。
p.terminate() #PyAudioを閉じる。
```

> 1.pyaudioを開く、2.ストリームを開く、3.ストリームにデータを書き込んで音を鳴らす、4.ストリームを閉じる、5.pyaudioを閉じる

## 波形の表示  
```
pl.plot(t,wv)
pl.show()
```

[Python3.7でPyAudioがインストールできない時の解決法  2019.05.21](https://watlab-blog.com/2019/05/21/pyaudio-install/)  

# pythonで音声処理  

## pydubを使う  

### 音声を読み込む    
```
import pydub
from pydub import AudioSegment

base_sound = AudioSegment.from_file(input.mp3, format="mp3")  # 音声を読み込み
length_seconds = base_sound.duration_seconds  # 長さを確認
base_sound.export("./result.mp3", format="mp3")  # 保存する
```

### １部分を切り出す  
```
first_five_second = base_sound[:5*1000]
last_ten_second = base_sound[10*1000:]
```

### 音を結合する    
```
concated_sound = first_five_second + last_ten_second  # 元の音声の最初と最後を結合
```

### 効果音をつける（音声を重ねる）   
```
effect_sound = AudioSegment.from_file(effect.mp3, format="mp3")  # 効果音を読み込み
start_time_ms = 5 * 1000  # 効果音を５秒時点から鳴らす
result_sound = base_sound.overlay(effect_sound, start_time_ms)  # ベースの音声に効果音をつける
```

### 音量を変える    
```
loud_sound = base_sound + 6  # 音量を6dbだけ上げる
quiet_sound = base_sound - 10  # 音量を10db下げる
```

```
from pydub.utils import db_to_float, ratio_to_db
ratio = 0.8  # 0.8倍の音量にしたい
quiet_sound = base_sound + ratio_to_db(ratio)
```

```
base_sound.rms
base_sound.dBFS
base_sound.max    
```

### RMSレベル

[レベル計測の方法：PEAK / RMS / LOUDNESS 2015年12月27日](https://sleepfreaks-dtm.com/dtm-mix-technique/level-metering/)  
![alt tag](https://sleepfreaks-dtm.com/wordpress/wp-content/uploads/2015/12/peak_RMS.png)  

> 簡単に言ってしまえば、平均的な信号レベルの大きさを表す指標ということになります。
> 実効値とも呼ばれ、単位は”dB”です。
> 音圧の大きさの指標として用いられることが多いように思います。

```
まず、ゼロレベル（無音）から振幅の幅のみを、信号レベルの大きさと考えると、
下記のようなイメージになります。
```
![alt tag](https://sleepfreaks-dtm.com/wordpress/wp-content/uploads/2015/12/rms_curve_1-1024x366.jpg)  

```
あまりに瞬間的な音量は人間には聴き取りづらいので、
平均的な信号レベルが実効値=RMSと、いうことになります。
注意点：耳に聞こえにくい周波数帯の信号レベルが大きい場合においても、RMSレベルは大きくなります。
```
![alt tag](https://sleepfreaks-dtm.com/wordpress/wp-content/uploads/2015/12/rms_curve_2-1024x366.jpg)  

```
ってことは、サウンド全体の平均的な音量を調節するにはこれを使えば良さそう！
```

```
delta = ratio_to_db(0.8)  # 音量を0.8倍にしたい
sound_quiet = sound_base + delta  # 音量を調節
result_ratio = sound_quiet.rms / sound_base.rms
print(resul_tratio)  # 0.7998836532867947が返ってきた
```

```
元のサウンドと比べてrms値がほぼ0.8倍になっているので、問題なしとします。

sound.maxの値を使って調整するやり方も考えられましたが、返り値の単位がよくわからないので却下。
```

## wav音频文件：音频信息，读取内容，获取时长，切割音频，波形图，pcm与wav互转  
[python处理wav音频文件：音频信息，读取内容，获取时长，切割音频，波形图，pcm与wav互转 2018-12-22](https://mp.weixin.qq.com/s/Kw_n3RgYfZCn_0ZOJpaxHg)  
[ silencesmile /python_wav ](https://github.com/silencesmile/python_wav)  

```
with wave.open(wav_path, "rb") as f:
    f = wave.open(wav_path)
```

```
返回内容为：

声道，采样宽度，帧速率，帧数，唯一标识，无损    
```
<img src="https://mmbiz.qpic.cn/mmbiz_png/daO6rm02504QicIojcXpztXXMz0ne1wt0m1D1tObmPPgs2apfMwIVMSBqx2lM2vrg6DMXyJqNOPKibezr9yZB8Fg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1"  width="300" height="300">

```
采样点的个数为 2510762，采样的频率为44100HZ，通过这两个参数可以得到声音信号的时长

每个采样点是16 bit = 2 bytes ,那么将采样点的个数 2510762*2/(1024*1024)=4.78889MB，那么这个信息就是文件大小信息。


检验一下声音波形的时间

 child1.wav 4.78MB,时长56s

time = 56.93337868480726

根据上面WAVE PCM soundfile format 的资料信息查询。有一个印象：WAV文件中由以下三个部分组成：


1."RIFF" chunk descriptor    
2.The "fmt" sub-chunk   
3.The "data" sub-chunk 存这些信息的时候都要要有 “ID”、“大小”、“格式”，这些信息标注了数据的位置，

“WAV”格式由“fmt”和“data”，两个部分组成，
其中“fmt”的存储块用来存音频文件的格式，
“data”的存储块用来存实际听到的声音的信息，
物理上描述的振幅和时间：长度(时间)和振幅，当然人的耳朵听听见的是长度和音调。


也就是说可以读取这个数组，在配合频率的信息直接画出波形图。
```
<img src="https://mmbiz.qpic.cn/mmbiz_png/daO6rm02504QicIojcXpztXXMz0ne1wt0OE0Ho30MX5lGR3h6QUlxrHiaSYGOBNxg4D5YmEsmMFrblzGyIQCkm3g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1"  width="600" height="400">


# LibROSA  
[信号処理とか音楽の分析に大活躍しそうなlibrosa ](https://qiita.com/tom_m_m/items/91ba624dd8507bc0b746)  

## Wavの読み込み  
```
import librosa

file_name = '/home/sound_process/data/sound/engine/1-18527-A-44.wav'
wav, sr = librosa.load(file_name, sr=44100)
```

```
注意しないといけないのが、srの値です。
srの値がデフォルトで22,050Hzになっています。
なので、返ってくる値が22,050Hzになってしまいます。
読み込みに直接影響はないですが、周波数計算する時とかグラフの横軸に影響がでます。
```

```
import librosa.display
import matplotlib.pyplot as plt

plt.figure()
plt.figure(figsize=(15, 5))
librosa.display.waveplot(wav, sr)
plt.show()
```

## Fourier transform 
Short-time Fourier transform (短時間フーリエ変換) ができます。
```
import numpy as np

stft_result = librosa.stft(wav)
abs_result = np.abs(stft_result)
power_spec = librosa.amplitude_to_db(abs_result, ref=np.max)

plt.figure(figsize=(25,5))
librosa.display.specshow(power_spec, y_axis='log', x_axis='time', sr = sr)
plt.title('Power Spectrogram')
plt.colorbar(format='%+2.0f dB')

plt.tight_layout()
plt.show()
```

## LibROSAで音声読み込み⇒スペクトログラム変換・表示⇒位相推定して音声復元
[Pythonの音声処理ライブラリ【LibROSA】で音声読み込み⇒スペクトログラム変換・表示⇒位相推定して音声復元 posted at Jul 05, 2020](https://qiita.com/lilacs/items/a331a8933ec135f63ab1)  

今回は以下の音声処理の基本処理をまとめました。
```

    音声の読み込み
    周波数を指定して音声を読み込み
    Notebook上で、音声をプレーヤーで再生
    音声波形のグラフを表示
    スペクトログラムへの変換
    STFTで音声からスペクトログラムへ変換
    強度をdB単位に変換
    スペクトログラムのカラープロットを表示
    音声を復元
    逆STFTでスペクトログラムから音声を復元する場合
    位相情報を推定して音声を復元する場合
```
ソースコード：https://github.com/lilacs2039/ColabNotebooks/blob/master/audio/LibROSA%E4%BD%BF%E3%81%84%E6%96%B9.ipynb

[pythonのlibrosaでサクッと音声波形を表示する posted at Mar 08, 2019](https://qiita.com/amuyikam/items/a5ba64d7bc045feee2d1)


# Beginner's Guide to Audio Data  
[音声データの初心者向けガイド 〜 updated at 2018-05-04](https://qiita.com/daisukelab/items/d084c0a82e3f229043a7)  


## 1. データの分析  

## 2. Raw波形を使ったモデルの構築  
```
ここでは2つのモデルを作ります。

   1.  一つ目はRaw波形(1次元配列)を入力とし、Conv1Dを主な演算処理とするモデル。
   2.  二つ目はMFCC(後述)を入力とするモデル。
```
### Raw波形を使ったKerasモデル  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fraw.githubusercontent.com%2Fzaffnet%2Fimages%2Fmaster%2Fimages%2Fraw_model.jpg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=52d76b7013c61c0ddfe7594732a956a8)  

## 3.3. MFCCの紹介  
### Librosaを使ったMFCCの生成  


[Python分离立体声WAV压缩文件的左右声道 - 机器在学习 Aug 13, 2019](http://www.siyuanblog.com/?p=104790)  
```
import soundfile as sf

musicFileName = "1016(37)_13733163362(4)_In_20190808140419.wav"
sig, sample_rate = sf.read(musicFileName)
print("采样率：%d" % sample_rate)    
print("时长：", sig.shape[0]/sample_rate, '秒')    

serviceData = sig.T[0]
clientData = sig.T[1]
```

```
import matplotlib.pyplot as plt
import numpy as np

plt.figure()
l=sig.shape[0]
x = [i/8000 for i in range(l)]
plt.plot(x, clientData, c='r')
plt.show()
```

```
import matplotlib.pyplot as plt
import numpy as np

plt.figure()
l=sig.shape[0]
x = [i/8000 for i in range(l)]
plt.plot(x, serviceData , c='b')
plt.show()
```


# Pythonで音響信号処理  
[Pythonで音響信号処理 updated at 2015-12-13](https://qiita.com/wrist/items/5759f894303e4364ebfd)  
```

    Pythonで音響信号処理をするモチベーション
    オーディオファイルの読み書き
    リアルタイムにオーディオ処理を行いたい
    周波数応答を表示したい
    デジタルフィルタを設計したい
    零点、極と係数配列b, aを変換したい
    デジタルフィルタを時系列信号に適用したい
    群遅延を計算したい
    時間相関(相互相関関数)を計算したい
    ピークを検出したい

```

## 周波数応答を表示したい  

# Pythonで音響信号処理(2)  
[Pythonで音響信号処理(2) updated at 2016-12-20](https://qiita.com/wrist/items/4b404230e264c5cb571c#%E3%81%9D%E3%81%AE%E4%BB%96)

## サンプリングレートを変換したい  
```
#!/usr/bin/env python
# vim:fileencoding=utf-8

from fractions import Fraction

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import scipy.signal as sg

import soundfile as sf

if __name__ == '__main__':
    plt.close("all")

    fs_target = 44100
    cutoff_hz = 21000.0
    n_lpf = 4096

    sec = 10

    wav, fs_src = sf.read("../wav/souvenir_mono_16bit_48kHz.wav")
    wav_48kHz = wav[:fs_src * sec]

    frac = Fraction(fs_target, fs_src)  # 44100 / 48000

    up = frac.numerator  # 147
    down = frac.denominator  # 160

    # up sampling
    wav_up = np.zeros(np.alen(wav_48kHz) * up)
    wav_up[::up] = up * wav_48kHz
    fs_up = fs_src * up

    cutoff = cutoff_hz / (fs_up / 2.0)
    lpf = sg.firwin(n_lpf, cutoff)

    # filtering and down sampling
    wav_down = sg.lfilter(lpf, [1], wav_up)[n_lpf // 2::down]

    # write wave file
    sf.write("down.wav", wav_down, fs_target)

    # lowpass filter plot
    w, h = sg.freqz(lpf, a=1, worN=1024)
    f = fs_up * w / (2.0 * np.pi)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.semilogx(f, 20.0 * np.log10(np.abs(h)))
    ax.axvline(fs_target, color="r")
    ax.set_ylim([-80.0, 10.0])
    ax.set_xlim([3000.0, fs_target + 5000.0])
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("power [dB]")

    plt.show()
```

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F8799%2F85b75f83-027d-0e87-0863-dd8ca57b8207.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=5855a131ce4dabfc7b59cb45e99dd1ae)  

## waveモジュールで24bitの音声ファイルを読みたい  
[e-onkyoのサンプル音源](http://www.e-onkyo.com/music/album/sample02/)
```
#!/usr/bin/env python
# vim:fileencoding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import wave

from struct import unpack

if __name__ == '__main__':
    plt.close("all")

    fname = "../wav/souvenir.wav"
    fp = wave.open(fname, "r")

    nframe = fp.getnframes()
    nchan = fp.getnchannels()
    nbyte = fp.getsampwidth()
    fs = fp.getframerate()

    print("frame:{0}, "
          "channel:{1}, "
          "bytewidth:{2}, "
          "fs:{3}".format(nframe, nchan, nbyte, fs))

    buf = fp.readframes(nframe * nchan)
    fp.close()

    read_sec = 40
    read_sample = read_sec * nchan * fs
    print("read {0} second (= {1} frame)...".format(read_sec,
                                                    read_sample))

    # 最下位bitに0を詰めてintにunpackすることで
    # 24bitの値を32bit intとして値を取り出す
    #  (<iはリトルエンディアンのint値を仮定)
    # unpackはtupleを返すので[0]を取る
    unpacked_buf = [unpack("<i",
                           bytearray([0]) + buf[nbyte * i:nbyte * (i + 1)])[0]
                    for i in range(read_sample)]

    # ndarray化
    ndarr_buf = np.array(unpacked_buf)

    # -1.0〜1.0に正規化
    float_buf = np.where(ndarr_buf > 0,
                         ndarr_buf / (2.0 ** 31 - 1),
                         ndarr_buf / (2.0 ** 31))

    # interleaveを解く(ステレオ音源の場合)
    wav_l = float_buf[::2]
    wav_r = float_buf[1::2]
    time = np.arange(np.alen(wav_l)) / fs

    # plot
    fig = plt.figure(1)

    ax = fig.add_subplot(2, 1, 1)
    ax.plot(time, wav_l)
    ax.set_xlabel("time [pt]")
    ax.set_ylabel("amplitude")
    ax.set_title("left channel")
    ax.grid()

    ax = fig.add_subplot(2, 1, 2)
    ax.plot(time, wav_r)
    ax.set_xlabel("time [pt]")
    ax.set_ylabel("amplitude")
    ax.set_title("right channel")
    ax.grid()

    plt.show()
```

## TSP信号を生成したい  
[金田先生のインパルス応答測定の基礎の講習資料](http://www.asp.c.dendai.ac.jp/ASP/IRseminor2016.pdf)  
```
#!/usr/bin/env python
# vim:fileencoding=utf-8

import numpy as np
import matplotlib.pyplot as plt

import scipy.fftpack as fft

import soundfile as sf

if __name__ == '__main__':
    plt.close("all")

    # parameters
    N_exp = 16
    m_exp = 2
    nrepeat = 5
    fs = 48000
    gain = 100.0

    N = 2 ** N_exp
    m = N // (2 ** m_exp)  # (J=2m)
    a = ((m * np.pi) * (2.0 / N) ** 2)

    tsp_freqs = np.zeros(N, dtype=np.complex128)
    tsp_freqs[:(N // 2) + 1] = np.exp(-1j * a * (np.arange((N // 2) + 1) ** 2))
    tsp_freqs[(N // 2) + 1:] = np.conj(tsp_freqs[1:(N // 2)][::-1])

    # ifft and real
    tsp = np.real(fft.ifft(tsp_freqs, N))

    # roll
    tsp = gain * np.roll(tsp, (N // 2) - m)

    # repeat
    tsp_repeat = np.r_[np.tile(tsp, nrepeat), np.zeros(N)]

    # write
    sf.write("tsp.wav", tsp_repeat, fs)

    fig = plt.figure(1)
    ax = fig.add_subplot(211)
    ax.plot(tsp)
    ax = fig.add_subplot(212)
    ax.plot(tsp_repeat)

    plt.show()
```

[【Audio入門】音声変換してみる♬ posted at 2019-07-07](https://qiita.com/MuAuan/items/675854ab602595c79612)  
[深層学習による声質変換 updated at 2016-12-23](https://qiita.com/satopirka/items/7a8a503725fc1a8224a5)  
[Pythonで音声信号処理  2011-05-14](http://aidiary.hatenablog.com/entry/20110514/1305377659)



# サンプリング周波数変換(SamplingRateConversion)  
[サンプリング周波数変換(SamplingRateConversion)を実装してみた．updated at 2020-04-02](https://qiita.com/sumita_v09/items/808a3f8506065639cf51)  
[ T-Sumida /SamplingRateConversion](https://github.com/T-Sumida/SamplingRateConversion)  

## Upsampling  
```
アップサンプリングは，基本的には補完処理を行います．
もとのサンプリング周波数 fs1 をサンプリング周波数 fs2 に変換する場合，
信号の各サンプルの間に (fs2/fs1 - 1) 個の新しい値0のサンプルを追加します．

このようにサンプルを増やしていきますが，こうしたとき波形がギザギザになってしまいます．
これは信号に不要な成分（折り返しノイズ）が入ってしまっているためです．
なので，もとのサンプリング周波数のナイキスト周波数 (fs1/2) 以上の周波数成分を除去するようなLPF（Low Pass Filter）処理を施します．
```

## Downsampling  
```
ダウンサンプリングはアップサンプリングとは対象的に，信号のサンプルを間引きます．
もとのサンプリング周波数 fs1 をサンプリング周波数 fs2 に変換する場合，
サンプル1個を取りだした後に (fs2/fs1 - 1) 個のサンプルを捨ててしまいます．

この時，間引いた信号には折り返しが発生する可能性があります（例：44.1kHzを22.05kHzに落とすとき，
元信号に20kHzの信号が入ってるとダウンサンプリングしたとき折り返しが発生する）．
なので，間引き処理を行う前に変換後のサンプリング周波数の半分（ナイキスト周波数）以上の周波数成分を除去するためにLPF処理を施します．
```

## Wavファイルの読み込み処理  
```
def readWav(filename):
    """
    wavファイルを読み込んで，データ・サンプリングレートを返す関数
    """
    wf = wave.open(filename)
    fs = wf.getframerate()
    # -1 ~ 1までに正規化した信号データを読み込む
    data = np.frombuffer(wf.readframes(wf.getnframes()),dtype="int16")/32768.0
    return (data,fs)
```

## Upsampling処理  
```
def upsampling(conversion_rate,data,fs):
    """
    アップサンプリングを行う．
    入力として，変換レートとデータとサンプリング周波数．
    アップサンプリング後のデータとサンプリング周波数を返す．
    """
    # 補間するサンプル数を決める
    interpolationSampleNum = conversion_rate-1

    # FIRフィルタの用意をする
    nyqF = fs/2.0     # 変換後のナイキスト周波数
    cF = (fs/2.0-500.)/nyqF             # カットオフ周波数を設定（変換前のナイキスト周波数より少し下を設定）
    taps = 511                          # フィルタ係数（奇数じゃないとだめ）
    b = scipy.signal.firwin(taps, cF)   # LPFを用意

    # 補間処理
    upData = []
    for d in data:
        upData.append(d)
        # 1サンプルの後に，interpolationSampleNum分だけ0を追加する
        for i in range(interpolationSampleNum):
            upData.append(0.0)

    # フィルタリング
    resultData = scipy.signal.lfilter(b,1,upData)
    return (resultData,fs*conversion_rate)
```

## Downsampling処理  
```
def downsampling(conversion_rate,data,fs):
    """
    ダウンサンプリングを行う．
    入力として，変換レートとデータとサンプリング周波数．
    ダウンサンプリング後のデータとサンプリング周波数を返す．
    """
    # 間引くサンプル数を決める
    decimationSampleNum = conversion_rate-1

    # FIRフィルタの用意をする
    nyqF = fs/2.0             # 変換後のナイキスト周波数
    cF = (fs/conversion_rate/2.0-500.)/nyqF     # カットオフ周波数を設定（変換前のナイキスト周波数より少し下を設定）
    taps = 511                                  # フィルタ係数（奇数じゃないとだめ）
    b = scipy.signal.firwin(taps, cF)           # LPFを用意

    #フィルタリング
    data = scipy.signal.lfilter(b,1,data)

    #間引き処理
    downData = []
    for i in range(0,len(data),decimationSampleNum+1):
        downData.append(data[i])

    return (downData,fs/conversion_rate)
```

## Wavファイルの書き出し処理  
```
def writeWav(filename,data,fs):
    """
    入力されたファイル名でwavファイルを書き出す．
    """
    # データを-32768から32767の整数値に変換
    data = [int(x * 32767.0) for x in data]
    #バイナリ化
    binwave = struct.pack("h" * len(data), *data)
    wf = wave.Wave_write(filename)
    wf.setparams((
        1,                          # channel
        2,                          # byte width
        fs,                         # sampling rate
        len(data),                  # number of frames
        "NONE", "not compressed"    # no compression
        ))
    wf.writeframes(binwave)
    wf.close()
```

## Mainスクリプト  
```
if __name__ == "__main__":
    # 何倍にするかを決めておく
    up_conversion_rate = 4
    # 何分の1にするか決めておく．ここではその逆数を指定しておく（例：1/2なら2と指定）
    down_conversion_rate = 4

    # テストwavファイルを読み込む
    data,fs = readWav("test.wav")

    upData,upFs = upsampling(up_conversion_rate,data,fs)
    downData,downFs = downsampling(down_conversion_rate,data,fs)

    writeWav("up.wav",upData,upFs)
    writeWav("down.wav",downData,downFs)
```

## wave.Error: unknown format:3  
[wave.Error: unknown format:3](https://www.twblogs.net/a/5d232ca8bd9eee1ede068342)  
![alt tag](https://pic1.xuehuaimg.com/proxy/csdn/https://img-blog.csdnimg.cn/20190708154152326.png)  

[Sox在Windows下的安装以及Sox在python中的安装](https://blog.csdn.net/weixin_43216017/article/details/88531363)
在python中安装Sox包  
![alt tag](https://img-blog.csdnimg.cn/20190313141410785.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxNjAxNw==,size_16,color_FFFFFF,t_70)  

[SoXをWindows10で使い始めるまでの手順(メモ) posted at 2019-01-17](https://qiita.com/teteyateiya/items/e4dc27e384d947b9946d)  

### SoXのインストール  
[公式サイト](https://sourceforge.net/projects/sox/)  

### 実際に使うには  
```
まず音声ファイルを保存するフォルダに移動し、次のようにパスを通す。
path %PATH%;C:\Program Files (x86)\sox-14-4-2
これでこのフォルダではsoxと打つだけでSoXが使えるようになる。

次に、出力・入力先デバイスをコマンドラインに教えてあげる必要がある。
今のままsox test.wav -dといったコマンドを打つと次のエラーが出る。
sox FAIL sox: Sorry, there is no default audio device configured
つまり、soxを使いたいけど入出力デバイスが設定されてないから使えないといった意味。

この問題は
set AUDIODRIVER=waveaudio
と打てば解決する。
デフォルトのデバイスを固定する必要があるということ。
この「waveaudio」はsox -hと打つとAUDIO DEVICE DRIVERS: waveaudioというように出てくるので確認してからsetする。
```


# From Stereo to Mono  
[PythonでWAVをステレオからモノラルに変換するにはど](https://stackoverrun.com/ja/q/1243814)  
```
from pydub import AudioSegment
sound = AudioSegment.from_wav("/path/to/file.wav")
sound = sound.set_channels(1)
sound.export("/output/path.wav", format="wav")
```

```
1つの注意点：ffmpegを使用してオーディオ形式の変換を処理しますが、wavのみを使用する場合は、純粋なpythonにすることができます。
```

[Pythonでモノラルとステレオのwavファイルを保存する方法  2019.10.23](https://watlab-blog.com/2019/10/23/wav-mono-stereo/)  
```
import soundfile as sf
from scipy.signal import chirp
import numpy as np
import matplotlib.pyplot as plt
 
# サンプル波形を生成（チャープ信号）
samplerate = 44100                                      # サンプリングレート
ts = 0                                                  # 信号の開始時間
tf = 4                                                  # 信号の終了時間
t = np.linspace(ts, tf, tf * samplerate)                # 時間軸を作成
L = chirp(t, f0=10, f1=5000, t1=10, method='linear')    # 縦軸を作成
 
# モノラルのwavファイルを保存
sf.write('mono.wav', L, samplerate)
 
# ここからグラフ描画
# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'
 
# 目盛を内側にする。
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
 
# グラフの上下左右に目盛線を付ける。
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')
 
# 軸のラベルを設定する。
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('L')
 
# データプロット。
ax1.plot(t, L)
 
# レイアウト設定
fig.tight_layout()
 
# グラフを表示する。
plt.show()
plt.close()
```

```
import soundfile as sf
from scipy.signal import chirp
import numpy as np
import matplotlib.pyplot as plt
 
# サンプル波形を生成（チャープ信号）
samplerate = 44100                                      # サンプリングレート
ts = 0                                                  # 信号の開始時間
tf = 4                                                  # 信号の終了時間
t = np.linspace(ts, tf, tf * samplerate)                # 時間軸を作成
L = chirp(t, f0=10, f1=5000, t1=10, method='linear')    # 1チャンネル目の縦軸を作成
R = np.flip(L) / 2                                      # 2チャンネル目の縦軸を作成
 
wave = np.array([L, R])                                 # チャンネル1と2を結合
wave = wave.T                                           # 多チャンネルwav形式に変換（転置）
 
# ステレオのwavファイルを保存
sf.write('stereo.wav', wave, samplerate)
 
# ここからグラフ描画
# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'
 
# 目盛を内側にする。
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
 
# グラフの上下左右に目盛線を付ける。
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')
ax2 = fig.add_subplot(212)
ax2.yaxis.set_ticks_position('both')
ax2.xaxis.set_ticks_position('both')
 
# 軸のラベルを設定する。
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('L')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('R')
 
# データプロット。
ax1.plot(t, L)
ax2.plot(t, R)
 
# レイアウト設定
fig.tight_layout()
 
# グラフを表示する。
plt.show()
plt.close()
```

```
モノラルの場合は生成した波形をそのまま保存すればよかったのですが、ステレオデータの場合はデータをリストでまとめた後に以下の図のように転置する必要があります。
```
<img src="https://watlab-blog.com/wp-content/uploads/2019/10/wav-save-stereodata-tenchi.png"  width="600" height="400">

[Python:ステレオwavファイルをLRに分ける  2018-07-30](https://gsmcustomeffects.hatenablog.com/entry/2018/07/30/073640)  
```
import wave
import matplotlib.pyplot as plt
import audio_func as af
import scipy

wf = wave.open("GS03.wav", "r")
af.printWaveInfo(wf)  # デバッグ用
data = wf.readframes(wf.getnframes())
num_data = scipy.fromstring(data,dtype = "int16")

if(wf.getnchannels() == 2):
    left = num_data[::2]
    right= num_data[1::2]

    #スライスの説明
    #a[1,2,3,4,5]ていうリストがあったとして
    #a[::2]  -> 1,3,5
    #a[1::2] -> 2,4

# left channel
plt.subplot(2, 1, 1)
plt.plot(left,label="left")
plt.legend()

# right channel
plt.subplot(2, 1, 2)
plt.plot(right,label="right")
plt.legend()
plt.show()
```

```
def printWaveInfo(wf):
    """WAVEファイルの情報を取得"""
    print("チャンネル数 : "+ str(wf.getnchannels()))
    print("サンプル幅 : "+ str(wf.getsampwidth()))
    print("サンプルレート : "+ str(wf.getframerate()))
    print("フレーム数 : "+ str(wf.getnframes()))
    print("総パラメータ（一括表示用） : "+ str(wf.getparams()))
    print("再生時間 : "+ str(float(wf.getnframes()) / wf.getframerate()))
```

[ @peterleif/peterleif/audio_test.py](https://gist.github.com/peterleif/babcab8881762845fd462237a010644d)  
(https://gist.github.com/peterleif/babcab8881762845fd462237a010644d#file-audio_test-py)

[モノラルの各wavファイルを一括フーリエ変換し、同じ名前のCSVで出力したい ](https://teratail.com/questions/275967)  
```
import wave
from pydub import AudioSegment
import glob
import os
import struct
from scipy import fromstring, int32
import numpy as np
from pylab import *
%matplotlib inline

os.chdir('C://Users//karita//sound//data//wav') #パス指定

def fourier(x, n, w):
    K = []
    for i in range(w):
        sample = x[i * n : (i + 1) * n]
        partial = np.fft.fft(sample)
        K.append(partial)
    return K

for file in glob.glob("*.wav"):
    wavfile = open(file, "rb")#サンプルwavファイル
    wr = wave.open(wavfile, "rb") #wavファイルの読み込み
    ch = wr.getnchannels() # モノラルなら1，ステレオなら2
    width = wr.getsampwidth() # サンプル長(1byte=8bit)
    fr = wr.getframerate() #サンプリンググレート（サンプリング周波数）
    fn = wr.getnframes() # 全体のオーディオフレーム数（全データ点数）⇒サンプリング周波数で割れば時間
    buf = wr.readframes(fn)

    mono = np.frombuffer(buf, dtype="int16")
    N = 256
    span = mono.size // N  # int(fn/N) と同じ


    print(wavfile)
    print('サンプル数',N)
    print('チャンネル', ch)
    print('サンプル長（bytes）', width)
    print('サンプリンググレート', fr)
    print('全オーディオフレーム数', fn)
    print("オーディオフレームのバイト数", len(buf))
    print('サンプル時間',fn/fr,'秒')
    print('N*span時間', 1.0 * N * span / fr, '秒')

    mono = np.frombuffer(buf, dtype="int16")
    N = 256
    span = mono.size // N  # int(fn/N) と同じ

    K = fourier(mono, N, span)
    freqlist = np.fft.fftfreq(N, d=1 / fr)
    amp = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in K]

    for i, file in enumerate(glob.glob("*.wav")):
        csv_path = os.path.splitext(os.path.basename(file))[0] + '.csv' # 出力CSVファイル名# 元のファイル名をそのままつける
        np.savetxt(csv_path, [amp], fmt="%.0f",delimiter=",")



    print('==============================================================================================================================')
```


# Build an Audio Spectrum Analyzer  
[markjay4k/Audio-Spectrum-Analyzer-in-Python](https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python)  

[Audio spectrum extraction from audio file by python Jun 24 '14](https://stackoverflow.com/questions/24382832/audio-spectrum-extraction-from-audio-file-by-python)  
```

```

[Understanding Audio data, Fourier Transform, FFT and Spectrogram features for a Speech Recognition System Jan 19](https://towardsdatascience.com/understanding-audio-data-fourier-transform-fft-spectrogram-and-speech-recognition-a4072d228520)  

## Reading Audio Files
## Fourier Transform (FT)
## Fast Fourier Transform (FFT)
## Spectrogram
## Speech Recognition using Spectrogram Features
## Conclusion


# Sound by Python  
## Comparison of Audio Libraries  
[Playing and Recording Sound in Python](https://realpython.com/playing-and-recording-sound-python/)  

| Library | Platform | Playback | Record | Convert | Dependencies | 
| :------------ |:---------------:|:---------------:|:---------------:|:---------------:|:---------------:|
playsound | Cross-platform | WAV, MP3 | - | - | None
simpleaudio | Cross-platform | WAV, array, bytes | - | - | None
winsound | Windows | WAV | - | - | None
sounddevice | Cross-platform | NumPy array | NumPy array | - | numpy, soundfile
pydub | Cross-platform | Any type supported by ffmpeg | - | Any type supported by ffmpeg | simpleaudio, ffmpeg
pyaudio | Cross-platform | bytes | bytes | - | wave
wavio | Cross-platform | - | - | WAV, NumPy array | numpy, wave
soundfile | Cross-platform | - | - | Any type supported by libsndfile | CFFI, libsndfile, numpy

## Play  

```
import winsound

winsound.PlaySound("sample.wav", winsound.SND_FILENAME)
```

```
# ビープ音の再生
import winsound

winsound.Beep(1000, 100) # 1000Hzのビープを100ms再生
```

## Record  
```
import sounddevice as sd
from scipy.io.wavfile import write

record_second = 3
fs = 44100

myrecording = sd.rec(int(record_second * fs), samplerate=fs, channels=2)

write('output.wav', fs, myrecording)
```

```
import pyaudio
import wave

chunk = 1024
format = pyaudio.paInt16
channels = 2
fs = 44100
record_second = 3

p = pyaudio.PyAudio()
stream = p.open(format=format, channels=channels, rate=fs, input=True, frames_per_buffer=chunk)

print("* recording")

frames = []

for i in range(int(fs / chunk * record_second)):
    data = stream.read(chunk)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("output.wav", "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
```

## Devices  
```
import sounddevice as sd
sd.query_devices()
```

> デバイスIDを、default.device に設定するか、play() や Stream() に device引数 として割り当てることで、デバイスの選択が可能

```
import sounddevice as sd
sd.default.device = 1, 5
```


# RaspberryPi + Python3でPyaudio  
[RaspberryPi + Python3でPyaudioとdocomo音声認識APIを使ってみる updated at 2018-10-27](https://qiita.com/yukky-k/items/0d18ec22420e8b35d0ac#%E3%83%9E%E3%82%A4%E3%82%AF%E3%81%A8%E3%82%B9%E3%83%94%E3%83%BC%E3%82%AB%E3%83%BC%E3%81%AE%E6%8E%A5%E7%B6%9A%E3%81%A8%E9%8C%B2%E9%9F%B3%E3%81%AE%E7%A2%BA%E8%AA%8D)  

## マイクとスピーカーの接続と録音の確認  
```
$ lsusb
Bus 001 Device 006: ID 054c:0686 Sony Corp.
Bus 001 Device 007: ID 0424:7800 Standard Microsystems Corp.
Bus 001 Device 003: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
Bus 001 Device 002: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

```
$ arecord -l
**** ハードウェアデバイス CAPTURE のリスト ****
カード 1: UAB80 [UAB-80], デバイス 0: USB Audio [USB Audio]
  サブデバイス: 1/1
  サブデバイス #0: subdevice #0
```

```
$ arecord -D plughw:1,0 test.wav
録音中 WAVE 'test.wav' : Unsigned 8 bit, レート 8000 Hz, モノラル

$ aplay -D plughw:1,0 test.wav
再生中 WAVE 'test.wav' : Unsigned 8 bit, レート 8000 Hz, モノラル
```

```
$ alsamixer
```

```
$ aplay -D plughw:1,0 /usr/share/sounds/alsa/Front_Center.wav
```

[windowsのGUIからpython呼び出す時のエラー通知方法というかwinsound.Beep  Sep 25, 2016](https://qiita.com/noexpect/items/382ee6bdb3b718aa838a)  

[OpenJTalk + python で日本語テキストを発話 Feb 20, 2016](https://qiita.com/kkoba84/items/b828229c374a249965a9)  

[OpenJTalk on Windows10 (環境構築からPythonで日本語をしゃべらせる) Dec 27, 2019](https://qiita.com/koichi_baseball/items/09cd984a409b3701b423)  

[Pythonのみを使って、今実運用可能なWindowsアプリ（exe）を作るとしたら Jul 15, 2020](https://qiita.com/miu200521358/items/557d9f7a29b1a6a9b28d#33-exe%E3%82%92%E4%BD%9C%E6%88%90%E3%81%99%E3%82%8B)
[ miu200521358 /PythonExeSample ](https://github.com/miu200521358/PythonExeSample)


# Return value of scipy.io.wavfile.read  
[python - scipy.io.wavfile.read返回的数据是什么意思？](https://www.coder.work/article/3164721)  
```
Returns
-------
rate : int
    Sample rate of wav file.
data : numpy array
    Data read from wav file.  Data-type is determined from the file;
    see Notes.
```

## What do the bytes in a .wav file represent?  
[What do the bytes in a .wav file represent? asked Oct 23 '12](https://stackoverflow.com/questions/13039846/what-do-the-bytes-in-a-wav-file-represent)  
![alt tag](https://i.stack.imgur.com/fV2nh.png)  
```
You see your audio wave (the gray line). 
The current value of that wave is repeatedly measured and given as a number. That's the numbers in those bytes. 
There are two different things that can be adjusted with this: 
The number of measurements you take per second (that's the sampling rate, given in Hz -- that's how many per second you grab). 
The other adjustment is how exact you measure. 
In the 2-byte case, you take two bytes for one measurement (that's values from -32768 to 32767 normally). 
So with those numbers given there, you can recreate the original wave (up to a limited quality, of course, but that's always so when storing stuff digitally). 
And recreating the original wave is what your speaker is trying to do on playback.
```

```
There are some more things you need to know. 
First, since it's two bytes, you need to know the byte order (big endian, little endian) to recreate the numbers correctly. 
Second, you need to know how many channels you have, and how they are stored. 
Typically you would have mono (one channel) or stereo (two), but more is possible. 
If you have more than one channel, you need to know, how they are stored. 
Often you would have them interleaved, that means you get one value for each channel for every point in time, 
and after that all values for the next point in time.
```

[Sampling (signal processing)](https://en.wikipedia.org/wiki/Sampling_(signal_processing)#Sampling_rate)  
Sampling rate | Use 
------------------------------------ | --------------------------------------------- 
8,000Hz | Telephone and encrypted walkie-talkie, wireless intercom and wireless microphone transmission; adequate for human speech but without sibilance (ess sounds like eff (/s/, /f/)).
16,000Hz | Wideband frequency extension over standard telephone narrowband 8,000 Hz. Used in most modern VoIP and VVoIP communication products.
32,000Hz | miniDV digital video camcorder, video tapes with extra channels of audio (e.g. DVCAM with four channels of audio), DAT (LP mode), Germany's Digitales Satellitenradio, NICAM digital audio, used alongside analogue television sound in some countries. High-quality digital wireless microphones. Suitable for digitizing FM radio.
44,100Hz | Audio CD, also most commonly used with MPEG-1 audio (VCD, SVCD, MP3). Originally chosen by Sony because it could be recorded on modified video equipment running at either 25 frames per second (PAL) or 30 frame/s (using an NTSC monochrome video recorder) and cover the 20 kHz bandwidth thought necessary to match professional analog recording equipment of the time. A PCM adaptor would fit digital audio samples into the analog video channel of, for example, PAL video tapes using 3 samples per line, 588 lines per frame, 25 frames per second. 
48,000Hz | The standard audio sampling rate used by professional digital video equipment such as tape recorders, video servers, vision mixers and so on. This rate was chosen because it could reconstruct frequencies up to 22 kHz and work with 29.97 frames per second NTSC video – as well as 25 frame/s, 30 frame/s and 24 frame/s systems. With 29.97 frame/s systems it is necessary to handle 1601.6 audio samples per frame delivering an integer number of audio samples only every fifth video frame.  Also used for sound with consumer video formats like DV, digital TV, DVD, and films. The professional Serial Digital Interface (SDI) and High-definition Serial Digital Interface (HD-SDI) used to connect broadcast television equipment together uses this audio sampling frequency. Most professional audio gear uses 48 kHz sampling, including mixing consoles, and digital recording devices. 

# speech_process_exercise  
[tam17aki /speech_process_exercise](https://github.com/tam17aki/speech_process_exercise)  
[speech_process_exercise/DigitalSignalProcessing/](https://github.com/tam17aki/speech_process_exercise/tree/master/DigitalSignalProcessing)

## ディジタル信号処理の基礎  


# 音楽のデジタル信号での各ビットの役割。
[N-1. 量子化のビット構成に付いて](https://qiita.com/Try-Jizy/items/178aefe3f06a634064ca#n-1-%E9%87%8F%E5%AD%90%E5%8C%96%E3%81%AE%E3%83%93%E3%83%83%E3%83%88%E6%A7%8B%E6%88%90%E3%81%AB%E4%BB%98%E3%81%84%E3%81%A6)  

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F277872%2Fbad72a9d-7e31-1cb3-a6b1-9944c64bca56.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=233e8bac1199460095c049e6b6b274fe)  

```
図-N11左半分では、「16bit符号付きリニアPCM」(WAV)のビット構成を表しています。CDもこの構成になっていると思われます。

すなわち、波形の「0 から +1」の信号を「 32,768 (15bit、2の15乗)ステップ」で、
「0 から -1(0を含まない)」の信号を同様に「 32,768 ステップ」で数値化し、
「プラスとマイナスを区別するために1bit」を用いて、「合計 16bitで表現している」となります。

ちなみに、アナログ時代からの著者は、この量子化が「16bitなので、65536(2の16乗)ステップ、96dBのダイナミックレンジがある」
と表現する事に違和感を感じています。
```

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F277872%2F9eda71ed-f598-f1c6-5cd3-57eafba7109c.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=46a23d0d0e91d5ed1457faa864a41038)  

```
図-N12は、デジタル編集が内部で計算に使う「32bit-float(符号付き、32bit浮動小数点数)」のビット構成です。
一番上位のビット(赤文字)が±の符号を表す符号部、その下の8bit(青文字)が指数(小数点の位置)を表す指数部、
さらにその下の23ビット(黒文字)が小数点の位置が指定されていない数値本体を表す仮数部です。<引用資料-N12>

特徴的なのは指数部が追加されていることです。これは、Excelでお馴染み「100000=1.0E+05 or 0.00001=1.0E-05」
の表現が出来ることなのでしょう。これにより、途中計算で扱える数値の幅が格段に増加して計算途中のクリップを防いでくれます。
入り口と出口は、自己責任ですが・・・・。
```

# DSP (digital signal processing ) functionality  
[Christian's Python Library](https://homepage.univie.ac.at/christian.herbst/python/index.html)
```
This is a collection of open source Python scripts that I found useful for analyzing data from human and mammalian vocalizations, 
and for generating aesthetically pleasing graphs and videos, 
to be used in publications and presentations/lectures. 
```

## Loading a wave file and saving a normalized version of the sound  
```
import myWave
import dspUtil
import numpy
import copy
import generalUtility
fName = 'WilhelmScream.wav'
# http://en.wikipedia.org/wiki/Wilhelm_scream
# http://www.youtube.com/watch?v=Zf8aBFTVNEU
# load the input file
# data is a list of numpy arrays, one for each channel
numChannels, numFrames, fs, data = myWave.readWaveFile(fName)
# normalize the left channel, leave the right channel untouched
data[0] = dspUtil.normalize(data[0])
# just for kicks, reverse (i.e., time-invert) all channels
for chIdx in range(numChannels):
    n = len(data[chIdx])
    dataTmp = copy.deepcopy(data[chIdx])
    for i in range(n):
        data[chIdx][i] = dataTmp[n - (i + 1)]
# save the normalized file (both channels)
# this is the explicit code version, to make clear what we're doing. since we've
# treated the data in place, we could simple write: 
# myWave.writeWaveFile(data, outputFileName, fs) and not declare dataOut
dataOut = [data[0], data[1]] 
fileNameOnly = generalUtility.getFileNameOnly(fName)
outputFileName = fileNameOnly + "_processed.wav"
myWave.writeWaveFile(dataOut, outputFileName, fs)
```

# Polar Response   
[Jupyter Notebookで指向性をグラフ化してみた updated at 2017-12-16](https://qiita.com/chanyou0311/items/1f4b09b3a9bcf28c3746)  
```
データ数が増えるのはいいとして、これ指向性だから極座標形式で描画しないといけない。
できるだろうけど文献がほとんどないぞ。がんばろう。
```

```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('sample.csv')

deg = df['Phi [deg]']
values = df.iloc[:, 1:]

lines = ['-', '--', '-.', ':', '.', ',']

ax = plt.subplot(111, projection='polar')

ax.axes.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlabel_position(0)
ax.set_xticks(np.pi/180. * np.linspace(0,  360, 12, endpoint=False))

ax.spines['polar'].set_color('darkgray')

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

plt.ylim(-60.1, 5)

theta = deg*np.pi/180
r = values

for i in range(len(values.columns)):
    label = values.columns[i]
    line = lines[i%len(lines)]
    ax.plot(theta, values.iloc[:, i], line, label=label)

plt.legend(bbox_to_anchor=(0.5, -0.15),  ncol=len(values.columns), loc='center')
plt.savefig('sample.png', dpi=500, bbox_inches='tight')
plt.show()
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F177433%2F444645cb-a8ce-a9f8-22e2-dbb64dfc3168.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=8dc76cfbe252f06d4a1d8828086d4776"  width="500" height="500">

[Matplotlibでレーダーチャートを描く（16行）updated at 2019-01-14](https://qiita.com/1007/items/80406e098a4212571b2e)  

```
要約すると

1. 極座標のAxesオブジェクトを作って、
2. そこにポリゴンを描画する。
3. 塗りつぶしても良し。

凡例やタイトルの追加、複数データのプロットは通常のグラフ同様にできるので省略。
```

```
import matplotlib.pyplot as plt
import numpy as np

def plot_polar(labels, values, imgname):
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)
    values = np.concatenate((values, [values[0]]))  # 閉じた多角形にする
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-')  # 外枠
    ax.fill(angles, values, alpha=0.25)  # 塗りつぶし
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)  # 軸ラベル
    ax.set_rlim(0 ,250)
    fig.savefig(imgname)
    plt.close(fig)

labels = ['HP', 'Attack', 'Defense', 'Speed']
values = [155, 156, 188, 139]
plot_polar(labels, values, "radar.png")
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F146259%2F5826f4fd-decd-b94e-7f3d-e962e81e350a.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=58e46ad60547cecb75f80d7e544c610c"  width="700" height="700">

[Pythonで音のSTFT計算を自作!スペクトログラム表示する方法 2019.05.19](https://watlab-blog.com/2019/05/19/python-spectrogram/)  

```
import function
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import chirp

# チャープ信号を作成
t = np.linspace(0, 5, 128000)
data = chirp(t, f0=1, f1=2000, t1=5, method='linear')
samplerate = 25600

x = np.arange(0, len(data)) / samplerate    #波形生成のための時間軸の作成

# Fsとoverlapでスペクトログラムの分解能を調整する。
Fs = 4096                                   # フレームサイズ
overlap = 75                               # オーバーラップ率

# オーバーラップ抽出された時間波形配列
time_array, N_ave, final_time = function.ov(data, samplerate, Fs, overlap)

# ハニング窓関数をかける
time_array, acf = function.hanning(time_array, Fs, N_ave)

# FFTをかける
fft_array, fft_mean, fft_axis = function.fft_ave(time_array, samplerate, Fs, N_ave, acf)

# スペクトログラムで縦軸周波数、横軸時間にするためにデータを転置
fft_array = fft_array.T

# ここからグラフ描画
# グラフをオブジェクト指向で作成する。
fig = plt.figure()
ax1 = fig.add_subplot(111)

# データをプロットする。
im = ax1.imshow(fft_array, \
                vmin = -10, vmax = 60,
                extent = [0, final_time, 0, samplerate], \
                aspect = 'auto',\
                cmap = 'jet')

# カラーバーを設定する。
cbar = fig.colorbar(im)
cbar.set_label('SPL [dBA]')

# 軸設定する。
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Frequency [Hz]')

# スケールの設定をする。
ax1.set_xticks(np.arange(0, 120, 1))
ax1.set_yticks(np.arange(0, 20000, 500))
ax1.set_xlim(0, 5)
ax1.set_ylim(0, 2000)

# グラフを表示する。
plt.show()
plt.close()
```
<img src="https://watlab-blog.com/wp-content/uploads/2019/09/spectrogram-chirp.png"  width="800" height="700">


# Kaldi  
[音声認識システム　Kaldiを試しに動かしてみた Apr 10, 2015](https://qiita.com/GushiSnow/items/43d5916cc8a0c939f1dd)  
## Kaldiインストール  
```
build-essential
gfortran
libgfortran3
python-dev(python3-dev)
libblas-dev
libatlas-base-dev
cython
g++ 
zlib1g-dev
automake
libtool
autoconf 
```

## Simple Guide To “KALDI”  
[Simple Guide To “KALDI” — an efficient open source speech recognition tool for Extreme Beginners — by a beginner! May 30, 2018](https://medium.com/@nikhilamunipalli/simple-guide-to-kaldi-an-efficient-open-source-speech-recognition-tool-for-extreme-beginners-98a48bb34756)

Kaldi- made easy steps start here :  
```
step 1 : Before you start with kaldi learn the foundation of docker with this simple video tutorial. 
: https://www.youtube.com/watch?v=pGYAg7TMmp0

```
```
step 2 : installation of docker : https://docs.docker.com/install/linux/docker-ce/ubuntu/

That was a great intro to docker. I advise you to learn docker usage with the official documentation : https://docs.docker.com/get-started/.

As already said lazy ones can skip learning.

```
```
step 3 : downloading tedlium dataset :https://phon.ioc.ee/%7Etanela/tedlium_nnet_ms_sp_online.tgz

This file must be stored in media/kaldi_models directory.

to access media, go to computer>media

open terminal there and make directory by running this command.

sudo mkdir kaldi_models

move the downloaded file, after extraction, from downloads to this directory by this command.

sudo mv /downloads/english media/kaldi_models/

this dataset is 1.4GB which is neither too big nor too small!

```
```
step 4 : pulling the docker image from dockerHub :

sudo docker pull jcsilva/docker-kaldi-gstreamer-server

run this command to download the image.

```
```
step 5 : yaml file download : https://github.com/alumae/kaldi-gstreamer-server/blob/master/sample_english_nnet2.yaml

from the above link download yaml file and name it nnet2.yaml.

store the file in english directory.

imp :open the file in the text editor and replace test/models with opt/models.

this will be explained later.

In the file, comment out the line

“full-post-processor: ./sample_full_post_processor.py”

as you wont have the sample_full_post_processor.py file . This wont effect the functionality of yaml file.

for further information about yaml follow this great video : https://www.youtube.com/watch?v=cdLNKUoMc6c

```
```
step 6: sudo docker container ls

this command gives the list of available containers. if you find a container with image : 
jcsilva/docker-kaldi-gstreamer-server:latest, your container allocation is successful 
under the port 8080:80.

```
```
step 7 : getting inside the container :

docker run -it -p 8080:80 -v /media/kaldi_models:/opt/models jcsilva/docker-kaldi-gstreamer-server:latest /bin/bash

this gets you inside the container which can almost be used as a normal linux terminal. 
Docker partitions memory for its container. place the yaml file in opt/models.

```
```
step 8 : starting master and worker by docker :

./start.sh -y /opt/models/nnet2.yaml

this will create master.log and worker.log in opt.

```
```
step 9 : run ls -l to see the available items in the container.

if the list contains :

gst-kaldi-nnet2-online, kaldi, kaldi-gstreamer-server, master.log, models, start.sh, stop.sh, worker.log

then your ./start was executed properly.

```
```
step 10 : run cat worker.doc to find whether worker is working.

you probably should encounter an error showing no path found which can be eliminated by modifying the conf files.

ls models/english/tedlium_nnet_ms_sp_online/conf/

this gives all the files in conf.

vi models/english/tedlium_nnet_ms_sp_online/conf/<file>

replace the <file> with the name of the file in conf folder. modify the test/models path anywhere 
if found to opt/models. View each file of conf folder by running the same command.

run cat worker.doc again to test the functionality. This time the error must be resolved 
and worker available message must be displayed.

```
```
step 11 : websocket url : http://www.websocket.org/echo.html

enter the web page. in the location enter : ws://localhost:8080/client/ws/status and press connect. On connecting, if you find the message : 
RECEIVED: {“num_workers_available”: 1, “num_requests_processed”: 9} in log, then the connection is perfect.

Congratulations!! now you have a working kaldi speech recognizer(english) with gstreamer and docker.
```

[【Kaldi 新手入門】手把手教你搭建簡易英文數字ASR系統 2018-12-18](https://www.itread01.com/content/1545129581.html)
[AndroidStudio2017 /digitsASR](https://github.com/AndroidStudio2017/digitsASR)


[Kaldiに関する処理を日本語のドキュメントでまとめてみた(データ準備編）１ 2015/04/15](http://qiita.com/GushiSnow/items/cc1440e0a8ea199e78c5)  
[Kaldiに関する処理を日本語のドキュメントでまとめてみた（データ準備編）2 2015/04/15](http://qiita.com/GushiSnow/items/a24cad7231de341738ee)  
[Kaldiに関する処理を日本語のドキュメントでまとめてみた（特徴量抽出編）3 2015/04/15](http://qiita.com/GushiSnow/items/e099baf9d1c2e72cb3d1)  
[Kaldiに関する処理を日本語のドキュメントでまとめてみた（学習編）4 2015/04/15](http://qiita.com/GushiSnow/items/d431a5c49dc4206def2d)  
[Kaldiに関する処理を日本語のドキュメントでまとめてみた（グラフ作成編）5 2015/04/16](https://qiita.com/GushiSnow/items/8e1c25b1d2eda8c1f2c3)  
[Kaldiに関する処理を日本語のドキュメントでまとめてみた（デコーディング編）6 2015/04/16](https://qiita.com/GushiSnow/items/01296c16f0d9d823ae55)  

[音声認識について噛み砕いてみた Dec 02, 2019](https://qiita.com/dcm_katou/items/9ec80f7c714631f568bb)
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F525974%2F11bd68e4-60ac-284e-351c-63a0af5444e4.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=e1eabfed9cf6938e27a78596ad558d58"  width="800" height="400">


[ここ10年の音声認識のアーキテクチャの変化を雑に整理する（前編） Dec 18, 2019](https://qiita.com/corocn/items/81c255e5f742f767144f)  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F66417%2F68e83929-e678-7f27-c75e-19cd11bdc557.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=12b4db9c31b6ecf94a86c07d18de757a"  width="800" height="400">


[ここ10年の音声認識のアーキテクチャの変化を雑に整理する（中編） Dec 14, 2019](https://qiita.com/corocn/items/7eb846ff83c0f67bca53)  
```
kaldi

    https://kaldi-asr.org/
    https://github.com/kaldi-asr/kaldi

こちらはWFST型の音声認識です。作者の論文はよく見てましたが、ちょうどKaldiが話題になったごろで音声認識から離れてしまったのでちゃんと動かしておらず。今でも結構使われてるみたいです。
```

[Kaldiを用いたリアルタイム音声認識 Dec 08, 2017](https://qiita.com/sayonari/items/936171340990c474be73)  
```
最近音声認識研究業界では標準になっているＫａｌｄｉを用いて，リアルタイム音声認識をする方法です．
音声が入力されている間にも，どんどん音声認識がされていく環境です
（１発話が終わってから，音声が認識開始されるのではない．）．

Kaldi GStreamer serverを用いて音声認識を行いますが，この環境がDockerイメージで公開されているので，
それを使います．使わなくてもできると思います．

以下の例では，DNNの音声認識モデルにて，英語の音声認識をします．kaldi用online_nnet2モデルがあれば，
日本語でもできるようです．
```
[Kaldi GStreamer server](https://github.com/alumae/kaldi-gstreamer-server)  
[docker-kaldi-gstreamer-server](https://github.com/jcsilva/docker-kaldi-gstreamer-server)  


# Progress Bar  
## light-progress  
[Pythonで `light-progress` を使って進捗(プログレスバー)を表示 updated at 2018-12-04](https://qiita.com/itkr/items/fab6a5e492b28bb07fab)  
```
format_str = '{} {} ({})'

widgets = [widget.Bar(), widget.Percentage(), widget.Num()]
ProgressBar.iteration(
    range(100),
    lambda item: sleep(0.01),
    widgets=widgets,
    format_str=format_str)

# [███████████████████████████████] 100% (100/100)
```

```
format_str = '{} *** {} *** ({})'

widgets = [widget.Bar(), widget.Percentage(), widget.Num()]
ProgressBar.iteration(
    range(100),
    lambda item: sleep(0.01),
    widgets=widgets,
    format_str=format_str)

# [███████████████████████████████] *** 100% *** (100/100)
```

## Download Large Files with Tqdm Progress Bar  
[Python Progress Bars with Tqdm by Example Dec 10, 2019](https://medium.com/better-programming/python-progress-bars-with-tqdm-by-example-ce98dbbc9697)  
```
#  Copyright 2019 tiptapcode Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# -*- coding: utf-8 -*-
import os
import sys
import tqdm
import requests
import validators


class FileDownloader(object):

    def get_url_filename(self, url):
        """
        Discover file name from HTTP URL, If none is discovered derive name from http redirect HTTP content header Location
        :param url: Url link to file to download
        :type url: str
        :return: Base filename
        :rtype: str
        """
        try:
            if not validators.url(url):
                raise ValueError('Invalid url')
            filename = os.path.basename(url)
            basename, ext = os.path.splitext(filename)
            if ext:
                return filename
            header = requests.head(url, allow_redirects=False).headers
            return os.path.basename(header.get('Location')) if 'Location' in header else filename
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            raise errh
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            raise errc
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            raise errt
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            raise err

    def download_file(self, url, filename=None, target_dir=None):
        """
        Stream downloads files via HTTP
        :param url: Url link to file to download
        :type url: str
        :param filename: filename overrides filename defined in Url param
        :type filename: str
        :param target_dir: target destination directory to download file to
        :type target_dir: str
        :return: Absolute path to target destination where file has been downloaded to
        :rtype: str
        """
        if target_dir and not os.path.isdir(target_dir):
            raise ValueError('Invalid target_dir={} specified'.format(target_dir))
        local_filename = self.get_url_filename(url) if not filename else filename

        req = requests.get(url, stream=True)
        file_size = int(req.headers['Content-Length'])
        chunk_size = 1024  # 1 MB
        num_bars = int(file_size / chunk_size)

        base_path = os.path.abspath(os.path.dirname(__file__))
        target_dest_dir = os.path.join(base_path, local_filename) if not target_dir else os.path.join(target_dir, local_filename)
        with open(target_dest_dir, 'wb') as fp:
            for chunk in tqdm.tqdm(req.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc=local_filename, leave=True, file=sys.stdout):
                fp.write(chunk)

        return target_dest_dir


if __name__== "__main__":

    links = ['https://nodejs.org/dist/v12.13.1/node-v12.13.1.pkg', 'https://aka.ms/windev_VM_virtualbox']

    downloader = FileDownloader()

    for url in links:
        downloader.download_file(url)
```

# 【Scipy】 FFT, STFT and wavelet

## STFT変換の例題  
```
#scipy.signal.istft example
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.istft.html
#
import numpy as np  #added by author
from scipy import signal
import matplotlib.pyplot as plt

#Generate a test signal, a 2 Vrms sine wave at 50Hz corrupted by 0.001 V**2/Hz of white noise sampled at 1024 Hz.
#テスト信号、1024 Hzでサンプリングされた0.001 V ** 2 / Hzのホワイトノイズで破損した50 Hzの2 Vrmsの正弦波を生成します

fs = 1024
N = 10*fs
nperseg = 512
amp = 2 * np.sqrt(2)
noise_power = 0.001 * fs / 2
time = np.arange(N) / float(fs)
carrier = amp * np.sin(2*np.pi*50*time)
noise = np.random.normal(scale=np.sqrt(noise_power),
                         size=time.shape)
x = carrier + noise
#Compute and plot the STFT’s magnitude.
#STFTの振幅を計算してプロットします

f, t, Zxx = signal.stft(x, fs=fs, nperseg=nperseg)
plt.figure()
plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=amp)
plt.ylim([f[1], f[-1]])
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.yscale('log')
plt.show()
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F233744%2Fbf55fa04-2c83-d05a-794d-62bc9fbbd714.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=7ed09b364b57c1d7f04b7521b984b835"  width="400" height="400">


## FFT変換の例  
[【Scipy】FFT、STFTとwavelet変換で遊んでみた♬  Jan 09, 2019](https://qiita.com/MuAuan/items/8850e037babcff991b8e)

```
スケールはともかく、時間領域（vs振幅）の図から、周波数領域（vsパワー）の図に変換される。どちらも、
周波数や時間（それぞれ共役量）の記憶がなくなる（積分される）。
```

```
from scipy.fftpack import fft, ifft
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 100, 10000, endpoint=False)
sig = np.cos(2 * np.pi * 4 * t)+np.cos(2 * np.pi * 8 * t)  + np.cos(2 * np.pi * 15 * t)    #*np.exp(-0.1*t) *5
plt.plot(t, sig)
plt.axis([0, 5, -5, 5])
plt.show()
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F233744%2Ffef2ad39-7ebf-fa12-05bb-ceff90e407d4.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=e68f25e83a131905fba545411ea95a2a"  width="400" height="400">

```
freq =fft(sig,1024)
Pyy = np.abs(freq)/1025    #freq*freq.conj(freq)/1025
f = np.arange(1024)
plt.plot(f,Pyy)
plt.axis([0, 200, 0, 1])
plt.show()
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F233744%2Fa72bfd7c-7318-d1ed-9eb1-68a2f89c29dc.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=a12ee65f00a40e273528a87e1c1854bb"  width="400" height="400">

```
t1=np.linspace(0, 10, 1024, endpoint=False)
sig1=ifft(freq)
plt.plot(t1, sig1)
plt.axis([0, 5, -5, 5])
plt.show()
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F233744%2F08d82c52-336a-efcc-3dbd-81d0559e8dc3.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=a96376eb4a0cabe30cc86d0284f3a509"  width="400" height="400">

## FFT変換・逆変換
[【Scipy】FFT、STFTとwavelet変換で遊んでみた♬～②不確定原理について～ Jan 12, 2019](https://qiita.com/MuAuan/items/504160465e83e556dd3e)  

```
ここで注意したいのは、最後のしっぽが完全には戻らないことである。

以上のとおり、FFTにおける不確定性原理は、時間軸から変換の共役変数である周波数軸に完全に移り、変換の前後で以前の空間の情報は完全に失われることである。
```

```
from scipy.fftpack import fft, ifft
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 100, 1000, endpoint=False)
sig=[]
for t1 in t:
    if t1<20:
        sig1 = np.cos(2 * np.pi * 0.5 * t1)
        print("5",t1)
    elif t1<40:
        sig1 = np.cos(2 * np.pi * 1 * t1)
        print("10",t1)
    elif t1<60:
        sig1 = np.cos(2 * np.pi * 1.5 * t1)
        print("20",t1)
    elif t1<80:
        sig1 = np.cos(2 * np.pi * 2 * t1)
        print("30",t1)
    else:
        sig1 = np.cos(2 * np.pi * 2.5 * t1)
        print(t1)
    sig.append(sig1)

plt.plot(t, sig)
plt.axis([0, 100, -2, 2])
plt.show()
```

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F233744%2F9a97485d-ec2c-53c8-4144-beaf08f72f1b.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=d3279fea4637b65ca8290d7bd997210c"  width="400" height="400">

```
freq =fft(sig,1024)
Pyy = np.sqrt(freq*freq.conj())/1025 #np.abs(freq)/1025    
f = np.arange(1024)
plt.plot(f,Pyy)
plt.axis([0, 512, 0, 0.2])
plt.show()
```

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F233744%2F1b251f2f-3215-47ab-efed-2cf5fb8ebd52.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=851edd84066c33b23cdf5a2d3489aa48"  width="400" height="400">

```
t1=np.linspace(0, 100, 1024, endpoint=False)
sig1=ifft(freq)
plt.plot(t1, sig1)
plt.axis([0, 100, -2, 2])
plt.show()
```

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F233744%2F6d6b9293-7e68-4d45-ff32-098d55cd390f.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=9a3ea13a07b005b3066058cfdb86bf33"  width="400" height="400">

## STFT変換・逆変換
[短時間フーリエ変換@Wikipedia](https://ja.wikipedia.org/wiki/%E7%9F%AD%E6%99%82%E9%96%93%E3%83%95%E3%83%BC%E3%83%AA%E3%82%A8%E5%A4%89%E6%8F%9B)  

## wavelet変換・逆変換  

<img src=""  width="400" height="400">

[【Scipy】FFT、STFTとwavelet変換で遊んでみた♬～③音声データに応用する～ Jan 21, 2019](https://qiita.com/MuAuan/items/858aab2879708668e2bb)  
[【Scipy】FFT、STFTとwavelet変換で遊んでみた♬～④FFTからwavelet変換まで；ちょっと理論 Jan 24, 2019](https://qiita.com/MuAuan/items/70c87d42c3a258d0b6fd)  
[【Scipy】FFT、STFTとwavelet変換で遊んでみた♬～音声合成アプリ Feb 08, 2019](https://qiita.com/MuAuan/items/1199a63797f50a6141a1)  
[【Scipy】FFT、STFTとwavelet変換で遊んでみた♬～⑦リアルタイム・スペクトログラム Feb 03, 2019](https://qiita.com/MuAuan/items/85b077640901dbb29514)  
[【Scipy】FFT、STFTとwavelet変換で遊んでみた♬～⑦リアルタイム・スペクトログラム；高速化 Feb 03, 2019](https://qiita.com/MuAuan/items/6c2ab8497409bac6304e)  
[【Audio入門】発生した音（音声）をSTFTする♬ Jul 17, 2019](https://qiita.com/MuAuan/items/53e5ae4983a307567dc8)  
[【Audio入門】FFT利用のフォルマント音声合成をリアルタイムでやってみる♬ Jul 21, 2019](https://qiita.com/MuAuan/items/2014dd4a28dc9761d86e)  
[【Raspi4；サウンド入門】pythonで音入力を安定して記録する♪  Jun 03, 2020](https://qiita.com/MuAuan/items/c86d45159655dc2fda0e)  

[【動物会話】Keras(Tensorflow), Opencv, pyaudio, ffmpeg, moviepyなどでCPU環境構築♬ Mar 21, 2019](https://qiita.com/MuAuan/items/3a698ef99bb6895aa100)  
[【Finetuningの極意】動物会話のアプリをFinetuning（＋中間層利用）で小規模かつ高速に作成♬  Mar 24, 2019](https://qiita.com/MuAuan/items/2dbf2d454786f9d3d2e4)  
[]()  

# ディープラーニング (Deep learning)声質変換環境構築
[初めての「誰でも好きなキャラの声になれる」ディープラーニング声質変換環境構築【Ubuntu 18.04LTS】updated at 2019-06-11](https://qiita.com/BURI55/items/92ba127c7beb95b2b3f0)  

[「ディープラーニングの力で結月ゆかりの声になる」*4レポジトリbecome-yukarin](https://github.com/Hiroshiba/become-yukarin)  
[「become-yukarin解説用」レポジトリ　become-yukarin](https://github.com/YoshikazuOota/become-yukarin)  

[『Yukarinライブラリ』become-yukarin, yukarin コマンド解説 updated at 2020-04-16](https://qiita.com/atticatticattic/items/37441f3be6916cd1e73a)
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F12429%2F30df6ea3-7c37-8043-04d2-ebaac6519306.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=97331b6e335cc3778fa0955f4ea4b720)  


# 音声を並列で再生する方法  
[pythonで音声を並列で再生する方法 updated at 2019-08-28](https://qiita.com/yunishi3/items/4fe5b7c6718a71fd4c81)  

```
import subprocess

A = '○○○.mp3'
B = '●●●.mp3'

subprocess.Popen(['mplayer', A])
subprocess.Popen(['mplayer', B])
```

```
pythonで音声を再生する際はpyAudioを使うのが一般的ですが、これをthreadingなどで並列処理化しても、
うまく並列再生されず、しまいにはおそらくメモリーエラーでSegmentation Faultになりました(信号の取得等の処理を入れています)。
```



# combine-multiple-channels-of-audio-files  
[combine-multiple-channels-of-audio-files](https://github.com/JiachuanDENG/combine-multiple-channels-of-audio-files/blob/master/combineMultiChannels.py)

## Usage  
```
change fns ,chns,output_fn in combineMultiChannels.py accordingly. 
Then do python3 combineMultiChannels.py
```

## Example  

If we want to get the channel 1's data of 1.wav  
<img src="https://user-images.githubusercontent.com/20760190/70675675-b47f1980-1c3e-11ea-8dac-b56580f8e6a4.png"  width="600" height="300">  

and channel 0 and channel 2's data of 2.wav  
<img src="https://user-images.githubusercontent.com/20760190/70681236-8ce47d00-1c4f-11ea-869b-47162a54b04c.png"  width="600" height="300">

We set: fns = ['1.wav','2.wav'] chns = [[1],[0,2]] output_fn = './output/out.wav' in combineMultiChannels.py, 
it will give us the output file out.wav  

<img src="https://user-images.githubusercontent.com/20760190/70681515-7db1ff00-1c50-11ea-860b-e3ec24361cc9.png"  width="600" height="300">

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

