# Purpose  
Take note of MQTT  in Python 

# Table of Contents  
[00. What's mosquitto?](#00-whats-mosquitto)  
[01. mosquitto Installation on ubuntu](#01-mosquitto-installation-on-ubuntu)  
[02. mosquitto Testing](#02-mosquitto-testing)  
[03. mosquitto Monitor](#03-mosquitto-monitor)  

[01. Link with your Android device using MQTT](#01-link-with-your-android-device-using-mqtt)  
[02. Python Binds Mosquitto MQTT Broker](#02-python-binds-mosquitto-mqtt-broker)


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

## Username and Password Usage
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
# wget http://mmonit.com/monit/dist/binary/5.14/monit-5.14-linux-x64.tar.gz
# tar zxvf monit-5.14-linux-x64.tar.gz
# cd monit-5.14/
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



[Mosquittoを用いてMQTT＋SSL/TLS通信を試してみる Mar 21, 2019](https://qiita.com/udai1532/items/c0f58e73f76900a8469f)  
[CentOS 7にmosquitto(MQTT)をインストールする Jan 09, 2016](https://qiita.com/s_edward/items/c044f3d3e4d4a05d2dee)
[Windows Server 2012 64bitにMQTT(Mosquitto)を入れるメモ Jun 20, 2016](https://qiita.com/ShikaTech/items/c99c48ce941912713443)
[mosquittoをnginxのstreamモジュールでラップしてみた Jun 09, 2017](https://qiita.com/toast-uz/items/ce25abad19705b2577a0)  
[DockerでMosquittoを動かしたメモ Jul 27, 2014](https://qiita.com/hiroeorz@github/items/455dfcce211866465d29)  



# 01. Link with your Android device using MQTT  
[Link Python applications with your Android device using MQTT Nov 25, 2019](https://towardsdatascience.com/link-python-applications-with-your-android-device-using-mqtt-c8e2c80f6a61)  

## Setup a free data channel at CloudMQTT  

# 02. Python Binds Mosquitto MQTT Broker  
[[ Data Visualization ] Python 串接 Mosquitto MQTT Broker 19 April 2019](https://oranwind.org/-data-visualization-python-chuan-jie-mosquitto-mqtt-broker-2/)  

## Prequirement  
1. 一台已連上網路的電腦  
2. 已安裝 [Mosquitto MQTT Broker](https://oranwind.org/-mqtt-zai-aws-ec2-an-zhuang-mosquitto/)  
3. 已安裝 [Node-RED](https://oranwind.org/-aws-zai-aws-ec2-an-zhuang-node-red/)  
4. 已設定完成 [Node-RED 串接 Mosquitto MQTT Broker](https://oranwind.org/-mqtt-node-red-she-ding-chuan-jie-mosquitto/)  

# 03. Connect to Ubidots MQTT broker with TLS Security   
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
