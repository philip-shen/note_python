
Table of Contents
=================
   * [Purpose](#purpose)
   * [ezhov-evgeny/webdav-client-python-3](#ezhov-evgenywebdav-client-python-3)
   * [python filesystem spec](#python-filesystem-spec)
      * [fsspec/gcsfs](#fsspecgcsfs)
      * [fsspec/sshfs](#fsspecsshfs)
      * [fsspec/ossfs](#fsspecossfs)
      * [fsspec/dropboxdrivefs](#fsspecdropboxdrivefs)
   * [skshetry/webdav4](#skshetrywebdav4)
      * [fsspec](#fsspec)
   * [CloudPolis/webdav-client-python](#cloudpoliswebdav-client-python)
   * [amnong/easywebdav](#amnongeasywebdav)
      * [Features](#features)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose  
Take some note of python filesystem spec 


# ezhov-evgeny/webdav-client-python-3  
[ezhov-evgeny/webdav-client-python-3](https://github.com/ezhov-evgeny/webdav-client-python-3)

Package webdavclient3 based on https://github.com/designerror/webdav-client-python but uses requests instead of PyCURL. It provides easy way to work with WebDAV-servers. 


# python filesystem spec 
[python filesystem spec ](https://github.com/orgs/fsspec/repositories?type=all)

## fsspec/gcsfs
[fsspec/gcsfs](https://github.com/fsspec/gcsfs)  
Pythonic file-system for Google Cloud Storage  

## fsspec/sshfs  
[fsspec/sshfs](https://github.com/fsspec/sshfs)
sshfs is an implementation of fsspec for the SFTP protocol using asyncssh.  

## fsspec/ossfs
[fsspec/ossfs](https://github.com/fsspec/ossfs)  
OSSFS is a Python-based interface for file systems that enables interaction with OSS (Object Storage Service). Through OSSFS, users can utilize fsspec's standard API to operate on OSS objects  

## fsspec/dropboxdrivefs 
[fsspec/dropboxdrivefs](https://github.com/fsspec/dropboxdrivefs)
dropbox implementation for intake module 


#  skshetry/webdav4 
[skshetry/webdav4](https://github.com/skshetry/webdav4)  

Webdav API with an (optional) fsspec[https://github.com/skshetry/webdav4#fsspec] implementation and a CLI[https://github.com/skshetry/webdav4#cli].
 
## fsspec 
```
$ pip install webdav4[fsspec]
```

```
from webdav4.fsspec import WebdavFileSystem

fs = WebdavFileSystem("https://webdav.com", auth=("username", "password"))
fs.exists("Documents/Readme.md")

fs.ls("Photos", detail=False)
```


# CloudPolis/webdav-client-python 
[CloudPolis/webdav-client-python](https://github.com/CloudPolis/webdav-client-python)    

Package webdavclient provides easy and convenient work with WebDAV-servers (Yandex.Drive, Dropbox, Google Drive, Box, 4shared, etc.). The package includes the following components: webdav API, resource API and wdc.  

# amnong/easywebdav  
[amnong/easywebdav](https://github.com/amnong/easywebdav)

## Features
* Basic authentication
* Creating directories, removing directories and files
* Uploading and downloading files
* Directory listing
* Support for client side SSL certificates



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
