
Table of Contents
=================

   * [Purpose](#purpose)
   * [PythonでZoomミーティングに自動出席しよう](#pythonでzoomミーティングに自動出席しよう)
   * [pywinauto の使い方メモ](#pywinauto-の使い方メモ)
      * [オンライン授業にPython Seleniumで自動出席したい！](#オンライン授業にpythonseleniumで自動出席したい)
      * [GUI-Inspect-Tool マイドキュメントのファイル一覧を取得する](#gui-inspect-tool-マイドキュメントのファイル一覧を取得する)
   * [ZOOMに自動的に接続する方法（コピペで簡単）](#zoomに自動的に接続する方法コピペで簡単)
      * [1. ミーティングIDとミーティングパスワードの取得](#1-ミーティングidとミーティングパスワードの取得)
      * [2. Batファイルの作成](#2-batファイルの作成)
      * [3. 引数つきBat](#3-引数つきbat)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents)

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



