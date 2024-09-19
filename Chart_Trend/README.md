Table of Contents
=================
   * [Purpose](#purpose)
   * [StockInsider](#stockinsider)   
      * [Usage](#usage)
         * [1. Create Virtual Environment](#1-create-virtual-environment)
         * [2. Active Virtual Environment](#2-active-virtual-environment)
         * [3. Install packages](#3-install-packages)
         * [4. Edit conf.json](#4-edit-conf.json)
         * [5. Excute Python Sample Code](#5-excute-python-sample-code)
      * [2330 BBIBOLL](#2330-bbiboll)
      * [2382 BBIBOLL](#2382-bbiboll)
      * [Reference](#reference)
      * [Troubleshooting](#troubleshooting)
   * [trendet](#trendet)   
      * [Usage](#usage-1)
         * [1. Create Virtual Environment](#1-create-virtual-environment-1)
         * [2. Active Virtual Environment](#2-active-virtual-environment-1)
         * [3. Install packages](#3-install-packages-1)
         * [4. Edit conf.json](#4-edit-conf.json-1)
         * [5. Excute Python Sample Code](#5-excute-python-sample-code-1)
      * [2330](#2330)
      * [Reference](#reference-1)
      * [Troubleshooting](#troubleshooting-1)
   * [TW_Stocker](#tw_stocker)   
      * [Usage](#usage-2)
         * [1. Create Virtual Environment](#1-create-virtual-environment-2)
         * [2. Active Virtual Environment](#2-active-virtual-environment-2)
         * [3. Install packages](#3-install-packages-2)
         * [4. Excute Python Sample Code](#4-excute-python-sample-code) 
      * [Reference](#reference-2)
      * [Troubleshooting](#troubleshooting-2)
   * [Trade_Strategy](#trade_strategy)   
      * [Turtle Trading](#turtle-trading)
         * [Usage](#usage-3)
            * [1. Create Virtual Environment](#1-create-virtual-environment-3)
            * [2. Active Virtual Environment](#2-active-virtual-environment-3)
            * [3. Install packages](#3-install-packages-3)
            * [4. Excute Python Sample Code](#4-excute-python-sample-code-1) 
         * [Reference](#reference-3)
         * [Troubleshooting](#troubleshooting-3)
   * [Stock_Selection](#stock_selection)            
      * [Reference](#reference-4)         
   * [Reference](#reference-5)
   * [Troubleshooting](#troubleshooting-5)
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
[test_bbibol.py](StockInsider/test_bbibol.py)
```
python test_bbibol.py --conf conf.json
```

[test_bbibol_fromGsheet.py](StockInsider/test_bbibol_fromGsheet.py)
```
run_fromGsheet.bat config_xxxxx.json GSheet_xxxxx.json
```

[test_twseotc_stocks.py](StockInsider/test_twseotc_stocks.py)  
```
run_twseotc_stocks.bat config_xxxxx.json GSheet_xxxxx.json
```

## 2330 BBIBOLL  
<img src="images/2330_BBIBOLL.png" width="600" height="400">   

## 2382 BBIBOLL  
<img src="images/2382_BBIBOLL.png" width="600" height="400">  

## Reference
[charlesdong1991/StockInsider](https://github.com/charlesdong1991/StockInsider)  
[smalldan1022 /Taiwan-Stocks](https://github.com/smalldan1022/Taiwan-Stocks)  
[litefunc /tse ](https://github.com/litefunc/tse)  

## Troubleshooting  
[Plotly fig.to_image is stucking on windows 11. #126](https://github.com/plotly/Kaleido/issues/126)  
[Static image export hangs using kaleido](https://community.plotly.com/t/static-image-export-hangs-using-kaleido/61519)  
[v0.1.0.post1](https://github.com/plotly/Kaleido/releases/tag/v0.1.0.post1)  
```
Downloading and installing 0.1.0.post1 1.2k should work.
I downloaded this wheel:

kaleido-0.1.0.post1-py2.py3-none-win_amd64.whl

And then installed:
pip install kaleido-0.1.0.post1-py2.py3-none-win_amd64.whl
```


# trendet  

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
    "ticker": "2330.TW",
    "up_trend_color": "red",
    "down_trend_color": "green",
    "images_folder":"xxxxx"
}
```

### 5. Excute Python Sample Code
```
python test_identify_chart_trends.py --conf config.json
```

## 2330
<img src="images/2330_trendet.jpg" width="600" height="400">  

## Reference
[alvarobartt/trendet](https://github.com/alvarobartt/trendet)  

## Troubleshooting  

# TW_Stocker    

## Usage  
### 1. Create Virtual Environment  
```
python3.10 -m venv ~/virtualenv/moneyhunter
```

### 2. Active Virtual Environment
```
source ~/virtualenv/moneyhunter/bin/activate
```

### 3. Install packages
```
pip install -r requirements.txt
```

### 4. Excute Python Sample Code
```
python test_backtest.py
```

## Reference
[polakowo/vectorbt](https://github.com/polakowo/vectorbt)  
[voidful/FTA](https://github.com/voidful/FTA)  
[voidful/tw_stocker](https://github.com/voidful/tw_stocker)  
[psemdel/py-trading-bot](https://github.com/psemdel/py-trading-bot)

## Troubleshooting  
[TW_Stocker/requirements_vectorbt.txt](TW_Stocker/requirements_vectorbt.txt)  
[TW_Stocker/install_tulip.sh](TW_Stocker/install_tulip.sh)  


# Trade_Strategy    

## Turtle Trading 

### Usage  

#### 1. Create Virtual Environment  
```
c:/Python310/python.exe -m venv c:\Users\xxxx\Envs\moneyhunter
```

#### 2. Active Virtual Environment
```
c:\Users\XXXXX\Envs\moneyhunter\Scripts\activate.bat
```

#### 3. Install packages
```
pip install -r requirements.txt
```

#### 4. Excute Python Sample Code
```
python test_trade.py
```

```
(moneyhunter) λ python test_trade.py
2024-05-01 13:20:18,826 - test_trade.py[line:31]- INFO: Start Time is 2024/5/1 13:20:18
2024-05-01 13:20:19,042 - test_trade.py[line:38]- INFO: Price of 2024-04-30: 790.0
2024-05-01 13:20:19,042 - test_trade.py[line:44]- INFO: N_value: 0.6
2024-05-01 13:20:19,042 - test_trade.py[line:45]- INFO: position_sizes: 21.097
2024-05-01 13:20:19,059 - test_trade.py[line:48]- INFO: None
2024-05-01 13:20:19,074 - test_trade.py[line:49]- INFO: None
2024-05-01 13:20:19,074 - test_trade.py[line:51]- INFO: [310, 311.25, 312.5, 313.75]
2024-05-01 13:20:19,074 - test_trade.py[line:52]- INFO: [310, 311.25, 312.5, 313.75, 315.0, 316.25]
2024-05-01 13:20:19,074 - test_trade.py[line:22]- INFO: Time Consumption: 00s.
```

### Reference
[The Original Turtle Trading Rules](https://oxfordstrat.com/coasdfASD32/uploads/2016/01/turtle-rules.pdf)  
[gabekutner/turtle-trading](https://github.com/gabekutner/turtle-trading)  

[shawn-guiqin/turtleTrader](https://github.com/shawn-guiqin/turtleTrader)  
[wpicon/gui](https://github.com/wpicon/gui)  
[pplonski/turtle-trading-python](https://github.com/pplonski/turtle-trading-python)  

### Troubleshooting  
[Warning - Certain functionality requires requests_html, which is not installed](https://stackoverflow.com/questions/76783292/warning-certain-functionality-requires-requests-html-which-is-not-installed)  

```
Warning - Certain functionality
             requires requests_html, which is not installed.

             Install using:
             pip install requests_html

             After installation, you may have to restart your Python session.
```

```
(moneyhunter) λ python test_req_html.py
Traceback (most recent call last):
  File "d:\projects\turtle-trading\src\test_req_html.py", line 1, in <module>
    from requests_html import HTMLSession
  File "c:\Users\amyfa\Envs\moneyhunter\lib\site-packages\requests_html.py", line 14, in <module>
    from lxml.html.clean import Cleaner
  File "c:\Users\amyfa\Envs\moneyhunter\lib\site-packages\lxml\html\clean.py", line 18, in <module>
    raise ImportError(
ImportError: lxml.html.clean module is now a separate project lxml_html_clean.
Install lxml[html_clean] or lxml_html_clean directly.
```

```
(moneyhunter) λ python test_req_html.py
<Response [200]>
```


# Stock_Selection      


## Reference
[obendidi/pstock](https://github.com/obendidi/pstock)   
```
Async yahoo-finance python api with pydantic models.
```

[ttamg/yahoo-finance-async](https://github.com/ttamg/yahoo-finance-async?tab=readme-ov-file)  
```
Python library that accesses the deprecated Yahoo Finance API for OHLC data using asyncio 
```

[pstocky/pstocky](https://github.com/pstocky/pstocky)
```
股票小数据
```

[ta-lib-python: Function API Examples](https://github.com/TA-Lib/ta-lib-python/blob/master/docs/func.md)  
[tkfy920/PythonQuantitativeFinance](https://github.com/tkfy920/PythonQuantitativeFinance/tree/master)  
```
专注于分享Python在金融领域的应用，欢迎关注微信公众号: Python金融量化 （id：tkfy920）
```
[myhhub/stock](https://github.com/myhhub/stock?tab=readme-ov-file)  
```
stock股票.获取股票数据,计算股票指标,识别股票形态,内置选股策略,股票验证回测,股票自动交易,支持PC及移动设备。 
```
[sngyai / Sequoia](https://github.com/sngyai/Sequoia?tab=readme-ov-file)  
```
A股自动选股程序，实现了海龟交易法则、缠中说禅牛市买点，以及其他若干种技术形态 
```
[zhouyantao / PythonStock](https://github.com/zhouyantao/PythonStock)  
```
使用python的tushare库编写的股票相关的应用
```
[ricequant / rqalpha](https://github.com/ricequant/rqalpha?tab=readme-ov-file)  
```
RQAlpha 从数据获取、算法交易、回测引擎，实盘模拟，实盘交易到数据分析，为程序化交易者提供了全套解决方案。
```

[如何使用Python取得歷史股價，簡介yfinance、ffn、FinMind 2021年11月7日](https://havocfuture.tw/blog/python-stock-history)  
[如何使用Python產生技術指標？TA-Lib簡易教學 2022年10月30日](https://havocfuture.tw/blog/python-indicators-talib)  
[Python 交易回測工具 Backtesting.py 簡易教學 2023年2月25日](https://havocfuture.tw/blog/python-backtesting-py)  
[0050-k20-backtesting-py.ipynb](https://colab.research.google.com/drive/13lan-S9uWLrmCU47iwX_j_4uskp2PbSi?usp=sharing)  

[用AI預測股價？實測 Facebook Prophet 預言家 2022年9月4日](https://havocfuture.tw/blog/ai-fb-prophet)  
[如何破解網站驗證碼，實測證交所買賣日報表 2022年1月11日](https://havocfuture.tw/blog/captcha-bsr#%E5%AF%A6%E6%B8%AC%E8%A8%98%E9%8C%84)  
[股票市場多少是合理的投資報酬率？實測美股大盤28年 2021年11月9日](https://havocfuture.tw/blog/reasonable-stock-return-spy)  
[高股息ETF是好的投資標的嗎？完整回測高股息ETF 0056 過去16年歷史股價報酬表現 2024年4月26日](https://havocfuture.tw/blog/backtesting-0056)    
```
結論
    回測十六年績效，採用股息全部再投入，不計算稅金和交易手續費，0056 的年報酬率(CAGR)為 6.37%，對比同時間的 0050 為 8.07%，兩者是有差距的
    這一、兩年 0056 的績效明顯比 0050 好，這個報酬率是例外，請不要當成常態來看待
    不同高股息 ETF 的報酬率有一定差異，想要投資還是需要去比較一下持股的成份
```

[louisnw01 / lightweight-charts-python](https://github.com/louisnw01/lightweight-charts-python?tab=readme-ov-file)  

[ファイナンス分野でInfluxDB+Grafanaを使う（株価をローソク足表示） 2022-08-27](https://qiita.com/ixtlan001/items/268dfab0d1ee21887602)   
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F2781605%2F6b4e35e6-6da5-0b1d-22b0-cd2b5c12b22a.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=13b6e612a7f3aab1659d2488a48331c0" width="900" height="500">  


# Reference

# Troubleshooting





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
