Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [YouTube Data API](#youtube-data-api)
      * [Setup project](#setup-project)
      * [Activate API Key](#activate-api-key)
      * [Publish API Key](#publish-api-key)
      * [Search YouTube video](#search-youtube-video)
   * [Youtube Data API by Python](#youtube-data-api-by-python)
      * [OAuth認証を設定する](#oauth認証を設定する)
   * [Installation](#installation)
   * [command line](#command-line)
   * [CODEX FFMPEG](#codex-ffmpeg)
   * [ytdl-org / youtube-dl](#ytdl-org--youtube-dl)
   * [How can i find all ydl_opts](#how-can-i-find-all-ydl_opts)
   * [youtube-dl](#youtube-dl)
      * [下載 mp4 格式的影片](#下載-mp4-格式的影片)
      * [下載 mp3 檔](#下載-mp3-檔)
      * [下載不同畫質與格式](#下載不同畫質與格式)
   * [YT-Downloader](#yt-downloader)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose
Take note of Youtube related stuff


# YouTube Data API  
[YouTube Data APIの始め方  2022.02.09](https://tro555-engineer.com/2022/02/09/youtube-data-api%e3%81%ae%e5%a7%8b%e3%82%81%e6%96%b9/)
[YouTube Data API v3 を使って YouTube 動画を検索する 2021-01-11](https://qiita.com/koki_develop/items/4cd7de3898dae2c33f20#%E5%89%8D%E6%8F%90)

## Setup project  

## Activate API Key   

## Publish API Key
( ※ キーを制限しない のままでも使用できますが、基本的に API キーの用途はなるべく制限しておいた方が無難です。)

## Search YouTube video 
[Search: list](https://developers.google.com/youtube/v3/docs/search/list#apps-script)

パラメータ名 	 | 説明
------------------------------------ | --------------------------------------------- | 
key 	 | 先程発行した API キー。
type 	| 検索するリソースのタイプ。 channel, playlist, video を指定できます。今回は動画を検索するので video を指定します。 
part | レスポンスに含めるリソースのプロパティを指定します。 id, snippet を指定できます。例えば snippet を指定するとレスポンスに動画 ID だけじゃなく、タイトルや説明が含まれるようになります。今回は snippet を指定します。
q | 検索クエリ。今回は適当に dog にしておきます。

```
$ curl 'https://www.googleapis.com/youtube/v3/search?key=AIzaSyBNbBNJjMafqIP651cERFKkw_3fBC7bG_U&type=video&part=snippet&q=dog'
```

[#101 使用 YouTube Data API 抓取有趣的 Youtuber 影片 & MV Feb 8, 2020](https://medium.com/%E5%BD%BC%E5%BE%97%E6%BD%98%E7%9A%84%E8%A9%A6%E7%85%89-%E5%8B%87%E8%80%85%E7%9A%84-100-%E9%81%93-swift-ios-app-%E8%AC%8E%E9%A1%8C/101-%E4%BD%BF%E7%94%A8-youtube-data-api-%E6%8A%93%E5%8F%96%E6%9C%89%E8%B6%A3%E7%9A%84-youtuber-%E5%BD%B1%E7%89%87-mv-d05c3a0c70aa)

```
https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId=playlist的id&key=API key&maxResults=影片數量
```

```
https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId=UUMUnInmOkrWN4gof9KlhNmQ&key=Abccato&maxResults=20
```


# Youtube Data API by Python 
[Youtube Data APIとPythonを使ってYoutube Music用の音楽プレイリストを作る 2021-08-07](https://qiita.com/cazamir0/items/0b754c9aea592b322b5b)

## OAuth認証を設定する 
[APIキー、OAuthクライアントID、サービスアカウントキーの違い:Google APIs  2020-10-08](https://messefor.hatenablog.com/entry/2020/10/08/080414#%E5%8F%96%E5%BE%97%E6%96%B9%E6%B3%95-1)

No. | 必要となるもの | アクセス可能なデータ | 	誰としてアクセスするか  |  具体例  
------------------------------------ | --------------------------------------------- |--------------------------------------------- | ---------------------------------------------   | ---------------------------------------------    
1 | APIキー | 一般公開データ | 匿名ユーザ | YouTubeにある動画をアプリケーション経由で検索する
2 | OAuth2.0クライアトID | 一般公開データ/ユーザーデータ | ユーザアカウント | あるユーザ（エンドユーザ）の代わりにユーザのGoogleドライブにアプリケーションを経由でデータを保存
3 | サービスアカウントキー | 一般公開データ/ユーザーデータ | サービスアカウント | 共同作業メンバのGoogleカレンダー情報にアプリケーションを経由してアクセスする 

PythonからOAuthクレデンシャルを使ってYouTubeのplaylistAPIを使うサンプルコードを掲載します。
以下はOAuth認証用の関数を定義をしています。この関数を使ってOAuth認証をし、その後ユーザデータにアクセスします。
今回はYouTubeに自分用の再生リストを作成したいと思います。実行のコードを下部にあります。 

```
'''OAuth認証用の関数'''
import os
import pickle

import numpy as np
import pandas as pd

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_credentials(client_secret_file, scopes,
                    token_storage_pkl='token.pickle'):
    '''google_auth_oauthlibを利用してOAuth2認証

        下記URLのコードをほぼそのまま利用。Apache 2.0
        https://developers.google.com/drive/api/v3/quickstart/python#step_1_turn_on_the_api_name
    '''
    creds = None
    # token.pickleファイルにユーザのアクセス情報とトークンが保存される
    # ファイルは初回の認証フローで自動的に作成される
    if os.path.exists(token_storage_pkl):
        with open(token_storage_pkl, 'rb') as token:
            creds = pickle.load(token)

    # 有効なクレデンシャルがなければ、ユーザーにログインしてもらう
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, scopes=scopes)
            creds = flow.run_local_server(port=0)

        # クレデンシャルを保存（次回以降の認証のため）
        with open(token_storage_pkl, 'wb') as token:
            pickle.dump(creds, token)

    return creds
```

以下のコードのCLIENT_SECRET_FILEに先程ダウンロードしたJSONを指定してください。
これを実行するとまずOAuth認証のためにブラウザが立ち上がり利用者にGoogleアカウントでのログインを求めます。 
認証が終わると「再生リストテスト」という名で空の再生リストが作成されます。

```
'''OAuth認証と再生リストの作成'''
# 利用するAPIサービス
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# OAuthのスコープとクレデンシャルファイル
YOUTUBE_READ_WRITE_SCOPE = 'https://www.googleapis.com/auth/youtube'
CLIENT_SECRET_FILE = 'client_secret.json'

# OAuth認証：クレデンシャルを作成
creds = get_credentials(
                    client_secret_file=CLIENT_SECRET_FILE,
                    scopes=YOUTUBE_READ_WRITE_SCOPE
                    )

# API のビルドと初期化
youtube_auth = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    credentials=creds)

# Add Playlist
# This code creates a new, private playlist in the authorized user's channel.
playlists_insert_response = youtube_auth.playlists().insert(
  part="snippet,status",
  body=dict(
    snippet=dict(
      title='再生リストテスト',
      description='APIで作成したプレイリスト'
    ),
    status=dict(
      privacyStatus="private"
    )
  )
).execute()
```

[Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python#step_3_set_up_the_sample)

# Installation  
```
沒特別裝管控pkg的話 .. 
通常虛擬環境會在
C:\Users\windows user\Envs
```

```
將ffmpeg的full包的bin資料夾下 3個exe
，放進去剛建立的環境內Scripts分類下
```


# command line
```
youtube-dl --extract-audio --audio-format wav  https://www.youtube.com/watch?v=3FBijeNg_Gs
```

# CODEX FFMPEG  
[CODEX FFMPEG](https://www.gyan.dev/ffmpeg/builds/)


#  ytdl-org / youtube-dl 
[ ytdl-org /youtube-dl ](https://github.com/ytdl-org/youtube-dl)


# How can i find all ydl_opts 
[How can i find all ydl_opts](https://stackoverflow.com/questions/38658046/how-can-i-find-all-ydl-opts)

All options for the Python Module are listed in [YoutubeDL.py](https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278)


# youtube-dl
[youtube-dl](https://ianwu.tw/press/topic/command_line_program/youtube-dl)

## 下載 mp4 格式的影片  
```
預設的下載格式是 webm (opens new window)，
如果要下載 mp4 格式可以用 -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' 指定聲音與影像的格式
```

```
youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' https://www.youtube.com/watch?v=rkAfWfZkfyo
```

## 下載 mp3 檔
```
youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=rkAfWfZkfyo
```


## 下載不同畫質與格式 
```
youtube-dl -F https://www.youtube.com/watch?v=rkAfWfZkfyo  
```


[](html#%E4%B8%8B%E8%BC%89-mp4-%E6%A0%BC%E5%BC%8F%E7%9A%84%E5%BD%B1%E7%89%87)


# YT-Downloader  
[YT-Downloader](https://github.com/Will-Bee/YT-Downloader)
```
Script for downloading mp3 files from youtube
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

No. | Test Name 
------------------------------------ | --------------------------------------------- | 
001 | Two Sum


