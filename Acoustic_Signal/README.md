
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

[【Audio入門】音声変換してみる♬ posted at 2019-07-07](https://qiita.com/MuAuan/items/675854ab602595c79612)  
[深層学習による声質変換 updated at 2016-12-23](https://qiita.com/satopirka/items/7a8a503725fc1a8224a5)  
[Pythonで音声信号処理  2011-05-14](http://aidiary.hatenablog.com/entry/20110514/1305377659)


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
