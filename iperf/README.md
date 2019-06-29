# note of_iperf
Take some note of iperf on Ubuntu
**Aviable on Linux not for Windows**

# Table of Content
[Install iperf3 from source (preferred)](#install-iperf3-from-source-preferred)  
[Install directly from the github repository](#install-directly-from-the-github-repository-activate-virtualenv-first)  

[iperf3 TCP Multiport Server/Client Test](#iperf3-tcp-multiport-serverclient-test)  
[Install ptyhon3 library under virtual environment](#install-ptyhon3-library-under-virtual-environment)  
[Edit config.ini to meet test environment](#edit-configini-to-meet-test-environment)  
[IPv6 iperf3 TCP Multiport Server/Client Test](#ipv6-iperf3-tcp-multiport-serverclient-test)  

[UDP Multiport Server/Client Test via Socket(Cause iperf3 server didn't support udp)](#udp-multiport-serverclient-test-via-socketcause-iperf3-server-didnt-support-udp)  
[Edit config_udp.ini to meet test environment](#edit-config_udpini-to-meet-test-environment)  

[IPv6 UDP Multiport Server/Client Test via Socket(Cause iperf3 server didn't support udp)](#ipv6-udp-multiport-serverclient-test-via-socketcause-iperf3-server-didnt-support-udp)  
[UDP Multiport Multicast Server/Client Test via Socket(Cause iperf3 server didn't support udp)](#udp-multiport-multicast-serverclient-test-via-socketcause-iperf3-server-didnt-support-udp)      
[IPv6 UDP Multiport Multicast Server/Client Test via Socket(Cause iperf3 server didn't support udp)](#ipv6-udp-multiport-multicast-serverclient-test-via-socketcause-iperf3-server-didnt-support-udp)      

[Befor iperf3 TCP Multiport(1~1024) Server/Client Test, Change to root](#befor-iperf3-tcp-multiport11024-serverclient-test-change-to-root)  

[Troubleshooting](#troubleshooting)  

# Install iperf3 from source (preferred)
[Install from source (preferred)](https://github.com/thiezn/iperf3-python#installation)
```
wget http://downloads.es.net/pub/iperf/iperf-3-current.tar.gz
tar xvf iperf-3-current.tar.gz
cd iperf-3.3/                # Or whatever the latest version is
./configure && make && sudo make install  
```
# Install directly from the github repository (Activate Virtualenv first)   
```
(iperf3) philshen@DESKTOP-7EDV2HB:~$git clone https://github.com/thiezn/iperf3-python.git
(iperf3) philshen@DESKTOP-7EDV2HB:~$cd iperf3-python
```
```
(iperf3) philshen@DESKTOP-7EDV2HB:~/iperf3-python$ python3 setup.py install
running install
running bdist_egg
running egg_info
creating iperf3.egg-info
.
.
Finished processing dependencies for iperf3==0.1.11
```
```
(iperf3) philshen@DESKTOP-7EDV2HB:~/iperf3-python$ pip3 list
Package    Version
---------- -------
iperf3     0.1.11
pip        19.1.1
setuptools 41.0.1
wheel      0.33.4
```
# iperf3 TCP Multiport Server/Client Test  
## Install ptyhon3 library under virtual environment 
```
$ pip3 install -r requirement_linux.txt
```
## Edit config.ini to meet test environment
```
[Server_Param]
;
;Server_IP = 0.0.0.0
; = 0.0.0.0 u IPv4
Server_IP = :: 

Server_Port = 5000,5002
Server_Protocol = tcp

[Client_Param]
;Remote_Server_IP = 220.18.1.119
;"::1"  # localhost
Remote_Server_IP = 2001:b011:20e0:3714:20c:29ff:fe78:2573   

Client_Port = 5002,5000
Client_Protocol = tcp
```

```
$ python3 test_multipt_srv.py

$ netstat -tlunp | grep tcp
```
## Check If Open Specific Port Number  
![alt tag](https://i.imgur.com/kGDNzrd.jpg)  

```
$ python3 test_multipt_srv.py
```
![alt tag](https://i.imgur.com/0Y3PPWL.jpg)  

```
$ python3 test_multipt_client.py config.ini
```
![alt tag](https://i.imgur.com/gJBeVEu.jpg)  

# IPv6 iperf3 TCP Multiport Server/Client Test   
```
$ python3 test_multipt_srv.py

```
![alt tag](https://i.imgur.com/GmA1yk1.jpg)  

```
$ python3 test_multipt_client.py config.ini
```
![alt tag](https://i.imgur.com/paXiTzi.jpg)  

# UDP Multiport Server/Client Test via Socket(Cause iperf3 server didn't support udp)  

## Edit config_udp.ini to meet test environment
```
[Server_Param]
;
;Server_IP = 0.0.0.0
; ::= 0.0.0.0 u IPv4
; 237.252.249.227 IPv4 multicast 
;ff15:7079:7468:6f6e:6465:6d6f:6d63:6173 IPv6 multicast 
Server_IP = ff15:7079:7468:6f6e:6465:6d6f:6d63:6173 

Server_Port = 5000,5002,8123
Server_Protocol = udp

[Client_Param]
;Remote_Server_IP = 220.18.1.119
;Remote_Server_IP = localhost
;"::1"  # localhost
; 237.252.249.227 IPv4 multicast 
;ff15:7079:7468:6f6e:6465:6d6f:6d63:6173 IPv6 multicast 
Remote_Server_IP = ff15:7079:7468:6f6e:6465:6d6f:6d63:6173

Client_Port = 5002,5000,8123
Client_Protocol = udp
```

```
$ python3 test_multipt_srv.py config_udp.ini

$ netstat -tlunp | grep udp
```
## Check If Open Specific Port Number  
![alt tag](https://i.imgur.com/527VcBr.jpg)  

```
$ python3 test_multipt_srv.py config_udp.ini
```
![alt tag](https://i.imgur.com/jAdLFyC.jpg)  

```
$ python3 test_multipt_client.py config_udp.ini
```
![alt tag](https://i.imgur.com/Tb8S6Z0.jpg)  

# IPv6 UDP Multiport Server/Client Test via Socket(Cause iperf3 server didn't support udp)  
```
$ python3 test_multipt_srv.py config_udp.ini

$ netstat -tlunp | grep udp
```
## Check If Open Specific Port Number  
![alt tag](https://i.imgur.com/gmIIxgS.jpg)  

```
$ python3 test_multipt_srv.py config_udp.ini
```
![alt tag](https://i.imgur.com/bvjxPre.jpg)  

```
$ python3 test_multipt_client.py config_udp.ini
```
![alt tag](https://i.imgur.com/mcV3mvw.jpg)  

# UDP Multiport Multicast Server/Client Test via Socket(Cause iperf3 server didn't support udp)  
```
$ python3 test_multipt_srv.py config_udp.ini

$ netstat -tlunp | grep udp
```
## Check If Open Specific Port Number  
![alt tag](https://i.imgur.com/5K7j0mf.jpg)  

```
$ python3 test_multipt_srv.py config_udp.ini
```
![alt tag](https://i.imgur.com/Af45HlZ.jpg)  

```
$ python3 test_multipt_client.py config_udp.ini
```
![alt tag](https://i.imgur.com/JzZY5CH.jpg)  

# IPv6 UDP Multiport Multicast Server/Client Test via Socket(Cause iperf3 server didn't support udp)  
```
$ python3 test_multipt_srv.py config_udp.ini

$ netstat -tlunp | grep udp
```
## Check If Open Specific Port Number  
![alt tag](https://i.imgur.com/jcp8SZE.jpg)  

```
$ python3 test_multipt_srv.py config_udp.ini
```
![alt tag](https://i.imgur.com/rOr1MHZ.jpg)  

```
$ python3 test_multipt_client.py config_udp.ini
```
![alt tag](https://i.imgur.com/nBdzcB1.jpg)  

# Befor iperf3 TCP Multiport(1~1024) Server/Client Test, Change to root  
```
$ sudo -i

# python3 test_multipt_srv.py
```
![alt tag](https://i.imgur.com/pP9hgY2.jpg)  

```

$ netstat -tlunp | grep tcp
```
## Check If Open Specific Port Number  
![alt tag](https://i.imgur.com/qMtn4KI.jpg)  

```
$ python3 test_multipt_client.py config.ini
```
![alt tag](https://i.imgur.com/9eu5STk.jpg)  

```
# python3 test_multipt_srv.py
```
![alt tag](https://i.imgur.com/2UeGQVp.jpg)  

# Troubleshooting  
## iperf3: error while loading shared libraries: libiperf.so.0: cannot open shared object file: No such file or directory  
[iperf 3.0.3 fails launch on non-existent shared library libiperf.so #168](https://github.com/esnet/iperf/issues/168)
[ldconfig needed in make install? #153](https://github.com/esnet/iperf/issues/153)  
Explicitly run ldconfig after "make install"
```
$ sudo ldconfig
philshen@DESKTOP-7EDV2HB:~/iperf-3.4$ /usr/local/bin/iperf3
iperf3: parameter error - must either be a client (-c) or server (-s)

Usage: iperf3 [-s|-c host] [options]
       iperf3 [-h|--help] [-v|--version]
```

## unable to set TCP_CONGESTION: Supplied congestion control algorithm not supported on this host Control connection MSS 0  
[Figure out the list of TCP congestion control algorithms supported by linux Feb 22, 2016](http://shouxi.name/blog/2016/02/list-the-currently-supported-tcp-congestion-control-algs-in-ubuntu.html)
```
iperf3 allows the client to specify its preferred TCP congestion control algorithm with option -C. However, the user might be unaware of which algorithms are supported by the running host. It is easy to get the supported list with command
```
```
cat /boot/config-(uname -r) | grep CONFIG_TCP_CONG
```
```
Note that, values y, n, and m stand for activated, deactivated, and activated as module, respectively.

In addition, one can figure out the default algorithm employed by the system with command
```
```
cat /proc/sys/net/ipv4/tcp_congestion_control
```
```
Tips: besides iperf3, the sender can track the real-time state of a TCP connection (e.g., congestion window size) with tcp_probe.
```

# Reference
* [[Python]製作一個類似iperf的測速程式-使用Socket | TK呱呱 201710](http://gienmin.blogspot.com/2017/10/pythoniperf-socket.html)  

* [Overview — Flent: The FLExible Network Tester](https://flent.org/)  
* [pythonでiperfを動かす - Qiita 2017-05-09](https://qiita.com/RIshioka/items/ff6cdb64d4a3b942f68e)  
* [Running Iperf Server and Client using Multithreading in Python causes Segmentation fault Jun 13, 2017](https://stackoverflow.com/questions/44519799/running-iperf-server-and-client-using-multithreading-in-python-causes-segmentati)  
* [thiezn/iperf3-python: Python wrapper around iperf3 - GitHub](https://github.com/thiezn/iperf3-python)  
* [justas-/py3iperf3: A native Python iPerf3 client - GitHub](https://github.com/justas-/py3iperf3)  
* [ipaddress — IPv4/IPv6 manipulation library](https://docs.python.org/3/library/ipaddress.html)  
* [Dealing with Multiple connections — Multicast Feb 2, 2019](https://medium.com/python-pandemonium/python-socket-communication-e10b39225a4c)  
* [IPv6 Multicast (Python recipe) Oct 28, 2005](http://code.activestate.com/recipes/442490-ipv6-multicast/)  
* [Python 3 IPv6 Multicast Jun 14, 2018](https://stackoverflow.com/questions/50848674/python-3-ipv6-multicast)  
* [[python]程式計時器 17th November 2018\r](http://dunkkm.blogspot.com/2018/11/python_62.html)  


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