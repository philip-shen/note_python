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
   * [Pandas—07  Deleting rows with Python in a CSV file](#pandas07--deleting-rows-with-python-in-a-csv-file)
   * [Pandas—08  Python: Number of rows affected by cursor.execute("SELECT …)](#pandas08--python-number-of-rows-affected-by-cursorexecuteselect-)
   * [Pandas—09  Export Pandas Table to Excel](#pandas09--export-pandas-table-to-excel)
      * [Library Installation](#library-installation)
      * [書き込む表データ](#書き込む表データ)
      * [ファイル名を指定して出力](#ファイル名を指定して出力)
      * [ヘッダーを表示しない](#ヘッダーを表示しない)
      * [インデックス（行名）を表示しない](#インデックス行名を表示しない)
      * [ヘッダーおよびインデックスを表示しない](#ヘッダーおよびインデックスを表示しない)
      * [上部に空白行を入れる](#上部に空白行を入れる)
      * [左に空白列を入れる](#左に空白列を入れる)
      * [小数点の最大表示桁数を指定](#小数点の最大表示桁数を指定)
      * [No such file or directory](#no-such-file-or-directory)
      * [Unicode error](#unicode-error)
   * [Pandas—10  Panda Execute SQL](#pandas10--panda-execute-sql)
   * [Display number with leading zeros](#display-number-with-leading-zeros)
   * [SQL—01  SQL count rows in a table](#sql01--sql-count-rows-in-a-table)
   * [SQL—02  INSERT IF NOT EXISTS ELSE UPDATE?](#sql02--insert-if-not-exists-else-update)
   * [SQL—03](#sql03)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of 3Quest  


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


# Pandas—07  Deleting rows with Python in a CSV file    
[Deleting rows with Python in a CSV file](https://stackoverflow.com/questions/29725932/deleting-rows-with-python-in-a-csv-file)

# Pandas—08  Python: Number of rows affected by cursor.execute("SELECT …)  
[Python: Number of rows affected by cursor.execute("SELECT …)](https://stackoverflow.com/questions/2511679/python-number-of-rows-affected-by-cursor-executeselect)
```
cursor.execute("SELECT COUNT(*) from result where server_state='2' AND name LIKE '"+digest+"_"+charset+"_%'")
result=cursor.fetchone()

number_of_rows=result[0]
```

```
cursor.execute("SELECT COUNT(*) from result where server_state='2' AND name LIKE '"+digest+"_"+charset+"_%'")
(number_of_rows,)=cursor.fetchone()
```


# Pandas—09  Export Pandas Table to Excel    
[【python】pandasの表をエクセルファイルに出力する方法 posted at 2020-06-16](https://qiita.com/yuta-38/items/cbe1981a3f71e1ccc6b9)  

## Library Installation  
```
pip install -U openpyxl
pip install -U xlwt
pip install -U pandas
```
> ①openpyxl：xlsx / xlsm / xltx / xltmファイルを読み書きするためのPythonライブラリ  
> ②xlwt：古いExcelファイル（.xlsなど）にデータとフォーマット情報を書き込むためのライブラリ(Excel2003以前)  
> ③pythonでデータ分析を行うためのライブラリ。表データの扱いで使用。  

## 書き込む表データ  
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F563526%2F254b4458-6d97-485e-020d-f7e9ca090152.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=b437ffc5262b9fe81b48cf2bfdffc4d8)  


## ファイル名を指定して出力  
```
df.to_excel('ファイルパス')
　└「df」：出力する表データ
　└「ファイルパス」：ファイル名も記載
```

```
import pandas as pd
df.to_excel('~/desktop/output.xlsx')
```

![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F563526%2F89758dd5-8bbd-3785-088e-76b542ed3d17.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=6bd6fb979b23039f7497e1b3d0cf4f6d)  

## ヘッダーを表示しない  
```
import pandas as pd
df.to_excel('~/desktop/output.xlsx', header=None)
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F563526%2F93727159-4dd4-8e32-5b91-d99be2687049.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=597be84bbe76a33a3152d9971f35eef3)  

## インデックス（行名）を表示しない  
```
import pandas as pd
df.to_excel('~/desktop/output.xlsx', index=None)
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F563526%2F1001e369-dd1c-6803-79c6-f8bd21c9eb9e.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=4507d508594d9ac7c039329a361bded0)  

## ヘッダーおよびインデックスを表示しない  
```
import pandas as pd
df.to_excel('~/desktop/output.xlsx', index=False, header=False)
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F563526%2F39ec13d7-c99d-cfae-526d-37affd64be3b.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=3c49efad520d71c68a88720db6c95bd5)  

## 上部に空白行を入れる  
```
オプションにstartrow=nを記述。
　└「n」:空ける行数
```

```
import pandas as pd
df.to_excel('~/desktop/output.xlsx', startrow=3)
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F563526%2F8e5c658a-a63b-d1b8-19d7-8f6d88e45d9a.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=980254f4ebb2961fabc007d114a745cf)  

## 左に空白列を入れる  
```
オプションにstartcol=nを記述。
　└「n」:空ける列数
```

```
import pandas as pd
df.to_excel('~/desktop/output.xlsx', startcol=2)
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F563526%2F7c62640f-cbed-e250-ea26-311383bb391f.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=834cc45929d8fd411054d27c5878b67b)  

## 小数点の最大表示桁数を指定  
```
オプションにfloat_format='%.nf'を記述。
　└「n」:表示する桁数
```

```
import pandas as pd
df.to_excel('~/desktop/output.xlsx', float_format='%.2f')
```
![alt tag](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F563526%2F9803707b-91c7-2b48-dd75-2a79d73a4855.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=b683ddfcf07cab684c2ca219c249961e)  

> n=2なら、3桁目を四捨五入し、小数点第2桁まで表示。  

## No such file or directory  
[【備忘録】unicode errorとNo such file or directoryの対処法（pandasで表をexcelファイルに出力） posted at 2020-04-04](https://qiita.com/yuta-38/items/f0d75a5585169c98da4a#no-such-file-or-directory)   
```
df2 = df.copy()
with pd.ExcelWriter('~/Desktop/GA-demo.xlsx') as writer:  
    df.to_excel(writer, sheet_name='AAA')
    df2.to_excel(writer, sheet_name='BBB')
```
```
エラー

FileNotFoundError: [Errno 2] No such file or directory: '~/Desktop/GA-demo.xlsx'
```

```
df2 = df.copy()
with pd.ExcelWriter('~\\Desktop\\GA-demo.xlsx') as writer:  
    df.to_excel(writer, sheet_name='AAA')
    df2.to_excel(writer, sheet_name='BBB')
```
```
エラー

FileNotFoundError: [Errno 2] No such file or directory: '~/Desktop/GA-demo.xlsx'
```

```
OK

df2 = df.copy()
with pd.ExcelWriter('C:/Users/name/Desktop/GA-demo3.xlsx') as writer:  
    df.to_excel(writer, sheet_name='AAA')
    df2.to_excel(writer, sheet_name='BBB')
```

## Unicode error
[【備忘録】unicode errorとNo such file or directoryの対処法（pandasで表をexcelファイルに出力） posted at 2020-04-04](https://qiita.com/yuta-38/items/f0d75a5585169c98da4a#no-such-file-or-directory)   
```
df2 = df.copy()
with pd.ExcelWriter('C:\Users\name\Desktop\GA-demo.xlsx') as writer:  
    df.to_excel(writer, sheet_name='AAA')
    df2.to_excel(writer, sheet_name='BBB')
```
```
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape
```
*バックスラッシュ「\」はエスケープのため。文字として認識させる場合は「\」とする必要がある。*

```
OK！

df2 = df.copy()
with pd.ExcelWriter('C:\\Users\\name\\Desktop\\GA-demo2.xlsx') as writer:  
    df.to_excel(writer, sheet_name='AAA')
    df2.to_excel(writer, sheet_name='BBB')
```

> 記述は下記どちらでもOK。
```
「C:\Users\name\」
「C://Users//name//」
```

# Pandas—10  Panda Execute SQL    
[SQLクエリの結果をPANDASデータ構造に変換する方法は？](https://www.it-swarm.dev/ja/python/sql%E3%82%AF%E3%82%A8%E3%83%AA%E3%81%AE%E7%B5%90%E6%9E%9C%E3%82%92pandas%E3%83%87%E3%83%BC%E3%82%BF%E6%A7%8B%E9%80%A0%E3%81%AB%E5%A4%89%E6%8F%9B%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95%E3%81%AF%EF%BC%9F/1067685717/)  


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

# SQL—01  SQL count rows in a table    
[SQL count rows in a table Mar 8, 2015](https://stackoverflow.com/questions/28916917/sql-count-rows-in-a-table)  
```
 SELECT COUNT(*) FROM TableName
```

# SQL—02  INSERT IF NOT EXISTS ELSE UPDATE?   
[INSERT IF NOT EXISTS ELSE UPDATE? Nov 13, 2014](https://stackoverflow.com/questions/3634984/insert-if-not-exists-else-update)  
[sqlite3 INSERT IF NOT EXIST (with Python) Sep 30, 2016](https://stackoverflow.com/questions/39793327/sqlite3-insert-if-not-exist-with-python)  
```
self.cur.execute('SELECT * FROM ProSolut WHERE (Col1=? AND Col2=? AND Col3=?)', ('a', 'b', 'c'))
entry = self.cur.fetchone()

if entry is None:
    self.cur.execute('INSERT INTO ProSolut (Col1, Col2, Col3) VALUES (?,?,?)', ('a', 'b', 'c'))
    print 'New entry added'
else:
    print 'Entry found'
```

[“Insert if not exists” statement in SQLite ](https://stackoverflow.com/questions/19337029/insert-if-not-exists-statement-in-sqlite)
```
INSERT INTO memos(id,text) 
SELECT 5, 'text to insert' 
WHERE NOT EXISTS(SELECT 1 FROM memos WHERE id = 5 AND text = 'text to insert');
```


# SQL—03   
```
SELECT DISTINCT noise.name,noise.description as noise, tb_nobgn.SMOS , tb_nobgn.NMOS , tb_nobgn.GMOS , tb_nobgn.delta_SNR, tb_nobgn.dut_foldername, tb_nobgn.insert_date, tb_nobgn.insert_time
FROM _3Quest_nobgn tb_nobgn 
INNER JOIN noise_type noise ON noise.name = tb_nobgn.noise
WHERE tb_nobgn.dut_foldername='boommic_SWout' and tb_nobgn.insert_date='20200627' and tb_nobgn.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_pub.SMOS , tb_pub.NMOS , tb_pub.GMOS , tb_pub.delta_SNR, tb_pub.dut_foldername, tb_pub.insert_date, tb_pub.insert_time
FROM _3Quest_pub tb_pub 
INNER JOIN noise_type noise ON noise.name = tb_pub.noise
WHERE tb_pub.dut_foldername='boommic_SWout' and tb_pub.insert_date='20200627' and tb_pub.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_road.SMOS , tb_road.NMOS , tb_road.GMOS , tb_road.delta_SNR, tb_road.dut_foldername, tb_road.insert_date, tb_road.insert_time
FROM _3Quest_road tb_road 
INNER JOIN noise_type noise ON noise.name = tb_road.noise
WHERE tb_road.dut_foldername='boommic_SWout' and tb_road.insert_date='20200627' and tb_road.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_crossroad.SMOS , tb_crossroad.NMOS , tb_crossroad.GMOS , tb_crossroad.delta_SNR, tb_crossroad.dut_foldername, tb_crossroad.insert_date, tb_crossroad.insert_time
FROM _3Quest_crossroad tb_crossroad 
INNER JOIN noise_type noise ON noise.name = tb_crossroad.noise
WHERE tb_crossroad.dut_foldername='boommic_SWout' and tb_crossroad.insert_date='20200627' and tb_crossroad.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_nobgn.SMOS , tb_nobgn.NMOS , tb_nobgn.GMOS , tb_nobgn.delta_SNR, tb_nobgn.dut_foldername, tb_nobgn.insert_date, tb_nobgn.insert_time
FROM _3Quest_nobgn tb_nobgn 
INNER JOIN noise_type noise ON noise.name = tb_nobgn.noise
WHERE tb_nobgn.dut_foldername='boommic_SWout' and tb_nobgn.insert_date='20200627' and tb_nobgn.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_train.SMOS , tb_train.NMOS , tb_train.GMOS , tb_train.delta_SNR, tb_train.dut_foldername, tb_train.insert_date, tb_train.insert_time
FROM _3Quest_train tb_train 
INNER JOIN noise_type noise ON noise.name = tb_train.noise
WHERE tb_train.dut_foldername='boommic_SWout' and tb_train.insert_date='20200627' and tb_train.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_car.SMOS , tb_car.NMOS , tb_car.GMOS , tb_car.delta_SNR, tb_car.dut_foldername, tb_car.insert_date, tb_car.insert_time
FROM _3Quest_car tb_car 
INNER JOIN noise_type noise ON noise.name = tb_car.noise
WHERE tb_car.dut_foldername='boommic_SWout' and tb_car.insert_date='20200627' and tb_car.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_cafeteria.SMOS , tb_cafeteria.NMOS , tb_cafeteria.GMOS , tb_cafeteria.delta_SNR, tb_cafeteria.dut_foldername, tb_cafeteria.insert_date, tb_cafeteria.insert_time
FROM _3Quest_cafeteria tb_cafeteria 
INNER JOIN noise_type noise ON noise.name = tb_cafeteria.noise
WHERE tb_cafeteria.dut_foldername='boommic_SWout' and tb_cafeteria.insert_date='20200627' and tb_cafeteria.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_mensa.SMOS , tb_mensa.NMOS , tb_mensa.GMOS , tb_mensa.delta_SNR, tb_mensa.dut_foldername, tb_mensa.insert_date, tb_mensa.insert_time
FROM _3Quest_mensa tb_mensa 
INNER JOIN noise_type noise ON noise.name = tb_mensa.noise
WHERE tb_mensa.dut_foldername='boommic_SWout' and tb_mensa.insert_date='20200627' and tb_mensa.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_callcenter.SMOS , tb_callcenter.NMOS , tb_callcenter.GMOS , tb_callcenter.delta_SNR, tb_callcenter.dut_foldername, tb_callcenter.insert_date, tb_callcenter.insert_time
FROM _3Quest_callcenter tb_callcenter 
INNER JOIN noise_type noise ON noise.name = tb_callcenter.noise
WHERE tb_callcenter.dut_foldername='boommic_SWout' and tb_callcenter.insert_date='20200627' and tb_callcenter.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_voice_distractor.SMOS , tb_voice_distractor.NMOS , tb_voice_distractor.GMOS , tb_voice_distractor.delta_SNR, tb_voice_distractor.dut_foldername, tb_voice_distractor.insert_date, tb_voice_distractor.insert_time
FROM _3Quest_voice_distractor tb_voice_distractor 
INNER JOIN noise_type noise ON noise.name = tb_voice_distractor.noise
WHERE tb_voice_distractor.dut_foldername='boommic_SWout' and tb_voice_distractor.insert_date='20200627' and tb_voice_distractor.insert_time='22:41:39'
UNION
SELECT DISTINCT noise.name,noise.description as noise, tb_AVG.SMOS , tb_AVG.NMOS , tb_AVG.GMOS , tb_AVG.delta_SNR, tb_AVG.dut_foldername, tb_AVG.insert_date, tb_AVG.insert_time
FROM _3Quest_AVG tb_AVG 
INNER JOIN noise_type noise ON noise.name = tb_AVG.noise
WHERE tb_AVG.dut_foldername='boommic_SWout' and tb_AVG.insert_date='20200627' and tb_AVG.insert_time='22:41:39'
```
![alt tag](https://i.imgur.com/Q5UC5uX.png)  


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


