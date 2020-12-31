Table of Contents
=================

   * [Purpose](#purpose)
   * [Table of Contents](#table-of-contents)
   * [Speech Recognition](#speech-recognition)
      * [Amazon Transcribe の使い方](#amazon-transcribe-の使い方)
      * [Google Cloud Speech-to-Text の使い方](#google-cloud-speech-to-text-の使い方)
      * [Microsoft Azure Speech-to-Text の使い方](#microsoft-azure-speech-to-text-の使い方)
   * [Google Cloud Speech-to-Text API](#google-cloud-speech-to-text-api)
      * [動作環境](#動作環境)
      * [GCPのプロジェクト作成](#gcpのプロジェクト作成)
      * [Cloud SDKの導入](#cloud-sdkの導入)
      * [speech-v1を使うように変更](#speech-v1を使うように変更)
      * [サービスアカウントキーの作成](#サービスアカウントキーの作成)
      * [GCP Procedures](#gcp-procedures)
      * [Troubles](#troubles)
   * [HarryVolek /PyTorch_Speaker_Verification](#harryvolek-pytorch_speaker_verification)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose  
Take note of Speaker Verification  


# Speech Recognition  
[主要4社のクラウド音声認識精度の比較 2020-09-27](https://qiita.com/kamikennn/items/6af3f8960cdacbec828b)  

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F391974%2Fcbe98175-f5e2-df4d-bb6d-248094f9487e.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=07d275d5a36d029969deeb34f1c1643f"  width="500" height="400">


[主要4社のクラウド音声認識サービスの使い方 2020-10-17](https://qiita.com/kamikennn/items/e88ecaf6b76a71cfd1e6)  
```
Amazon:
    Transcribe
Google:
    Cloud Speech-to-Text
IBM:
    Watson Speech-to-Text
Microsoft:
    Azure Speech-to-Text
```
## Amazon Transcribe の使い方  
[Amazon Transcribe の使い方](https://qiita.com/kamikennn/items/e88ecaf6b76a71cfd1e6#amazon-transcribe-%E3%81%AE%E4%BD%BF%E3%81%84%E6%96%B9)  
```
まず，認識させたい音声ファイルをS3というAWSのクラウドストレージの置く必要があります．

    S3のページの左上辺りにあるCreate bucketをクリックしてバケットを作成します．バケット名はなんでもいいです.地域(region)はtokyoにしておきました．
        Bucket name: recognitiontest(なんでも良い)
        Region: Asia Pacific(Tokyo)
```

```
バケットを作成したら，作成したバケットに音声ファイルをアップロードすれば準備完了です．
左上辺りにUploadというボタンがあるので，クリックすればアップロードできます．
フォルダを作成して複数の音声ファイルをまとめることもできるのでお好みでやってください．        
```

## Google Cloud Speech-to-Text の使い方  
[Google Cloud Speech-to-Text の使い方](https://qiita.com/kamikennn/items/e88ecaf6b76a71cfd1e6#google-cloud-speech-to-text-%E3%81%AE%E4%BD%BF%E3%81%84%E6%96%B9)  
```
Amazon Transcribeとは違い，認識させたい音声をクラウドに置く必要はありません.

    ローカルにある音声を認識可能
    認識させたい音声ファイルのパスを記載したテキストファイルを用意しておく
        以下のサンプルプログラムではspeech_data_path.txt
        IBM Watson, Microsoft Azure でも同様のものを使用

```

```
それではまずAPIキーを含む環境変数を通しておきます．APIキーの情報はjsonファイルに記載されています．このjsonファイルはGCPのコンソールからダウンロードしておく必要があります．ナビゲーションメニューのAPIとサービスへ行けばjson形式の認証情報をダウンロードできます．
```

## Microsoft Azure Speech-to-Text の使い方  
[Microsoft Azure Speech-to-Text の使い方](https://qiita.com/kamikennn/items/e88ecaf6b76a71cfd1e6#microsoft-azure-speech-to-text-%E3%81%AE%E4%BD%BF%E3%81%84%E6%96%B9)  
```
AzureはIBM Watsonと同様にプログラム内にAPIキー(speech_key)とregionを記述します

    speech_key: [自分のspeech_key] を書き換えてください
    service_region:japaneast としました
```


<img src=""  width="300" height="400">


# Google Cloud Speech-to-Text API  
[Google Cloud Speech-to-Text APIでマイク入力からストリーミング音声認識をする Sep 10, 2019](https://qiita.com/hamham/items/3733ac8cd9e3d7b9ccae)  

## 動作環境  
```
 Windows 10
 Python 3.6.8 (64bit)
 Google Cloud SDK
```
> GCPでプロジェクトを作成したり、gcloudの初期設定をしたり、Pythonのセットアップしたり、必要なパッケージをpipでインストールしたりは、前述の記事とほぼ変わりませんので参考にしてください。

## GCPのプロジェクト作成  
[GCPのプロジェクト作成](https://qiita.com/hamham/items/9b553d0759a2319ea211#gcp%E3%81%AE%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E4%BD%9C%E6%88%90)  

## Cloud SDKの導入  
[Cloud SDKの導入](https://qiita.com/hamham/items/9b553d0759a2319ea211#cloud-sdk%E3%81%AE%E5%B0%8E%E5%85%A5)  

## speech-v1を使うように変更  
```
pip install grpc.google.cloud.speech-v1
```

```
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
```

```
from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types
```

## サービスアカウントキーの作成  
```
GCPコンソールの「APIとサービス ＞ 認証情報」からサービスアカウントキーを作成します。
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F272753%2F7c60bd0e-58af-1f3f-00e1-23e74232c280.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=011a773d5e05206b82d04997bff7a054"  width="500" height="300">  

```
サービスアカウントキーに適当な名前（この記事ではspeech-to-text）をつけます。
役割は何が最低限必要かよくわからなかったのですが、Projectの「閲覧者」を与えれば結果的に動作しました。
```
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F272753%2Facbe573f-d20e-a9cd-128c-2ccf3fb1d461.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=b2388fe37143918e385a12e16d878640"  width="500" height="300">

```
これでjsonファイルを作成します。（この記事ではcredential.jsonとしてCドライブ直下に保存します）

そしてコマンドプロンプトから、環境変数としてこのjsonを指定します。
```

```
set GOOGLE_APPLICATION_CREDENTIALS=C:\credential.json
```

## GCP Procedures  
[Google Cloud Speech API を使った音声の文字起こし手順 2019-03-10](https://qiita.com/knyrc/items/7aab521edfc9bfb06625#8-%E5%AE%9F%E8%A1%8C%E7%B5%90%E6%9E%9C)  
```
1. コンソール画面に入る
2. Google Cloud Speech API を有効化する
3. APIの認証情報の作成（サービスアカウントキーの作成）
4. Google Cloud ShellでAPI認証する（サービスアカウントキーJSONのアップロード&環境変数登録）
5. 音声データのアップロード
6. 文字起こし実行Pythonスクリプトの作成
7. 音声文字起こしの実行
8. 実行結果
```

## Troubles   
[超初心者でもgoogle-cloud-speechを使えるが、つまずいた所はある。2019-08-04](https://qiita.com/hanlio/items/875b91e0d4931a57e86b)
```
第一関門：ImportError: cannot import name speechと表示された。

第二関門：403 Cloud Speech APIと表示された。

第三関門：文字化け
```


#  HarryVolek /PyTorch_Speaker_Verification  
[ HarryVolek /PyTorch_Speaker_Verification ](https://github.com/HarryVolek/PyTorch_Speaker_Verification?fbclid=IwAR0ROhwtLOKXtnalGWkHmSEghdlZCFA1hywtbFilBhHxfNqDGqwzh2sfcBI)  



# Troubleshooting


# Reference


* []()
![alt tag]()
<img src=""  width="300" height="400">

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


