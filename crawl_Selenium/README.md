# Purpose  
Take note of Selenium

# Table of Contents  
[Status Check Table](#status-check-table)  

[DUT Setting of WiFi 2.4G/5G Throughput Test](#dut-setting-of-wifi-24g5g-throughput-test)  

[System](#system)  
[WiFi Smart Connect](#wifi-smart-connect)  
[WiFi 2.4GHz](#wifi-2.4GHz)  
[WiFi 5GHz](#wifi-5GHz)  

[Selenium IDE Hand On](#selenium-ide-hand-on)  
[Selenium IDE for Firefox](#selenium-ide-for-firefox)  
[Selenium IDE for Chrome](#selenium-ide-for-chrome)  
[Selenium IDE REC function](#selenium-ide-rec-function)  

[Selenium and python](#selenium-and-python)  
[Element Click Intercepted Exception](#element-click-intercepted-exception)  
[How to select a drop-down menu option value with Selenium (Python)](#how-to-select-a-drop-down-menu-option-value-with-Selenium-python)  
[Converting Python dict to kwargs?](#converting-python-dict-to-kwargs?)  

[Selenium 4](#selenium-4)  

[Reference](#reference)  
[Can I run multiple instances at once(simultaneously) with selenium-webdriver?](#can-i-run-multiple-instances-at-oncesimultaneously-with-selenium-webdriver)  
[Error message: “'chromedriver' executable needs to be available in the path”](#error-message-chromedriver-executable-needs-to-be-available-in-the-path)  
[How to change the language of the browser in Selenium](#how-to-change-the-language-of-the-browser-in-Selenium)  

# Status Check Table  

## DUT Setting of WiFi 2.4G/5G Throughput Test  
Test Case ID | Test Case Description
------------------------------------ | ---------------------------------------------
dlink_wifi_001 | wifi_2.4G_channel01_WPA/WPA2-Personal
dlink_wifi_002 | wifi_2.4G_channel06_WPA/WPA2-Personal
dlink_wifi_003 | wifi_2.4G_channel11_WPA/WPA2-Personal
dlink_wifi_004 | wifi_5G_channel036_WPA/WPA2-Personal
dlink_wifi_005 | wifi_5G_channel149_WPA/WPA2-Personal

Item | Date Time
------------------------------------ | ---------------------------------------------
Start Time | 2019/10/11 16:55:22
End Time | 2019/10/11 17:0:59
Total Test Duration | 5(tests/sec_mode)*3(directories)*2(mins/test)+6(mins_dut_settings)~36(mins)

Refer [Log file](https://github.com/philip-shen/note_python/raw/master/crawl_Selenium/logs/dut_setup_wifi_thruput.log) to check detail process.

## System  
Item | Description
------------------------------------ | ---------------------------------------------
Reset Function | Button, Disable, Modification could be changed. 
Reboot Function | Button, Disable, Modification could be changed.

## WiFi Smart Connect  
Item | Description
------------------------------------ | ---------------------------------------------
Smart Connect | Button, Disable, Modification could be changed.
```
DevTools listening on ws://127.0.0.1:59644/devtools/browser/20c185e0-8773-4e48-a707-2b26d9062ea7
2019-09-23 09:40:58,404 - api_selenium.py[line:19] - <MainThread 1872>- <Process 8084> - INFO: Initial Chrome Webbrowser!
2019-09-23 09:40:58,419 - api_selenium.py[line:33] - <MainThread 1872>- <Process 8084> - INFO: Open url:http://220.18.1.1
2019-09-23 09:40:58,966 - api_selenium.py[line:37] - <MainThread 1872>- <Process 8084> - INFO: Set Browser Size:1080*705
2019-09-23 09:41:03,169 - api_selenium.py[line:45] - <MainThread 1872>- <Process 8084> - INFO: Click by_ID:logIn_btn
2019-09-23 09:41:03,246 - api_selenium.py[line:50] - <MainThread 1872>- <Process 8084> - INFO: Mouse Over by_ID:menu_Settings
2019-09-23 09:41:04,833 - api_selenium.py[line:45] - <MainThread 1872>- <Process 8084> - INFO: Click by_ID:menuBtn_WiFi
2019-09-23 09:41:04,939 - api_selenium.py[line:117] - <MainThread 1872>- <Process 8084> - INFO: Click by_CSS_SELECTOR:#RADIO_smart .chkbox_enabled
2019-09-23 09:41:06,706 - api_selenium.py[line:117] - <MainThread 1872>- <Process 8084> - INFO: Click by_CSS_SELECTOR:.radio24_advBtn > span
2019-09-23 09:41:06,803 - api_selenium.py[line:117] - <MainThread 1872>- <Process 8084> - INFO: Click by_CSS_SELECTOR:#coexistence_24_tr .chkbox_enabled
2019-09-23 09:41:06,890 - api_selenium.py[line:45] - <MainThread 1872>- <Process 8084> - INFO: Click by_ID:Save_btn
2019-09-23 09:41:06,970 - api_selenium.py[line:45] - <MainThread 1872>- <Process 8084> - INFO: Click by_ID:popalert_ok
2019-09-23 09:41:57,302 - api_selenium.py[line:29] - <MainThread 1872>- <Process 8084> - INFO: Close Chrome Webbrowser!
2019-09-23 09:42:01,676 - api_selenium.py[line:25] - <MainThread 1872>- <Process 8084> - INFO: Teardown Chrome Webbrowser!
```

## WiFi 2.4GHz  
Item | Description
------------------------------------ | ---------------------------------------------
SSID | Text, Modification could be changed.
Password | Text, Modification could be changed.

Security Mode | Description
------------------------------------ | ---------------------------------------------
None | 
WPA/WPA2-Personal | Select box, Modification could be changed.
WPA3-Personal | Select box, Modification could be changed.

Wi-Fi Channel | Description
------------------------------------ | ---------------------------------------------
Auto | Select box, Modification could be changed. 
1 | Select box, Modification could be changed.
6 | Select box, Modification could be changed. 
11 | Select box, Modification could be changed.

Transmission Power | Description
------------------------------------ | ---------------------------------------------
High | 
Medium | 
Low | 

Visibility Status | Description
------------------------------------ | ---------------------------------------------
Visible | Select box, Modification could be changed.
Invisible | Select box, Modification could be changed.

Channel Width | Description
------------------------------------ | ---------------------------------------------
Auto 20/40 MHz | Select box, Modification could be changed.  
20 MHz  | Select box, Modification could be changed. 

HT20/40 Coexistence | Description
------------------------------------ | ---------------------------------------------
Disable | always for performance testing

## WiFi 5GHz  
Item | Description
------------------------------------ | ---------------------------------------------
SSID | Text, Modification could be changed.
Password | Text, Modification could be changed.

Security Mode | Description
------------------------------------ | ---------------------------------------------
None | Select box, Modification could be changed. 
WPA/WPA2-Personal | Select box, Modification could be changed.   
WPA3-Personal | Select box, Modification could be changed.

Wi-Fi Channel | Description
------------------------------------ | ---------------------------------------------
Auto | Select box, Modification could be changed.   
36 | Select box, Modification could be changed.  
149 | Select box, Modification could be changed.   

Transmission Power | Description
------------------------------------ | ---------------------------------------------
High | 
Medium | 
Low | 

Visibility Status | Description
------------------------------------ | ---------------------------------------------
Visible | Select box, Modification could be changed.   
Invisible | Select box, Modification could be changed.    
```
DevTools listening on ws://127.0.0.1:53709/devtools/browser/7ac777df-3003-4350-9184-30da3572b3fa
2019-09-23 17:04:17,959 - api_selenium.py[line:19] - <MainThread 5372>- <Process 1116> - INFO: Initial Chrome Webbrowser!
2019-09-23 17:04:17,974 - api_selenium.py[line:33] - <MainThread 5372>- <Process 1116> - INFO: Open url:http://220.18.1.1
2019-09-23 17:04:18,459 - api_selenium.py[line:37] - <MainThread 5372>- <Process 1116> - INFO: Set Browser Size:1080*705
2019-09-23 17:04:22,667 - api_selenium.py[line:45] - <MainThread 5372>- <Process 1116> - INFO: Click by_ID:logIn_btn
2019-09-23 17:04:22,760 - api_selenium.py[line:50] - <MainThread 5372>- <Process 1116> - INFO: Mouse Over by_ID:menu_Settings
2019-09-23 17:04:23,766 - api_selenium.py[line:45] - <MainThread 5372>- <Process 1116> - INFO: Click by_ID:menuBtn_WiFi
2019-09-23 17:04:23,925 - api_selenium.py[line:117] - <MainThread 5372>- <Process 1116> - INFO: Click by_CSS_SELECTOR:.radio24_advBtn > span
2019-09-23 17:04:25,749 - api_selenium.py[line:81] - <MainThread 5372>- <Process 1116> - INFO: Type by_ID:wifiName_24 value:testdlink-2G
2019-09-23 17:04:25,984 - api_selenium.py[line:81] - <MainThread 5372>- <Process 1116> - INFO: Type by_ID:password_24 value:00000000
2019-09-23 17:04:26,157 - api_selenium.py[line:57] - <MainThread 5372>- <Process 1116> - INFO: Click by_XPath:(//a[contains(@href, '#')])[14]
2019-09-23 17:04:26,253 - api_selenium_dir17x19x.py[line:186] - <MainThread 5372>- <Process 1116> - INFO: args[0] lower :visible
2019-09-23 17:04:26,254 - api_selenium.py[line:57] - <MainThread 5372>- <Process 1116> - INFO: Click by_XPath://a[contains(@href, 'true')]
2019-09-23 17:04:26,344 - api_selenium.py[line:76] - <MainThread 5372>- <Process 1116> - INFO: Click by_Link_Text:Visible
2019-09-23 17:04:26,467 - api_selenium.py[line:81] - <MainThread 5372>- <Process 1116> - INFO: Type by_ID:wifiName_5 value:testdlink-5G
2019-09-23 17:04:26,693 - api_selenium.py[line:81] - <MainThread 5372>- <Process 1116> - INFO: Type by_ID:password_5 value:00000000
2019-09-23 17:04:26,861 - api_selenium.py[line:117] - <MainThread 5372>- <Process 1116> - INFO: Click by_CSS_SELECTOR:#RADIO_5 > .advButton > span
2019-09-23 17:04:26,962 - api_selenium.py[line:57] - <MainThread 5372>- <Process 1116> - INFO: Click by_XPath:(//a[contains(@href, '#')])[20]
2019-09-23 17:04:27,057 - api_selenium.py[line:76] - <MainThread 5372>- <Process 1116> - INFO: Click by_Link_Text:WPA3-Personal
2019-09-23 17:04:27,162 - api_selenium.py[line:57] - <MainThread 5372>- <Process 1116> - INFO: Click by_XPath:(//a[contains(@href, '#')])[24]
2019-09-23 17:04:27,254 - api_selenium.py[line:76] - <MainThread 5372>- <Process 1116> - INFO: Click by_Link_Text:Auto
2019-09-23 17:04:27,371 - api_selenium.py[line:57] - <MainThread 5372>- <Process 1116> - INFO: Click by_XPath:(//a[contains(@href, '#')])[28]
2019-09-23 17:04:27,461 - api_selenium.py[line:76] - <MainThread 5372>- <Process 1116> - INFO: Click by_Link_Text:Auto 20/40/80 MHz
2019-09-23 17:04:27,603 - api_selenium.py[line:57] - <MainThread 5372>- <Process 1116> - INFO: Click by_XPath:(//a[contains(@href, '#')])[30]
2019-09-23 17:04:27,697 - api_selenium_dir17x19x.py[line:201] - <MainThread 5372>- <Process 1116> - INFO: args[0] lower :visible
2019-09-23 17:04:27,697 - api_selenium.py[line:57] - <MainThread 5372>- <Process 1116> - INFO: Click by_XPath:(//a[contains(@href, 'true')])[2]
2019-09-23 17:04:27,780 - api_selenium.py[line:76] - <MainThread 5372>- <Process 1116> - INFO: Click by_Link_Text:Visible
2019-09-23 17:04:27,871 - api_selenium.py[line:45] - <MainThread 5372>- <Process 1116> - INFO: Click by_ID:Save_btn
2019-09-23 17:04:27,967 - api_selenium.py[line:45] - <MainThread 5372>- <Process 1116> - INFO: Click by_ID:popalert_ok
2019-09-23 17:05:17,788 - api_selenium.py[line:29] - <MainThread 5372>- <Process 1116> - INFO: Close Chrome Webbrowser!
2019-09-23 17:05:22,222 - api_selenium.py[line:25] - <MainThread 5372>- <Process 1116> - INFO: Teardown Chrome Webbrowser!
```

Channel Width | Description
------------------------------------ | ---------------------------------------------
Auto 20/40/80 MHz | 
Auto 20/40 MHz  | 

```
DevTools listening on ws://127.0.0.1:59892/devtools/browser/2e87f7b3-1cd7-451c-9c3f-7be50465ef9e
2019-09-23 09:50:25,538 - api_selenium.py[line:19] - <MainThread 13552>- <Process 16588> - INFO: Initial Chrome Webbrowser!
2019-09-23 09:50:25,538 - api_selenium.py[line:33] - <MainThread 13552>- <Process 16588> - INFO: Open url:http://220.18.1.1
2019-09-23 09:50:25,943 - api_selenium.py[line:37] - <MainThread 13552>- <Process 16588> - INFO: Set Browser Size:1080*705
2019-09-23 09:50:30,122 - api_selenium.py[line:45] - <MainThread 13552>- <Process 16588> - INFO: Click by_ID:logIn_btn
2019-09-23 09:50:30,222 - api_selenium.py[line:50] - <MainThread 13552>- <Process 16588> - INFO: Mouse Over by_ID:menu_Settings
2019-09-23 09:50:31,297 - api_selenium.py[line:45] - <MainThread 13552>- <Process 16588> - INFO: Click by_ID:menuBtn_WiFi
2019-09-23 09:50:31,413 - api_selenium.py[line:117] - <MainThread 13552>- <Process 16588> - INFO: Click by_CSS_SELECTOR:.radio24_advBtn > span
2019-09-23 09:50:33,134 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, '#')])[4]
2019-09-23 09:50:33,213 - api_selenium.py[line:76] - <MainThread 13552>- <Process 16588> - INFO: Click by_Link_Text:None
2019-09-23 09:50:33,322 - api_selenium.py[line:81] - <MainThread 13552>- <Process 16588> - INFO: Type by_ID:wifiName_24 value:testdlink-2G
2019-09-23 09:50:33,546 - api_selenium.py[line:81] - <MainThread 13552>- <Process 16588> - INFO: Type by_ID:password_24 value:00000000
2019-09-23 09:50:33,704 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, '#')])[8]
2019-09-23 09:50:33,788 - api_selenium.py[line:76] - <MainThread 13552>- <Process 16588> - INFO: Click by_Link_Text:11
2019-09-23 09:50:34,452 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, '#')])[10]
2019-09-23 09:50:34,520 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, '#')])[10]
2019-09-23 09:50:34,588 - api_selenium.py[line:76] - <MainThread 13552>- <Process 16588> - INFO: Click by_Link_Text:High
2019-09-23 09:50:34,693 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, '#')])[12]
2019-09-23 09:50:34,760 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, '#')])[12]
2019-09-23 09:50:34,816 - api_selenium.py[line:76] - <MainThread 13552>- <Process 16588> - INFO: Click by_Link_Text:Auto 20/40 MHz
2019-09-23 09:50:34,919 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, '#')])[14]
2019-09-23 09:50:35,008 - api_selenium.py[line:76] - <MainThread 13552>- <Process 16588> - INFO: Click by_Link_Text:Invisible
2019-09-23 09:50:35,666 - api_selenium.py[line:117] - <MainThread 13552>- <Process 16588> - INFO: Click by_CSS_SELECTOR:#RADIO_5 > .advButton > span
2019-09-23 09:50:35,759 - api_selenium.py[line:81] - <MainThread 13552>- <Process 16588> - INFO: Type by_ID:wifiName_5 value:testdlink-5G
2019-09-23 09:50:35,957 - api_selenium.py[line:81] - <MainThread 13552>- <Process 16588> - INFO: Type by_ID:password_5 value:00000000
2019-09-23 09:50:36,136 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, '#')])[20]
2019-09-23 09:50:36,225 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, 'WPA3-PSK')])[2]
2019-09-23 09:50:36,846 - api_selenium.py[line:57] - <MainThread 13552>- <Process 16588> - INFO: Click by_XPath:(//a[contains(@href, '#')])[30]
2019-09-23 09:50:36,928 - api_selenium.py[line:76] - <MainThread 13552>- <Process 16588> - INFO: Click by_Link_Text:Invisible
2019-09-23 09:50:37,032 - api_selenium.py[line:45] - <MainThread 13552>- <Process 16588> - INFO: Click by_ID:Save_btn
2019-09-23 09:50:37,127 - api_selenium.py[line:45] - <MainThread 13552>- <Process 16588> - INFO: Click by_ID:popalert_ok
2019-09-23 09:51:26,734 - api_selenium.py[line:29] - <MainThread 13552>- <Process 16588> - INFO: Close Chrome Webbrowser!
2019-09-23 09:51:31,063 - api_selenium.py[line:25] - <MainThread 13552>- <Process 16588> - INFO: Teardown Chrome Webbrowser!
```

# Selenium IDE Hand On  
[10分でわかるブラウザ処理自動化！初心者向けSelenium IDE入門ガイド (2019/08版 : Selenium IDE v3.12.0)  2019-09-01](https://qiita.com/oh_rusty_nail/items/5b584c95e01759c00869)  

## Selenium IDE for Firefox  
[Firefoxを利用する場合](https://qiita.com/oh_rusty_nail/items/5b584c95e01759c00869#firefox%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B%E5%A0%B4%E5%90%88)  

## Selenium IDE for Chrome  
[Chromeを利用する場合](https://qiita.com/oh_rusty_nail/items/5b584c95e01759c00869#chrome%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B%E5%A0%B4%E5%90%88)  

## Selenium IDE REC function  
[Selenium IDEのREC(記録)機能を使ったテストの作成](https://qiita.com/oh_rusty_nail/items/5b584c95e01759c00869#selenium-ide%E3%81%AErec%E8%A8%98%E9%8C%B2%E6%A9%9F%E8%83%BD%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9F%E3%83%86%E3%82%B9%E3%83%88%E3%81%AE%E4%BD%9C%E6%88%90)  

# Selenium and python  
[seleniumとpythonを使用しルーターを自動再起動させる 2019-09-12](https://qiita.com/yosida/items/2059bf9326da2259285c)   
```
環境

・Windows10
・Python3.7.4
・selenium

windowsでのpython導入法は他の方がめちゃくちゃ詳しく書いてくださってますので省略
seleniumは
pip install selenium
これだけ
```


## Element Click Intercepted Exception  
[Error Handling in Selenium on Python 14 Oct 2018](https://www.pingshiuanchua.com/blog/post/error-handling-in-selenium-on-python)  
```
If it's not a pop-up, the problem could be solved by scrolling away, 
hoping that the blocking element moves with you and away from the button/link to be clicked
```

```
from selenium.common.exceptions import ElementClickInterceptedException
try:
  # Tries to click an element
  driver.find_element_by_css_selector("button selector").click()
except ElementClickInterceptedException:
  # Use Javascript to scroll down to bottom of page
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```
# How to select a drop-down menu option value with Selenium (Python)  
[How to select a drop-down menu option value with Selenium (Python) Feb 20, 2015](https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-option-value-with-selenium-python)
```
For example:

<select id="fruits01" class="select" name="fruits">
  <option value="0">Choose your fruits:</option>
  <option value="1">Banana</option>
  <option value="2">Mango</option>
</select>
```
```
Here is an example:

from selenium import webdriver
b = webdriver.Firefox()
b.find_element_by_xpath("//select[@name='element_name']/option[text()='option_text']").click()
```
[What is the correct way to select an <option> using Selenium's Python WebDriver Jul 7 '11](https://sqa.stackexchange.com/questions/1355/what-is-the-correct-way-to-select-an-option-using-seleniums-python-webdriver)  
```
The easiest way that I have found was to do something along the lines of:

el = driver.find_element_by_id('id_of_select')
for option in el.find_elements_by_tag_name('option'):
    if option.text == 'The Options I Am Looking For':
        option.click() # select() in earlier versions of webdriver
        break
```

```
This may have some runtime issues if there are a large number of options, but for us it suffices.
Also this code will work with multi-select

def multiselect_set_selections(driver, element_id, labels):
    el = driver.find_element_by_id(element_id)
    for option in el.find_elements_by_tag_name('option'):
        if option.text in labels:
            option.click()
```
[Python selenium —— 操作select标签的下拉选择框 Sep 8, 2016](https://huilansame.github.io/huilansame.github.io/archivers/drop-down-select)  
1.导入（import）  
```
from selenium.webdriver.support.ui import Select
# 或者直接从select导入
# from selenium.webdriver.support.select import Select

```

2.选择（select）

select_by_index(index)
select_by_value(value)
select_by_visible_text(text)

```
针对于示例网站中的第一个select框：

<select id="s1Id">
<option></option>
<option value="o1" id="id1">o1</option>
<option value="o2" id="id2">o2</option>
<option value="o3" id="id3">o3</option>
</select>


我们可以这样定位：

from selenium import webdriverd
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
driver.get('http://sahitest.com/demo/selectTest.htm')

s1 = Select(driver.find_element_by_id('s1Id'))  # 实例化Select

s1.select_by_index(1)  # 选择第二项选项：o1
s1.select_by_value("o2")  # 选择value="o2"的项
s1.select_by_visible_text("o3")  # 选择text="o3"的值，即在下拉时我们可以看到的文本

driver.quit()

以上是三种选择下拉框的方式，注意：

    index从 0 开始
    value是option标签的一个属性值，并不是显示在下拉框中的值
    visible_text是在option标签中间的值，是显示在下拉框的值

```

3.反选（deselect）
```
自然的，有选择必然有反选，即取消选择。Select提供了四个方法给我们取消原来的选择：

deselect_by_index(index)
deselect_by_value(value)
deselect_by_visible_text(text)
deselect_all()

前三种分别于select相对应，第四种是全部取消选择，是的，你没看错，是全部取消。有一种特殊的select标签，即设置了multiple="multiple"属性的select，这种select框是可以多选的，你可以通过多次select，选择多项选项，而通过deselect_all()来将他们全部取消。

全选？NO，不好意思，没有全选，不过我想这难不倒你，尤其是看了下面的这几个属性。
```

4.选项（options）
options 
all_selected_options  
first_selected_option  

上面三个属性，分别返回这个select元素所有的options、所有被选中的options以及第一个被选中的option。  
```

```

# Converting Python dict to kwargs?  
[Converting Python dict to kwargs? Sep 9, 2018](https://stackoverflow.com/questions/5710391/converting-python-dict-to-kwargs)
```
Use the double-star (aka double-splat?) operator:
func(**{'type':'Event'})

is equivalent to
func(type='Event')
```



# Selenium 4  
[Selenium 4 is releasing soon: What every QA must know? Dec 4, 2018 ](https://medium.com/@muntasir./selenium-4-is-releasing-soon-what-every-qa-must-know-c82d4914be0a)  

## W3C WebDriver Standardization  
[WebDriver W3C specs](https://github.com/w3c/webdriver)  
## Selenium 4 IDE  


# Reference  
## Can I run multiple instances at once(simultaneously) with selenium-webdriver?  
[Can I run multiple instances at once(simultaneously) with selenium-webdriver? Nov 16 '15](https://stackoverflow.com/questions/33741921/can-i-run-multiple-instances-at-oncesimultaneously-with-selenium-webdriver)  
```
Well you need to create multiple threads instead of looping, then you can start each upload in parallel threads. You are on the right track. You dont need selenium grid to achieve this.

lookup about multithreading. You can start with this answer

It's not right you need grid for executing multiple browser sessions. You can invoke multiple browser sessions by just creating multiple driver objects, and managing them. Each session will be separate if you want them to be.

Grid is for scaling as there is a limitation on the no of browser instances you can run keeping your machine performance intact and tests stable. Like more than 5 chrome instances in a single machine. If you want to do more than that then you have to use selenium Grid.
```
## Error message: “'chromedriver' executable needs to be available in the path”
[Error message: “'chromedriver' executable needs to be available in the path” Oct 18, 2018](https://stackoverflow.com/questions/29858752/error-message-chromedriver-executable-needs-to-be-available-in-the-path)  
```
Alternatively you can use a direct path to the chromedriver like this:

 driver = webdriver.Chrome('/path/to/chromedriver') 
So in your specific case:

 driver = webdriver.Chrome("C:/Users/michael/Downloads/chromedriver_win32/chromedriver.exe")
```
## How to change the language of the browser in Selenium  
[Trouble modifying the language option in selenium python bindings ](https://stackoverflow.com/questions/55150118/trouble-modifying-the-language-option-in-selenium-python-bindings)  
```
Working Solution:

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
driver = webdriver.Chrome(chrome_options=options)

Try using below code:

prefs = {
  "translate_whitelists": {"your native language":"en"},
  "translate":{"enabled":"True"}
}
options.add_experimental_option("prefs", prefs)
```

[selenium change language browser chrome / firefox Oct 8, 2015](https://stackoverflow.com/questions/33016300/selenium-change-language-browser-chrome-firefox)  

The answer is already available in one of the very recent post:  
[Change language on Firefox with Selenium Python Sep 22 '15](https://stackoverflow.com/questions/32728302/change-language-on-firefox-with-selenium-python)
```
def get_webdriver(attempts=3, timeout=60, locale='en-us'):
  firefox_profile = webdriver.FirefoxProfile()
  firefox_profile.set_preference("intl.accept_languages", locale)
  firefox_profile.update_preferences()

  desired_capabilities = getattr(
      DesiredCapabilities, "FIREFOX").copy()

  hub_url = urljoin('http://hub:4444', '/wd/hub')
  driver = webdriver.Remote(
    command_executor=hub_url, desired_capabilities=desired_capabilities,
    browser_profile=firefox_profile)

  return driver
```

[How to change the language of the browser in Selenium Aug 23, 2017](https://softwaretestingboard.com/q2a/2347/how-to-change-the-language-of-the-browser-selenium-webdriver#axzz60QospnL3)
```
Below is the syntax you can use for Firefox Browser :

FirefoxProfile profile = new FirefoxProfile();
//setting the locale french : 'fr'
profile.setPreference("intl.accept_languages","fr");
driver = new FirefoxDriver(profile);
driver.get("http://www.google.com);

Below is the syntax you can use for Chrome Browser :

System.setProperty("webdriver.chrome.driver","D:/.../chromedriver.exe");
ChromeOptions options = new ChromeOptions();
options.addArguments("-lang= sl");
ChromeDriver driver = new ChromeDriver(options);
driver.get("http://www.google.com);

Here are few samples for different languages:

//options.AddArgument("--lang=es"); //espanol
//options.AddArgument("--lang=es-mx"); //espanol (Latinoamerica), espanol
//options.AddArgument("--lang=en-ca"); //english (UK), english (us), english
//options.AddArgument("--lang=en-au"); //english (UK), english (us), english
//options.AddArgument("--lang=en-nz"); //english (UK), english (us), english
//options.AddArgument("--lang=zh"); //english (us), english
//options.AddArgument("--lang=zh-tw"); //Chinese (Traditional Chinese), Chinese, english (us), english
//options.AddArgument("--lang=zh-hk"); //Chinese (Traditional Chinese), Chinese, english (us), english
//options.AddArgument("--lang=zh-cn"); //Chinese (Simplified Chinese), Chinese, english (us), english
options.AddArgument("--lang=fr"); //Francais (France), Francais, english (us), english
//options.AddArgument("--lang=fr-ca"); //Francais (France), Francais, english (us), english
//options.AddArgument("--lang=aus"); //Francais (France), Francais, english (us), english
 

For IE browser, we need to update the locale manually in the browser.
```
* [Max的搶票機器人，python + selenium 小程式分享](https://github.com/max32002/tixcraft_bot)  

* [全国のSeleniumer必読 2019-09-09](https://qiita.com/oh_rusty_nail/items/b8ba525d31ea7c522856#jenkins)  

[Selenium IDE](https://qiita.com/oh_rusty_nail/items/b8ba525d31ea7c522856#selenium-ide)
```
Selenium IDEについては、2019/08時点での最新の記事を書きましたのでそちらをご覧ください。
```
* [10分でわかるブラウザ処理自動化！初心者向けSelenium IDE入門ガイド (2019/08版 : Selenium IDE v3.12.0)  2019-09-01](https://qiita.com/oh_rusty_nail/items/5b584c95e01759c00869)  
* [Selenium IDE コマンドリファレンス (2019/09版 : Selenium IDE v3.12.0 [全96コマンドを徹底解説])  2019-09-08](https://qiita.com/oh_rusty_nail/items/77782973b4152992017b)  
* [Selenium IDEで作ったテストをselenium-side-runnerを使ってheadlessで動かしてTravisCIでビルドする 2019-09-09](https://qiita.com/oh_rusty_nail/items/3844f10e2dd83e9e2f27)  

* [Clear text from textarea with selenium Jan 6, 2015](https://stackoverflow.com/questions/7732125/clear-text-from-textarea-with-selenium)  
```
driver.find_element_by_id('foo').clear()
```

* [【python】飲み会の開催場所をwebスクレイピングで決めてみた 2019-03-11](https://qiita.com/Fuminori_Souma/items/52deb61146407acdce59)  
```
環境

    PC：windows10
    言語 ：python 3.6.3
    IDE ：pycharm
    GUI ：Tkinter
    ブラウザ操作：Selenium

pythonを選んだのは、今後、仕事で使う予定があるため。
開発環境以下は、pythonを初めて使うためとりあえず
定番(っぽい)のを選択した。

また、情報を抽出するサイトは、普段使用している駅探を選択。
```

* [Seleniumを用いた自己満足のオークションショッピング 2018-04-12](https://qiita.com/qchin/items/08d07b7a0cba6d3a7353)  
```
開発環境の要件は下記のものです。

    Windows (OS)
    Chrome (ブラウザ)
    ChromeのSeleniumドライバ (ダウンロードリンク)
    Python 3 (言語、IDE)
    Seleniumライブラリ
```
* [Selenium IDE commands ](https://ui.vision/docs/selenium-ide)  
```
Flow Control and !statusOK

!statusOK is an internal variable that contains the status of the last executed command. Thus its value is true if the command was successful or false if the command encountered an error. It is typically used with !ErrorIgnore set to true so the macro execution continues after an error. 
```


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