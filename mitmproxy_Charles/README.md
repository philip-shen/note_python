# note of HTTPS Proxy
Take some note of HTTPS Proxy, ex: mitmproxy, Charles

# Table of Content  
[Modes of Operation in mitmproxy](#modes-of-operation-in-mitmproxy)  
[Regular Proxy](#regular-proxy)  
[Transparent Proxy](#transparent-proxy)  

[Install mitmporxy in Ubuntu 18.04 WSL](#install-mitmporxy-in-ubuntu-1804-wsl)  
[Step 1 remove original mitmproxy package](#step-1-remove-original-mitmproxy-package)  
[Step 2 virtualenv for mitmproxy](#step-2-virtualenv-for-mitmproxy)  
[Step 3 pip3 install mitmproxy](#step-3--pip3-install-mitmproxy)  
[Step 4 Check .mitmdump/](#step-4-check-mitmdump)  
[Step 5 Check mitmproxy](#step-5-check-mitmproxy)  
[Step 6 Start mitmproxy](#step-6-start-mitmproxy)  
[Trouble](#trouble)  
[Step 7 Setup Browser Proxy](#step-7-setup-browser-proxy)  
[Step 8 Open Browser](#step-8-open-browser)  
[Step 9 Click to Install Certificate](#step-9-click-to-install-certificate)  
[Step 10 Check Console by SSH](#step-10-check-console-by-ssh)  


[3 mitmproxy Tips You Might Not Know About](#3-mitmproxy-tips-you-might-not-know-about)  
[Tips 1: Custom configuration and key binding](#tips-1-custom-configuration-and-key-binding)  
[Tips 2: Knowing client connection status when a filter is applied](#tips-2-knowing-client-connection-status-when-a-filter-is-applied)  
[Tips 3: Using mitmproxy as a mock server](#tips-3-using-mitmproxy-as-a-mock-server)  


[使用 mitmproxy + python 做拦截代理](#%E4%BD%BF%E7%94%A8-mitmproxy--python-%E5%81%9A%E6%8B%A6%E6%88%AA%E4%BB%A3%E7%90%86)  
[Script](#script)  
[Event](#event)  
[Example](#[example)  


[iOS実機のSSL通信をプロキシによって傍受したり改ざんする方法](#ios%E5%AE%9F%E6%A9%9F%E3%81%AEssl%E9%80%9A%E4%BF%A1%E3%82%92%E3%83%97%E3%83%AD%E3%82%AD%E3%82%B7%E3%81%AB%E3%82%88%E3%81%A3%E3%81%A6%E5%82%8D%E5%8F%97%E3%81%97%E3%81%9F%E3%82%8A%E6%94%B9%E3%81%96%E3%82%93%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95)  
[MacでWifi共有で透過的にmitmproxy](#mac%E3%81%A7wifi%E5%85%B1%E6%9C%89%E3%81%A7%E9%80%8F%E9%81%8E%E7%9A%84%E3%81%ABmitmproxy)  
[mitmproxyを使ってSSL通信の中身を確認する](#mitmproxy%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6ssl%E9%80%9A%E4%BF%A1%E3%81%AE%E4%B8%AD%E8%BA%AB%E3%82%92%E7%A2%BA%E8%AA%8D%E3%81%99%E3%82%8B)  
[モバイルアプリ開発者のための mitmproxy 入門](#%E3%83%A2%E3%83%90%E3%82%A4%E3%83%AB%E3%82%A2%E3%83%97%E3%83%AA%E9%96%8B%E7%99%BA%E8%80%85%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE-mitmproxy-%E5%85%A5%E9%96%80)  
[mitmproxyでiOSの通信を確認するまで](#mitmproxy%E3%81%A7ios%E3%81%AE%E9%80%9A%E4%BF%A1%E3%82%92%E7%A2%BA%E8%AA%8D%E3%81%99%E3%82%8B%E3%81%BE%E3%81%A7)  

[ubuntu14.04 をアクセスポイントにして透過型プロキシ通す](#ubuntu1404-%E3%82%92%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88%E3%81%AB%E3%81%97%E3%81%A6%E9%80%8F%E9%81%8E%E5%9E%8B%E3%83%97%E3%83%AD%E3%82%AD%E3%82%B7%E9%80%9A%E3%81%99)  
[Installing mitmproxy on Windows Subsystem for Linux (WSL)](#installing-mitmproxy-on-windows-subsystem-for-linux-wsl)  

[APP有用HTTPS傳輸，但資料還是被偷了](#app%E6%9C%89%E7%94%A8https%E5%82%B3%E8%BC%B8%E4%BD%86%E8%B3%87%E6%96%99%E9%82%84%E6%98%AF%E8%A2%AB%E5%81%B7%E4%BA%86)  
[Windows10使用WSL安装mitmproxy进行抓包](#windows10%E4%BD%BF%E7%94%A8wsl%E5%AE%89%E8%A3%85mitmproxy%E8%BF%9B%E8%A1%8C%E6%8A%93%E5%8C%85)  

[Reference](#reference)  
[apt - How do I install mitmproxy on ubuntu 18.0.4](#apt---how-do-i-install-mitmproxy-on-ubuntu-1804)  
[How To: Use mitmproxy to read and modify HTTPS traffic](#how-to-use-mitmproxy-to-read-and-modify-https-traffic)  
[mitmproxy的安装及环境搭建](#mitmproxy%E7%9A%84%E5%AE%89%E8%A3%85%E5%8F%8A%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA)  
[How to configure mitmproxy to intercept https?](#how-to-configure-mitmproxy-to-intercept-https)  

# Modes of Operation in mitmproxy  
[Modes of Operation](https://docs.mitmproxy.org/stable/concepts-modes/#modes-of-operation)  

* Regular (the default)  
* Transparent  
* Reverse Proxy  
* Upstream Proxy  
* SOCKS Proxy  

```
Now, which one should you pick? Use this flow chart:
```
![alt tag](https://docs.mitmproxy.org/stable/schematics/proxy-modes-flowchart.png)  

## Regular Proxy  
```
Mitmproxy’s regular mode is the simplest and the easiest to set up.

1. Start mitmproxy.
2. Configure your client to use mitmproxy by explicitly setting an HTTP proxy.
3. Quick Check: You should already be able to visit an unencrypted HTTP site through the proxy.
4. Open the magic domain mitm.it and install the certificate for your device.
```
```
Unfortunately, some applications bypass the system HTTP proxy settings 
- Android applications are a common example. 
In these cases, you need to use mitmproxy's transparent mode. 
```
```
If you are proxying an external device, your network will probably look like this:
```
![alt tag](https://docs.mitmproxy.org/stable/schematics/proxy-modes-regular.png)  

## Transparent Proxy  
```
In transparent mode, traffic is directed into a proxy at the network layer, 
without any client configuration required. 
This makes transparent proxying ideal for situations where you can’t change client behaviour. 
In the graphic below, a machine running mitmproxy has been inserted between the router and the internet:
```
![alt tag](https://docs.mitmproxy.org/stable/schematics/proxy-modes-transparent-1.png)  

```
The square brackets signify the source and destination IP addresses. 
Round brackets mark the next hop on the Ethernet/data link layer. 
This distinction is important: when the packet arrives at the mitmproxy machine, 
it must still be addressed to the target server. 

This means that Network Address Translation should not be applied before the traffic reaches mitmproxy, 
since this would remove the target information, leaving mitmproxy unable to determine the real destination.
```
![alt tag](https://docs.mitmproxy.org/stable/schematics/proxy-modes-transparent-wrong.png)  

# Install mitmporxy in Ubuntu 18.04 WSL  
## Step 1 remove original mitmproxy package   
```
~$ sudo apt remove mitmproxy
```
![alt tag](https://i.imgur.com/n89qp3v.jpg) 

## Step 2 virtualenv for mitmproxy   
```
$ virtualenv -p /usr/bin/python3 virtualenv/mitmproxy

$ source ~/virtualenv/mitmproxy/bin/activate

$ pip list -l
```
![alt tag](https://i.imgur.com/8myCRHG.jpg) 

## Step 3  pip3 install mitmproxy  
```
$ pip3 install mitmproxy
```
![alt tag](https://i.imgur.com/T7q0dyB.jpg) 
![alt tag](https://i.imgur.com/YwKuZ9k.jpg) 

## Step 4 Check .mitmproxy/  
```
$ls -l .mitmproxy/
```
![alt tag](https://i.imgur.com/aVUqXMP.jpg) 

### CA and cert files  
Test ID | Test Cases
------------------------------------ | ---------------------------------------------
mitmproxy-ca.pem | The certificate and the private key in PEM format.
mitmproxy-ca-cert.pem | The certificate in PEM format. Use this to distribute on most non-Windows platforms.
mitmproxy-ca-cert.p12 | The certificate in PKCS12 format. For use on Windows.
mitmproxy-ca-cert.cer | Same file as .pem, but with an extension expected by some Android devices.

## Step 5 Check mitmproxy   
```
$ mitmproxy --version

Mitmproxy: 4.0.4
Python:    3.6.7
OpenSSL:   OpenSSL 1.1.0i  14 Aug 2018
Platform:  Linux-4.15.0-47-generic-x86_64-with-Ubuntu-18.04-bionic

```

## Step 6 Start mitmproxy   
```
$ mitmproxy -p 8080 -v
```
![alt tag](https://i.imgur.com/LDYd0ji.jpg) 

## Trouble 
![alt tag](https://i.imgur.com/PC607Ku.jpg) 

![alt tag](https://i.imgur.com/CPc7CVU.jpg) 


## Step 6 Start mitmweb  
```
$ mitmweb --web-iface 192.168.1.242
```
![alt tag](https://i.imgur.com/P2ZUcer.jpg) 

![alt tag](https://i.imgur.com/x5HIVzB.jpg) 

## Step 7 Setup Browser Proxy  
![alt tag](https://i.imgur.com/YvWeDO1.jpg) 

## Step 8 Open Browser 
```
keyin http://--web-iface:8081  
```
![alt tag](https://i.imgur.com/k8MVErg.jpg) 

## Step 9 Click to Install Certificate    
![alt tag](https://i.imgur.com/fMzZ70G.jpg) 

![alt tag](https://i.imgur.com/dlr0gu2.jpg)  

![alt tag](https://i.imgur.com/W2Df3Ps.jpg)  

## Step 10 Check Console by SSH  

![alt tag](https://i.imgur.com/9ORfTPV.jpg) 


# 3 mitmproxy Tips You Might Not Know About  
[3 mitmproxy Tips You Might Not Know About ](https://dev.to/kevcui/3-mitmproxy-tips-you-might-not-know-about-5dbg)  

## Tips 1: Custom configuration and key binding  
~/.mitmproxy/config.yaml:
```
console_palette: "dark"
console_palette_transparent: True
console_mouse: False
console_focus_follow: True
ignore_hosts: []
```

~/.mitmproxy/keys.yaml:
```
-
  key: j
  ctx: ["global"]
  cmd: console.nav.up
-
  key: k
  ctx: ["global"]
  cmd: console.nav.down
-
  key: l
  ctx: ["flowlist"]
  cmd: console.nav.select
```
To know more about which command to use in cmd field, type K (shift + k) in mitmproxy.  

## Tips 2: Knowing client connection status when a filter is applied  
```
An easy way is to add | .* in the filter, which will reveal all incoming requests. 
Yep, regex magic:
```
[mitmproxy filter on](https://kevcui.github.io/videos/mitmproxy-filter-on.svg)  


```
Another easy way is to simply type E (shift+e), which will open events logs. 
It shows the client connection status. Use q to quit events view:
```
[mitmproxy events view](https://kevcui.github.io/videos/mitmproxy-events-view.svg)  


## Tips 3: Using mitmproxy as a mock server  
```
Map http://example.com/pass to test_pass.json (terminal on the bottom left)
Create mock response data in test_pass.json (terminal on the bottom right)
Visit http://example.com/pass on the client side
The initial response is now replaced by the one in test_pass.json (terminal on top)
```
![alt tag](https://res.cloudinary.com/practicaldev/image/fetch/s--Rh3qMV5K--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://raw.githubusercontent.com/KevCui/mitm-scripts/master/screenshot/mitm-rewrite-example.jpg)  

[mitm-scripts collection](https://github.com/KevCui/mitm-scripts)  
[some examples](https://github.com/mitmproxy/mitmproxy/tree/master/examples/simple)  


# 使用 mitmproxy + python 做拦截代理  
[使用 mitmproxy + python 做拦截代理 Jun 8, 2018](https://blog.wolfogre.com/posts/usage-of-mitmproxy/)  

## Script  
```
import mitmproxy.http
from mitmproxy import ctx


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)


addons = [
    Counter()
]
```

```
mitmweb -s addons.py
```

```
Web server listening at http://127.0.0.1:8081/
Loading script addons.py
Proxy server listening at http://*:8080
We've seen 1 flows
……
……
We've seen 2 flows
……
We've seen 3 flows
……
We've seen 4 flows
……
……
We've seen 5 flows
……
```
## Event  
### 1. 针对 HTTP 生命周期  
```
def http_connect(self, flow: mitmproxy.http.HTTPFlow):
```
```
def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
```
```
def request(self, flow: mitmproxy.http.HTTPFlow):
```
```
def responseheaders(self, flow: mitmproxy.http.HTTPFlow):
```
```
def response(self, flow: mitmproxy.http.HTTPFlow):
```
```
def error(self, flow: mitmproxy.http.HTTPFlow):
```

### 2. 针对 TCP 生命周期  

### 3. 针对 Websocket 生命周期  
```
def websocket_handshake(self, flow: mitmproxy.http.HTTPFlow):
```
```
def websocket_start(self, flow: mitmproxy.websocket.WebSocketFlow):
```
```
def websocket_message(self, flow: mitmproxy.websocket.WebSocketFlow):
```
```
def websocket_error(self, flow: mitmproxy.websocket.WebSocketFlow):
```
```
def websocket_end(self, flow: mitmproxy.websocket.WebSocketFlow):
```

### 4. 针对网络连接生命周期  

### 5. 通用生命周期  

## Example  
```
需求是这样的：

1. 因为百度搜索是不靠谱的，所有当客户端发起百度搜索时，
    记录下用户的搜索词，再修改请求，将搜索词改为“360 搜索”；

2. 因为 360 搜索还是不靠谱的，所有当客户端访问 360 搜索时，
    将页面中所有“搜索”字样改为“请使用谷歌”。

3. 因为谷歌是个不存在的网站，所有就不要浪费时间去尝试连接服务端了，
    所有当发现客户端试图访问谷歌时，直接断开连接。

4. 将上述功能组装成名为 Joker 的 addon，并保留之前展示名为 Counter 的 addon，都加载进 mitmproxy。
```

```
def request(self, flow: mitmproxy.http.HTTPFlow):
    # 忽略非百度搜索地址
    if flow.request.host != "www.baidu.com" or not flow.request.path.startswith("/s"):
        return

    # 确认请求参数中有搜索词
    if "wd" not in flow.request.query.keys():
        ctx.log.warn("can not get search word from %s" % flow.request.pretty_url)
        return

    # 输出原始的搜索词
    ctx.log.info("catch search word: %s" % flow.request.query.get("wd"))
    # 替换搜索词为“360搜索”
    flow.request.query.set_all("wd", ["360搜索"])
```

```
def response(self, flow: mitmproxy.http.HTTPFlow):
    # 忽略非 360 搜索地址
    if flow.request.host != "www.so.com":
        return

    # 将响应中所有“搜索”替换为“请使用谷歌”
    text = flow.response.get_text()
    text = text.replace("搜索", "请使用谷歌")
    flow.response.set_text(text)
```

```
def http_connect(self, flow: mitmproxy.http.HTTPFlow):
    # 确认客户端是想访问 www.google.com
    if flow.request.host == "www.google.com":
        # 返回一个非 2xx 响应断开连接
        flow.response = http.HTTPResponse.make(404)
```

joker.py
```
import mitmproxy.http
from mitmproxy import ctx, http


class Joker:
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host != "www.baidu.com" or not flow.request.path.startswith("/s"):
            return

        if "wd" not in flow.request.query.keys():
            ctx.log.warn("can not get search word from %s" % flow.request.pretty_url)
            return

        ctx.log.info("catch search word: %s" % flow.request.query.get("wd"))
        flow.request.query.set_all("wd", ["360搜索"])

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host != "www.so.com":
            return

        text = flow.response.get_text()
        text = text.replace("搜索", "请使用谷歌")
        flow.response.set_text(text)

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host == "www.google.com":
            flow.response = http.HTTPResponse.make(404)
```

counter.py
```
import mitmproxy.http
from mitmproxy import ctx


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)

```

addons.py 
```
import counter
import joker

addons = [
    counter.Counter(),
    joker.Joker(),
]

```

```
mitmweb -s addons.py
```


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

## iOS  
```
iOS の場合は、
「設定」
→「Wi-fi」に行って、いま接続しているネットワークをタップ 
→ 「HTTPプロキシ」でプロキシの設定ができます。
設定項目には以下を入力します。なお、ポート番号はデフォルトで 8080 ですが、
後述のようにプロキシサーバー起動時に別の番号を指定可能です。

    サーバー：自分のマシンの IP アドレス
    ポート番号：8080
    認証：オフ
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F224%2F36306%2F23b998e2-9a81-5511-2ab5-8aa43e6daf47.png?ixlib=rb-1.2.2&auto=compress%2Cformat&gif-q=60&w=1400&fit=max&s=54e30fc840cca36ec653d62cad55befd)  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F224%2F36306%2F4423ea25-a70f-fa2f-5f32-713c696c6f2b.png?ixlib=rb-1.2.2&auto=compress%2Cformat&gif-q=60&s=0745cea60fc15b8bc36046bf8689a691)  

## Andorid  
```
Android の場合は、
「設定」
→「Wi-Fi」に行って、いま接続しているネットワークを長押し 
→「ネットワークを変更」をタップして、
開いたダイアログの「詳細オプションを表示」のチェックボックスにチェックを入れるとプロキシ設定の入力欄が表示されます。
設定項目については、iOS と同じなので省略します。
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F224%2F36306%2F9440dca1-77a2-2020-0b96-39cdb1402253.png?ixlib=rb-1.2.2&auto=compress%2Cformat&gif-q=60&s=d4a796a112d7be5cf189df8f8f8a3fed)  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F224%2F36306%2F5e55593d-d769-2666-b081-11de9ef26dfe.png?ixlib=rb-1.2.2&auto=compress%2Cformat&gif-q=60&s=9fa3185ead0247626dd7072b76e7ac22)  


# mitmproxyでiOSの通信を確認するまで  
[mitmproxyでiOSの通信を確認するまで Aug 25, 2017](https://qiita.com/wtotw/items/69290b178371c4d7cf76)  
## 証明書を有効にする  
```
設定>一般>情報>証明書信頼設定>mitmproxyのところをオンにする。
いろんなサイト見たけど何故か書いてなかった。
```

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


# APP有用HTTPS傳輸，但資料還是被偷了  
[APP有用HTTPS傳輸，但資料還是被偷了。Sep 20, 2019](https://medium.com/zrealm-ios-dev/app%E6%9C%89%E7%94%A8https%E5%82%B3%E8%BC%B8-%E4%BD%86%E8%B3%87%E6%96%99%E9%82%84%E6%98%AF%E8%A2%AB%E5%81%B7%E4%BA%86-46410aaada00)  

```
實際操作
環境: MacOS + iOS
```

## 讓手機跟Mac在同個區域網路內&取得Mac的IP位址  
```
方法(1) Mac 連接 WiFi、手機也使用同個 WiFi
Mac的IP位址 = 「系統偏好設定」->「網路」->「Wi-Fi」->「IP Address」

方法(2) Mac 使用有線網路，開啟網路分享；手機連上該熱點網路:
```
![alt tag](https://miro.medium.com/max/598/1*R9fthpHlrWzTh4R3fEwO5Q.gif)

Mac的IP位址 = 192.168.2.1 （️️注意⚠️ 不是乙太網路網路的IP，是Mac用做網路分享基地台的IP) 

## 手機網路設置WiFi — Proxy伺服器資訊  
![alt tag](https://miro.medium.com/max/1369/1*ziIFrGQaMr2kYrQHwLYNJg.jpeg)  

> 這時網頁打不開、出現憑證錯誤是正常的；我們繼續往下做… 

## 安裝 mitmproxy 自訂 https 憑證  
```
如同上述所說，中間人攻擊的實現方式就是在通訊之中使用自己的憑證做抽換加解密資料；所以我們也要在手機上安裝這個自訂的憑證。

1.用手機safari打開 http://mitm.it
```
![alt tag](https://miro.medium.com/max/2730/1*qKDHxi9HxUP41oDJahBfBA.jpeg)  

> ⚠️到這裡還沒結束，我們還要去關於裡啟用描述檔  

![alt tag](https://miro.medium.com/max/1369/1*mOijblpQepazFPIwob4r8Q.jpeg)  
```
完成！這時我們再回去瀏覽器就能正常瀏覽網頁了。
```
## 回到Mac 上操作 mitmproxy  
![alt tag](https://miro.medium.com/max/611/1*kiEPaTm5bhnFLBfQngQPgA.png)  

![alt tag](https://miro.medium.com/max/661/1*5I6l9cO3LeXfcwGLpWGKPQ.gif)  


# Windows10使用WSL安装mitmproxy进行抓包  
[Windows10使用WSL安装mitmproxy进行抓包 Jun 9, 2018](https://juejin.im/post/5b05336d5188252ab653e84b)  
## 1. Windows10启用Linux系统支持   
## 2. 使用python安装mitmproxy。  
## 3. Ubuntu安装证书：   
[how-do-i-install-a-root-certificate edited Oct 10 2013](https://askubuntu.com/questions/73287/how-do-i-install-a-root-certificate/94861#94861)  
```
1. 转换mitmproxy-ca-cert.pem格式文件为对应的mitmproxy-ca-cert.crt格式文件，输入命令：
openssl x509 -in mitmproxy-ca-cert.pem -inform PEM -out mitmproxy-ca-cert.crt

2. 在**/usr/share/ca-certificates**创建一个额外的目录：sudo mkdir /usr/share/ca-certificates/extra

3. 复制转换好的mitmproxy-ca-cert.crt文件到刚才创建的目录中：sudo cp mitmproxy-ca-cert.crt /usr/share/ca-certificates/extra/mitmproxy-ca-cert.crt

4. 让Ubuntu将.crt文件相对于/usr/share/ca-certificates的路径添加到/etc/ca-certificates.conf文件里面：sudo dpkg-reconfigure ca-certificates回车后需要输入用户密码。

5. 会弹出一个框：
```
![alt tag](https://user-gold-cdn.xitu.io/2018/6/9/163e51ef46753404?imageslim)

```
回车确定后再弹出一个框： 
```
![alt tag](https://user-gold-cdn.xitu.io/2018/6/9/163e51f45e2b0e63?imageslim)

```
使用空格将刚才添加的mitmproxy-ca-cert.crt证书勾选上，如上图所示，然后回车确定，等待系统更新证书信息 
```
![alt tag](https://user-gold-cdn.xitu.io/2018/6/9/163e5226807dc8c0?imageslim)

```
6. 然后启动mitmproxy，在Ubuntu终端里面输入mitmproxy, 运行截图如下： 
```
![alt tag](https://user-gold-cdn.xitu.io/2018/6/9/163e53f51d280a79?imageslim)

## 4. 手机安装证书：  
## 取消代理  
```
对了！当你停止了mitmporxy程序后记得取消你设置的代理！！！！！
不然到时打不开网页不要怪我没提醒你噢！
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
## apt - How do I install mitmproxy on ubuntu 18.0.4  
* [apt - How do I install mitmproxy on ubuntu 18.0.4 Sep 23, 2019](https://askubuntu.com/questions/1176109/how-do-i-install-mitmproxy-on-ubuntu-18-0-4)  
```
Firstly, run the following command in the terminal to remove apt installed mitmproxy package:

sudo apt remove mitmproxy
```

```
Secondly, install PIP3 if it is not installed by running the following command in the terminal:

sudo apt install python3-pip

Or update it if it is already installed by running the following command in the terminal:

sudo pip3 install -U pip
```

```
Thirdly, install mitmproxy via PIP3 by running the following command in the terminal:

sudo pip3 install mitmproxy
```

```
Finally, type mitmproxy in the terminal and press Enter to start it.
```

## How To: Use mitmproxy to read and modify HTTPS traffic  
* [How To: Use mitmproxy to read and modify HTTPS traffic Jul 1, 2013](https://blog.heckel.io/2013/07/01/how-to-use-mitmproxy-to-read-and-modify-https-traffic-of-your-phone/)  

![alt tag](https://d3u5jkmuxaiujc.cloudfront.net/wp-content/uploads/2013/07/mitmproxy-example.png)  

```
2.3. Enable IP forwarding and port redirection ¶

The mitmproxy application internally runs on TCP port 8080, but externally has to listen 
on ports 80/HTTP and 443/HTTPS. 
Therefore, a IP forwarding in general (the system must act as a router) and 
a redirection from 8080 to 80 and 443 is necessary for all arriving IP packets. 
The “nat” table of iptables can be used to do that pretty easily. 

This is also described in the Linux section of the mitmproxy manual.

1 sysctl -w net.ipv4.ip_forward=1
2 iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
3 iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8080

It’s not clear to me why the application does not simply bind to the ports 80 and 443 ports, but that’s how it is right now.
```

## mitmproxy的安装及环境搭建  
[mitmproxy的安装及环境搭建 2018-09-09](https://blog.csdn.net/u014229742/article/details/82562571)  
```
所以可以确定，我们代理IP端口号为8080，于是，在手机Wifi设置手动代理，输入本机IP和端口号8080。此时，
打开mitmproxy界面并操作手机，可以看到手机请求信息：
```
![alt tag](https://img-blog.csdn.net/20180909211617650?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQyMjk3NDI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)  

* [window上MitmProxy的安装 2018-10-17](https://blog.csdn.net/supramolecular/article/details/83104211)  
```
下载之后直接双击安装包即可安装。
注意在 Windows 上不支持 MitmProxy 的控制台接口，但是可以使用 MitmDump 和 MitmWeb。
```

## How to configure mitmproxy to intercept https?  
[How to configure mitmproxy to intercept https? Feb 26, 2018](https://serverfault.com/questions/898919/how-to-configure-mitmproxy-to-intercept-https)  
```
The web gui is very comfortable. You can use mitmproxy instead.

1. Run the proxy server $ mitmweb --listen-port 44700
    Make sure that 44700 port is open in firewall. 
    You can specify the IP of proxy with --listen-host flag. 
    I.E. --listen-host 192.168.0.10 or try --listen-host 0.0.0.0 if can not access remotely.

2. Configure in the remote device the IP and port proxy.

3. Open browser in the remote device and go to http://mitm.it, is a local page, 
    in a local DNS, that you can download and install the certs.
    If android, you must specify a pin lock screen.

4. Open web gui, by default in port 8081 in your browser: http://127.0.0.1:8081/#/flows

    Enjoy networks intercepts.
```

## Ubuntu（mint）下fiddler进行http抓包Chrome遇到的问题  
[Ubuntu（mint）下fiddler进行http抓包Chrome遇到的问题 Mar 14, 2018](https://blog.csdn.net/saonianpai/article/details/79553439)  
```
2、获取mitmproxy证书

    打开mitmproxy，Chrome设置好代理，进入”mitm.it“，如果出现”If you can see this, traffic is not passing through mitmproxy.“说明没有设置好代理。设置好代理后，正常进入网站后选择你的操作系统，证书开始下载。
```

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