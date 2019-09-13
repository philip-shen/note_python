# note of_WiFI
Take some note of WiFi

# Table of Content
[How to Perform Automated WiFi (WPA/WPA2) Cracking](#how-to-perform-automated-wifi-(WPA/WPA2)-cracking)  
[pyDot11](#pydot11)  
[wps](#wps)  
[Heatmap of WiFi](#heatmap-of-wifi)  

[Reference](#reference)

# How to Perform Automated WiFi (WPA/WPA2) Cracking  
[How to Perform Automated WiFi (WPA/WPA2) Cracking 18 November 2018](https://www.shellvoide.com/wifi/how-to-perform-automated-wifi-wpa-wpa2-cracking/2222222214)  
```

WiFite :-

WiFite is an automated WiFi Cracking tool written in Python. It is basically a combination of various famous pentest tools like airmon, aircrack and reaver etc. It is widely used for cracking WEP and WPA (WPS) wireless networks. WiFite version 2 has been released and is likely to be already installed if you are running Kali or Parrot linux distros.

However, since i want this tutorial to be followed by the users of Raspberry Pi and Ubuntu as well, we will make a head-start installing installing WiFite.
```

## STEP 5 WPA/WPA2 cracking using PMKID  
```
Lately, a new method was discovered by Jen Steube for cracking WPA/WPA2. The difference in between handshake and PMKID is that handshake requires the whole 4-way handshake to compute the key to be bruteforced. However, with this new trick an attacker make the Access Point transfer the first EAPOL message which contains the key to be bruteforced. PMKID attack requires two more tools. Install hcxtools:
```
```
$ git clone https://github.com/ZerBea/hcxtools.git
$ cd hcxtools
$ sudo make && sudo make install
```

```
Then install hcxdumptool:
```
```
$ git clone https://github.com/ZerBea/hcxdumptool.git
$ cd hcxdumptool/
$ sudo make && sudo make install
```

```
To crack WiFi Networks using pmkid attack:

$ wifite -i wlan1mon --verbose --nodeauths \
    --pmkid --pmkid-timeout 40 --dict /path/to/wordlist
```
```
Arguments:

    --pmkid: Only use PMKID to crack wireless networks.
    --pmkid-timeout: Timeout for first Message to receive.
    --dict: Wordlist with passwords to brute force.
```
![alt tag](https://www.shellvoide.com/media/images/common/3471153439.jpeg)

# pyDot11  
[pyDot11](https://github.com/ICSec/pyDot11)  
```
pyDot11 currently supports the following:


    Decryption of WEP
    Encryption of WEP
    Decryption of WPA
        TKIP
        CCMP
    Encryption of WPA
        CCMP

Prerequisites:

packetEssentials-1.2.0 pbkdf2-1.3 pycryptodomex-3.4.5 rc4-0.1 scapy 2.4.0
```

# wps  
[wps](https://github.com/devttys0/wps)  
```
wps

Utilities related to WiFi Protected Setup security.
```

# Heatmap of WiFi  
[WiFiヒートマップをPYTHONで動かしてみた Apr 25, 2019](https://qiita.com/JUN91824893/items/7c8cb91b580abc284a18)  
```
屋内のWiFi電波状況を可視化する。電波の悪いところが見える化されるので中継器をどこに置くかが容易にわかる。アイオーデータ社のWi-Fiミレル等が有名。

GitHub（https://github.com/beaugunderson/wifi-heatmap）
にサンプルコードがあったので動かしてみる。

エラーがでました。
　　import tabular as tb
ModuleNotFoundError: No module named 'tabular'

残念、動きません。
```
* [wifi-heatmap 23 Jan 2017](https://github.com/beaugunderson/wifi-heatmap)  


# Reference  
* [Wireless Sniffing: How to Build a simple WiFi Sniffer in Python 21 July 2018](https://www.shellvoide.com/python/how-to-code-a-simple-wireless-sniffer-in-python/)  
```
In this tutorial, we are going to build a wireless sniffer using Python by manipulating fields from captured packets. You might have seen airodump working before and had observed that how it excellently sniff and manipulate packets over the air while hopping through random channels. We will try to extract network ESSIDs and will take utmost care of various possibilities of how the packet is sequenced.

But before, let's dig into the beacon frames. The beacon frame is one of the management frames in 802.11 specifications by IEEE and is sent from Access Point to let other stations know of its presence. This helps stations recognizing various characteristics like Cipher, Channel and encryption the AP is using. Tough we will not study any other packet but such an identical frame is Probe response frame which is also sent from APs.

Prerequisities

A bit knowledge of networking and previous experience with scapy and Python. Scapy is what we are going to use throughout the rest of this tutorial.   
```

* []()  
```

```

* []()  
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