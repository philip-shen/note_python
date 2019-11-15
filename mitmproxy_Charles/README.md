# note of_HTTPS Proxy_
Take some note of HTTPS Proxy, ex: mitmproxy, Charles

# Table of Content
[iOS実機のSSL通信をプロキシによって傍受したり改ざんする方法]()  
[MacでWifi共有で透過的にmitmproxy]()  


[Reference](#reference)  

# iOS実機のSSL通信をプロキシによって傍受したり改ざんする方法  
[iOS実機のSSL通信をプロキシによって傍受したり改ざんする方法 Dec 16, 2013](https://qiita.com/yimajo/items/c67cb711851f747c35e5)
## mitmproxyとその導入について  
mitmproxyはコマンドライン製のプロキシツールです。
名前のmitmとはman-in-the-middleの略で通信用語のman-in-the-middle attack(中間者攻撃)
などに使われる用語から来ているようです。  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F16400%2Fdf954d03-10dd-a3a3-94de-cac3361ef0b2.jpeg?ixlib=rb-1.2.2&auto=compress%2Cformat&gif-q=60&w=1400&fit=max&s=951adbe026ea4e66a0b996c9191a56d8)  

## Pythonのインストール  
## mitmproxyのインストール  
```
 pip install mitmproxy

 $ pip install mitmproxy -U
```
## mitmproxyの起動  
```
$ mitmproxy -p 8080
```
iOSのWiFi設定からHTTPプロキシで手動を選択しサーバーのアドレスと
ポート番号を指定できるようになっています。
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F16400%2F3278c67d-2e5a-e130-abbc-67bce4a044ad.jpeg?ixlib=rb-1.2.2&auto=compress%2Cformat&gif-q=60&s=f7c1c0bd301af1985ff240c39c1856e0)  

## iPhone実機へのルート証明書のインストール  
またmitmproxyを実行すると~/.mitmproxy/にmitmroxy-ca.pemという証明書が作成されます。
OS XからiPhoneへこの証明書をメール送信し、iPhone側のメールクライアントから
証明書を開くことでインストールすることが可能です。
なお、この証明書はiOSアプリ開発者にはお馴染み[設定][一般][プロビジョニング]から確認できます。


# MacでWifi共有で透過的にmitmproxy  
[MacでWifi共有で透過的にmitmproxy 2014-02-04 ](http://bagpack.hatenablog.jp/entry/2014/02/04/225553)  
## 手順  
```
1. mitmproxyのインストール
2. 証明書を端末（iPhone/Android)にインストール
3. Wifi共有の設定
4. Packet forwardingの設定
```
## 2. 証明書を端末（iPhone/Android)にインストール  
下記に配置されているのでメールなどを使って端末に送る。 
添付ファイルをタップすれば自動的にインストールのためのアプリ選択画面が表示される。  
```
$ ~/.mitmproxy/mitmproxy-ca-cert.pem
```
![alt tag](http://cdn-ak.f.st-hatena.com/images/fotolife/b/bagpack/20140204/20140204225038.png)  

## 4.Packet forwardingの設定  
```
$ ifconfig
```
Packet forwardingを有効にする  
```
$ sudo sysctl -w net.inet.ip.forwarding=1
```
Packet forwardingの設定を下記のような感じにする。  
```
$ sudo vi /private/etc/pf.conf
```

```
scrub-anchor "com.apple/*"
nat-anchor "com.apple/*"
rdr-anchor "com.apple/*"
rdr pass on bridge0 inet proto tcp from 192.168.2.0/24 to any port http -> 127.0.0.1 port 8080
rdr pass on bridge0 inet proto tcp from 192.168.2.0/24 to any port https -> 127.0.0.1 port 8080
dummynet-anchor "com.apple/*"
anchor "com.apple/*"
load anchor "com.apple" from "/etc/pf.anchors/com.apple"
```

pfを有効にする。  
```
$ sudo pfctl -f /private/etc/pf.conf
$ sudo pfctl -e
```

mitmproxyを透過的プロキシモードで起動する。
```
$ mitmproxy -T --host
```

# mitmproxyを使ってSSL通信の中身を確認する   
[mitmproxyを使ってSSL通信の中身を確認する 2012/01/29](https://ku.ido.nu/post/90510462254/how-to-use-mitmproxy) 

# モバイルアプリ開発者のための mitmproxy 入門
[モバイルアプリ開発者のための mitmproxy 入門 Sep 02, 2014](https://qiita.com/hkurokawa/items/9034274cc1b9e1405c68)  

# ubuntu14.04 をアクセスポイントにして透過型プロキシ通す  
[ubuntu14.04 をアクセスポイントにして透過型プロキシ通す Jun 16, 2015](https://qiita.com/arc279/items/944cd8bb0f438cb6dde1)  

[mitmproxy×透過型×ARPスプーフィング 2013-01-24](https://asannou.hatenablog.com/entries/2013/01/24)

# Installing mitmproxy on Windows Subsystem for Linux (WSL)  
[Installing mitmproxy on Windows Subsystem for Linux (WSL) Feb 9, 2019]()  
```
sudo apt install python3-pip && sudo pip3 install -U pip && sudo pip3 install mitmproxy
```

# 
[iOSアプリのAPIリクエストのトレースはどうするのが効率的か？ 2016-02-11](https://qiita.com/WorldDownTown/items/42d9ab6c746fe7a6bc9c)  

ライブラリ | メリット | デメリット
------------------------------------ | ------------------------------------ | ---------------------------------------------
ResponseDetective | カスタマイズ性が高い | アプリ実装多め
Wireshark | アプリ実装不要 | https不可
Charles | アプリ実装不要・設定が簡単・高機能 | 有料
PonyDebugger | ChromeのDeveloper Toolが見やすい | 古い・メンテ少ない
netfox | アプリ実装は一行だけ | リアルタイムに通信を見れない
mitmproxy | アプリ実装不要・CUI・無料でSSLも確認できる | なし

# 
[【Ruby, Python】開発時に通信傍受プロキシを設置した時、ルート証明書を与えて、ハンドシェイクエラーを回避する 2018-02-12](https://qiita.com/dogwood008/items/3e17ef73800bee7adbb0)  

どうやって覗くの？  
```
この辺を使ってください。私はcharles大好き人間なので課金して使っています。今回はcharlesを使いますが、mitm-pythonの場合もほぼ同様です。
```
* [daniel4x/mitm-python](https://github.com/daniel4x/mitm-python)

# Reference  
* [Charles 破解版免费下载和注册安装教程 4.2.28激活](https://www.axihe.com/charles/charles/free-use.html)  
```
Charles 破解原理一：文件覆盖
```
```
## Charles 破解原理二：注册码进行注册
```
* [Charles 破解工具web版](https://github.com/8enet/Charles-Crack)  

* [Charles 4.2.8 Mac破解版(实测可用) ](https://litets.com/article/2019/3/14/43.html)  
```
方式一

共享版本下载：下载地址 密码:lg6n 实测可用。
```

* [通信系のデバッグには Charles が便利 2017-11-27](https://qiita.com/usagimaru/items/d340e87da98e62f99b60)  

* [AndroidのSSL通信をCharlesで確認する方法 2017-03-23](https://qiita.com/Capotasto/items/a51a76a8670e67798861)  

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