Table of Contents
=================

   * [Purpose](#purpose)
   * [Active Selenium and Headless Chrome and Python3 on Docker](#active-selenium-and-headless-chrome-and-python3-on-docker)
   * [Python and Selenium on Windows](#python-and-selenium-on-windows)
   * [Watir](#watir)
   * [Requests-HTML](#requests-html)
      * [京急線の時刻表をスクレイピング](#京急線の時刻表をスクレイピング)
      * [PythonでHTMLを解析してデータ収集してみる？ スクレイピングが最初からわかる『Python 2年生』](#pythonでhtmlを解析してデータ収集してみる-スクレイピングが最初からわかるpython-2年生)
      * [requestsで取得できないWebページをスクレイピングする方法](#requestsで取得できないwebページをスクレイピングする方法)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose
Leave some tracks of topic.


# Active Selenium and Headless Chrome and Python3 on Docker
* [Docker上でSeleniumとHeadless ChromeとPython3を動かす 2018-07-04](https://qiita.com/sikkim/items/447b72e6ec45849058cd)

```
docker-compose up -d
```
![alt tag](https://i.imgur.com/HW2Eoy1.jpg)

![alt tag](https://i.imgur.com/wzIL2Eo.jpg)

![alt tag](https://i.imgur.com/m7mdpfJ.jpg)
> mkdir /host_mnt/d: file exists Error Happened

![alt tag](https://i.imgur.com/8uCBofM.jpg)

* [mkdir /host_mnt/d: file exists](https://github.com/philip-shen/docker_Win10Home/tree/master/08_Docker_GitHubPage_jekyll#mkdir-host_mntd-file-exists)

![alt tag](https://i.imgur.com/nXnHGTq.jpg)

![alt tag](https://i.imgur.com/5DC7L1Y.jpg)

# Python and Selenium on Windows   
[在Windows上安裝Python & Selenium + 簡易教學 May 21, 2018](https://medium.com/@NorthBei/%E5%9C%A8windows%E4%B8%8A%E5%AE%89%E8%A3%9Dpython-selenium-%E7%B0%A1%E6%98%93%E6%95%99%E5%AD%B8-eade1cd2d12d)  
Step2.安裝Selenium
```
pip install selenium
```

Step3.下載webdriver
```
1.Global — 把webdriver放在Python的安裝目錄

2.Local — 把webdriver放在跟python file同一個資料夾內
```

* [How do I install ChromeDriver on Windows 10 and run Selenium tests with Chrome? asked Oct 15 '15](https://stackoverflow.com/questions/33150351/how-do-i-install-chromedriver-on-windows-10-and-run-selenium-tests-with-chrome)  
```
1. Download the chromedriver.exe and save it to a desired location
2. Specify the executable_path to its saved path

As Uri stated in Update #2 of the question, if we put the chromedriver.exe under C:/Windows, then there is no need to specify executable_path since Python will search under C:/Windows.
```

# Watir  
[Browser automation with Watir - guide (not only) for testers Apr 25, 2017](https://binarapps.com/blog/browser-automation-with-watir-guide/)  

*Finding elements* 
```
The browser class includes the `Container` module, allowing us to access child elements through their HTML tags (all supported HTML5 tags are included), input type (e.g. “text_field” or “radio”) or through generic “element” keyword.

Most elements we interact with also include this module, so we can access their child elements using the very same methods.

These methods take selectors as parameters - a selector is a key-value pair consisting of a property to be checked and the value we're looking for. Most importantly, you can locate elements based on their text or HTML attributes.

The list of handled attributes is finite, but extensive. If you're not sure, just give it a try (remember to replace dashes with underscores, e.g. in “data-something” attributes). If an attribute isn't supported, you can always use `xpath: ''` and `css: ''` locators to make up for it.

If multiple elements fit the description, the first one is selected.
```

[Finding Page Elements](https://github.com/watir/watir_meta/wiki/Finding-Page-Elements)  
[Using IRB 29 Jun 2013](https://github.com/watir/watir_meta/wiki/Using-IRB)  
[Use IRB to Find Page Objects](https://github.com/watir/watir_meta/wiki/Using-IRB#use-irb-to-find-page-objects)  
```
Use IRB to Find Page Objects

To find out what objects are on a page you are writing a test script for, use IRB to get instant feedback.

The show_all_objects method is a useful way to identify the attributes of objects you will need to use in a test script.
```
```
irb(main):003:0> ie.show_all_objects
-----------Objects in page -------------
text name=test_text id= 11 value= alt= src=
submit name=test_button id= 12 value=Click Me alt= click src=
```
[Do we have to initialize class methods in Watir:Browser before using them? Jun 20, 2016](https://stackoverflow.com/questions/36411811/do-we-have-to-initialize-class-methods-in-watirbrowser-before-using-them)  
```
The show_all_objects method does not exist. The method existed in the original Watir implementation, which is now called Watir-Classic. However, the method was removed in Aug 2012. The method was never implemented in Watir-Webdriver.
```

# Requests-HTML  
## 京急線の時刻表をスクレイピング 
[京急線の時刻表をスクレイピング](https://qiita.com/zakuzakuzaki/items/a6e8b48990857de8cdc2)
```

```

## PythonでHTMLを解析してデータ収集してみる？ スクレイピングが最初からわかる『Python 2年生』
[PythonでHTMLを解析してデータ収集してみる？ スクレイピングが最初からわかる『Python 2年生』](https://codezine.jp/article/detail/12230)


## requestsで取得できないWebページをスクレイピングする方法
[requestsで取得できないWebページをスクレイピングする方法](https://gammasoft.jp/blog/how-to-download-web-page-created-javascript/)  

```
from requests_html import HTMLSession

url = "https://search.yahoo.co.jp/realtime"

# セッション開始
session = HTMLSession()
r = session.get(url)

# ブラウザエンジンでHTMLを生成させる
r.html.render()

# スクレイピング
ranking_rows = r.html.find("div.lst.cf")
ranking_list = []
if ranking_rows:
    # 1〜5位だけを取得
    ranking_top5 = ranking_rows[0].find("p.que_3")
    for item in ranking_top5:
        ranking_list.append(item.text[2:])

print(ranking_list)
```




# Reference

* [[Python] selenium 的等待 2019-01-17](http://stackoverflow.max-everyday.com/2019/01/python-selenium-wait/)
* [[Python] How to handle alerts in selenium? 2019-03-18](http://stackoverflow.max-everyday.com/2019/03/python-how-to-handle-alerts-in-selenium/)

* [在爬蟲網頁時，一開始就遇到「我不是機器人」的recaptcha認證要求，之後每讀約30頁資料又要再認證一次，以至於無法讓程式排程自動化。]()
```
李旺財 相信我 萬般解驗証不如弄多點ip
李旺財 你有聽過HTTP PROXY 和SOCKS5嗎?搜一下
```
* [What Is Socks5 Proxy? September 4th, 2018](https://www.ibvpn.com/2018/09/what-is-socks5-proxy/)
```
In simple words, a Socks proxy works as a bridge between your device and the Internet. In this way, all the traffic generated while using this proxy server can’t be associated with your real IP.

An important thing to mention is that Socks5 is popular among users who don’t require a high level of security and don’t want to connect securely. In other words, the Socks5 proxy server will change your real IP but will not encrypt your traffic.
```

* [翻牆不求人，透過 Synology NAS 搭建 shadowsocks Socks5 代理伺服器（VPN）2018/09/02](https://steachs.com/archives/40187)
```
這次要建立的方式是採用內建的 Docker，不需要用指令（網路有一堆用 SSH 連線用指令來做），省時省力又簡單。

Docker 安裝完成後，開啟在左側找到倉庫伺服器，然後搜尋「gists-shadowsocks」這名稱可能有時搜了找不到內容，可以自己增減文字搜看看，反正最後要安裝的是「gists/shadowsocks-libev」這個套件。
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

