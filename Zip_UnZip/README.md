# Purpose  
Take note of Zip and UnZip  

# Table of Contents  
[Setup and Usage](#setup-and-usage)  
[01. Install library by pip](#01-install-library-by-pip)  
[02. Go to \Zip_UnZip\test](#02-go-to-zip_unziptest)  
[03. Places zip files in \Zip_UnZip\logzip](#03-places-zip-files-in-zip_unziplogzip)  
[04. Excute python test_unzip.py ..\logzip](#04-excute-python-test_unzip.py-\logzip)  
[05. Check \Zip_UnZip\logs\WiFiPerformance.db by sqlite browser](#05-check-zip_unziplogswifiperformancedb-by-sqlite-browser)  
[06. Query reslut by ugin SQL](#06-query-reslut-by-ugin-sql)  

[SQL Sytnax](#sql-sytnax)  
[SQL COUNT](#sql-count)  

[Delete Redundant Rows by Client and Test_Mode Using INNER JOIN](#delete-redundant-rows-by-client-and-test_mode-using-inner-join)  
[Delete Redundant Rows by 11AC](#delete-redundant-rows-by-11ac)  
[Delete Redundant Rows by 11N](#delete-redundant-rows-by-11n)  
[Select Client1 and 2nd run](#select-client1-and-2nd-run)  
[Select Client1, TX and all runs](#select-client1-tx-and-all-runs)  
[Select Client1, Bidirectional and all runs](#select-client1-bidirectional-and-all-runs)  
[Select Mode, Wireless_Mode](#select-mode-wireless_mode)  
[Select Mode, Wireless_Mode 11AC, Test_Mode, Client, TX](#select-mode-wireless_mode-11ac-test_mode-client-tx)  
[Select Mode, Wireless_Mode 11N, Test_Mode, Client, Bi](#select-mode-wireless_mode-11n-test_mode-client-bi)  
[Regrssion Test, Wireless_Mode 11AC, Both](#regrssion-test-wireless_mode-11ac-both)  
[Regrssion Test, Wireless_Mode 11AC, WAN_Type PPTP, TX](#regrssion-test-wireless_mode-11ac-wan_type-pptp-tx)


[SQL JOIN](#sql-join)  

[Regular Express](#regular-express)

[Troubleshooting](#troubleshooting)  

[Reference](#reference)  

# Setup and Usage  
## 01. Install library by pip  
```
pip install -r requiremnets.txt
```

## 02. Go to \Zip_UnZip\test  

## 03. Places zip files in \Zip_UnZip\logzip  

## 04. Excute python test_unzip.py ..\logzip
```
 python test_unzip.py ..\logzip
```
![alt tag](https://i.imgur.com/TcIZJGX.gif)  

![alt tag](https://i.imgur.com/4nDyXCs.gif)  

## 05. Check \Zip_UnZip\logs\WiFiPerformance.db by sqlite browser  
![alt tag](https://i.imgur.com/DORE80g.jpg)  

## 06. Query reslut by ugin SQL  

# SQL Sytnax  
[SQL語法](https://www.1keydata.com/tw/sql/sql-syntax.html) 
```
在這一頁中，我們列出所有在這個網站有列出 SQL 指令的語法。若要更詳盡的說明，請點選 指令名稱。

這一頁的目的是提供一個簡潔的 SQL 語法做為讀者參考之用。我們建議您現在就按 Control-D 將本 頁加入您的『我的最愛』。
```

## SQL COUNT  
[SQL COUNT](https://www.1keydata.com/tw/sql/sqlcount.html)  

```
SELECT COUNT (Store_Name)
FROM Store_Information
WHERE Store_Name IS NOT NULL;
```

```
COUNT 和 DISTINCT 經常被合起來使用，目的是找出表格中有多少筆不同的資料 (至於這些資料實際上是什麼並不重要)。
舉例來說，如果我們要找出我們的表格中有多少個不同的 Store_Name，我們就鍵入，
```
```
SELECT COUNT (DISTINCT Store_Name)
FROM Store_Information;
```

```
SELECT COUNT (DISTINCT csv_foldername)
FROM Chariot_Log;
```

## [SQL]查詢筆數重複的資料  
[[SQL]查詢筆數重複的資料 Aug 08 Tue 2006](https://wthomasu.pixnet.net/blog/post/38017237)  

```
依stud_no欄位查詢stud_no欄位資料重複的筆數

SELECT stud_no, COUNT(*) AS count
FROM student_data
GROUP BY stud_no
HAVING (COUNT(*) > 1)
```

```
SELECT csv_foldername, model, fw, channel, test_method, test_client, COUNT(*) AS count
FROM Chariot_Log
GROUP BY csv_foldername
HAVING (COUNT(*) > 1)
ORDER BY test_method, test_client;
```

```
SELECT *, COUNT(*) AS count
FROM Chariot_CSV_Throughput
GROUP BY csv_foldername
HAVING (COUNT(*) > 1)
ORDER BY csv_foldername, csv_filename;
```

```
SELECT csv_foldername,csv_filename,throughput_avg,throughput_min,throughput_max, COUNT(*) AS count
FROM Chariot_CSV_Throughput
GROUP BY csv_foldername
HAVING (COUNT(*) > 1)
ORDER BY csv_filename ASC;
```

```
SELECT csv_foldername,csv_filename,throughput_avg
FROM Chariot_CSV_Throughput
ORDER BY csv_foldername ASC;
```

```
SELECT csv_foldername,csv_filename,throughput_avg,throughput_min,throughput_max
FROM Chariot_CSV_Throughput
GROUP BY csv_foldername
ORDER BY csv_filename ASC;
```

## Delete Redundant Rows by Client and Test_Mode Using INNER JOIN 
```
SELECT DISTINCT char_log.test_method, char_log.model, char_log.fw, char_csv.csv_foldername, char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_csv.csv_filename REGEXP  '^Client[0-9]' and  char_log.test_method REGEXP  '^PPTP'
ORDER BY char_csv.csv_foldername ASC;
```

## Delete Redundant Rows by 11AC  
```
SELECT DISTINCT char_log.test_method, char_log.model, char_log.fw, char_log.wireless_mode, char_csv.csv_foldername, char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9]AC' and char_csv.csv_filename REGEXP  '^P[0-9]-Client[0-9]' and  char_log.test_method REGEXP  '^Chamber'
ORDER BY char_csv.csv_foldername ASC
```

## Delete Redundant Rows by 11N  
```
SELECT DISTINCT char_log.test_method, char_log.model, char_log.fw, char_log.wireless_mode, char_csv.csv_foldername, char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9]N' and char_csv.csv_filename REGEXP  '^P[0-9]-Client[0-9]' and  char_log.test_method REGEXP  '^Chamber'
ORDER BY char_csv.csv_foldername ASC
```

### Select Client1 and 2nd run  
```
SELECT DISTINCT char_log.test_method, char_log.model, char_log.fw, char_log.wireless_mode, char_csv.csv_foldername, char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9][A-Z][A-Z]$' and char_csv.csv_filename REGEXP  '^.*Client[^2345]_[^13]*\.csv$' and  char_log.test_method REGEXP  '^Chamber'
ORDER BY char_csv.csv_filename DESC
```

### Select Client1, TX and all runs  
```
SELECT DISTINCT char_log.test_method, char_log.model, char_log.fw, char_log.wireless_mode, char_csv.csv_foldername, char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9][A-Z][A-Z]$' and char_csv.csv_filename REGEXP  '^.*Client[^2345]_Tx_.*_.*\.csv$' and  char_log.test_method REGEXP  '^Chamber'
ORDER BY char_csv.csv_filename ASC
```

### Select Client1, Bidirectional and all runs  
```
SELECT DISTINCT char_log.test_method, char_log.model, char_log.fw, char_log.wireless_mode, char_csv.csv_foldername, char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9][A-Z][A-Z]$' and char_csv.csv_filename REGEXP  '^.*Client[^2345]_Bi.*_.*_.*\.csv$' and  char_log.test_method REGEXP  '^Chamber'
ORDER BY char_csv.csv_filename ASC
```

### Select Mode, Wireless_Mode  
```
SELECT DISTINCT char_log.test_method, char_csv.csv_foldername, char_log.model, char_log.fw, char_log.wireless_mode,  char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9][A-Z][A-Z]$' and  char_log.test_method REGEXP  '^Chamber' and char_log.model REGEXP '^COVR1900'
ORDER BY (char_csv.csv_filename and char_log.model) DESC
```

### Select Mode, Wireless_Mode 11AC, Test_Mode, Client, TX
```
SELECT DISTINCT char_log.test_method, char_log.model, char_csv.csv_foldername,  char_log.fw, char_log.wireless_mode,  char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9][A-Z][A-Za-z]$'  and char_csv.csv_filename REGEXP  '^.*Client[^2345]_Tx_.*_.*\.csv$' and  char_log.test_method REGEXP  '^Chamber' and char_log.model REGEXP '^COVR1900'
ORDER BY char_log.model  ASC
```

![alt tag](https://i.imgur.com/Cpiyb8Y.png)

### Select Mode, Wireless_Mode 11N, Test_Mode, Client, Bi  
```
SELECT DISTINCT char_log.test_method, char_log.model, char_csv.csv_foldername,  char_log.fw, char_log.wireless_mode,  char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9][A-Za-z]$'  and char_csv.csv_filename REGEXP  '^.*Client[^2345]_Bi.*_.*_.*\.csv$' and  char_log.test_method REGEXP  '^Chamber' and char_log.model REGEXP '^COVR1900'
ORDER BY char_log.model  ASC
```

![alt tag](https://i.imgur.com/uBTz9ax.png)

### Regrssion Test, Wireless_Mode 11AC, Both   
```
SELECT DISTINCT char_log.test_method, char_log.model, char_csv.csv_foldername,  char_log.fw, char_log.wireless_mode,  char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9][A-Za-z][A-Za-z]$'  and char_csv.csv_filename REGEXP  '^.*Client[12345]_Bi.*_.*_.*\.csv$' and  char_log.test_method REGEXP  '^Chamber' and char_log.model REGEXP '^DIR-17'
ORDER BY char_csv.csv_filename  ASC
```

![alt tag](https://i.imgur.com/5eLofDU.png)

### Regrssion Test, Wireless_Mode 11AC, WAN_Type PPTP, TX   
```
SELECT DISTINCT char_log.test_method, char_log.model, char_csv.csv_foldername,  char_log.fw, char_log.wireless_mode,  char_csv.csv_filename, char_csv.throughput_avg
FROM Chariot_CSV_Throughput char_csv 
INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
WHERE char_log.wireless_mode REGEXP  '^[0-9][0-9][0-9].[0-9][0-9][A-Za-z][A-Za-z]$'  and char_csv.csv_filename REGEXP  '^Client[12345]-W[0-9]_T.*_.*_.*\.csv$' and  char_log.test_method REGEXP  '^PPTP' and char_log.model REGEXP '^DIR-17'
ORDER BY char_csv.csv_filename  ASC
```

![alt tag](https://i.imgur.com/DUvcecS.png)  


[SQL語法筆記 - Digishot Web Design Source  2013-09-09](https://digishot.keenchief.com/tw/1585550028/1585550028)  


[[SQL] 多個各自count之後還要join成一張表 (在多個表格裡count資料) Sep 16 Fri 2011](https://j796160836.pixnet.net/blog/post/29729775)
```
解答

找好久才找到這個解答

我個人認為其重要性接近死背這個架構

 

SELECT `A_id`, `A_name`,
(SELECT COUNT(*) FROM `tableB` WHERE  `tableB`.`A_id`=`tableA`.`A_id`) AS `B_count`,  
(SELECT COUNT(*) FROM `tableC` WHERE  `tableC`.`A_id`=`tableA`.`A_id`) AS `C_count`,  
FROM `tableA`;

 

這個架構叫做

關聯子查詢

SQL語句裡面跟外面有產生關聯的
但是光看問題不會馬上想到這個架構
```

```
解釋

簡單來說一句SQL語法做了三個動作

 

從刮號裡面先看好了

裡面有二句SQL語法，看起來像是獨立的但不能跑

會有這個錯誤

#1054 - Unknown column 'tableA.A_id' in 'where clause'

因為他找不到tableA在哪裡

 

 

SELECT COUNT(*) FROM `tableB` WHERE  `tableB`.`A_id`=`tableA`.`A_id`

這句的意思是計算tableB總共有幾筆

我們有學到在WHERE裡面打上

`tableB`.`A_id`=`tableA`.`A_id`

意思就是要讓表格合併起來 (像是INNER JOIN)

 

----------------------------------------------------


*TIPS:

 

WHERE id=id能獨立跑的是這個

SELECT `tableA`.*, `tableB`.* FROM `tableA`, `tableB` WHERE `tableB`.`A_id`=`tableA`.`A_id`

用INNER JOIN 改寫變成

SELECT `tableA`.*, `tableB`.* FROM `tableA`INNER JOIN `tableB` ON `tableB`.`A_id`=`tableA`.`A_id`

 

----------------------------------------------------

在來就是外面那層

SELECT `A_id`, `A_name`, (......) AS `B_count`,  (......) AS `C_count`,  FROM `tableA`;

就只有簡單的撈整張表格出來而已

 

AS就是做欄位別名

整個SQL語句要做為一個欄位賦予別名

那該SQL語句必須資料輸出一個欄位而已

這裡輸出COUNT(*)剛好只有一欄，符合規定

 

----------------------------------------------------

其它範例

 

有個問卷的系統，表格長這樣

這個學生詢問了向各種對象，問各種不同的問題，放在不同的表格

而如今他想要把他的問題做統計

 

欄位名稱如下

Student(id,name,mykad,...)
Customer Service(id, Q1,Q2,Q3,date)
Instructor(id, Q1,Q2,Q3,date)
Runner(id, Q1,Q2,Q3,date)

SQL語法如下：

SELECT A.name, A.mykad, 

(select count(*) from customerservice B where B.id = A.id and B.Q1='Excellent') AS E, 
(select count(*) from customerservice C where C.id = A.id and C.Q1='Satisfaction') AS S,
(select count(*) from customerservice D where D.id = A.id and D.Q1='Poor') AS P
FROM student A

 

就會輸出欄位

name   mykad  E  S  P
```

[SQL: Combine Select count(*) from multiple tables edited Aug 1 '17](http://stackoverflow.com/questions/1279569/sql-combine-select-count-from-multiple-tables)  
[Multiple SQL count, join and where ](http://www.daniweb.com/software-development/legacy-and-other-languages/threads/352342)  

## SQL JOIN  
[SQL 語法Multiple Tables JOIN – Benjr.tw 2019-09-04](http://benjr.tw/101957)  

![alt tag](http://benjr.tw/wp-content/uploads/2019/09/sqljoin00569.png)  

```
SELECT p.name , p.member , s.dept , d.info
FROM project p 
INNER JOIN staff s ON p.member = s.name  
INNER JOIN dept d ON s.dept = d.name  
WHERE p.name='A';
```
```
SELECT p.name , p.member , s.dept , d.info FROM project p INNER JOIN staff s ON p.member = s.name INNER JOIN dept d ON s.dept = d.name WHERE p.name='A';
+------+--------+------+-----------------+
| name | member | dept | info            |
+------+--------+------+-----------------+
| A    | Ben    | HR   | Human Resource  |
| A    | Jason  | HW   | HardWare        |
| A    | Thomas | Test | Validation Test |
+------+--------+------+-----------------+
3 rows in set (0.00 sec)
```

### UNION  
 
[SQL 語法JOIN 與UNION – Benjr.tw 2019-08-20](http://benjr.tw/101855)  
```
多個資料表單有相對應的欄位時,我們可以透過 JOIN 來同時查詢多個資料表單的資料, UNION 可以把一個以上的查詢結果合併為一個.
```

```

UNION 合併查詢,可以把一個以上的查詢結果合併為一個,前提是欄位名稱需相同.
下面兩個獨立的查詢,可以用 OR 或是 UNION 合併查詢的方式.
```

```
SELECT name,member 
FROM project 
WHERE name LIKE 'A';
```

```
SELECT name,member 
FROM project 
WHERE name LIKE 'B' ;
```

使用 OR 的語法合併兩次 SELECT 出來的結果.  
```
SELECT name,member 
FROM project 
WHERE name LIKE 'A' OR name LIKE 'B';
```

使用 UNION 的語法合併兩次 SELECT 出來的結果.
```
SELECT name,member 
FROM project 
WHERE name LIKE 'A'
UNION 
SELECT name,member 
FROM project 
WHERE name LIKE 'B';
```

```
SELECT name,member FROM project WHERE name LIKE 'A' UNION SELECT name,member FROM project WHERE name LIKE 'B';

+------+--------+
| name | member |
+------+--------+
| A    | Ben    |
| A    | Jason  |
| A    | Thomas |
| B    | Jack   |
| B    | Andy   |
| B    | Chuck  |
+------+--------+
6 rows in set (0.02 sec)
```


## Convert Column to Row (Pivot Table)  
[MySQL- Convert Column to Row (Pivot Table 樞紐分析表) 2019-09-11](http://benjr.tw/102000)  

```
將資料庫的列 (Column) 轉換為行 (row) 來呈現 (Pivot Table : 樞紐分析表) 其統計結果,如下圖所示.
```

![alt tag](http://benjr.tw/wp-content/uploads/2019/09/PivotTable0013.png)  

```

```
```

```

# Regular Express  
[[實用] 用 Regular Expression 做字串比對 23 Jun 2016](https://larry850806.github.io/2016/06/23/regex/)  
RegExp | Description | Example
------------------------------------ | --------------------------------------------- | ---------------------------------------------
/^\d{4}-\d{2}-\d{2}$/ | 西元生日格式 | "1996-08-06"
/^[A-Z]\d{9}$/ | 身分證字號 | "A123456789"
/^09\d{8}$/ | 手機號碼 | "0912345678"
/^[^aeiou]*$/ | 不包含小寫母音的字串 | "hEllO","ApplE"
/^.*@gmail\.com$/ | gmail 信箱 | "test@gmail.com"
/^[0-9\+\-\*\/]*$/ | 四則運算算式 | "1+2*3" 

![alt tag]()  

# Troubleshooting  


# Reference  
[Python: How to unzip a file | Extract Single, multiple or all files from a ZIP archive December 1, 2018](https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/)  
```
def main():
 
    print('Extract all files in ZIP to current directory')
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile('sampleDir.zip', 'r') as zipObj:
       # Extract all the contents of zip file in current directory
       zipObj.extractall()
 
    print('Extract all files in ZIP to different directory')
 
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile('sampleDir.zip', 'r') as zipObj:
       # Extract all the contents of zip file in different directory
       zipObj.extractall('temp')
 
    print('Extract single file from ZIP')
 
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile('sampleDir.zip', 'r') as zipObj:
       # Get a list of all archived file names from the zip
       listOfFileNames = zipObj.namelist()
       # Iterate over the file names
       for fileName in listOfFileNames:
           # Check filename endswith csv
           if fileName.endswith('.csv'):
               # Extract a single file from zip
               zipObj.extract(fileName, 'temp_csv')
 
 
 
if __name__ == '__main__':
   main()
```

[pythonでzipファイルを再帰的に展開 Jun 01, 2017](https://qiita.com/arwtyxouymz0110/items/2caed2f760d586969972)  

```
 expand_zip.py

# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import glob


def unzip(filename):
    with zipfile.ZipFile(filename, "r") as zf:
        zf.extractall(path=os.path.dirname(filename))
    delete_zip(filename)


def delete_zip(zip_file):
    os.remove(zip_file)


def walk_in_dir(dir_path):
    for filename in glob.glob(os.path.join(dir_path, "*.zip")):
        unzip(filename=os.path.join(dir_path,filename))

    for dirname in (d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))):
        walk_in_dir(os.path.join(dir_path, dirname))


if __name__ == "__main__":
    args = sys.argv
    try:
        if(os.path.isdir(args[1])):
            walk_in_dir(args[1])
        else:
            unzip(os.path.join(args[1]))
            name, _ = os.path.splitext(args[1])
            if (os.path.isdir(name)):
                walk_in_dir(name)
    except IndexError:
        print('IndexError: Usage "python %s ZIPFILE_NAME" or "python %s DIR_NAME"' % (args[0], args[0]))
    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])
```

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
