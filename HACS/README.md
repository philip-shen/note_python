Table of Contents
=================

   * [note_HACS](#note_hacs)
   * [Home Assistant Installation](#home-assistant-installation)
      * [Install Home Assistant Container](#install-home-assistant-container)
   * [Home Assistant Community Store (HACS) Installaion](#home-assistant-community-store-hacs-installaion)
      * [HACS' GitHub](#hacs-github)
   * [tapo-p100-python](#tapo-p100-python)
      * [Reverse engineering TP-Link TAPO](#reverse-engineering-tp-link-tapo)
   * [plugp100](#plugp100)
   * [home-assistant-tapo-p100](#home-assistant-tapo-p100)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# note_HACS
Take some note of Home Assistant Community Store


# Home Assistant Installation 
[智慧家庭第一步 在Synology上架設Home Assistant 2021-11-20](https://www.alvinchen.club/2021/11/20/%e6%99%ba%e6%85%a7%e5%ae%b6%e5%ba%ad%e7%ac%ac%e4%b8%80%e6%ad%a5-%e5%9c%a8synology%e4%b8%8a%e6%9e%b6%e8%a8%adhome-assistant/)

## Install Home Assistant Container  
[Install Home Assistant Container](https://www.home-assistant.io/installation/linux#install-home-assistant-container)


# Home Assistant Community Store (HACS) Installaion
[智慧家庭第二步 Home Assistant安裝 HACS 2021-11-25](https://www.alvinchen.club/2021/11/25/%E6%99%BA%E6%85%A7%E5%AE%B6%E5%BA%AD%E7%AC%AC%E4%BA%8C%E9%83%A8-home-assistant%E5%AE%89%E8%A3%9D-hacs/) 

## HACS' GitHub
[HACS Prerequisites](https://hacs.xyz/docs/setup/prerequisites)  


# tapo-p100-python
[K4CZP3R / tapo-p100-python](https://github.com/K4CZP3R/tapo-p100-python)

## Reverse engineering TP-Link TAPO  
[Reverse engineering TP-Link TAPO](https://k4czp3r.xyz/reverse-engineering/tp-link/tapo/2020/10/15/reverse-engineering-tp-link-tapo.html)

*Plain HTTP and own encryption method.*

The TAPO app communicates using two methods. Bluetooth and HTTP. 
Bluetooth is used to connect with unpaired devices (Exchange wifi ssid&psk etc). 
HTTP is used for every other request after the initial pairing process 
(get/set plug state and settings, update firmware, etc).


# plugp100
[petretiandrea / plugp100](https://github.com/petretiandrea/plugp100)

```
3b392c8477d65f98de2b7ae4b9c0ac1149c02421
{'device_id': '802299B35734CC793845219AF4DCCC7E2035A21F', 'fw_ver': '1.3.2 Build 20210122 Rel. 57063', 'hw_ver': '1.0.0', 'type': 'SMART.TAPOPLUG', 'model': 'P105', 'mac': '34-60-F9-9C-6A-38', 
'hw_id': '58070BD9D8ECC915CD3D6F20A2172712', 
'fw_id': '1D18AD293A25ABDE41405B20C6F98816', 
'oem_id': '0349962536A820DC6F195EAA35496092', 
'specs': 'US', 'device_on': False, 'on_time': 0, 'overheated': False, 
'nickname': 'dHBsaW5rX3AxMDU=', 'location': '', 
'avatar': 'plug', 'longitude': 1210023, 'latitude': 248446, 'has_set_location_info': True, 'ip': 'xxx.xxx.xxx.xxx', 'ssid': 'cGhpbF9ob21lXzExYWF4', 'signal_level': 3, 'rssi': -22, 'region': 'Asia/Taipei', 'time_diff': 480, 'lang': ''}

```


# home-assistant-tapo-p100 
[home-assistant-tapo-p100](https://github.com/petretiandrea/home-assistant-tapo-p100)

*Home Assistant Tapo Integration*

This is a custom integration to control Tapo devices from home assistant.
The core of the integration is provied by plugp100 python library based on work of @K4CZP3R.

# Troubleshooting


# Reference

* []()  
![alt tag]()
<img src="" width="400" height="500">  

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

