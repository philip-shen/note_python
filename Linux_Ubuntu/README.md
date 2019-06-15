# note of Python on Ubuntu
Take some note of Python on Ubuntu

# Table of Content
[ubuntu安裝python3.7，並更新python默認指向爲python3.7](#ubuntu%E5%AE%89%E8%A3%9Dpython37%E4%B8%A6%E6%9B%B4%E6%96%B0python%E9%BB%98%E8%AA%8D%E6%8C%87%E5%90%91%E7%88%B2python37)  
[Creating a Virtual Environment for Python on Ubuntu 16.04](#creating-a-virtual-environment-for-python-on-ubuntu-1604)  
[Reference](#reference)  

# ubuntu安裝python3.7，並更新python默認指向爲python3.7
[ubuntu安裝python3.7，並更新python默認指向爲python3.7 2018-12-25](https://www.twblogs.net/a/5c2245eabd9eee16b3dafa25)  
## 改爲手動安裝  
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

# Creating a Virtual Environment for Python on Ubuntu 16.04  
[Creating a Virtual Environment for Python on Ubuntu 16.04 Updated: January 11, 2019](https://www.liquidweb.com/kb/creating-virtual-environment-ubuntu-16-04/)  

## Step 1: Install Virtualenv  
```
$ pip install virtualenv --user
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


* []()  
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