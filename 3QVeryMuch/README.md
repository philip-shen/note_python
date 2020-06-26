Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Pandas—01  [Python] Pandas 基礎教學](#pandas01--python-pandas-基礎教學)
   * [Pandas—02  Python 資料處理筆記 - 使用Panda進行數據處理](#pandas02--python-資料處理筆記---使用panda進行數據處理)
      * [資料操作](#資料操作)
   * [Pandas—03  How to get column by number in Pandas?](#pandas03--how-to-get-column-by-number-in-pandas)
   * [Pandas—04  How to select multiple columns in a pandas dataframe](#pandas04--how-to-select-multiple-columns-in-a-pandas-dataframe)
   * [Pandas—05  How to Convert Pandas DataFrame into a List](#pandas05--how-to-convert-pandas-dataframe-into-a-list)
   * [Pandas—06  Pandas DataFrame column to list](#pandas06--pandas-dataframe-column-to-list)
   * [Display number with leading zeros](#display-number-with-leading-zeros)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose

# Pandas—01  [Python] Pandas 基礎教學  
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


# Pandas—02  Python 資料處理筆記 - 使用Panda進行數據處理  
[Python 資料處理筆記 - 使用Panda進行數據處理 Nov 22, 2018](https://medium.com/@yanweiliu/python-pandas%E4%BD%BF%E7%94%A8%E7%AD%86%E8%A8%98-a4682e254d90)  

## 資料操作  
```
基本操作
df.head(10)  #顯示出前10筆資料，預設值為5筆資料
df.tail(10)  #顯示倒數10筆資料
df.shape()   #顯示出資料共有(X行,Y列)
len(df)      #顯示資料總筆數
df.dtypes    #顯示資料類型
df.select_dtypes("string") #選取字串類型的資料(新功能)
df.describe()#顯示統計數字(最大、最小、平均......等)
df[['AQI']]  #顯示Columns(列)為AQI的數據
df.AQI       #顯示Columns(列)為AQI的數據
df.rename(columns={'舊欄位名稱': '新欄位名稱'}) #修改欄位名稱
df.columns                        #顯示有哪些欄位
df.columns = ['XXX','XXX', 'XXX'] #新增欄位
df.T         #行與列互換，等同於df.transpose()
             #例如df.describe().transpose()
df.info()    #顯示資料的狀態與資訊
df.info(memory_usage='deep') #顯示記憶體使用狀況
df.query('A < 0.5 and B < 0.5')      #查詢A<0.5且B<0.5的資料
df.corr()['PM25'].sort_values()      #顯示PM2.5與其他欄位間的相關係數
df.get_dummies      #One-hot編碼
df.AQI.values       #將資料轉成numpy的array
df.Danger.unique()  #找出唯一值
df.duplicated()     #顯示重複的資料
df.drop_duplicates()#刪除重複的資料
df.drop_duplicates(['Name']) #刪除Name欄位重複的資料

df.value_counts()  #查看有哪些不同的值，並計算每個值有多少個重複值
```

```
groupby方法
dfTotal=df.groupby(['AQI','PM25']).sum() 
#合併種類的名稱，並且顯示該名稱欄位的所有數量總合
dfTotal.sum()                        
#加總所有欄位成一數字
-------------------------------------------------------------------
df_Danger_PM25=df[df.PM25>35.5].groupby("Danger_Air")
#合併所有PM2.5數值>35.5以上的資料成一個新欄位「Danger_Air」df_Danger_PM25["AQI"].sum()
#查詢Danger_Air中，所有的AQI值總合
```

```
iloc,loc,ix方法
df.iloc[4]   #顯示第4筆資料的所有數據 
df1 = df.set_index(['測站'])       #將測站設定為索引(即擺到第一行第一列)
df1 = df1.reset_index(['測站'])    #恢復原本設置
df1.loc['左營']                    #列出所有左營的數據
df.loc[df['name'] == 'Jason']     #列出Name為Jason的資料
```

```
找極端的排序
(例如:前n個大的值或n個最小的值，實際一點的例子像是查詢班上的前三名是誰)
df.nlargest(3,'HEIGHT')    #查詢HEIGHT欄位中數值前3大的
df.nsmallest(3,'WEIGHT')   #查詢WEIGHT欄位中數值前3小的
```

```
刪除資料
df.drop(labels=['SO2','CO'],axis='columns') #刪除SO2和CO這兩個欄位
df.drop(labels=['SO2','CO'],axis='columns',inplace=True)
df=df.drop_duplicates()                     #刪除重複的資料
df.drop(df.index[-1])                       #刪除最後一筆資料axis=0和asxis='row'一樣
axis=1和axis='columns'一樣
使用inplace=True才會把原本的資料改變
```

```
處理Nan資料
df.isnull()                          #判斷是否有遺失值
df.isnull().any()                    #迅速查看是否有遺失值(大筆數資料)
df.isnull().sum()                    #查看每個欄位有幾個缺失值
df.dropna()                          #刪除NaN的資料
df=df.dropna()                       #將刪除後的資料存到變數
df.dropna(axis=1)                    #删除所有包含空值的列
df.dropna(axis=0)                    #删除所有包含空值的行
df.dropna(how='all')                 #只刪除全部欄位都是NaN的列
df.dropna(thresh=4)                  #刪除小於4項缺失值的行
df.dropna(subset=['PM25'])           #只刪除PM25欄位中的缺失值df=df.fillna(0)                      #把NaN資料替換成0 
df=df.fillna(method='pad')           #填入前一筆資料的數值
df=df.fillna(method='bfill')         #填入下一筆資料的數值
df['PM25']=df['PM25'].fillna((df['PM25'].mode())) #填入眾數
df['PM25'] = df['PM25'].interpolate()#使用插值法填入數字(用函數方式)

df['PM25'].fillna(value=df['PM25'].mean()) #把NaN值改成該屬性的所有平均值
```

```
Sort排序
df.sort_index(ascending=True).head(100)         #升階排序
df.sort_index(ascending=False).head(100)        #降階排序
```

```
#指定欄位進行由小到大的排序
dfSort=df.sort_values(by='物種中文名',ascending=False).head(100) 
```

```
#指定多個欄位進行由小到大的排序
dfSort=df.sort_values(by=['名稱1', '名稱2'], ascending=False)
```

```
備註
基本上df[['AQI']]和df.AQI功能一樣

loc:以行列標題選擇資料(隻對字串類型有用)
ix擁有iloc與loc的功能
iloc:以第幾筆來選擇資料(隻對數值類型有用)
```

# Pandas—03  How to get column by number in Pandas?  
[How to get column by number in Pandas? - Stack Overflow May 32, 2017](https://stackoverflow.com/questions/17193850/how-to-get-column-by-number-in-pandas)  

One is a column (aka Series), while the other is a DataFrame:  
```
In [1]: df = pd.DataFrame([[1,2], [3,4]], columns=['a', 'b'])

In [2]: df
Out[2]:
   a  b
0  1  2
1  3  4
```

The column 'b' (aka Series):
```
In [3]: df['b']
Out[3]:
0    2
1    4
Name: b, dtype: int64
```

The subdataframe with columns (position) in [1]:

```
In [4]: df[[1]]
Out[4]:
   b
0  2
1  4
```

Note: it's preferable (and less ambiguous) to specify whether you're talking about the column name e.g. ['b'] or the integer location, since sometimes you can have columns named as integers:

```
In [5]: df.iloc[:, [1]]
Out[5]:
   b
0  2
1  4

In [6]: df.loc[:, ['b']]
Out[6]:
   b
0  2
1  4

In [7]: df.loc[:, 'b']
Out[7]:
0    2
1    4
Name: b, dtype: int64
```


# Pandas—04  How to select multiple columns in a pandas dataframe  
[How to select multiple columns in a pandas dataframe](https://www.geeksforgeeks.org/how-to-select-multiple-columns-in-a-pandas-dataframe/)  
```
# Import pandas package 
import pandas as pd 
  
# Define a dictionary containing employee data 
data = {'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'], 
        'Age':[27, 24, 22, 32], 
        'Address':['Delhi', 'Kanpur', 'Allahabad', 'Kannauj'], 
        'Qualification':['Msc', 'MA', 'MCA', 'Phd']} 
  
# Convert the dictionary into DataFrame  
df = pd.DataFrame(data) 
  
# iloc[row slicing, column slicing] 
df.iloc [0:2, 1:3] 
```
![alt tag](https://media.geeksforgeeks.org/wp-content/uploads/df_col7.png)  


# Pandas—05  How to Convert Pandas DataFrame into a List  
[How to Convert Pandas DataFrame into a List January 6, 2020](https://datatofish.com/convert-pandas-dataframe-to-list/)  
```
from pandas import DataFrame

products = {'Product': ['Tablet','iPhone','Laptop','Monitor'],
            'Price': [250,800,1200,300]
            }

df = DataFrame(products, columns= ['Product', 'Price'])

products_list = df.values.tolist()
print (products_list)
```
![alt tag](https://datatofish.com/wp-content/uploads/2018/09/0002_tolist.png)

```
from pandas import DataFrame

products = {'Product': ['Tablet','iPhone','Laptop','Monitor'],
            'Price': [250,800,1200,300]
            }

df = DataFrame(products, columns= ['Product', 'Price'])

products_list = [df.columns.values.tolist()] + df.values.tolist()
print (products_list)
```
![alt tag](https://datatofish.com/wp-content/uploads/2018/09/0003_tolist.png)


# Pandas—06  Pandas DataFrame column to list  
[Pandas DataFrame column to list [duplicate] May 20, 2019](https://stackoverflow.com/questions/23748995/pandas-dataframe-column-to-list)  



[Deleting rows with Python in a CSV file](https://stackoverflow.com/questions/29725932/deleting-rows-with-python-in-a-csv-file)

[csv.Error: iterator should return strings, not bytes](https://stackoverflow.com/questions/8515053/csv-error-iterator-should-return-strings-not-bytes)

[TypeError: a bytes-like object is required, not 'str' in python and CSV](https://stackoverflow.com/questions/34283178/typeerror-a-bytes-like-object-is-required-not-str-in-python-and-csv)

[How to convert list to string - Stack Overflow](https://stackoverflow.com/questions/5618878/how-to-convert-list-to-string)  

```
list1 = ['1', '2', '3']
str1 = ''.join(list1)

Or if the list is of integers, convert the elements before joining them.

list1 = [1, 2, 3]
str1 = ''.join(str(e) for e in list1)
```

[CSV in Python adding an extra carriage return, on Windows](https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows)  

```
Python 3:

    As described by YiboYang, set newline=''

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    

    As noted in the comments by CoDEmanX, set newline='\n'

with open('output.csv', 'w', newline='\n', encoding='utf-8') as f:
    writer = csv.writer(f)
```


     

[rstrip not removing newline char what am I doing wrong? [duplicate] Jan 23 '10](https://stackoverflow.com/questions/2121839/rstrip-not-removing-newline-char-what-am-i-doing-wrong)  
```
The clue is in the signature of rstrip.

It returns a copy of the string, but with the desired characters stripped, thus you'll need to assign line the new value:

line = line.rstrip('\n')

This allows for the sometimes very handy chaining of operations:

"a string".strip().upper()
```

# Display number with leading zeros   
[Display number with leading zeros](https://stackoverflow.com/questions/134934/display-number-with-leading-zeros/33860138)  
```
print "%02d" % (1,)

print("{:02d}".format(1))
```

[How to add element in Python to the end of list using list.insert?](https://stackoverflow.com/questions/30212447/how-to-add-element-in-python-to-the-end-of-list-using-list-insert)  
```
a=[1,2,3,4]
a.insert(len(a),5)
a

[1, 2, 3, 4, 5]
```


# Troubleshooting


# Reference
[12_Pandas.DataFrame删除指定行和列（drop） 发表时间：2020-04-28](https://www.pythonf.cn/read/98780)  
'''
                    df_noindex = pd.read_csv('./data/12/sample_pandas_normal.csv')
                    print(df_noindex)
                    #       name  age state  point
                    # 0    Alice   24    NY     64
                    # 1      Bob   42    CA     92
                    # 2  Charlie   18    CA     70
                    # 3     Dave   68    TX     70
                    # 4    Ellen   24    CA     88
                    # 5    Frank   30    NY     57

                    print(df_noindex.index)
                    # RangeIndex(start=0, stop=6, step=1)

                    如果是序列号，则无论原样指定数字值还是使用index属性，结果都将相同。

                    print(df_noindex.drop([1, 3, 5]))
                    #       name  age state  point
                    # 0    Alice   24    NY     64
                    # 2  Charlie   18    CA     70
                    # 4    Ellen   24    CA     88

                    print(df_noindex.drop(df_noindex.index[[1, 3, 5]]))
                    #       name  age state  point
                    # 0    Alice   24    NY     64
                    # 2  Charlie   18    CA     70
                    # 4    Ellen   24    CA     88
'''

![alt tag](https://i.imgur.com/7trpv4N.png)  

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


