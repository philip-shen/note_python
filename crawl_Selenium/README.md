# Purpose  
Take note of Selenium

# Table of Contents
[Selenium IDE Hand On](#selenium-ide-hand-on)  
[Selenium IDE for Firefox](#selenium-ide-for-firefox)  
[Selenium IDE for Chrome](#selenium-ide-for-chrome)  
[Selenium IDE REC function](#selenium-ide-rec-function)  

[Selenium and python](#selenium-and-python)  
[Element Click Intercepted Exception](#element-click-intercepted-exception)
[How to select a drop-down menu option value with Selenium (Python)](#how-to-select-a-drop-down-menu-option-value-with-Selenium-(python))
[Converting Python dict to kwargs?](#converting-python-dict-to-kwargs?)  

[Selenium 4](#selenium-4)  

[Reference](#reference) 

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