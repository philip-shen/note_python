Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Create a .csv file with values from a Python list](#create-a-csv-file-with-values-from-a-python-list)
   * [使用python獲取csv文字的某行或某列資料的例項](#使用python獲取csv文字的某行或某列資料的例項)
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

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose
Take a note of CSV in Python


# Create a .csv file with values from a Python list
[Create a .csv file with values from a Python list](https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list)


# 使用python獲取csv文字的某行或某列資料的例項   
[使用python獲取csv文字的某行或某列資料的例項](https://www.itread01.com/article/1522718793.html)
[pilicurg / GetCsvColumn](https://github.com/pilicurg/GetCsvColumn/blob/master/demo.py)


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

