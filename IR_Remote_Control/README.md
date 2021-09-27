Table of Contents
=================

   * [Purpose](#purpose)
   * [IoT 家中の赤外線リモコン製品をpythonから操作する。](#iot-家中の赤外線リモコン製品をpythonから操作する)
      * [準備(接続)](#準備接続)
      * [ライブラリを導入します。](#ライブラリを導入します)
      * [リモコンの赤外線コードの取得](#リモコンの赤外線コードの取得)
      * [コンピュータからテレビの電源をONする。](#コンピュータからテレビの電源をonする)
   * [mjg59 / python-broadlink](#mjg59--python-broadlink)
      * [Example use](#example-use)
   * [python-broadlinkでRM mini3をコントロール[on Onion Omega2 ]](#python-broadlinkでrm-mini3をコントロールon-onion-omega2)
      * [0.前提条件](#0前提条件)
      * [1.必要なパッケージをインストール](#1必要なパッケージをインストール)
      * [2.python-broadlinkのインストール](#2python-broadlinkのインストール)
      * [3.python-broadlinkをセットアップする](#3python-broadlinkをセットアップする)
      * [4.リモコン設定と制御](#4リモコン設定と制御)
   * [黒豆 (Broadlink RM Mini 3) の IR 信号解析してみたよ♪](#黒豆-broadlink-rm-mini-3-の-ir-信号解析してみたよ)
      * [送信コードが分かると何が嬉しいの・・・？](#送信コードが分かると何が嬉しいの)
      * [参考情報](#参考情報)
         * [IR コードについての基礎知識](#ir-コードについての基礎知識)
         * [家製協フォーマットの詳細](#家製協フォーマットの詳細)
         * [エアコンのIR信号](#エアコンのir信号)
         * [いろんな IR コマンドのデータベース](#いろんな-ir-コマンドのデータベース)
         * [Philips Prontoコードを黒豆コードに変換するサンプル](#philips-prontoコードを黒豆コードに変換するサンプル)
      * [■送信コードの解析結果](#送信コードの解析結果)
      * [■実践編](#実践編)
   * [smartHomeHub / SmartIR](#smarthomehub--smartir)
   * [eschava / broadlink-mqtt](#eschava--broadlink-mqtt)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose  
Take some notes of IR Remote Control

# IoT 家中の赤外線リモコン製品をpythonから操作する。
[IoT 家中の赤外線リモコン製品をpythonから操作する。updated at 2019-01-10](https://qiita.com/hiratarich/items/cc2a5c42e21e408e1316)

## 準備(接続) 
**wifiから制御するためにssid/passwordをセットする**
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F274715%2F7a84db8c-01b2-d47d-ce62-9a4bf1084690.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=e6424176cd255cd147aec061f97c0b04" width="700" height="200">  

## ライブラリを導入します。  
**pip install broadlink**
[Python control for Broadlink devices](https://github.com/mjg59/python-broadlink)

```
discover.py
```

```
import broadlink
broadlink.setup('myssid', 'mynetworkpass', 3)
dev = broadlink.discover(timeout=5)
net=[]
for d in dev:
    d.auth()
    n=dict(type=d.get_type(),ip=d.host[0],port =d.host[1],
             mac = "-".join([format(x,"02x") for x in [x for x in reversed(d.mac)]]),
             timeout = d.timeout)
    net.append(n)
print(net)
```

```
[{'type': 'RM2', 'ip': '192.168.1.102', 'port': 80, 'mac': '78-xx-77-xx-xx-xx', 'timeout': 10}]
```

## リモコンの赤外線コードの取得  
<img src="https://camo.qiitausercontent.com/9cabb524274f7cbe7267e9aea65af0d213497c48/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3237343731352f32623636383164642d653063612d666336312d363061362d3261343339396666363730342e706e67" width="700" height="200">  

**制御に必要な赤外線リモコンのボタンを表示する。**
**これらをデータベース化すれば制御するためのデータとなる。**
**ボタンを押し続けると赤外線コードを出し続けるのでオペレーションするときに注意する。**

```
getCode.py
```

```
import broadlink,pyperclip,netaddr,time,binascii,json,sys
net={'type': 'RM2', 'ip': '192.168.1.102', 'port': 80, 'mac': '78-xx-xx-xx-xx-xx', 'timeout': 10}
lb,text='ontv','OnTv'
RM3 = broadlink.rm((net["ip"], net["port"]),netaddr.EUI(net["mac"]),net["timeout"])
RM3.auth()
RM3.enter_learning()
while True:
    cmd= RM3.check_data()
    if cmd is None: continue
    else:
        break
d={"IR":cmd.hex(),"name":text,"lb":lb}
print(json.dumps(d))

```

**赤外線リモコンのボタンを押すと下記の結果が得られる。**
```
{"IR": "260002017438110c0f0d1029102a100c102a100c100d100c102a100c100d1029100d1029100d0f2a100d0f0d1029110c100c100d100c100d
100c102a0f0d102a0f2a100d0f0d1029100d1029102a1029102a100c100d100009a77438100d100c102a0f2a100d0f28130c0f0d100d0f2a100c100d
1029100d1029100d1029100d100c102a0f0d100d0f0d100d0f0d100c1028120c102a1029100d100c102a100c102a0f2a102a0f2a100d0f0d100009a6
7737100c100c11291128110c1128100d110b110c1128110c100c1129110b1129100c1128110c110c1029110b110c110c100c110c100c1128110c1128
1129110b110c1128110b1129112811291128120b110c10000d05000000000000", "name": "OnTv", "lb": "ontv"}
```

## コンピュータからテレビの電源をONする。  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F274715%2F9b25b69f-05df-ce8d-f1f5-65010772009b.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=e6b143ed203c703429207370cab38193" width="700" height="200">  

```
sendIR.py
```

```
import broadlink,pyperclip,netaddr,time,binascii,json,sys
cmd={"IR": "260002017438110c0f0d1029102a100c102a100c100d100c102a100c100d1029100d1029100d0f2a100d0f0d1029110c100c100d100c100d100c102a0f0d102a0f2a100d0f0d1029100d1029102a1029102a100c100d100009a77438100d100c102a0f2a100d0f28130c0f0d100d0f2a100c100d1029100d1029100d1029100d100c102a0f0d100d0f0d100d0f0d100c1028120c102a1029100d100c102a100c102a0f2a102a0f2a100d0f0d100009a67737100c100c11291128110c1128100d110b110c1128110c100c1129110b1129100c1128110c110c1029110b110c110c100c110c100c1128110c11281129110b110c1128110b1129112811291128120b110c10000d05000000000000", "name": "OnTv", "lb": "ontv"}

net={'type': 'RM2', 'ip': '192.168.1.102', 'port': 80, 'mac': '78-0f-77-1a-31-a0', 'timeout': 10}
RM3= broadlink.rm((net["ip"], net["port"]),netaddr.EUI(net["mac"]),net["timeout"])
RM3.auth()
RM3.send_data(bytearray.fromhex(cmd['IR']))
```


# mjg59 / python-broadlink 
[Python control for Broadlink devices](https://github.com/mjg59/python-broadlink)

## Example use  
**Setup a new device on your local wireless network:**
**1. Put the device into AP Mode**
**2. Long press the reset button until the blue LED is blinking quickly.**
**3. Long press again until blue LED is blinking slowly.**
**4. Manually connect to the WiFi SSID named BroadlinkProv.**
**5. Run setup() and provide your ssid, network password (if secured), and set the security mode**
**6. Security mode options are (0 = none, 1 = WEP, 2 = WPA1, 3 = WPA2, 4 = WPA1/2)**


**You may need to specify local_ip_address or discover_ip_address if discovery does not return any devices. Using your machine's IP address with local_ip_address**

```
import broadlink
devices = broadlink.discover(timeout=5, local_ip_address='192.168.0.100')
```

**Using your subnet's broadcast address with discover_ip_address**
```
import broadlink
devices = broadlink.discover(timeout=5, discover_ip_address='192.168.0.255')
```


# python-broadlinkでRM mini3をコントロール[on Onion Omega2+]  
[python-broadlinkでRM mini3をコントロール[on Onion Omega2+] updated at 2018-11-17](https://qiita.com/spiderx_jp/items/8f04019c83fabdc336d4)


## 0.前提条件  
```
    RM mini3は、セットアップしてローカルwifi環境に接続済
        私は、Broadlink e-Control Appを使用してiPhoneから設定しました。
    python-broadlink
    pycryptodomex-3.4.11の代わりにpython-crypto-2.6.1-1を使用
```

## 1.必要なパッケージをインストール  
```
Omega2+にtelnetまたはシリアル通信で接続します。
以下のコマンドで必要なパッケージをインストールします。
今回、pycryptodomexの代わりにpython-cryptoを使用するので、python-cryptoもインストールします。
※pycryptodomexは、opkgで提供されていません（2018/09現在）。
```

```
$ opkg update
$ opkg install git git-http ca-bundle python-crypto python-pip
$ pip install setuptools
```

## 2.python-broadlinkのインストール 
**githubからpython-broadlinkをダウンロードします。**
```
$ cd /root
$ git clone https://github.com/mjg59/python-broadlink.git
```

**setup.pyは、pycryptodomexをインストールするような記述となっています。**
**今回、pycryptodomexの代わりにpython-cryptoを使用するため、setup.pyを編集してpycryptodomexのインストールが無効になりようにします。**

```
$ cd python-broadlink
$ vi setup.py
```

**dynamic_requires の部分を以下のように変更します。**
**※try:の中で import pyaesがありますが、Omega2+では、エラーになるので、except:側が実行されます。**

```
setup.py
```

```
try:
    import pyaes
    dynamic_requires = ["pyaes==1.6.0"]
except ImportError as e:
    dynamic_requires = []
    #dynamic_requires = ['pycryptodome==3.4.11']

```

```
$ python setup.py install
```

## 3.python-broadlinkをセットアップする  
**まずは、ネットワーク上からRM mini3を探します。**
**「./broadlink_discovery」コマンドを実行すると、RM mini3をネットワーク上から探してくれます。**

```
$ cd ~/python-broadlink/cli
$ ./broadlink_discovery
Discovering...
###########################################
RM2
# broadlink_cli --type 0x2737 --host 192.168.1.32 --mac 25xxxxxxxxxx
Device file data (to be used with --device @filename in broadlink_cli) :
0x2737 192.168.1.32 25xxxxxxxxxx
temperature = 0.0
```

**「0x2737 192.168.1.32 25xxxxxxxxxx」をファイル ROOM.device に格納します。**
```
$ echo "0x2737 192.168.1.32 25xxxxxxxxxx" > ROOM.device
```

## 4.リモコン設定と制御  
**制御したい赤外線リモコンを用意します。**
**私は、リビングのリーリングライトを制御してみます。**
**以下のコマンドで FLOOR_LIGHT.on というファイルにリモコンの制御コマンドをダンプします。「Learning...」と表示されたら、RM mini3 目がけてリモコンでスイッチONします。**
```
$ ./broadlink_cli --device @ROOM.device --learnfile FLOOR_LIGHT.on
Learning...
Saving to FLOOR_LIGHT.on
```

**以下のようにダンプされていることが確認できます。**
```
$ cat FLOOR_LIGHT.on
2600580000012a91160f16341610151015101510151016341634160f16351535151015351634160f160f16351510151015101634160f163416351510153515351634160f163515101500054c00012a4815000c6700012a4815000d05
```

**OFFのリモコン制御コマンドもダンプします。**
```
$ ./broadlink_cli --device @ROOM.device --learnfile FLOOR_LIGHT.off
Learning...
Saving to FLOOR_LIGHT.off
$ cat FLOOR_LIGHT.off
26006000000128931411143614121312131213121411143614361412133713371312143614361411141213371337143614361436141213371337131214111411160f1411163515101500054c00012b4715000c6700012a4716000c6600012b4716000d050000000000000000
```

**準備が整いました。**
**以下のコマンドで、シーリングライトをONできると思います。**
```
$ ./broadlink_cli --device @ROOM.device --send @FLOOR_LIGHT.on
```

**OFFの場合も同じように以下のコマンドを実行します。**
```
$ ./broadlink_cli --device @ROOM.device --send @FLOOR_LIGHT.off
```




# 黒豆 (Broadlink RM Mini 3) の IR 信号解析してみたよ♪  
[黒豆 (Broadlink RM Mini 3) の IR 信号解析してみたよ♪](https://qiita.com/kt-sz/items/1c36a7b22a58359a8e6f)  

## 送信コードが分かると何が嬉しいの・・・？  
```
送信コード仕様が分かると・・・

・他の IR デバイス向けに公開されている多くの機器の IR コードを変換して使ったり
・本来の仕様の通りの綺麗な波形に整形＆送信して対象機器側の認識率をUPさせたり
・隠しコードの調査をしたり
　（例えばTVだと実は On/Off 個別にコードあるのでそれを探したり）

などなど、単に黒豆で信号学習するだけでなく、赤外線信号で色々遊べるようになります ：D

※それでも意味が分からない？と言う方のためにこのページの後半に実践編を載せました。
　この記事で掲載している解析データをどうやって活用するか具体例でご紹介しています。
```

## 参考情報  
### IR コードについての基礎知識  
[http://shrkn65.nobody.jp/remocon/index.htm](http://shrkn65.nobody.jp/remocon/index.htm)
[https://watenoblog.blogspot.jp/2014/01/irkitjson.html](https://watenoblog.blogspot.jp/2014/01/irkitjson.html)
[http://www.asahi-net.or.jp/~gt3n-tnk/IR_TX1.html](http://www.asahi-net.or.jp/~gt3n-tnk/IR_TX1.html)
[http://elm-chan.org/docs/ir_format.html](http://elm-chan.org/docs/ir_format.html)

### 家製協フォーマットの詳細  
[http://shrkn65.nobody.jp/remocon/panasonic_bsd.htm](http://shrkn65.nobody.jp/remocon/panasonic_bsd.htm)

### エアコンのIR信号  
[https://raspibb2.blogspot.jp/2016/06/raspberry-pilirc.html](https://raspibb2.blogspot.jp/2016/06/raspberry-pilirc.html)

### いろんな IR コマンドのデータベース  
[http://www.256byte.com/remocon/iremo_db.php](http://www.256byte.com/remocon/iremo_db.php) 
[http://bit-trade-one.co.jp/blog/20171225-2/](http://bit-trade-one.co.jp/blog/20171225-2/) 
[http://www.remotecentral.com/cgi-bin/codes/](http://www.remotecentral.com/cgi-bin/codes/) 

### Philips Prontoコードを黒豆コードに変換するサンプル  
```
今回の解析はこちらの情報をベースに独自の解析を加えたものです。
※中間コードのLIRC形式はオン/オフを　Micro Sec で示したものの様です。
```
[https://gist.github.com/appden/42d5272bf128125b019c45bc2ed3311f#file-pronto2broadlink-py-L10](https://gist.github.com/appden/42d5272bf128125b019c45bc2ed3311f#file-pronto2broadlink-py-L10)


## ■送信コードの解析結果   
[http://shrkn65.nobody.jp/remocon/panasonic_bsd.htm](http://shrkn65.nobody.jp/remocon/panasonic_bsd.htm)
```
以上が家製協フォーマットを例にした場合の黒豆のIRコードの仕様ですが、上記リンクや

の内容と何度も見比べながら読むと理解しやすいと思います

以下のリーダー～トレーラー２までの数値は大体近い値ならIR信号としては有効です。実際に黒豆で学習した IR 信号も以下と全く同じではなく近い数値になっていることが多いです。
以下は赤外線リモコン規格上の理想的な数値・波形に近いので、実際にリモコンから学習したコマンドも、この数値に書き換えて送信すると機器側の認識精度が上がる場合があります。
```

## ■実践編
[http://itline.jp/~svx/diary/?date=20110612](http://itline.jp/~svx/diary/?date=20110612)
[https://qiita.com/yamori813/items/9a6587bc22e8f61ce182](https://qiita.com/yamori813/items/9a6587bc22e8f61ce182)


# smartHomeHub / SmartIR 
[smartHomeHub /SmartIR ](https://github.com/smartHomeHub/SmartIR)  

#  eschava / broadlink-mqtt
[eschava / broadlink-mqtt](https://github.com/eschava/broadlink-mqtt#rm2rm3rm4)


** **

* []()  

![alt tag]()
<img src="" width="" height="">  

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



