Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Create a .csv file with values from a Python list](#create-a-csv-file-with-values-from-a-python-list)
   * [使用python獲取csv文字的某行或某列資料的例項](#使用python獲取csv文字的某行或某列資料的例項)
   * [python dict to csv transpose](#python-dict-to-csv-transpose)
      * [If you don't care about the order of your columns (since dictionaries are unordered), you can simply use zip():](#if-you-dont-care-about-the-order-of-your-columns-since-dictionaries-are-unordered-you-can-simply-use-zip)
      * [If you do care about order, you need to sort the keys:](#if-you-do-care-about-order-you-need-to-sort-the-keys)
   * [transpose dict of lists and write to csv](#transpose-dict-of-lists-and-write-to-csv)
   * [Troubleshooting](#troubleshooting)
      * [python csv2libsvm.py: AttributeError: '_csv.reader' object has no attribute 'next'](#python-csv2libsvmpy-attributeerror-_csvreader-object-has-no-attribute-next)
      * [Error: “ 'dict' object has no attribute 'iteritems' ”](#error--dict-object-has-no-attribute-iteritems-)
      * [TypeError: 'dict_keys' object does not support indexing](#typeerror-dict_keys-object-does-not-support-indexing)
   * [Reference](#reference)
      * [Python中split()和os.path.split()](#python中split和ospathsplit)
      * [os.path套件處理檔案路徑名稱](#ospath套件處理檔案路徑名稱)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)
# Purpose
Take a note of CSV in Python


# Create a .csv file with values from a Python list
[Create a .csv file with values from a Python list](https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list)


# 使用python獲取csv文字的某行或某列資料的例項   
[使用python獲取csv文字的某行或某列資料的例項](https://www.itread01.com/article/1522718793.html)
[pilicurg / GetCsvColumn](https://github.com/pilicurg/GetCsvColumn/blob/master/demo.py)


# python dict to csv transpose  
[Write dictionary of lists to a CSV file 2019年5月17日](https://stackoverflow.com/questions/23613426/write-dictionary-of-lists-to-a-csv-file)  

## If you don't care about the order of your columns (since dictionaries are unordered), you can simply use zip():  

'''
d = {"key1": [1,2,3], "key2": [4,5,6], "key3": [7,8,9]}
with open("test.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(d.keys())
   writer.writerows(zip(*d.values()))
'''

'''
Result:

key3    key2    key1
7       4       1
8       5       2
9       6       3
'''

## If you do care about order, you need to sort the keys:  
'''
keys = sorted(d.keys())
with open("test.csv", "wb") as outfile:
   writer = csv.writer(outfile, delimiter = "\t")
   writer.writerow(keys)
   writer.writerows(zip(*[d[key] for key in keys]))
'''

'''
Result:

key1    key2    key3
1       4       7
2       5       8
3       6       9
'''

# transpose dict of lists and write to csv 
[transpose dict of lists and write to csv 2017年6月15日](https://stackoverflow.com/questions/36870201/transpose-dict-of-lists-and-write-to-csv)  

'''
defaultdict(<type 'list'>, {1: ['Genemark1.10973_g', 'missense_variant', 'MODERATE', 'scaffold_100', 305, '605', 'Asp', 'Gly', 'YES', 'NO', 'NO', 'NO'], 2: ['estExt_Genewise1Plus.C_1000001', 'disruptive_inframe_insertion', 'MODERATE', 'scaffold_100', 5002, '7172', 'Gly', '', 'YES', 'NO', 'NO', 'NO'], 3: ['fgenesh2_pm.100_#_3', 'inframe_insertion', 'MODERATE', 'scaffold_100', 10104, '265266', 'Leu', '', 'YES', 'NO', 'NO', 'NO'], 4: ['estExt_fgenesh2_pg.C_100178', 'inframe_deletion', 'MODERATE', 'scaffold_10', 711411, '351352', 'Gln', '', 'YES', 'NO', 'NO', 'NO'], 5: ['estExt_fgenesh2_pm.C_1060001', 'disruptive_inframe_deletion', 'MODERATE', 'scaffold_106', 5189, '832', 'Leu', 'del', 'YES', 'NO', 'NO', 'NO'], 6: ['Genemark1.10980_g', 'frameshift_variant', 'HIGH', 'scaffold_101', 10838, '313', 'Leu', 'fs', 'NO', 'YES', 'NO', 'NO'], 7: ['Genemark1.10973_g', 'missense_variant', 'MODERATE', 'scaffold_100', 2043, '26', 'Ile', 'Leu', 'YES', 'NO', 'NO', 'NO'], 8: ['fgenesh2_pm.104_#_2', 'stop_gained', 'HIGH', 'scaffold_104', 8574, '310', 'Tyr', '*', 'YES', 'NO', 'NO', 'NO']})
'''

'''
No need to zip for your requirement. Think about it. You want each element of a row to appear in its column, which is same as just keeping the row intact.
'''

'''
def printAnn(d):
    w = csv.writer(sys.stdout, delimiter='\t', quoting=csv.QUOTE_NONE, lineterminator='\n')
    w.writerows(d.values())

printAnn(d)
Genemark1.10973_g       missense_variant        MODERATE        scaffold_100 305     605     Asp     Gly     YES     NO      NO      NO
estExt_Genewise1Plus.C_1000001  disruptive_inframe_insertion    MODERATE scaffold_100    5002    7172    Gly             YES     NO      NO      NO
fgenesh2_pm.100_#_3     inframe_insertion       MODERATE        scaffold_100 10104   265266  Leu             YES     NO      NO      NO
estExt_fgenesh2_pg.C_100178     inframe_deletion        MODERATE       scaffold_10     711411  351352  Gln             YES     NO      NO      NO
estExt_fgenesh2_pm.C_1060001    disruptive_inframe_deletion     MODERATE scaffold_106    5189    832     Leu     del     YES     NO      NO      NO
Genemark1.10980_g       frameshift_variant      HIGH    scaffold_101    10838 313     Leu     fs      NO      YES     NO      NO
Genemark1.10973_g       missense_variant        MODERATE        scaffold_100 2043    26      Ile     Leu     YES     NO      NO      NO
fgenesh2_pm.104_#_2     stop_gained     HIGH    scaffold_104    8574    310 Tyr     *       YES     NO      NO      NO
'''



# Troubleshooting
## python csv2libsvm.py: AttributeError: '_csv.reader' object has no attribute 'next'  
[python csv2libsvm.py: AttributeError: '_csv.reader' object has no attribute 'next'](https://stackoverflow.com/questions/42767250/python-csv2libsvm-py-attributeerror-csv-reader-object-has-no-attribute-nex)    

'''
write next(reader) instead of reader.next() 
'''

## Error: “ 'dict' object has no attribute 'iteritems' ”      
[Error: “ 'dict' object has no attribute 'iteritems' ”](https://stackoverflow.com/questions/30418481/error-dict-object-has-no-attribute-iteritems)          
'''
use dict.items() instead of dict.iteritems()
'''

## TypeError: 'dict_keys' object does not support indexing  
[TypeError: 'dict_keys' object does not support indexing](https://stackoverflow.com/questions/17322668/typeerror-dict-keys-object-does-not-support-indexing)  

'''
python2.x (when d.keys() returned a list). 
With python3.x, d.keys() returns a dict_keys object which behaves a lot more like a set than a list. 
As such, it can't be indexed.

The solution is to pass list(d.keys()) (or simply list(d)) to shuffle.
'''


# Reference  
## Python中split()和os.path.split()  
[Python中split()和os.path.split()](https://zhuanlan.zhihu.com/p/43577892)  

## os.path套件處理檔案路徑名稱  
[os.path套件處理檔案路徑名稱](https://b0212066.pixnet.net/blog/post/212659818-os.path%E5%A5%97%E4%BB%B6%E8%99%95%E7%90%86%E6%AA%94%E6%A1%88%E8%B7%AF%E5%BE%91%E5%90%8D%E7%A8%B1)  



* []()  
![alt tag]()  
<img src=""  width="300" height="400">

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



