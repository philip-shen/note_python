# Purpose  
Take note of HTTP Signatures  

# Table of Contents  
[HTTPS Stuffs](#https-stuffs)  
[HTTP Signatures](#http-signatures)  
[]()  

# HTTPS Stuffs  
[Exploring HTTPS With Python – Real Python Jan 8, 2020](https://realpython.com/python-https/)  
## How Does Cryptography Help?  
[How Does Cryptography Help?](https://realpython.com/python-https/#how-does-cryptography-help)  

```
$ pip install cryptography
```

## HTTPS connection Python  
[HTTPS connection Python ](https://stackoverflow.com/questions/2146383/https-connection-python)
To verify if SSL is enabled, try:  
```
>>> import socket
>>> socket.ssl
<function ssl at 0x4038b0>
```

## Implementing TLS Clients With Python  
[17.2.5. Implementing TLS Clients With Python](https://docs.fedoraproject.org/en-US/Fedora_Security_Team/1/html/Defensive_Coding/sect-Defensive_Coding-TLS-Client-Python.html)  
```
Currently, most Python function which accept https:// URLs or otherwise implement HTTPS support do not perform certificate validation at all. (For example, this is true for the httplib and xmlrpclib modules.) If you use HTTPS, you should not use the built-in HTTP clients. The Curl class in the curl module, as provided by the python-pycurl package implements proper certificate validation. 
```

## SSL Certificate Verification  
[[Python] python遷入信任憑證| 阿輝的零碎筆記- 點部落 Jun 21, 2018](https://dotblogs.com.tw/grayyin/2018/06/21/144121)  
```
最近執行python叫用API時發生憑證問題,
執行 request.get(...) 時發生錯誤.

兩個解法,
1. Disable SSL verify驗證.
2. 把目標server 的 cert加入python執行環境的信任憑證清單中.
```
### 1. Disable SSL verify驗證.
```
>>> requests.get('https://kennethreitz.org', verify=False)
<Response [200]>
```
```
>>> requests.get('https://kennethreitz.org', cert=('/path/client.cert', '/path/client.key'))
<Response [200]>
```

```
>>> requests.get('https://www.twse.com.tw/exchangeReport/MI_INDEX?date=20200930&response=json&type=ALL&_=1601807588776', verify=False)

Traceback (most recent call last):
  File "C:\Users\SCS\Envs\MoneyHunter\lib\site-packages\urllib3\connectionpool.py", line 600, in urlopen
    chunked=chunked)
  File "C:\Users\SCS\Envs\MoneyHunter\lib\site-packages\urllib3\connectionpool.py", line 343, in _make_request
    self._validate_conn(conn)
  File "C:\Users\SCS\Envs\MoneyHunter\lib\site-packages\urllib3\connectionpool.py", line 839, in _validate_conn
    conn.connect()
  File "C:\Users\SCS\Envs\MoneyHunter\lib\site-packages\urllib3\connection.py", line 344, in connect
    ssl_context=context)
  File "C:\Users\SCS\Envs\MoneyHunter\lib\site-packages\urllib3\util\ssl_.py", line 344, in ssl_wrap_socket
    return context.wrap_socket(sock, server_hostname=server_hostname)
  File "c:\programdata\anaconda3\Lib\ssl.py", line 407, in wrap_socket
    _context=self, _session=session)
  File "c:\programdata\anaconda3\Lib\ssl.py", line 814, in __init__
    self.do_handshake()
  File "c:\programdata\anaconda3\Lib\ssl.py", line 1068, in do_handshake
    self._sslobj.do_handshake()
  File "c:\programdata\anaconda3\Lib\ssl.py", line 689, in do_handshake
    self._sslobj.do_handshake()
ConnectionResetError: [WinError 10054] 遠端主機已強制關閉一個現存的連線。
```

### 2. 把目標server 的 cert加入python執行環境的信任憑證清單中.   
[Creating a .pem File for SSL Certificate Installations ](https://www.digicert.com/kb/ssl-support/pem-ssl-creation.htm)  

```
# pip install certifi --no-verify --proxy=http://proxy-server.com:80
```

```
pyton → >> import certifi → >> certifi.where() → usually python certifi cacert.pem located /usr/lib/python2.7/site-packages/certifi/cacert.pem
```

## CA Installation  
[独自(root)CA のインストール方法 Jan 25, 2020](https://qiita.com/msi/items/9cb90271836386dafce3)  

### python - certifi/requests の CA 設定  
[python - certifi/requests の CA 設定](https://qiita.com/msi/items/9cb90271836386dafce3#python---certifirequests-%E3%81%AE-ca-%E8%A8%AD%E5%AE%9A)  
```
λ python -c "import certifi; print(certifi.where())"
C:\Users\~\lib\site-packages\certifi\cacert.pem
```

```
λ python -c "import requests;print(requests.__version__)"
2.24.0
```

```
λ python -c "import requests; print(requests.certs.where())"
C:\Users\~\lib\site-packages\certifi\cacert.pem
```

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import certifi

cabundle = certifi.where()
local_rootCA = 'mylocal-root-cacert.crt'

print( 'read from {}'.format( local_rootCA ) )
with open( local_rootCA, 'rb' ) as infile:
    myrootca = infile.read()

print( 'append to {}'.format( cabundle ) )
with open( cabundle, 'ab' ) as outfile:
    outfile.write( myrootca )

print( '{} has been imported.'.format( local_rootCA ) )
```

### python - ssl の設定  
```
$ python3 -c "import ssl; print(ssl.get_default_verify_paths())"; (set -x; ls -l /usr/lib/ssl)
DefaultVerifyPaths(cafile=None, capath='/usr/lib/ssl/certs', openssl_cafile_env='SSL_CERT_FILE', openssl_cafile='/usr/lib/ssl/cert.pem', openssl_capath_env='SSL_CERT_DIR', openssl_capath='/usr/lib/ssl/certs')
+ ls -l /usr/lib/ssl
total 4
lrwxrwxrwx 1 root root   14 Apr 23  2018 certs -> /etc/ssl/certs
drwxr-xr-x 2 root root 4096 Nov 20 06:52 misc
lrwxrwxrwx 1 root root   20 Nov 13 01:58 openssl.cnf -> /etc/ssl/openssl.cnf
lrwxrwxrwx 1 root root   16 Apr 23  2018 private -> /etc/ssl/private
```

### Windows 10  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F555032%2F48bbcadc-af98-9d96-25ec-f3acd8d199de.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=59cd0e74b534f7a7d4df2be7f1ae17de)  

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F555032%2Feacf12b9-39c9-7186-a953-621dd46e1277.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=3a9456f4d81ae7c3ffad6cca1e7b6065)  



[[youtube-dl] python3のSSLエラー(CERTIFICATE_VERIFY_FAILED) Apr 08, 2020](https://qiita.com/tommy19970714/items/96edba36dfde468e26f3)  
```
pip3 install --upgrade certifi
```

```
>>> import certifi
>>> certifi.where()
'/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/certifi/cacert.pem'
```

```
export SSL_CERT_FILE=/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/certifi/cacert.pem
```


## PycURL  
[PycURLでHTTPリクエストあれこれ May 21, 2016](https://qiita.com/TakesxiSximada/items/db015b8d030cefa578a1)  
```

```
[PycURL installation on Python 3.7.0 (Windows 10) Nov 27, 2018](https://stackoverflow.com/questions/53492993/pycurl-installation-on-python-3-7-0-windows-10)  
```
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl
```
```
pip install C:/path/to/downloaded/file/pycurl‑7.43.1‑cp37‑cp37m‑win_amd64.whl
```


# HTTP Signatures  
[HTTP Signatures ](https://developer.moneyou.cloud/http-signatures?fbclid=IwAR2a7HGd9ET0soexdHSw5LC1QnV4nVO2qsJsdHWve7PdCSOBGJ_VoX-pivw)   

## A HTTP Signature consists of the following elements  
```
keyId - This is the serial number of the certificate as defined in 
'TPP-Signing-Certificate' header combined with the distinguished name of the issuer.

    Note: The Berlin Group specification (v.1.3.x) does not specify the format of 
    the distinguished name of the issuer very clearly. We therefore at this moment 
    only validate the serial number part of the keyId.
    
    Example: SN=08d6d2a9d5922000,CA=CN=Moneyou Taiichi Team XCA CA, OU=Secure Digital Certificate Signing, 
    O=Moneyou Taiichi Team, L=Schiphol-Rijk, C=NL

algorithm - Either rsa-sha256 of rsa-sha512 (dependent on the used certificate).

headers - list of header fields to sign
    Headers that must always be present:
        Digest
        X-Request-ID
    Headers that must be present if they are part of the request to be signed:
        PSU-ID
        PSU-Corporate-ID
        TPP-Redirect-URI

signature string - is a signed text (signed by TPP private key) of the above headers fields.
```


# Python TW  
```
Chris Lin 分享了 1 條連結。
2小時

昨天在弄HTTP Signatures的Digest時卡關，所以爬到以下文章，試著做出一樣結果來練手，卻怎樣也做不出來，想向各位前輩請益一下：

https://developer.moneyou.cloud/http-signatures

目標：digest = Base64(SHA256( JSON Body)

思路：

Step1. 把JSON Body以dict 打好後，用JSON dumps轉成JSON字串 (名為json_data)

Step2.寫一行Sha256押碼後轉base64eencode字串輸出：

digest=base64.b64encode(sha256(json_data.encode('utf-8')).digest())

文章結果是：TGGHcPGLechhcNo4gndoKUvCBhWaQOPgtoVDIpxc6J4=

但我做出的是：

lO1rtY6JGM81aJzXeItb48GqYcsOrjJtvkvTaZUoRn8=

在想是不是JSON Body沒處理好，還是漏了哪部分？

------

from hashlib import sha256

import base64
import json

data={"instructedAmount": {"currency": "EUR", "amount": "123.50"}, "debtorAccount": {"iban": "DE40100100103307118608"}, "creditorName": "Merchant123", "creditorAccount": {"iban": "DE02100100109307118603"}, "remittanceInformationUnstructured": "Ref Number Merchant"}

json_data=json.dumps(data)

digest=base64.b64encode(sha256(json_data.encode('utf-8')).digest())

print(digest.decode('utf-8'))
```

![alt tag](https://scontent.ftpe7-2.fna.fbcdn.net/v/t1.0-9/87654150_4143189469040580_2142469084703358976_o.jpg?_nc_cat=109&_nc_sid=1480c5&_nc_ohc=2X8rVHXd6cwAX95jqOk&_nc_ht=scontent.ftpe7-2.fna&oh=01ce50f6bfce5edc3a19cd3283d272c6&oe=5EFFAF30)  


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
