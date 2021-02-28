Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [ドローン操作システムを作ろう（目次）](#ドローン操作システムを作ろう目次)
      * [最終的なシステム構成](#最終的なシステム構成)
      * [目次](#目次)
      * [dronekit-python を使ってみる(実機編)](#dronekit-python-を使ってみる実機編)
         * [準備するもの](#準備するもの)
   * [Google Homeに話しかけてドローンを音声操作してみる](#google-homeに話しかけてドローンを音声操作してみる)
   * [Tello Eduを用いたPythonプログラミング教育支援環境（SDK2対応，改訂版）](#tello-eduを用いたpythonプログラミング教育支援環境sdk2対応改訂版)
      * [実行環境](#実行環境)
      * [Source Code](#source-code)
   * [トイドローンTelloをPython3で制御する](#トイドローンtelloをpython3で制御する)
      * [動作環境](#動作環境)
      * [大きな変更点](#大きな変更点)
         * [tello3.pyとstats3.pyについて](#tello3pyとstats3pyについて)
         * [tello_test3.pyについて](#tello_test3pyについて)
   * [Tello Eduをpythonで動かそう！（SDK2対応）](#tello-eduをpythonで動かそうsdk2対応)
      * [gotello関数の内部で使える命令（コマンド）](#gotello関数の内部で使える命令コマンド)
   * [トイドローン Tello をプログラミングで機能拡張！顔認識と自動追尾を実装してみた](#トイドローン-tello-をプログラミングで機能拡張顔認識と自動追尾を実装してみた)
      * [動作確認環境](#動作確認環境)
      * [Source Code](#source-code-1)
      * [参考](#参考)
   * [DJI Tello 設定教學](#dji-tello-設定教學)
      * [(1)手機下載Tello的APP](#1手機下載tello的app)
      * [(2)按一下Tello的電源鍵。](#2按一下tello的電源鍵)
      * [(3)開啟手機wifi，收尋Tello字樣的訊號，連接。](#3開啟手機wifi收尋tello字樣的訊號連接)
      * [(4)出現前鏡頭的畫面後，表示你可以控制Tello了。](#4出現前鏡頭的畫面後表示你可以控制tello了)
      * [電腦與空拍機的連線](#電腦與空拍機的連線)
         * [DJI Tello 內建的方式是可以用wifi的連接](#dji-tello-內建的方式是可以用wifi的連接)
         * [Tello的插件(另外要有python latest(2.7 or 3.7))](#tello的插件另外要有python-latest27-or-37)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose  
Take some note of Drone


# ドローン操作システムを作ろう（目次）  
[ドローン操作システムを作ろう（目次） updated at 2020-04-03](https://qiita.com/hsgucci/items/86eedb5555b4234ee0e7)  

## 最終的なシステム構成  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F256470%2Ff51f0b3b-eb72-1b0e-9b8f-a2a9e62ed617.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=1f5abc4b8e1b43f823bca2b1b4c41d1e" width="500" height="500">  

## 目次  
* 01[dronekit-python を使ってみる SITL編](https://qiita.com/hsgucci/items/27fa33d7c7de505839da)
* 02[補足：dronekitのサンプルプログラム](https://qiita.com/hsgucci/items/5f16bd161d1fb9c5683f)
* 03[dronekit-python を使ってみる 実機編](https://qiita.com/hsgucci/items/e72ef6c172b9d2e62d72)
* 04[ドローンを動かす SITL編](https://qiita.com/hsgucci/items/c795cb1e66879ccfe755)
* 05[ドローン操作システムの概要](https://qiita.com/hsgucci/items/ef6c6adc87f9c7b4443c)
* 06[ドローンを動かす 実機・Raspberry Pi編](https://qiita.com/hsgucci/items/7af8da302f80bf38de68)
* 07[MQTTブローカーのセットアップ](https://qiita.com/hsgucci/items/be9665bafe6e449377c9)
* 08[pythonでMQTT送受信](https://qiita.com/hsgucci/items/6461d8555ea1245ef6c2)
* 09[dronekitの情報をMQTTで送信してみる](https://qiita.com/hsgucci/items/ec3df139cfa23da4ea0a)
* 10[MQTTをWebブラウザで受信してみる](https://qiita.com/hsgucci/items/3d07e36320115c29cc9c)
* 11[地図上にドローンの位置を表示してみる](https://qiita.com/hsgucci/items/b93532a0aee0e5dabd0c)
* 12[Leafletのマーカーを変更する](https://qiita.com/hsgucci/items/c47057268af1416a18c2)
* 13[MQTTでドローンにコマンドを送る](https://qiita.com/hsgucci/items/9633099281506e8ae45b)
* 14[Webブラウザからドローンにコマンドを送る](https://qiita.com/hsgucci/items/7d9e0bd64475c15fb03b)
* 15[地図上のクリックした場所を目標地点にする](https://qiita.com/hsgucci/items/00d682b2eb49c5a411f4)
* 16[VPSで環境構築する](https://qiita.com/hsgucci/items/a7abcceb2b6d89fd85da)
* 17インターネット経由で実機ドローンを動かす

## dronekit-python を使ってみる(実機編)  
[dronekit-python を使ってみる(実機編) updated at 2019-10-03](https://qiita.com/hsgucci/items/e72ef6c172b9d2e62d72)
### 準備するもの  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F256470%2Fd48e00f4-88ae-9a21-a93a-73a2acec141b.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=c00dd7264deb233871c389254e23c32f" width="800" height="300">  



# Google Homeに話しかけてドローンを音声操作してみる  
[Google Homeに話しかけてドローンを音声操作してみる May 14, 2018](https://qiita.com/miso_develop/items/a482dc4d168ec0a33818)  

[microlinux /tello](https://github.com/microlinux/tello) 
```
The unit of distance is feet or meters. The SDK accepts distances of 1 to 500 centimeters. Realistically, this translates to .1 - 5 meters or .7 - 16.4 feet.

Tello.move_forward(distance) Tello.move_backward(distance) Tello.move_right(distance) Tello.move_left(distance) Tello.move_up(distance) Tello.move_down(distance)

Methods that rotate require a single parameter, degrees. The SDK accepts values from 1 to 360. Responses are 'OK' or 'FALSE'.
```


# Tello Eduを用いたPythonプログラミング教育支援環境（SDK2対応，改訂版）  
[Tello Eduを用いたPythonプログラミング教育支援環境（SDK2対応，改訂版）updated at 2020-02-11](https://qiita.com/yoomori/items/7e93d11fba2eadd769ce)

## 実行環境  
* python3.7.6　（注：3.8系にすると以下のパッケージが対応でいていないものもある）
* PyCharm 2019.3.2 (Community Edition)
* opencv 3.4.2
* pillow 7.0.0
* pyzbar 0.1.8
* matplotlib 3.1.1
* numpy 1.17.4

## Source Code  
[Github yoomori/PPETelloEdu](https://github.com/yoomori/PPETelloEdu)  


# トイドローンTelloをPython3で制御する  
[トイドローンTelloをPython3で制御する updated at 2020-03-06](https://qiita.com/coffiego/items/54c8bb553394590787f9) 
## 動作環境  
* Mac Mojave 10.14.5
* Python ver. 3.7.0

## 大きな変更点 
### tello3.pyとstats3.pyについて 
```
大きな変更はありませんが、
・printに()をつけた
・except socket.error, exc: -> except socket.error as exc: に変更
```

### tello_test3.pyについて  
```
こちらは結構変更しています。
もともと、tello_test.pyはcommand.txtにコマンドを入れて、
そのcommandを順にtelloに送信するという形になっています。
これでは、もともと決めた順でしかtelloを動かせません。
そのままのtello_test.pyを試したい方は以下の記事を参考にしてやってみてください。
URL: https://qiita.com/hsgucci/items/a199e021bb55572bb43d

その場でターミナルにコマンドを打って動かしたいのでinput()関数でcommandを入力してtelloに送信する仕様に変えました。
また、細かい部分でちょっと変更していますのでそこはコードを見てください。
```


# Tello Eduをpythonで動かそう！（SDK2対応）  
[Tello Eduをpythonで動かそう！（SDK2対応）updated at 2019-12-10](https://qiita.com/yoomori/items/e847166433d44ab53c29)

## gotello関数の内部で使える命令（コマンド）  
コマンド | 引数 | 説明 | 返値
------------------------------------ | --------------------------------------------- | --------------------------------------------- | ---------------------------------------------
command() | なし | Tello EduのモードをSDK2に設定最初にこのコマンドを送信する必要がある | なし
takeoff() | なし | 離陸（約1m上昇する） | なし
land() | なし | 着陸 | なし
stop() | なし | ホバリング（次のコマンドを50秒以内に送信 | なし
up(x) | x: 20cm〜200cm | 上昇 | なし
down(x) | x: 20cm〜200cm | 下降 | なし
left(x) | x: 20cm〜200cm | 左側に動く | なし
right(x) | x: 20cm〜200cm | 右側に動く | なし
forward(x) | x: 20cm〜200cm | 前進 | なし
back(x) | x: 20cm〜200cm | 後進 | なし
cw(x) | x:1度〜360度 | 時計回りに回転(Clockwise Rotation) | なし
ccw(x) | x:1度〜360度 | 反時計回りに回転(Counter Clockwise Rotation) | なし
end() | なし | すべてのコマンドを終了（一番最後に送信する必要がある） | なし
streamon() | なし | ビデオ録画開始　※録画中にget_qrcode()を呼び出さないこと | なし
streamoff() | なし | ビデオ録画終了 | なし
set_speed(x) | x:10〜100 | ドローンの動くスピードを指定 | なし
get_qrcode() | なし | QRコードを撮影して解析　※解析中にstreamon()を呼び出さないこと | 解析結果（文字列）
get_speed() | なし | ドローンに設定されてるスピード情報を得ることができる | スピード（数値：浮動小数点）
get_battery() | なし | ドローンのバッテリー残量を得ることができる | 残量（0〜100）
emergency() | なし | 緊急停止（4つのモータを停止させる | なし


# トイドローン Tello をプログラミングで機能拡張！顔認識と自動追尾を実装してみた  
[トイドローン Tello をプログラミングで機能拡張！顔認識と自動追尾を実装してみた updated at 2018-07-12](https://qiita.com/mozzio369/items/1f80103339faaedc6be3)

## 動作確認環境  
* macOS 10.12.6
* python 3.6.5
* opencv 3.4.1

## Source Code
[ mozzio369 /playtello ](https://github.com/mozzio369/playtello)  

## 参考  
[Python版OpenCVとカメラで簡易距離計測](http://opencv.blog.jp/python/%E7%B0%A1%E6%98%93%E8%B7%9D%E9%9B%A2%E8%A8%88%E6%B8%AC)   
[PythonとOpenCV 3でPCのビデオカメラでリアルタイム顔認識してみた](http://totech.hateblo.jp/entry/2017/10/22/100726)   
[OpenCVを利用したアプリ開発 顔認識](http://robinit.hatenablog.com/entry/2018/01/13/190349)   
[Python+OpenCVでWebカメラの画像中のものをトラッキングする話](http://ensekitt.hatenablog.com/entry/2017/12/21/200000)   
[OpenCV3.3.1 顔認識とトラッキングのサンプルプログラム #2](http://www.netosa.com/blog/2017/12/opencv331-2.html)   

# DJI Tello 設定教學   
[DJI Tello 設定教學 2018年3月17日 星期六](https://farmer0093.blogspot.com/2018/03/dji-tello.html)  

## (1)手機下載Tello的APP  
## (2)按一下Tello的電源鍵。  
## (3)開啟手機wifi，收尋Tello字樣的訊號，連接。  
```
空機時並沒有設定密碼，開啟後請依個人情況去設定。我建議是設定，避免人家開wifi去劫持你的飛機。
```
<img src="https://1.bp.blogspot.com/-5O-5spo00CE/WqzeT7e_C6I/AAAAAAAACJE/7dn3kPKYeBwwrAcbq3EyLiKOigTVOxGZwCK4BGAYYCw/s400/IMG_8268.jpg" width="500" height="300">  

## (4)出現前鏡頭的畫面後，表示你可以控制Tello了。

## 電腦與空拍機的連線  
[DJI Tello 的基礎操作與套件 Feb 23, 2020](https://www.coderbridge.com/series/726ee8e84edc4073aab642d1ab5965fa/posts/68c91aee8877432b9348ea69745f328a)  

### DJI Tello 內建的方式是可以用wifi的連接  
```
注意:因為圖像辨識傳輸的數據量大，訊號要強，必須使用外接wifi接收器

    裝上電池，開啟Tello(開機按鈕於機身側面)
    開機後，確認Tello 前方之LED燈是否亮起並閃爍
    使用筆電 or 手機連接wifi: TELLO-XXXXXX
```

### Tello的插件(另外要有python latest(2.7 or 3.7))  
[ hanyazou /TelloPy ](https://github.com/hanyazou/TelloPy)  



* []()  
![alt tag]()
<img src="" width="" height="">  

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


