Table of Contents
=================
   * [Purpose](#purpose)
   * [Usage](#usage)
      * [1. Create Virtual Environment](#1-create-virtual-environment)
      * [2. Active Virtual Environment](#2-active-virtual-environment)
      * [3. Install packages](#3-install-packages)
      * [4. Edit conf.json](#4-edit-conf.json)
      * [5. Excute Python Sample Code](#5-excute-python-sample-code)
   * [2330 BBIBOLL](#2330-bbiboll)
   * [2382 BBIBOLL](#2382-bbiboll)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference-1)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)


Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose  
Take note of Chart Trend

# StockInsider  

## Usage  
### 1. Create Virtual Environment  
```
 c:/Python310/python.exe -m venv c:\Users\XXXXX\Envs\chart_trend  
```

### 2. Active Virtual Environment
```
c:\Users\XXXXX\Envs\chart_trend\Scripts\activate.bat
```

### 3. Install packages
```
pip install -r requirements.txt
```

### 4. Edit conf.json 
```
{
    "stock_indexes": ["2303",
                       "2330" 
    ], 
    "twse_otc_id_pickle":"xxxxx.pickle"
}
```

### 5. Excute Python Sample Code
```
python test_bbibol.py --conf conf.json
```

## 2330 BBIBOLL  
<img src="images/2330_BBIBOLL.png" width="600" height="400">   

## 2382 BBIBOLL  
<img src="images/2382_BBIBOLL.png" width="600" height="400">  

## Reference
[charlesdong1991/StockInsider](https://github.com/charlesdong1991/StockInsider)  


# Troubleshooting


# Reference



* []()  
![alt tag]()
<img src="" width="400" height="500">  

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
