# Purpose  
Take note of MQTT  in Python 

# Table of Contents  
[What's mosquitto?](#whats-mosquitto) 
[mosquitto Installation on ubuntu](#mosquitto-installation-on-ubuntu)  
[mosquitto Testing](#mosquitto-testing)  

[01. Link with your Android device using MQTT](#01-link-with-your-android-device-using-mqtt)  
[02. Python Binds Mosquitto MQTT Broker](#02-python-binds-mosquitto-mqtt-broker)


# What's mosquitto?  
[IoT初心者向け mosquittoでPub/Sub通信やってみた  Jun 23, 2019](https://qiita.com/sheep29/items/637f9f00e35cc707f681)  

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F319145%2Ff455cb66-a9e1-d452-e8c9-91c187b769db.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=f9de837c5683d1ed7b95e758207bdf00)  

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F319145%2F0a467abb-4302-4d2f-f47a-779ae37e3ba7.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=93c0ab27a38e0398e80800718f0ddc65)  

* mosquitto → Brokerとして動くよ  
* mosquitto client　→　Pub/Sub通信を提供するよ  

# mosquitto Installation on ubuntu  
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

# mosquitto Testing  
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



[Mosquittoを用いてMQTT＋SSL/TLS通信を試してみる Mar 21, 2019](https://qiita.com/udai1532/items/c0f58e73f76900a8469f)  



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
