# Take notes of pandas releated stuffs

# Table of Contents
[Setting up a Bollinger Band with Python](#setting-up-a-bollinger-band-with-python)  

[How to compute and plot Bollinger Bands® in Python](#how-to-compute-and-plot-bollinger-bands-in-python)  

[Trading: Calculate Technical Analysis Indicators with Pandas](#trading-calculate-technical-analysis-indicators-with-pandas)  
[Prerequisite environment setup](#prerequisite-environment-setup)  
[Data:](#data)  
[Code:](#code)  

[%B Indicator](#b-indicator)  
[Introduction](#introduction)  
[Calculation](#calculation)  
[Signals: Overbought/Oversold](#signals:-overbought/oversold)
[Signals: Trend Identification](#signals:-trend-identification)  

[Reference](#reference)

# Setting up a Bollinger Band with Python  
[Setting up a Bollinger Band with Python Jan 13, 2018](https://medium.com/python-data/setting-up-a-bollinger-band-with-python-28941e2fa300)
## Main Components of a Bollinger Bands  
* 1. Upper Band: The upper band is simply two standard deviations above the moving average of a stock’s price.
* 2. Middle Band: The middle band is simply the moving average of the stock’s price.
* 3. Lower Band: Two standard deviations below the moving average is the lower band.

## The formula for a typical 20 day Bollinger Band:  
```
Middle Band = 20 day moving average
Upper Band = 20 day moving average + (20 Day standard deviation of price x 2) 
Lower Band = 20 day moving average - (20 Day standard deviation of price x 2)
```
## Bollinger Band in Python  
```
# import needed libraries
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as web

# Make function for calls to Yahoo Finance
def get_adj_close(ticker, start, end):
    '''
    A function that takes ticker symbols, starting period, ending period
    as arguments and returns with a Pandas DataFrame of the Adjusted Close Prices
    for the tickers from Yahoo Finance
    '''
    start = start
    end = end
    info = web.DataReader(ticker, data_source='yahoo', start=start, end=end)['Adj Close']
    return pd.DataFrame(info)

# Get Adjusted Closing Prices for Facebook, Tesla and Amazon between 2016-2017
fb = get_adj_close('fb', '1/2/2016', '31/12/2017')
tesla = get_adj_close('tsla', '1/2/2016', '31/12/2017')
amazon = get_adj_close('amzn', '1/2/2016', '31/12/2017')

# Calculate 30 Day Moving Average, Std Deviation, Upper Band and Lower Band
for item in (fb, tesla, amazon):
    item['30 Day MA'] = item['Adj Close'].rolling(window=20).mean()
    item['30 Day STD'] = item['Adj Close'].rolling(window=20).std()
    item['Upper Band'] = item['30 Day MA'] + (item['30 Day STD'] * 2)
    item['Lower Band'] = item['30 Day MA'] - (item['30 Day STD'] * 2)

# Simple 30 Day Bollinger Band for Facebook (2016-2017)
fb[['Adj Close', '30 Day MA', 'Upper Band', 'Lower Band']].plot(figsize=(12,6))
plt.title('30 Day Bollinger Band for Facebook')
plt.ylabel('Price (USD)')
plt.show();
```
[View Raw](https://gist.github.com/PyDataBlog/04df02f5084d1fd376c9b4ce198e6a0e/raw/40f56e2c1ae88df9cf0ec8bf2d01f4fe2ae471cf/Simple%20Bollinger%20Plot.py)  


# How to compute and plot Bollinger Bands® in Python  
[How to compute and plot Bollinger Bands® in Python July 8, 2019](https://skipperkongen.dk/2019/07/08/how-to-compute-and-plot-bollinger-bands-in-python/)
![alt tag](https://i1.wp.com/skipperkongen.dk/wp-content/uploads/2019/07/Screenshot-2019-07-08-at-13.20.42.png?w=768&ssl=1)  
```
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

N = 100
XMAX = 5
WINMA = 10
ALPHA = 2

def get_bollinger(data, winma=10, alpha=2):
    ser = pd.Series(data)
    ma = ser.rolling(winma).mean()
    std = ser.rolling(winma).std()
    lower = pd.Series(ma - alpha*std).fillna(method='bfill').values
    upper = pd.Series(ma + alpha*std).fillna(method='bfill').values
    return lower, upper

def get_alerts(data, lower, upper):
    low = np.argwhere(data < lower)
    high = np.argwhere(data > upper)
    return low, high

if __name__=='__main__':

    X = np.linspace(0.0, XMAX, num=N)
    data = np.sin(X) + np.random.random(N)
    lower, upper = get_bollinger(data, winma=WINMA, alpha=ALPHA)
    low, high = get_alerts(data, lower, upper)
    for i in low:
        plt.plot(X[i], data[i], 'ro')
    for i in high:
        plt.plot(X[i], data[i], 'ro')
    plt.plot(X, lower)
    plt.plot(X, data)
    plt.plot(X, upper)
    plt.show()
```
# Trading: Calculate Technical Analysis Indicators with Pandas  
[Trading: Calculate Technical Analysis Indicators with Pandas Apr 30, 2018](https://towardsdatascience.com/trading-technical-analysis-with-pandas-43e737a17861)  


## Prerequisite environment setup  
## Data:  
[Collect Trading Data with Pandas Library Apr 29, 2018 ](https://towardsdatascience.com/collect-trading-data-with-pandas-library-8904659f2122)
Step1: Environment setup (virtual env)
```
python3 -m venv tutorial-env
source ~/tutorial-env/bin/activate
pip install panda
pip install pandas_datareader
pip install matplotlib
pip install scipy
```

Step2: Code (fetching data and dump to a csv file)  
```
import matplotlib.pyplot as plt
import pandas_datareader.data as web
# collect data for Amazon from 2017-04-22 to 2018-04-22
start = '2017-04-22'
end = '2018-04-22'
df = web.DataReader(name='AMZN', data_source='iex', start=start, end=end)
print(df)
df.to_csv("~/workspace/{}.csv".format(symbol))
```

Step3: Visualize what was collected with matplotlib
```
# select only close column
close = df[['close']]
# rename the column with symbole name
close = close.rename(columns={'close': symbol})
ax = close.plot(title='Amazon')
ax.set_xlabel('date')
ax.set_ylabel('close price')
ax.grid()
plt.show()
```
![alt tag](https://miro.medium.com/max/640/1*-NmkCDiCu2J1PUziNXhptQ.png)  


## Code:  
```
import pandas as pd
import matplotlib.pyplot as plt

symbol='AMZN'
# read csv file, use date as index and read close as a column
df = pd.read_csv('~/workspace/{}.csv'.format(symbol), index_col='date',
                 parse_dates=True, usecols=['date', 'close'],
                 na_values='nan')
# rename the column header with symbol name
df = df.rename(columns={'close': symbol})
df.dropna(inplace=True)

# calculate Simple Moving Average with 20 days window
sma = df.rolling(window=20).mean()

# calculate the standar deviation
rstd = df.rolling(window=20).std()

upper_band = sma + 2 * rstd
upper_band = upper_band.rename(columns={symbol: 'upper'})
lower_band = sma - 2 * rstd
lower_band = lower_band.rename(columns={symbol: 'lower'})


df = df.join(upper_band).join(lower_band)
ax = df.plot(title='{} Price and BB'.format(symbol))
ax.fill_between(df.index, lower_band['lower'], upper_band['upper'], color='#ADCCFF', alpha='0.4')
ax.set_xlabel('date')
ax.set_ylabel('SMA and BB')
ax.grid()
plt.show()
```
![alt tag](https://miro.medium.com/max/1280/1*JsLK7dWaeY04fBA5aJn87w.png)  

# %B Indicator  
## Introduction  
[%B Indicator](https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_band_perce)  

Item | Description
------------------------------------ | ---------------------------------------------
%B < 0 | when price is below the lower band
%B = 0 | when price is at the lower band
%B > 0 and < .50 | when price is between the lower and middle band (20-day SMA)
%B < .50 and < 1 | when price is between the upper and middle band (20-day SMA)
%B = 1 | when price is at the upper band
%B > 1 | when price is above the upper band

## Calculation  
```
%B = (Price - Lower Band)/(Upper Band - Lower Band)
```
The default setting for %B is based on the default setting for Bollinger Bands (20,2). 
The bands are set 2 standard deviations above and below the 20-day simple 
[moving average](https://school.stockcharts.com/doku.php?id=glossary_m#moving_average_ma), 
which is also the middle band. Security price is the close or the last trade. 

## Signals: Overbought/Oversold  
```
%B can be used to identify overbought and oversold situations. 
However, it is important to know when to look for overbought vs. oversold readings. 
As with most momentum oscillators, it is best to look for short-term oversold situations 
when the medium-term trend is up and short-term overbought situations when the medium-term trend is down. 
In other words, look for opportunities in the direction of the bigger trend, 
such as a pullback within a bigger uptrend. You must define the bigger trend before looking for overbought or oversold readings.
```
```
Chart 1 shows Apple (AAPL) within a strong uptrend. %B moved above 1 several times, 
but these “overbought” readings still failed to produce good sell signals. 
Pullbacks were shallow as Apple reversed well above the lower band and resumed its uptrend. 
John Bollinger refers to “walking the band” during strong trends. 
This refers to the notion that, in a strong uptrend, prices can walk up the upper band and rarely touch the lower band. 
Conversely, in a strong downtrend, prices can walk down the lower band and rarely touch the upper band. 
```
![alt tag](https://school.stockcharts.com/lib/exe/fetch.php?media=technical_indicators:bollinger_band_perce:bbpb-1-aaplwalk.png)  

```
After identifying a bigger uptrend, %B can be considered oversold when it moves to zero or below. 
Remember, %B moves to zero when price hits the lower band and below zero when price moves below the lower band. 
This represents a move that is 2 standard deviations below the 20-day moving average. 
Chart 2 shows the Nasdaq 100 ETF (QQQQ) within an uptrend that began in March 2009. 
%B moved below zero three times during this uptrend. 
The oversold readings in early July and early November provided good entry points to partake in the bigger uptrend (green arrows). 
```
![alt tag](https://school.stockcharts.com/lib/exe/fetch.php?media=technical_indicators:bollinger_band_perce:bbpb-2-qqqqup.png)  

## Signals: Trend Identification  
```
John Bollinger described a trend-following system using %B with the Money Flow Index (MFI). 
An uptrend begins when %B is above .80 and MFI(10) is above 80. MFI is bound between zero and one hundred. 
A move above 80 places MFI(10) in the upper 20% of its range, which is a strong reading. 
Downtrends are identified when %B is below .20 and MFI(10) is below 20. 
```
![alt tag](https://school.stockcharts.com/lib/exe/fetch.php?media=technical_indicators:bollinger_band_perce:bbpb-3-fdxmfi.png)  

[[教學] - 布林通道與波動率@ 交易者的E甸園 Jul 16, 2013](https://ebigmoney.pixnet.net/blog/post/152356080-%5B%E6%95%99%E5%AD%B8%5D---%E5%B8%83%E6%9E%97%E9%80%9A%E9%81%93%E8%88%87%E6%B3%A2%E5%8B%95%E7%8E%87)
```
因此根據%B是價格處於帶狀的位置所形成的指標
我們就可以知道
如果是正式突破帶寬的多頭%B就會大於0.8
而正式跌破帶寬的空頭%B就會小於0.2
這時候只要將關鍵的0.8和0.2的位置標注出來
當布林通道經過盤整壓縮整理並進行突破
```
![alt tag](http://3.bp.blogspot.com/-vzt8JJNQSc8/UeVzqEGJ81I/AAAAAAAAGt8/B3AoV6wuPYo/s320/5349-%2525B.gif)  


[布林通道](http://note-barsine.blogspot.com/2017/06/blog-post.html)  
```
正負一個標準差所涵蓋的機率約68%，
正負兩個標準差則高達95.4%，
也就是股價的變化要超出正負兩個標準差外，機率而言並不容易，
所以一旦超出就可以提供投資人寶貴的參考訊號。
```
![alt tag](https://1.bp.blogspot.com/-7umMgug2FsE/WSe26tn9c6I/AAAAAAAAOq4/IX_utlD8C0E5VG0WmtWXUNvWafTUcucHgCPcB/s640/x80c.jpg)  


[布林通道參數設定與%b Dec 16, 2016](https://bfhopeangel.pixnet.net/blog/post/189274248-%E5%B8%83%E6%9E%97%E9%80%9A%E9%81%93%E5%8F%83%E6%95%B8%E8%A8%AD%E5%AE%9A%E8%88%87%25b)  

# Reference
* [Bollinger Bands Backtest using Python and REST API | Part 1 November 22, 2018](https://www.quantnews.com/bollinger-bands-backtest-using-python-rest-api-part-1/)  
[fxcm/RestAPI](https://github.com/fxcm/RestAPI) 

```
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