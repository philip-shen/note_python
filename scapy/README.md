# Purpose
Take note of Scapy  

# Table of Contents  
[Installation On Windows](#installation-on-windows)  
[Step 1 Install python2.7 on Windows](#step-1-install-python2.7-on-windows)  
[Step 2 Install scapy](#step-2-install-scapy)  
[Step 3 Check Installation and Excute scapy](#step-3-check-installation-and-excute-scapy)  
[Step 4 Capture Packets by WiFi Client](#step-4-capture-packets-by-wifi-client)  

[Reference](#reference)  

# Installation On Windows  
[Installation On Windows](https://scapy.readthedocs.io/en/latest/installation.html#windows)  
```
You need the following software in order to install Scapy on Windows:

    * Python: Python 2.7.X or 3.4+. After installation, add the Python installation directory and its Scripts subdirectory to your PATH. Depending on your Python version, the defaults would be C:\Python27 and C:\Python27\Scripts respectively.
    * Npcap: the latest version. Default values are recommended. Scapy will also work with Winpcap.
    * Scapy: latest development version from the Git repository. Unzip the archive, open a command prompt in that directory and run python setup.py install.
```

## Step 1 Install python2.7 on Windows  
[Installing python2.7 hosts on python3.6 Laptop](https://github.com/philip-shen/note_python#installing-python27-hosts-on-python36-laptop)  

## Step 2 Install scapy  
```
d:\project\
(pholus) λ git clone https://github.com/secdev/scapy.git
```
```
d:\project\
(pholus) λ cd scapy

d:\project\scapy\
(pholus) λ python setup.py install

d:\project\scapy\
(pholus) λ pip install cryptography

d:\project\scapy\
(pholus) λ pip install ipython

d:\project\scapy\
(pholus) λ pip install matplotlib
```

## Step 3 Check Installation and Excute scapy  
```
d:\project\scapy (master -> origin)
(pholus) λ pip list -l
DEPRECATION: Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Package    Version
---------- -----------
asn1crypto                         0.24.0
backports.functools-lru-cache      1.5
backports.shutil-get-terminal-size 1.0.0
cffi                               1.12.3
colorama                           0.4.1
cryptography                       2.7
cycler                             0.10.0
decorator                          4.4.0
enum34                             1.1.6
ipaddress                          1.0.22
ipython                            5.8.0
ipython-genutils                   0.2.0
kiwisolver                         1.1.0
matplotlib                         2.2.4
numpy                              1.16.5
pathlib2                           2.3.4
pickleshare                        0.7.5
pip                                19.2.3
prompt-toolkit                     1.0.16
pycparser                          2.19
Pygments                           2.4.2
pyparsing                          2.4.2
python-dateutil                    2.8.0
pytz                               2019.2
scandir                            1.10.0
setuptools                         41.2.0
simplegeneric                      0.8.1
six                                1.12.0
traitlets                          4.3.2
wcwidth                            0.1.7
wheel                              0.33.6
win-unicode-console                0.5
```

```
d:\project\scapy (master -> origin)
(pholus) λ run_scapy_py2.bat
```
```
>>> s=IP(dst="google.com")/ICMP()
>>> s.show()
```
![alt tag](https://i.imgur.com/JtERE1Y.jpg)

## Step 4 Capture Packets by WiFi Client
```
d:\project\scapy (master -> origin)
(pholus) λ netsh wlan sh int

d:\project\scapy (master -> origin)
(pholus) λ run_scapy_py2.bat
```
![alt tag](https://i.imgur.com/uHF31NQ.jpg)

# Troubleshooting


# Reference  
* [Scapy入門 2019-06-14](https://qiita.com/shoooooo/items/4080752d0d8c7a9ef2aa)  
```
注意

scapyはroot権限がないと実行できないです
```
```
パケットの作り方

    Ethernetパケット
        Ether()
    IPパケット
        IP()
    TCPパケット
        TCP()
    ARPパケット
        ARP()
    DNSパケット
        DNS()
```
```
複数のレイヤのパケットの作り方

    "/"で区切るだけ
        Ether()/IP()/TCP()
```
* [Python不慣れな人が書いた Scapy メモ 2019-07-15](https://qiita.com/ken_hamada/items/736e1c22f6c40702d1a7)  
```

```
* [python3+scapy 2018-03-16](https://qiita.com/komo/items/4da7acb07fdddfb3eb4d)  
```
scapy-python3というライブラリを使う必要がありました。さらにこのscapy-python3、
微妙に更新が遅いのかIPv6周りのバグが残ったままの様子……。

またこちらUbuntu 16.04での話となりますのでご注意ください
```
```
 send_udp.py

import scapy.all as scapy

packet = scapy.IPv6(dst='2001:1:1:11::2', src='2001:1:1:11::555')
packet.show()
scapy.send(packet/scapy.UDP())
```

* [scapy IPv6 2016-09-01](https://qiita.com/kwi/items/bcc158cbcd0aa943f92b)  
```
備忘録的な。

Router solicit

DHCPv6 solicit には client-id が必須(RFC 3351)

DHCPv6 solicit, advertise, request, reply とつなげるとこんな感じ。dnsmasq はとりあえず応答してくれる。

Cisco は DHCPv6_Solicit に DHCP6OptIA_NA が無いと、応答しない。RFC 3351 の記述をそのまま実行すると付くことになる（いちおう validation では要求されていない）。

さらに DHCPv6-RelayForward, RelayReply をする。下の例の src アドレスは stateful に割り当てられた時の値を抜き出している。slaac 使ってる場合は、手元で計算していれるべし。
```
* [Scapy入門①（Scapyのインストールから実行まで） 2017-09-23](https://qiita.com/akakou/items/f17cc50b9891d8105d86)  
```
Scapyのインストール

pipを使ってインストールします。
$ sudo pip3 install scapy-python3
Scapyの起動

私の環境だと、パケット送信のときにパーミッションが必要だったのでsudoをつかって起動します。
$ sudo scapy

Pythonモジュールとしての使用

一行目で以下のコードを実行することで、scapyを直接起動した状態と同じ状態を作ることができます。
ファイルに保存されたスクリプトとして使用する場合は、こちらを使いましょう。

# Scapyのインポート
from scapy.all import *
```
* [Scapy入門②（Scapyを使ったICMP、HTTP(TCP)送信） 2017-09-24](https://qiita.com/akakou/items/eaffe038feeb66f2cf8a)  
```
ICMP(PING)

# googleのサーバに向けたICMPパケットの作成
# IPパケットの上にICMPを積んでいるイメージ
packet = IP(dst='www.google.com')/ICMP()

# パケットの中身を表示
packet.show()

# パケットを送信
# ＆ 返ってきたパケットの表示
sr1(packet)

TCP(HTTP)
コネクションから送信まで

'''TCPにおけるコネクションの流れ'''

'''基本パケットの作成'''
# IPパケットの作成
ip = IP(dst='www.google.com')

# TCP(HTTP)パケットの作成
# sport, seqは適当 
# dportは標準である80版ポート, flagは'S'
tcp = TCP(sport=50000,dport=80,flags='S',seq=100)


'''3ハンドシェイクの実装'''
# SYNパケットの作成
syn= ip/tcp
# SYNパケットの送信
# ＆ SYN ACKの受取
syn_ack = sr1(syn)

'''HTTPリクエストの作成(ACKパケットの作成)'''
# ACKパケットの設定
tcp.seq += 1
tcp.ack = syn_ack.seq + 1
# ACKパケットのflagは'A'
tcp.flags = 'A'
# ACKパケット送信
ack = ip/tcp
send(ack)

# HTTP GETのパケットを乗っける
get = 'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n' 
http = ip/tcp/get
# リクエスト送信
response = sr(http, multi=1, timeout=1)
tcp.seq += len(get)

# レスポンスの表示
response[0][1][1]["Raw"].load

コネクションを切る

'''コネクションを切る'''
# 上記のコードの続き

# FAフラグを持ったFINACKパケットの送信
tcp.flags = 'FA'
fin_ack = sr1(ip/tcp)
tcp.seq += 1

# 最後にACKを返す
tcp.ack = fin_ack.seq + 1
tcp.flags = 'A'
send(ip/tcp)

```

* [Scapyでパケット解析の練習、その１ 2019-05-10](https://qiita.com/kiwamizamurai/items/9bb8f547ce6051792f2a)  
```
パケット解析を勉強したい。そんな時に見つけたけどレイヤとかまだ全然わからんからどんどん勉強していく。

    https://github.com/secdev/scapy
    https://blogs.sans.org/pen-testing/files/2016/04/ScapyCheatSheet_v0.2.pdf
    https://www.cybrary.it/0p3n/sniffing-inside-thread-scapy-python/
    https://qiita.com/akakou/items/eaffe038feeb66f2cf8a#_reference-0ce0659e05b30493e912
```
* [python3+scapy 2018-03-16](https://qiita.com/komo/items/4da7acb07fdddfb3eb4d)  
```

```



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
