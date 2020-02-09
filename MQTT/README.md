# Purpose  
Take note of MQTT  in Python 

# Table of Contents  
[00. What's mosquitto?](#00-whats-mosquitto)  
[01. mosquitto Installation on ubuntu](#01-mosquitto-installation-on-ubuntu)  
[02. mosquitto Testing](#02-mosquitto-testing)  
[02.01 Username and Password Usage](#0201-username-and-password-usage)  
[03. mosquitto Monitor](#03-mosquitto-monitor)  
[04. Node-RED Installation](#04-node-red-installation)  
[04.01 Automatic Installation](#0401-automatic-installation)  
[04.02 Manaul Installation](#0402-manaul-installation)  


[Link with your Android device using MQTT](#link-with-your-android-device-using-mqtt)  
[Python Binds Mosquitto MQTT Broker](#python-binds-mosquitto-mqtt-broker)


# 00. What's mosquitto?  
[IoT初心者向け mosquittoでPub/Sub通信やってみた  Jun 23, 2019](https://qiita.com/sheep29/items/637f9f00e35cc707f681)  

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F319145%2Ff455cb66-a9e1-d452-e8c9-91c187b769db.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=f9de837c5683d1ed7b95e758207bdf00)  

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F319145%2F0a467abb-4302-4d2f-f47a-779ae37e3ba7.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=93c0ab27a38e0398e80800718f0ddc65)  

* mosquitto → Brokerとして動くよ  
* mosquitto client　→　Pub/Sub通信を提供するよ  

# 01. mosquitto Installation on ubuntu  
[ubuntuでMQTTブローカー「mosquitto」のインストール方法 ](https://qiita.com/rui0930/items/40bd5a1cfd3422206ad3)  

```
sudo add-apt-repository ppa:mosquitto-dev/mosquitto-ppa
```

```
sudo apt-get update
```

```
sudo apt-get install mosquitto-clients
```

```
sudo apt-get install mosquitto
```

# 02. mosquitto Testing  
```
sudo mosquitto
```
![alt tag](https://i.imgur.com/OcVDwFz.jpg)  

```
$ mosquitto_sub -d -t test

```
![alt tag](https://i.imgur.com/X0lJh1l.jpg)  

```
$  mosquitto_pub -d -t test -m "Hello world!"
```
![alt tag](https://i.imgur.com/5oNRSP9.jpg)  

## 02.01 Username and Password Usage
[Mosquitto で Username と Password を使う Feb 09, 2018](https://qiita.com/ekzemplaro/items/77bfa6274cbddd4b5624)  
```
$ nano password.txt
```

```
$ cat password.txt
steve:password
jim:topsecret
```

2)   
```
$ mosquitto_passwd -U password.txt

$ cat password.txt
steve:$6$yOPU3/t8UeDjEqO1$bXo7EX9vVewHlsFuz+dsxA/DjVKA4eMmGd7K03pKwPCF5YR2+tq/NMVMALTnfPgAYrzOpuYdM5G70PEwgoXfxw==
jim:$6$Lt6wUb8xOEfOVa7d$LjHY2t4cdx1qieAmrU/TGISuTvSiN4p2fqQRBuE432c/zJ/vPXdZiacJJHLZhm1gS2QohHLVtoQqKV7Ku2fMhA==
```

3) 
```
$ sudo cp ./password.txt /etc/mosquitto/
```

4) /etc/mosquitto/mosquitto.conf を編集します。  
```
#allow_anonymous true
allow_anonymous false
password_file /etc/mosquitto/password.txt
```
![alt tag](https://i.imgur.com/0ekbNiV.jpg)  

5) mosquitto を再起動します。  
```
sudo systemctl restart mosquitto
```
![alt tag](https://i.imgur.com/RD5TM61.jpg)  

```
mosquitto_sub -d -t orz \
        -u jim -P topsecret \
        --topic sensors/topic_1
```
![alt tag](https://i.imgur.com/gXCypYG.jpg)  

```
mosquitto_pub -d -t orz -m "こんにちは Feb/09/2018 PM 13:47" \
        -u jim -P topsecret \
        --topic sensors/topic_1
```
![alt tag](https://i.imgur.com/69kWawT.png)  


# 03. mosquitto Monitor  
[MQTT入門(導入編) Mar 19, 2016](https://qiita.com/pocket8137/items/0205b7a1c0b38890523e)  
## monitによる監視  
[monitによる監視](https://qiita.com/pocket8137/items/0205b7a1c0b38890523e#-monit%E3%81%AB%E3%82%88%E3%82%8B%E7%9B%A3%E8%A6%96)  

[Latest Monit setup on Ubuntu](https://easyengine.io/tutorials/monitoring/monit/)  
```
# cd ~
# wget http://mmonit.com/monit/dist/binary/5.26.0/monit-5.26.0-linux-x64.tar.gz
# tar zxvf monit-5.26.0-linux-x64.tar.gz
# cd monit-5.26.0/
# cp bin/monit /usr/bin/monit
# mkdir /etc/monit
# touch /etc/monit/monitrc
# chmod 0700 /etc/monit/monitrc 
# ln -s /etc/monit/monitrc /etc/monitrc
# wget https://gist.githubusercontent.com/rahul286/9975061/raw/1aa107e62ecaaa2dacfdb61a12f13efb6f15005b/monit -P /etc/init.d/
# chmod u+x /etc/init.d/monit
# echo "START=yes" > /etc/default/monit
# monit -t
# /sbin/chkconfig  --add monit
# /sbin/chkconfig  monit on
# /sbin/chkconfig --list monit
# view /etc/monit.d/mosquitto.conf
check process mosquitto with pidfile /var/run/mosquitto.pid
start = "/etc/init.d/mosquitto start"
stop = "/etc/init.d/mosquitto stop"
```
![alt tag](https://i.imgur.com/1MlNLaE.jpg)  

![alt tag](https://i.imgur.com/nur4A5F.jpg)  

![alt tag](https://i.imgur.com/gjDaumE.jpg)  


```
# sudo mkdir /var/log/mosquitto
# sudo chown mosquitto /var/log/mosquitto

# view /etc/mosquitto/mosquitto.conf
合計 0
pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest syslog
log_dest file /var/log/mosquitto/mosquitto.log
#log_type debug
log_type error
log_type warning
log_type notice
log_type information
#log_type none
log_type subscribe
log_type unsubscribe
#log_type websockets
#log_type all

connection_messages true

log_timestamp true

include_dir /etc/mosquitto/conf.d

# /etc/init.d/mosquitto reload
```
![alt tag](https://i.imgur.com/tIfVVmW.jpg)  


# 04. Node-RED Installation  
[[ AWS ] 在 AWS EC2 安裝 Node-RED 18 April 2019](https://oranwind.org/-aws-zai-aws-ec2-an-zhuang-node-red/)  

Service | Port Number
------------------------------------ | ---------------------------------------------
Mosquitto | 1883
Node-RED | 1880
InfluxDB | 8086
Grafana | 3000

![alt tag](https://oranwind.s3.amazonaws.com/2019/Apr/_____2019_04_19___10_27_28-1555640863471.png)  

## 04.01 Automatic Installation  
[Node.js v12.x:](https://github.com/nodesource/distributions)
```
# Using Ubuntu
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install -y nodejs
```
```
# Optional: install build tools  

# use `sudo` on Ubuntu or run this as root on debian
sudo apt-get install -y build-essential
```
![alt tag](https://i.imgur.com/WGpciSU.jpg)  

## 04.02 Manaul Installation  
1) Remove the old PPA if it exists  
```
# add-apt-repository may not be present on some Ubuntu releases:
# sudo apt-get install python-software-properties
sudo add-apt-repository -y -r ppa:chris-lea/node.js
sudo rm -f /etc/apt/sources.list.d/chris-lea-node_js-*.list
sudo rm -f /etc/apt/sources.list.d/chris-lea-node_js-*.list.save
```

2) Add the NodeSource package signing key  
```
curl -sSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | sudo apt-key add -
# wget can also be used:
# wget --quiet -O - https://deb.nodesource.com/gpgkey/nodesource.gpg.key | sudo apt-key add -
```

3) Add the desired NodeSource repository  
```
# Replace with the branch of Node.js or io.js you want to install: node_6.x, node_8.x, etc...
VERSION=node_12.x

# The below command will set this correctly, but if lsb_release isn't available, you can set it manually:
# - For Debian distributions: jessie, sid, etc...
# - For Ubuntu distributions: xenial, bionic, etc...
# - For Debian or Ubuntu derived distributions your best option is to use the codename corresponding to the upstream release your distribution is based off. This is an advanced scenario and unsupported if your distribution is not listed as supported per earlier in this README.

DISTRO="$(lsb_release -s -c)"
echo "deb https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee /etc/apt/sources.list.d/nodesource.list
echo "deb-src https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee -a /etc/apt/sources.list.d/nodesource.list
```
![alt tag](https://i.imgur.com/SWo4mZV.jpg)  

4) Update package lists and install Node.js  
```
sudo apt-get update
sudo apt-get install nodejs
```
![alt tag](https://i.imgur.com/WGpciSU.jpg)  

![alt tag](https://i.imgur.com/Tp1KkpY.jpg)  

5)  
```
sudo apt-get install -y nodejs build-essential 
```
![alt tag](https://i.imgur.com/TwvNRJX.jpg)  

6)  
```
sudo npm install -g --unsafe-perm node-red --allow-root
```
![alt tag](https://i.imgur.com/IlfowCa.jpg)  

7) Start node-red   
```
node-red
```
![alt tag](https://i.imgur.com/OP6vA2Y.jpg)  

![alt tag](https://i.imgur.com/bqUy29L.png)  




[Node-RED紹介（インストールからWebGUI作成）](https://qiita.com/tshimizu8/items/f71c1a5209cb3a19ce51)

[Node-RED事始め Oct 30, 2015](https://qiita.com/joeartsea/items/93e8483a31292067c654)  
[Node-RED超入門 Jan 21, 2018](https://qiita.com/makaishi2/items/5c7b1b6a72b6938cf3d2)  
[Node-REDの設定 Dec 03, 2015](https://qiita.com/joeartsea/items/b5e8e14498f3098990c3)  
[Node-REDをインストールする  Aug 07, 2017](https://qiita.com/egplnt/items/cf79f49660f2df1c54cc)  
[ハンズオン】Node-RED入門編 May 13, 2016](https://qiita.com/joohounsong/items/5b5241df84f910df6627)  
[【Node-RED】 Node-REDでLINEを扱う。Part1 アクセストークン定期更新 Jul 27, 2019](https://qiita.com/ronkabu/items/096facc43cc50b4ace92)  
[【Node-RED】 Node-REDでLINEを扱う。Part2 ダッシュボードのボタンとテキスト入力 Aug 03, 2019](https://qiita.com/ronkabu/items/ccc56d514cf0eb0193c2)  
[【Node-RED】 Node-REDでLINEを扱う。Part3 ブロードキャストメッセージを送る Aug 06, 2019](https://qiita.com/ronkabu/items/035f0bb918df26f95629)  
[Alexaをしゃべらせる（Node-red編）Oct 09, 2019](https://qiita.com/naka-kazz/items/293aa118c8735e376c4f)  
[Node-REDにおけるコンテキストの活用について Nov 06, 2019](https://qiita.com/utaani/items/4f9b12f2ee6b1c5a620f)
[Windowsで（WSLを利用して）Node-RED環境を構築する Nov 11, 2019](https://qiita.com/yossihard/items/309a6fe0d61c595cac98)

[Node-RED系の記事のまとめ May 02, 2019](https://qiita.com/kazutxt/items/8c72448eefcba56dabef)  


[Mosquittoを用いてMQTT＋SSL/TLS通信を試してみる Mar 21, 2019](https://qiita.com/udai1532/items/c0f58e73f76900a8469f)  
[CentOS 7にmosquitto(MQTT)をインストールする Jan 09, 2016](https://qiita.com/s_edward/items/c044f3d3e4d4a05d2dee)
[Windows Server 2012 64bitにMQTT(Mosquitto)を入れるメモ Jun 20, 2016](https://qiita.com/ShikaTech/items/c99c48ce941912713443)
[mosquittoをnginxのstreamモジュールでラップしてみた Jun 09, 2017](https://qiita.com/toast-uz/items/ce25abad19705b2577a0)  
[DockerでMosquittoを動かしたメモ Jul 27, 2014](https://qiita.com/hiroeorz@github/items/455dfcce211866465d29)  



# Link with your Android device using MQTT  
[Link Python applications with your Android device using MQTT Nov 25, 2019](https://towardsdatascience.com/link-python-applications-with-your-android-device-using-mqtt-c8e2c80f6a61)  

## Setup a free data channel at CloudMQTT  

# Python Binds Mosquitto MQTT Broker  
[[ Data Visualization ] Python 串接 Mosquitto MQTT Broker 19 April 2019](https://oranwind.org/-data-visualization-python-chuan-jie-mosquitto-mqtt-broker-2/)  

## Prequirement  
1. 一台已連上網路的電腦  
2. 已安裝 [Mosquitto MQTT Broker](https://oranwind.org/-mqtt-zai-aws-ec2-an-zhuang-mosquitto/)  
3. 已安裝 [Node-RED](https://oranwind.org/-aws-zai-aws-ec2-an-zhuang-node-red/)  
4. 已設定完成 [Node-RED 串接 Mosquitto MQTT Broker](https://oranwind.org/-mqtt-node-red-she-ding-chuan-jie-mosquitto/)  

# Connect to Ubidots MQTT broker with TLS Security   
[Connect to Ubidots MQTT broker with TLS Security](https://help.ubidots.com/en/articles/1083734-connect-to-ubidots-mqtt-broker-with-tls-security)  


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
