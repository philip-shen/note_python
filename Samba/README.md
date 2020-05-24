Table of Contents  
=================


# Purpose
Taken note of Samba Stuffs by Python 

# Windows Floders Access by Python  
[PythonでWindows共有フォルダへアクセス updated at 2018-04-23](https://qiita.com/t2kojima/items/250d68c56a8c9fe95f52)  

## Environment  
```
python 3.5.3
pysmb 1.1.19
```

## Installation  
```
pip install pysmb
```

## Get File List  
> \\<ip_address>\temp\a\b\cのファイルリストを取得する場合  

```
# samba_test.py

# !/usr/bin/env python
# coding:utf-8

import platform
from smb.SMBConnection import SMBConnection

if __name__ == "__main__":

    # connection open
    conn = SMBConnection(
        '<user>',
        '<password>',
        platform.uname().node,
        '<remote_hostname>',
        domain='WORKGROUP',
        use_ntlm_v2=True)
    conn.connect('<ip_address>', 139)

    items = conn.listPath('temp', 'a/b/c')
    print([item.filename for item in items])

    conn.close()
```
* itemsへはSharedFileクラスのリストが返される。
* tempおよびa/b/cが存在しない場合は当然エラーとなる。
* domainは指定しなくても繋がるよう、domain=''でもOK

## Get a File   
> \\<ip_address>\temp\a\b\c\hoge.txtを/var/hogeとして保存する。  

```
#samba_test.py

# !/usr/bin/env python
# coding:utf-8
""" samba_test.py """

import platform
from smb.SMBConnection import SMBConnection

if __name__ == "__main__":

    # connection open
    conn = SMBConnection(
        '<user>',
        '<password>',
        platform.uname().node,
        '<remote_hostname>',
        domain='WORKGROUP',
        use_ntlm_v2=True)
    conn.connect('<ip_address>', 139)

    with open('/var/hoge', 'wb') as file:
        conn.retrieveFile('temp', 'a/b/c/hoge.txt', file)

    conn.close()
```

> ファイル自体は不要で、中身だけ知りたい場合はBytesIOを使う  

```
#samba_test.py

import io

with io.BytesIO() as file:
    conn.retrieveFile('temp', 'a/b/c/hoge.txt', file)
    file.seek(0)
    print([line.decode() for line in file])
```

## Write a File  
> /var/hogeを\\<ip_address>\temp\a\b\c\hoge.txtとして保存する。  

```
# samba_test.py

# !/usr/bin/env python
# coding:utf-8
""" samba_test.py """

import platform
from smb.SMBConnection import SMBConnection

if __name__ == "__main__":

    # connection open
    conn = SMBConnection(
        '<user>',
        '<password>',
        platform.uname().node,
        '<remote_hostname>',
        domain='WORKGROUP',
        use_ntlm_v2=True)
    conn.connect('<ip_address>', 139)

    with open('/var/hoge', 'rb') as file:
        conn.storeFile('temp', 'a/b/c/hoge.txt', file)

    conn.close()
```
* ディレクトリa/b/cが存在しない場合はエラーになるので事前に作成しておく必要がある。  

## pysmbの使い方（ロギング）   
[pysmbの使い方（ロギング）updated at 2018-04-24](https://qiita.com/t2kojima/items/4fc5e2e2c041b2c16824)  
```

```

### ルートロガーに出力  
[ルートロガーに出力](https://qiita.com/t2kojima/items/4fc5e2e2c041b2c16824#%E3%83%AB%E3%83%BC%E3%83%88%E3%83%AD%E3%82%AC%E3%83%BC%E3%81%AB%E5%87%BA%E5%8A%9B)  
```
import logging
import platform
from smb.SMBConnection import SMBConnection

logging.basicConfig(filename='example.log', level=logging.DEBUG)

conn = SMBConnection(
    'IEUser',
    'Passw0rd!',
    platform.uname().node,
    'IEWIN7')
conn.connect('172.28.0.198', 139)

logging.info(conn.listPath('Share', ''))

conn.close()
```

### ロガーを分けて出力  
[ロガーを分けて出力](https://qiita.com/t2kojima/items/4fc5e2e2c041b2c16824#%E3%83%AD%E3%82%AC%E3%83%BC%E3%82%92%E5%88%86%E3%81%91%E3%81%A6%E5%87%BA%E5%8A%9B)  

> dictConfigを使うパターンです。  

```
from logging import getLogger
from logging.config import dictConfig
import platform
from smb.SMBConnection import SMBConnection

dictConfig({
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(name)s %(module)s.%(funcName)s [%(levelname)s] %(message)s"
        },
    },
    "handlers": {
        "app_name": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": 'app_name.log',
        },
        "smb": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": 'smb.log',
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": []
    },
    'loggers': {
        "app_name": {
            "level": "DEBUG",
            "handlers": ["app_name"]
        },
        "SMB.SMBConnection": {
            "level": "DEBUG",
            "handlers": ["smb"]
        }
    },
    "disable_existing_loggers": False,
})

logger = getLogger('app_name')

conn = SMBConnection(
    'IEUser',
    'Passw0rd!',
    platform.uname().node,
    'IEWIN7')
conn.connect('172.28.0.198', 139)

logger.info(conn.listPath('Share', ''))

conn.close()
```

## pysmbの使い方（接続・切断）  
[pysmbの使い方（接続・切断）updated at 2018-04-24](https://qiita.com/t2kojima/items/5db8dadaa6e07321d25f)  
```

```

### Connection  
> 接続に失敗した場合は以下のような例外を投げます。  

* usernameやpasswordが間違っている場合はNotReadyError
* remote_nameが間違っている場合はNotConnectedError
* ipやportが間違っている場合はTimeoutError

### Close 

```
from samba import Smb

params = {
    'username': 'IEUser',
    'password': 'Passw0rd!',
    'remote_name': 'IEWIN7',
    'ip': '172.28.0.198'
}
with Smb(**params) as smb:
    print(smb.echo("echo !!"))
```
>まあ、close()忘れを気にしなくていいくらいで

## pysmbの使い方（ファイル受信）  
[pysmbの使い方（ファイル受信）updated at 2018-04-24](https://qiita.com/t2kojima/items/6c20a7801467221470ac)  
```

```

### SharedFile  
[SharedFile](https://qiita.com/t2kojima/items/6c20a7801467221470ac#sharedfile)  
```
files = [f.filename for f in conn.listPath('Share', '/')]
```
```
    filename
    ファイル名（もしくはフォルダ名）

    short_name
    8.3形式の短いファイル名

    file_attributes
    SMB_EXT_FILE_ATTRの論理和、詳しくは[MS-CIFS]: 2.2.1.2.3を参照

    alloc_size
    ファイルを格納する為割り当てられたサイズ、いわゆるディスク上のサイズ（Byte）

    file_size 
    ファイルのサイズ（Byte）

    create_time
    1970-01-01 00:00:00からの経過秒数でファイル作成日時を表す。
    
    last_access_time
    1970-01-01 00:00:00からの経過秒数で最終ファイルアクセス日時を表す。
    
    last_write_time
    1970-01-01 00:00:00からの経過秒数で最終ファイル更新日時を表す。
    
    last_attr_change_time
    1970-01-01 00:00:00からの経過秒数で最終ファイル属性変更日時を表す。
    
    isDirectory
    フォルダかどうか
    
    isReadOnly
    読み取り専用かどうか
```

### 共有フォルダのファイルを全部列挙  
```
def list_all(service_name, path=''):
    entries = conn.listPath(service_name, path)
    for item in (e for e in entries if not e.filename in ['.', '..']):
        if item.isDirectory:
            yield from list_all(service_name, path=f'{path}/{item.filename}')
        else:
            yield f'{path}/{item.filename}'


print([f for f in list_all('Share')])
```

## pysmbの使い方（ファイル送信）   
[pysmbの使い方（ファイル送信）updated at 2018-04-24](https://qiita.com/t2kojima/items/a6b81de771ac45c9948b)  
```

```

### フォルダを作る  
[フォルダを作る](https://qiita.com/t2kojima/items/a6b81de771ac45c9948b#%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E3%82%92%E4%BD%9C%E3%82%8B)  
```
def exists(service_name, path):
    parent = Path(path).parent.as_posix().replace('.', '/')
    if parent == '/' or exists(service_name, parent):        
        return bool([f for f in conn.listPath(service_name, parent) if f.filename == Path(path).name])


def makedirs(service_name, path):
    parent = Path(path).parent.as_posix().replace('.', '/')
    if not parent == '/' and not exists(service_name, parent):
        makedirs(service_name, parent)
    if not exists(service_name, path):
        conn.createDirectory(service_name, path)


makedirs('Share', 'aaa/bbb/ccc')
```

### フォルダの削除  
[フォルダの削除](https://qiita.com/t2kojima/items/a6b81de771ac45c9948b#%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E3%81%AE%E5%89%8A%E9%99%A4)  
```
def exists(service_name, path):
    parent = Path(path).parent.as_posix().replace('.', '/')
    if parent == '/' or exists(service_name, parent):        
        return bool([f for f in conn.listPath(service_name, parent) if f.filename == Path(path).name])


def removedirs(service_name, path):
    if exists(service_name, path):
        entries = conn.listPath(service_name, path)
        for item in (e for e in entries if not e.filename in ['.', '..']):
            if item.isDirectory:
                removedirs(service_name, f'{path}/{item.filename}')                
            else:
                conn.deleteFiles(service_name, f'{path}/{item.filename}')
        conn.deleteDirectory(service_name, path)

removedirs('Share', 'aaa/bbb/ccc')
# -> 'ccc'フォルダ配下は全て削除
```

## pysmbの使い方（匿名接続）  
[pysmbの使い方（匿名接続）posted at 2018-04-24](https://qiita.com/t2kojima/items/c84a803c73daf043f053)  

### WindowsVista以降の場合   
```
「パスワード保護共有」をオフにすることで簡易に匿名アクセスが有効になります。この方法ではGuestアカウントを有効にする必要もありません。

コントロールパネルのネットワークと共有センターを開き、左側のメニューから共有の詳細設定を選びます。パスワード保護共有という項目があるのでオフに設定します。
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F204683%2Fdb8752a7-37bd-7be9-c3c3-413167556bb8.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=5f44ba49f0aea95e62f5e298ba95e831)  

```
# main.py

import platform
from smb.SMBConnection import SMBConnection

conn = SMBConnection(
    '',
    '',
    platform.uname().node,
    'IEWIN7')
conn.connect('172.28.0.198', 139)

print(conn.echo('echo success'))

conn.close()
```

```
from smb.SMBConnection import SMBConnection

conn = SMBConnection(
    'a',
    'a',
    'a',
    'a',
    is_direct_tcp=True)
conn.connect('172.28.0.198', 445)

print(conn.echo('echo success'))

conn.close()
```


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
