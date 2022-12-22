Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [note_Telegram_Bot](#note_telegram_bot)
   * [Telegram Bot](#telegram-bot)
   * [Activate Telegram Bot](#activate-telegram-bot)
      * [Get Telegram ID](#get-telegram-id)
   * [TradingView-Webhook-Bot](#tradingview-webhook-bot)
   * [Delete telegram bot queue](#delete-telegram-bot-queue)
      * [1. Call getUpdates() to get the update_id of the latest message](#1-call-getupdates-to-get-the-update_id-of-the-latest-message)
      * [2. Increment the update_id by 1](#2-increment-the-update_id-by-1)
      * [3. On the next getUpdates() call, set the offset parameter to the id:](#3-on-the-next-getupdates-call-set-the-offset-parameter-to-the-id)
      * [GET UPDATES](#get-updates)
      * [DELETE MESSAGE (UPDATE)](#delete-message-update)
   * [flask-telegram-bot](#flask-telegram-bot)
   * [IP-Details](#ip-details)
   * [teleflask](#teleflask)
   * [Python-ChatGPT-TelegramBot-Docker](#python-chatgpt-telegrambot-docker)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# note_Telegram_Bot
Take some note of Telegram Bot python


# Telegram Bot 
[Telegram用の人工無能を作ってみた 2019-01-06](https://qiita.com/Ovismeme/items/cc59a2de1cf537c977cf)
[ovismeme /telegram_autoreply_bot](https://github.com/ovismeme/telegram_autoreply_bot)

# Activate Telegram Bot  
[Telegram聊天機器人超詳細懶人包，商管人都看得懂【附Python程式碼】2 4 月,2021](https://marketingliveincode.com/?p=172)

<img src="https://miro.medium.com/max/945/1*rnD4_EMcxwFmeDelnMsdEg.png " width="350" height="300">  

## Get Telegram ID  
```
https://api.telegram.org/bot【你的token】/getUpdates
```
<img src="https://miro.medium.com/max/15730/1*dtZF_vCysAHRLbsBkLoNXA.png" width="900" height="70">  


# TradingView-Webhook-Bot 
[fabston / TradingView-Webhook-Bot]()https://github.com/fabston/TradingView-Webhook-Bot

The TradingView Webhook Bot gear listens to TradingView alerts via webhooks using flask. 
All alerts can be instantly sent to Telegram, Discord, Twitter and/or Email.

# Delete telegram bot queue
[How to delete queue updates in telegram api? 2020/05/23](https://stackoverflow.com/questions/61976560/how-to-delete-queue-updates-in-telegram-api)

## 1. Call getUpdates() to get the update_id of the latest message
```
https://api.telegram.org/<MY-TOKEN>/getUpdates
```
## 2. Increment the update_id by 1

## 3. On the next getUpdates() call, set the offset parameter to the id:
```
https://api.telegram.org/<MY-TOKEN>/getUpdates?offset=343126594
```

[How to delete all queue updates in telegram api? 2022/03/07](https://stackoverflow.com/questions/71384308/how-to-delete-all-queue-updates-in-telegram-api)

## GET UPDATES
```
https://api.telegram.org/bot{BOT_ID}/getUpdates
```

## DELETE MESSAGE (UPDATE)
```
https://api.telegram.org/bot{BOT_ID}/getUpdates?offset={UPDATE_ID}}
```

# flask-telegram-bot
[gwvsol / flask-telegram-bot](https://github.com/gwvsol/flask-telegram-bot)

Flask, pyTelegramBotAPI and RethinkDB. 


# IP-Details  
[jainamoswal / IP-Details](https://github.com/jainamoswal/IP-Details) 

An Flask app made with Python for getting user IP address right to your inbox in Telegram.
This is proven very useful to me slightly_smiling_face to track approx location of anyone.


# teleflask
[luckydonald / teleflask](https://github.com/luckydonald/teleflask)


# Python-ChatGPT-TelegramBot-Docker
[ pyfbsdk59 / Python-ChatGPT-TelegramBot-Docker ](https://github.com/pyfbsdk59/Python-ChatGPT-TelegramBot-Docker)
一個Python ChatGPT TelegramBot快速建置平台。

# Troubleshooting


# Reference
* [從零開始的Telegram Bot May 18, 2017](https://blog.sean.taipei/2017/05/telegram-bot)  
```
如果有 Android 手機，強烈建議用這個 app 測試 Methods，比較不會遇到 URL encode 等奇怪的坑
```
[Telegram 機器人](https://play.google.com/store/apps/details?id=taipei.sean.telegram.botplayground)  
* [Python Telegram Bot 教學 (by 陳達仁) ](https://hackmd.io/@BpUgvpG2TZy_PvDRF1bwvw/HkgaMUc24?type=view)  

* [（一）一步步打造 Telegram Bot Jun 29, 2018](https://medium.com/@zaoldyeck9970/%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E4%BD%A0%E6%80%8E%E9%BA%BC%E6%89%93%E9%80%A0-telegram-bot-a7b539c3402a)  
* [（二）為 Chatbot 增加 NLP 功能 Jun 29, 2018](https://medium.com/@zaoldyeck9970/%E5%88%A9%E7%94%A8-olami-open-api-%E7%82%BA-chatbot-%E5%A2%9E%E5%8A%A0-nlp-%E5%8A%9F%E8%83%BD-e6b37940913d)  
* [（三）為 Chatbot 添加新技能 Jun 29, 2018](https://medium.com/@zaoldyeck9970/add-custom-skill-into-chatbot-cef9bfeeef52)  
* [實戰篇－打造人性化 Telegram Bot Jun 21, 2018](https://medium.com/@zaoldyeck9970/%E5%AF%A6%E6%88%B0%E7%AF%87-%E6%89%93%E9%80%A0%E4%BA%BA%E6%80%A7%E5%8C%96-telegram-bot-ed9bb5b8a6d9)  
![alt tag](https://miro.medium.com/max/1250/1*HC_Mr36vPnsCetH3ESXqWg.png)

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
