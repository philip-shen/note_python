Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [pythonでスマホゲーム自動化<del>PCからandroidの操作を自動化編</del>](#pythonでスマホゲーム自動化pcからandroidの操作を自動化編)
      * [スマホの設定](#スマホの設定)
      * [adbコマンドの確認](#adbコマンドの確認)
         * [touchscreen](#touchscreen)
         * [swipe](#swipe)
         * [screencap](#screencap)
         * [pull](#pull)
   * [[Android] タッチの座標を確認する](#android-タッチの座標を確認する)
   * [androidの操作を自動化したときの覚書](#androidの操作を自動化したときの覚書)
      * [タップ](#タップ)
      * [スワイプ](#スワイプ)
      * [タッチイベントを拾う](#タッチイベントを拾う)
   * [Android中通過adb shell input來模擬滑動、按鍵、點選事件](#android中通過adb-shell-input來模擬滑動按鍵點選事件)
      * [input keyevent用法](#input-keyevent用法)
      * [input swipe用法](#input-swipe用法)
   * [python實現電腦操控安卓手機](#python實現電腦操控安卓手機)
      * [滑動](#滑動)
      * [長按](#長按)
      * [keyevent](#keyevent)
   * [pure-python-adb](#pure-python-adb)
   * [android_autoclicker](#android_autoclicker)
   * [py-scrcpy](#py-scrcpy)
   * [Naive Scrcpy Client](#naive-scrcpy-client)
   * [Certificate-tool-Android](#certificate-tool-android)
      * [Installation on Windows:](#installation-on-windows)
      * [Installation on Linux:](#installation-on-linux)
   * [python-devices](#python-devices)
   * [frida-android-helper](#frida-android-helper)
   * [daemon not running 5037](#daemon-not-running-5037)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose  
Take note about adb shell

# pythonでスマホゲーム自動化~PCからandroidの操作を自動化編~
[pythonでスマホゲーム自動化~PCからandroidの操作を自動化編~ updated at 2021-05-02](https://qiita.com/m_tani_july/items/6691bc590693c3cf65cb)

## スマホの設定 
USBデバッグをONにし，adbコマンドを許可する．
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F259285%2F4dfecc23-d41b-735b-e4b4-930e3f99cc74.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=8ad9789f1c2aee250887cbc000cbaedf" width="300" height="500">  

## adbコマンドの確認 
### touchscreen  
```
>adb shell input touchscreen tap 330 600
```

### swipe
```
adb shell input swipe 50 50 500 500
```

### screencap
```
adb shell screencap -p /sdcard/screen.png
```

### pull
```
adb pull /sdcard/screen.png
```


# [Android] タッチの座標を確認する 
[[Android] タッチの座標を確認する updated at 2019-11-13](https://qiita.com/takeoverjp/items/69c89d300b50b8fe4367)
タッチの座標をお手軽に確認する方法の紹介。
input tapするときの座標を確認するときに便利。
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F37714%2Ff25e647e-e8d7-e336-0c65-5e640c02eb34.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=acaf4edd6b8b75bd47d65e279f610a43" width="300" height="500">  

開発者オプションの"Pointer location"機能を有効にすることで、
画面上部にタッチイベントの詳細が表示される。

タッチ数・座標・測度・強さ・大きさおよび、タッチの軌跡が確認できる。
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F37714%2F34637aa5-b7a4-a6a3-b962-36570deaef0c.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=699f4de6ceb757529474aa8f4c1f6357" width="600" height="50">  

"Pointer Location"機能は、adbでも制御できる。
```
# Pointer Locationを有効化
adb shell settings put system pointer_location 1

# Pointer Locationを無効化
adb shell settings put system pointer_location 0
```


# androidの操作を自動化したときの覚書
[androidの操作を自動化したときの覚書 updated at 2016-03-07](https://qiita.com/techno-tanoC/items/b93723618a792c7096ee)

## タップ
```
adb shell input touchscreen tap x y
```

## スワイプ
```
adb shell input swipe x1 y1 x2 y2
```

## タッチイベントを拾う
```
adb shell getevent /dev/input/event0
```

# Android中通過adb shell input來模擬滑動、按鍵、點選事件
[Android中通過adb shell input來模擬滑動、按鍵、點選事件 2018.06.08](https://codertw.com/ios/59189/)

## input keyevent用法
```
input keyevent 3    // Home 

input keyevent 4    // Back 

input keyevent 19  //Up 

input keyevent 20  //Down 

input keyevent 21  //Left 

input keyevent 22  //Right 

input keyevent 23  //Select/Ok 

input keyevent 24  //Volume 

input keyevent 25  // Volume- 

input keyevent 82  // Menu 選單
```

## input swipe用法
input swipe模擬的是滑動事件，
input swipe <x1> <y1> <x2> <y2> [duration(ms)] (Default: touchscreen)，需要將起始的座標傳進去。
```
如下面程式碼，將會向左滑動

shell@lentk6735_66t_l1:/ $ input swipe 600 800 300 800  
```

```
如下面程式碼，將會向右滑動

shell@lentk6735_66t_l1:/ $ input swipe 300 800 600 800  
```


# python實現電腦操控安卓手機  
[python實現電腦操控安卓手機 Posted on 2021-05-21](https://walkonnet.com/archives/98199)

## 滑動
adb shell input swipe x1 y1 x2 y2 
adb input touchscreen swipe x1 y1 x2 y2 100

```
adb shell input swipe 100 100 400 100  300 #左往右
adb shell input swipe 400 100 100 100  300 #右往左
adb shell input swipe 100 100 100 400  300 #上往下
adb shell input swipe 100 400 100 100  300 #下往上
adb shell input swipe 100 100 400 400  300 #上往下斜
adb shell input swipe 400 400 100 100  300 #下往上斜
```

## 長按
```
adb shell input swipe 100 100 100 100  1000 //在 100 100 位置長按 1000毫秒

adb shell input swipe 367 469 367 469 800
```

## keyevent
```
adb shell input keyevent 20 #向下

adb shell input keyevent 4 #返回

adb shell input keyevent 3 #Home

adb shell input keyevent 6 #掛機

adb shell input keyevent 84 #搜索

adb shell input keyevent 26 #電源

adb shell input keyevent 24 #音量+

adb shell input keyevent 25 #音量-
```


# pure-python-adb 
[pure-python-adb](https://github.com/Swind/pure-python-adb)
```
This is pure-python implementation of the ADB client.
You can use it to communicate with adb server (not the adb daemon on the device/emulator).
When you use adb command
```

When you use adb command:
<img src="https://raw.githubusercontent.com/Swind/pure-python-adb/master/docs/adb_cli.png" width="600" height="200">  

Now you can use pure-python-adb to connect to adb server as adb command line:
<img src="https://raw.githubusercontent.com/Swind/pure-python-adb/master/docs/adb_pure_python_adb.png" width="600" height="200">  

# android_autoclicker
[android_autoclicker](https://github.com/JKookaburra/android_autoclicker)
```
An autoclicker for android using a scrcpy over USB

Add "screpy-server.jar" to assets/server/

Add "AdbWinUsbApi.dll", "AdbWinApi.dll", "adb.exe" to assets/adb/
```


# py-scrcpy
[Allong12 / py-scrcpy](https://github.com/Allong12/py-scrcpy/blob/master/scrcpy_client.py)

```
A client implementation of the Android interfacing SCRCPY project, completely in Python!
```


# Naive Scrcpy Client
[LostXine / naive-scrcpy-client](https://github.com/LostXine/naive-scrcpy-client)
```
Dependence

   Android Debug Bridge
   ffmpeg shared libraries
   opencv-pythons (for GUI)
```

```
To Start

   Install OpenCV for Python. Naive Scrcpy Client use OpenCV for GUI. You can replace it with PIL or anything else easily.

   pip install opencv-python

   Copy/link recent ffmpeg shared libraries to ./lib, the required files were listed below. Make sure the version of libs matches to the architecture of your Python (e.g. x86->32bit).
   
   Windows:

   avcodec-58.dll
   avformat-58.dll
   avutil-56.dll
   swresample-3.dll

   Linux:

   libavcodec.so
   libavformat.so
   libavutil.so
   libswresample.so

   Get ADB ready on your PC and leave USB Debug Mode open on your phone.

   Let's rock!

   python run_client.py

   Check config in run_client.py for more information.
```


# Certificate-tool-Android
[Certificate-tool-Android](https://github.com/orilevicyber/Certificate-tool-Android-)
```
How to install at windows Link Video:
https://www.youtube.com/watch?v=30FrWXM03ao

The recommended version for Python 3 is 3.10.x
python 3.10.2 link download: https://www.python.org/downloads/release/python-3102/
```

## Installation on Windows:
```
Install openssl and then insert it into environment variables
C:\Program Files\OpenSSL-Win64\bin

link download: https://slproweb.com/download/Win64OpenSSL-3_0_2.exe

Installation on Windows:
pip install -r requirements.txt
```

## Installation on Linux:
```
How to install at Linux Link Video:

https://youtu.be/z_aTVYuNrEM

Installation on Linux:
git clone https://github.com/orilevicyber/Certificate-tool-Android-.git

pip install -r requirements.txt
```

# python-devices
[ maslyankov /python-devices](https://github.com/maslyankov/python-devices)
```
Python Package for interfacing with devices such as: 
Android Devices (via adb), USB Camera devices 
```

# frida-android-helper
[minhgalaxy /frida-android-helper](https://github.com/minhgalaxy/frida-android-helper)
```
This is a modified version of Frida Android Helper to compatible with LDPlayer.

It uses pure-python-adb to interface with the ADB server.
```

# daemon not running 5037 
[Android Stduio4.1.1中一次性解决不能识别真机的问题 2021-01-20](https://baijiahao.baidu.com/s?id=1686877409865440541&wfr=spider&for=pc)

## Add Environment Variable  
<img src="https://pics0.baidu.com/feed/78310a55b319ebc4af3e3652011123fb1f171671.png@f_auto?token=60e4dca1440f381d0cf5468ab97bfa66&s=5498CC328D6A4520044831DA0300C0B2" width="600" height="200">  



* []()  
![alt tag]()  
<img src="" width="400" height="500">  

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


