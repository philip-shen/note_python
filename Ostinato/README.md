# Purpose
Take note of Ostinato  

# Table of Contents  
[Software-Based Traffic Generators using Docker](#software-based-traffic-generators-using-docker)  

# Software-Based Traffic Generators using Docker  
* [An Evaluation of Software-Based Traffic Generators using Docker SWEDEN2018 SAI MAN WONG](http://www.nada.kth.se/~ann/exjobb/sai-man_wong.pdf)  
```  
4.3.3  OstinatoOstinato is compatible with Windows, Linux, BSD and macOS [22, 60]. This tool issimilar to Mausezahn as it can craft, generate and analyze packets. Also, Ostinatosupports protocols from layer 2 to 7, for example, Ethernet/802.3, VLAN, ARP,IPv4, IPv6, TCP, UDP and HTTP to only mention a few. Its architecture consistsof controller(s) and agent(s). That is, it is possible to use either a GUI or PythonAPI as a controller to manage the agent and generate streams of packets from asingle or several machines at the same time.The Ostinato solution consists of the imagessaimanwong/ostinato-droneandsaimanwong/ostinato-python-api, as shown in Appendix B.3 and Appendix B.4 respectively. The first image creates a container with an Ostinato agent that waitsfor instructions to generate packets. Finally, the second image spins up a controllercontainer to communicate with the agent via a Python script
```  
[saimanwong/mastersthesis](https://github.com/saimanwong/mastersthesis)  


# Troubleshooting


# Reference


* [Introduction to Ostinato, network packet crafting and generator. Dec 9, 2015](https://www.slideshare.net/kentaroebisawa/introduction-to-ostinato-network-packet-crafting-and-generator)  
* [第2回: ネットワーク自動化開発実践 - Python でルータを操作する  2018-11-30](https://qiita.com/radiantmarch/items/936b43f32210e4689179)  
```  
普段、IOS ルータの操作には何を使うでしょうか？ 最近の IOS-XE では GUI, REST API, NetConf/YANG など様々な実装が進んできていますが、いまだに Telnet/SSH での CLI 操作が多いのではないでしょうか？

ところが Telnet/SSH はそのままだとプログラミングには不向きです。そこで、Python で Telnet/SSH を使って IOS ルータに接続する方法を考えてみます。
1. paramiko を使う

paramiko は Python の SSH ライブラリです。これを使った、ルータに接続してコマンドを実行する Python コードは以下のような感じになります。
```  
```  
#!/usr/bin/env python

import paramiko
import time

host = "10.x.x.x"
port = 22

# login details
username = "admin"
password = "admin"

# Create a new Paramiko SSH connection object
conn = paramiko.SSHClient()
# Automatically add SSH hosts keys
conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("--------------------",host,"--------------------")
# create a shell session for multiple commands
conn.connect(host, port, username, password, look_for_keys=False, allow_agent=False)
remote_shell = conn.invoke_shell()
time.sleep(2)
# receive remote host shell output
output = remote_shell.recv(65535)
# display the output
print(output)

# send the command
remote_shell.send("show version\n")
time.sleep(1)
output = remote_shell.recv(65535)
print(output)
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
