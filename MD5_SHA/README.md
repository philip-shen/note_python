Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [MD5 and SHA](#md5-and-sha)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of MD5 and SHA  stuffs

# MD5 and SHA  
[Python 計算MD5 與SHA 雜湊教學與範例 Jan 23, 2018](https://blog.gtwang.org/programming/python-md5-sha-hash-functions-tutorial-examples/)  
```
#!/usr/bin/python3
import hashlib
m = hashlib.md5()
data = "G. T. Wang"

# 先將資料編碼，再更新 MD5 雜湊值
m.update(data.encode("utf-8"))

h = m.hexdigest()
print(h)
```

```
#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib

filename = "my_data.txt"
m = hashlib.md5()

with open(filename, "rb") as f:
  # 分批讀取檔案內容，計算 MD5 雜湊值
  for chunk in iter(lambda: f.read(4096), b""):
    m.update(chunk)

h = m.hexdigest()
print(h)
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


