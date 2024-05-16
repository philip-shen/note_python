# note_google_spreadsheet
Take some note of google_spreadsheet in python

# Table of Contents

   * [note_google_spreadsheet](#note_google_spreadsheet)
   * [Table of Content](#table-of-content)
   * [PythonでGoogleDriveへアクセス](#pythonでgoogledriveへアクセス)
      * [（APIキー、OAuth2.0）について](#apiキーoauth20について)
         * [1. APIキー](#1-apiキー)
         * [2. OAuth2](#2-oauth2)
   * [PythonでGoogleDriveへアクセス](#pythonでgoogledriveへアクセス-1)
   * [PythonからOAuth2.0を利用してスプレッドシートにアクセスする](#pythonからoauth20を利用してスプレッドシートにアクセスする)
      * [OAuth2.0での認証方法](#oauth20での認証方法)
         * [1. Drive APIの有効化](#1-drive-apiの有効化)
         * [2. OAuth用クライアントIDの作成](#2-oauth用クライアントidの作成)
         * [3. スプレッドシートの共有設定](#3-スプレッドシートの共有設定)
         * [4. ソースコード](#4-ソースコード)
      * [遭遇したエラー](#遭遇したエラー)
         * [PKCS12 format is not supported by the PyCrypto library.](#pkcs12-format-is-not-supported-by-the-pycrypto-library)
         * [対応](#対応)
   * [Python で Google Spreadsheets (など)の無人操作](#python-で-google-spreadsheets-などの無人操作)
      * [プロジェクトとサービスアカウント](#プロジェクトとサービスアカウント) 
   * [Google Spread Sheet by gspread library](#google-spread-sheet-by-gspread-library)   
      * [PreRequirement](#prerequirement)
         * [default python version 3.10](#default-python-version-3.10)
         * [Execute setup.bat to setup virtualenv](#execute-setup.bat-to-setup-virtualenv)
      * [Google Spread Sheets prepation for Python](#google-spread-sheets-prepation-for-python)
         * [1. New project steup](#1-new-project-steup)
         * [2. Google Drive API activation](#2-google-drive-api-activation)
         * [3. Google Spread Sheets API activation](#3-google-spread-sheets-api-activation)
         * [4. Credentilas setup](#4-credentilas-setup)
         * [5. Private Key setup (json format)](#5-private-key-setup-json-format)
      * [Google Spread Sheets setup for Python access](#google-spread-sheets-setup-for-python-access)
         * [1. Google Spread Sheet share setup](#1-google-spread-sheet-share-setup)
         * [2. Google Spread Sheet key acquire](#2-google-spread-sheet-key-acquire)
         * [3. Python coding](#3-python-coding)
      * [Reference](#reference)
   * [Reference](#reference-1)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# PythonでGoogleDriveへアクセス 
[PythonでGoogleDriveへアクセス 2022-03-26](https://qiita.com/yo16/items/2824bacf144c6c190e57)

## （APIキー、OAuth2.0）について  
### 1. APIキー
```
APIキーは、Google Driveでは使えないようです。
ログインせずに誰でも使えるサービス用の簡単なアクセス制御用なので。
使う場面は例えば Google Map とかでは使えるようです。

とはいえ、Google Driveのフォルダを「リンクを知っている人は編集可能」な状態でシェアすれば使えるかなーと思ってみたりしたのですが、ダメでした。

なおGoogle DriveのAPIの認証のところで、OAuth2かサービスアカウントが使えますよーとしっかり丁寧に書いてあるんですが、それは後からわかった話ということで。。
```

### 2. OAuth2
```
OAuth2は、使用するユーザーが、例えば「このサービスをyo16が使いますよ」と名乗ってその人なりの権限で操作する、
というものです。つまり広くログインせず使うサービスの場合は適さないです。

技術的には、OAuth2認証してGoogle Driveへのアクセスをする実装をすると、
認証が必要な場面になると Googleのどのアカウントでこのサービスを使いますか？ という確認ダイアログが出ました。
```


# PythonでGoogleDriveへアクセス
[PythonでGoogleDriveへアクセス posted at 2020-01-06](https://qiita.com/user0/items/c4a4846b66421e7408ed)

client_secrets.jsonファイルが必要
```
{
  "installed": {
    "client_id": "ここにclient_IDを記述する",
    "project_id": "mapapp-1350",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "ここにclient_secretを記述する",
    "redirect_uris": [
      "urn:ietf:wg:oauth:2.0:oob",
      "http://localhost"
    ]
  }
}
```


# PythonからOAuth2.0を利用してスプレッドシートにアクセスする
[PythonからOAuth2.0を利用してスプレッドシートにアクセスする updated at 2015-06-06](https://qiita.com/koyopro/items/d8d56f69f863f07e9378)

## OAuth2.0での認証方法
### 1. Drive APIの有効化

### 2. OAuth用クライアントIDの作成
同じくDevelopers Consoleでプロジェクトを開いた画面で、左側のメニューから「認証情報」を選択。

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F62874%2F0d207395-6a00-87bc-8683-4045fa1ec07e.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=7d5f031f71505b791db4124153a8f58c" width="400" height="300">  

「新しいクライアントIDを作成」

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F62874%2Fd2ca1675-0059-d1eb-fed3-dc36603d1d7f.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=f17f70a1bdbb8e8ed896c1bfd1ec465d" width="500" height="300">  


「サービス アカウント」を選んで「クライアントIDを作成」

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F62874%2F696728e8-e191-994b-a45f-0e4d2aa308d7.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=75377e25d5639e8546441cd800bec906" width="600" height="300">  

ローカルにjsonファイルがダウンロードされ、完了のダイアログが表示される。
(今回の手順ではこのjsonファイルは利用しない)

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F62874%2Fd9649b58-d78c-db75-596a-538a334af0f0.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=1106d9a1ed735d3890609cdaa8e5acfe" width="300" height="300">  

クライアントIDが発行されたことを確認。
「新しいP12キーを生成」を選び、秘密鍵(.p12)をダウンロードする。

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F62874%2Fdb733fc6-ba67-9e96-afef-d04215b80438.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=0239d9c1b60447a65c425590c0e6a4b8" width="500" height="200">  


秘密鍵がローカルに保存された。(保存された秘密鍵を「MyProject.p12」とする)

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F62874%2F1fdd9b71-97ae-f0cc-09a2-578e4131519d.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=e7a9686516621e4ed376b1ceb985cd4d" width="200" height="300">  

### 3. スプレッドシートの共有設定

### 4. ソースコード
```
oauth2.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oauth2client.client import SignedJwtAssertionCredentials
import gdata.spreadsheets.client

# 認証に必要な情報
client_email = "123456789000-abc123def456@developer.gserviceaccount.com" # 手順2で発行されたメールアドレス
with open("MyProject.p12") as f: private_key = f.read() # 手順2で発行された秘密鍵

# 認証情報の作成
scope = ["https://spreadsheets.google.com/feeds"]
credentials = SignedJwtAssertionCredentials(client_email, private_key,
    scope=scope)

# スプレッドシート用クライアントの準備
client = gdata.spreadsheets.client.SpreadsheetsClient()

# OAuth2.0での認証設定
auth_token = gdata.gauth.OAuth2TokenFromCredentials(credentials)
auth_token.authorize(client)

# ---- これでライブラリを利用してスプレッドシートにアクセスできる ---- #

# ワークシートの取得
sheets = client.get_worksheets("1TAVVsyhCM_nprkpa0-LGWBheaXt_ipX84fIIhJw2fa0") # スプレッドシートIDを指定
for sheet in sheets.entry:
    print sheet.get_worksheet_id(), sheet.title

```


## 遭遇したエラー
### PKCS12 format is not supported by the PyCrypto library.

```
PKCS12 format is not supported by the PyCrypto library.
Try converting to a "PEM" (openssl pkcs12 -in xxxxx.p12 -nodes -nocerts > privatekey.pem) or using PyOpenSSL if native code is an option.
```

```
with open("MyProject.p12") as f
```

### 対応

エラー文に載っているようにして秘密鍵の形式を変更すればよい。

```
$ openssl pkcs12 -in MyProject.p12 -nodes -nocerts > MyProject.pem
Enter Import Password: #「notasecret」と入力
```

それからコード中で読み込むファイルを変える。
```
with open("MyProject.p12") as f
```

[python - Using Spreadsheet API OAuth2 with Certificate Authentication - Stack Overflow](http://stackoverflow.com/questions/20209178/using-spreadsheet-api-oauth2-with-certificate-authentication/20211057#20211057)

[]()

# Python で Google Spreadsheets (など)の無人操作
[Python で Google Spreadsheets (など)の無人操作 updated at 2020-03-28](https://qiita.com/yagshi/items/3ab2a03b5e55181ec300)

```
    Google Spreadsheets の表を Python プログラムを使って無人操作する方法を書きました。

    公式 Quick Start は人間が介在する OAuth2 のやり方だけど、ようはこれの無人版です。

    サービスアカウントというものを作って、それに必要な権限を与え、そのアカウントの秘密鍵を使ってアクセスします。
```

## プロジェクトとサービスアカウント

```
各種ドキュメントを操作するには当然権限が必要です。プログラムから操作する場合は、大雑把に行って2とおりの権限獲得の手法があります。

    一時的に人間の許可を得て、その人間のアカウントで操作
    権限を与えられた 機械ようのアカウント で操作

ざっくり言うと前者はインタラクティヴなソフトで使う方法で、後者は自動化システムで使う方法です。
今回は後者の方法を使います。ここで「機械ようのアカウント」を サービスアカウントと言います。
つまり、まずはサービスアカウントを作り、必要な権限を与える必要がります。だいたい以下の手順です。
```

```
   1. GCPのコンソール に行って、プロジェクトを作ります。
   
   2. GCPの左上のハンバーガーメニュー > IAMと管理 > サービスアカウント > サービスアカウントを作成
   
   3. 入力は必須項目だけで良いと思います。name@project.iam.gserviceaccount.com というアカウントができます。
   
   4. アカウントを作ると秘密鍵 (private key) をダウンロードできると思います。JSON形式でダウンロードしてください。
   
   5. このアカウントに対して、操作したいファイル(スプレッドシート)の操作権限を与えてください(=共有してください)。
        与え方は通常の人間向けの権限操作といっしょです。
   
   6. ハンバーガーメニュー > APIとサービス > ダッシュボード > +APIとサービスを有効化 と進み、
        Google Sheets API を有効化してください。
```


# Google Spread Sheet by gspread library 

## PreRequirement  
### default python version 3.10  
### Execute setup.bat to setup virtualenv  

## Google Spread Sheets prepation for Python  
### 1. New project steup
### 2. Google Drive API activation  
### 3. Google Spread Sheets API activation  
### 4. Credentilas setup  
### 5. Private Key setup (json format)  

## 
## Google Spread Sheets setup for Python access  
### 1. Google Spread Sheet share setup  
### 2. Google Spread Sheet key acquire  
```
https://docs.google.com/spreadsheets/d/aaaaaaaaaaaaaa/edit#gid=0
```
### 3. Python coding  
[gspread_simple.py](gspread/gspread_simple.py) 
[gspread_update.py](gspread/gspread_update.py)

## Reference  
[Google Spread Sheets に Pythonを用いてアクセスしてみた 2020-08-02](https://qiita.com/164kondo/items/eec4d1d8fd7648217935)  
[【もう迷わない】Pythonでスプレッドシートに読み書きする初期設定まとめ](https://tanuhack.com/operate-spreadsheet/)  
[gspreadライブラリの使い方まとめ！Pythonでスプレッドシートを操作する](https://tanuhack.com/library-gspread/#i-9)  
[For Bots: Using Service Account](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account)  
[For End Users: Using OAuth Client ID](https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id)  

[pythonでGoogle Spread Sheetをいじる(OAuth)](https://qiita.com/AAkira/items/22719cbbd41b26dbd0d1)  
[Google スプレッドシートを curl で読む  2023-08-04](https://qiita.com/ekzemplaro/items/83f225b08bc4ee9739aa)  
[Pythonで多めのデータをGoogleスプレッドシートに書く時の注意点 2019-07-16](https://qiita.com/satsukiya/items/9495fd7e9549197bd327)  
[gspread_asyncio](https://gspread-asyncio.readthedocs.io/en/latest/)


# Reference
* [【Google Drive upload 教學】使用Python上傳檔案，其實不難！2020 年 5 月 27 日](https://markteaching.com/google-drive-upload/?fbclid=IwAR3YjpRc70evRU5ScLWr0qQuTrq0USP-iqt2fDDxuXoR-UaDv5MGEWk_jE0)  
```


目錄

    Python 上傳檔案到 Google Drive 三步驟
        取得 Google Drive API
        安裝Google 套件
        執行Google Drive 程式碼
        How does Python upload to Google Drive work?
    Python 上傳檔案到 Google Drive 指定資料夾
        Results of Python uploading files to Google Drive to specify folders
        Upload a file to Google Drive to specify folder code
    Python 如何上傳多個檔案 UploadFiles 到Google Drive 資料夾？
        Upload multiple files to Google Drive to specify the folder code
    Google Drive API Upload files 使用 Python thread，執行速度提升2倍
        Uploading multiple files to Google Drive – Using Thread Differences
        Thread Upload 程式碼講解
    結論
```

* [Download a spreadsheet from Google Docs using Python - Stack Overflow Nov 7, 2011](https://www.google.com/search?q=python+download+google+spreadsheet&client=firefox-b-d&ei=x6fNXP_5H4vX8QWNsZrADw&start=0&sa=N&ved=0ahUKEwi_-fDqkILiAhWLa7wKHY2YBvg4ChDy0wMIdA&biw=1499&bih=816)  
```


In case anyone comes across this looking for a quick fix, here's another (currently) working solution that doesn't rely on the gdata client library:
```  

```
The https://github.com/burnash/gspread library is a newer, simpler way to interact with Google Spreadsheets, rather than the old answers to this that suggest the gdata library which is not only too low-level, but is also overly-complicated.

You will also need to create and download (in JSON format) a Service Account key: https://console.developers.google.com/apis/credentials/serviceaccountkey

Here's an example of how to use it:
```

* [How do i download google spreadsheet using python? Jun 14, 2018](https://stackoverflow.com/questions/50856503/how-do-i-download-google-spreadsheet-using-python) 
```
This component is useful for downloading spreadsheet using sheets API in python. Please refer to the link below to understand the end to end process.

https://github.com/Countants-Team/download-google-spreadsheet-using-python

```     
* [How to access Google Sheet data using the Python API and convert to Pandas dataframe Apr 28, 2018](https://towardsdatascience.com/how-to-access-google-sheet-data-using-the-python-api-and-convert-to-pandas-dataframe-5ec020564f0e)  
* [How to export a dataset to a Google Spreadsheet? Aug 2, 2015](https://www.dataiku.com/learn/guide/code/python/export-a-dataset-to-google-spreadsheets.html)  
* [Google Sheet With Python – 碼農勤耕田– Medium Apr 24, 2018](https://medium.com/nine9devtw/google-sheet-with-python-1-21268dd68773)  
* [[系列活動] Python 爬蟲實戰 - SlideShare Dec 13, 2017](https://www.slideshare.net/tw_dsconf/python-83977397)  


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

