from typing import Optional
import re
import pickle
from datetime import datetime, date, timedelta

import requests
from requests.exceptions import Timeout
import pandas as pd

from insider.logger_setup import *

import asyncio
from pstock import Bars, BarsMulti

from gspreadsheet.constants import (
    STOCK_URL,
    KTYPE_CONVERSION,
    KTYPES,
    DAY_COL,
    NUMERIC_COLUMNS,
    MA_COLORS,
    MA_COLS,
)


def date_changer_twse( date):
    
    year = date[:4]
    year = str(int(year))
    month = date[4:6]
    day = date[6:]
        
    return year+"-"+month+"-"+day
'''
http://yhhuang1966.blogspot.com/2022/09/python-yfinance.html

download() 參數	 說明
 symbol	 股票代號 (字串), 美股例如  'AMD' (超微), 台股後面要加 '.tw', 例如 '0050.tw'
 start	 起始日期 YYYY-MM-DD (字串), 例如 '2022-08-22'
 end	 結束日期 YYYY-MM-DD (字串), 例如 '2022-09-06', 注意, 不包含此日資料
 period	 期間, 可用 d (日), mo(月), y(年), ytd, max(全部), 例如 5d (5 天), 3mo(三個月) 
 interval	 頻率, 可用 m(分), h(小時), d(日), wk(周), mo(月), 例如 1m(一分線)
'''
def date_changer_twse_yfinance_end_date( date):
    
    curr_date_temp = datetime.strptime(date, '%Y%m%d')
    next_date = curr_date_temp + timedelta(days=1)
    next_date = str(next_date)
    '''
    20240909, 
    2024-09-10 00:00:00
    '''    
    #logger.info(f'{date}, {next_date}')
    
    year = next_date[:4]
    #year = str(int(year))
    month = next_date[5:7]
    next_day = next_date[8:10]
    '''
    2024-09-10 00:00:00, 2024, 09, 10
    '''
    #logger.info(f'{next_date}, {year}, {month}, {next_day}')
    
    return year+"-"+month+"-"+next_day

'''
To get Bars there are a couple of arguments that can be specified:

    interval: one of 1m, 2m, 5m, 15m, 30m, 1h, 1d, 5d, 1mo, 3mo, defaults to None
    period: one of 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max, defaults to None
    start: Any date/datetime supported by pydnatic, defaults to None
    end: Any date/datetime supported by pydnatic, defaults to None
    events: one of div, split, div,splits, defaults to div,splits
    include_prepost: Bool, include Pre and Post market bars, default to False

'''
'''
INFO: HTTP Request: GET https://query2.finance.yahoo.com/v8/finance/chart/2330.TW?interval=1h&events=div%2Csplits&includePrePost=false&period1=1717372800&period2=1726790400 "HTTP/1.1 200 OK"
INFO: ticker: 2330.TW; stock name: 台積電
INFO: bars.df:
                         date   open   high    low  close  adj_close     volume        interval
0   2024-06-03 01:00:00+00:00  839.0  847.0  837.0  847.0      847.0        0.0 0 days 01:00:00
1   2024-06-03 02:00:00+00:00  847.0  853.0  846.0  852.0      852.0  5924046.0 0 days 01:00:00
2   2024-06-03 03:00:00+00:00  853.0  853.0  850.0  851.0      851.0  2344066.0 0 days 01:00:00
3   2024-06-03 04:00:00+00:00  851.0  851.0  848.0  849.0      849.0  3034463.0 0 days 01:00:00
4   2024-06-03 05:00:00+00:00  849.0  852.0  849.0  850.0      850.0  2087760.0 0 days 01:00:00
..                        ...    ...    ...    ...    ...        ...        ...             ...
371 2024-09-19 02:00:00+00:00  938.0  950.0  938.0  949.0      949.0  7523344.0 0 days 01:00:00
372 2024-09-19 03:00:00+00:00  950.0  952.0  947.0  952.0      952.0  6381810.0 0 days 01:00:00
373 2024-09-19 04:00:00+00:00  952.0  952.0  949.0  952.0      952.0  4122869.0 0 days 01:00:00
374 2024-09-19 05:00:00+00:00  951.0  955.0  951.0  955.0      955.0  4916511.0 0 days 01:00:00
375 2024-09-19 05:30:00+00:00  960.0  960.0  960.0  960.0      960.0        0.0 0 days 01:00:00
'''

class stock_indicator_pstock:
    def __init__(self, ticker, startdate, enddate, period='1y', interval='1d', opt_verbose='OFF'):
        self.stock_ticker = ticker.upper()
        self.opt_verbose = opt_verbose
        self.interval = interval
        self.period = period
        self.startdate = startdate
        self.enddate = enddate
            
    def pstock_interval_period(self):
        # initialize Asset object 
        try:
            bars = asyncio.run(Bars.get(self.stock_ticker, period=self.period, interval=self.interval))
            self.stock_data = bars.df.copy()
            self.stock_data.reset_index(inplace=True)
        except Exception as e:
            logger.info(f'Error: {e}')
            exit(0)
    
    def pstock_interval_startdate_enddate(self):
        # initialize Asset object 
        try:
            bars = asyncio.run(Bars.get(self.stock_ticker, start=self.startdate, end=self.enddate, interval=self.interval))
            self.stock_data = bars.df.copy()
            self.stock_data.reset_index(inplace=True)
        except Exception as e:
            logger.info(f'Error: {e}')
            exit(0)
                    
    # 移動平均線を計算する関数
    def calculate_moving_averages(self, weekly_window=5, Dweekly_window=10, \
                                    monthly_window=20, quarterly_window=60, yearly_window=200):
        self.stock_data['MA_5'] = self.stock_data['close'].rolling(window=weekly_window).mean()
        self.stock_data['MA_10'] = self.stock_data['close'].rolling(window=Dweekly_window).mean()
        self.stock_data['MA_20'] = self.stock_data['close'].rolling(window=monthly_window).mean()
        self.stock_data['MA_60'] = self.stock_data['close'].rolling(window=quarterly_window).mean()
        self.stock_data['MA_200'] = self.stock_data['close'].rolling(window=yearly_window).mean()

    def calculate_exponential_moving_averages(self, weekly_window=5, Dweekly_window=10, \
                                    monthly_window=20, quarterly_window=60, yearly_window=200):
        self.stock_data['EMA_5'] = self.stock_data['close'].ewm(ignore_na=False, span=weekly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_10'] = self.stock_data['close'].ewm(ignore_na=False, span=Dweekly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_20'] = self.stock_data['close'].ewm(ignore_na=False, span=monthly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_60'] = self.stock_data['close'].ewm(ignore_na=False, span=quarterly_window, min_periods=0, adjust=False).mean()    
        self.stock_data['EMA_200'] = self.stock_data['close'].ewm(ignore_na=False, span=yearly_window, min_periods=0, adjust=False).mean()    
    
    def stand_Up_On_fall_Down_MAs(self):
        #logger.info("{}".format("Stand_Up_On_MAs (針對你Fetch data區間的最後一天做分析):"))

        # 抓出所需data
        stock_price = self.stock_data['close'].astype(float).iloc[-1]
        MA5 = self.stock_data['MA_5'].iloc[-1] if not self.stock_data['MA_5'].isnull().values.all() else 0
        MA10 = self.stock_data['MA_10'].iloc[-1] if not self.stock_data['MA_10'].isnull().values.all() else 0
        MA20 = self.stock_data['MA_20'].iloc[-1] if not self.stock_data['MA_20'].isnull().values.all() else 0
        MA60 = self.stock_data['MA_60'].iloc[-1] if not self.stock_data['MA_60'].isnull().values.all() else 0

        four_MAs = MA5 and MA10 and MA20 and MA60
        three_MAs = MA5 and MA10 and MA20
        two_MAs = MA5 and MA10
        one_MAs = MA5
        
        self.four_flag = True if four_MAs and max(stock_price, MA5, MA10, MA20, MA60) == stock_price else False
        self.three_flag = True if three_MAs and max(stock_price, MA5, MA10, MA20) == stock_price else False
        self.two_flag = True if two_MAs and max(stock_price, MA5, MA10) == stock_price else False
        self.one_flag = True if one_MAs and max(stock_price, MA5) == stock_price else False
        
        self.four_dog = True if four_MAs and min(stock_price, MA5, MA10, MA20, MA60) == stock_price else False
        self.three_dog = True if three_MAs and min(stock_price, MA5, MA10, MA20) == stock_price else False 
        self.two_dog = True if two_MAs and min(stock_price, MA5, MA10) == stock_price else False 
        self.one_dog = True if one_MAs and min(stock_price, MA5, MA10) == stock_price else False 
        
        # Exponential_moving_averages
        EMA5 = self.stock_data['EMA_5'].iloc[-1] if not self.stock_data['EMA_5'].isnull().values.all() else 0
        EMA10 = self.stock_data['EMA_10'].iloc[-1] if not self.stock_data['EMA_10'].isnull().values.all() else 0
        EMA20 = self.stock_data['EMA_20'].iloc[-1] if not self.stock_data['EMA_20'].isnull().values.all() else 0
        EMA60 = self.stock_data['EMA_60'].iloc[-1] if not self.stock_data['EMA_60'].isnull().values.all() else 0
        
        four_Expon_MAs = EMA5 and EMA10 and EMA20 and EMA60
        three_Expon_MAs = EMA5 and EMA10 and EMA20
        two_Expon_MAs = EMA5 and EMA10
        one_Expon_MAs = EMA5
        '''
        self.four_E_flag = True if four_Expon_MAs and max(stock_price, EMA5, EMA10, EMA20, EMA60) == stock_price else False
        self.three_E_flag = True if three_Expon_MAs and max(stock_price, EMA5, EMA10, EMA20) == stock_price else False
        self.two_E_flag = True if two_Expon_MAs and max(stock_price, EMA5, EMA10) == stock_price else False
        self.one_E_flag = True if one_Expon_MAs and max(stock_price, EMA5) == stock_price else False
        '''
        self.four_E_flag = True if not self.four_flag and \
                            (four_Expon_MAs and max(stock_price, EMA5, EMA10, EMA20, EMA60) == stock_price) else False
        self.three_E_flag = True if not self.three_flag and \
                            (three_Expon_MAs and max(stock_price, EMA5, EMA10, EMA20) == stock_price) else False
        self.two_E_flag = True if not self.two_flag and \
                            (two_Expon_MAs and max(stock_price, EMA5, EMA10) == stock_price) else False
        self.one_E_flag = True if not self.one_flag and \
                            (one_Expon_MAs and max(stock_price, EMA5) == stock_price) else False
        
        
        self.four_E_dog = True if not self.four_dog and \
                            (four_Expon_MAs and min(stock_price, EMA5, EMA10, EMA20, EMA60) == stock_price) else False
        self.three_E_dog = True if not self.three_dog and \
                            (three_Expon_MAs and min(stock_price, EMA5, EMA10, EMA20) == stock_price) else False
        self.two_E_dog = True if not self.two_dog and \
                            (two_Expon_MAs and min(stock_price, EMA5, EMA10) == stock_price) else False
        self.one_E_dog = True if not self.one_dog and \
                            (one_Expon_MAs and min(stock_price, EMA5) == stock_price) else False
                                
    def check_MAs_status(self):
        # 必要な列を抽出
        #data = self.stock_data[['Close', 'Volume', 'High', 'Low']].copy()
        
        # 移動平均線を計算
        self.calculate_moving_averages()
        self.calculate_exponential_moving_averages()
        
        self.stand_Up_On_fall_Down_MAs() 
        #logger.info(f'self.stock_data:\n {self.stock_data}' )    
        
        if self.opt_verbose.lower() == 'on':
            # 判斷data值
            if self.four_flag:
                logger.info("股價已站上5日、10日、20日、60日均線均線，為四海遊龍型股票!!")
            elif self.three_flag:
                logger.info("股價已站上5日、10日、20日均線，為三陽開泰型股票!!")
            #elif not self.four_MAs:
            #   logger.info("目前的data數量不足以畫出四條均線，請補足後再用此演算法!!")
            #elif not self.three_MAs:
            #    logger.info("目前的data數量不足以畫出三條均線，請補足後再用此演算法!!")
            else:
                logger.info("目前股價尚未成三陽開泰型、四海遊龍型股票!!")
    
        self.close = self.stock_data['close'].astype(float).iloc[-1]
        self.open = self.stock_data['open'].astype(float).iloc[-1]
        self.high = self.stock_data['high'].astype(float).iloc[-1]
        self.low = self.stock_data['low'].astype(float).iloc[-1]
        self.MA_5 = self.stock_data['MA_5'].astype(float).iloc[-1]
        self.MA_10 = self.stock_data['MA_10'].astype(float).iloc[-1]
        self.MA_20 = self.stock_data['MA_20'].astype(float).iloc[-1]
        self.MA_60 = self.stock_data['MA_60'].astype(float).iloc[-1]
        self.MA_200 = self.stock_data['MA_200'].astype(float).iloc[-1]
        
    def filter_MAs_status(self):
        if self.four_flag:
            self.stock_MA_status = 'four_star'
            return
        elif self.three_flag:
            self.stock_MA_status = 'three_star'
            return
        elif self.two_flag:
            self.stock_MA_status = 'two_star'    
            return
        elif self.one_flag:
            self.stock_MA_status = 'one_star'    
            return
        
        elif self.four_dog:
            self.stock_MA_status = 'four_dog'
            return
        elif self.three_dog:
            self.stock_MA_status = 'three_dog'
            return
        
        elif self.four_E_flag:
            self.stock_MA_status = 'Expo_four_star'
            return
        elif self.three_E_flag:
            self.stock_MA_status = 'Expo_three_star'
            return  
        elif self.two_E_flag:
            self.stock_MA_status = 'Expo_two_star'    
            return  
        elif self.one_E_flag:
            self.stock_MA_status = 'Expo_one_star'    
            return
        elif self.four_E_dog:
            self.stock_MA_status = 'Expo_four_dog'
            return
        elif self.three_E_dog:
            self.stock_MA_status = 'Expo_three_dog'
            return
        elif self.two_E_dog:
            self.stock_MA_status = 'Expo_two_dog'
            return
        elif self.one_E_dog:
            self.stock_MA_status = 'Expo_one_dog'
            return
        else:
            self.stock_MA_status = 'NA'    