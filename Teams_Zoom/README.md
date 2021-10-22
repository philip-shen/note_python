
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [自動でMicrosoft teamsで個人あてにチャットを送る方法](#自動でmicrosoft-teamsで個人あてにチャットを送る方法)
      * [Microsoft Teamsを操作するプログラム](#microsoft-teamsを操作するプログラム)
         * [1.Microsoft公式Teams app "Incoming Webhook"を使う。](#1microsoft公式teams-app-incoming-webhookを使う)
         * [2.Microsoft公式Tool ""Power Automate for desktop""を使う](#2microsoft公式tool-power-automate-for-desktopを使う)
         * [3.Seleniumによりブラウザを操作して、Web版teamsを操作する。  　](#3seleniumによりブラウザを操作してweb版teamsを操作する--)
      * [Chrome Driver](#chrome-driver)
      * [Web版teamsの操作](#web版teamsの操作)
   * [Teamsの個人チャットへ自動送信する（２段階認証回避）](#teamsの個人チャットへ自動送信する２段階認証回避)
      * [躓いたポイント](#躓いたポイント)
      * [seleniumでby_class_nameでスペースが入った要素が取得できずエラーになる時の対処法](#seleniumでby_class_nameでスペースが入った要素が取得できずエラーになる時の対処法)
   * [続！pyAutoGUIでリモートワークサボり隊！](#続pyautoguiでリモートワークサボり隊)
      * [Python(pyAutoGUI)を使って操作してる風にみせる](#pythonpyautoguiを使って操作してる風にみせる)
   * [MS-Teams-Automation](#ms-teams-automation)
   * [PythonでZoomミーティングに自動出席しよう](#pythonでzoomミーティングに自動出席しよう)
   * [pywinauto の使い方メモ](#pywinauto-の使い方メモ)
      * [オンライン授業にPython Seleniumで自動出席したい！](#オンライン授業にpythonseleniumで自動出席したい)
      * [GUI-Inspect-Tool マイドキュメントのファイル一覧を取得する](#gui-inspect-tool-マイドキュメントのファイル一覧を取得する)
   * [ZOOMに自動的に接続する方法（コピペで簡単）](#zoomに自動的に接続する方法コピペで簡単)
      * [1. ミーティングIDとミーティングパスワードの取得](#1-ミーティングidとミーティングパスワードの取得)
      * [2. Batファイルの作成](#2-batファイルの作成)
      * [3. 引数つきBat](#3-引数つきbat)
   * [オンライン授業にPython Seleniumで自動出席したい！](#オンライン授業にpythonseleniumで自動出席したい-1)
   * [MacでSelenum PyautoGUIを使ってZoomに自動出席](#macでselenumpyautoguiを使ってzoomに自動出席)
      * [環境](#環境)
      * [PyautoGUIについて](#pyautoguiについて)
         * [Installation_Windows](#installation_windows)
   * [python開機時自動進入google meet](#python開機時自動進入google-meet)
   * [AutoLogin-Google-Meet](#autologin-google-meet)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose  
Take note of Teams and Zoom Automation  

# 自動でMicrosoft teamsで個人あてにチャットを送る方法 
[自動でMicrosoft teamsで個人あてにチャットを送る方法 updated at 2021-10-16](https://qiita.com/grapefruit_0514/items/62e49d4d5cac7a323aeb)

## Microsoft Teamsを操作するプログラム  
### 1.Microsoft公式Teams app "Incoming Webhook"を使う。 
### 2.Microsoft公式Tool ""Power Automate for desktop""を使う
### 3.Seleniumによりブラウザを操作して、Web版teamsを操作する。  　

## Chrome Driver  
```
今回はGoogle Chromeの自動化を紹介する。Seleniumによるブラウザ操作には各ブラウザのdriverのダウンロードが必要である。以下のリンクから適当なフォルダにダウンロードして置いておこう。
```
[Chrome driver](https://chromedriver.chromium.org/downloads)
[Microsoft-edge driver](https://developer.microsoft.com/ja-jp/microsoft-edge/tools/webdriver/)

## Web版teamsの操作  
```
今回はChrome web driverを使ってWeb版TeamsをChromeで開いて操作する。
開くページのURLにチャットの相手のユーザーネームが書いてるので、複数送りたい相手がいる場合はその箇所を送りたい相手に変更する。
```

```
driver_path = r'/path/chromedriver.exe'
driver = webdriver.Chrome(executable_path = driver_path)

driver.get('https://teams.microsoft.com/dl/launcher/***' + Name +'**')
driver.maximize_window()
```

```
デスクトップアプリ版を使うかどうかアラートが出る場合があるので、例外処理でアラートへswichして"いいえ"を押す。
```

```
try:
    alert = driver.switch_to.alert
    text = alert.text
    alert.dismiss()
except:
    pass
```

```
メッセージボックスをクリックして入力可能状態にし、過去の未送信のメッセージがある場合があるのでBack Spaceで消して、送りたいメッセージを送る。
```

```
driver.find_element_by_xpath('message boxのxpath').click()
for i in range(30):
    driver.find_element_by_xpath('message boxのxpath').send_keys(Keys.BACK_SPACE)
message = """
Hello! jon
How are you doing?
Would you like to go fishing with me this weekend?
"""
driver.find_element_by_xpath('message boxのxpath').send_keys(message)
driver.find_element_by_id('send-message-button').click()
```


# Teamsの個人チャットへ自動送信する（２段階認証回避）  
[Teamsの個人チャットへ自動送信する（２段階認証回避） updated at 2021-10-05](https://qiita.com/mimuro_syunya/items/8a75397bc9c22f1c300f)

[[2] PythonのSeleniumを使って、起動済みのブラウザを操作する。](https://qiita.com/mimuro_syunya/items/2464cd2404b67ea5da56)  

[ mimuro-lab /teams_sendmsg ](https://github.com/mimuro-lab/teams_sendmsg)

## 躓いたポイント
```
xpathの取得は、chromeブラウザ上の右クリック「検証」で要素を探して（以下画像のクリックするボタン）、
コード上で右クリック「copy」からxpathを取得できます。
```

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F554112%2F4941fcf3-d02c-3011-2775-fc6ceec93a83.jpeg?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=76a25e50618ee5e99c236192b3bdbd58" width="600" height="200">

## seleniumでby_class_nameでスペースが入った要素が取得できずエラーになる時の対処法
[seleniumでby_class_nameでスペースが入った要素が取得できずエラーになる時の対処法](https://qiita.com/hanonaibaobabu/items/e547410865d857aa25ec)


# 続！pyAutoGUIでリモートワークサボり隊！
[続！pyAutoGUIでリモートワークサボり隊！ posted at 2020-10-02](https://qiita.com/pnd75/items/f0918c330ebb5b0df6ba)

## Python(pyAutoGUI)を使って操作してる風にみせる 
```
MicrosoftTeamsでは退席中表示は放置5分だったと思う。
しっかり仕事中でもそのぐらい放置することは多々ある。
その際、復帰させようとして

    マウス/タッチパネルでのカーソルの移動
    キーボード(矢印キー、タブキー)でのカーソル移動

と動かしてみると「退席中」のまま変わらない…ということが起きていた。
この時の退席中表示を確実に解除する方法はキー入力操作だ。
ということは、同じことをPythonにさせればいいんじゃないだろうか。
```

```
sample2.py

import pyautogui as pg
import time
try:
    while True:
        time.sleep(180)

        # chromeを開く
        pg.hotkey('win','r')
        pg.typewrite('chrome.exe')
        pg.press('enter')
        time.sleep(5)

        # 文字列testを検索
        pg.typewrite('test')
        pg.press('enter')
        time.sleep(5)

        # ウィンドウを閉じる
        pg.hotkey('alt','f4')

except KeyboardInterrupt:
    print('仕事しよ')
```

```
解説はソース内のコメントのとおり。
前回のマウス操作を「Chromeを開いて「test」という文字列で検索して閉じる」に変更しただけだ。
[Alt]+[F4]で別のものまで閉じないように、
それぞれの処理に待ち時間を設定している(時間は適当なので起動しながら調整してほしい)。
```

# MS-Teams-Automation  
[ayushi7rawat / MS-Teams-Automation](https://github.com/ayushi7rawat/MS-Teams-Automation)

```
Automating MS Teams with Python using PyAutoGui
```



# PythonでZoomミーティングに自動出席しよう  
[PythonでZoomミーティングに自動出席しよう Feb 26, 2021](https://qiita.com/hima_zin331/items/97fc5c9093057bb06572)  


# pywinauto の使い方メモ  
[pywinauto の使い方メモ  2020-11-13](https://qiita.com/nobu-maple/items/51901b2e27e4448f102b)  

## オンライン授業にPython+Seleniumで自動出席したい！ 
[オンライン授業にPython+Seleniumで自動出席したい！ 2021-03-06](https://qiita.com/LemniscaterN/items/80b2f8ca99c0693d42ff)  


## GUI-Inspect-Tool マイドキュメントのファイル一覧を取得する  
```
コントロール名称や階層構造などは UISPY というツールを使うと参考になる
この辺からダウンロードとか　
```
[ blackrosezy /gui-inspect-tool ](https://github.com/blackrosezy/gui-inspect-tool)  


# ZOOMに自動的に接続する方法（コピペで簡単）  
[ZOOMに自動的に接続する方法（コピペで簡単） 2020.10.06](https://blog.isarver.com/automatically-join-zoom/)

## 1. ミーティングIDとミーティングパスワードの取得  
```
https://zoom.us/j/12345678901?pwd=abcdefghijklmnopqrstuvxwzABCDEFG

赤い部分がミーティングIDで

青い部分がハッシュ化されたミーティングパスワードです
```

## 2. Batファイルの作成  
```
赤い部分がミーティングID

青い部分がハッシュ化されたミーティングパスワード

start zoommtg:”//zoom.us/join?action=join&confno=12345678901&pwd=abcdefghijklmnopqrstuvxwzABCDEFG“
```

## 3. 引数つきBat
```
@echo off
set MEETINGID=%~1
set PASSWORD=%~2
start zoommtg:"//zoom.us/join?action=join&confno=%MEETINGID%&pwd=%PASSWORD%"
```


# オンライン授業にPython+Seleniumで自動出席したい！  
[オンライン授業にPython+Seleniumで自動出席したい！ updated at 2021-03-06](https://qiita.com/LemniscaterN/items/80b2f8ca99c0693d42ff)

# MacでSelenum+PyautoGUIを使ってZoomに自動出席  
[MacでSelenum+PyautoGUIを使ってZoomに自動出席 updated at 2021-03-06](https://qiita.com/LemniscaterN/items/d137d8b0a0bb7b8af7c5)


## 環境  
```
macOS Big Sur 11.2.2
Python 3.8.6
PyautoGUI 0.9.52
Google Chrome 88.0.4324.192（Official Build） （x86_64）
```

## PyautoGUIについて  
```
今回改めて自動出席プログラムに挑戦しようと考えた最大の理由がPyautoGUIの存在です。
PyAutoGUIは、Python のモジュールの一つで、マウスやキーボード操作を自動化することが出来ます。
イメージマッチングが簡単に利用でき、クロスプラットフォームなのでMac、Windows、Linuxで利用出来ます。
```
[pyautoguiのあれこれ posted at 2020-12-15](https://qiita.com/hideto1198/items/a2e822892a27af03fe5a)  

### Installation_Windows    
[PyAutoGuiで繰り返し作業をPythonにやらせよう updated at 2021-01-05](https://qiita.com/hirohiro77/items/78e26a59c2e45a0fe4e3)  

```
C:\Python37\Scripts\pip.exe install pyautogui
```

```
Windowsの場合、COM制御系のモジュールも入れておくといいかも、ウインドウの場所が識別できるので、
ちなみに、pywin32にもwin32guiは含まれてるはずなんだけど、
Windows10だとwin32guiも単独で入れておかないとなぜかハンドリングに失敗する謎な現象が出ます(実は別物?)
※WindowsのCOMにアタッチしないのであれば、win32guiは不要でした
```

```
C:\Python37\Scripts\pip.exe install pywin32
C:\Python37\Scripts\pip.exe install win32gui
C:\Python37\Scripts\pip.exe install Image
C:\Python37\Scripts\pip.exe install pillow
C:\Python37\Scripts\pip.exe install pyscreeze
C:\Python37\Scripts\pip.exe install PyTweening
C:\Python37\Scripts\pip.exe install opencv_python
```


# python開機時自動進入google meet  
[用python開機時自動進入google meet 2021年6月1日](https://www.youtube.com/watch?v=61u8r8U5_04)
[meet.py](https://drive.google.com/file/d/1DB4XveaDmjqbkKjI6cjsyLN5n4rXT1mc/view)

# AutoLogin-Google-Meet 
[AutoLogin-Google-Meet](https://github.com.cnpmjs.org/RyzerZ/AutoLogin-Google-Meet/blob/master/login.py)


# Troubleshooting


# Reference


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
