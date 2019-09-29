# Take notes of pandas releated stuffs

# Table of Contents
[Setting up a Bollinger Band with Python](#setting-up-a-bollinger-band-with-python)  

[How to compute and plot Bollinger Bands® in Python](#how-to-compute-and-plot-bollinger-bands-in-python)  

[Trading: Calculate Technical Analysis Indicators with Pandas](#trading-calculate-technical-analysis-indicators-with-pandas)  
[Prerequisite environment setup](#prerequisite-environment-setup)  
[Data:](#data)  
[Code:](#code)  

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