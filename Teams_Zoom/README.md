
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
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




