# note of_iperf
Take some note of iperf on Ubuntu

# Table of Content
[Install iperf3 from source (preferred)](#install-iperf3-from-source-preferred)  
[Install directly from the github repository](#install-directly-from-the-github-repository-activate-virtualenv-first)  
[iperf3 TCP Multiport Server/Client Test](#iperf3-tcp-multiport-serverclient-test)  
[IPv6 iperf3 TCP Multiport Server/Client Test]()  
[UDP Multiport Server/Client Test via Socket(Cause iperf3 server didn't support udp)](#udp-multiport-serverclient-test-via-socketcause-iperf3-server-didnt-support-udp)  
[IPv6 UDP Multiport Server/Client Test via Socket(Cause iperf3 server didn't support udp)](#ipv6-udp-multiport-serverclient-test-via-socketcause-iperf3-server-didnt-support-udp)  

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
```
$ python3 test_multipt_srv.py config_udp.ini

$ netstat -tlunp | grep tcp
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

$ netstat -tlunp | grep tcp
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

* []()  
![alt tag]()  
![alt tag]()  
![alt tag]()  
![alt tag]()  
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