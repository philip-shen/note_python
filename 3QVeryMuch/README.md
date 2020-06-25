Table of Contents  
=================


# Purpose

[[Python] Pandas 基礎教學 01 October 2017](https://oranwind.org/python-pandas-ji-chu-jiao-xue/)
```
# Pandas 透過使用中括號 [] 與 .iloc 可以很靈活地從 data frame 中選擇想要的元素
# Python 在指定 0:1 時不包含 1，在指定 0:2 時不包含 2

import pandas as pd

groups = ["Movies", "Sports", "Coding", "Fishing", "Dancing", "cooking"]  
num = [46, 8, 12, 12, 6, 58]

dict = {"groups": groups,  
        "num": num
       }

select_df = pd.DataFrame(dict)

print(select_df.iloc[0, 1]) # 第一列第二欄：組的人數  
print("---")  
print(select_df.iloc[0:1,:]) # 第一列：組的組名與人數  
print("---")  
print(select_df.iloc[:,1]) # 第二欄：各組的人數  
print("---")  
print(select_df["num"]) # 各組的人數  
print("---")  
print(select_df.num) # 各組的人數  
```


# Troubleshooting


# Reference
[12_Pandas.DataFrame删除指定行和列（drop） 发表时间：2020-04-28](https://www.pythonf.cn/read/98780)  


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
