Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [SSH, SCP on Paramiko](#ssh-scp-on-paramiko)
   * [Survey scp.SCPClient().get() and scp.SCPClient().put()](#survey-scpscpclientget-and-scpscpclientput)
      * [get()](#get)
      * [put()](#put)
   * [scp module for paramiko](#scp-module-for-paramiko)
      * [Uploading file-like objects](#uploading-file-like-objects)
      * [Tracking progress of your file uploads/downloads](#tracking-progress-of-your-file-uploadsdownloads)
   * [Install Paramiko and Netmiko on Windows](#install-paramiko-and-netmiko-on-windows)
      * [5. Unzip the  ~
etmiko-2.3.3.tar\dist
etmiko-2.3.3.tar file again.](#5-unzip-the--netmiko-233tardistnetmiko-233tar-file-again)
      * [6. Open cmd and use command "cd" go the this folder ~
etmiko-2.3.3.tar\dist
etmiko-2.3.3](#6-open-cmd-and-use-command-cd-go-the-this-folder-netmiko-233tardistnetmiko-233)
      * [7. Typing command "python setup.py install"](#7-typing-command-python-setuppy-install)
      * [8. It will auto install.](#8-it-will-auto-install)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of SSH, SCP on Python  

# SSH, SCP on Paramiko  
[Paramiko + scp 導入 ~ SSH接続 ~ SCPでファイル転送 updated at 2017-06-19](https://qiita.com/int_main_void/items/1cdec761b745010629d5)  

# Survey scp.SCPClient().get() and scp.SCPClient().put()  
[scp.SCPClient().get()と.put()を調べた posted at 2019-05-17](https://qiita.com/Angelan1720/items/a962e12fa81724b57526) 

```
import paramiko
import scp

# サーバに繋ぐ
with paramiko.SSHClient() as sshc:
  sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  sshc.connect(hostname='XXX.XXX.XXX.XXX', port=22, username='hoge', password='hogehoge')

  # SSHClient()の接続設定を合わせてあげる
  with scp.SCPClient(sshc.get_transport()) as scpc:
    scpc.get('取得したいファイルのパス')
```

## get() 
```
# get_example.py

with scp.SCPClient(ssh.get_transport()) as scpc:
  scpc.get(
    remote_path='取得したいファイルパス',
    local_path='保存先のパス',
    recursive=True, #再帰的に転送するならTrue
    preserve_times=True #mtimeとatimeを保存したいならTrue
  )
```

## put()  
```
#origin_example.py

from paramiko import SSHClient
from scp import SCPClient

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('example.com')

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())

# -------------------- この部分 -------------------------
scp.put('test.txt', 'test2.txt') #(files, remote_path)
scp.get('test2.txt') #(remote_path)
# -----------------------------------------------------
```

# paramiko+scp  
[paramiko+scpで共有サーバにファイル転送する updated at 2018-03-08](https://qiita.com/Kata_Oka/items/d361ed94db8f680e3d6d)  
```
import paramiko
import scp

with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='XXX.XXX.XXX.XX', port=22, username='username', password='password')
with scp.SCPclient(ssh.get_transport()) as scp:
        scp.put('filename', '/upload/to/remote/directory/')
        scp.get('/upload/to/remote/directory/')

```

[python:ローカルファイルをtimestampでソートしてscpで転送 posted at 2018-03-08](https://qiita.com/Kata_Oka/items/48990fb4aeda9d367cb5)  
local.py  
```
import os 

localpath = r"C:\test

def sorted_ls(localpath):
    mtime = lambda m: os.stat(os.path.join(localpath, m)).st_mtime
    return list(sorted(os.listdir(localpath), key=mtime))

print(sorted_ls(localpath))
```

ssh.py  
```
#-*- coding:utf-8 -*-
import paramiko
import scp
import os

localpath = 'localpath'
remotepath = 'remotepath'

def sorted_ls(localpath):
    mtime = lambda x: os.stat(os.path.join(localpath, x)).st_mtime
    return list(sorted(os.listdir(localpath), key=mtime))

files = sorted_ls(localpath)

with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username=username, password=password)

    with scp.SCPClient(ssh.get_transport()) as scp:
        for f in files:
            scp.put(localpath + f,remotepath)
            os.remove(localpath + f)
```


# scp module for paramiko  
[jbardin/scp.py (https://github.com/jbardin/scp.py)  

## Uploading file-like objects  
[Uploading file-like objects](https://github.com/jbardin/scp.py#uploading-file-like-objects)  
```
import io
from paramiko import SSHClient
from scp import SCPClient

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('example.com')

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())

# generate in-memory file-like object
fl = io.BytesIO()
fl.write(b'test')
fl.seek(0)
# upload it directly from memory
scp.putfo(fl, '/tmp/test.txt')
# close connection
scp.close()
# close file handler
fl.close()
```

## Tracking progress of your file uploads/downloads  
[Tracking progress of your file uploads/downloads](https://github.com/jbardin/scp.py#tracking-progress-of-your-file-uploadsdownloads)  

> A progress function can be given as a callback to the SCPClient to handle how the current SCP operation handles the progress of the transfers. In the example below we print the percentage complete of the file transfer.  

```
from paramiko import SSHClient
from scp import SCPClient
import sys

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('example.com')

# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

# SCPCLient takes a paramiko transport and progress callback as its arguments.
scp = SCPClient(ssh.get_transport(), progress=progress)

# you can also use progress4, which adds a 4th parameter to track IP and port
# useful with multiple threads to track source
def progress4(filename, size, sent, peername):
    sys.stdout.write("(%s:%s) %s\'s progress: %.2f%%   \r" % (peername[0], peername[1], filename, float(sent)/float(size)*100) )
scp = SCPClient(ssh.get_transport(), progress4=progress4)

scp.put('test.txt', '~/test.txt')
# Should now be printing the current progress of your put function.

scp.close()
```

# Install Paramiko and Netmiko on Windows  
[05 - Install Paramiko and Netmiko on Windows 10月 08, 2018](http://juilin77.blogspot.com/2018/10/05-install-paramiko-and-netmiko-on.html)  

## 5. Unzip the  ~\netmiko-2.3.3.tar\dist\netmiko-2.3.3.tar file again.  

## 6. Open cmd and use command "cd" go the this folder ~\netmiko-2.3.3.tar\dist\netmiko-2.3.3

## 7. Typing command "python setup.py install"  

## 8. It will auto install.  
![alt tag](https://1.bp.blogspot.com/-PrVaLv3K3B4/XRLlrKmZxAI/AAAAAAAACCA/j8Q06CrK6qsJolr5mhs0_2ax9VOUbKFkACLcBGAs/s1600/8.jpg)  


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



