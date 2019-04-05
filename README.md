# note_python
Take some note of python

# Table of Content
[Installation](#installation)  
[Step1 Install Python3.6-32bit]()  
[Step2 Upgrade pip]()  
[Step3 Install VirtualEnv & Install VirtualEnvWrapper-win]()  
[Step4 Make virtualenv]()  
[Step5 Set Project Directory]()  
[Step6 Deactivate]()  
[Step7 Workon]()  
[Step8 Install modules]()  
[Step9 Check installed mdules]()  
[Step10 Install modules manually]()
[Step11 Double Check installed mdules]()    
[Step12 Dump installed modules inot requirement.txt]()    

[Troubleshooting](#troubleshooting)  
[Reference](#reference)  

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

# Troubleshooting
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

# Reference
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