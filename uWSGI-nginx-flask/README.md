# Purpose
Take note of uWSGI+nginx+flask for Web App  

# Table of Contents  
[PythonのフレームワークFlaskを使用してWebアプリ作成](#python%E3%81%AE%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%83%AF%E3%83%BC%E3%82%AFflask%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6web%E3%82%A2%E3%83%97%E3%83%AA%E4%BD%9C%E6%88%90)  
[DockerでPython+uWSGI+Nginxの環境を作成](#docker%E3%81%A7pythonuwsginginx%E3%81%AE%E7%92%B0%E5%A2%83%E3%82%92%E4%BD%9C%E6%88%90)  
[]()  
[]()  

# PythonのフレームワークFlaskを使用してWebアプリ作成  

## PythonのFlaskを使用してWebアプリ作成してみよう（１）こんにちは世界  
[PythonのFlaskを使用してWebアプリ作成してみよう（１）こんにちは世界 Jul 13, 2019 ]()  
```
目的

    PythonのフレームワークであるFlaskを使用してWebアプリに必要な機能の作成と解説をやります。
    普段の勉強のアウトプットとして書いています。質問や指摘は大歓迎です。

今回の目標

    『Hello World』をFlaskで出力してみよう！
```

## PythonのFlaskを使用してWebアプリ作成してみよう（２）HTMLの表示とメソッドとパラメータの受け取りかた  
[PythonのFlaskを使用してWebアプリ作成してみよう（２）HTMLの表示とメソッドとパラメータの受け取りかた Jul 13, 2019]()  
```
このシリーズの目的

    PythonのフレームワークであるFlaskを使用してWebアプリに必要な機能の作成と解説をやります。
    普段の勉強のアウトプットとして書いています。質問や指摘は大歓迎です。

今回の目標

    FlaskでHtmlを返してみよう
    ３種類のパラメータの受け取りかたを知ろう
        urlの場合
        getの場合
        postの場合
```

## PythonのフレームワークFlaskを使用してWebアプリ作成の物語（３）Docker登場　DBの準備  
[PythonのフレームワークFlaskを使用してWebアプリ作成の物語（３）Docker登場　DBの準備 Jul 14, 2019]()  
```
このシリーズの目的

    PythonのフレームワークであるFlaskを使用してWebアプリに必要な機能の作成と解説をやります。
    普段の勉強のアウトプットとして書いています。質問や指摘は大歓迎です。

目的

    Flask で使用する DB（PostgreSQL） を Docker を使用して準備する
    DB を pgadmin4 で見れるようにする
```

## PythonのフレームワークFlaskを使用してWebアプリ作成の物語（４）DBに接続して操作してみよう  
[PythonのフレームワークFlaskを使用してWebアプリ作成の物語（４）DBに接続して操作してみよう Jul 28, 2019]()  
```
このシリーズの目的

    PythonのフレームワークであるFlaskを使用してWebアプリに必要な機能の作成と解説をやります。
    普段の勉強のアウトプットとして書いています。質問や指摘は大歓迎です。

目的

    Flask で Postgresql に接続
    DB にレコードを登録できること
    DB からレコードを取得できること
```

## PythonのフレームワークFlaskを使用してWebアプリ作成の物語（5）nginxの登場  
[PythonのフレームワークFlaskを使用してWebアプリ作成の物語（5）nginxの登場  Aug 25, 2019]()  
```
目的

    nginxで静的なコンテンツを分離してみる
```
静的なコンテツの配信をnginxにお願いすることで、flaskはアプリケーションの内部の実装のみに専念させることができます。  

今回の記事の構成は以下の様になります。  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F190554%2Fa4902fbd-a85d-2614-0ad8-f9cb1806fe77.png?ixlib=rb-1.2.2&auto=compress%2Cformat&gif-q=60&w=1400&fit=max&s=86d41e8a8e5d1b1951c572d4093aa9fd)  


## PythonのフレームワークFlaskを使用してWebアプリ作成の物語（6）非同期通信でFlaskにアクセスしてみよう  
[PythonのフレームワークFlaskを使用してWebアプリ作成の物語（6）非同期通信でFlaskにアクセスしてみよう  Sep 29, 2019](https://qiita.com/penpenta/items/15223262b1e146cf8474)  
```
目的

    非同期通信でflaskに問い合わせをしてみよう
```

イメージ図  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F190554%2F246efd72-91b2-9b00-03fa-ff501e3f38ce.png?ixlib=rb-1.2.2&auto=compress%2Cformat&gif-q=60&w=1400&fit=max&s=762f66b29165375fa3ebf45e5e217972)  



# DockerでPython+uWSGI+Nginxの環境を作成  
[DockerでPython+uWSGI+Nginxの環境を作成 Aug 02, 2018](https://qiita.com/hiroykam/items/748c3fab31c616994db9)  

## ディレクトリ構成  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F135559%2Fe3442a78-949b-b3a1-fdc2-a1d4b7cfeffb.png?ixlib=rb-1.2.2&auto=compress%2Cformat&gif-q=60&s=ed7fafd6c839df983144d09ca30ecf06)  

## コンテナの操作  
ビルドと起動両方を実施する場合（-dオプションを指定するとバックグラウンドで起動）：  
```
$ docker-compose up --build
```

ビルドのみの場合：
```
$ docker-compose build
```
起動のみの場合（-dオプションを指定するとバックグラウンドで起動）：
```
$ docker-compose up
```
![alt tag](https://i.imgur.com/2SJMeI9.jpg)  


## コンテナIDの確認  
```
$ docker ps -a
```
![alt tag](https://i.imgur.com/KGNmg5Z.jpg)  


## コンテナの停止・開始  
上記の”コンテナIDの確認”を例にするとCONTAINER_ID

停止する場合：
```
$ docker stop CONTAINER_ID
```
開始する場合：
```
$ docker start CONTAINER_ID
```
再起動する場合：
```
$ docker restart CONTAINER_ID
```

## 起動しているコンテナにログイン  
コンテナに入ることができ、サーバの状態等が確認できる。
```
$ docker exec -it CONTAINER_ID bash
```

## コンテナの削除  
コンテナが停止している状態であれば、削除可能。
```
$docker rm CONTAINER_ID
```

## デモ  
コンテナを起動して、http://localhost:8080にブラウザでアクセスすると、
"Hello World"が表示される。
![alt tag](https://i.imgur.com/UT17Mqe.jpg)  


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
