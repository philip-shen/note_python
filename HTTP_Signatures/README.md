# Purpose  
Take note of HTTP Signatures  

# Table of Contents  
[HTTP Signatures](#http-signatures)  
[]()  
[]()  


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
