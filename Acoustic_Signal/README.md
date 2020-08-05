Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
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
   * [LibROSA](#librosa)
      * [Wavの読み込み](#wavの読み込み)
      * [Fourier transform](#fourier-transform)
   * [Beginner's Guide to Audio Data](#beginners-guide-to-audio-data)
      * [1. データの分析](#1-データの分析)
      * [2. Raw波形を使ったモデルの構築](#2-raw波形を使ったモデルの構築)
         * [Raw波形を使ったKerasモデル](#raw波形を使ったkerasモデル)
      * [3.3. MFCCの紹介](#33-mfccの紹介)
         * [Librosaを使ったMFCCの生成](#librosaを使ったmfccの生成)
   * [LibROSA](#librosa-1)
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
   * [RaspberryPi   Python3でPyaudio](#raspberrypi--python3でpyaudio)
      * [マイクとスピーカーの接続と録音の確認](#マイクとスピーカーの接続と録音の確認)
   * [Return value of scipy.io.wavfile.read](#return-value-of-scipyiowavfileread)
      * [What do the bytes in a .wav file represent?](#what-do-the-bytes-in-a-wav-file-represent)
   * [音楽のデジタル信号での各ビットの役割。](#音楽のデジタル信号での各ビットの役割)
   * [ディープラーニング (Deep learning)声質変換環境構築](#ディープラーニング-deep-learning声質変換環境構築)
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

# LibROSA  
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
[Sox在Windows下的安装以及Sox在python中的安装](https://blog.csdn.net/weixin_43216017/article/details/88531363)
在python中安装Sox包

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


# ディープラーニング (Deep learning)声質変換環境構築
[初めての「誰でも好きなキャラの声になれる」ディープラーニング声質変換環境構築【Ubuntu 18.04LTS】updated at 2019-06-11](https://qiita.com/BURI55/items/92ba127c7beb95b2b3f0)  

[「ディープラーニングの力で結月ゆかりの声になる」*4レポジトリbecome-yukarin](https://github.com/Hiroshiba/become-yukarin)  
[「become-yukarin解説用」レポジトリ　become-yukarin](https://github.com/YoshikazuOota/become-yukarin)  

[『Yukarinライブラリ』become-yukarin, yukarin コマンド解説 updated at 2020-04-16](https://qiita.com/atticatticattic/items/37441f3be6916cd1e73a)
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F12429%2F30df6ea3-7c37-8043-04d2-ebaac6519306.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=97331b6e335cc3778fa0955f4ea4b720)  


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





