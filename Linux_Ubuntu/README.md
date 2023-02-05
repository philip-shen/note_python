
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Note of Python on Ubuntu](#note-of-python-on-ubuntu)
   * [ubuntu安裝python3.7，並更新python默認指向爲python3.7](#ubuntu安裝python37並更新python默認指向爲python37)
      * [改爲手動安裝](#改爲手動安裝)
      * [更新python默認指向爲python3.7](#更新python默認指向爲python37)
   * [Python3 Virtual Environment](#python3-virtual-environment)
      * [Ubuntu_01](#ubuntu_01)
      * [Ubuntu_02](#ubuntu_02)
      * [Windows 10](#windows-10)
   * [Creating a Virtual Environment for Python on Ubuntu 16.04](#creating-a-virtual-environment-for-python-on-ubuntu-1604)
      * [Step 1: Install Virtualenv](#step-1-install-virtualenv)
         * [below is wrong](#below-is-wrong)
      * [Step 2: Create a Virtual Environment &amp; Install Python 3](#step-2-create-a-virtual-environment--install-python-3)
      * [Step 3: Activate Your Virtual Environment](#step-3-activate-your-virtual-environment)
   * [Install Python 2.7](#install-python-27)
   * [Update Python 3.5 to 3.6 via terminal after installed Python3.6](#update-python-35-to-36-via-terminal-after-installed-python36)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
      * [Method 1: Manually Installing Python](#method-1-manually-installing-python)
      * [Method 2: Installing Python via PPA](#method-2-installing-python-via-ppa)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Note of Python on Ubuntu
Take some note of Python on Ubuntu


# ubuntu安裝python3.7，並更新python默認指向爲python3.7
[ubuntu安裝python3.7，並更新python默認指向爲python3.7 2018-12-25](https://www.twblogs.net/a/5c2245eabd9eee16b3dafa25)  
## 改爲手動安裝  
Step0: sudo apt update; sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget

步驟1：在python官網找到python-3.7.1.tgz的地址：https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz  
步驟2：wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz  下載安裝包  
步驟3：tar -zxvf Python-3.7.1.tgz  解壓安裝包  
步驟4：cd Python-3.7.1.tgz  切換到解壓後的目錄下  
步驟5：./configure  
步驟6：make
             沒有安裝make的安裝一下       
步驟7：make test
             關於make test命令出現ModuleNotFoundError: No module named ‘_ctypes’ 錯誤，請移步我的另外一篇博文https://blog.csdn.net/u014775723/article/details/85224447  
步驟8：sudo make install（安裝後可執行文件默認放在/usr /local/bin，庫文件默認放在/usr/local/lib，配置文件默認放在/usr/local/etc，其它的資源文件放在/usr /local/share）  
步驟9：查看安裝目錄，可以看到此時python3.7安裝到了/usr/local/lib/  
步驟10：測試，輸入python3.7  
## 更新python默認指向爲python3.7  
步驟1：ls -l /usr/bin | grep python  查看python命令指向  
步驟2：rm /usr/bin/python 刪除原有鏈接  
步驟3：一般來說，如步驟1的圖，python3.4爲系統自帶的，可以直接用 ln -s /usr/bin/python3.4 /usr/bin/python建立新鏈接，但是由於python3.7是自己安裝的，不在/usr/bin下，而在usr/local/bin下。 因此需要先加一條軟鏈接並且把之前的python命令改爲python.bak，同時pip也需要更改。依次執行以下命令  
![alt tag](https://pic1.xuehuaimg.com/proxy/csdn/https://img-blog.csdnimg.cn/20181224174631859.PNG)  

```
mv /usr/bin/python /usr/bin/python.bak
ln -s /usr/local/bin/python3 /usr/bin/python
mv /usr/bin/pip /usr/bin/pip.bak
ln -s /usr/local/bin/pip3 /usr/bin/pip
```
```
sudo mv /usr/bin/python3 /usr/bin/python3.bak
sudo ln -s /usr/local/bin/python3 /usr/bin/python3
sudo ln -s /usr/local/bin/pip3 /usr/bin/pip3
```

步驟4：此時輸入python驗證  
```
$ python3 --version
Python 3.6.8
```

setp5: Test pip3
```
sudo mv /usr/bin/lsb_release /usr/bin/lsb_release-old

$ pip3 list
Package    Version
---------- -------
pip        18.1
setuptools 40.6.2
You are using pip version 18.1, however version 19.1.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

```

# Python3 Virtual Environment 

## Ubuntu_01
[建立 Python 的虛擬環境 2022-12-30](https://cynthiachuang.github.io/Create-a-Virtual-Environment-for-Python/)

```
$ sudo apt-get install python3-venv
```

```
$ python3 -m venv ~/virtual/pytorch
```

```
$ ls -al ~/virtualenv/
```

```
$ source ~/virtualenv/pytorch/bin/activate
```

```
(pytorch)$ pip list -l
Package                Version      
---------------------- -------------
appdirs                1.4.3        
apturl                 0.5.2        
bcrypt                 3.1.7        
blinker                1.4          
Brlapi                 0.7.0        
certifi                2019.11.28   
chardet                3.0.4        
Click                  7.0          
colorama               0.4.3        
command-not-found      0.3          
cryptography           2.8          
cupshelpers            1.0          
dbus-python            1.2.16       
defer                  1.0.6        
distlib                0.3.6        
distro                 1.4.0        
distro-info            0.23ubuntu1  
duplicity              0.8.12.0     
entrypoints            0.3          
fasteners              0.14.1       
filelock               3.9.0        
future                 0.18.2       
httplib2               0.14.0       
idna                   2.8          
importlib-metadata     1.5.0        
keyring                18.0.1       
language-selector      0.1          
launchpadlib           1.10.13      
lazr.restfulclient     0.14.2       
lazr.uri               1.0.3        
lockfile               0.12.2       
louis                  3.12.0       
macaroonbakery         1.3.1        
Mako                   1.1.0        
MarkupSafe             1.1.0        
monotonic              1.5          
more-itertools         4.2.0        
netifaces              0.10.4       
oauthlib               3.1.0        
olefile                0.46         
paramiko               2.6.0        
pexpect                4.6.0        
Pillow                 7.0.0        
pip                    20.0.2       
platformdirs           2.6.2        
protobuf               3.6.1        
pycairo                1.16.2       
pycups                 1.9.73       
PyGObject              3.36.0       
PyJWT                  1.7.1        
pymacaroons            0.13.0       
PyNaCl                 1.3.0        
pyRFC3339              1.1          
python-apt             2.0.1        
python-dateutil        2.7.3        
python-debian          0.1.36ubuntu1
pytz                   2019.3       
pyxdg                  0.26         
PyYAML                 5.3.1        
reportlab              3.5.34       
requests               2.22.0       
requests-unixsocket    0.2.0        
SecretStorage          2.3.1        
setuptools             45.2.0       
simplejson             3.16.0       
six                    1.14.0       
systemd-python         234          
ubuntu-advantage-tools 27.10        
ubuntu-drivers-common  0.0.0        
ufw                    0.36         
unattended-upgrades    0.1          
urllib3                1.25.8       
usb-creator            0.3.7        
virtualenv             20.17.1      
wadllib                1.3.3        
wheel                  0.34.2       
xkit                   0.0.0        
zipp                   1.0.0        
```

```
$ deactivate
```

```
$ pip list -l
Package      Version
------------ -------
distlib      0.3.6  
filelock     3.9.0  
platformdirs 2.6.2  
virtualenv   20.17.1
```

## Ubuntu_02
[Python - Python3 虛擬環境參考筆記 2021-09-17](https://ithelp.ithome.com.tw/articles/10265702)

```
sudo pip3 install virtualenvwrapper
```

下文字添加到 shell 啟動文件的末尾（這是家目錄中的隱藏文件名： .bashrc）。
```
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```
*注意： VIRTUALENVWRAPPER_PYTHON 和 VIRTUALENVWRAPPER_VIRTUALENV_ARGS 變數是指向 Python3 的正常安裝位置，source /usr/local/bin/virtualenvwrapper.sh指向 virtualenvwrapper.sh 腳本的正常位置。*
*如果 virtualenv 在測試時不起作用，那麼要檢查的地方就是 Python 和 .sh 腳本是否位於預期的位置（然後適當地更改啟動文件）。*

*您可以使用 which virtualenvwrapper.sh 和 which python3. 的指令找到系統的正確位置。*

```
source ~/.bashrc
```

*完成之後，就可以使用 mkvirtualenv 指令來建立新的虛擬環境。*

## Windows 10

# Creating a Virtual Environment for Python on Ubuntu 16.04  
[Creating a Virtual Environment for Python on Ubuntu 16.04 Updated: January 11, 2019](https://www.liquidweb.com/kb/creating-virtual-environment-ubuntu-16-04/)  

## Step 1: Install Virtualenv  
```
$ sudo pip install virtualenv
```
```
~$  pip3 show virtualenv
Name: virtualenv
Version: 16.6.1
Summary: Virtual Python Environment builder
Home-page: https://virtualenv.pypa.io/
Author: Ian Bicking
Author-email: ianb@colorstudy.com
License: MIT
Location: /usr/local/lib/python3.6/site-packages
Requires:
Required-by:

```

### below is wrong  
```
$ pip install virtualenv --user
```
```
$ pip3 show virtualenv
Name: virtualenv
Version: 16.6.1
Summary: Virtual Python Environment builder
Home-page: https://virtualenv.pypa.io/
Author: Ian Bicking
Author-email: ianb@colorstudy.com
License: MIT
Location: /home/test/.local/lib/python3.6/site-packages
Requires:
Required-by:
```

## Step 2: Create a Virtual Environment & Install Python 3  
```
~$ virtualenv -p /usr/bin/python3 virtualenv/iperf3
Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /home/philshen/virtualenv/iperf3/bin/python3
Also creating executable in /home/philshen/virtualenv/iperf3/bin/python
Installing setuptools, pip, wheel...
done.
```
## Step 3: Activate Your Virtual Environment  
```
~$ source virtualenv/iperf3/bin/activate
(iperf3) philshen@DESKTOP-7EDV2HB:~$ pip3 list
Package    Version
---------- -------
pip        19.1.1
setuptools 41.0.1
wheel      0.33.4
(iperf3) philshen@DESKTOP-7EDV2HB:~$ deactivate
philshen@DESKTOP-7EDV2HB:~$
```

# Install Python 2.7  
[How to Install Python 2.7.16 on Ubuntu & LinuxMint May 13, 2019](https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/)  
```
Step 1 – Prerequsiteis
$ sudo apt-get update
$ sudo apt-get install build-essential checkinstall
$ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

Step 2 – Download Python 2.7
Step 3 – Compile Python Source
Step 4 – Check Python Version
```
[Install Python 2.7.6 in ubuntu 16.04 Jun 27, 2018](https://askubuntu.com/questions/1050084/install-python-2-7-6-in-ubuntu-16-04/1050098)  
```
Use the following command instead

sudo apt-get install python-minimal

This will give you the most recommended python version 2.7.12. But if you must install 2.7.6 then do the following:

wget  https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz  
./configure
make
make install

You can switch between different versions using

sudo update-alternatives --config python
```

# Update Python 3.5 to 3.6 via terminal after installed Python3.6  
[Update Python 3.5 to 3.6 via terminal ](https://askubuntu.com/questions/922853/update-python-3-5-to-3-6-via-terminal)  
```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
```
  
```
sudo update-alternatives --config python3
```

```
Then select the /usr/bin/python3.6 -- automode in choices menu, for me that was 0 row.
```

```
$ python3 --version
```
![alt tag](https://i.imgur.com/M3xxACA.jpg)


# Troubleshooting  
* [zipimport.ZipImportError: can't decompress data; zlib not available in spark(ubuntu 16.04 LTS) [closed] Feb 26, 2018](https://askubuntu.com/questions/1009998/zipimport-zipimporterror-cant-decompress-data-zlib-not-available-in-sparkubu?rq=1)  
```
Answer to a similar question raised here suggested installing zlib1g-dev in order to solve this error:

sudo apt-get install zlib1g-dev

More info about zlib1g-dev
```
* [pip is showing error 'lsb_release -a' returned non-zero exit status 1 ](https://stackoverflow.com/questions/44967202/pip-is-showing-error-lsb-release-a-returned-non-zero-exit-status-1)  
```
Ahhh the classic lsb_release issue. I have battled this problem many times. The issue is that your default Python implementation is trying to use Python 3 but lsb_release requires Python 2. To fix this problem do the following:

    Open /usr/bin/lsb_release (Make sure you use sudo or open as root!)
    Edit the first line to be #! /usr/bin/python2.7
    Save the file

now you can use pip again and everything should be fine.
```

* [Error with 'lsb_release -a' in Ubuntu 16.04 Xenial Dec 11, 2016](https://askubuntu.com/questions/853377/error-with-lsb-release-a-in-ubuntu-16-04-xenial)  
```
I also encountered this 'lsb_release -a' error these days in Ubuntu 17.10. I finally solved this issue by

sudo rm -rf /usr/bin/lsb_release

If I keep this file in computer, even if I specify a correct python directory in it, it gives me the errors: subprocess.CalledProcessError: Command 'lsb_release -a' returned non-zero exit status 1.

So, I deleted it in my computer and it works.
```

* [pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available ](https://stackoverflow.com/questions/45954528/pip-is-configured-with-locations-that-require-tls-ssl-however-the-ssl-module-in)  
```
For Debian users, the following may be of use:

$ sudo -s 
apt install libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev libtk8.5 libgdm-dev libdb4o-cil-dev libpcap-dev

Then cd to the folder with the Python 3.X library source code and run:

$ ./configure
$ make
$ make install
```


* [Can't decompress data; zlib not available ](https://askubuntu.com/questions/173829/cant-decompress-data-zlib-not-available)  
```
I don't find a Python 2.4 package for Ubuntu, so I assume you tried to compile it from source. If so, you would have had to explicitly configure and compile it with zlib support.

I found a blog article on how to do this here:

http://www.1stbyte.com/2005/06/26/configure-and-compile-python-with-zlib/

basically install zlib1g-dev, and then configure Python with

./configure --with-zlib=/usr/include

then you can do "make" to generate the Python 2.4 binaries.
```


# Reference  
* [Installing the Latest Python 3.7 on Ubuntu 16.04 / 18.04 Jan 13, 2019](https://websiteforstudents.com/installing-the-latest-python-3-7-on-ubuntu-16-04-18-04/)  
## Method 1: Manually Installing Python  
```
$ sudo apt update
$ sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget

$ cd /tmp
$ wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz

$ tar -xf Python-3.7.2.tar.xz
$ cd Python-3.7.2
$ ./configure --enable-optimizations

My machine has 1 CPU core, so I use the make command with -j 1 option…
$ make -j 1
$ sudo make altinstall

$ python3.7 --version
```

## Method 2: Installing Python via PPA  
```
sudo apt update
sudo apt install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update
sudo apt install python3.7
```

* [How to completely uninstall python 2.7.13 on Ubuntu 16.04 ](https://stackoverflow.com/questions/44602191/how-to-completely-uninstall-python-2-7-13-on-ubuntu-16-04)  
```
caution : It is not recommended to remove the default Python from Ubuntu, it may cause GDM(Graphical Display Manager, that provide graphical login capabilities) failed.

To completely uninstall Python2.x.x and everything depends on it. use this command:

sudo apt purge python2.x-minimal

As there are still a lot of packages that depend on Python2.x.x. So you should have a close look at the packages that apt wants to remove before you let it proceed.

Thanks, I hope it will be helpful for you.  
```

* [How To Install Git on Ubuntu 16.04 LTS Updated: March 8, 2019](https://www.liquidweb.com/kb/install-git-ubuntu-16-04-lts/)  
```
sudo apt-get update

sudo apt-get install git-core
git --version
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

