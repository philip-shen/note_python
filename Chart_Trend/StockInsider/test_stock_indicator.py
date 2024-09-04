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

import twseotc_stocks.lib_misc as lib_misc
from insider.logger_setup import *
from insider.stock import *

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
    datestr = json_data["lastest_datastr_twse_tpex"][-1]#'20240801'
    r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
    # 整理資料，變成表格
    df_twse_website_info = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
        
    ##### 上櫃公司
    datestr = date_changer(json_data["lastest_datastr_twse_tpex"][-1])#'113/08/01'
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
    

def query_twse_tpex_ticker(path_pickle_stock_id, opt_verbose= 'OFF'):
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

def date_changer_twse( date):
    
    year = date[:4]
    year = str(int(year))
    month = date[4:6]
    day = date[6:]
        
    return year+"-"+month+"-"+day

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
    end_date = date_changer_twse(json_data["start_end_date"][1])

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
    end_date = date_changer_twse(json_data["start_end_date"][1])

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
    def __init__(self, json_data: dict, list_path_pickle_ticker: list,  opt_verbose='OFF'):
        
        self.json_data = json_data
        self.list_path_pickle_ticker = list_path_pickle_ticker
        self.opt_verbose = opt_verbose

        self.num_twse_cpn = 0; self.num_tpex_cpn = 0
        
        self.four_star_twse_cpn = 0; self.four_star_tpex_cpn = 0; 
        self.three_star_twse_cpn = 0; self.three_star_tpex_cpn = 0; 
        self.two_star_twse_cpn = 0; self.two_star_tpex_cpn = 0; 
        self.one_star_twse_cpn = 0; self.one_star_tpex_cpn = 0; 
        
        self.expo_four_star_twse_cpn = 0; self.expo_four_star_tpex_cpn = 0; 
        self.expo_three_star_twse_cpn = 0; self.expo_three_star_tpex_cpn = 0; 
        self.expo_two_star_twse_cpn = 0; self.expo_two_star_tpex_cpn = 0; 
        self.expo_one_star_twse_cpn = 0; self.expo_one_star_tpex_cpn = 0; 
        
        self.four_dog_twse_cpn = 0; self.four_dog_tpex_cpn = 0; 
        self.three_dog_twse_cpn = 0; self.three_dog_tpex_cpn = 0
        self.two_dog_twse_cpn = 0; self.two_dog_tpex_cpn = 0; 
        self.one_dog_twse_cpn = 0; self.one_dog_tpex_cpn = 0      
        
        self.expo_four_dog_twse_cpn = 0; self.expo_four_dog_tpex_cpn = 0; 
        self.expo_three_dog_twse_cpn = 0; self.expo_three_dog_tpex_cpn = 0; 
        self.expo_two_dog_twse_cpn = 0; self.expo_two_dog_tpex_cpn = 0; 
        self.expo_one_dog_twse_cpn = 0; self.expo_one_dog_tpex_cpn = 0; 
        
    def store_TWSE_TPEX_MAs_status(self):
        list_MAs_status = []
        start_date = date_changer_twse(json_data["start_end_date"][0])
        end_date = date_changer_twse(json_data["start_end_date"][1])

        for ticker, cpn_name in self.dict_twse_tpex_ticker_cpn_name.items():
            #logger.info('\n ticker: {}; cpn_name: {}'.format(key, value) )    
            ##### 上市公司 or ETF or 正2 ETF
            if bool(re.match('^[0-9][0-9][0-9][0-9].TW$', ticker)) or \
                bool(re.match('^00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('^00[0-9][0-9][0-9]L.TW$', ticker))  :
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
                '''
                if bool(re.match('^00951.TW$', ticker) ):
                    continue 
                
                logger.info(f"ticker: {target_ticker}; stock name: {cpn_name}")    
                                 
                #yf_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
                #four_flag, three_flag, four_MAs, three_MAs, close, four_dog, three_dog = check_MAs_status(yf_data, opt_verbose='OFF')            
            
                local_stock_indicator = stock_indicator(ticker=target_ticker, startdate= start_date, enddate= end_date)
                local_stock_indicator.check_MAs_status()            
                local_stock_indicator.filter_MAs_status()
            
                dict_temp = {
                    "ticker" : target_ticker,
                    "stock_name": stock_name,
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
                    "2_dog": local_stock_indicator.two_dog,
                    "1_dog": local_stock_indicator.one_dog,
                    
                    "Expo_4_dog": local_stock_indicator.four_E_dog,
                    "Expo_3_dog": local_stock_indicator.three_E_dog,
                    "Expo_2_dog": local_stock_indicator.two_E_dog,
                    "Expo_1_dog": local_stock_indicator.one_E_dog,
                    
                    "MAs_status": local_stock_indicator.stock_MA_status,
                }
                list_MAs_status.append(dict_temp)
                
                #logger.info(f'dict_temp: {dict_temp}')

        self.TWSE_TPEX_MAs_status = list_MAs_status

    def count_4_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'four_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為四海遊龍型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.four_star_twse_cpn += 1                     
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.four_star_tpex_cpn += 1 

    def count_3_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'three_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):    
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為三陽開泰型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.three_star_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.three_star_tpex_cpn += 1 
    
    def count_2_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'two_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):        
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為雙囍臨門型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.two_star_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.two_star_tpex_cpn += 1 
    
    def count_1_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'one_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):                        
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為一星報喜型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.one_star_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.one_star_tpex_cpn += 1 
    
    def count_4_expo_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_four_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_四海遊龍型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_four_star_twse_cpn += 1                     
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_four_star_tpex_cpn += 1 
    
    def count_3_expo_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_three_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為指數_三陽開泰型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_three_star_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_three_star_tpex_cpn += 1 
    
    def count_2_expo_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_two_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):    
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為指數_雙囍臨門型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_two_star_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_two_star_tpex_cpn += 1 
    
    def count_1_expo_star_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_one_star' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):            
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為指數_一星報喜型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_one_star_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_one_star_tpex_cpn += 1
                                                            
    def count_4_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'four_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):            
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為四腳朝天型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.four_dog_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.four_dog_tpex_cpn += 1 
    
    def count_3_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'three_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):                
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為三人成虎型股票!!')                
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.three_dog_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.three_dog_tpex_cpn += 1 
    
    def count_2_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'two_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):                
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為二竪作惡型股票!!')                
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.two_dog_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.two_dog_tpex_cpn += 1 
    
    def count_1_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'one_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):                
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}: 為一敗塗地型股票!!')                
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.one_dog_twse_cpn += 1 
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.one_dog_tpex_cpn += 1 
    
    def count_4_expo_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_four_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_四腳朝天型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_four_dog_twse_cpn += 1                     
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_four_dog_tpex_cpn += 1 
    
    def count_3_expo_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_three_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_三人成虎型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_three_dog_twse_cpn += 1                     
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_three_dog_tpex_cpn += 1 
    
    def count_2_expo_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_two_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_二竪作惡型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_two_dog_twse_cpn += 1                     
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_two_dog_tpex_cpn += 1 
                
    def count_1_expo_dog_num(self, twse_tpex_ticker_MAs_info):
        if twse_tpex_ticker_MAs_info["MAs_status"] == 'Expo_one_dog' and (twse_tpex_ticker_MAs_info["close"] >= 20.0):
            logger.info(f'{twse_tpex_ticker_MAs_info["ticker"]} {twse_tpex_ticker_MAs_info["stock_name"]}:為指數_一敗塗地型股票!!')
            if bool(re.search('TW$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_one_dog_twse_cpn += 1                     
            elif bool(re.search('TWO$', twse_tpex_ticker_MAs_info["ticker"])):
                self.expo_one_dog_tpex_cpn += 1 
                                                                                        
    def check_TWSE_TPEX_MAs_status(self):
        
        for dict_twse_tpex_ticker_MAs in self.TWSE_TPEX_MAs_status:
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
            
            if bool(re.search('TW$', dict_twse_tpex_ticker_MAs["ticker"])):
                self.num_twse_cpn += 1 
            elif bool(re.search('TWO$', dict_twse_tpex_ticker_MAs["ticker"])):
                self.num_tpex_cpn += 1    
            
    def calculate_TWSE_TPEX_MAs_status(self):
        self.dict_twse_tpex_ticker_cpn_name = query_twse_tpex_ticker(self.list_path_pickle_ticker[-1])
    
        #for key, value in dict_twse_tpex_ticker_cpn_name.items():
        #        logger.info('\n ticker: {}; cpn_name: {}'.format(key, value) )
    
        self.store_TWSE_TPEX_MAs_status()    
        self.check_TWSE_TPEX_MAs_status()
                                
        logger.info(f'TWSE 股票家數: {self.num_twse_cpn}' )    
        logger.info('TWSE 四海遊龍型股票家數: {} %:{:.3f}; TWSE 三陽開泰型股票家數: {} %:{:.3f}'.format(\
                self.four_star_twse_cpn, self.four_star_twse_cpn/self.num_twse_cpn, 
                self.three_star_twse_cpn, self.three_star_twse_cpn/self.num_twse_cpn) )
        logger.info('TWSE 雙囍臨門型股票家數: {} %:{:.3f}; TWSE 一星報喜型股票家數: {} %:{:.3f}'.format(\
                self.two_star_twse_cpn, self.two_star_twse_cpn/self.num_twse_cpn, 
                self.one_star_twse_cpn, self.one_star_twse_cpn/self.num_twse_cpn) )
        
        logger.info('TWSE 指數_四海遊龍型股票家數: {} %:{:.3f}; TWSE 指數_三陽開泰型股票家數: {} %:{:.3f}'.format(\
                self.expo_four_star_twse_cpn, self.expo_four_star_twse_cpn/self.num_twse_cpn, 
                self.expo_three_star_twse_cpn, self.expo_three_star_twse_cpn/self.num_twse_cpn) )
        
        logger.info('TWSE 指數_雙囍臨門型股票家數: {} %:{:.3f}; TWSE 指數_一星型股票家數: {} %:{:.3f}'.format(\
                self.expo_two_star_twse_cpn, self.expo_two_star_twse_cpn/self.num_twse_cpn, 
                self.expo_one_star_twse_cpn, self.expo_one_star_twse_cpn/self.num_twse_cpn) )
        
        logger.info('TWSE 四腳朝天型股票家數: {} %:{:.3f}; TWSE 三笑杯型股票家數: {} %:{:.3f}'.format(\
                self.four_dog_twse_cpn, self.four_dog_twse_cpn/self.num_twse_cpn, 
                self.three_dog_twse_cpn, self.three_dog_twse_cpn/self.num_twse_cpn) )
        
        logger.info(f'TPEX 股票家數: {self.num_tpex_cpn}' )    
        logger.info('TPEX 四海遊龍型股票家數: {} %:{:.3f}; TPEX 三陽開泰型股票家數: {} %:{:.3f}'.format(\
                self.four_star_tpex_cpn, self.four_star_tpex_cpn/self.num_tpex_cpn, 
                self.three_star_tpex_cpn, self.three_star_tpex_cpn/self.num_tpex_cpn) )
        
        logger.info('TPEX 雙囍臨門型股票家數: {} %:{:.3f}; TPEX 一星報喜型股票家數: {} %:{:.3f}'.format(\
                self.two_star_tpex_cpn, self.two_star_tpex_cpn/self.num_tpex_cpn, 
                self.one_star_tpex_cpn, self.one_star_tpex_cpn/self.num_tpex_cpn) )
        
        logger.info('TPEX 指數_四海遊龍型股票家數: {} %:{:.3f}; TPEX 指數_三陽開泰型股票家數: {} %:{:.3f}'.format(\
                self.expo_four_star_tpex_cpn, self.expo_four_star_tpex_cpn/self.num_twse_cpn, 
                self.expo_three_star_tpex_cpn, self.expo_three_star_tpex_cpn/self.num_twse_cpn) )
        
        logger.info('TPEX 指數_雙囍臨門型股票家數: {} %:{:.3f}; TPEX 指數_一星型股票家數: {} %:{:.3f}'.format(\
                self.expo_two_star_tpex_cpn, self.expo_two_star_tpex_cpn/self.num_twse_cpn, 
                self.expo_one_star_tpex_cpn, self.expo_one_star_tpex_cpn/self.num_twse_cpn) )
        
        logger.info('TPEX 四腳朝天型股票家數: {} %:{:.3f}; TPEX 三笑杯型股票家數: {} %:{:.3f}'.format(\
                self.four_dog_tpex_cpn, self.four_dog_tpex_cpn/self.num_tpex_cpn, 
                self.three_dog_tpex_cpn, self.three_dog_tpex_cpn/self.num_tpex_cpn) )   
         
        logger.info(f'\n{self.four_star_twse_cpn}\n{self.three_star_twse_cpn}\n{self.two_star_twse_cpn}\n{self.one_star_twse_cpn}\n{self.expo_four_star_twse_cpn}\n{self.expo_three_star_twse_cpn}\n{self.expo_two_star_twse_cpn}\n{self.expo_one_star_twse_cpn}\n{self.four_dog_twse_cpn}\n{self.three_dog_twse_cpn}') 
        #logger.info(f'\n{self.expo_four_star_twse_cpn}\n{self.expo_three_star_twse_cpn}\n{self.expo_two_star_twse_cpn}\n{self.expo_one_star_twse_cpn}') 
        #logger.info(f'\n{self.four_dog_twse_cpn}\n{self.three_dog_twse_cpn}')
        
        logger.info(f'\n{self.four_star_tpex_cpn}\n{self.three_star_tpex_cpn}\n{self.two_star_tpex_cpn}\n{self.one_star_tpex_cpn}\n{self.expo_four_star_tpex_cpn}\n{self.expo_three_star_tpex_cpn}\n{self.expo_two_star_tpex_cpn}\n{self.expo_one_star_tpex_cpn}\n{self.four_dog_tpex_cpn}\n{self.three_dog_tpex_cpn}') 
        #logger.info(f'\n{self.expo_four_star_tpex_cpn}\n{self.expo_three_star_tpex_cpn}\n{self.expo_two_star_tpex_cpn}\n{self.expo_one_star_tpex_cpn}') 
        #logger.info(f'\n{self.four_dog_tpex_cpn}\n{self.three_dog_tpex_cpn}')
    
    def calculate_TWSE_MAs_status(self):
        self.dict_twse_tpex_ticker_cpn_name = query_twse_tpex_ticker(self.list_path_pickle_ticker[0])
    
        self.store_TWSE_TPEX_MAs_status()    
        self.check_TWSE_TPEX_MAs_status()
                                
        logger.info(f'TWSE 股票家數: {self.num_twse_cpn}' )    
        logger.info('TWSE 四海遊龍型股票家數: {} %:{:.3f}; TWSE 三陽開泰型股票家數: {} %:{:.3f}'.format(\
                self.four_star_twse_cpn, self.four_star_twse_cpn/self.num_twse_cpn, 
                self.three_star_twse_cpn, self.three_star_twse_cpn/self.num_twse_cpn) )
        logger.info('TWSE 雙囍臨門型股票家數: {} %:{:.3f}; TWSE 一星報喜型股票家數: {} %:{:.3f}'.format(\
                self.two_star_twse_cpn, self.two_star_twse_cpn/self.num_twse_cpn, 
                self.one_star_twse_cpn, self.one_star_twse_cpn/self.num_twse_cpn) )
        
        logger.info('TWSE 指數_四海遊龍型股票家數: {} %:{:.3f}; TWSE 指數_三陽開泰型股票家數: {} %:{:.3f}'.format(\
                self.expo_four_star_twse_cpn, self.expo_four_star_twse_cpn/self.num_twse_cpn, 
                self.expo_three_star_twse_cpn, self.expo_three_star_twse_cpn/self.num_twse_cpn) )
        
        logger.info('TWSE 指數_雙囍臨門型股票家數: {} %:{:.3f}; TWSE 指數_一星報喜型股票家數: {} %:{:.3f}'.format(\
                self.expo_two_star_twse_cpn, self.expo_two_star_twse_cpn/self.num_twse_cpn, 
                self.expo_one_star_twse_cpn, self.expo_one_star_twse_cpn/self.num_twse_cpn) )
        
        logger.info('TWSE 四腳朝天型股票家數: {} %:{:.3f}; TWSE 三人成虎型股票家數: {} %:{:.3f}'.format(\
                self.four_dog_twse_cpn, self.four_dog_twse_cpn/self.num_twse_cpn, 
                self.three_dog_twse_cpn, self.three_dog_twse_cpn/self.num_twse_cpn) )
        
        logger.info('TWSE 二竪作惡型股票家數: {} %:{:.3f}; TWSE 一敗塗地型股票家數: {} %:{:.3f}'.format(\
                self.two_dog_twse_cpn, self.one_dog_twse_cpn/self.num_twse_cpn, 
                self.two_dog_twse_cpn, self.one_dog_twse_cpn/self.num_twse_cpn) )
        
        logger.info('TWSE 指數_四腳朝天型股票家數: {} %:{:.3f}; TWSE 指數_三人成虎型股票家數: {} %:{:.3f}'.format(\
                self.expo_four_dog_twse_cpn, self.expo_four_dog_twse_cpn/self.num_twse_cpn, 
                self.expo_three_dog_twse_cpn, self.expo_three_dog_twse_cpn/self.num_twse_cpn) )
        
        logger.info('TWSE 指數_二竪作惡型股票家數: {} %:{:.3f}; TWSE 指數_一敗塗地型股票家數: {} %:{:.3f}'.format(\
                self.expo_two_star_twse_cpn, self.expo_two_star_twse_cpn/self.num_twse_cpn, 
                self.expo_one_star_twse_cpn, self.expo_one_star_twse_cpn/self.num_twse_cpn) )
        
        path_fname = pathlib.Path(dirnamelog)/(json_data["start_end_date"][-1]+'_TWS_MA.txt')
        list_cnt = [self.num_twse_cpn,
                    self.four_star_twse_cpn, self.three_star_twse_cpn, self.two_star_twse_cpn, self.one_star_twse_cpn, 
                    self.expo_four_star_twse_cpn, self.expo_three_star_twse_cpn, self.expo_two_star_twse_cpn, self.expo_one_star_twse_cpn,
                    
                    self.four_dog_twse_cpn, self.three_dog_twse_cpn, self.two_dog_twse_cpn, self.one_dog_twse_cpn,
                    self.expo_four_dog_twse_cpn, self.expo_three_dog_twse_cpn, self.expo_two_dog_twse_cpn, self.expo_one_dog_twse_cpn
                    ]
        
        lib_misc.list_out_file(path_fname, list_cnt, opt_verbose='on')
        
        path_fname = pathlib.Path(dirnamelog)/(json_data["start_end_date"][-1]+'_ML_TWS_MA.txt')
        lib_misc.list_out_ML_file(path_fname, list_cnt, opt_verbose='on')
        
    def calculate_TPEX_MAs_status(self):
        self.dict_twse_tpex_ticker_cpn_name = query_twse_tpex_ticker(self.list_path_pickle_ticker[1])
    
        self.store_TWSE_TPEX_MAs_status()    
        self.check_TWSE_TPEX_MAs_status()
        
        logger.info(f'TPEX 股票家數: {self.num_tpex_cpn}' )    
        logger.info('TPEX 四海遊龍型股票家數: {} %:{:.3f}; TPEX 三陽開泰型股票家數: {} %:{:.3f}'.format(\
                self.four_star_tpex_cpn, self.four_star_tpex_cpn/self.num_tpex_cpn, 
                self.three_star_tpex_cpn, self.three_star_tpex_cpn/self.num_tpex_cpn) )
        
        logger.info('TPEX 雙囍臨門型股票家數: {} %:{:.3f}; TPEX 一星報喜型股票家數: {} %:{:.3f}'.format(\
                self.two_star_tpex_cpn, self.two_star_tpex_cpn/self.num_tpex_cpn, 
                self.one_star_tpex_cpn, self.one_star_tpex_cpn/self.num_tpex_cpn) )
        
        logger.info('TPEX 指數_四海遊龍型股票家數: {} %:{:.3f}; TPEX 指數_三陽開泰型股票家數: {} %:{:.3f}'.format(\
                self.expo_four_star_tpex_cpn, self.expo_four_star_tpex_cpn/self.num_tpex_cpn, 
                self.expo_three_star_tpex_cpn, self.expo_three_star_tpex_cpn/self.num_tpex_cpn) )
        
        logger.info('TPEX 指數_雙囍臨門型股票家數: {} %:{:.3f}; TPEX 指數_一星型股票家數: {} %:{:.3f}'.format(\
                self.expo_two_star_tpex_cpn, self.expo_two_star_tpex_cpn/self.num_tpex_cpn, 
                self.expo_one_star_tpex_cpn, self.expo_one_star_tpex_cpn/self.num_tpex_cpn) )
        
        logger.info('TPEX 四腳朝天型股票家數: {} %:{:.3f}; TPEX 三笑杯型股票家數: {} %:{:.3f}'.format(\
                self.four_dog_tpex_cpn, self.four_dog_tpex_cpn/self.num_tpex_cpn, 
                self.three_dog_tpex_cpn, self.three_dog_tpex_cpn/self.num_tpex_cpn) ) 
        
        logger.info('TPEX 二竪作惡型股票家數: {} %:{:.3f}; TPEX 一敗塗地型股票家數: {} %:{:.3f}'.format(\
                self.two_dog_tpex_cpn, self.one_dog_tpex_cpn/self.num_tpex_cpn, 
                self.two_dog_tpex_cpn, self.one_dog_tpex_cpn/self.num_tpex_cpn) )
        
        logger.info('TPEX 指數_四腳朝天型股票家數: {} %:{:.3f}; TPEX 指數_三人成虎型股票家數: {} %:{:.3f}'.format(\
                self.expo_four_dog_tpex_cpn, self.expo_four_dog_tpex_cpn/self.num_tpex_cpn, 
                self.expo_three_dog_tpex_cpn, self.expo_three_dog_tpex_cpn/self.num_tpex_cpn) )
        
        logger.info('TPEX 指數_二竪作惡型股票家數: {} %:{:.3f}; TPEX 指數_一敗塗地型股票家數: {} %:{:.3f}'.format(\
                self.expo_two_dog_tpex_cpn, self.expo_two_dog_tpex_cpn/self.num_tpex_cpn, 
                self.expo_one_dog_tpex_cpn, self.expo_one_dog_tpex_cpn/self.num_tpex_cpn) )
        
        path_fname = pathlib.Path(dirnamelog)/(json_data["start_end_date"][-1]+'_OTC_MA.txt')
        list_cnt = [self.num_tpex_cpn,
                    self.four_star_tpex_cpn, self.three_star_tpex_cpn, self.two_star_tpex_cpn, self.one_star_tpex_cpn, 
                    self.expo_four_star_tpex_cpn, self.expo_three_star_tpex_cpn, self.expo_two_star_tpex_cpn, self.expo_one_star_tpex_cpn, 
                    
                    self.four_dog_tpex_cpn, self.three_dog_tpex_cpn, self.two_dog_tpex_cpn, self.one_dog_tpex_cpn, 
                    self.expo_four_dog_tpex_cpn, self.expo_three_dog_tpex_cpn, self.expo_two_dog_tpex_cpn, self.expo_one_dog_tpex_cpn
                    ]
        
        lib_misc.list_out_file(path_fname, list_cnt, opt_verbose='on')
        
        path_fname = pathlib.Path(dirnamelog)/(json_data["start_end_date"][-1]+'_ML_OTC_MA.txt')
        lib_misc.list_out_ML_file(path_fname, list_cnt, opt_verbose='on')
        
        logger.info('\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.\
                    format(self.num_twse_cpn,                    
                            self.four_star_twse_cpn, self.three_star_twse_cpn, self.three_star_twse_cpn, self.one_star_twse_cpn,\
                            self.expo_four_star_twse_cpn, self.expo_three_star_twse_cpn, self.expo_two_star_twse_cpn, self.expo_one_star_twse_cpn,\
                            self.four_dog_twse_cpn, self.three_dog_twse_cpn, self.two_dog_twse_cpn, self.one_dog_twse_cpn,\
                            self.expo_four_dog_twse_cpn, self.expo_three_dog_twse_cpn, self.expo_two_dog_twse_cpn, self.expo_one_dog_twse_cpn)) 
        
        logger.info('\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.\
                    format(self.num_tpex_cpn,                    
                            self.four_star_tpex_cpn, self.three_star_tpex_cpn, self.two_star_tpex_cpn, self.one_star_tpex_cpn,\
                            self.expo_four_star_tpex_cpn, self.expo_three_star_tpex_cpn, self.expo_two_star_tpex_cpn, self.expo_one_star_tpex_cpn,\
                            self.four_dog_tpex_cpn, self.three_dog_tpex_cpn, self.two_dog_tpex_cpn, self.one_dog_tpex_cpn,\
                            self.expo_four_dog_tpex_cpn, self.expo_three_dog_tpex_cpn, self.expo_two_dog_tpex_cpn, self.expo_one_dog_tpex_cpn)) 
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='plot stock chart trend')
    parser.add_argument('--conf_json', type=str, default='config.json', help='Config json')
    parser.add_argument('--gspred_json', type=str, default='xxxx.json', help='Google Sheet Certi json')
    
    args = parser.parse_args()
    
    logger_set(strdirname)
    
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    
    json_file= args.conf_json
    
    json_path_file = pathlib.Path(strdirname)/json_file
    
    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )    
        est_timer(t0)
        sys.exit()

    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f)  
        
    opt_verbose= 'OFF'
    
    path_xlsx_stock_id=  'twse_tpex_ticker.xlsx'
    list_path_pickle_ticker= json_data["twse_otc_id_pickle"]#['twse_ticker.pickle', 'tpex_ticker.pickle', 'twse_tpex_ticker.pickle']
    
    if json_data["lastest_datastr_twse_tpex"][0].lower() == "request":
        store_twse_tpex_ticker(json_data, list_path_pickle_ticker, path_csv_stock_id= '', opt_verbose= 'On')
    
    else:
        start_date = date_changer_twse(json_data["start_end_date"][0])
        end_date = date_changer_twse(json_data["start_end_date"][1])
        logger.info(f'start_date: {start_date}; end_date: {end_date}') 
        local_twse_tpex_ma_status = TWSE_TPEX_MAs_status(json_data, list_path_pickle_ticker, opt_verbose)
        local_twse_tpex_ma_status.calculate_TWSE_MAs_status()
        local_twse_tpex_ma_status.calculate_TPEX_MAs_status()
    
    '''    
    stock_price_graph(tickers=tickers_TW, start_date="2023-10-01", end_date="2024-08-25")
    '''    
    est_timer(t0)    