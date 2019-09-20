# Purpose  
Take note of Selenium

# Table of Contents
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