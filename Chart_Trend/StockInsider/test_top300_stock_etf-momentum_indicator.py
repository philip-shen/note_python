'''
ChatGPTに教わりながら株式投資の指標を作ってみた
株価    投資    株式投資    ChatGPT
Last updated at 2024-06-26Posted at 2024-06-26
https://qiita.com/takurot/items/03b03de1c81f4e231da6
'''
'''
財務指標フィルタリング条件
    PBRが0.6〜1.0くらいでいい感じに成長余地があるもの
    増収増益している
    営業キャッシュフローがプラス

ひとまずこの辺で銘柄を絞ってから時系列のグラフを作成して
    半年間の株価が右肩上がり
    RSIが0.3近傍
'''
import os, sys, time
import pandas as pd
import yfinance as yf
import warnings
# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import matplotlib.pyplot as plt
from arch import arch_model
import argparse
import pathlib
import requests
from requests.exceptions import Timeout
from io import StringIO
import json, re, pickle
#from datetime import datetime, date, timedelta

from insider import StockInsider

import twseotc_stocks.lib_misc as lib_misc
from insider.logger_setup import *
from insider.stock import *
import gspreadsheet.googleSS as googleSS
import gspreadsheet.yahooFinance as yahooFinance

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.'.format( time_consumption)#msg = 'Time duration: {:.3f} seconds.'
    logger.info(msg)

# Change the date
#############################################
def date_changer( date):
    
    year = date[:4]
    year = str(int(year)-1911)
    month = date[4:6]
    day = date[6:]
        
    return year+"/"+month+"/"+day
'''
INFO: df_twse_stock_idx:
        證券代號      證券名稱        成交股數    成交筆數           成交金額     開盤價     最高價     最低價     收盤價 漲跌(+/-)  漲跌價差  最後揭示買價 最後揭示買量  最後揭示賣價 最後揭示賣量     本益比  Unnamed: 16
0      0050    元大台灣50  14,525,195  14,649  2,671,260,519  185.00  185.10  182.70  184.00       +  3.15  184.00     18  184.05      7    0.00          NaN
39005  9958       世紀鋼   4,060,753   3,220    898,422,458  220.00  224.00  219.00  220.50       +  1.00  220.50     28  221.00      2   31.86          NaN

INFO: df_tpex_stock_idx:
            代號        名稱    收盤       漲跌    開盤     最高      最低    均價        成交股數          成交金額(元)   成交筆數    最後買價  最後買量(千股)   最後賣價  最後賣量(千股)          發行股數   次日參考價    次日漲停價   次日跌停價
12139    9950       萬國通  15.55   +0.25  15.30  15.60  15.30  15.49       96,553      1,495,521      55  15.55         8  15.60         6    167,716,000   15.55    17.10  14.00
12140    9951        皇田  70.60   +0.70  70.70  70.90  70.40  70.56       53,350      3,764,360      62  70.50         4  70.70         1     74,900,000   70.60    77.60  63.60
            
'''
### waste 3~4 sec to request so move main routine
def requests_twse_tpex_stock_idx(json_data):
    ##### 上市公司
    datestr = json_data["lastest_datastr_twse_tpex"][2]#'20240801'
    r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
    # 整理資料，變成表格
    df_twse_website_info = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
        
    ##### 上櫃公司
    datestr = date_changer(json_data["lastest_datastr_twse_tpex"][2])#'113/08/01'
    r = requests.post('http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=' + datestr + '&s=0,asc,0')
    # 整理資料，變成表格    
    df_tpex_website_info = pd.read_csv(StringIO(r.text), header=2).dropna(how='all', axis=1).dropna(how='any')
        
    logger.info("Request TWSE and TPEX Stock index..")
    
    return [df_twse_website_info, df_tpex_website_info]

def store_twse_tpex_ticker(json_data, path_pickle_stock_id: list, path_csv_stock_id= '', opt_verbose= 'OFF'):
    
    list_df_twse_tpex_stock_idx = requests_twse_tpex_stock_idx(json_data)
    
    df_twse_stock_idx = list_df_twse_tpex_stock_idx[0]
    df_tpex_stock_idx = list_df_twse_tpex_stock_idx[1]
    
    if opt_verbose.lower() == 'on':
        logger.info(f'df_twse_stock_idx:\n {df_twse_stock_idx}' )    
        logger.info(f'df_tpex_stock_idx:\n {df_tpex_stock_idx}' )
        
    df_twse_ticker = df_twse_stock_idx[['證券代號', '證券名稱' ]]
    df_twse_ticker['證券代號'] = df_twse_stock_idx['證券代號'].copy()+'.TW'
    # Rename multiple columns
    df_twse_ticker = df_twse_ticker.rename(columns={
                                    '證券代號': 'ticker',
                                    '證券名稱': 'cpn_name',
                                    })
    
    df_tpex_ticker = df_tpex_stock_idx[['代號', '名稱' ]]
    df_tpex_ticker['代號'] = df_tpex_stock_idx['代號'].copy()+'.TWO'
    df_tpex_ticker = df_tpex_ticker.rename(columns={
                                    '代號': 'ticker',
                                    '名稱': 'cpn_name',
                                    })
    
    df_twse_tpex_ticker = pd.concat([df_twse_ticker, df_tpex_ticker], ignore_index=True)    
    
    if opt_verbose.lower() == 'on':
        logger.info(f'df_twse_ticker:\n {df_twse_ticker}' )    
        logger.info(f'df_tpex_ticker:\n {df_tpex_ticker}' )
        logger.info(f'df_twse_tpex_ticker:\n {df_twse_tpex_ticker}')

    if path_csv_stock_id != "":
        df_twse_tpex_ticker.to_csv(path_csv_stock_id, index=False) 
    
    dict_data= dict(zip(df_twse_ticker.ticker, df_twse_ticker.cpn_name))
    
    if opt_verbose.lower() == 'on':
        for key, value in dict_data.items():
            logger.info('\n key: {}; value: {}'.format(key, value) )
    
    # save dictionary to pickle file
    with open(path_pickle_stock_id[0], 'wb') as file:
        pickle.dump(dict_data, file, protocol=pickle.HIGHEST_PROTOCOL)
        #pickle.dump(list_twse_data, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    dict_data= dict(zip(df_tpex_ticker.ticker, df_tpex_ticker.cpn_name))
    with open(path_pickle_stock_id[1], 'wb') as file:
        pickle.dump(dict_data, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    dict_data= dict(zip(df_twse_tpex_ticker.ticker, df_twse_tpex_ticker.cpn_name))
    with open(path_pickle_stock_id[-1], 'wb') as file:
        pickle.dump(dict_data, file, protocol=pickle.HIGHEST_PROTOCOL)
'''
台股權值100大排行榜
https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm?MSCI=0

臺灣證券交易所發行量加權股價指數成分股暨市值比重
https://www.taifex.com.tw/cht/2/weightedPropertion
'''    
'''
INFO: 1th key: 2330.TW; value: 2330台積電 weight_ration_value: 0.3673
INFO: 2th key: 2317.TW; value: 2317鴻海 weight_ration_value: 0.0383
INFO: 3th key: 2454.TW; value: 2454聯發科 weight_ration_value: 0.0277
INFO: 4th key: 2881.TW; value: 2881富邦金 weight_ration_value: 0.0172
INFO: 5th key: 2382.TW; value: 2382廣達 weight_ration_value: 0.0147

INFO: 297th key: 6451.TW; value: 6451訊芯-KY weight_ration_value: 0.000315
INFO: 298th key: 3013.TW; value: 3013晟銘電 weight_ration_value: 0.000312
INFO: 299th key: 9938.TW; value: 9938百和 weight_ration_value: 0.000308
INFO: 300th key: 8028.TW; value: 8028昇陽半導體 weight_ration_value: 0.000307
'''
def store_twse_tpex_ticker_weight_ration_fromCSV(json_data, path_pickle_stock_id: dict, path_csv_stock_id= '', opt_verbose= 'OFF'):
    
    df_twse_tpex_us_stock_idx = pd.read_csv(json_data["lastest_datastr_twse_tpex"][3], sep=',', lineterminator='\r')
    df_twse_stock_idx = pd; df_tpex_stock_idx = pd; df_us_stock_idx = pd
    #if opt_verbose.lower() == 'on':
    #        logger.info(f'df_twse_tpex_stock_idx:\n {df_twse_tpex_us_stock_idx}' )    
        
    if bool(re.match('^twse', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
        pickle_fname_ticker_weight_ration = path_pickle_stock_id["twse"][1]#'twse_ticker_weight_ration.pickle'
        df_twse_stock_idx = df_twse_tpex_us_stock_idx
            
        df_twse_ticker = df_twse_stock_idx[['stk_idx', 'cpn_name', 'percent_twse']]
        df_twse_ticker['ticker'] = df_twse_stock_idx['stk_idx'].astype(str).replace("'", "").copy()+'.TW'
        
        if opt_verbose.lower() == 'on':
            logger.info(f'df_twse_stock_idx:\n {df_twse_stock_idx}' )    
        
        dict_data_twse_ticker_cpn_name= dict(zip(df_twse_ticker.ticker, df_twse_ticker.cpn_name))
        dict_data_twse_ticker_weight_ration= dict(zip(df_twse_ticker.ticker, df_twse_ticker.percent_twse))
        
        if opt_verbose.lower() == 'on':
            num = 0
            for key, value in dict_data_twse_ticker_cpn_name.items():
                num+=1
                logger.info('{}th key: {}; value: {} weight_ration_value: {}'.format(num, key, value, dict_data_twse_ticker_weight_ration[key]) )

        # save dictionary to pickle file
        #with open(path_pickle_stock_id[0], 'wb') as file:
        with open(path_pickle_stock_id["twse"][0], 'wb') as file:
            pickle.dump(dict_data_twse_ticker_cpn_name, file, protocol=pickle.HIGHEST_PROTOCOL)
        
        with open(pickle_fname_ticker_weight_ration, 'wb') as file:
            pickle.dump(dict_data_twse_ticker_weight_ration, file, protocol=pickle.HIGHEST_PROTOCOL)
                    
    elif bool(re.match('^tpex', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
        pickle_fname_ticker_weight_ration = path_pickle_stock_id["tpex"][1]#'tpex_ticker_weight_ration.pickle'        
        df_tpex_stock_idx = df_twse_tpex_us_stock_idx

        df_tpex_ticker = df_tpex_stock_idx[['stk_idx', 'cpn_name', 'percent_tpex' ]]
        df_tpex_ticker['ticker'] = df_tpex_stock_idx['stk_idx'].astype(str).copy()+'.TWO'
        
        if opt_verbose.lower() == 'on':
            logger.info(f'df_tpex_stock_idx:\n {df_tpex_stock_idx}' )
            
        dict_data_tpex_ticker_cpn_name= dict(zip(df_tpex_ticker.ticker, df_tpex_ticker.cpn_name))
        dict_data_tpex_ticker_weight_ration= dict(zip(df_tpex_ticker.ticker, df_tpex_ticker.percent_tpex))
        
        #with open(path_pickle_stock_id[1], 'wb') as file:
        with open(path_pickle_stock_id["tpex"][0], 'wb') as file:
            pickle.dump(dict_data_tpex_ticker_cpn_name, file, protocol=pickle.HIGHEST_PROTOCOL)

        with open(pickle_fname_ticker_weight_ration, 'wb') as file:
            pickle.dump(dict_data_tpex_ticker_weight_ration, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    else:
        df_us_stock_idx = df_twse_tpex_us_stock_idx
        
        df_us_ticker = df_us_stock_idx[['stk_idx', 'cpn_name', 'percent_us' ]]
        df_us_ticker['ticker'] = df_us_stock_idx['stk_idx'].astype(str).copy()
        
        if opt_verbose.lower() == 'on':
            logger.info(f'df_us_stock_idx:\n {df_us_stock_idx}' )
        
        dict_data_us_ticker_cpn_name= dict(zip(df_us_ticker.ticker, df_us_ticker.cpn_name))
        dict_data_us_ticker_weight_ration= dict(zip(df_us_ticker.ticker, df_us_ticker.percent_us))
        
        if opt_verbose.lower() == 'on':
            num = 0
            for key, value in dict_data_us_ticker_cpn_name.items():
                num+=1
                logger.info('{}th key: {}; value: {} weight_ration_value: {}'.format(num, key, value, dict_data_us_ticker_weight_ration[key]) )
                
        if bool(re.match('^sp500', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            pickle_fname_ticker = path_pickle_stock_id["sp500"][0]
            pickle_fname_ticker_weight_ration = path_pickle_stock_id["sp500"][1]
                
        elif bool(re.match('^nasdaq100', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            pickle_fname_ticker = path_pickle_stock_id["nasdaq100"][0]
            pickle_fname_ticker_weight_ration = path_pickle_stock_id["nasdaq100"][1]
            
        with open(pickle_fname_ticker, 'wb') as file:
            pickle.dump(dict_data_us_ticker_cpn_name, file, protocol=pickle.HIGHEST_PROTOCOL)    
        with open(pickle_fname_ticker_weight_ration, 'wb') as file:
            pickle.dump(dict_data_us_ticker_weight_ration, file, protocol=pickle.HIGHEST_PROTOCOL)
                    
    return pickle_fname_ticker_weight_ration

def query_dic_from_pickle(path_pickle_stock_id, opt_verbose= 'OFF'):
    with open(path_pickle_stock_id, "rb") as f:
        #with open("data/steady_growth.pickle", "rb") as f:
        #with open("data/ETF.pickle", "rb") as f:    
        TICKER_LIST = pickle.load(f)

    return TICKER_LIST

# データフレームを初期化
columns = ['Ticker', 'PBR', 'Revenue Growth', 'Profit Growth', 'ROE', 'PER', 'Volume', 'Operating Cash Flow']
data = []

def Indicators(tickers, opt_verbose='OFF'):
    
    # 各ティッカーについてデータを取得
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        financials = stock.financials
        cashflow = stock.cashflow
        history = stock.history(period="1y")  # 過去1年間のデータを取得

        # PBR、ROE、PERを取得
        pbr = info.get('priceToBook', None)
        roe = info.get('returnOnEquity', None)
        per = info.get('forwardPE', None)
            
        # 売上高と利益の成長率を計算
        try:
            revenue_growth = (financials.loc['Total Revenue'][0] - financials.loc['Total Revenue'][1]) / financials.loc['Total Revenue'][1]
            profit_growth = (financials.loc['Net Income'][0] - financials.loc['Net Income'][1]) / financials.loc['Net Income'][1]
            operating_cash_flow = cashflow.loc['Operating Cash Flow'][0]            
            average_volume = history['Volume'].mean()
        except:
            print(f'Error: {ticker}')
            continue
        
        if opt_verbose.lower() == 'on':
            logger.info(f'ticker: {ticker}')
            logger.info(f'pbr: {pbr}')
            logger.info(f'roe: {roe}')
            logger.info(f'per: {per}')
            logger.info(f'revenue_growth: {revenue_growth}')
            logger.info(f'profit_growth: {profit_growth}')
            logger.info(f'operating_cash_flow: {operating_cash_flow}')
            logger.info(f'average_volume: {average_volume}\n')
                
        # PBRが1以下で、増収増益している企業をフィルタリング
        if pbr is not None and pbr < 1.0 and pbr > 0.6 \
            and revenue_growth > 0 and profit_growth > 0 \
            and per is not None and per > 0 and operating_cash_flow > 0:
            data.append([ticker, pbr, revenue_growth, profit_growth, roe, per, average_volume, operating_cash_flow])

    # データフレームに変換
    df = pd.DataFrame(data, columns=columns)

    # フィルタリングされたティッカーのみを配列として抽出
    tickers = df['Ticker'].tolist()
    # 営業キャッシュフローの大きい順にソート
    df = df.sort_values(by='Operating Cash Flow', ascending=False)
    
    return df

'''
Beginning Indicators for charting
https://www.reddit.com/r/RobinHood/comments/p4huvr/beginning_indicators_for_charting/

RSI (Relative Strength Index): 
Relative Strength Index measures whether a stock is being overbought or oversold. 
Lower RSI indicates people have sold more and that you could be looking for an increase in buying. 
Two points to watch are when RSI is close to 70, meaning it’s moving towards overbought, and 30, meaning it’s oversold.

MACD (Moving Average Convergence/Divergence): 
MACD helps show the price movement, moving average on a shorter period versus a longer period. 
Tradingview shows a shorter exponential moving average as blue with the signal line, the longer exponential moving average, as red. 
The short EMA will always meet the long EMA but it helps determine possible uptrends or downtrends when the blue line crosses the red line. 
Crossing downward is bearish and upward is the opposite. MACD can contain gold and death crosses. 
Gold Cross has the blue line shoot up through the red line, creating a cross and a bullish indicator. Death Cross has the blue line drop through the red line, a bearish signal.

MFI (Money Flow Index): 
Money Flow Index is similar to RSI in that it can also help determine overbought or oversold areas with usual indicators at 80 and 20, similar indications to RSI. 
Using MFI with RSI can help spot divergences. If RSI and the stock go up, but MFI is down, this can signal a reversal in price.

ADL (Advance/Decline Line): 
ADL helps determine the amount of shares being bought or sold, a positive number showing more bullish indication and negative showing bearish. 
Spikes in ADL can show possible artificial breakout without justification in price movement. 
A great example below, we see a spike in ADL but not much of an increase in price, so shows possible fake breakout and artificial increase in truly advancing stocks.

Bollinger Bands: 
Bollinger Bands help identify when a stock might be trading outside their price range. 
Bollinger Bands are usually set at 2 standard deviations away from the price, as statistically, 2stdev is considered an outlier. 
This can help identify a breakout from its trading range or retest the Bollinger Bands and come back inside it’s range.

VWAP (Volume Weighted Average Price): 
“If Volume is king, VWAP is queen” VWAP, recommended by shorter time frames, is the average price the stock is trading at, taking volume into account. 
If a stock is trading above VWAP, you can most likely expect it to come down to the average price, tending towards equilibrium as economics rule #1. 
Overall, it’s important to use multiple indicators as they can tell different stories, and using them on multiple timelines can also help you determine what the short term and long term prospects.
'''    
# RSIを計算する関数
def calculate_RSI(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# MFIを計算する関数
def calculate_MFI(data, window=14):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    money_flow = typical_price * data['Volume']

    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)

    positive_mf = positive_flow.rolling(window=window, min_periods=1).sum()
    negative_mf = negative_flow.rolling(window=window, min_periods=1).sum()

    mfi = 100 - (100 / (1 + (positive_mf / negative_mf)))
    return mfi

# ボリンジャーバンドを計算する関数
def calculate_bollinger_bands(data, window=20):
    sma = data['Close'].rolling(window=window).mean()
    std = data['Close'].rolling(window=window).std()
    data['Bollinger Middle'] = sma
    data['Bollinger Upper'] = sma + (std * 2)
    data['Bollinger Lower'] = sma - (std * 2)
    return data

# 移動平均線を計算する関数
def calculate_moving_averages(data, weekly_window=5, Dweekly_window=10, \
                                monthly_window=20, quarterly_window=60):
    data['MA_5'] = data['Close'].rolling(window=weekly_window).mean()
    data['MA_10'] = data['Close'].rolling(window=Dweekly_window).mean()
    data['MA_20'] = data['Close'].rolling(window=monthly_window).mean()
    data['MA_60'] = data['Close'].rolling(window=quarterly_window).mean()
    return data

def calculate_volume_weighted_average_price(data):
    data['cum_volume'] = data['Volume'].cumsum()
    data['cum_volume_price'] = (data['Close'] * data['Volume']).cumsum()
    data = data['cum_volume_price'] / data['cum_volume']
    return data

def stand_Up_On_fall_Down_MAs(data):
    #logger.info("{}".format("Stand_Up_On_MAs (針對你Fetch data區間的最後一天做分析):"))

    # 抓出所需data
    stock_price = data['Close'].astype(float).iloc[-1]
    MA5 = data['MA_5'].iloc[-1] if not data['MA_5'].isnull().values.all() else 0
    MA10 = data['MA_10'].iloc[-1] if not data['MA_10'].isnull().values.all() else 0
    MA20 = data['MA_20'].iloc[-1] if not data['MA_20'].isnull().values.all() else 0
    MA60 = data['MA_60'].iloc[-1] if not data['MA_60'].isnull().values.all() else 0

    four_MAs = MA5 and MA10 and MA20 and MA60
    three_MAs = MA5 and MA10 and MA20
        
    four_flag = True if four_MAs and max(stock_price, MA5, MA10, MA20, MA60) == stock_price else False
    three_flag = True if three_MAs and max(stock_price, MA5, MA10, MA20) == stock_price else False
    four_dog = True if four_MAs and min(stock_price, MA5, MA10, MA20, MA60) == stock_price else False
    three_dog = True if three_MAs and min(stock_price, MA5, MA10, MA20) == stock_price else False 

    return four_flag, three_flag, four_MAs, three_MAs, four_dog, three_dog
    
                    
def stock_price_graph(tickers: list, start_date: str, end_date: str):
    # グラフのサイズを小さくして複数表示
    plt.figure(figsize=(tickers.__len__(), 60))
    plt.subplots_adjust(hspace=0.5)
    
    for i, ticker in enumerate(tickers):
        data = yf.download(ticker, start=start_date, end=end_date, interval="1d")

        if data.empty:
            continue

        # 必要な列を抽出
        data = data[['Close', 'Volume', 'High', 'Low']].copy()

        # VWAPを計算        
        data['VWAP'] = calculate_volume_weighted_average_price(data)

        # RSIを計算
        data['RSI'] = calculate_RSI(data)

        # MFIを計算
        data['MFI'] = calculate_MFI(data)

        # ボリンジャーバンドを計算
        data = calculate_bollinger_bands(data)

        # 移動平均線を計算
        data = calculate_moving_averages(data)

        # 日次リターンの計算
        returns = 100 * data['Close'].pct_change().dropna()

        # GARCHモデルの適用
        model = arch_model(returns, vol='Garch', p=1, q=1)
        model_fitted = model.fit(disp='off')

        # サブプロットを設定
        ax1 = plt.subplot(len(tickers), 2, i * 2 + 1)
        ax2 = plt.subplot(len(tickers), 2, i * 2 + 2)

        # 終値、VWAP、ボリンジャーバンド、移動平均線のプロット
        ax1.plot(data.index, data['Close'], label='Close Price')
        ax1.plot(data.index, data['VWAP'], label='VWAP', linestyle='--')
        #ax1.plot(data.index, data['Bollinger Middle'], label='Bollinger Middle', linestyle='--')
        #ax1.plot(data.index, data['Bollinger Upper'], label='Bollinger Upper', linestyle='--')
        #ax1.plot(data.index, data['Bollinger Lower'], label='Bollinger Lower', linestyle='--')
        #ax1.set_title(f'{ticker} - Close Price, VWAP, Bollinger Bands & Moving Averages')
        
        ax1.plot(data.index, data['MA_5'], label='5-Day MA', linestyle='-', color='blue')
        ax1.plot(data.index, data['MA_20'], label='20-Day MA', linestyle='-', color='red')
        #ax1.plot(data.index, data['MA_10'], label='10-Day MA', linestyle='-', color='yellow')
        ax1.plot(data.index, data['MA_60'], label='60-Day MA', linestyle='-', color='brown') 
        ax1.set_title(f'{ticker} - Close Price, VWAP, Moving Averages')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)

        # ゴールデンクロスのプロット
        golden_cross = data[(data['MA_5'] > data['MA_20']) & (data['MA_5'].shift(1) <= data['MA_20'].shift(1))]
        ax1.plot(golden_cross.index, data.loc[golden_cross.index, 'MA_5'], '*', markersize=10, label='Golden Cross', color='gold')

        # RSIとMFIのプロット
        ax2.plot(data.index, data['RSI'], label='RSI', color='orange')
        ax2.plot(data.index, data['MFI'], label='MFI', color='purple')
        ax2.axhline(70, color='red', linestyle='--')
        ax2.axhline(30, color='green', linestyle='--')
        ax2.set_title(f'{ticker} - RSI & MFI')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Indicator Value')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)

        #data.to_csv(f'{dirnamelog}/{ticker}_indicators.csv', index=False)
        stand_Up_On_fall_Down_MAs(data)
        
    plt.show()

def check_MAs_status(data, opt_verbose='OFF'):
    # 必要な列を抽出
    data = data[['Close', 'Volume', 'High', 'Low']].copy()
        
    # 移動平均線を計算
    data = calculate_moving_averages(data)
    #logger.info(f'data_moving_averages:\n {data}' )    
        
    four_flag, three_flag, four_MAs, three_MAs, four_dog, three_dog = stand_Up_On_fall_Down_MAs(data) 
    
    if opt_verbose.lower() == 'on':
        # 判斷data值
        if four_flag:
            logger.info("股價已站上5日、10日、20日、60日均線均線，為四海遊龍型股票!!")
        elif three_flag:
            logger.info("股價已站上5日、10日、20日均線，為三陽開泰型股票!!")
        #elif not four_MAs:
        #    logger.info("目前的data數量不足以畫出四條均線，請補足後再用此演算法!!")
        #elif not three_MAs:
        #    logger.info("目前的data數量不足以畫出三條均線，請補足後再用此演算法!!")
        else:
            logger.info("目前股價尚未成三陽開泰型、四海遊龍型股票!!")
    
    close_price = data['Close'].astype(float).iloc[-1]
        
    return four_flag, three_flag, four_MAs, three_MAs, close_price, four_dog, three_dog

def store_TWSE_MAs_status(json_data: dict, twse_ticker: pd, twse_stock_data: pd, opt_verbose='OFF'):
    list_twse_MAs_status = []
    start_date = date_changer_twse(json_data["start_end_date"][0])
    end_date = date_changer_twse_yfinance_end_date(json_data["start_end_date"][1])

    for i, ticker in enumerate(twse_ticker.to_list()):
        
        ##### 上市公司 or ETF or 正2 ETF
        if bool(re.match('^[0-9][0-9][0-9][0-9].TW$', ticker)) or \
            bool(re.match('^00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('^00[0-9][0-9][0-9]L.TW$', ticker))  :
            target_ticker = ticker
        else:
            target_ticker = None
        
        if target_ticker != None:
            if opt_verbose.lower() == 'on':
                logger.info(f"ticker: {target_ticker}; stock name: {twse_stock_data['證券名稱'][i]}")    
                
            #yf_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
            #four_flag, three_flag, four_MAs, three_MAs, close, four_dog, three_dog = check_MAs_status(yf_data, opt_verbose='OFF')            
            
            local_stock_indicator = stock_indicator(ticker=target_ticker)
            local_stock_indicator.check_MAs_status()            
            local_stock_indicator.filter_MAs_status()
            
            dict_temp = {
                "ticker" : target_ticker,
                "stock_name": twse_stock_data['證券名稱'][i],
                "4_flag": local_stock_indicator.four_flag,
                "3_flag": local_stock_indicator.three_flag,
                "2_flag": local_stock_indicator.two_flag,
                "1_flag": local_stock_indicator.one_flag,
                
                "Expo_4_flag": local_stock_indicator.four_E_flag,
                "Expo_3_flag": local_stock_indicator.three_E_flag,
                "Expo_2_flag": local_stock_indicator.two_E_flag,
                "Expo_1_flag": local_stock_indicator.one_E_flag,
                
                "close": local_stock_indicator.close,
                "4_dog": local_stock_indicator.four_dog,
                "3_dog": local_stock_indicator.three_dog,
            }
            list_twse_MAs_status.append(dict_temp)
    
    return list_twse_MAs_status

def store_TPEX_MAs_status(json_data: dict, tpex_ticker: pd, tpex_stock_data: pd, opt_verbose='OFF'):
    list_tpex_MAs_status = []
    start_date = date_changer_twse(json_data["start_end_date"][0])
    end_date = date_changer_twse_yfinance_end_date(json_data["start_end_date"][1])

    for i, ticker in enumerate(tpex_ticker.to_list()):
        
        ##### 上櫃公司
        if bool(re.match('^[0-9][0-9][0-9][0-9].TWO$', ticker)):
            target_ticker = ticker
        else:
            target_ticker = None

        if target_ticker != None:
            if opt_verbose.lower() == 'on':
                logger.info(f"ticker: {target_ticker}; stock name: {tpex_stock_data['名稱'][i]}")    
                
            #yf_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
            #four_flag, three_flag, four_MAs, three_MAs, close, four_dog, three_dog = check_MAs_status(yf_data, opt_verbose='OFF')            
            
            local_stock_indicator = stock_indicator(ticker=target_ticker)
            local_stock_indicator.check_MAs_status()            
            local_stock_indicator.filter_MAs_status()
            
            dict_temp = {
                "ticker" : target_ticker,
                "stock_name": tpex_stock_data['名稱'][i],
                "4_flag": local_stock_indicator.four_flag,
                "3_flag": local_stock_indicator.three_flag,
                "2_flag": local_stock_indicator.two_flag,
                "1_flag": local_stock_indicator.one_flag,
                
                "Expo_4_flag": local_stock_indicator.four_E_flag,
                "Expo_3_flag": local_stock_indicator.three_E_flag,
                "Expo_2_flag": local_stock_indicator.two_E_flag,
                "Expo_1_flag": local_stock_indicator.one_E_flag,
                
                "close": local_stock_indicator.close,
                "4_dog": local_stock_indicator.four_dog,
                "3_dog": local_stock_indicator.three_dog,
            }
            list_tpex_MAs_status.append(dict_temp)
            
    return list_tpex_MAs_status

class TWSE_TPEX_MAs_status():
    def __init__(self, json_data: dict, json_gsheet_cert: dict, path_pickle_ticker: dict, list_path_pickle_ticker: list, pt_stock, opt_verbose='OFF'):
        
        self.json_data = json_data
        self.json_gsheet_cert = json_gsheet_cert
        self.dict_path_pickle_ticker = path_pickle_ticker
        self.list_path_pickle_ticker = list_path_pickle_ticker
        self.pt_stock = pt_stock
        self.opt_verbose = opt_verbose
        
    def store_TWSE_TPEX_MAs_status(self, start_date, end_date):
        list_MAs_status = []
        
        for ticker, cpn_name in self.dict_twse_tpex_ticker_cpn_name.items():
            #logger.info('\n ticker: {}; cpn_name: {}'.format(key, value) )    
            ##### 上市公司 or ETF or 正2 ETF
            #if bool(re.match('^[0-9][0-9][0-9][0-9].TW$', ticker)) or \
            #    bool(re.match('^00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('^00[0-9][0-9][0-9]L.TW$', ticker)):
            if bool(re.match('[0-9][0-9][0-9][0-9].TW$', ticker)) or \
                bool(re.match('00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('00[0-9][0-9][0-9]L.TW$', ticker)):
                target_ticker = ticker        
                stock_name = cpn_name
        
            ##### 上櫃公司
            elif bool(re.match('^[0-9][0-9][0-9][0-9].TWO$', ticker)):
                target_ticker = ticker    
                stock_name = cpn_name
            else:
                target_ticker = None 
        
            if target_ticker != None:
                
                '''
                ERROR: ['1457.TW']: Exception('%ticker%: No price data found, symbol may be delisted (1d 2024-01-01 -> 2024-07-26)')
                ERROR: ['2442.TW']: Exception('%ticker%: No price data found, symbol may be delisted (1d 2024-01-01 -> 2024-07-26)')
                ERROR: ['5383.TWO']: Exception('%ticker%: No timezone found, symbol may be delisted')
                ERROR: ['00940.TW']: Exception("%ticker%: Data doesn't exist for startDate = 1701360000, endDate = 1711900800")       
                ERROR: ['3536.TW']: Exception('%ticker%: No timezone found, symbol may be delisted')    
                ERROR: ['3682.TW']: Exception('%ticker%: No timezone found, symbol may be delisted')    
                ERROR: ['8480.TW']: Exception('%ticker%: No timezone found, symbol may be delisted') 
                '''
                if bool(re.match('^0000.TW$', ticker) or re.match('^0000.TW$', ticker) or re.match('^0000.TW$', ticker)  or \
                        re.match('^0000.TW$', ticker) or re.match('^0000.TW$', ticker) or re.match('^0000.TW$', ticker)):
                    continue 
                
                logger.info(f"ticker: {target_ticker}; stock name: {cpn_name}")    
                                 
                #yf_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
                #four_flag, three_flag, four_MAs, three_MAs, close, four_dog, three_dog = check_MAs_status(yf_data, opt_verbose='OFF')            
            
                local_stock_indicator = stock_indicator_pstock(ticker=target_ticker,  period="3mo", interval="1d", \
                                                                startdate= start_date, enddate= end_date, opt_verbose=self.opt_verbose)
                
                if self.json_data["lastest_datastr_twse_tpex"][0].lower() == "start_end_date":                    
                    #2025/2/24 remark cause Error 429 too many request
                    #local_stock_indicator.pstock_interval_startdate_enddate()
                    local_stock_indicator.yfinance_asyncio_interval_startdate_enddate()
                else:
                    local_stock_indicator.pstock_interval_period()
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'local_stock_indicator.stock_data: \n{local_stock_indicator.stock_data}')
                
                local_stock_indicator.check_MAs_status()            
                local_stock_indicator.filter_MAs_status()
            
                dict_temp = {
                    "ticker" : target_ticker,
                    "stock_name": stock_name,
                    "weight": float(self.dict_twse_tpex_ticker_weight_ration[target_ticker]),
                    "4_flag": local_stock_indicator.four_flag,
                    "3_flag": local_stock_indicator.three_flag,
                    "2_flag": local_stock_indicator.two_flag,
                    "1_flag": local_stock_indicator.one_flag,
                
                    "Expo_4_flag": local_stock_indicator.four_E_flag,
                    "Expo_3_flag": local_stock_indicator.three_E_flag,
                    "Expo_2_flag": local_stock_indicator.two_E_flag,
                    "Expo_1_flag": local_stock_indicator.one_E_flag,
                
                    "4_dog": local_stock_indicator.four_dog,
                    "3_dog": local_stock_indicator.three_dog,
                    "2_dog": local_stock_indicator.two_dog,
                    "1_dog": local_stock_indicator.one_dog,
                    
                    "Expo_4_dog": local_stock_indicator.four_E_dog,
                    "Expo_3_dog": local_stock_indicator.three_E_dog,
                    "Expo_2_dog": local_stock_indicator.two_E_dog,
                    "Expo_1_dog": local_stock_indicator.one_E_dog,
                    
                    "open": local_stock_indicator.open,
                    "close": local_stock_indicator.close,
                    "high": local_stock_indicator.high,
                    "low": local_stock_indicator.low,
                    "prev_day_close": local_stock_indicator.prev_day_close,
                    "MAs_status": local_stock_indicator.stock_MA_status,
                }
                list_MAs_status.append(dict_temp)
                
                #logger.info(f'dict_temp: {dict_temp}')
        self.TWSE_TPEX_MAs_status = list_MAs_status

    def store_dict_MAs_status(self, start_date, end_date, stock_end_date):
        list_MAs_status = []
        target_ticker = None 
        
        for ticker, cpn_name in self.dict_ticker_cpn_name.items():
            #logger.info('\n ticker: {}; cpn_name: {}'.format(key, value) )    
            ##### 上市公司 or ETF or 正2 ETF
            #if bool(re.match('^[0-9][0-9][0-9][0-9].TW$', ticker)) or \
            #    bool(re.match('^00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('^00[0-9][0-9][0-9]L.TW$', ticker)):
            if bool(re.match('[0-9][0-9][0-9][0-9].TW$', ticker)) or \
                bool(re.match('00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('00[0-9][0-9][0-9]L.TW$', ticker)):
                target_ticker = ticker        
                stock_name = cpn_name
            
            ##### 上櫃公司
            elif bool(re.match('^[0-9][0-9][0-9][0-9].TWO$', ticker)):
                target_ticker = ticker    
                stock_name = cpn_name
            
            ##### US market
            else:
                target_ticker = ticker    
                stock_name = cpn_name 
        
            if target_ticker != None:
                
                if bool(re.match('^0000.TW$', ticker) or re.match('^0000.TW$', ticker) or re.match('^0000.TW$', ticker)  or \
                        re.match('^0000.TW$', ticker) or re.match('^0000.TW$', ticker) or re.match('^0000.TW$', ticker)):
                    continue 
                
                logger.info(f"ticker: {target_ticker}; stock name: {cpn_name}")    
                
                local_stock_indicator = stock_indicator_pstock(ticker=target_ticker,  period="3mo", interval="1d", \
                                                                startdate= start_date, enddate= end_date, opt_verbose=self.opt_verbose)
                
                if self.json_data["lastest_datastr_twse_tpex"][0].lower() == "start_end_date":                    
                    #2025/2/24 remark cause Error 429 too many request
                    #local_stock_indicator.pstock_interval_startdate_enddate()
                    local_stock_indicator.yfinance_asyncio_interval_startdate_enddate()
                else:
                    local_stock_indicator.pstock_interval_period()
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'local_stock_indicator.stock_data: \n{local_stock_indicator.stock_data}')
                
                local_stock_indicator.check_MAs_status()            
                local_stock_indicator.filter_MAs_status()
                
                dict_temp = {
                    "ticker" : target_ticker,
                    "stock_name": stock_name,
                    "weight": float(self.dict_ticker_weight_ration[target_ticker]),
                    "4_flag": local_stock_indicator.four_flag,
                    "3_flag": local_stock_indicator.three_flag,
                    "2_flag": local_stock_indicator.two_flag,
                    "1_flag": local_stock_indicator.one_flag,
                
                    "Expo_4_flag": local_stock_indicator.four_E_flag,
                    "Expo_3_flag": local_stock_indicator.three_E_flag,
                    "Expo_2_flag": local_stock_indicator.two_E_flag,
                    "Expo_1_flag": local_stock_indicator.one_E_flag,
                
                    "4_dog": local_stock_indicator.four_dog,
                    "3_dog": local_stock_indicator.three_dog,
                    "2_dog": local_stock_indicator.two_dog,
                    "1_dog": local_stock_indicator.one_dog,
                    
                    "Expo_4_dog": local_stock_indicator.four_E_dog,
                    "Expo_3_dog": local_stock_indicator.three_E_dog,
                    "Expo_2_dog": local_stock_indicator.two_E_dog,
                    "Expo_1_dog": local_stock_indicator.one_E_dog,
                    
                    "open": local_stock_indicator.open,
                    "close": local_stock_indicator.close,
                    "high": local_stock_indicator.high,
                    "low": local_stock_indicator.low,
                    "prev_day_close": local_stock_indicator.prev_day_close,
                    "MAs_status": local_stock_indicator.stock_MA_status,
                    "End_Date": str(stock_end_date)
                }
                list_MAs_status.append(dict_temp)
                
                #logger.info(f'dict_temp: {dict_temp}')
        self.dict_MAs_status = list_MAs_status
        
    def store_dict_ShortMediumTerm_trend(self, start_date, end_date):
        list_ShortMediumTerm_trend = []
        target_ticker = None 
        
        for ticker, cpn_name in self.dict_ticker_cpn_name.items():
            #logger.info('\n ticker: {}; cpn_name: {}'.format(key, value) )    
            ##### 上市公司 or ETF or 正2 ETF
            #if bool(re.match('^[0-9][0-9][0-9][0-9].TW$', ticker)) or \
            #    bool(re.match('^00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('^00[0-9][0-9][0-9]L.TW$', ticker)):
            if bool(re.match('[0-9][0-9][0-9][0-9].TW$', ticker)) or \
                bool(re.match('00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('00[0-9][0-9][0-9]L.TW$', ticker)):
                target_ticker = ticker        
                stock_name = cpn_name
            
            ##### 上櫃公司
            elif bool(re.match('^[0-9][0-9][0-9][0-9].TWO$', ticker)):
                target_ticker = ticker    
                stock_name = cpn_name
            
            ##### US market
            else:
                target_ticker = ticker    
                stock_name = cpn_name 
        
            if target_ticker != None:
                
                logger.info(f"ticker: {target_ticker}; stock name: {cpn_name}")    
                local_stock_indicator = stock_indicator_pstock(ticker=target_ticker,  period="3mo", interval="1d", \
                                                                startdate= start_date, enddate= end_date, opt_verbose=self.opt_verbose)
                
                if self.json_data["lastest_datastr_twse_tpex"][0].lower() == "start_end_date":                    
                    #2025/2/24 remark cause Error 429 too many request
                    #local_stock_indicator.pstock_interval_startdate_enddate()
                    local_stock_indicator.yfinance_asyncio_interval_startdate_enddate()
                else:
                    local_stock_indicator.pstock_interval_period()                
                
                #if self.opt_verbose.lower() == 'on':
                #    logger.info(f'local_stock_indicator.stock_data: \n{local_stock_indicator.stock_data}')
                local_stock_indicator.adjust_price_StockDividend(list_ticker=[target_ticker.split('.')[0]])
                    
                local_stock_indicator.check_ShortMediumTerm_MAs()
                local_stock_indicator.filter_ShortMediumTerm_MAs()                
                local_stock_indicator.calculate_bollinger_bands()
                local_stock_indicator.calculate_RSI()
                local_stock_indicator.calculate_MACD()
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'local_stock_indicator.stock_data: \n{local_stock_indicator.stock_data}')
                    
                dict_temp = {
                    "ticker" : target_ticker,
                    "stock_name": stock_name,
                    "weight": float(self.dict_ticker_weight_ration[target_ticker]),
                    "MA_3days": local_stock_indicator.stock_data['MA_3'].astype(float).iloc[-1],
                    "MA_5days": local_stock_indicator.stock_data['MA_5'].astype(float).iloc[-1],
                    "MA_7days": local_stock_indicator.stock_data['MA_7'].astype(float).iloc[-1],
                    "MA_13days": local_stock_indicator.stock_data['MA_13'].astype(float).iloc[-1],
                    "MA_28days": local_stock_indicator.stock_data['MA_28'].astype(float).iloc[-1],
                    "MA_84days": local_stock_indicator.stock_data['MA_84'].astype(float).iloc[-1],                    
                    "MA_10days": local_stock_indicator.stock_data['MA_10'].astype(float).iloc[-1],
                    "MA_20days": local_stock_indicator.stock_data['MA_20'].astype(float).iloc[-1],
                    "MA_60days": local_stock_indicator.stock_data['MA_60'].astype(float).iloc[-1],
                    
                    "BBband_Middle": local_stock_indicator.stock_data['Bollinger Middle'].astype(float).iloc[-1],
                    "BBband_Upper": local_stock_indicator.stock_data['Bollinger Upper'].astype(float).iloc[-1],
                    "BBband_Lower": local_stock_indicator.stock_data['Bollinger Lower'].astype(float).iloc[-1],
                    "RSI": local_stock_indicator.stock_data['RSI'].astype(float).iloc[-1],
                    "MACD": local_stock_indicator.stock_data['MACD'].astype(float).iloc[-1],
                    "MACD_Signal": local_stock_indicator.stock_data['MACD Signal'].astype(float).iloc[-1],
                    "MACD_Histogram": local_stock_indicator.stock_data['MACD Histogram'].astype(float).iloc[-1],        
                    "ShortMediumTerm_trend_flag": local_stock_indicator.shortmediumTerm_trend_MA_status,
                    
                    "open": local_stock_indicator.open,
                    "close": local_stock_indicator.close,
                    "high": local_stock_indicator.high,
                    "low": local_stock_indicator.low,
                    "prev_day_close": local_stock_indicator.prev_day_close,
                    "volume": local_stock_indicator.volume, 
                    "volume_avg_weekly": local_stock_indicator.volume_avg_weekly, 
                }
                list_ShortMediumTerm_trend.append(dict_temp)
        
        self.dict_ShortMediumTerm_trend = list_ShortMediumTerm_trend
    
    def store_dict_MAs_status_ShortMediumTerm_trend(self, start_date, end_date, stock_end_date):
        list_MAs_status = []
        list_ShortMediumTerm_trend = []
        target_ticker = None 
        ith = 0
        
        for ticker, cpn_name in self.dict_ticker_cpn_name.items():
            #logger.info('\n ticker: {}; cpn_name: {}'.format(key, value) )    
            ##### 上市公司 or ETF or 正2 ETF
            #if bool(re.match('^[0-9][0-9][0-9][0-9].TW$', ticker)) or \
            #    bool(re.match('^00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('^00[0-9][0-9][0-9]L.TW$', ticker)):
            if bool(re.match('[0-9][0-9][0-9][0-9].TW$', ticker)) or \
                bool(re.match('00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('00[0-9][0-9][0-9]L.TW$', ticker)):
                target_ticker = ticker        
                stock_name = cpn_name
            
            ##### 上櫃公司
            elif bool(re.match('^[0-9][0-9][0-9][0-9].TWO$', ticker)):
                target_ticker = ticker    
                stock_name = cpn_name
            
            ##### US market
            else:
                target_ticker = ticker    
                stock_name = cpn_name 
            
            if target_ticker != None:
                ith += 1
                logger.info(f"{ith}th ticker: {target_ticker}; stock name: {cpn_name}")    
                local_stock_indicator = stock_indicator_pstock(ticker=target_ticker,  period="3mo", interval="1d", \
                                                                startdate= start_date, enddate= end_date, opt_verbose=self.opt_verbose)
                
                if self.json_data["lastest_datastr_twse_tpex"][0].lower() == "start_end_date":                    
                    #2025/2/24 remark cause Error 429 too many request
                    #local_stock_indicator.pstock_interval_startdate_enddate()
                    local_stock_indicator.yfinance_asyncio_interval_startdate_enddate()
                else:
                    local_stock_indicator.pstock_interval_period()
                
                local_stock_indicator.check_MAs_status()            
                local_stock_indicator.filter_MAs_status()
                
                dict_temp = {
                    "ticker" : target_ticker,
                    "stock_name": stock_name,
                    "weight": float(self.dict_ticker_weight_ration[target_ticker]),
                    "4_flag": local_stock_indicator.four_flag,
                    "3_flag": local_stock_indicator.three_flag,
                    "2_flag": local_stock_indicator.two_flag,
                    "1_flag": local_stock_indicator.one_flag,
                
                    "Expo_4_flag": local_stock_indicator.four_E_flag,
                    "Expo_3_flag": local_stock_indicator.three_E_flag,
                    "Expo_2_flag": local_stock_indicator.two_E_flag,
                    "Expo_1_flag": local_stock_indicator.one_E_flag,
                
                    "4_dog": local_stock_indicator.four_dog,
                    "3_dog": local_stock_indicator.three_dog,
                    "2_dog": local_stock_indicator.two_dog,
                    "1_dog": local_stock_indicator.one_dog,
                    
                    "Expo_4_dog": local_stock_indicator.four_E_dog,
                    "Expo_3_dog": local_stock_indicator.three_E_dog,
                    "Expo_2_dog": local_stock_indicator.two_E_dog,
                    "Expo_1_dog": local_stock_indicator.one_E_dog,
                    
                    "open": local_stock_indicator.open,
                    "close": local_stock_indicator.close,
                    "high": local_stock_indicator.high,
                    "low": local_stock_indicator.low,
                    "prev_day_close": local_stock_indicator.prev_day_close,
                    "MAs_status": local_stock_indicator.stock_MA_status,
                    "End_Date": str(stock_end_date),
                }
                list_MAs_status.append(dict_temp)                
                #logger.info(f'dict_temp: {dict_temp}')
                
                local_stock_indicator.check_ShortMediumTerm_MAs()
                local_stock_indicator.filter_ShortMediumTerm_MAs()
                local_stock_indicator.calculate_RSI()
                local_stock_indicator.calculate_MACD()
                local_stock_indicator.check_ShortMediumTerm_Volume()
                local_stock_indicator.filter_ShortMediumTerm_Volume()
                
                #local_stock_indicator.calculate_bollinger_bands()
                #local_stock_indicator.calculate_bollinger_bands(sma_window=20, std_window=20)
                local_stock_indicator.filter_ShortMediumTerm_Trend()
                
                local_stock_indicator.latest_dividend_cover_days = None
                local_stock_indicator.total_StockDividend = None
                # for ETF dividend purpose
                if bool(re.match('^twse_etf', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
                    local_stock_indicator.goodinfo_StockDividend(stock_id=[target_ticker.replace('\n', '').split('.')[0]])
                                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'local_stock_indicator.stock_data: \n{local_stock_indicator.stock_data}')
                
                dict_temp = {
                    "ticker" : target_ticker,
                    "stock_name": stock_name,
                    "weight": float(self.dict_ticker_weight_ration[target_ticker]),
                    "MA_3days": local_stock_indicator.stock_data['MA_3'].astype(float).iloc[-1],
                    "MA_5days": local_stock_indicator.stock_data['MA_5'].astype(float).iloc[-1],
                    "MA_7days": local_stock_indicator.stock_data['MA_7'].astype(float).iloc[-1],
                    "MA_13days": local_stock_indicator.stock_data['MA_13'].astype(float).iloc[-1],
                    "MA_28days": local_stock_indicator.stock_data['MA_28'].astype(float).iloc[-1],
                    "MA_84days": local_stock_indicator.stock_data['MA_84'].astype(float).iloc[-1],                    
                    "MA_10days": local_stock_indicator.stock_data['MA_10'].astype(float).iloc[-1],
                    "MA_20days": local_stock_indicator.stock_data['MA_20'].astype(float).iloc[-1],
                    "MA_60days": local_stock_indicator.stock_data['MA_60'].astype(float).iloc[-1],                    
                    "ShortTerm_BBband_Middle": local_stock_indicator.stock_data['Short Term Bollinger Middle'].astype(float).iloc[-1],
                    "ShortTerm_BBband_Upper": local_stock_indicator.stock_data['Short Term Bollinger Upper'].astype(float).iloc[-1],
                    "ShortTerm_BBband_Lower": local_stock_indicator.stock_data['Short Term Bollinger Lower'].astype(float).iloc[-1],
                    "MediumTerm_BBband_Middle": local_stock_indicator.stock_data['Medium Term Bollinger Middle'].astype(float).iloc[-1],
                    "MediumTerm_BBband_Upper": local_stock_indicator.stock_data['Medium Term Bollinger Upper'].astype(float).iloc[-1],
                    "MediumTerm_BBband_Lower": local_stock_indicator.stock_data['Medium Term Bollinger Lower'].astype(float).iloc[-1],                    
                    "RSI": local_stock_indicator.stock_data['RSI'].astype(float).iloc[-1],
                    "MACD": local_stock_indicator.stock_data['MACD'].astype(float).iloc[-1],
                    "MACD_Signal": local_stock_indicator.stock_data['MACD Signal'].astype(float).iloc[-1],
                    "MACD_Histogram": local_stock_indicator.stock_data['MACD Histogram'].astype(float).iloc[-1],                     
                    "Volume_avg_Weekly": local_stock_indicator.stock_data['volume_avg_weekly'].astype(float).iloc[-1],
                    "Volume_avg_BiWeekly": local_stock_indicator.stock_data['volume_avg_biweekly'].astype(float).iloc[-1],
                    "Volume_avg_Monthly": local_stock_indicator.stock_data['volume_avg_monthly'].astype(float).iloc[-1],
                    "Volume_avg_Quarterly": local_stock_indicator.stock_data['volume_avg_quarterly'].astype(float).iloc[-1],
        
                    "ShortMediumTerm_Trend_flag": local_stock_indicator.shortTerm_trend_status,       
                    "ShortMediumTerm_MA_flag": local_stock_indicator.shortmediumTerm_MA_status,
                    "ShortMediumTerm_Trade_Volume_flag": local_stock_indicator.shortmediumTerm_trade_volume_status,
                    
                    "MAs_status": local_stock_indicator.stock_MA_status,
                    "End_Date": str(stock_end_date),
                    "Latest_Dividend_Cover_Days": local_stock_indicator.latest_dividend_cover_days,
                    "Total_Stock_Dividend": local_stock_indicator.total_StockDividend,
                    
                    "open": local_stock_indicator.open,
                    "close": local_stock_indicator.close,
                    "high": local_stock_indicator.high,
                    "low": local_stock_indicator.low,
                    "prev_day_close": local_stock_indicator.prev_day_close,
                    "volume": local_stock_indicator.volume, 
                    "volume_avg_weekly": local_stock_indicator.volume_avg_weekly, 
                }
                list_ShortMediumTerm_trend.append(dict_temp)
        
        self.dict_MAs_status = list_MAs_status    
        self.dict_ShortMediumTerm_trend = list_ShortMediumTerm_trend
        
    def count_4_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'four_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為四海遊龍型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.four_star_twse_cpn += 1
                self.four_star_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\nfour_star_twse_weight_ratio: {"{:.5f}".format(self.four_star_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.four_star_tpex_cpn += 1 
                self.four_star_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
    
    def count_3_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'three_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):    
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為三陽開泰型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.three_star_twse_cpn += 1 
                self.three_star_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\nthree_star_twse_weight_ratio: {"{:.5f}".format(self.three_star_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.three_star_tpex_cpn += 1 
                self.three_star_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                                   
    def count_2_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'two_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):        
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為雙囍臨門型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.two_star_twse_cpn += 1 
                self.two_star_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\ntwo_star_twse_weight_ratio: {"{:.5f}".format(self.two_star_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.two_star_tpex_cpn += 1 
                self.two_star_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
    
    def count_1_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'one_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):                        
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為一星報喜型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.one_star_twse_cpn += 1 
                self.one_star_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\none_star_twse_weight_ratio: {"{:.5f}".format(self.one_star_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.one_star_tpex_cpn += 1 
                self.one_star_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
    
    def count_dict_4_star_num(self, dict_ticker_MAs_info):
        if dict_ticker_MAs_info["MAs_status"] == 'four_star' and (dict_ticker_MAs_info["close"] >= 0.1):
            logger.info(f'{dict_ticker_MAs_info["ticker"]} {dict_ticker_MAs_info["stock_name"]}:為四海遊龍型股票!! weight_ratio: {dict_ticker_MAs_info["weight"]}')
            
            self.four_star_cpn += 1
            self.four_star_weight_ratio += dict_ticker_MAs_info["weight"]
            if self.opt_verbose.lower() == 'on':
                logger.info(f'\nfour_star_weight_ratio: {"{:.5f}".format(self.four_star_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_weighted_indicator: {"{:.5f}".format(self.volatility_weighted_indicator)}')
                                        
    def count_dict_3_star_num(self, dict_ticker_MAs_info):
        if dict_ticker_MAs_info["MAs_status"] == 'three_star' and (dict_ticker_MAs_info["close"] >= 0.1):
            logger.info(f'{dict_ticker_MAs_info["ticker"]} {dict_ticker_MAs_info["stock_name"]}:為三陽開泰型股票!! weight_ratio: {dict_ticker_MAs_info["weight"]}')
            
            self.three_star_cpn += 1
            self.three_star_weight_ratio += dict_ticker_MAs_info["weight"]
            if self.opt_verbose.lower() == 'on':
                logger.info(f'\nthree_star_weight_ratio: {"{:.5f}".format(self.three_star_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_weighted_indicator: {"{:.5f}".format(self.volatility_weighted_indicator)}')
                         
    def count_dict_2_star_num(self, dict_ticker_MAs_info):
        if dict_ticker_MAs_info["MAs_status"] == 'two_star' and (dict_ticker_MAs_info["close"] >= 0.1):
            logger.info(f'{dict_ticker_MAs_info["ticker"]} {dict_ticker_MAs_info["stock_name"]}:為雙囍臨門型股票!! weight_ratio: {dict_ticker_MAs_info["weight"]}')
            
            self.two_star_cpn += 1
            self.two_star_weight_ratio += dict_ticker_MAs_info["weight"]
            if self.opt_verbose.lower() == 'on':
                logger.info(f'\ntwo_star_weight_ratio: {"{:.5f}".format(self.two_star_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_weighted_indicator: {"{:.5f}".format(self.volatility_weighted_indicator)}')
                    
    def count_dict_1_star_num(self, dict_ticker_MAs_info):
        if dict_ticker_MAs_info["MAs_status"] == 'one_star' and (dict_ticker_MAs_info["close"] >= 0.1):
            logger.info(f'{dict_ticker_MAs_info["ticker"]} {dict_ticker_MAs_info["stock_name"]}:為一星報喜型股票!! weight_ratio: {dict_ticker_MAs_info["weight"]}')
            
            self.one_star_cpn += 1
            self.one_star_weight_ratio += dict_ticker_MAs_info["weight"]
            if self.opt_verbose.lower() == 'on':
                logger.info(f'\none_star_weight_ratio: {"{:.5f}".format(self.one_star_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_weighted_indicator: {"{:.5f}".format(self.volatility_weighted_indicator)}')
                    
    def count_4_expo_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_four_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_四海遊龍型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_four_star_twse_cpn += 1
                self.expo_four_star_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\nexpo_four_star_twse_weight_ratio: {"{:.5f}".format(self.expo_four_star_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_four_star_tpex_cpn += 1 
                self.expo_four_star_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
    
    def count_3_expo_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_three_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為指數_三陽開泰型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')            
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_three_star_twse_cpn += 1 
                self.expo_three_star_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\nexpo_three_star_twse_weight_ratio: {"{:.5f}".format(self.expo_three_star_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_three_star_tpex_cpn += 1 
                self.expo_three_star_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
            
    def count_2_expo_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_two_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):    
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為指數_雙囍臨門型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_two_star_twse_cpn += 1 
                self.expo_two_star_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\nexpo_two_star_twse_weight_ratio: {"{:.5f}".format(self.expo_two_star_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_two_star_tpex_cpn += 1 
                self.expo_two_star_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
            
    def count_1_expo_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_one_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):            
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為指數_一星報喜型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_one_star_twse_cpn += 1 
                self.expo_one_star_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\nexpo_one_star_tpex_weight_ratio: {"{:.5f}".format(self.expo_one_star_tpex_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_one_star_tpex_cpn += 1
                self.expo_one_star_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                                                            
    def count_4_dog_num(self, twse_tpex_ticker_MAs_info):
        
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'four_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):            
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為四腳朝天型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.four_dog_twse_cpn += 1 
                self.four_dog_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\nfour_dog_twse_weight_ratio: {"{:.5f}".format(self.four_dog_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.four_dog_tpex_cpn += 1 
                self.four_dog_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]

    def count_3_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'three_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):                
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為三人成虎型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')                
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.three_dog_twse_cpn += 1 
                self.three_dog_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\nthree_dog_twse_weight_ratio: {"{:.5f}".format(self.three_dog_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.three_dog_tpex_cpn += 1 
                self.three_dog_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
    
    def count_2_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'two_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):                
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為二竪作惡型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')                
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.two_dog_twse_cpn += 1 
                self.two_dog_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\ntwo_dog_twse_weight_ratio: {"{:.5f}".format(self.two_dog_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.two_dog_tpex_cpn += 1 
                self.two_dog_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                                    
    def count_1_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'one_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):                
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為一敗塗地型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')                
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.one_dog_twse_cpn += 1 
                self.one_dog_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'\none_dog_twse_weight_ratio: {"{:.5f}".format(self.one_dog_twse_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_TWSE_weighted_indicator: {"{:.5f}".format(self.volatility_twse_weighted_indicator)}')
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.one_dog_tpex_cpn += 1 
                self.one_dog_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
    
    
    def count_dict_4_dog_num(self, dict_ticker_MAs_info):
        if dict_ticker_MAs_info["MAs_status"] == 'four_dog' and (dict_ticker_MAs_info["close"] >= 0.1):
            logger.info(f'{dict_ticker_MAs_info["ticker"]} {dict_ticker_MAs_info["stock_name"]}:為四腳朝天型股票!! weight_ratio: {dict_ticker_MAs_info["weight"]}')
            
            self.four_dog_cpn += 1
            self.four_dog_weight_ratio += dict_ticker_MAs_info["weight"]
            if self.opt_verbose.lower() == 'on':
                logger.info(f'\nfour_dog_weight_ratio: {"{:.5f}".format(self.four_dog_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_weighted_indicator: {"{:.5f}".format(self.volatility_weighted_indicator)}')
                    
    def count_dict_3_dog_num(self, dict_ticker_MAs_info):
        if dict_ticker_MAs_info["MAs_status"] == 'three_dog' and (dict_ticker_MAs_info["close"] >= 0.1):
            logger.info(f'{dict_ticker_MAs_info["ticker"]} {dict_ticker_MAs_info["stock_name"]}:為三人成虎型股票!! weight_ratio: {dict_ticker_MAs_info["weight"]}')
            
            self.three_dog_cpn += 1
            self.three_dog_weight_ratio += dict_ticker_MAs_info["weight"]
            if self.opt_verbose.lower() == 'on':
                logger.info(f'\nthree_dog_weight_ratio: {"{:.5f}".format(self.three_dog_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_weighted_indicator: {"{:.5f}".format(self.volatility_weighted_indicator)}')
                            
    def count_dict_2_dog_num(self, dict_ticker_MAs_info):
        if dict_ticker_MAs_info["MAs_status"] == 'two_dog' and (dict_ticker_MAs_info["close"] >= 0.1):
            logger.info(f'{dict_ticker_MAs_info["ticker"]} {dict_ticker_MAs_info["stock_name"]}:為二竪作惡型股票!! weight_ratio: {dict_ticker_MAs_info["weight"]}')
            
            self.two_dog_cpn += 1
            self.two_dog_weight_ratio += dict_ticker_MAs_info["weight"]
            if self.opt_verbose.lower() == 'on':
                logger.info(f'\ntwo_dog_weight_ratio: {"{:.5f}".format(self.two_dog_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_weighted_indicator: {"{:.5f}".format(self.volatility_weighted_indicator)}')
                    
    def count_dict_1_dog_num(self, dict_ticker_MAs_info):
        if dict_ticker_MAs_info["MAs_status"] == 'one_dog' and (dict_ticker_MAs_info["close"] >= 0.1):
            logger.info(f'{dict_ticker_MAs_info["ticker"]} {dict_ticker_MAs_info["stock_name"]}:為一敗塗地型股票!! weight_ratio: {dict_ticker_MAs_info["weight"]}')
            
            self.one_dog_cpn += 1
            self.one_dog_weight_ratio += dict_ticker_MAs_info["weight"]
            if self.opt_verbose.lower() == 'on':
                logger.info(f'\none_dog_weight_ratio: {"{:.5f}".format(self.one_dog_weight_ratio)}, volatility_stock_weighted_indicator: {"{:.5f}".format(self.volatility_stock_weighted_indicator)}, volatility_weighted_indicator: {"{:.5f}".format(self.volatility_weighted_indicator)}')
                    
    def count_4_expo_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_four_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_四腳朝天型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_four_dog_twse_cpn += 1
                self.expo_four_dog_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_four_dog_tpex_cpn += 1 
                self.expo_four_dog_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
    
    def count_3_expo_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_three_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_三人成虎型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_three_dog_twse_cpn += 1
                self.expo_three_dog_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_three_dog_tpex_cpn += 1 
                self.expo_three_dog_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
    
    def count_2_expo_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_two_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_二竪作惡型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_two_dog_twse_cpn += 1
                self.expo_two_dog_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_two_dog_tpex_cpn += 1 
                self.expo_two_dog_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
                
    def count_1_expo_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_one_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_一敗塗地型股票!! weight_ratio: {twse_tpex_ticker_MAs_info["weight"]}')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_one_dog_twse_cpn += 1
                self.expo_one_dog_twse_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
            elif bool(re.search('\.TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_one_dog_tpex_cpn += 1
                self.expo_one_dog_tpex_weight_ratio += twse_tpex_ticker_MAs_info["weight"]
    
    def calculate_TWSE_TPEX_weighted_indicator(self, twse_tpex_ticker_MAs_info):
        diff =  twse_tpex_ticker_MAs_info["close"] - twse_tpex_ticker_MAs_info["open"]
        prev_day_close_diff =  twse_tpex_ticker_MAs_info["close"] - twse_tpex_ticker_MAs_info["prev_day_close"]
        self.volatility_stock_weighted_indicator = prev_day_close_diff * twse_tpex_ticker_MAs_info["weight"]
        self.volatility_twse_weighted_indicator += self.volatility_stock_weighted_indicator
        logger.info(f'prev_day_close_diff: {prev_day_close_diff}, diff: {diff}')
    
    def calculate_dict_weighted_indicator(self, dict_ticker_MAs_info):
        diff =  dict_ticker_MAs_info["close"] - dict_ticker_MAs_info["open"]
        prev_day_close_diff =  dict_ticker_MAs_info["close"] - dict_ticker_MAs_info["prev_day_close"]
        self.volatility_stock_weighted_indicator = prev_day_close_diff * dict_ticker_MAs_info["weight"]
        self.volatility_weighted_indicator += self.volatility_stock_weighted_indicator
        logger.info(f'prev_day_close_diff: {prev_day_close_diff}, diff: {diff}')
        
    def check_TWSE_TPEX_MAs_status(self):
        
        for dict_twse_tpex_ticker_MAs in self.TWSE_TPEX_MAs_status:
            self.calculate_TWSE_TPEX_weighted_indicator(dict_twse_tpex_ticker_MAs)
            
            self.count_4_star_num(dict_twse_tpex_ticker_MAs)
            self.count_3_star_num(dict_twse_tpex_ticker_MAs)
            self.count_2_star_num(dict_twse_tpex_ticker_MAs)
            self.count_1_star_num(dict_twse_tpex_ticker_MAs)
            
            self.count_4_expo_star_num(dict_twse_tpex_ticker_MAs)
            self.count_3_expo_star_num(dict_twse_tpex_ticker_MAs)
            self.count_2_expo_star_num(dict_twse_tpex_ticker_MAs)
            self.count_1_expo_star_num(dict_twse_tpex_ticker_MAs)
            
            self.count_4_dog_num(dict_twse_tpex_ticker_MAs)
            self.count_3_dog_num(dict_twse_tpex_ticker_MAs)      
            self.count_2_dog_num(dict_twse_tpex_ticker_MAs)
            self.count_1_dog_num(dict_twse_tpex_ticker_MAs)

            if bool(re.search('TW$', dict_twse_tpex_ticker_MAs["ticker"])):
                self.num_twse_cpn += 1 
            elif bool(re.search('\.TWO$', dict_twse_tpex_ticker_MAs["ticker"])):
                self.num_tpex_cpn += 1    

    def check_dict_MAs_status(self):
        
        for dict_ticker_MAs in self.dict_MAs_status:
            self.calculate_dict_weighted_indicator(dict_ticker_MAs)

            self.count_dict_4_star_num(dict_ticker_MAs)
            self.count_dict_3_star_num(dict_ticker_MAs)
            self.count_dict_2_star_num(dict_ticker_MAs)
            self.count_dict_1_star_num(dict_ticker_MAs)
            
            #self.count_4_expo_star_num(dict_ticker_MAs)
            #self.count_3_expo_star_num(dict_ticker_MAs)
            #self.count_2_expo_star_num(dict_ticker_MAs)
            #self.count_1_expo_star_num(dict_ticker_MAs)
            
            self.count_dict_4_dog_num(dict_ticker_MAs)
            self.count_dict_3_dog_num(dict_ticker_MAs)      
            self.count_dict_2_dog_num(dict_ticker_MAs)
            self.count_dict_1_dog_num(dict_ticker_MAs)
            
            self.num_cpn += 1
    
    def log_all_ticker_dict_MAs_cnts(self, path_all_tikcers_ma, dict_MAs_momentum_status):
        list_all_tickers_ma_cnt = []
        default_time_format = '%Y-%m-%d %H:%M:%S'
        
        for dict_ticker_MAs_momentum in dict_MAs_momentum_status:
            #logger.info(f'length of dict_ticker_MAs_momentum: {dict_ticker_MAs_momentum.__len__()}')
            #logger.info(f'dict_ticker_MAs_momentum: {dict_ticker_MAs_momentum}')
            if dict_ticker_MAs_momentum.__len__() == 26:
                list_all_tickers_ma_cnt.append([dict_ticker_MAs_momentum["ticker"].replace('\n', ''),dict_ticker_MAs_momentum["stock_name"],\
                                '{:.2f}'.format(dict_ticker_MAs_momentum["open"]),'{:.2f}'.format(dict_ticker_MAs_momentum["close"]), \
                                '{:.2f}'.format(dict_ticker_MAs_momentum["high"]),'{:.2f}'.format(dict_ticker_MAs_momentum["low"]),\
                                '{:.2f}'.format(dict_ticker_MAs_momentum["prev_day_close"]),'{:.5f}'.format(dict_ticker_MAs_momentum["weight"]),\
                                dict_ticker_MAs_momentum["MAs_status"],dict_ticker_MAs_momentum["End_Date"]]
                            )                
            else:
                list_all_tickers_ma_cnt.append([dict_ticker_MAs_momentum["ticker"].replace('\n', ''),dict_ticker_MAs_momentum["stock_name"],\
                                '{:.2f}'.format(dict_ticker_MAs_momentum["open"]),'{:.2f}'.format(dict_ticker_MAs_momentum["close"]), \
                                '{:.2f}'.format(dict_ticker_MAs_momentum["high"]),'{:.2f}'.format(dict_ticker_MAs_momentum["low"]),\
                                '{:.2f}'.format(dict_ticker_MAs_momentum["prev_day_close"]),'{:.5f}'.format(dict_ticker_MAs_momentum["weight"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["volume"]), '{:.5f}'.format(dict_ticker_MAs_momentum["volume_avg_weekly"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["MA_3days"]), '{:.5f}'.format(dict_ticker_MAs_momentum["MA_5days"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["MA_7days"]), '{:.5f}'.format(dict_ticker_MAs_momentum["MA_13days"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["MA_28days"]), '{:.5f}'.format(dict_ticker_MAs_momentum["MA_84days"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["MA_10days"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["MA_20days"]), '{:.5f}'.format(dict_ticker_MAs_momentum["MA_60days"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["ShortTerm_BBband_Middle"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["ShortTerm_BBband_Upper"]),'{:.5f}'.format(dict_ticker_MAs_momentum["ShortTerm_BBband_Lower"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["MediumTerm_BBband_Middle"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["MediumTerm_BBband_Upper"]),'{:.5f}'.format(dict_ticker_MAs_momentum["MediumTerm_BBband_Lower"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["RSI"]), '{:.5f}'.format(dict_ticker_MAs_momentum["MACD"]),\
                                '{:.5f}'.format(dict_ticker_MAs_momentum["MACD_Signal"]),'{:.5f}'.format(dict_ticker_MAs_momentum["MACD_Histogram"]),\
                                '{:.1f}'.format(dict_ticker_MAs_momentum["Volume_avg_Weekly"]),'{:.1f}'.format(dict_ticker_MAs_momentum["Volume_avg_BiWeekly"]), \
                                '{:.1f}'.format(dict_ticker_MAs_momentum["Volume_avg_Monthly"]),'{:.1f}'.format(dict_ticker_MAs_momentum["Volume_avg_Quarterly"]),\
                                
                                dict_ticker_MAs_momentum["ShortMediumTerm_Trend_flag"],\
                                dict_ticker_MAs_momentum["ShortMediumTerm_MA_flag"],\
                                dict_ticker_MAs_momentum["ShortMediumTerm_Trade_Volume_flag"],\
                                        
                                dict_ticker_MAs_momentum["MAs_status"], \
                                dict_ticker_MAs_momentum["End_Date"], \
                                dict_ticker_MAs_momentum["Latest_Dividend_Cover_Days"], dict_ticker_MAs_momentum["Total_Stock_Dividend"]                                
                                ]
                            )
        
        list_all_tickers_ma_cnt.append([f'{self.json_data["lastest_datastr_twse_tpex"][1].upper()} 股票家數: {self.num_cpn}'])
        
        list_all_tickers_ma_cnt.append(['{} 四海遊龍型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 三陽開泰型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.json_data["lastest_datastr_twse_tpex"][1].upper(),
                self.four_star_cpn, self.four_star_cpn/self.num_cpn, self.four_star_weight_ratio,
                self.three_star_cpn, self.three_star_cpn/self.num_cpn, self.three_star_weight_ratio)])
        
        list_all_tickers_ma_cnt.append(['{} 雙囍臨門型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 一星報喜型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.json_data["lastest_datastr_twse_tpex"][1].upper(),
                self.two_star_cpn, self.two_star_cpn/self.num_cpn, self.two_star_weight_ratio,
                self.one_star_cpn, self.one_star_cpn/self.num_cpn, self.one_star_weight_ratio)])
        
        list_all_tickers_ma_cnt.append(['{} 四腳朝天型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 三人成虎型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.json_data["lastest_datastr_twse_tpex"][1].upper(),
                self.four_dog_cpn, self.four_dog_cpn/self.num_cpn, self.four_dog_weight_ratio,
                self.three_dog_cpn, self.three_dog_cpn/self.num_cpn, self.three_dog_weight_ratio)])
        
        list_all_tickers_ma_cnt.append(['{} 二竪作惡型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 一敗塗地型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.json_data["lastest_datastr_twse_tpex"][1].upper(),
                self.two_dog_cpn, self.two_dog_cpn/self.num_cpn, self.two_dog_weight_ratio,
                self.one_dog_cpn, self.one_dog_cpn/self.num_cpn, self.one_dog_weight_ratio)])
        
        t = time.localtime()
        list_all_tickers_ma_cnt.append([time.strftime(default_time_format, t)])
        
        #logger.info(f'list_all_tickers_ma_cnt: {list_all_tickers_ma_cnt}' )        
        lib_misc.list_out_all_tickers_MA_cnts_file(path_all_tikcers_ma, list_all_tickers_ma_cnt, opt_verbose='on')
                
    def log_info_TWSE_MAs_status(self):
        logger.info(f'TWSE 股票家數: {self.num_twse_cpn}' )    
        logger.info('TWSE 四海遊龍型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 三陽開泰型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.four_star_twse_cpn, self.four_star_twse_cpn/self.num_twse_cpn, self.four_star_twse_weight_ratio,
                self.three_star_twse_cpn, self.three_star_twse_cpn/self.num_twse_cpn, self.three_star_twse_weight_ratio) )
        
        logger.info('TWSE 雙囍臨門型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 一星報喜型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.two_star_twse_cpn, self.two_star_twse_cpn/self.num_twse_cpn, self.two_star_twse_weight_ratio,
                self.one_star_twse_cpn, self.one_star_twse_cpn/self.num_twse_cpn, self.one_star_twse_weight_ratio) )
        
        logger.info('TWSE 指數_四海遊龍型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 指數_三陽開泰型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.expo_four_star_twse_cpn, self.expo_four_star_twse_cpn/self.num_twse_cpn, self.expo_four_star_twse_weight_ratio,
                self.expo_three_star_twse_cpn, self.expo_three_star_twse_cpn/self.num_twse_cpn, self.expo_three_star_twse_weight_ratio) )
        
        logger.info('TWSE 指數_雙囍臨門型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 指數_一星型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.expo_two_star_twse_cpn, self.expo_two_star_twse_cpn/self.num_twse_cpn, self.expo_two_star_twse_weight_ratio,
                self.expo_one_star_twse_cpn, self.expo_one_star_twse_cpn/self.num_twse_cpn, self.expo_one_star_twse_weight_ratio) )
        
        logger.info('TWSE 四腳朝天型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 三人成虎型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.four_dog_twse_cpn, self.four_dog_twse_cpn/self.num_twse_cpn, self.four_dog_twse_weight_ratio,
                self.three_dog_twse_cpn, self.three_dog_twse_cpn/self.num_twse_cpn, self.three_dog_twse_weight_ratio) )

        logger.info('TWSE 二竪作惡型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 一敗塗地型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.two_dog_twse_cpn, self.two_dog_twse_cpn/self.num_twse_cpn, self.two_dog_twse_weight_ratio,
                self.one_dog_twse_cpn, self.one_dog_twse_cpn/self.num_twse_cpn, self.one_dog_twse_weight_ratio) )
        
        logger.info('TWSE 指數_四腳朝天型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 指數_三人成虎型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.expo_four_dog_twse_cpn, self.expo_four_dog_twse_cpn/self.num_twse_cpn, self.expo_four_dog_twse_weight_ratio,
                self.expo_three_dog_twse_cpn, self.expo_three_dog_twse_cpn/self.num_twse_cpn, self.expo_three_dog_twse_weight_ratio) )
        
        logger.info('TWSE 指數_二竪作惡型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 指數_一敗塗地型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.expo_two_star_twse_cpn, self.expo_two_star_twse_cpn/self.num_twse_cpn, self.expo_two_star_twse_weight_ratio,
                self.expo_one_star_twse_cpn, self.expo_one_star_twse_cpn/self.num_twse_cpn, self.expo_one_star_twse_weight_ratio) )
    
    def log_info_dict_MAs_status(self):
        logger.info(f'{self.json_data["lastest_datastr_twse_tpex"][1].upper()} 股票家數: {self.num_cpn}' )    
        
        logger.info('{} 四海遊龍型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 三陽開泰型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.json_data["lastest_datastr_twse_tpex"][1].upper(),
                self.four_star_cpn, self.four_star_cpn/self.num_cpn, self.four_star_weight_ratio,
                self.three_star_cpn, self.three_star_cpn/self.num_cpn, self.three_star_weight_ratio) )
        
        logger.info('{} 雙囍臨門型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 一星報喜型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.json_data["lastest_datastr_twse_tpex"][1].upper(),
                self.two_star_cpn, self.two_star_cpn/self.num_cpn, self.two_star_weight_ratio,
                self.one_star_cpn, self.one_star_cpn/self.num_cpn, self.one_star_weight_ratio) )
        
        logger.info('{} 四腳朝天型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 三人成虎型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.json_data["lastest_datastr_twse_tpex"][1].upper(),
                self.four_dog_cpn, self.four_dog_cpn/self.num_cpn, self.four_dog_weight_ratio,
                self.three_dog_cpn, self.three_dog_cpn/self.num_cpn, self.three_dog_weight_ratio) )

        logger.info('{} 二竪作惡型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TWSE 一敗塗地型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.json_data["lastest_datastr_twse_tpex"][1].upper(),
                self.two_dog_cpn, self.two_dog_cpn/self.num_cpn, self.two_dog_weight_ratio,
                self.one_dog_cpn, self.one_dog_cpn/self.num_cpn, self.one_dog_weight_ratio) )
                
    def log_info_TPEX_MAs_status(self):
        logger.info(f'TPEX 股票家數: {self.num_tpex_cpn}' )    
        logger.info('TPEX 四海遊龍型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TPEX 三陽開泰型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.four_star_tpex_cpn, self.four_star_tpex_cpn/self.num_tpex_cpn, self.four_star_tpex_weight_ratio,
                self.three_star_tpex_cpn, self.three_star_tpex_cpn/self.num_tpex_cpn, self.three_star_tpex_weight_ratio) )
        
        logger.info('TPEX 雙囍臨門型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TPEX 一星報喜型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.two_star_tpex_cpn, self.two_star_tpex_cpn/self.num_tpex_cpn, self.two_star_tpex_weight_ratio,
                self.one_star_tpex_cpn, self.one_star_tpex_cpn/self.num_tpex_cpn, self.one_star_tpex_weight_ratio) )
        
        logger.info('TPEX 指數_四海遊龍型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TPEX 指數_三陽開泰型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.expo_four_star_tpex_cpn, self.expo_four_star_tpex_cpn/self.num_twse_cpn, self.expo_four_star_tpex_weight_ratio,
                self.expo_three_star_tpex_cpn, self.expo_three_star_tpex_cpn/self.num_twse_cpn, self.expo_three_star_tpex_weight_ratio) )
        
        logger.info('TPEX 指數_雙囍臨門型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TPEX 指數_一星型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.expo_two_star_tpex_cpn, self.expo_two_star_tpex_cpn/self.num_twse_cpn, self.expo_two_star_tpex_weight_ratio,
                self.expo_one_star_tpex_cpn, self.expo_one_star_tpex_cpn/self.num_twse_cpn, self.expo_one_star_tpex_weight_ratio) )
        
        logger.info('TPEX 四腳朝天型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TPEX 三笑杯型股票家數: {} %:{:.3f}  weight_ratio_%:{:.3f}'.format(\
                self.four_dog_tpex_cpn, self.four_dog_tpex_cpn/self.num_tpex_cpn, self.four_dog_tpex_weight_ratio,
                self.three_dog_tpex_cpn, self.three_dog_tpex_cpn/self.num_tpex_cpn, self.three_dog_tpex_weight_ratio) ) 
        
        logger.info('TPEX 二竪作惡型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TPEX 一敗塗地型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.two_dog_tpex_cpn, self.one_dog_tpex_cpn/self.num_tpex_cpn, self.one_dog_tpex_weight_ratio,
                self.two_dog_tpex_cpn, self.one_dog_tpex_cpn/self.num_tpex_cpn, self.one_dog_tpex_weight_ratio) )
        
        logger.info('TPEX 指數_四腳朝天型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TPEX 指數_三人成虎型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.expo_four_dog_tpex_cpn, self.expo_four_dog_tpex_cpn/self.num_tpex_cpn, self.expo_four_dog_tpex_weight_ratio,
                self.expo_three_dog_tpex_cpn, self.expo_three_dog_tpex_cpn/self.num_tpex_cpn, self.expo_three_dog_tpex_weight_ratio) )
        
        logger.info('TPEX 指數_二竪作惡型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}; TPEX 指數_一敗塗地型股票家數: {} %:{:.3f} weight_ratio_%:{:.3f}'.format(\
                self.expo_two_dog_tpex_cpn, self.expo_two_dog_tpex_cpn/self.num_tpex_cpn, self.expo_two_dog_tpex_weight_ratio,
                self.expo_one_dog_tpex_cpn, self.expo_one_dog_tpex_cpn/self.num_tpex_cpn, self.expo_one_dog_tpex_weight_ratio) )
                            
    def calculate_TWSE_TPEX_MAs_status(self):
        self.dict_twse_tpex_ticker_cpn_name = query_dic_from_pickle(self.list_path_pickle_ticker[2])
        #self.dict_twse_tpex_ticker_weight_ration = query_dic_from_pickle(self.list_path_pickle_ticker[-1])
        
        #for key, value in dict_twse_tpex_ticker_cpn_name.items():
        #        logger.info('\n ticker: {}; cpn_name: {}'.format(key, value) )
    
        self.store_TWSE_TPEX_MAs_status()    
        self.check_TWSE_TPEX_MAs_status()
                                
        self.log_info_TWSE_MAs_status()
        self.log_info_TPEX_MAs_status()          
         
        logger.info(f'\n{self.four_star_twse_cpn}\n{self.three_star_twse_cpn}\n{self.two_star_twse_cpn}\n{self.one_star_twse_cpn}\n{self.expo_four_star_twse_cpn}\n{self.expo_three_star_twse_cpn}\n{self.expo_two_star_twse_cpn}\n{self.expo_one_star_twse_cpn}\n{self.four_dog_twse_cpn}\n{self.three_dog_twse_cpn}') 
        #logger.info(f'\n{self.expo_four_star_twse_cpn}\n{self.expo_three_star_twse_cpn}\n{self.expo_two_star_twse_cpn}\n{self.expo_one_star_twse_cpn}') 
        #logger.info(f'\n{self.four_dog_twse_cpn}\n{self.three_dog_twse_cpn}')
        logger.info(f'\n{self.four_star_twse_weight_ratio}\n{self.three_star_twse_weight_ratio}\n{self.two_star_twse_weight_ratio}\n{self.one_star_twse_weight_ratio}\n{self.expo_four_star_twse_weight_ratio}\n{self.expo_three_star_twse_weight_ratio}\n{self.expo_two_star_twse_weight_ratio}\n{self.expo_one_star_twse_weight_ratio}\n{self.four_dog_twse_weight_ratio}\n{self.three_dog_twse_weight_ratio}') 
        
        logger.info(f'\n{self.four_star_tpex_cpn}\n{self.three_star_tpex_cpn}\n{self.two_star_tpex_cpn}\n{self.one_star_tpex_cpn}\n{self.expo_four_star_tpex_cpn}\n{self.expo_three_star_tpex_cpn}\n{self.expo_two_star_tpex_cpn}\n{self.expo_one_star_tpex_cpn}\n{self.four_dog_tpex_cpn}\n{self.three_dog_tpex_cpn}')         
        #logger.info(f'\n{self.expo_four_star_tpex_cpn}\n{self.expo_three_star_tpex_cpn}\n{self.expo_two_star_tpex_cpn}\n{self.expo_one_star_tpex_cpn}') 
        #logger.info(f'\n{self.four_dog_tpex_cpn}\n{self.three_dog_tpex_cpn}')
        logger.info(f'\n{self.four_star_tpex_weight_ratio}\n{self.three_star_tpex_weight_ratio}\n{self.two_star_tpex_weight_ratio}\n{self.one_star_tpex_weight_ratio}\n{self.expo_four_star_tpex_weight_ratio}\n{self.expo_three_star_tpex_weight_ratio}\n{self.expo_two_star_tpex_weight_ratio}\n{self.expo_one_star_tpex_weight_ratio}\n{self.four_dog_tpex_weight_ratio}\n{self.three_dog_tpex_weight_ratio}')         
    
    def yfinance_StockInsider(self, stock_idx):
        si = StockInsider( code= None, stock_idx= stock_idx, \
                            list_df_twse_tpex_stock_info= requests_twse_tpex_stock_idx(self.json_data), 
                            json_data = self.json_data)
        df_stockdata= si.show_data()
        df_stockdata.reset_index(inplace=True)
        
        return  df_stockdata
    '''
    yfinance==0.2.54
    Price        Date         Close          High           Low          Open   Volume
    Ticker                    ^TWII         ^TWII         ^TWII         ^TWII    ^TWII
    0      2024-10-25  23348.449219  23388.529297  23222.769531  23255.070312  2744200
    ..            ...           ...           ...           ...           ...      ...
    74     2025-02-19  23604.080078  23683.460938  23550.990234  23589.439453        0
    '''
    def calculate_TWSE_index_info(self, start_date, end_date):
        str_TWSE_ticker = '^TWII'
        
        #by yfinance 
        twse_stock_indicator = stock_indicator(ticker=str_TWSE_ticker, startdate= start_date, enddate= end_date)
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'twse_stock_indicator.stock_data: \n{twse_stock_indicator.stock_data}')
        
        #df_stock_data = self.yfinance_StockInsider(str_TWSE_ticker)
        self.twse_close = twse_stock_indicator.stock_data['Close'].astype(str).iloc[-1]
        self.twse_open = twse_stock_indicator.stock_data['Open'].astype(str).iloc[-1]
        self.twse_high = twse_stock_indicator.stock_data['High'].astype(str).iloc[-1]
        self.twse_low = twse_stock_indicator.stock_data['Low'].astype(str).iloc[-1]
        self.twse_volume = twse_stock_indicator.stock_data['Volume'].astype(str).iloc[-1]
            
        #by pstock(asyncio mode)
        '''
        twse_stock_indicator_pstock = stock_indicator_pstock(ticker=str_TWSE_ticker,  period="3mo", interval="1d", \
                                                            startdate= start_date, enddate= end_date, opt_verbose=self.opt_verbose)
                
        if self.json_data["lastest_datastr_twse_tpex"][0].lower() == "start_end_date":                    
            twse_stock_indicator_pstock.pstock_interval_startdate_enddate()
        else:
            twse_stock_indicator_pstock.pstock_interval_period()
                
        if self.opt_verbose.lower() == 'on':
            logger.info(f'twse_stock_indicator_pstock.stock_data: \n{twse_stock_indicator_pstock.stock_data}')
                            
        self.twse_close = twse_stock_indicator_pstock.stock_data['close'].astype(float).iloc[-1]
        self.twse_open = twse_stock_indicator_pstock.stock_data['open'].astype(float).iloc[-1]
        self.twse_high = twse_stock_indicator_pstock.stock_data['high'].astype(float).iloc[-1]
        self.twse_low = twse_stock_indicator_pstock.stock_data['low'].astype(float).iloc[-1]
        self.twse_volume = twse_stock_indicator_pstock.stock_data['volume'].astype(float).iloc[-1]
        '''
    
    def calculate_dict_index_info(self, str_ticker, start_date, end_date):
        
        #by yfinance 
        dict_stock_indicator = stock_indicator(ticker=str_ticker, startdate= start_date, enddate= end_date)
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'{self.json_data["lastest_datastr_twse_tpex"][1].upper()} stock_indicator.stock_data: \n{dict_stock_indicator.stock_data}')
        
        #df_stock_data = self.yfinance_StockInsider(str_TWSE_ticker)
        self.close = dict_stock_indicator.stock_data['Close'].astype(str).iloc[-1]
        self.open = dict_stock_indicator.stock_data['Open'].astype(str).iloc[-1]
        self.high = dict_stock_indicator.stock_data['High'].astype(str).iloc[-1]
        self.low = dict_stock_indicator.stock_data['Low'].astype(str).iloc[-1]
        self.volume = dict_stock_indicator.stock_data['Volume'].astype(str).iloc[-1]
            
    def calculate_TPEX_index_info(self, start_date, end_date):
        str_TPEX_ticker = '^TWOII'
        tpex_stock_indicator = stock_indicator(ticker=str_TPEX_ticker, startdate= start_date, enddate= end_date)
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'tpex_stock_indicator.stock_data: \n{tpex_stock_indicator.stock_data}')
            
        self.tpex_close = tpex_stock_indicator.stock_data['Close'].astype(float).iloc[-1]
        self.tpex_open = tpex_stock_indicator.stock_data['Open'].astype(float).iloc[-1]
        self.tpex_high = tpex_stock_indicator.stock_data['High'].astype(float).iloc[-1]
        self.tpex_low = tpex_stock_indicator.stock_data['Low'].astype(float).iloc[-1]
        self.tpex_volume = tpex_stock_indicator.stock_data['Volume'].astype(float).iloc[-1]
        
    def init_count_TWSE_variables(self):
        self.num_twse_cpn = 0        
        self.volatility_stock_weighted_indicator = 0
        self.volatility_twse_weighted_indicator = 0
        self.four_star_twse_cpn = 0; self.three_star_twse_cpn = 0; 
        self.two_star_twse_cpn = 0; self.one_star_twse_cpn = 0; 
        
        self.four_star_twse_weight_ratio = 0; self.three_star_twse_weight_ratio = 0; 
        self.two_star_twse_weight_ratio = 0; self.one_star_twse_weight_ratio = 0; 
        
        self.expo_four_star_twse_cpn = 0; self.expo_three_star_twse_cpn = 0; 
        self.expo_two_star_twse_cpn = 0; self.expo_one_star_twse_cpn = 0; 
        
        self.expo_four_star_twse_weight_ratio = 0; self.expo_three_star_twse_weight_ratio = 0; 
        self.expo_two_star_twse_weight_ratio = 0; self.expo_one_star_twse_weight_ratio = 0; 
            
        self.four_dog_twse_cpn = 0; self.three_dog_twse_cpn = 0; 
        self.two_dog_twse_cpn = 0; self.one_dog_twse_cpn = 0; 

        self.four_dog_twse_weight_ratio = 0; self.three_dog_twse_weight_ratio = 0; 
        self.two_dog_twse_weight_ratio = 0; self.one_dog_twse_weight_ratio = 0; 
            
        self.expo_four_dog_twse_cpn = 0; self.expo_three_dog_twse_cpn = 0; 
        self.expo_two_dog_twse_cpn = 0; self.expo_one_dog_twse_cpn = 0; 

        self.expo_four_dog_twse_weight_ratio = 0; self.expo_three_dog_twse_weight_ratio = 0; 
        self.expo_two_dog_twse_weight_ratio = 0; self.expo_one_dog_twse_weight_ratio = 0; 
    
    def init_count_dict_variables(self):
        self.num_cpn = 0        
        self.volatility_stock_weighted_indicator = 0
        self.volatility_weighted_indicator = 0
        self.four_star_cpn = 0; self.three_star_cpn = 0; 
        self.two_star_cpn = 0; self.one_star_cpn = 0; 
        
        self.four_star_weight_ratio = 0; self.three_star_weight_ratio = 0; 
        self.two_star_weight_ratio = 0; self.one_star_weight_ratio = 0; 
            
        self.four_dog_cpn = 0; self.three_dog_cpn = 0; 
        self.two_dog_cpn = 0; self.one_dog_cpn = 0; 

        self.four_dog_weight_ratio = 0; self.three_dog_weight_ratio = 0; 
        self.two_dog_weight_ratio = 0; self.one_dog_weight_ratio = 0; 
        
    def update_200MA_plan_on_gspreadsheet(self, start_date, end_date):
        dict_gspreadsheet = self.json_data["gSpredSheet_certificate"]        
        list_worksheet_spread = self.json_data["worksheet_gSpredSheet"]
        
        for gspreadsheet, cert_json in dict_gspreadsheet.items():
            # Declare GoogleSS() from googleSS.py
            localGoogleSS=googleSS.GoogleSS(cert_json, self.json_data, self.opt_verbose)    
            
            for count, worksheet_spread in enumerate(list_worksheet_spread):    
                t1 = time.time()
                try:
                    localGoogleSS.open_GSworksheet(gspreadsheet, worksheet_spread)
                except Exception as e:
                    logger.info(f'Error: {e}')
                    sys.exit(0)
        
                logger.info(f'Read row data of WorkSheet: {worksheet_spread} from {gspreadsheet}')
                #inital row count value 2
                inital_row_num = 5
                
                # remark 20250718           
                #localGoogleSS.update_GSpreadworksheet_200MA_plan_batch_update(inital_row_num, self.pt_stock)
            
                # remark cause Response [429 Too Many Requests]
                localGoogleSS.update_GSpreadworksheet_200MA_plan_from_pstock(inital_row_num, self.pt_stock)
            
                est_timer(t1)
    
    def update_dict_200MA_plan_on_gspreadsheet(self, start_date, end_date):
        dict_gspreadsheet = self.json_data["gSpredSheet_certificate"]        
        dict_worksheet_spread = self.json_data["dict_worksheet_gSpredSheet"]
        
        for gspreadsheet, cert_json in dict_gspreadsheet.items():
            # Declare GoogleSS() from googleSS.py
            localGoogleSS=googleSS.GoogleSS(cert_json, self.json_data, self.opt_verbose)    
            
            if bool(re.match('^twse', json_data["lastest_datastr_twse_tpex"][3].lower())  ):
                worksheet_spread = dict_worksheet_spread["twse"]
                
            elif bool(re.match('^sp500', json_data["lastest_datastr_twse_tpex"][3].lower())  ):
                worksheet_spread = dict_worksheet_spread["sp500"]
                
            elif bool(re.match('^nasdaq100', json_data["lastest_datastr_twse_tpex"][3].lower())  ):
                worksheet_spread = dict_worksheet_spread["nasdaq100"]
            
            elif bool(re.match('^twse_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
                worksheet_spread = dict_worksheet_spread["twse_volatility"]
            elif bool(re.match('^tpex_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
                worksheet_spread = dict_worksheet_spread["tpex_volatility"]    
                
            t1 = time.time()
            try:
                localGoogleSS.open_GSworksheet(gspreadsheet, worksheet_spread)
            except Exception as e:
                logger.info(f'Error: {e}')
                sys.exit(0)
        
            logger.info(f'Read row data of WorkSheet: {worksheet_spread} from {gspreadsheet}')
            #inital row count value 2
            inital_row_num = 5
            
            localGoogleSS.update_GSpreadworksheet_200MA_plan_batch_update(inital_row_num, self.pt_stock)
            
            # remark cause Response [429 Too Many Requests]
            #localGoogleSS.update_GSpreadworksheet_200MA_plan_from_pstock(inital_row_num, self.pt_stock)
            
            est_timer(t1)
    
    def update_dict_etf_momentum_on_gspreadsheet(self):
        dict_gspreadsheet = self.json_data["gSpredSheet_certificate"]        
        dict_worksheet_spread = self.json_data["dict_worksheet_gSpredSheet"]
        if bool(re.match('^twse_etf', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
                    worksheet_spread = dict_worksheet_spread["twse_etf"]
        elif bool(re.match('^twse_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
                    worksheet_spread = dict_worksheet_spread["twse_volatility"]
        elif bool(re.match('^tpex_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
                    worksheet_spread = dict_worksheet_spread["tpex_volatility"]
        elif bool(re.match('^twse_tpex_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
                    worksheet_spread = dict_worksheet_spread["twse_tpex_volatility"]
        elif bool(re.match('^sp500', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
                    worksheet_spread = dict_worksheet_spread["sp500"]
                                                                            
        for gspreadsheet, cert_json in dict_gspreadsheet.items():
            
            if bool(re.match('^200ma', gspreadsheet.lower())  ):
                # Declare GoogleSS() from googleSS.py
                localGoogleSS=googleSS.GoogleSS(cert_json, self.json_data, self.opt_verbose)    
            
                t1 = time.time()
                try:
                    localGoogleSS.open_GSworksheet(gspreadsheet, worksheet_spread)
                except Exception as e:
                    logger.info(f'Error: {e}')
                    sys.exit(0)
        
                logger.info(f'Read row data of WorkSheet: {worksheet_spread} from {gspreadsheet}')
                inital_row_num = 2
            
                localGoogleSS.update_GSpreadworksheet_etf_momentum_batch_update(self.dict_ShortMediumTerm_trend, inital_row_num)
            
                est_timer(t1)
                
    def update_MAs_status_on_gspreadsheet(self, list_MA_data):
        dict_gspreadsheet = self.json_data["gSpredSheet_certificate"]
        list_worksheet_spread = self.json_data["worksheet_gSpredSheet"]
    
        for gspreadsheet, cert_json in dict_gspreadsheet.items():
            # Declare GoogleSS() from googleSS.py
            localGoogleSS=googleSS.GoogleSS(cert_json, self.json_data, self.opt_verbose)    
            
            for count, worksheet_spread in enumerate(list_worksheet_spread):    
                t1 = time.time()
                try:
                    localGoogleSS.open_GSworksheet(gspreadsheet, worksheet_spread)
                except Exception as e:
                    logger.info(f'Error: {e}')
                    sys.exit(0)
        
                logger.info(f'Read row data of WorkSheet: {worksheet_spread} from {gspreadsheet}')
                #inital row count value 2
                inital_row_num = 2
            
                localGoogleSS.update_GSpreadworksheet_MA_status(inital_row_num, list_MA_data)
                est_timer(t1)
                # delay delay_sec secs
                #if count < len(list_worksheet_spread)-1:
                #    lib_misc.random_timer(self.json_data["list_delay_sec"][0], self.json_data["list_delay_sec"][-1])        
    
    def update_dict_MAs_status_on_gspreadsheet(self, list_MA_data):
        dict_gspreadsheet = self.json_data["gSpredSheet_certificate"]
        dict_worksheet_spread = self.json_data["dict_worksheet_gSpredSheet"]
        
        if bool(re.match('^twse', json_data["lastest_datastr_twse_tpex"][3].lower())  ):
            worksheet_spread = dict_worksheet_spread["twse"]
        elif bool(re.match('^sp500', json_data["lastest_datastr_twse_tpex"][3].lower())  ):
            worksheet_spread = dict_worksheet_spread["sp500"]
        elif bool(re.match('^nasdaq100', json_data["lastest_datastr_twse_tpex"][3].lower())  ):
            worksheet_spread = dict_worksheet_spread["nasdaq100"]
                        
        for gspreadsheet, cert_json in dict_gspreadsheet.items():
            # Declare GoogleSS() from googleSS.py
            localGoogleSS=googleSS.GoogleSS(cert_json, self.json_data, self.opt_verbose)    
            
            t1 = time.time()
            try:
                localGoogleSS.open_GSworksheet(gspreadsheet, worksheet_spread)
            except Exception as e:
                logger.info(f'Error: {e}')
                sys.exit(0)
        
            logger.info(f'Read row data of WorkSheet: {worksheet_spread} from {gspreadsheet}')
            #inital row count value 2
            inital_row_num = 2
            
            localGoogleSS.update_GSpreadworksheet_MA_status(inital_row_num, list_MA_data)
            est_timer(t1)
                        
    def calculate_TWSE_MAs_status(self):
        self.dict_twse_tpex_ticker_cpn_name = query_dic_from_pickle(self.list_path_pickle_ticker[0])
        self.dict_twse_tpex_ticker_weight_ration = query_dic_from_pickle(self.list_path_pickle_ticker[-1][0])
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'pickle fname of twse_tpex_ticker_weight_ration: \n{self.list_path_pickle_ticker[-1][0]}')
        
        list_delay_sec = self.json_data["int_delay_sec"]
            
        for idx, list_start_end_date in enumerate(self.json_data["start_end_date"]):
            str_temp = date_changer_twse(list_start_end_date[0])
            list_str_temp =str_temp.split('-')
            startdate = datetime(int(list_str_temp[0]), int(list_str_temp[1]), int(list_str_temp[2]))
            #for yfinance purpose
            str_temp = date_changer_twse_yfinance_end_date(list_start_end_date[-1])
            list_str_temp =str_temp.split('-')
            enddate = datetime(int(list_str_temp[0]), int(list_str_temp[1]), int(list_str_temp[2]))

            logger.info(f'start_date: {startdate}; end_date: {date_changer_twse(list_start_end_date[-1])}') 
            
            # Update 200MA before 4 stars 4 dogs
            self.update_200MA_plan_on_gspreadsheet(start_date=startdate, end_date=enddate)
            
            # by pstock(asyncio mode)
            self.init_count_TWSE_variables()
            self.store_TWSE_TPEX_MAs_status(start_date=startdate, end_date=enddate)    
            self.check_TWSE_TPEX_MAs_status()                                
            self.log_info_TWSE_MAs_status()
            
            # by yfinance or pstock(asyncio mode)
            self.calculate_TWSE_index_info(start_date=startdate, end_date=enddate)    
            
            #self.num_twse_cpn = 'nn'
            path_ma_fname = pathlib.Path(dirnamelog)/(date_changer_twse(list_start_end_date[-1])+f'_TWS_{self.num_twse_cpn}_MA.txt')
            path_ml_fname = pathlib.Path(dirnamelog)/(date_changer_twse(list_start_end_date[-1])+f'_ML_TWS_{self.num_twse_cpn}_MA.txt')
            
            list_cnt = [date_changer_twse(list_start_end_date[-1]), self.num_twse_cpn,
                        self.four_star_twse_cpn, self.three_star_twse_cpn, self.two_star_twse_cpn, self.one_star_twse_cpn, 
                        self.expo_four_star_twse_cpn, self.expo_three_star_twse_cpn, self.expo_two_star_twse_cpn, self.expo_one_star_twse_cpn,
                        self.four_dog_twse_cpn, self.three_dog_twse_cpn, self.two_dog_twse_cpn, self.one_dog_twse_cpn,
                        self.expo_four_dog_twse_cpn, self.expo_three_dog_twse_cpn, self.expo_two_dog_twse_cpn, self.expo_one_dog_twse_cpn,\
                        '{:.5f}'.format(self.four_star_twse_weight_ratio), '{:.5f}'.format(self.three_star_twse_weight_ratio) , 
                        '{:.5f}'.format(self.two_star_twse_weight_ratio) , '{:.5f}'.format(self.one_star_twse_weight_ratio),
                        '{:.5f}'.format(self.expo_four_star_twse_weight_ratio), '{:.5f}'.format(self.expo_three_star_twse_weight_ratio) , 
                        '{:.5f}'.format(self.expo_two_star_twse_weight_ratio), '{:.5f}'.format(self.expo_one_star_twse_weight_ratio),
                        '{:.5f}'.format(self.four_dog_twse_weight_ratio), '{:.5f}'.format(self.three_dog_twse_weight_ratio), 
                        '{:.5f}'.format(self.two_dog_twse_weight_ratio), '{:.5f}'.format(self.one_dog_twse_weight_ratio),
                        '{:.5f}'.format(self.expo_four_dog_twse_weight_ratio), '{:.5f}'.format(self.expo_three_dog_twse_weight_ratio), 
                        '{:.5f}'.format(self.expo_two_dog_twse_weight_ratio), '{:.5f}'.format(self.expo_one_dog_twse_weight_ratio),\
                        '{:.5f}'.format(self.volatility_twse_weighted_indicator),\
                        self.twse_open, self.twse_high, self.twse_low, self.twse_close, self.twse_volume]
        
            lib_misc.list_out_file(path_ma_fname, list_cnt, opt_verbose='on')
            lib_misc.list_out_ML_file(path_ml_fname, list_cnt, opt_verbose='on')
            
            self.update_MAs_status_on_gspreadsheet(list_MA_data=list_cnt)            
            
            if idx < len(self.json_data["start_end_date"])-1:
                lib_misc.random_timer(list_delay_sec[0], list_delay_sec[-1])
        
    def calculate_dict_MAs_status(self):
        if bool(re.match('^twse', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            str_ticker = '^TWII'
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["twse"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["twse"][1]
        
        elif bool(re.match('^tpex', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            str_ticker = '^TWOII'
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["tpex"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["tpex"][1]
            
        elif bool(re.match('^sp500', json_data["lastest_datastr_twse_tpex"][3].lower())  ):
            str_ticker = '^GSPC'
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["sp500"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["sp500"][1]
        
        elif bool(re.match('^nasdaq100', json_data["lastest_datastr_twse_tpex"][3].lower())  ):
            str_ticker = '^NDX'
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["nasdaq100"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["nasdaq100"][1]
        
        elif bool(re.match('^twse_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            str_ticker = '^TWII'
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["twse_volatility"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["twse_volatility"][1]
        
        elif bool(re.match('^tpex_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            str_ticker = '^TWOII'
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["tpex_volatility"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["tpex_volatility"][1]
        
        target_market = json_data["lastest_datastr_twse_tpex"][1].upper()                    
        self.dict_ticker_cpn_name = query_dic_from_pickle(fname_ticker_cpn_name)
        self.dict_ticker_weight_ration = query_dic_from_pickle(fname_ticker_weight_ration)
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'pickle fname of ticker_weight_ration: \n{fname_ticker_weight_ration}')
        
        list_delay_sec = self.json_data["int_delay_sec"]
        
        for idx, list_start_end_date in enumerate(self.json_data["start_end_date"]):
            str_temp = date_changer_twse(list_start_end_date[0])
            list_str_temp =str_temp.split('-')
            startdate = datetime(int(list_str_temp[0]), int(list_str_temp[1]), int(list_str_temp[2]))
            #for yfinance purpose
            str_temp = date_changer_twse_yfinance_end_date(list_start_end_date[-1])
            list_str_temp =str_temp.split('-')
            enddate = datetime(int(list_str_temp[0]), int(list_str_temp[1]), int(list_str_temp[2]))

            logger.info(f'start_date: {startdate}; end_date: {date_changer_twse(list_start_end_date[-1])}') 
            
            # Update 200MA before 4 stars 4 dogs
            self.update_dict_200MA_plan_on_gspreadsheet(start_date=startdate, end_date=enddate)
            
            # by pstock(asyncio mode)
            self.init_count_dict_variables()
            self.store_dict_MAs_status(start_date=startdate, end_date=enddate, \
                                        stock_end_date=date_changer_twse(list_start_end_date[-1]))    
            self.check_dict_MAs_status()                                
            self.log_info_dict_MAs_status()
            
            # log out all tickers start-dog MA status
            path_all_tickers_fname = pathlib.Path(dirnamelog)/(date_changer_twse(list_start_end_date[-1])+f'_All_Tickers_{target_market}_{self.num_cpn}_MA.txt')
            self.log_all_ticker_dict_MAs_cnts(path_all_tickers_fname, self.dict_MAs_status)
            
            # by yfinance or pstock(asyncio mode)
            self.calculate_dict_index_info(str_ticker= str_ticker, start_date=startdate, end_date=enddate)    
            
            #self.num_twse_cpn = 'nn'
            path_ma_fname = pathlib.Path(dirnamelog)/(date_changer_twse(list_start_end_date[-1])+f'_{target_market}_{self.num_cpn}_MA.txt')
            path_ml_fname = pathlib.Path(dirnamelog)/(date_changer_twse(list_start_end_date[-1])+f'_ML_{target_market}_{self.num_cpn}_MA.txt')
            
            list_cnt = [date_changer_twse(list_start_end_date[-1]), self.num_cpn,
                        self.four_star_cpn, self.three_star_cpn, self.two_star_cpn, self.one_star_cpn,\
                        self.four_dog_cpn, self.three_dog_cpn, self.two_dog_cpn, self.one_dog_cpn,\
                        '{:.5f}'.format(self.four_star_weight_ratio), '{:.5f}'.format(self.three_star_weight_ratio) , 
                        '{:.5f}'.format(self.two_star_weight_ratio) , '{:.5f}'.format(self.one_star_weight_ratio),
                        '{:.5f}'.format(self.four_dog_weight_ratio), '{:.5f}'.format(self.three_dog_weight_ratio), 
                        '{:.5f}'.format(self.two_dog_weight_ratio), '{:.5f}'.format(self.one_dog_weight_ratio),
                        '{:.5f}'.format(self.volatility_weighted_indicator),\
                        self.open, self.high, self.low, self.close, self.volume]
        
            lib_misc.list_out_file(path_ma_fname, list_cnt, opt_verbose='on')
            lib_misc.list_out_ML_file(path_ml_fname, list_cnt, opt_verbose='on')
            
            self.update_dict_MAs_status_on_gspreadsheet(list_MA_data=list_cnt)            
            
            if idx < len(self.json_data["start_end_date"])-1:
                lib_misc.random_timer(list_delay_sec[0], list_delay_sec[-1])
    
    def calculate_dict_momentum(self):
        if bool(re.match('^twse_etf', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            str_ticker = '^TWII'
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["twse_etf"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["twse_etf"][1]
        elif bool(re.match('^twse_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["twse_volatility"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["twse_volatility"][1]
        elif bool(re.match('^tpex_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["tpex_volatility"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["tpex_volatility"][1]    
        elif bool(re.match('^twse_tpex_volatility', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["twse_tpex_volatility"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["twse_tpex_volatility"][1]
        elif bool(re.match('^sp500', json_data["lastest_datastr_twse_tpex"][1].lower())  ):
            fname_ticker_cpn_name = self.dict_path_pickle_ticker["sp500"][0]
            fname_ticker_weight_ration = self.dict_path_pickle_ticker["sp500"][1]
                    
        target_market = json_data["lastest_datastr_twse_tpex"][1].upper()                    
        self.dict_ticker_cpn_name = query_dic_from_pickle(fname_ticker_cpn_name)
        self.dict_ticker_weight_ration = query_dic_from_pickle(fname_ticker_weight_ration)
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'pickle fname of ticker_weight_ration: \n{fname_ticker_weight_ration}')
        
        list_delay_sec = self.json_data["int_delay_sec"]
        
        for idx, list_start_end_date in enumerate(self.json_data["start_end_date"]):
            str_temp = date_changer_twse(list_start_end_date[0])
            list_str_temp =str_temp.split('-')
            startdate = datetime(int(list_str_temp[0]), int(list_str_temp[1]), int(list_str_temp[2]))
            #for yfinance purpose
            str_temp = date_changer_twse_yfinance_end_date(list_start_end_date[-1])
            list_str_temp =str_temp.split('-')
            enddate = datetime(int(list_str_temp[0]), int(list_str_temp[1]), int(list_str_temp[2]))

            logger.info(f'start_date: {startdate}; end_date: {date_changer_twse(list_start_end_date[-1])}') 
            
            # by pstock(asyncio mode)
            self.init_count_dict_variables()
            ## remark by combine two function into store_dict_MAs_status_ShortMediumTerm_trend
            ##self.store_dict_MAs_status(start_date=startdate, end_date=enddate)    
            ##self.store_dict_ShortMediumTerm_trend(start_date=startdate, end_date=enddate)
            
            self.store_dict_MAs_status_ShortMediumTerm_trend(start_date=startdate, end_date=enddate, \
                                                                stock_end_date=date_changer_twse(list_start_end_date[-1]))
                
            self.check_dict_MAs_status()                                
            self.log_info_dict_MAs_status()
            # log out all tickers start-dog MA status
            path_all_tickers_fname = pathlib.Path(dirnamelog)/(date_changer_twse(list_start_end_date[-1])+f'_All_Tickers_{target_market}_{self.num_cpn}_MA.txt')
            self.log_all_ticker_dict_MAs_cnts(path_all_tickers_fname, self.dict_MAs_status)
                        
            # log out all tickers start-dog MA status
            path_all_tickers_fname = pathlib.Path(dirnamelog)/(date_changer_twse(list_start_end_date[-1])+f'_All_Tickers_{target_market}_{self.num_cpn}_ShortMediumTerm_trend.txt')
            self.log_all_ticker_dict_MAs_cnts(path_all_tickers_fname, self.dict_ShortMediumTerm_trend)
            
            # Update etf momentum
            self.update_dict_etf_momentum_on_gspreadsheet()
            
            if idx < len(self.json_data["start_end_date"])-1:
                lib_misc.random_timer(list_delay_sec[0], list_delay_sec[-1])
                                                                            
    def init_count_TPEX_variables(self):
        self.num_tpex_cpn = 0
        self.volatility_TPEX_weighted_indicator = 0
        self.four_star_tpex_cpn = 0; self.three_star_tpex_cpn = 0; 
        self.two_star_tpex_cpn = 0;  self.one_star_tpex_cpn = 0; 
            
        self.four_star_tpex_weight_ratio = 0; self.three_star_tpex_weight_ratio = 0; 
        self.two_star_tpex_weight_ratio = 0; self.one_star_tpex_weight_ratio = 0; 
            
        self.expo_four_star_tpex_cpn = 0; self.expo_three_star_tpex_cpn = 0; 
        self.expo_two_star_tpex_cpn = 0; self.expo_one_star_tpex_cpn = 0; 
            
        self.expo_four_star_tpex_weight_ratio = 0; self.expo_three_star_tpex_weight_ratio = 0; 
        self.expo_two_star_tpex_weight_ratio = 0; self.expo_one_star_tpex_weight_ratio = 0; 
            
        self.four_dog_tpex_cpn = 0; self.three_dog_tpex_cpn = 0;   
        self.two_dog_tpex_cpn = 0; self.one_dog_tpex_cpn = 0      
            
        self.four_dog_tpex_weight_ratio = 0; self.three_dog_tpex_weight_ratio = 0;   
        self.two_dog_tpex_weight_ratio = 0; self.one_dog_tpex_weight_ratio = 0      
            
        self.expo_four_dog_tpex_cpn = 0; self.expo_three_dog_tpex_cpn = 0;  
        self.expo_two_dog_tpex_cpn = 0; self.expo_one_dog_tpex_cpn = 0; 
            
        self.expo_four_dog_tpex_weight_ratio = 0; self.expo_three_dog_tpex_weight_ratio = 0;  
        self.expo_two_dog_tpex_weight_ratio = 0; self.expo_one_dog_tpex_weight_ratio = 0
        
    def calculate_TPEX_MAs_status(self):
        self.dict_twse_tpex_ticker_cpn_name = query_dic_from_pickle(self.list_path_pickle_ticker[1])
        self.dict_twse_tpex_ticker_weight_ration = query_dic_from_pickle(self.list_path_pickle_ticker[-1][1])
        list_delay_sec = self.json_data["int_delay_sec"]
        
        for idx, list_start_end_date in enumerate(self.json_data["start_end_date"]):
            str_temp = date_changer_twse(list_start_end_date[0])
            list_str_temp =str_temp.split('-')
            startdate = datetime(list_str_temp[0], list_str_temp[1], list_str_temp[2])
            #for yfinance purpose
            str_temp = date_changer_twse_yfinance_end_date(list_start_end_date[-1])
            list_str_temp =str_temp.split('-')
            enddate = datetime(list_str_temp[0], list_str_temp[1], list_str_temp[2])
            
            logger.info(f'start_date: {startdate}; end_date: {date_changer_twse(list_start_end_date[-1])}') 
            
            self.init_count_TPEX_variables()
            
            self.calculate_TPEX_index_info(start_date=startdate, end_date=enddate)    
            
            self.store_TWSE_TPEX_MAs_status(start_date=startdate, end_date=enddate)    
            self.check_TWSE_TPEX_MAs_status()
        
            self.log_info_TPEX_MAs_status()

            #self.calculate_TPEX_index_info(start_date=startdate, end_date=enddate)    
            
            path_ma_fname = pathlib.Path(dirnamelog)/(date_changer_twse(list_start_end_date[-1])+f'_OTC_{self.num_tpex_cpn}_MA.txt')
            path_ml_fname = pathlib.Path(dirnamelog)/(date_changer_twse(list_start_end_date[-1])+f'_ML_OTC_{self.num_tpex_cpn}_MA.txt')
            
            list_cnt = [date_changer_twse(list_start_end_date[-1]), self.num_tpex_cpn,
                        self.four_star_tpex_cpn, self.three_star_tpex_cpn, self.two_star_tpex_cpn, self.one_star_tpex_cpn, 
                        self.expo_four_star_tpex_cpn, self.expo_three_star_tpex_cpn, self.expo_two_star_tpex_cpn, self.expo_one_star_tpex_cpn,
                        self.four_dog_tpex_cpn, self.three_dog_tpex_cpn, self.two_dog_tpex_cpn, self.one_dog_tpex_cpn, 
                        self.expo_four_dog_tpex_cpn, self.expo_three_dog_tpex_cpn, self.expo_two_dog_tpex_cpn, self.expo_one_dog_tpex_cpn,\
                        self.four_star_tpex_weight_ratio, self.three_star_tpex_weight_ratio, self.two_star_tpex_weight_ratio, self.one_star_tpex_weight_ratio, 
                        self.expo_four_star_tpex_weight_ratio, self.expo_three_star_tpex_weight_ratio, self.expo_two_star_tpex_weight_ratio, self.expo_one_star_tpex_weight_ratio,
                        self.four_dog_tpex_weight_ratio, self.three_dog_tpex_weight_ratio, self.two_dog_tpex_weight_ratio, self.one_dog_tpex_weight_ratio, 
                        self.expo_four_dog_tpex_weight_ratio, self.expo_three_dog_tpex_weight_ratio, self.expo_two_dog_tpex_weight_ratio, self.expo_one_dog_tpex_weight_ratio,\
                        self.tpex_open, self.tpex_high, self.tpex_low, self.tpex_close, self.tpex_volume]   
        
            lib_misc.list_out_file(path_ma_fname, list_cnt, opt_verbose='on')        
            lib_misc.list_out_ML_file(path_ml_fname, list_cnt, opt_verbose='on')
            
            if idx < len(self.json_data["start_end_date"])-1:
                lib_misc.random_timer(list_delay_sec[0], list_delay_sec[-1])
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='stock indicator')
    parser.add_argument('--conf_json', type=str, default='config.json', help='Config json')
    #parser.add_argument('--gspred_json', type=str, default='xxxx.json', help='Google Sheet Certi json')
    
    args = parser.parse_args()
    
    logger_set(strdirname)
    
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    
    json_file= args.conf_json
    json_gsheet= None#args.gspred_json
    
    json_path_file = pathlib.Path(strdirname)/json_file
    
    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )    
        est_timer(t0)
        sys.exit()

    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f)  
        
    opt_verbose= 'OFF'
    
    #path_xlsx_stock_id=  'twse_tpex_ticker.xlsx'
    list_path_pickle_ticker= json_data["twse_otc_id_pickle"]#['twse_ticker.pickle', 'tpex_ticker.pickle', 'twse_tpex_ticker.pickle']
    dict_path_pickle_ticker= json_data["dict_twse_otc_us_id_pickle"]
    
    # for accelerate get twse tpex idx purpose   
    local_stock= yahooFinance.Stock(json_data)        
    
    #logger.info(f'json_data["lastest_datastr_twse_tpex"][0].lower(): {json_data["lastest_datastr_twse_tpex"][0].lower()}' )    
    
    if json_data["lastest_datastr_twse_tpex"][0].lower() == "request":
        store_twse_tpex_ticker(json_data, list_path_pickle_ticker, path_csv_stock_id= '', opt_verbose= 'On')
    elif json_data["lastest_datastr_twse_tpex"][0].lower() == "csv":        
        pickle_ticker_weight_ration = store_twse_tpex_ticker_weight_ration_fromCSV(json_data, dict_path_pickle_ticker, path_csv_stock_id= '', opt_verbose= 'On')
        
    else:        
        list_path_pickle_ticker.append(['twse_ticker_weight_ration.pickle', 'tpex_ticker_weight_ration.pickle'])
        local_twse_tpex_ma_status = TWSE_TPEX_MAs_status(json_data, json_gsheet, dict_path_pickle_ticker, list_path_pickle_ticker, \
                                                            local_stock, opt_verbose)
        
        if json_data["lastest_datastr_twse_tpex"][1].lower() == "all":
            local_twse_tpex_ma_status.calculate_TWSE_MAs_status()
            local_twse_tpex_ma_status.calculate_TPEX_MAs_status()
        elif bool(re.match('twse$', json_data["lastest_datastr_twse_tpex"][1].lower()) ):
            logger.info(f'json_data["lastest_datastr_twse_tpex"][1]: {json_data["lastest_datastr_twse_tpex"][1]}' )
            #local_twse_tpex_ma_status.calculate_TWSE_MAs_status()
            local_twse_tpex_ma_status.calculate_dict_MAs_status()
        
        elif bool(re.match('tpex$', json_data["lastest_datastr_twse_tpex"][1].lower()) ):
            local_twse_tpex_ma_status.calculate_TPEX_MAs_status()        
        
        elif json_data["lastest_datastr_twse_tpex"][1].lower() == "twse_etf":
            logger.info(f'json_data["lastest_datastr_twse_tpex"][1]: {json_data["lastest_datastr_twse_tpex"][1]}' )
            local_twse_tpex_ma_status.calculate_dict_momentum()
        
        elif bool(re.match('t[w|p][s|e][e|x]_volatility', json_data["lastest_datastr_twse_tpex"][1].lower()) ):
            logger.info(f'json_data["lastest_datastr_twse_tpex"][1]: {json_data["lastest_datastr_twse_tpex"][1]}' )    
            local_twse_tpex_ma_status.calculate_dict_momentum()
        
        elif json_data["lastest_datastr_twse_tpex"][1].lower() == "sp500":
            logger.info(f'json_data["lastest_datastr_twse_tpex"][1]: {json_data["lastest_datastr_twse_tpex"][1]}' )
            local_twse_tpex_ma_status.calculate_dict_momentum()
                    
        else:
            #logger.info(f'json_data["lastest_datastr_twse_tpex"][1]: {json_data["lastest_datastr_twse_tpex"][1]}' )    
            local_twse_tpex_ma_status.calculate_dict_MAs_status()
                
    est_timer(t0)    