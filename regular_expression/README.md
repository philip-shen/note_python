
# Purpose  
Take some note of regular expression  

# Regular Expression
[給自己的Python小筆記 — 強大的數據處理工具 — 正則表達式 — Regular Expression — regex詳細教學 Nov 24, 2020](https://chwang12341.medium.com/%E7%B5%A6%E8%87%AA%E5%B7%B1%E7%9A%84python%E5%B0%8F%E7%AD%86%E8%A8%98-%E5%BC%B7%E5%A4%A7%E7%9A%84%E6%95%B8%E6%93%9A%E8%99%95%E7%90%86%E5%B7%A5%E5%85%B7-%E6%AD%A3%E5%89%87%E8%A1%A8%E9%81%94%E5%BC%8F-regular-expression-regex%E8%A9%B3%E7%B4%B0%E6%95%99%E5%AD%B8-a5d20341a0b2)

## 基本的匹配  
<img src="https://miro.medium.com/max/875/0*8qxOmuKVIEYjDOai.png" width="800" height="200">  

## 補充：常見的[…]匹配規則  
<img src="https://miro.medium.com/max/875/0*6UYboATqsx89mP7l.png" width="800" height="200">  

## 定義好的字符集  
<img src="https://miro.medium.com/max/875/0*U1mo3WMzWnGrkC-V.png" width="800" height="200">  

## 邊界上的匹配  
<img src="https://miro.medium.com/max/875/0*2pSb0Vn58UzUJ9pH.png" width="800" height="200">  

## 數量上的匹配（通常用在其它匹配符之後） 
<img src="https://miro.medium.com/max/875/0*h7NK5aieWOcxwk4b.png" width="800" height="200">  

## 邏輯與分組的概念
<img src="https://miro.medium.com/max/875/0*FVEd2vjdCfOPB04l.png" width="800" height="200">  

## 特殊用法（不是用於分組） 
<img src="https://miro.medium.com/max/875/0*KFP5WVjDsS0yd8gM.png" width="800" height="200">  

## 轉義字符
<img src="https://miro.medium.com/max/875/0*syxO2Kdwo6lUxCSH.png" width="800" height="200">  

## 特殊情況：當需要匹配一些在正則表達式中有特殊意義的字符時，像是\d、\w、\s等，此時就要多加一個””  
<img src="https://miro.medium.com/max/875/0*LK2gb-U1D0RASFyf.png" width="800" height="200">  

## 大部分的正則表達式函數中，都會有一個參數flags，它是用來控制匹配的模式的，裡面有如下表的標誌可以供選擇，如果想一次指定多個標誌，可以使用OR(“|”)，像是re.I | re.S等組合  
<img src="https://miro.medium.com/max/875/0*8i8EASD_Y59TgnMx.png" width="800" height="200">  

## 正則表達式的貪婪與非貪婪模式
<img src="https://miro.medium.com/max/875/0*1Csmw0LQuOFsMtYJ.png" width="800" height="200">  

## 1. match 函數用法  
```
re.match(pattern, string, flags)
```

## 2. Search 函數用法   
```
re.search(pattern, string, flags)
```

## 3. findall 函數用法  
```
findall(pattern, string, pos, endpos)
```

## 4. sub 函數用法  
```
re.sub(pattern, repl, string, count = 0, flags)
```

```
pattern: 匹配的規則，使用正則表達式的語法來撰寫

repl: 欲替換的字符，也可以用函數的形式傳入喔
    
string: 要進行匹配的字符串
    
count: 匹配好字符後，替換的最大數量，預設為0，表示要全部替換
    
flags: 設定一些正則表達式的方式，像是規則是否忽略大小寫、使用UNICODE字符規則來解析字符等，如果沒有特別需求可以忽略不寫 可以選擇的標誌，可以參考我上面有提到的正則表達式修飾符號喔
```

## 5. Compile 函數  
```
re.compile(pattern, flags)
```

## 6. finditer 函數用法  
```
re.finditer(pattern, string, flags)
```

## 7. split 函數用法  
```
re.split(pattern, string, maxsplit, flags)
```

```
pattern: 匹配的規則，使用正則表達式的語法撰寫

string: 欲進行匹配的字符串

maxsplit: 分割的次數，如maxsplit=1，代表分割一次，預設為0，表示不限分割次數

flags: 設定一些匹配的模式
```

* []()  
![alt tag]()
<img src="" width="" height="">  

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
