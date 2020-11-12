
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Installation](#installation)
      * [Step1 Install Python3.6-32bit](#step1-install-python36-32bit)
      * [Step2 Upgrade pip](#step2-upgrade-pip)
      * [Step3 Install VirtualEnv &amp; Install VirtualEnvWrapper-win](#step3-install-virtualenv--install-virtualenvwrapper-win)
      * [Step4 Make virtualenv](#step4-make-virtualenv)
      * [Step5 Set Project Directory](#step5-set-project-directory)
      * [Step6 Deactivate](#step6-deactivate)
      * [Step7 Workon](#step7-workon)
      * [Step8 Install modules](#step8-install-modules)
      * [Step9 Check installed mdules](#step9-check-installed-mdules)
      * [Step10 Install modules manually](#step10-install-modules-manually)
      * [Step11 Double Check installed mdules](#step11-double-check-installed-mdules)
      * [Step12 Dump installed modules inot requirement.txt](#step12-dump-installed-modules-inot-requirementtxt)
   * [Installing python2.7 hosts on python3.6 Laptop](#installing-python27-hosts-on-python36-laptop)
   * [how-to-use-args-and-kwargs-in-python-3](#how-to-use-args-and-kwargs-in-python-3)
   * [if <strong>name</strong> == '<strong>main</strong>' ?](#if-name--main-)
      * [何をしているか](#何をしているか)
      * [原理](#原理)
      * [実用例](#実用例)
         * [①import helloの場合](#import-helloの場合)
         * [②$python hello.pyの場合](#python-hellopyの場合)
   * [method, @classmethod, @staticmethod](#method-classmethod-staticmethod)
      * [method](#method)
      * [classmethod](#classmethod)
      * [staticmethod](#staticmethod)
      * [@abstractmethod](#abstractmethod)
      * [@abstractclassmethod (version 3.2)](#abstractclassmethod-version-32)
      * [@abstractstaticmethod (version 3.2)](#abstractstaticmethod-version-32)
      * [Duck Typing（ダック・タイピング）](#duck-typingダックタイピング)
   * [Environment](#environment)
   * [Troubleshooting](#troubleshooting)
      * [Permission denied error by installing matplotlib](#permission-denied-error-by-installing-matplotlib)
      * [Python 3 ImportError: No module named 'ConfigParser'](#python-3-importerror-no-module-named-configparser)
   * [Reference](#reference)
      * [如何在 Windows 打造 Python 開發環境設定基礎入門教學](#如何在-windows-打造-python-開發環境設定基礎入門教學)
      * [How can I download Anaconda for python 3.6](#how-can-i-download-anaconda-for-python-36)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose
Take some note of python

# Installation
## Step1 Install Python3.6-32bit  
* [如何在 Windows 打造 Python 開發環境設定基礎入門教學](https://happycoder.org/2017/11/17/how-to-setup-python-development-environment-in-windows/)  
* [在Windows底下最適當安裝Python環境的方法 2018-11-30](https://ithelp.ithome.com.tw/articles/10210071?sc=rss.qu)  

## Step2 Upgrade pip  
## Step3 Install VirtualEnv & Install VirtualEnvWrapper-win  
![alt tag](https://i.imgur.com/4nT6A8n.jpg)    

## Step4 Make virtualenv  
## Step5 Set Project Directory
![alt tag](https://i.imgur.com/kNFsmhf.jpg)  

## Step6 Deactivate  
## Step7 Workon  
![alt tag](https://i.imgur.com/4taDATR.jpg)  

## Step8 Install modules  
>  pip install -r requiremenets.txt  
![alt tag](https://i.imgur.com/HisxZfI.jpg)  
![alt tag](https://i.imgur.com/ivjWNGS.jpg)  

## Step9 Check installed mdules  
```
d:\project\Python\moneyhunter (master -> origin)
(moneyhunter) λ  pip list
Package                  Version
------------------------ ----------
beautifulsoup4           4.6.3
bs4                      0.0.1
cachetools               3.0.0
certifi                  2018.10.15
chardet                  3.0.4
cycler                   0.10.0
google-api-core          1.5.2
google-api-python-client 1.7.4
google-auth              1.6.1
google-auth-httplib2     0.0.3
google-cloud-core        0.28.1
google-cloud-firestore   0.30.0
google-cloud-storage     1.13.0
google-resumable-media   0.3.1
googleapis-common-protos 1.5.5
greenlet                 0.4.15
gspread                  3.0.1
gunicorn                 19.9.0
h5py                     2.8.0
httplib2                 0.12.0
idna                     2.7
kiwisolver               1.0.1
lxml                     4.2.5
matplotlib               2.2.3
mpl-finance              0.10.0
numpy                    1.15.4
oauth2client             4.1.3
pandas                   0.23.4
Pillow                   5.3.0
pip                      19.0.3
protobuf                 3.6.1
pyasn1                   0.4.4
pyasn1-modules           0.2.2
PyDrive                  1.3.1
pyparsing                2.3.0
python-dateutil          2.7.5
pytz                     2018.7
PyYAML                   3.13
requests                 2.20.1
rsa                      4.0
setuptools               40.9.0
six                      1.11.0
twstock                  1.1.1
uritemplate              3.0.0
urllib3                  1.24.1
wheel                    0.33.1
xlrd                     1.1.0
xlutils                  2.0.0
xlwt                     1.3.0
```

## Step10 Install modules manually  
>  pip install TA_Lib-0.4.17-cp36-cp36m-win32.whl  
![alt tag](https://i.imgur.com/vLf11tF.jpg)  

## Step11 Double Check installed mdules  
```
(moneyhunter) λ  pip list
Package                  Version
------------------------ ----------
beautifulsoup4           4.6.3
bs4                      0.0.1
cachetools               3.0.0
certifi                  2018.10.15
chardet                  3.0.4
cycler                   0.10.0
google-api-core          1.5.2
google-api-python-client 1.7.4
google-auth              1.6.1
google-auth-httplib2     0.0.3
google-cloud-core        0.28.1
google-cloud-firestore   0.30.0
google-cloud-storage     1.13.0
google-resumable-media   0.3.1
googleapis-common-protos 1.5.5
greenlet                 0.4.15
gspread                  3.0.1
gunicorn                 19.9.0
h5py                     2.8.0
httplib2                 0.12.0
idna                     2.7
kiwisolver               1.0.1
lxml                     4.2.5
matplotlib               2.2.3
mpl-finance              0.10.0
numpy                    1.15.4
oauth2client             4.1.3
pandas                   0.23.4
Pillow                   5.3.0
pip                      19.0.3
protobuf                 3.6.1
pyasn1                   0.4.4
pyasn1-modules           0.2.2
PyDrive                  1.3.1
pyparsing                2.3.0
python-dateutil          2.7.5
pytz                     2018.7
PyYAML                   3.13
requests                 2.20.1
rsa                      4.0
setuptools               40.9.0
six                      1.11.0
TA-Lib                   0.4.17
twstock                  1.1.1
uritemplate              3.0.0
urllib3                  1.24.1
wheel                    0.33.1
xlrd                     1.1.0
xlutils                  2.0.0
xlwt                     1.3.0
```

## Step12 Dump installed modules inot requirement.txt
```
d:\project\Python\moneyhunter\test (master -> origin)  
pip freeze > ..\requiremenets.txt  
```

# Installing python2.7 hosts on python3.6 Laptop  
```
c:\Python27\Scripts
λ virtualenv -p c:\Python27\python.exe c:\Users\amyfa\Envs\pholus
```
```
c:\Python27\Scripts
λ Workon pholus
c:\Python27\Scripts
(pholus) λ python -V
Python 2.7.16

c:\Python27\Scripts
(pholus) λ pip2 list
```
![alt tag](https://i.imgur.com/oJ6DR5e.jpg)  

# how-to-use-args-and-kwargs-in-python-3  
[how-to-use-args-and-kwargs-in-python-3 November 20, 2017](https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3)
```
def multiply(*args):
    z = 1
    for num in args:
        z *= num
    print(z)

multiply(4, 5)
multiply(10, 9)
multiply(2, 3, 4)
multiply(3, 5, 10, 6)
```

```
def print_values(**kwargs):
    for key, value in kwargs.items():
        print("The value of {} is {}".format(key, value))

print_values(
            name_1="Alex",
            name_2="Gray",
            name_3="Harper",
            name_4="Phoenix",
            name_5="Remy",
            name_6="Val"
        )
```
```
Output
The value of name_2 is Gray
The value of name_6 is Val
The value of name_4 is Phoenix
The value of name_5 is Remy
The value of name_3 is Harper
The value of name_1 is Alex
```

# if __name__ == '__main__' ?  
[【python】if __name__ == '__main__':とは？ updated at 2020-06-08](https://qiita.com/yuta-38/items/5107914933fc6d5babb8)  

## 何をしているか  
```
・ファイルをimportしたときに、if以下は実行しない。

デフォルトとして、.pyファイルをインポートすると、ファイルの中身が実行される。

if __name__ == '__main__':以下に記述することで、import時の実行を回避できる。
```

## 原理  
```
変数 __name__が、importした場合と、ファイル実行した場合で挙動が異なる性質を利用。
「__name__」

    importした場合は "モジュール名" に置き換わる。
    ファイルを実行した場合は、"main"に置き換わる。
```

## 実用例  
```
hello.py

def hello():
    print("hello world")

if __name__ == "__main__":
    hello()
```

### ①import helloの場合  
```
    何も出力しない。
    __name__にモジュール名「"hello"」が代入される
```

### ②$python hello.pyの場合  
```
    "hello world"を出力
    __name__に「__main__」が代入される
```

# method, @classmethod, @staticmethod   
[Pythonで、呼び出し方によってメソッドの振る舞いを変える posted at 2017-04-29](https://qiita.com/masaru/items/5ebf2e96d6524830511b)  

```
Pythonのクラスのメソッドは3種類ある。
    通常のメソッド（インスタンスメソッド）
        第1引数は必須で、慣例としてselfにする。
        インスタンス経由で呼び出すと、呼び出したインスタンスが第1引数に入る。
        クラス経由で呼び出すと、呼び出したときの引数がそのまま渡される。

    クラスメソッド
        @classmethodを付けて定義する。第1引数は必須で、慣例としてclsにする。
        インスタンス経由で呼び出すと、呼び出したインスタンスのクラスが第1引数に入る。
        クラス経由で呼び出すと、そのクラスが第1引数に入る。

    スタティックメソッド
        @staticmethodを付けて定義する。引数は必須ではない。
        呼び出したときの引数がそのまま渡される。
```

```
class C:
  val = 20
  def __init__(self):
    self.val = 1
  def normal_method(self, v):
    return self.val + v + 2
  @classmethod
  def class_method(cls, v):
    return cls.val + v + 3
  @staticmethod
  def static_method(v):
    return C.val + v + 4

i = C()
i.normal_method(5)    # i.val + 5 + 2 = 1 + 5 + 2 = 8
i.class_method(6)     # C.val + 6 + 3 = 20 + 6 + 3 = 29
i.static_method(7)    # C.val + 7 + 4 = 20 + 7 + 4 = 31
C.normal_method(5)    # requires 2 args but 1: error
C.normal_method(i, 6) # i.val + 6 + 2 = 1 + 6 + 2 = 9
C.normal_method(C, 7) # C.val + 7 + 2 = 20 + 7 + 2 = 29
C.class_method(8)     # C.val + 8 + 3 = 20 + 8 + 3 = 31
C.static_method(9)    # C.val + 9 + 4 = 20 + 9 + 4 = 33
```

```
通常のメソッドも関数であることに変わりはない。

    第1引数がselfというのは単なるお約束であって、selfの型については制約はない。
    インスタンス経由で呼び出すと、処理系が勝手に第1引数にそのインスタンスを入れている。

これを逆手にとって、第1引数によって振る舞いを変えることができる。
```

```
class C:
  # 上記に追加
  def trick_method(arg, v):
    if isinstance(arg, C):
      return arg.val * 2 * v
    else:
      return C.val + arg * v

i.trick_method(4)    # i.val * 2 * 4 = 1 * 2 * 4 = 8
C.trick_method(5)    # requires 2 args but 1: error
C.trick_method(6, 7) # C.val + 6 * 7 = 20 + 6 * 7 = 62
C.trick_method(i, 8) # i.val * 2 * 8 = 1 * 2 * 8 = 16
C.trick_method(C, 9) # C.val + C * v: error
```

[Pythonで classmethod、staticmethod を使う updated at 2018-01-18](https://qiita.com/msrks/items/fdc9afd12effc2cba1bc)  
## method  
## classmethod  
## staticmethod  
```
    インスタンス変数やインスタンスメソッドにアクセスしないとき(メソッド内でselfを使わないとき）は classmethod、staticmethodを使おう。

    classmethod: クラス変数にアクセスすべきときや、継承クラスで動作が変わるべきときは classmethodを使おう。
    
    staticmethod: 継承クラスでも動作が変わらないときはstaticmethodを使おう

どちらもデコレーターで定義できる。classmethodでは第一引数にclsを与えて定義する。
```

```
class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        """平均成績を返す

        インスタンス変数にアクセスしたいのでinstancemethodを使う。
        """
        return sum(self.marks) / len(self.marks)

    @classmethod
    def friend(cls, origin, friend_name, *args):
        """同じ学校の友達を追加する。

        継承クラスで動作が変わるべき(継承クラスでは salaryプロパティがある)
        なのでclassmethodを使う。
        子クラスの初期化引数は *argsで受けるのがいい
        """
        return cls(friend_name, origin.school, *args)

    @staticmethod
    def say_hello():
        """先生に挨拶する

        継承しても同じ動きでいいのでstaticmethodを使う
        """
        print("Hello Teacher!")

class WorkingStudent(Student):
    def __init__(self, name, school, salary):
        super().__init__(name, school)
        self.salary = salary

hiro = WorkingStudent("Hiro", "Stanford", 20.00)
mitsu = WorkingStudent.friend(hiro, "Mitsu", 15.00)
print(mitsu.salary)
```

[PythonのABC - 抽象クラスとダック・タイピング posted at Dec 08, 2015](https://qiita.com/kaneshin/items/269bc5f156d86f8a91c4)  
## @abstractmethod  
```
抽象メソッドを示すデコレータです。
抽象メソッドですが、デコレータを指定したメソッドに処理を記述し、サブクラスから呼び出すことも可能です。
```

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Animal(metaclass=ABCMeta):
    @abstractmethod
    def sound(self):
        print("Hello")

# 抽象クラスを継承
class Cat(Animal):
    def sound(self):
        # 継承元のsoundを呼び出す
        super(Cat, self).sound()
        print("Meow")

if __name__ == "__main__":
    print(Cat().sound())
```

```
super(Cat, self).sound()で継承元の抽象メソッドを呼び出すことができます。Javaとは少し違う印象ですね。
```

## @abstractclassmethod (version 3.2)  
```
class Animal(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def sound_classmethod(self):
        pass
```

## @abstractstaticmethod (version 3.2)  
```
class Animal(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def sound_staticmethod(self):
        pass
```

## Duck Typing（ダック・タイピング） 
```
"If it walks like a duck and quacks like a duck, it must be a duck." 
- 「アヒルのように歩き、鳴けば、それはアヒルだ。」
```

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Animal(metaclass=ABCMeta):
    @abstractmethod
    def sound(self):
        pass

class Cat(Animal):
    def sound(self):
        print("Meow")

class Dog():
    def sound(self):
        print("Bow")

class Book():
    pass

Animal.register(Dog)

def output(animal):
    print(animal.__class__.__name__, end=": ")
    animal.sound()

if __name__ == "__main__":
    c = Cat()
    output(c)

    d = Dog()
    output(d)

    b = Book()
    output(b)
```

```
Cat: Meow
Dog: Bow
AttributeError: 'Book' object has no attribute 'sound'
```


# Environment  
windows 10 64bit  
python 3.6.2  

# Troubleshooting  
## Permission denied error by installing matplotlib  
* [Permission denied error by installing matplotlib 2018年4月29日](https://stackoverflow.com/questions/50087098/permission-denied-error-by-installing-matplotlib)  
```
Windows

From the Command Prompt, you can install the package for your user only, like this:
pip install <package> --user

OR

You can install the package as Administrator, by following these steps:
    Right click on the Command Prompt icon.
    Select the option Run This Program As An Administrator.
    Run the command pip install <package>
```

## Python 3 ImportError: No module named 'ConfigParser'  
[Python 3 ImportError: No module named 'ConfigParser' ](https://stackoverflow.com/questions/14087598/python-3-importerror-no-module-named-configparser)  
```
In Python 3, ConfigParser has been renamed to configparser for PEP 8 compliance. It looks like the package you are installing does not support Python 3.
```


# Reference  
## 如何在 Windows 打造 Python 開發環境設定基礎入門教學  
* [如何在 Windows 打造 Python 開發環境設定基礎入門教學](https://happycoder.org/2017/11/17/how-to-setup-python-development-environment-in-windows/)  
```
  1.  安裝 Microsoft VSCode
  2.  安裝 Cmder
  3.  安裝 Anaconda（記得勾選加入環境變數）
  4.  安裝 virtualenv (在終端機使用：pip install virtualenv 安裝)
  5.  在桌面創建一個 python_example 資料夾，打開 Microsoft VSCode 後開啟該專案資料夾，創建一個 hello.py 的檔案並在裡面打上 print('hello python!!')
  6.  打開 cmder 終端機 cd 移動到 hello.py 所在資料夾
  7.  執行 python hello.py，恭喜你完成第一個 Python 程式！
```

## How can I download Anaconda for python 3.6  
[How can I download Anaconda for python 3.6](https://stackoverflow.com/questions/54801513/how-can-i-download-anaconda-for-python-3-6)  
```
As suggested here, with an installation of the last anaconda you can create an environment 
just like Cleb explained or downgrade python :
conda install python=3.6.0

With this second solution, you may encouter some incompatibility issues with other packages. 
I tested it myself and did not encouter any issue but I guess it depends on the packages you installed.

If you don't want to handle environments or face incompatibilities issues, 
you can download any Anaconda version here: https://repo.continuum.io/archive/. 
For example, Anaconda3-5.1.0-XXX or Anaconda3-5.2.0-XXX provides python 3.6 
(the sufffix XXX depends on your OS).
```

* [在Windows底下最適當安裝Python環境的方法 2018-11-30](https://ithelp.ithome.com.tw/articles/10210071?sc=rss.qu)  
```
結論

其實Python在Windows有很多因為路徑爆炸的問題，目前有遇到兩個
1.路徑太長
2.路徑不能有空白
這就是為什麼不安裝在預設地C:\Program Files\Python36
所以不要把Python安裝在Program Files裡面是最佳解
```

* [Python windows 安裝, 心得, 教學 2018-05-21](https://wwssllabcd.github.io/blog/2018/05/21/how-to-install-python-on-windows/)  
```
  1.  最好選擇 Python 3.x, 因為選 2.7 會有檔名多國語言問題, dos 下讀檔會亂碼, py 3 就沒有這問題
  2.  最好選 32bit 的, 因為如果要打包成單一執行檔(exe file), 打包完在 32 bit 的環境跑不起來, 且有 include dll 批配的問題
  3.  要選 32bit 還是 64 bit, 基本上要看你用到的 DLL 決定, 例如你有些額外的 dll 是使用 w32 的, 那基本上你使用 64bit 的 ptyhon 就不行, 使用而且 64 bit dll 還有 ctype call address 的問題, 建議如果不想搞死自己, 那就最好是選 32bit 的比較保險

安裝時請注意以下幾點
    請注意安裝路徑, 他預設是在"使用者"目錄下面, 最好換到非中文目錄底下
    要移除時, 必須執行安裝程式後, 裡面有個uninstall, 在 window 那邊好像找不到移除方式
    安裝時選 customize install, 這樣才可以自選安裝路徑
    也順便選 Add python 3.6 to path
```

* [Python, Pip, virtualenv installation on Windows March 16, 2016](http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/)  
```
SETUP
4 Steps:
Install Python
Install Pip
Install VirtualEnv
Install VirtualEnvWrapper-win

USAGE
7 Steps:
Make a Virtual Environment
Connect our project with our Environment
Set Project Directory
Deactivate
Workon
Pip Install
Flask! 
```

* [Python args and kwargs: Demystified Sep 04, 2019](https://realpython.com/python-kwargs-and-args/)  

[Using the Python kwargs Variable in Function Definitions](https://realpython.com/python-kwargs-and-args/#using-the-python-kwargs-variable-in-function-definitions)  
```
Okay, now you’ve understood what *args is for, but what about **kwargs? **kwargs works just like *args, 
but instead of accepting positional arguments it accepts keyword (or named) arguments. Take the following example:
```

* [PYTHON安裝TALIB @ 張郎生活的筆記:: 痞客邦:: 2018年10月5日](http://tn00343140a.pixnet.net/blog/post/175064616-python%E5%AE%89%E8%A3%9Dtalib)  
```
再次參考網路的文章, 試試看用輪子吧!

https://www.lfd.uci.edu/~gohlke/pythonlibs/
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
