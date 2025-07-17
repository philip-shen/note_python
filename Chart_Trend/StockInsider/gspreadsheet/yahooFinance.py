from insider.logger_setup import *

import re
import pickle, json
import yfinance as yf
import requests
from requests.exceptions import Timeout
from io import StringIO
import pandas as pd
import pathlib

class Asset:
    """Class to initialize the stock, given a ticker, period and interval"""
    def __init__(self, ticker, start_date, end_date, period='1y', interval='1d'):
        self.ticker = ticker.upper()
        self.period = period
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date    

    def __repr__(self):
        return f"Ticker: {self.ticker}, Period: {self.period}, Interval: {self.interval}"

    def get_info(self):
        """Uses yfinance to get information about the ticker
        returns a dictionary filled with at-point information about the ticker"""
        ticker_info = yf.Ticker(self.ticker).info
        return ticker_info

    def get_data(self):
        '''
        yfinance 0.2.54 ** can not work**
        How to deal with multi-level column names downloaded with yfinance 
        https://stackoverflow.com/questions/63107594/how-to-deal-with-multi-level-column-names-downloaded-with-yfinance/63107801#63107801
        
        Ticker         8081.TW                                                ticker
        Price             Open        High         Low       Close   Volume         
        Date                                                                        
        2024-02-21  249.793682  255.037443  249.316977  252.653915  1025610  8081.TW
        ...                ...         ...         ...         ...      ...      ...
        2025-02-21  246.500000  251.000000  246.000000  246.500000   895100  8081.TW
        '''
        '''
        2024年12月9日 星期一
        [Python] 使用 Yahoo Finance API 的 yfinance 函式庫進行各種金融數據查詢 
        
        https://cheng-min-i-taiwan.blogspot.com/2024/12/python-yahoo-finance-api-yfinance.html
        '''
        '''
        Drop the ticker row of yfinance dataframe Dec 18, 2024 
        https://stackoverflow.com/questions/79291334/drop-the-ticker-row-of-yfinance-dataframe        
        
        '''
        try:
            self.data = yf.download(
                            tickers= self.ticker,
                            #period=self.period,
                            start= self.start_date, 
                            end= self.end_date,
                            interval= self.interval,
                            multi_level_index=False)            
            #self.data = pd.concat([yf.download(self.ticker, 
            #                                period=self.period,
            #                                interval=self.interval).assign(ticker=ticker) for ticker in [self.ticker]], ignore_index=True)
            
            return self.data
        except Exception as e:
            return e

def get_ticker_from_stock_id(options, ticker, opt_verbose='OFF'):    
        
    if opt_verbose.lower() == 'on':
        logger.info(f"options: {options}") 
    
    for option in options:
        if ticker+'.TW' in option["label"]:
            #logger.info(f"option['label']: {option['label']} == ticker: {ticker}") 
            return option["label"]
        elif ticker+'.TWO' in option["label"]:
            #logger.info(f"option['label']: {option['label']} == ticker: {ticker}")     
            return option["label"]

    raise ValueError(
        f"{ticker} cannot map yfinance ticker index ."
    )
    
def gen_ticker_dict(json_data, opt_verbose='off'):
    if opt_verbose.lower() == 'on':
        logger.info(f'json_data["twse_otc_id_pickle"]: {json_data["twse_otc_id_pickle"]}')
    
    with open(json_data["twse_otc_id_pickle"], "rb") as f:
        TICKER_LIST = pickle.load(f)       
    options=[
        {
            "label": str(TICKER_LIST[i]),
            "value": str(TICKER_LIST[i]),
        }
        for i in range(len(TICKER_LIST))
    ]

    return options

class Stock:
    def __init__(self, json_data: dict):        
            
        # Check whether it is a TWSE or TPEX stock
        self.Flag_tpex_stocks = False
        self.Flag_twse_stocks = False
        self.str_datastr_twse_tpex = json_data["start_end_date"][0][-1]
        self.df_twse_website_info = None
        self.df_tpex_website_info = None
        self.requests_twse_tpex_stock_idx()
    
    def check_stocks(self, df, check_name, check_num):
        
        if df[df[check_name]==self.stock_name].empty and df[df[check_num]==self.stock_num].empty:
            return False
        else:
            if self.stock_name != "" and self.stock_num != '':
                # assert df[df[check_name] == self.stock_name][check_num].values[0] == self.stock_num, "股票名稱與股票代號不符!! 請重新輸入!!"
                assert df[df[check_name] == self.stock_name][check_num].values[0] == self.stock_num, "The stock name is inconsistent with the stock number!! Please enter again!!"
                
            if not self.stock_name:
                self.stock_name = df[df[check_num] == self.stock_num][check_name].values[0]
            if not self.stock_num:
                self.stock_num = df[df[check_name] == self.stock_name][check_num].values[0]
            
            logger.info("Pass checking... Starts analyzing stocks..")

            return True
    
    # Change the date
    #############################################
    def date_changer(self, date):

        year = date[:4]
        year = str(int(year)-1911)
        month = date[4:6]
        day = date[6:]
        #logger.info(f'{year}+"/"+{month}+"/"+{day}')
        
        return year+"/"+month+"/"+day
    '''
    https://ithelp.ithome.com.tw/m/articles/10263439
    
    這些資料放在政府的資料開放平台上，不過我們只需要下載位置就可以了。
    上市公司資料
    https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv

    上櫃公司資料
    https://mopsfin.twse.com.tw/opendata/t187ap03_O.csv

    興櫃公司資料
    https://mopsfin.twse.com.tw/opendata/t187ap03_R.csv
    '''    
    '''    
    stockAanlysis/get_securities_lists.py
    https://github.com/JacquesBlazor/stockAanlysis/blob/main/get_securities_lists.py
    
    df = df[['公司代號', '公司名稱', '公司簡稱', '外國企業註冊地國', '營利事業統一編號', '成立日期', '上市日期', '普通股每股面額', '英文簡稱', '網址']]
    '''        
    '''        
    神秘金字塔資料爬取(資料更新至2020522當周)
    [i=s] 本帖最後由 Mark陳 於 2020-5-24 11:30 編輯 [/i]
    http://finlabcourse.imotor.com/archiver/?tid-541.html
    '''
    def twse_stock_list(self):
        res = requests.get('http://mopsfin.twse.com.tw/opendata/t187ap03_L.csv')
        res.encoding='utf-8'
        self.df_twse_website_info = pd.read_csv(StringIO(res.text), header=0, \
                                                dtype={'出表日期':str,'公司代號':str, '產業別':str}).dropna(how='all', axis=1).dropna(how='any')
        
    '''
    self.df_tpex_website_info.dtypes:
    出表日期                  int64
    公司代號                  int64
    公司名稱                 object
    公司簡稱                 object
    外國企業註冊地國             object
    產業別                   int64
    住址                   object
    '''    
    '''
    Changing data type
    https://www.ritchieng.com/pandas-changing-datatype/

    Method 1: Change datatype after reading the csv
    # to change use .astype() 
    drinks['beer_servings'] = drinks.beer_servings.astype(float)
    

    Method 2: Change datatype before reading the csv
    drinks = pd.read_csv(url, dtype={'beer_servings':float})
    '''
    def otc_stock_list(self):
        res = requests.post('http://mopsfin.twse.com.tw/opendata/t187ap03_O.csv')
        res.encoding='utf-8'
        self.df_tpex_website_info =  pd.read_csv(StringIO(res.text), header=0, \
                                                dtype={'出表日期':str,'公司代號':str, '產業別':str}).dropna(how='all', axis=1).dropna(how='any')
        #logger.info(f'self.df_tpex_website_info.dtypes:\n{self.df_tpex_website_info.dtypes}')
    
    def requests_twse_tpex_stock_idx(self):
        ##### 上市公司
        #datestr = self.str_datastr_twse_tpex#'20240801'
        #r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
        
        # 整理資料，變成表格
        #self.df_twse_website_info = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
        #logger.info(f'self.df_twse_website_info:\n{self.df_twse_website_info}')    
        
        # before trade day 14:00 no data to get
        csv_log = 'MI_INDEX_ALL_202501.csv'
        usecols = ["證券代號", "證券名稱"]
        self.df_twse_website_info = pd.read_csv(csv_log,usecols=usecols).dropna(how='all', axis=1).dropna(how='any')
        logger.info(f'**** TWSE Server before trade day 14:00 no data to get from 202501 ****')    
        #logger.info(f'self.df_twse_website_info:\n{self.df_twse_website_info}')    
            
        ##### 上櫃公司
        #datestr = self.date_changer(self.str_datastr_twse_tpex)#'113/08/01'
        #本中心官網自本(113)年10月27日(星期日)全新改版
        #舊版官網可透過網址https://wwwov.tpex.org.tw 繼續使用並將於114年05月31日停用。
        #r = requests.post('http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=' + datestr + '&s=0,asc,0')
        
        #r = requests.post('http://wwwov.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=' + datestr + '&s=0,asc,0')        
        # 整理資料，變成表格
        #self.df_tpex_website_info = pd.read_csv(StringIO(r.text), header=2).dropna(how='all', axis=1).dropna(how='any')
        
        self.otc_stock_list()
        
        logger.info("Request TWSE and TPEX Stock index..")
                
    def check_twse_tpex_us_stocks(self, stock_idx: str):        
        self.stock_idx = stock_idx        
        self.stock_name = ""
        self.stock_num = stock_idx
        
        ##### 上市公司
        self.Flag_twse_stocks = self.check_stocks(self.df_twse_website_info, check_name="證券名稱", check_num="證券代號")
        
        if self.Flag_twse_stocks:
            self.ticker = self.stock_idx+'.TW' 
            #logger.info(f"ticker: {self.ticker}")
            return
        
        ##### 上櫃公司
        if not self.Flag_twse_stocks:            
            #self.Flag_tpex_stocks = self.check_stocks(self.df_tpex_website_info, check_name="名稱", check_num="代號")
            self.Flag_tpex_stocks = self.check_stocks(self.df_tpex_website_info, check_name="公司簡稱", check_num="公司代號")
            
            if self.Flag_tpex_stocks:
                self.ticker = self.stock_idx+'.TWO' 
                #logger.info(f"ticker: {self.ticker}")
                return
            
        # assert Flag_tpex_stocks or Flag_tsw_stocks, "非上市上櫃公司!"
        #assert self.Flag_tpex_stocks or self.Flag_twse_stocks, "Not Listed company!"
        if "^" in self.stock_idx.lower():
                self.ticker=  self.stock_idx
                #logger.info(f"ticker: {self.ticker}")
                return
            
        if bool(re.match('^[a-zA-Z]+$', self.stock_idx)):
                self.ticker=  self.stock_idx
                #logger.info(f"ticker: {self.ticker}")
                return
            
        raise ValueError(
            f"{self.stock_idx} cannot map yfinance ticker index ."
        )
        
def get_asset_from_yfinance_ticker(stock_ticker, opt_verbose='off', period='1y', interval='1d'):    
        
    ''' fase out
    options = gen_ticker_dict(json_data, opt_verbose)    
    ticker= get_ticker_from_stock_id(options, tw_tse_otc_stk_idx)
    '''
    ''' remark for accelerate get twse tpex idx purpose   
    local_stock=Stock(tw_tse_otc_stk_idx)
    ticker = local_stock.ticker
    '''
            
    # initialize Asset object 
    asset = Asset( stock_ticker, period=period, interval=interval)
    asset_info = asset.get_info()  # Information about the Company
    asset_df = asset.get_data()    # Historical price data    
    
    asset_df.reset_index(inplace=True)
    '''
    # Renaming columns using a dictionary
    df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)
    '''
    asset_df.rename(columns={"Date": "day", "Open": "open", "High": "high", 
                                  "Low": "low", "Close": "close", "Adj Close": "adj close", 
                                  "Volume":"volume"}, inplace=True)
    
    if opt_verbose.lower() == 'on':
        logger.info(f"\nasset_df.keys(): {asset_df.keys()}")
            
    asset_df["day"]= asset_df["day"].apply(lambda x: x.strftime('%Y-%m-%d'))
            
    #logger.info(f"asset_df['close']:\n {asset_df['close']}")
    
    ## Check 4 stock prices: 1.final, 2.open, 3.high, 4.low
    stock_price_final = asset_df['close'].iloc[-1]
    stock_price_open = asset_df['open'].iloc[-1]
    stock_price_high = asset_df['high'].iloc[-1]
    stock_price_low = asset_df['low'].iloc[-1]
    
    if opt_verbose.lower() == 'on':
        logger.info("lastest value of close: {:.2f}, open: {:.2f}, high: {:.2f}, low: {:.2f}".\
                    format(stock_price_final, stock_price_open, stock_price_high, stock_price_low))        
    
    dict_stock_price_OHLC ={
        "close": stock_price_final,
        "open": stock_price_open,
        "high": stock_price_high,
        "low": stock_price_low 
    }
    
    return dict_stock_price_OHLC

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
class stock_indicator:
    def __init__(self, ticker, startdate, enddate, period='1y', interval='1d', opt_verbose='OFF'):
        self.stock_ticker = ticker.upper()
        self.opt_verbose = opt_verbose
        self.startdate = startdate
        self.enddate = enddate    
        
        # initialize Asset object 
        asset = Asset( self.stock_ticker, start_date= self.startdate, end_date= self.enddate, \
                        period=period, interval=interval)
        asset_info = asset.get_info()  # Information about the Company
        asset_df = asset.get_data()    # Historical price data    

        asset_df.reset_index(inplace=True)
        '''
        # Renaming columns using a dictionary
        df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)
        '''
        #asset_df.rename(columns={"Date": "day", "Open": "open", "High": "high", 
        #                          "Low": "low", "Close": "close", "Adj Close": "adj close", 
        #                          "Volume":"volume"}, inplace=True)

        self.stock_data = asset_df
        #logger.info(f'self.stock_data:\n{self.stock_data}')
        
    # RSIを計算する関数
    def calculate_RSI(self, window=14):
        delta = self.stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)

        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()

        rs = avg_gain / avg_loss
        self.rsi = 100 - (100 / (1 + rs))
        #return rsi

    # MFIを計算する関数
    def calculate_MFI(self, window=14):
        typical_price = (self.stock_data['High'] + self.stock_data['Low'] + self.stock_data['Close']) / 3
        money_flow = typical_price * self.stock_data['Volume']

        positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
        negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)

        positive_mf = positive_flow.rolling(window=window, min_periods=1).sum()
        negative_mf = negative_flow.rolling(window=window, min_periods=1).sum()

        self.mfi = 100 - (100 / (1 + (positive_mf / negative_mf)))
        #return mfi

    # ボリンジャーバンドを計算する関数
    def calculate_bollinger_bands(self, window=20):
        sma = self.stock_data['Close'].rolling(window=window).mean()
        std = self.stock_data['Close'].rolling(window=window).std()
        self.stock_data['Bollinger Middle'] = sma
        self.stock_data['Bollinger Upper'] = sma + (std * 2)
        self.stock_data['Bollinger Lower'] = sma - (std * 2)
        #return data

    # 移動平均線を計算する関数
    def calculate_moving_averages(self, weekly_window=5, Dweekly_window=10, \
                                    monthly_window=20, quarterly_window=60, yearly_window=200):
        self.stock_data['MA_5'] = self.stock_data['Close'].rolling(window=weekly_window).mean()
        self.stock_data['MA_10'] = self.stock_data['Close'].rolling(window=Dweekly_window).mean()
        self.stock_data['MA_20'] = self.stock_data['Close'].rolling(window=monthly_window).mean()
        self.stock_data['MA_60'] = self.stock_data['Close'].rolling(window=quarterly_window).mean()
        self.stock_data['MA_200'] = self.stock_data['Close'].rolling(window=yearly_window).mean()

    def calculate_exponential_moving_averages(self, weekly_window=5, Dweekly_window=10, \
                                    monthly_window=20, quarterly_window=60, yearly_window=200):
        self.stock_data['EMA_5'] = self.stock_data['Close'].ewm(ignore_na=False, span=weekly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_10'] = self.stock_data['Close'].ewm(ignore_na=False, span=Dweekly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_20'] = self.stock_data['Close'].ewm(ignore_na=False, span=monthly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_60'] = self.stock_data['Close'].ewm(ignore_na=False, span=quarterly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_200'] = self.stock_data['Close'].ewm(ignore_na=False, span=yearly_window, min_periods=0, adjust=False).mean()    
        
    def calculate_volume_weighted_average_price(self):
        self.stock_data['cum_volume'] = self.stock_data['Volume'].cumsum()
        self.stock_data['cum_volume_price'] = (self.stock_data['Close'] * self.stock_data['Volume']).cumsum()
        data = self.stock_data['cum_volume_price'] / self.stock_data['cum_volume']
        return data
    
    def stand_Up_On_fall_Down_MAs(self):
        #logger.info("{}".format("Stand_Up_On_MAs (針對你Fetch data區間的最後一天做分析):"))

        # 抓出所需data
        stock_price = self.stock_data['Close'].astype(float).iloc[-1]
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
        '''        
        
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
    
        self.close = self.stock_data['Close'].astype(float).iloc[-1]
        self.open = self.stock_data['Open'].astype(float).iloc[-1]
        self.high = self.stock_data['High'].astype(float).iloc[-1]
        self.low = self.stock_data['Low'].astype(float).iloc[-1]
        self.MA_5 = self.stock_data['MA_5'].astype(float).iloc[-1]
        self.MA_10 = self.stock_data['MA_10'].astype(float).iloc[-1]
        self.MA_20 = self.stock_data['MA_20'].astype(float).iloc[-1]
        self.MA_60 = self.stock_data['MA_60'].astype(float).iloc[-1]
        self.MA_200 = self.stock_data['MA_200'].astype(float).iloc[-1]
        
    def filter_MAs_status(self):
        '''
        if self.four_flag:
            self.stock_MA_status = 'four_star'
            return
        elif not self.four_flag and self.three_flag:
            self.stock_MA_status = 'three_star'
            return
        elif not (self.four_flag and self.three_flag) and self.two_flag:
            self.stock_MA_status = 'two_star'    
            return
        elif not (self.four_flag and self.three_flag and self.two_flag)  and self.one_flag:
            self.stock_MA_status = 'one_star'    
            return
                    
        elif self.four_dog and self.three_dog:
            self.stock_MA_status = 'four_dog'
            return
        elif not self.four_dog and self.three_dog:
            self.stock_MA_status = 'three_dog'
            return
        
        elif self.four_E_flag:
            self.stock_MA_status = 'Expo_four_star'
            return
        elif not self.four_E_flag and self.three_E_flag:
            self.stock_MA_status = 'Expo_three_star'
            return    
        elif not (self.four_E_flag and self.three_E_flag) and self.two_E_flag:
            self.stock_MA_status = 'Expo_two_star'    
            return
        elif not (self.four_E_flag and self.three_E_flag and self.two_E_flag)  and self.one_E_flag:
            self.stock_MA_status = 'Expo_one_star'    
            return
        else:
            self.stock_MA_status = 'NA'    
        '''    
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