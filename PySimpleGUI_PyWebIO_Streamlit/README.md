Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Pythonでも簡単にGUIは作れる](#pythonでも簡単にguiは作れる)
      * [GUIを作ってみる](#guiを作ってみる)
   * [PySimpleGUIを使ってプレゼン用カウントダウンタイマーを作った](#pysimpleguiを使ってプレゼン用カウントダウンタイマーを作った)
      * [subterraneananimism/timer](#subterraneananimismtimer)
      * [効果音ラボ](#効果音ラボ)
   * [async-desktop-chat](#async-desktop-chat)
   * [Animated-Popup](#animated-popup)
   * [Bitcoin-wallet-cracker](#bitcoin-wallet-cracker)
   * [PySimpleGuiで入力に応じてグラフを表示・更新する](#pysimpleguiで入力に応じてグラフを表示更新する)
   * [Python画像処理のためのGUI入門（PySimpleGUI解説）](#python画像処理のためのgui入門pysimplegui解説)
   * [「PyWebIO」があればPython 100\xでWebアプリ作れるってマジ！？](#pywebioがあればpython-100でwebアプリ作れるってマジ)
   * [Python PySimpleGUIで作るPDFリーダー](#python-pysimpleguiで作るpdfリーダー)
      * [PySimpleGUI/DemoPrograms/Demo_PDF_Viewer.py](#pysimpleguidemoprogramsdemo_pdf_viewerpy)
      * [How do I resolve "No module named 'frontend'" error message?](#how-do-i-resolve-no-module-named-frontend-error-message)
   * [PySimpleGuiでTrelloを操作する](#pysimpleguiでtrelloを操作する)
   * [WebSocket Client](#websocket-client)
      * [websocket-client](#websocket-client-1)
         * [Long-lived Connection](#long-lived-connection)
   * [Websocket GUI Debug Tool比較](#websocket-gui-debug-tool比較)
      * [Browser WebSocket Client](#browser-websocket-client)
   * [Streamlit vs PyWebIO Webフレームワーク対決！](#streamlit-vs-pywebio-webフレームワーク対決)
      * [Streamlit](#streamlit)
      * [コード実行](#コード実行)
         * [Streamlit](#streamlit-1)
         * [PyWebIO](#pywebio)
      * [画面遷移](#画面遷移)
         * [Streamlit](#streamlit-2)
      * [データ可視化](#データ可視化)
         * [Streamlit](#streamlit-3)
   * [streamlitで遊ぼう！](#streamlitで遊ぼう)
   * [Streamlitで爆速アプリ開発](#streamlitで爆速アプリ開発)
      * [デプロイもできちゃう](#デプロイもできちゃう)
   * [【Python】LINEのグルチャ履歴をヌルヌル動くグラフにしてみた～原理からWebアプリ化まで～](#pythonlineのグルチャ履歴をヌルヌル動くグラフにしてみた原理からwebアプリ化まで)
   * [Streamlitで作成した株価アプリをWEB公開した（キャッシュ説明あり）](#streamlitで作成した株価アプリをweb公開したキャッシュ説明あり)
      * [キャッシュ化](#キャッシュ化)
      * [Docker環境準備](#docker環境準備)
   * [PyCaretとStreamlitでAutoMLのGUIツールをさくっと作ってみる](#pycaretとstreamlitでautomlのguiツールをさくっと作ってみる)
   * [【Streamlit】JavaScriptが嫌いだからPythonだけでWebアプリをつくる](#streamlitjavascriptが嫌いだからpythonだけでwebアプリをつくる)
      * [WEBUIを使ってインタラクティブなアプリにする](#webuiを使ってインタラクティブなアプリにする)
   * [Streamlit極簡易的Dashboard開發 - Neutron](#streamlit極簡易的dashboard開發---neutron)
      * [Streamlit 概念](#streamlit-概念)
   * [Streamlitを用いた音響信号処理ダッシュボードの開発(Tokyo BISH Bash #03発表資料)](#streamlitを用いた音響信号処理ダッシュボードの開発tokyo-bish-bash-03発表資料)
   * [Python: Streamlit を使って手早く WebUI 付きのプロトタイプを作る](#python-streamlit-を使って手早く-webui-付きのプロトタイプを作る)
      * [Column](#column)
      * [container](#container)
      * [Expander](#expander)
      * [Sidebar](#sidebar)
      * [Help](#help)
      * [単一のスクリプトで複数のアプリケーションを扱う](#単一のスクリプトで複数のアプリケーションを扱う)
      * [Argparse](#argparse)
      * [Click](#click)
   * [【Streamlit】株価データのお手軽GUI分析](#streamlit株価データのお手軽gui分析)
   * [cdsdashboards](#cdsdashboards)
   * [Streamlit Offical API](#streamlit-offical-api)
   * [GUI Console](#gui-console)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of Webscreenshoot  

# Pythonでも簡単にGUIは作れる
[Pythonでも簡単にGUIは作れる posted at Aug 23, 2020](https://qiita.com/konitech913/items/61dc715ddaad54505a29)

## GUIを作ってみる
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F634673%2F937af746-1be8-8813-63da-63bfc612ca0f.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=e4778b46a02aa37871bcd347ad563c4a" width="500" height="600">  

```

```

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F634673%2Ff9dba0c5-405a-7402-c805-893433177cc5.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=8674caa7e9170a508ca59230327b16ab" width="500" height="600">

# PySimpleGUIを使ってプレゼン用カウントダウンタイマーを作った  
[PySimpleGUIを使ってプレゼン用カウントダウンタイマーを作った Feb 14, 2021](https://qiita.com/nemous_nuke/items/8ddd0a4290209410d25d)

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1107922%2F6da80b25-ca45-f16f-2903-1b11bf47287e.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=9c4489b12069b51dcc46928316876675" width="600" height="400">

## subterraneananimism/timer  
[subterraneananimism/timer](https://github.com/subterraneananimism/timer/blob/main/timer_nosound.py)   

## 効果音ラボ  
次のフリー効果音素材サイトにアラーム音あり  
[効果音ラボ](https://soundeffect-lab.info/sound/machine/machine2.html)

# async-desktop-chat  
[async-desktop-chat](https://github.com/nngogol/async-desktop-chat)  

<img src="https://user-images.githubusercontent.com/46163555/81684482-ffd36900-9424-11ea-9ef1-a6015de75e28.gif" width="800" height="600">  

<img src="https://raw.githubusercontent.com/nngogol/async-desktop-chat/master/diagram.jpg" width="400" height="500">  

<img src="https://raw.githubusercontent.com/nngogol/async-desktop-chat/master/diagrams/output/en.diagram-start.svg.png" width="600" height="500">  

<img src="https://raw.githubusercontent.com/nngogol/async-desktop-chat/master/diagrams/output/en.diagram2_1.svg.png" width="600" height="500">  

<img src="https://raw.githubusercontent.com/nngogol/async-desktop-chat/master/diagrams/output/en.diagram2_2.svg.png" width="600" height="500">  

<img src="https://raw.githubusercontent.com/nngogol/async-desktop-chat/master/diagrams/output/en.diagram2_3.svg.png" width="600" height="500">   

[PySimpleGUIのユーザー入力を非表示にする方法 Jul 18, 2020](https://qiita.com/konson78960/items/d56434f6025b05e79d2f)  

# Animated-Popup  
[israel-dryer / Animated-Popup](https://github.com/israel-dryer/Animated-Popup)  

<img src="https://raw.githubusercontent.com/israel-dryer/Animated-Popup/master/examples/splashscreen.gif" width="500" height="600">  

<img src="https://raw.githubusercontent.com/israel-dryer/Animated-Popup/master/examples/animated_popup.gif" width="300" height="300">  

<img src="https://raw.githubusercontent.com/israel-dryer/Animated-Popup/master/examples/ascii_progress.gif" width="400" height="500">  

# Bitcoin-wallet-cracker   
[Py-Project / Bitcoin-wallet-cracker ](https://github.com/Py-Project/Bitcoin-wallet-cracker)

<img src="https://raw.githubusercontent.com/Py-Project/Bitcoin-wallet-cracker/main/bc.gif" width="400" height="500">  


# PySimpleGuiで入力に応じてグラフを表示・更新する  
[PySimpleGuiで入力に応じてグラフを表示・更新する Jan 11, 2021](https://qiita.com/Qlitre/items/d07d3b16c8f55dfc1d7d)  

[ PySimpleGUI /PySimpleGUI ](https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Embedded_Toolbar.py)  

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F951203%2F3825c8bc-7396-fe7d-af34-a6474c522825.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=8ff2d8dfda8f254e84605bd4f8c1903a" width="600" height="700">  

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F951203%2F53997628-69bc-f717-1685-74c77b61b9c8.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=ae816604977b7831d2450dd0e0deb425" width="600" height="700">    

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F951203%2F36a29f22-fa10-9adc-c4bf-ba83509e114d.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=3287ea503c1a93eb4438d3d61df14545" width="600" height="700">  

# Python画像処理のためのGUI入門（PySimpleGUI解説）  
[Python画像処理のためのGUI入門（PySimpleGUI解説）](https://qiita.com/soymushroom/items/da002d628d7a28cd6e97)  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1536445%2Fb3210f1e-6b4e-6080-8112-64a502fe4804.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=e41517a4e5bd7dfafa562e31bac9e85b" width="600" height="400">  

# 「PyWebIO」があればPython 100%でWebアプリ作れるってマジ！？
[「PyWebIO」があればPython 100%でWebアプリ作れるってマジ！？ Jul 06, 2021](https://qiita.com/payaneco/items/51a11a8063b7f0654561)

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F81851%2F12aa82b7-e50f-67d4-42ab-004a0cf092ce.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=5e45055760710a4ffdd3aa9c442fbbea" width="500" height="400">

# Python PySimpleGUIで作るPDFリーダー
[Python PySimpleGUIで作るPDFリーダー 2022.01.25](https://qlitre-weblog.com/pysimplegui-pdf-reader/)


起動すると、以下のようにGUIが立ち上がります。
<img src="https://images.microcms-assets.io/assets/4d9da4ddd0c2424e9dcb766ded76ca61/bb901785544647cb969a2cce3bbba7fe/image.png" width="500" height="400">


Browseボタンを押してPDFファイルを指定しますと、以下のように表示されます。
<img src="https://images.microcms-assets.io/assets/4d9da4ddd0c2424e9dcb766ded76ca61/9611eeff8f89494bbbd4525ddeb6afd9/image.png" width="500" height="400">


後は必要に応じてページ送りをしたり、簡単なズームができるという感じです。
<img src="https://images.microcms-assets.io/assets/4d9da4ddd0c2424e9dcb766ded76ca61/0f9ca3c7ae5d4951894bd0e909524a12/Animation_.gif" width="500" height="400">

## PySimpleGUI/DemoPrograms/Demo_PDF_Viewer.py  
[PySimpleGUI/DemoPrograms/Demo_PDF_Viewer.py](https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_PDF_Viewer.py)

## How do I resolve "No module named 'frontend'" error message?
[How do I resolve "No module named 'frontend'" error message?](https://stackoverflow.com/questions/56467667/how-do-i-resolve-no-module-named-frontend-error-message)

```
pip install PyMuPDF
```


# PySimpleGuiでTrelloを操作する 
[PySimpleGuiでTrelloを操作する 2021.09.05](https://qlitre-weblog.com/pysimplegui-trello-app)

[qlitre /pysimplegui-trello](https://github.com/qlitre/pysimplegui-trello)


# WebSocket Client  
[[Python]WebSocket Client實作  2020-03-25](https://ithelp.ithome.com.tw/articles/10230592)  
```
產生websocket的連線

直接將websocket的網址，傳入物件裡面，就會開始嘗試連線，這邊可以一起傳入各種事件觸發時候要執行的function，或是稍後再指定也是可以的
```

```
from websocket import enableTrace, WebSocketApp

# 取物件的時候就直接指定事件方法
ws = WebSocketApp(
    "ws://localhost:9453",
    on_message=MessageFunc,
    on_error=ErrorFunc,
    on_close=CloseFunc
)

# 取完物件再指定事件方法
ws.on_open = OpenFunc
```

```
這幾種事件觸發的時機，分別如下：

    on_open：開啟連線成功時執行
    on_message：收到來自server端傳來的訊息時執行
    on_error：連線發生錯誤時執行
    on_close：關閉連線時執行
```

## websocket-client  
[websocket-client /websocket-client](https://github.com/websocket-client/websocket-client)  
```
websocket-client is a WebSocket client for Python. It provides access to low level APIs for WebSockets. websocket-client implements version hybi-13 of the WebSocket procotol. This client does not currently support the permessage-deflate extension from RFC 7692.
```

### Long-lived Connection  
```
import websocket
import _thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://echo.websocket.org/",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
```

# Websocket GUI Debug Tool比較  
[Websocket GUI Debug Tool比較 updated at 2020-06-09](https://qiita.com/snamiki1212/items/9ee83302dfec39c80a2f)  

## Browser WebSocket Client  
[Browser WebSocket Client](https://qiita.com/snamiki1212/items/9ee83302dfec39c80a2f#4-browser-websocket-client)

<img src="https://camo.qiitausercontent.com/cb310ed21fe64237e177e7c7573b801be29f0a11/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3138363232382f65336635643562662d356361312d653333392d333630362d6339396436663835323839622e706e67" width="400" height="600"> 

[[Python] Websocket Example - Justin 程式教學 2018年11月7日](https://jccsc.blogspot.com/2018/11/python-websocket-example.html)  

# Streamlit vs PyWebIO Webフレームワーク対決！  
[Streamlit vs PyWebIO Webフレームワーク対決！ 2021-08-07](https://qiita.com/payaneco/items/050a7e21a9f3c020ff4f)

```
Streamlitを使えばHTMLを一行も書かずにPython 100%でWebアプリを作れるお手軽フレームワークを味わったよ！
```

## Streamlit  
```
Streamlitはデータ可視化機能が豊富に用意されてる。

公式サイトで紹介されてるstreamlit helloコマンドを打つだけでアニメーションとか地図とかグラフがぐねぐね動いて「おーさむ！1」ってなること請け合い。
まだ2021年7月に出たばかりのVersion 0.84でセッション情報を扱う機能が追加されるなど、ページ遷移ロジックの定石は確立されてないようにも見える。
標準で用意されている機能が多く追加変更が早い分、凝り性の人はこだわりが多くなるかもしれない。

ちなみにSharing・Streamlitに申し込むことでHerokuやPython AnywhereのようにGithubから爆速無料でWebアプリを公開できるっぽい点も魅力的。
```

## コード実行  
### Streamlit  
```
Djangoみたいに専用コマンドがある。

streamlit run .\test.py
```

### PyWebIO
```
BottleとかFlaskみたいにpython実行で呼び出す。

python .\test.py
```

## 画面遷移  
```
変数を保持しながら画面遷移するコードの比較だよ。
どっちのフレームワークもあんまり資料がなくて苦労したよ。
```
<img src="https://camo.qiitausercontent.com/38bcbba09a638dbad5e5d67aab4a45c3f7cc8ba1/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f38313835312f31323934343865372d633338392d623662652d663263652d3730623434613233386134352e706e67" width="400" height="500">  

### Streamlit  
```
グローバル変数とかは最初に読み込まれるだけで、ラジオボタンを選択し直しても再読み込みしてくれないっぽい。
対策として最近できたSession State APIを使ってセッションに残したデータを遷移先でも使うコードにしてみた。
※0.84より前でも一工夫すればできる
```
<img src="https://camo.qiitausercontent.com/1558a525e5de6d391d04ffd379a6fee1ecc66567/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f38313835312f37616566656362312d646534322d663061362d313539652d6566623233373635343065652e706e67" width="400" height="300">  


## データ可視化  
### Streamlit  
```
せっかくだから外部ツールと連携してData Virtualizationもしとく。
これをやっておくとできる！SEって感じがするからね！

matplotlibとかbokehとかnumpyのインストール方法は省略するよ。
```
<img src="https://camo.qiitausercontent.com/057b5122f3c2850254f16c95e74145856c947204/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f38313835312f64616139313534642d316161642d353362312d383664382d3330383731316462343962612e706e67" width="400" height="500">  


# streamlitで遊ぼう！  
[streamlitで遊ぼう！ updated at 2021-01-13](https://qiita.com/irisu-inwl/items/9d49a14c1c67391565f8)

repository: https://github.com/irisu-inwl/streamlit-tutorial
動作確認環境: windwos10, docker for windows


# Streamlitで爆速アプリ開発  
[Streamlitで爆速アプリ開発 posted at 2020-12-14](https://qiita.com/nyax/items/fc418416e97a12141d0a)

## デプロイもできちゃう  
```
Streamlitでデプロイもできてしまう、、！
https://docs.streamlit.io/en/stable/deploy_streamlit_app.html
に沿ってするとできます
```

# 【Python】LINEのグルチャ履歴をヌルヌル動くグラフにしてみた～原理からWebアプリ化まで～  
[【Python】LINEのグルチャ履歴をヌルヌル動くグラフにしてみた～原理からWebアプリ化まで～ posted at 2021-02-17](https://qiita.com/adumaru0828/items/4be1c07aeb461f7d9341) 
```
app.py
```

# Streamlitで作成した株価アプリをWEB公開した（キャッシュ説明あり）  
[Streamlitで作成した株価アプリをWEB公開した（キャッシュ説明あり）updated at 2021-02-01](https://qiita.com/morita-toyscreation/items/c9c873bce8d54cfe5b36)  

## キャッシュ化  
```
このままWEB公開するとBigQueryアクセスが多くなるのでキャッシュ化を行う
@st.cacheデコレーターを付けることで返り値をキャッシュする
@st.cacheは引数種類別にキャッシュする
2回目以降はキャッシュを使いBigQueryにアクセスしない
allow_output_mutationをTrueにすると返り値が変わってもエラーにならない
```

```
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def _get_stock(stock_no: str, start_date: str, end_date: str):
```

## Docker環境準備  
```
Dockerfile作成
Cloud Runで動かすのでポート8080に設定する
```

```
FROM python:3.7.4

WORKDIR /app
ADD . /app

RUN apt-get update && apt-get clean;
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV TZ Asia/Tokyo
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV GOOGLE_APPLICATION_CREDENTIALS /app/config/xxx.json

EXPOSE 8080

CMD streamlit run --server.port 8080 app.py
```

```
$ docker build -t kabu-analysis .
```

```
$ docker run --name kabu-analysis \
-p 8080:8080 -v ~/Sites/kabu-analysis/:/app -it --rm kabu-analysis
```

# PyCaretとStreamlitでAutoMLのGUIツールをさくっと作ってみる   
[PyCaretとStreamlitでAutoMLのGUIツールをさくっと作ってみる posted at 2021-02-21](https://qiita.com/ryoshi81/items/e9560ade1f0adedbaf6c)


# 【Streamlit】JavaScriptが嫌いだからPythonだけでWebアプリをつくる  
[【Streamlit】JavaScriptが嫌いだからPythonだけでWebアプリをつくる updated at 2020-08-08](https://qiita.com/SPShota/items/a63e19807779175aa29b)

```
フロント（SPA）開発案件2つのプレイングマネージャーと開発リーダーやってますが、JavaScriptが死ぬほど嫌いです。
ブラウザ上で動作するスクリプトなので仕方ないし、async-awaitで大分便利になったけど、非同期処理がやっぱり好きじゃないです。

JavaとかPythonとかそれなりの期間触った言語は大概「みんな違ってみんないい」みたいな感じになるんですが、JavaScriptだけそうならないので本当に嫌いなんだと思います。

因みにCSSはもっと嫌いです。

機械学習モデルの構築をPythonで実装することは多いと思いますが、ちょっとしたデモアプリでも作るとなると、フロント側はどうしてもHTML、JavaScript、CSSで組まないといけないです。

Jupyter Notebookも選択肢に入るかもしれませんが、Webアプリと比べると表現の自由度は下がるし、コードセルが見えるのはなんか煩雑に見えます。

嫌いかどうかは置いておいて、フロント開発の煩わしさを抱えている人って結構いるんじゃないかなって思ってます。 ・・・いるよね？
7月の連休中に触ったStreamlitっていうライブラリが滅茶苦茶便利だったので、今回はこれを使ってPython "だけ" でWEBアプリを作ってみようと思います！
```

## WEBUIを使ってインタラクティブなアプリにする  
```
ここまでだと、Jupyterで可視化してるのとあまり差がないのでWEBアプリケーションらしいインタラクションを実装します。

データ取得処理の後に日付の範囲指定をするコンポーネントの表示処理を追加して、データフレームを絞り込みます。
bodyの場合はst.コンポーネント名、サイドバーにの場合、st.sidebar.コンポーネント名でUIコンポーネントを追加します。
```


# Streamlit極簡易的Dashboard開發 - Neutron 
[Streamlit極簡易的Dashboard開發 - Neutron Dec 16, 2020](https://neutron0916.medium.com/streamlit%E6%A5%B5%E7%B0%A1%E6%98%93%E7%9A%84dashboard%E9%96%8B%E7%99%BC-c433e1da1559) 

## Streamlit 概念  
<img src="https://miro.medium.com/max/2000/1*lU7YeppmSvFiZmEkUDX06w.png" width="700" height="500">  


# Streamlitを用いた音響信号処理ダッシュボードの開発(Tokyo BISH Bash #03発表資料) 
[Streamlitを用いた音響信号処理ダッシュボードの開発(Tokyo BISH Bash #03発表資料) 2020-10-13](https://www.hiromasa.info/posts/22/) 
[ wrist /streamlit-dsp ](https://github.com/wrist/streamlit-dsp)

[window_viwer.py](https://github.com/wrist/streamlit-dsp/blob/master/streamlit_dsp/window_viewer.py)

# Python: Streamlit を使って手早く WebUI 付きのプロトタイプを作る  
[Python: Streamlit を使って手早く WebUI 付きのプロトタイプを作る 2021-05-14](https://blog.amedama.jp/entry/streamlit-tutorial)  

## Column  
[カラム](https://blog.amedama.jp/entry/streamlit-tutorial#%E3%82%AB%E3%83%A9%E3%83%A0) 
```
# -*- coding: utf-8 -*-

import streamlit as st


def main():
    # カラムを追加する
    col1, col2, col3 = st.beta_columns(3)

    # コンテキストマネージャとして使う
    with col1:
        st.header('col1')

    with col2:
        st.header('col2')

    with col3:
        st.header('col3')

    # カラムに直接書き込むこともできる
    col1.write('This is column 1')
    col2.write('This is column 2')
    col3.write('This is column 3')


if __name__ == '__main__':
    main()
```
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/momijiame/20210511/20210511184758.png" width="600" height="400">  

## container 
[コンテナ](https://blog.amedama.jp/entry/streamlit-tutorial#%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A)
```
# -*- coding: utf-8 -*-

import streamlit as st


def main():
    # コンテナを追加する
    container = st.beta_container()

    # コンテキストマネージャとして使うことで出力先になる
    with container:
        st.write('This is inside the container')
    # これはコンテナの外への書き込み
    st.write('This is outside the container')

    # コンテナに直接書き込むこともできる
    container = st.beta_container()
    container.write('1')
    st.write('2')
    # 出力順は後だがレイアウト的にはこちらが先に現れる
    container.write('3')


if __name__ == '__main__':
    main()
```
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/momijiame/20210511/20210511185155.png" width="600" height="400">  

```
# -*- coding: utf-8 -*-

import streamlit as st


def main():
    placeholder = st.empty()
    # プレースホルダにコンテナを追加する
    container = placeholder.beta_container()
    # コンテナにカラムを追加する
    col1, col2 = container.beta_columns(2)
    # それぞれのカラムに書き込む
    with col1:
        st.write('Hello, World')
    with col2:
        st.write('Konnichiwa, Sekai')


if __name__ == '__main__':
    main()
```
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/momijiame/20210511/20210511185307.png" width="600" height="400">  


## Expander
[エキスパンダ](https://blog.amedama.jp/entry/streamlit-tutorial#%E3%82%A8%E3%82%AD%E3%82%B9%E3%83%91%E3%83%B3%E3%83%80)
```
# -*- coding: utf-8 -*-

import streamlit as st


def main():
    with st.beta_expander('See details'):
        st.write('Hidden item')


if __name__ == '__main__':
    main()
```
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/momijiame/20210511/20210511185400.png" width="600" height="400">  

## Sidebar
[サイドバー](https://blog.amedama.jp/entry/streamlit-tutorial#%E3%82%B5%E3%82%A4%E3%83%89%E3%83%90%E3%83%BC)  

```
ウィジェットやオブジェクトの表示をサイドバーに配置することもできる。 使い方は単純で、サイドバーに置きたいなと思ったら sidebar をつけて API を呼び出す。

以下のサンプルコードでは、サイドバーにボタンを配置している。 前述したとおり、streamlit.button() を streamlit.sidebar.button() に変えるだけ。 同様に、streamlit.sidebar.dataframe() のように間に sidebar をはさむことで大体の要素はサイドバーに置ける。
```

```
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np


def main()  :
    # サイドバーにリロードボタンをつける
    st.sidebar.button('Reload')
    # サイドバーにデータフレームを書き込む
    data = np.random.randn(20, 3)
    df = pd.DataFrame(data, columns=['x', 'y', 'z'])
    st.sidebar.dataframe(df)


if __name__ == '__main__':
    main()
```
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/momijiame/20210512/20210512222116.png" width="600" height="400">  

## Help   
[オブジェクトの docstring を表示する](https://blog.amedama.jp/entry/streamlit-tutorial#%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AE-docstring-%E3%82%92%E8%A1%A8%E7%A4%BA%E3%81%99%E3%82%8B) 
```
# -*- coding: utf-8 -*-

import pandas as pd

import streamlit as st


def main():
    st.help(pd.DataFrame)


if __name__ == '__main__':
    main()
```
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/momijiame/20210512/20210512222544.png" width="600" height="400">  

## 単一のスクリプトで複数のアプリケーションを扱う
```
# -*- coding: utf-8 -*-

import streamlit as st


def render_gup():
    """GuP のアプリケーションを処理する関数"""
    character_and_quotes = {
        'Miho Nishizumi': 'パンツァーフォー',
        'Saori Takebe': 'やだもー',
        'Hana Isuzu': '私この試合絶対勝ちたいです',
        'Yukari Akiyama': '最高だぜ！',
        'Mako Reizen': '以上だ',
    }
    selected_items = st.multiselect('What are your favorite characters?',
                                    list(character_and_quotes.keys()))
    for selected_item in selected_items:
        st.write(character_and_quotes[selected_item])


def render_aim_for_the_top():
    """トップ！のアプリケーションを処理する関数"""
    selected_item = st.selectbox('Which do you like more in the series?',
                                 [1, 2])
    if selected_item == 1:
        st.write('me too!')
    else:
        st.write('2 mo ii yo ne =)')


def main():
    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        'GIRLS und PANZER': render_gup,
        'Aim for the Top! GunBuster': render_aim_for_the_top,
    }
    selected_app_name = st.sidebar.selectbox(label='apps',
                                             options=list(apps.keys()))

    if selected_app_name == '-':
        st.info('Please select the app')
        st.stop()

    # 選択されたアプリケーションを処理する関数を呼び出す
    render_func = apps[selected_app_name]
    render_func()


if __name__ == '__main__':
    main()
```
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/momijiame/20210512/20210512223221.png" width="600" height="400">  

<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/momijiame/20210512/20210512223230.png" width="600" height="400">  

<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/momijiame/20210512/20210512223239.png" width="600" height="400">  


## Argparse  
```
# -*- coding: utf-8 -*-

import argparse

import streamlit as st


def main():
    parser = argparse.ArgumentParser(description='parse argument example')
    # --message または -m オプションで文字列を受け取る
    parser.add_argument('--message', '-m', type=str, default='World')
    # 引数をパースする
    args = parser.parse_args()
    # パースした引数を表示する
    st.write(f'Hello, {args.message}!')


if __name__ == '__main__':
    main()
```

```
$ streamlit run example.py -m Sekai
Usage: streamlit run [OPTIONS] TARGET [ARGS]...
Try 'streamlit run --help' for help.

Error: no such option: -m
```

```
$ streamlit run example.py -- -m Sekai
```

## Click  
```
続いてサードパーティ製のパッケージである Click を使う場合。 
Click は純粋なコマンドラインパーサ以外の機能もあることから、スクリプトを記述する時点から注意点がある。 
具体的には、デコレータで修飾したオブジェクトを呼び出すときに standalone_mode を False に指定する。 
こうすると、デフォルトでは実行が完了したときに exit() してしまう振る舞いを抑制できる。
```

```
# -*- coding: utf-8 -*-

import streamlit as st
import click


@click.command()
@click.option('--message', '-m', type=str, default='World')
def main(message):
    # パースした引数を表示する
    st.write(f'Hello, {message}!')


if __name__ == '__main__':
    # click.BaseCommand.main() メソッドが呼ばれる
    # デフォルトの動作では返り値を戻さずに exit してしまう
    # スタンドアロンモードを無効にすることで純粋なコマンドラインパーサとして動作する
    main(standalone_mode=False)
```

```
$ streamlit run example.py -- -m Sekai
```


# 【Streamlit】株価データのお手軽GUI分析  
[【Streamlit】株価データのお手軽GUI分析  2021-03-20](https://dajiro.com/entry/2021/03/20/171130)  
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/D/Dajiro/20210320/20210320160918.png" width="700" height="500">  


# cdsdashboards 
[ideonate/cdsdashboards](https://github.com/ideonate/cdsdashboards/tree/master/examples/sample-source-code/streamlit)  


# Streamlit Offical API  
[Streamlit Offical API](https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py)  


# GUI Console 
[ Network-and-Database-Programming /week-10](https://github.com/Network-and-Database-Programming/week-10/tree/main)  

```
Simple Command Application to GUI
Can run & generate command, also print output on the GUI output.  
```

<img src="https://camo.githubusercontent.com/facad0f1ea2391566d047df827f1b045fca25af513ba60a35a2b95beb9f858fe/68747470733a2f2f692e696d6775722e636f6d2f66556c4e3048392e706e67" width="500" height="400">  

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



