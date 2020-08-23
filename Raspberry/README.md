Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Pythonでpandas](#pythonでpandas)
      * [対処方法](#対処方法)
   * [IR Control](#ir-control)
      * [構成図](#構成図)
      * [ADRSIRから家電操作](#adrsirから家電操作)
      * [Beebotteの設定](#beebotteの設定)
   * [Raspberry pi で音声会話をする](#raspberry-pi-で音声会話をする)
      * [作り方Ⅰ（マイクの設定）](#作り方ⅰマイクの設定)
      * [設定Ⅱ（スピーカの設定）](#設定ⅱスピーカの設定)
      * [設定Ⅲ（pyaudio）](#設定ⅲpyaudio)
   * [音楽(wav/mp3)ファイルを再生する方法 python編](#音楽wavmp3ファイルを再生する方法-python編)
      * [1. pygame](#1-pygame)
      * [2. PyAudio](#2-pyaudio)
      * [3. vlc](#3-vlc)
      * [4. aplay](#4-aplay)
      * [5. mpg321](#5-mpg321)
      * [おまけ1： 音楽出力先の指定](#おまけ1-音楽出力先の指定)
         * [1. コマンドラインでの操作](#1-コマンドラインでの操作)
         * [2.raspi-configでの操作](#2raspi-configでの操作)
      * [おまけ2：音質](#おまけ2音質)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of Raspberry stuffs

# Pythonでpandas  
[ラズベリーパイのPythonでpandasが正常にインストールされない場合 updated at 2018-09-21](https://qiita.com/Avocado/items/ba800e5afffc2bd98dc6)  

## 対処方法  
```
pandasのインストール方法をpipからapt-getに変更します。
```

# IR Control  
[RaspberryPi＋ADRSIRを用いた赤外線機器操作 posted at 2019-12-15](https://qiita.com/Kept1994/items/012928af94dd41bb4d6c)  

## 構成図  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F406130%2Fb6da4c3d-9683-2537-490f-14c8adbca34e.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=10b1c7d1b24806a9644cc61d86b785cc)  

##  ADRSIRから家電操作  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F406130%2Fcff1fe8c-ea28-4edc-bcb9-68cd4d0d4792.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=66aa1e9f5bce94890df9a5589a57df34)  

##  Beebotteの設定  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F406130%2Fccc2804b-7e02-1f84-d8b9-066accdc6570.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=d8c45a3a9adda2595c2300b30ad037d8)  

[LIRCでRaspberry Piの赤外線制御 （家電、エアコン、照明、テレビなどを制御するホームIoT）](https://www.indoorcorgielec.com/resources/%E5%BF%9C%E7%94%A8%E4%BE%8B/lirc%E3%81%A7rpitph-monitor-rpz-ir-sensor%E3%81%AE%E8%B5%A4%E5%A4%96%E7%B7%9A%E5%88%B6%E5%BE%A1/)  

# Raspberry pi で音声会話をする  
[Raspberry pi で音声会話をする updated at 2018-03-26](https://qiita.com/saitenn/items/ecf9488039eb93babf5e)  

## 作り方Ⅰ（マイクの設定）  
```
sudo nano /etc/modprobe.d/alsa-base.conf
```

```
options snd slots=snd_usb_audio,snd_bcm2835
options snd_usb_audio index=0
options snd_bcm2835 index=1
```

```
$ cat /proc/asound/modules
 0 snd_usb_audio
 1 snd_bcm2835
```

マイクの音量調整は  
```
$ amixer sset Mic 16 -c 0
Simple mixer control 'Mic',0
  Capabilities: cvolume cvolume-joined cswitch cswitch-joined penum
  Capture channels: Mono
  Limits: Capture 0 - 62
  Mono: Capture 62 [100%] [22.50dB] [on]
```

## 設定Ⅱ（スピーカの設定）  
オーディオをミニプラグに出力させる場合  
```
$ amixer cset numid=3 1
```

オーディオをHDMIに出力させる場合
```
$ amixer cset numid=3 2
```

スピーカテスト
```
$ aplay /usr/share/sounds/alsa/Front_Center.wav
```

## 設定Ⅲ（pyaudio）  
[raspberryPi と pyaudioで録音、音声波形処理 2014 12月21](https://hanpakousaku.tumblr.com/post/105771613672/raspberrypi-%E3%81%A8-pyaudio%E3%81%A7%E9%8C%B2%E9%9F%B3%E9%9F%B3%E5%A3%B0%E6%B3%A2%E5%BD%A2%E5%87%A6%E7%90%86)  

```
sudo apt-get install python-pyaudio
```

でpyaudio_test.pyを作成して
```

```

```
# -*- coding: utf-8 -*-
#マイク0番からの入力を受ける。一定時間(RECROD_SECONDS)だけ録音し、ファイル名：mono.wavで保存する。

import pyaudio
import sys
import time
import wave

if __name__ == '__main__':
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    #サンプリングレート、マイク性能に依存
    RATE = 16000
     #録音時間
    RECORD_SECONDS = input('Please input recoding time>>>')

    #pyaudio
    p = pyaudio.PyAudio()

    #マイク0番を設定
    input_device_index = 0
    #マイクからデータ取得
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    all = []
    for i in range(0, RATE / chunk * RECORD_SECONDS):
        data = stream.read(chunk)
        all.append(data)

    stream.close()
    data = ''.join(all)
    out = wave.open('mono.wav','w')
    out.setnchannels(1) #mono
    out.setsampwidth(2) #16bits
    out.setframerate(RATE)
    out.writeframes(data) out.close()

    p.terminate()
```

[簡単にできる！音声認識と音声合成を使ってRaspberrypiと会話 updated at 2016-01-19](https://qiita.com/kinpira/items/75513eaab6eed19da9a3)  
[Raspberry Piで音声認識 updated at 2016-05-16](https://qiita.com/t_oginogin/items/f0ba9d2eb622c05558f4#usb%E3%83%9E%E3%82%A4%E3%82%AF%E3%81%AE%E7%A2%BA%E8%AA%8D)  


# 音楽(wav/mp3)ファイルを再生する方法 python編  
[Raspberry Piで音楽(wav/mp3)ファイルを再生する方法 python編 updated at 2020-08-12](https://qiita.com/Nyanpy/items/cb4ea8dc4dc01fe56918#4aplay)  

## 1. pygame  

## 2. PyAudio  
```
#-*- cording: utf-8 -*-

import wave
import pyaudio

# チャンク数を指定
CHUNK = 1024
filename = "ファイル名.wav"

wf = wave.open(filename, 'rb')

# PyAudioのインスタンスを生成
p = pyaudio.PyAudio()

# Streamを生成
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

"""
 format: ストリームを読み書きする際のデータ型
 channels: モノラルだと1、ステレオだと2、それ以外の数字は入らない
 rate: サンプル周波数
 output: 出力モード
"""

# データを1度に1024個読み取る
data = wf.readframes(CHUNK)

# 実行
while data != '':
    # ストリームへの書き込み
    stream.write(data)
    # 再度1024個読み取る
    data = wf.readframes(CHUNK)

# ファイルが終わったら終了処理
stream.stop_stream()
stream.close()

p.terminate()
```

## 3. vlc  
```
さて、vlcをコマンドライン上で操作するには2つの方法があります。

    cvlcコマンドの利用
    vlc -I rcコマンドの利用
```

```
#-*- cording: utf-8 -*-

import subprocess

subprocess.call("vlc -I rc --play-and-stop ファイル名.wav", shell=True)
```

[python-vlc](https://wiki.videolan.org/Python_bindings/)  
[python-vlc sample](https://git.videolan.org/?p=vlc/bindings/python.git;a=tree;f=examples;hb=HEAD)  

## 4. aplay
```
#-*- cording: utf-8 -*-

import subprocess

subprocess.call("aplay ファイル名.wav", shell=True)
```

## 5. mpg321

## おまけ1： 音楽出力先の指定  
### 1. コマンドラインでの操作  
### 2.raspi-configでの操作  

## おまけ2：音質

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






