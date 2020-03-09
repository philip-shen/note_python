# Purpose  
Take note of Zip and UnZip  

# Table of Contents  
[]()  

[SQL Sytnax](#sql-sytnax)  

# 
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
