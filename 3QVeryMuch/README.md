Table of Contents  
=================


# Purpose

# Pandas—01
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


# Pandas—02
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
df.value_counts()  #查看有哪些不同的值，並計算每個值有多少個重複值groupby方法
dfTotal=df.groupby(['AQI','PM25']).sum() 
#合併種類的名稱，並且顯示該名稱欄位的所有數量總合
dfTotal.sum()                        
#加總所有欄位成一數字
-------------------------------------------------------------------
df_Danger_PM25=df[df.PM25>35.5].groupby("Danger_Air")
#合併所有PM2.5數值>35.5以上的資料成一個新欄位「Danger_Air」df_Danger_PM25["AQI"].sum()
#查詢Danger_Air中，所有的AQI值總合iloc,loc,ix方法
df.iloc[4]   #顯示第4筆資料的所有數據 
df1 = df.set_index(['測站'])       #將測站設定為索引(即擺到第一行第一列)
df1 = df1.reset_index(['測站'])    #恢復原本設置
df1.loc['左營']                    #列出所有左營的數據
df.loc[df['name'] == 'Jason']     #列出Name為Jason的資料找極端的排序
(例如:前n個大的值或n個最小的值，實際一點的例子像是查詢班上的前三名是誰)
df.nlargest(3,'HEIGHT')    #查詢HEIGHT欄位中數值前3大的
df.nsmallest(3,'WEIGHT')   #查詢WEIGHT欄位中數值前3小的刪除資料
df.drop(labels=['SO2','CO'],axis='columns') #刪除SO2和CO這兩個欄位
df.drop(labels=['SO2','CO'],axis='columns',inplace=True)
df=df.drop_duplicates()                     #刪除重複的資料
df.drop(df.index[-1])                       #刪除最後一筆資料axis=0和asxis='row'一樣
axis=1和axis='columns'一樣
使用inplace=True才會把原本的資料改變處理Nan資料
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
df['PM25'] = df['PM25'].interpolate()#使用插值法填入數字(用函數方式)df['PM25'].fillna(value=df['PM25'].mean()) #把NaN值改成該屬性的所有平均值Sort排序
df.sort_index(ascending=True).head(100)         #升階排序
df.sort_index(ascending=False).head(100)        #降階排序#指定欄位進行由小到大的排序
dfSort=df.sort_values(by='物種中文名',ascending=False).head(100) #指定多個欄位進行由小到大的排序
dfSort=df.sort_values(by=['名稱1', '名稱2'], ascending=False)備註
基本上df[['AQI']]和df.AQI功能一樣

loc:以行列標題選擇資料(隻對字串類型有用)
ix擁有iloc與loc的功能
iloc:以第幾筆來選擇資料(隻對數值類型有用)
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
