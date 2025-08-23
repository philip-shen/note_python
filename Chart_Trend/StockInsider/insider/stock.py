from typing import Optional
import re
import pickle
from datetime import datetime, date, timedelta

import requests
from requests.exceptions import Timeout
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

from insider.logger_setup import *

import asyncio
from pstock import Bars, BarsMulti

from insider.constants import (
    STOCK_URL,
    KTYPE_CONVERSION,
    KTYPES,
    DAY_COL,
    NUMERIC_COLUMNS,
    MA_COLORS,
    MA_COLS,
)
from insider.utils import set_layout


class Stock:
    """
    Stock Class which collects historical stock trading data and plots the basic
    stock price and k-lines
    """

    def __init__(self, code: str, stock_idx: str, list_df_twse_tpex_stock_info: list, json_data: dict, \
                    ktype: str = "D", period='1y', interval='1d'):
        """
        code: Full stock code，(e.g. 'sz002156')，股票完整代码
        ktype: freq, valid values are `D`, `W`, and `M`，股票趋势频率
        """
        if code != None:
            self.code = self._check_code(code)
            self.stock_code = re.findall(r"\d+", self.code)[0]
            self.ktype, self.converted_ktype = self._check_ktype(ktype)
            self.url = STOCK_URL.format(ktype=self.converted_ktype, code=self.code)
            self._df = self._get_stock_data()
        
        if code == None:
            self.code = None
            self.stock_idx = stock_idx
            self.json_data = json_data
            self.period = period
            self.interval = interval
            self.fname_twse_otc_id_pickle= self.json_data["twse_otc_id_pickle"]
            #self.gen_ticker_dict() #fase out
            #self.get_ticker_from_stock_idx() #fase out
            
            self.stock_name = ""
            self.stock_num = stock_idx
            
            # Check whether it is a TWSE or TPEX stock
            self.Flag_tpex_stocks = False
            self.Flag_twse_stocks = False
            self.df_twse_website_info = list_df_twse_tpex_stock_info[0]
            self.df_tpex_website_info = list_df_twse_tpex_stock_info[1]            
            self.check_twse_tpex_us_stocks() 
                       
            self.ticker_info= self.get_yfinance_stock_info()        
            self._df = self.get_yfinance_stock_data()
            self._df.reset_index(inplace=True)
            '''
            # Renaming columns using a dictionary
            df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)
            '''
            self._df.rename(columns={"Date": "day", "Open": "open", "High": "high", 
                                  "Low": "low", "Close": "close", "Adj Close": "adj close", 
                                  "Volume":"volume"}, inplace=True)
            logger.info(f"self._df.keys(): \n{self._df.keys()}")
            
            self._df["day"]= self._df["day"].apply(lambda x: x.strftime('%Y-%m-%d'))
            
    def gen_ticker_dict(self):
        with open(self.fname_twse_otc_id_pickle, "rb") as f:
            TICKER_LIST = pickle.load(f)       
        options=[
            {
                "label": str(TICKER_LIST[i]),
                "value": str(TICKER_LIST[i]),
            }
            for i in range(len(TICKER_LIST))
        ]

        self.options= options
        
    def get_ticker_from_stock_idx( self, stock_idx: str, opt_verbose='OFF'):    
        
        if opt_verbose.lower() == 'on':
            logger.info(f"options: {self.options}") 
    
        for option in self.options:
            if stock_idx+'.TW' in option["label"]:
                #logger.info(f"option['label']: {option['label']} == ticker: {ticker}") 
                self.ticker= option["label"]
                return
            elif stock_idx+'.TWO' in option["label"]:
                #logger.info(f"option['label']: {option['label']} == ticker: {ticker}")     
                self.ticker=  option["label"]
                return
            elif "^" in stock_idx.lower():
                self.ticker=  stock_idx
                return
            elif bool(re.match('^[a-zA-Z]+$', stock_idx)):
                self.ticker=  stock_idx
                return
            
        raise ValueError(
            f"{stock_idx} cannot map yfinance ticker index ."
        )
    
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
    ''' waste 3~4 sec to request so move main routine
    def requests_twse_tpex_stock_idx(self):
        ##### 上市公司
        datestr = self.json_data["lastest_datastr_twse_tpex"][0]#'20240801'
        r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
        # 整理資料，變成表格
        self.df_twse_website_info = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
        
        ##### 上櫃公司
        datestr = self.json_data["lastest_datastr_twse_tpex"][1]#'113/08/01'
        r = requests.post('http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=' + datestr + '&s=0,asc,0')
        # 整理資料，變成表格
        self.df_tpex_website_info = pd.read_csv(StringIO(r.text), header=2).dropna(how='all', axis=1).dropna(how='any')
        
        logger.info("Request TWSE and TPEX Stock index..")
    '''                
    def check_twse_tpex_us_stocks(self):
        
        ##### 上市公司
        self.Flag_twse_stocks = self.check_stocks(self.df_twse_website_info, check_name="證券名稱", check_num="證券代號")
        
        if self.Flag_twse_stocks:
            self.ticker = self.stock_idx+'.TW' 
            logger.info(f"ticker: {self.ticker}")
            return
        
        ##### 上櫃公司
        if not self.Flag_twse_stocks:
            self.Flag_tpex_stocks = self.check_stocks(self.df_tpex_website_info, check_name="名稱", check_num="代號")
            
            if self.Flag_tpex_stocks:
                self.ticker = self.stock_idx+'.TWO' 
                logger.info(f"ticker: {self.ticker}")
                return
            
        # assert Flag_tpex_stocks or Flag_tsw_stocks, "非上市上櫃公司!"
        #assert self.Flag_tpex_stocks or self.Flag_twse_stocks, "Not Listed company!"
        if "^" in self.stock_idx.lower():
                self.ticker=  self.stock_idx
                logger.info(f"ticker: {self.ticker}")
                return
            
        if bool(re.match('^[a-zA-Z]+$', self.stock_idx)):
                self.ticker=  self.stock_idx
                logger.info(f"ticker: {self.ticker}")
                return
        #DE000SL0EC48.SG
        if bool(re.match('^[a-zA-Z]+(\d{1,3}.)?.+', self.stock_idx)):
                self.ticker=  self.stock_idx
                logger.info(f"ticker: {self.ticker}")
                return
                
        raise ValueError(
            f"{self.stock_idx} cannot map yfinance ticker index ."
        )
        
    def get_yfinance_stock_data(self):
        """Uses yfinance to get data, returns a Pandas DataFrame object
        Index: Date
        Columns: Open, High, Low, Close, Adj Close, Volume
        """
        try:
            self.data = yf.download(
                tickers=self.ticker,
                period=self.period,
                interval=self.interval)            
            return self.data
        except Exception as e:
             raise ValueError(
                e
             )
    
    def get_yfinance_stock_info(self):
        """Uses yfinance to get information about the ticker
        returns a dictionary filled with at-point information about the ticker"""
        try:
            
            ticker_info = yf.Ticker(self.ticker).info
            return ticker_info
        except Exception as e:
             raise ValueError(
                e
             )
             
    def _check_code(self, code: str) -> str:
        if not code.startswith("sz") and not code.startswith("sh"):
            raise ValueError("Stock code needs to be either sz or sh.")
        elif len(code) != 8:
            raise ValueError(f"Invalid code length: requires 8, but get {len(code)}")
        elif not code[2:].isdigit():
            raise ValueError("Code must be all digits after sh or sz.")
        return code

    def _check_ktype(self, ktype: str) -> (str, str):
        upper_ktype = ktype.upper()
        if upper_ktype not in KTYPES:
            raise ValueError(f"Invalid ktype is given, valid inputs are {KTYPES}")
        converted_ktype = KTYPE_CONVERSION[upper_ktype]
        return upper_ktype, converted_ktype

    @property
    def full_data(self):
        df = self._df.copy()
        return df

    def _get_stock_data(self):
        try:
            r = requests.get(self.url, timeout=10)
        except Timeout:
            raise ValueError("The request timed out. Please try again.")
        else:
            logger.info(f"url: {self.url}")
            logger.info(f"request: {r}")
            
            data = r.json()["record"]
            if data:
                df = pd.DataFrame(data, columns=DAY_COL + NUMERIC_COLUMNS)
                df[NUMERIC_COLUMNS] = (
                    df[NUMERIC_COLUMNS]
                    .applymap(lambda x: x.replace(",", ""))
                    .astype("float64")
                )
                self._df = df
                return df
            else:
                raise ValueError(
                    "No data about the stock is found. Please check if the stock code is correct."
                )

    @staticmethod
    def _choose_date(self, df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        if start_date:
            if self.code != None:
                df = df[df["day"] >= start_date]
            elif self.code == None:
                df = df[df["Date"] >= start_date]
        if end_date:
            if self.code != None:
                df = df[df["day"] <= end_date]
            elif self.code == None:
                df = df[df["Date"] <= end_date]
                
        return df

    def show_data(
        self, start_date:Optional[str] = None, 
            end_date: Optional[str] = None
    ):
        """Return the data in Pandas DataFrame，以DataFrame的形式显示历史数据。

        Parameters:
            start_date: start date of data to show, e.g. '2019-01-01'，起始时间
            end_date: end date of data to show, e.g. '2020-01-01'，终止时间

        Returns:
            Truncated DataFrame based on the dates, default is to show
            the full data.
            根据定义的起止时间而截取的历史数据，默认将会返回所有下载的数据。
        """
        df = self._df.copy()
        return self._choose_date(self, df, start_date, end_date)
    
    """
             Open   High    Low  Close   Adj Close    Volume
    Date                                                        
    2023-03-27  533.0  536.0  531.0  531.0  520.431213  16111177
    2023-03-28  525.0  530.0  524.0  525.0  514.550781  17234120
    2023-03-29  533.0  533.0  525.0  530.0  519.451233  17280749
    """
    """
    DF not recognizing Date as a column
    https://github.com/ranaroussi/yfinance/issues/530
    
    Accessing a Pandas index like a regular column
    https://stackoverflow.com/questions/52139506/accessing-a-pandas-index-like-a-regular-column
    
    [Day09]Pandas索引的運用！ 
    https://ithelp.ithome.com.tw/articles/10194006?sc=hot
    
    bond.reset_index(inplace=True)
    """
    """
    INFO:  Index(['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], dtype='object')
    
    INFO:  DatetimeIndex(['2024-03-27','2024-03-28','2024-03-29'], dtype='datetime64[ns]', name='Date', freq=None)
    """
    '''
    Comparison between datetime and datetime64[ns] in pandas – Datetime
    https://deycode.com/posts/comparison-between-datetime-and-datetime64ns-in-pandas/
    
    Solution 1: Using pd.to_datetime()
    Solution 2: Using pd.Timestamp()
    Solution 3: Using Comparison Methods
    '''
    @staticmethod
    def _plot_stock_data(self, df: pd.DataFrame, head: int):
        if head:
            df = df.tail(head)
            logger.info(f" {df.index}" )
            
        if self.code != None:            
            stock_data = go.Candlestick(
                x=df["day"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                increasing_line_color="red",
                decreasing_line_color="green",
                name="stock price",
            )
            
        elif self.code == None:
            #df.reset_index(inplace=True)
            logger.info(f" {df.keys()}" )
            
            stock_data = go.Candlestick(
                x=df["day"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                increasing_line_color="red",
                decreasing_line_color="green",
                name=self.ticker,
            )
            logger.info(f" {df['close'].iloc[-1]},{df['open'].iloc[-1]},{df['high'].iloc[-1]},{df['low'].iloc[-1]}" )
            
        return stock_data

    @staticmethod
    def _plot_ma_data(self, df: pd.DataFrame, head: int):
        if head:
            df = df.tail(head)

        ma_data = []
        for col, color in zip(MA_COLS, MA_COLORS):
            data = go.Scatter(x=df["day"], y=df[col], name=col, marker_color=color)
                    
            ma_data.append(data)

        return ma_data

    def plot(
        self,
        head: int = 90,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        verbose: bool = True,
    ):
        """Plot the stock price over time. 绘出股票走势图。

        Parameters:
            head: The recent number of trading days to plot, default is 90, 最近交易日的天数，
            默认90，将会绘出最近90个交易日的曲线。
            start_date: start date, default is None, 起始时间
            end_date: end date, default is None, 终止时间
            verbose: If to plot K-line or not, default is True, 是否同时绘出k线，默认是会绘出。
        """
        df = self._df.copy()
        df = self._choose_date(self, df, start_date, end_date)

        stock_data = self._plot_stock_data(self, df, head)
        data = [stock_data]
        if verbose:
            ma_data = self._plot_ma_data(self, df, head)
            data.extend(ma_data)

        fig = go.Figure(data=data, layout=set_layout())
        
        if self.code != None:
            str_title_text=f"Stock Price Chart ({self.stock_code})"
        elif self.code == None:
            str_title_text=f"Stock Price Chart ({self.ticker})"
                
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            title_text=str_title_text,
        )
        fig.show()

class Asset:
    """Class to initialize the stock, given a ticker, period and interval"""
    def __init__(self, ticker, start, end, period='1y', interval='1d'):
        self.ticker = ticker.upper()
        self.period = period
        self.interval = interval
        self.start_date = start
        self.end_date = end

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
                            tickers=self.ticker,
                            period=self.period,
                            interval=self.interval,
                            multi_level_index=False)            
            #self.data = pd.concat([yf.download(self.ticker, 
            #                                period=self.period,
            #                                interval=self.interval).assign(ticker=ticker) for ticker in [self.ticker]], ignore_index=True)
            
            return self.data
        except Exception as e:
            return e

    def get_start_end_date_data(self):
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
                tickers=self.ticker,
                start=self.start_date, 
                end=self.end_date,
                interval=self.interval,
                multi_level_index=False)
            
            return self.data
        except Exception as e:
            return e
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
        
        # initialize Asset object 
        asset = Asset( self.stock_ticker, start=startdate, end=enddate, period=period, interval=interval)
        asset_info = asset.get_info()  # Information about the Company
        #asset_df = asset.get_data()    # Historical price data    
        asset_df = asset.get_start_end_date_data()    # Historical price data    

        asset_df.reset_index(inplace=True)
        '''
        # Renaming columns using a dictionary
        df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)
        '''
        #asset_df.rename(columns={"Date": "day", "Open": "open", "High": "high", 
        #                          "Low": "low", "Close": "close", "Adj Close": "adj close", 
        #                          "Volume":"volume"}, inplace=True)
    
        self.stock_data = asset_df
        
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

    def calculate_MACD(self, period1=12, period2=26, period3=9):
        """Default is set to 12 and 26 exponential moving average for macd
        9 period units for signal"""
        # ewm = exponential weighted mean from pandas
        ema1 = self.data['Close'].ewm(span=period1, adjust=False).mean()   
        ema2 = self.data['Close'].ewm(span=period2, adjust=False).mean()
        macd_line = ema1 - ema2
        macd_signal = self.data['Close'].ewm(span=period3, adjust=False).mean()

        self.data['MACD'] = macd_line
        self.data['MACD Signal'] = macd_signal
        self.data['MACD Histogram'] = macd_line - macd_signal

        #return self.data

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
                                    monthly_window=20, quarterly_window=60):
        self.stock_data['MA_5'] = self.stock_data['Close'].rolling(window=weekly_window).mean()
        self.stock_data['MA_10'] = self.stock_data['Close'].rolling(window=Dweekly_window).mean()
        self.stock_data['MA_20'] = self.stock_data['Close'].rolling(window=monthly_window).mean()
        self.stock_data['MA_60'] = self.stock_data['Close'].rolling(window=quarterly_window).mean()
        #return data

    def calculate_exponential_moving_averages(self, weekly_window=5, Dweekly_window=10, \
                                    monthly_window=20, quarterly_window=60):
        self.stock_data['EMA_5'] = self.stock_data['Close'].ewm(ignore_na=False, span=weekly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_10'] = self.stock_data['Close'].ewm(ignore_na=False, span=Dweekly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_20'] = self.stock_data['Close'].ewm(ignore_na=False, span=monthly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_60'] = self.stock_data['Close'].ewm(ignore_na=False, span=quarterly_window, min_periods=0, adjust=False).mean()
        
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
        self.two_dog = True if three_MAs and min(stock_price, MA5, MA10) == stock_price else False 
        self.one_dog = True if three_MAs and min(stock_price, MA5) == stock_price else False 
        
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
        
        self.four_E_dog = True if four_Expon_MAs and min(stock_price, EMA5, EMA10, EMA20, EMA60) == stock_price else False
        self.three_E_dog = True if not self.three_dog and three_Expon_MAs and min(stock_price, EMA5, EMA10, EMA20) == stock_price else False
        self.two_E_dog = True if not self.two_dog and two_Expon_MAs and min(stock_price, EMA5, EMA10) == stock_price else False
        self.one_E_dog = True if not self.one_dog and one_Expon_MAs and min(stock_price, EMA5) == stock_price else False                                                            
                            
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
        elif self.two_dog:
            self.stock_MA_status = 'two_dog'
            return
        elif self.one_dog:
            self.stock_MA_status = 'one_dog'
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
async def yfinance_fetch(ticker, startdate, enddate, opt_verbose='OFF'):    
    data = yf.download(tickers=ticker, start=startdate, end=enddate,
                        interval='1d', multi_level_index=False)
    
    data.rename(columns={"Date": "day", "Open": "open", "High": "high", 
                        "Low": "low", "Close": "close", "Volume":"volume"}, inplace=True)
    
    if opt_verbose.lower() == 'low':
        logger.info(f'data: {data}')
        
    return {"meta": data}

async def yfinance_asyncio(ticker, startdate, enddate, opt_verbose='OFF'):
    yfData = await yfinance_fetch(ticker, startdate, enddate, opt_verbose=opt_verbose)
    yf_df = yfData['meta'].copy()
                
    if opt_verbose.lower() == 'on':
         logger.info(f'yf_df:\n{yf_df}')                

    return yf_df

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
    
    
    def yfinance_asyncio_interval_startdate_enddate(self):
        # initialize Asset object 
        try:
            bars = asyncio.run(yfinance_asyncio(ticker= self.stock_ticker, 
                                                startdate= self.startdate, 
                                                enddate= self.enddate, 
                                                opt_verbose= self.opt_verbose))
            self.stock_data = bars.copy()
            self.stock_data.reset_index(inplace=True)
        except Exception as e:
            logger.info(f'Error: {e}')
            exit(0)
                            
    # 移動平均線を計算する関数
    def calculate_moving_averages(self, weekly_window=5, Dweekly_window=10, \
                                    monthly_window=20, quarterly_window=60):
        self.stock_data['MA_5'] = self.stock_data['close'].rolling(window=weekly_window).mean()
        self.stock_data['MA_10'] = self.stock_data['close'].rolling(window=Dweekly_window).mean()
        self.stock_data['MA_20'] = self.stock_data['close'].rolling(window=monthly_window).mean()
        self.stock_data['MA_60'] = self.stock_data['close'].rolling(window=quarterly_window).mean()
        #return data

    def calculate_ShortMediumTerm_moving_averages(self, three_window=3, weekly_window=5, seven_window=7, thirteen_window=13, \
                                    twentyeight_window=28, eightyfour_window=84, \
                                    Dweekly_window=10, monthly_window=20, quarterly_window=60):
        self.stock_data['MA_3'] = self.stock_data['close'].rolling(window=three_window).mean()
        self.stock_data['MA_5'] = self.stock_data['close'].rolling(window=weekly_window).mean()
        self.stock_data['MA_7'] = self.stock_data['close'].rolling(window=seven_window).mean()
        self.stock_data['MA_13'] = self.stock_data['close'].rolling(window=thirteen_window).mean()
        self.stock_data['MA_28'] = self.stock_data['close'].rolling(window=twentyeight_window).mean()
        self.stock_data['MA_84'] = self.stock_data['close'].rolling(window=eightyfour_window).mean()
        
        self.stock_data['MA_10'] = self.stock_data['close'].rolling(window=Dweekly_window).mean()
        self.stock_data['MA_20'] = self.stock_data['close'].rolling(window=monthly_window).mean()
        self.stock_data['MA_60'] = self.stock_data['close'].rolling(window=quarterly_window).mean()
        
    def calculate_exponential_moving_averages(self, weekly_window=5, Dweekly_window=10, \
                                    monthly_window=20, quarterly_window=60):
        self.stock_data['EMA_5'] = self.stock_data['close'].ewm(ignore_na=False, span=weekly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_10'] = self.stock_data['close'].ewm(ignore_na=False, span=Dweekly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_20'] = self.stock_data['close'].ewm(ignore_na=False, span=monthly_window, min_periods=0, adjust=False).mean()
        self.stock_data['EMA_60'] = self.stock_data['close'].ewm(ignore_na=False, span=quarterly_window, min_periods=0, adjust=False).mean()
    
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
        self.two_dog = True if three_MAs and min(stock_price, MA5, MA10) == stock_price else False 
        self.one_dog = True if three_MAs and min(stock_price, MA5) == stock_price else False 
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'four_flag: {self.four_flag}; three_flag: {self.three_flag}; two_flag: {self.two_flag}; one_flag: {self.one_flag}')
            logger.info(f'four_dog: {self.four_dog}; three_dog: {self.three_dog}; two_dog: {self.two_dog}; one_dog: {self.one_dog}')

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
        
        self.four_E_dog = True if four_Expon_MAs and min(stock_price, EMA5, EMA10, EMA20, EMA60) == stock_price else False
        self.three_E_dog = True if not self.three_dog and three_Expon_MAs and min(stock_price, EMA5, EMA10, EMA20) == stock_price else False
        self.two_E_dog = True if not self.two_dog and two_Expon_MAs and min(stock_price, EMA5, EMA10) == stock_price else False
        self.one_E_dog = True if not self.one_dog and one_Expon_MAs and min(stock_price, EMA5) == stock_price else False 
    
    def stand_Up_ShortMediumTerm_trend(self):
        # 抓出所需data
        stock_price = self.stock_data['close'].astype(float).iloc[-1]
        MA3 = self.stock_data['MA_3'].iloc[-1] if not self.stock_data['MA_3'].isnull().values.all() else 0
        MA5 = self.stock_data['MA_5'].iloc[-1] if not self.stock_data['MA_5'].isnull().values.all() else 0
        MA7 = self.stock_data['MA_7'].iloc[-1] if not self.stock_data['MA_7'].isnull().values.all() else 0
        MA13 = self.stock_data['MA_13'].iloc[-1] if not self.stock_data['MA_13'].isnull().values.all() else 0
        MA28 = self.stock_data['MA_28'].iloc[-1] if not self.stock_data['MA_28'].isnull().values.all() else 0
        MA84 = self.stock_data['MA_84'].iloc[-1] if not self.stock_data['MA_84'].isnull().values.all() else 0
        
        shortTerm_trend = MA3 and MA5 and MA7 and MA13
        mediumTerm_trend = MA7 and MA28 and MA84
        
        self.shortTerm_trend_flag = True if shortTerm_trend and max(stock_price, MA3, MA5, MA7, MA13) == stock_price else False
        self.mediumTerm_trend_flag = True if mediumTerm_trend and max(stock_price, MA7, MA28, MA84) == stock_price else False

        #if self.opt_verbose.lower() == 'on':
        logger.info(f'shortTerm_trend_flag: {self.shortTerm_trend_flag}; mediumTerm_trend_flag: {self.mediumTerm_trend_flag}')
            
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
                logger.info("股價已站上5日、10日、20日、60日均線，為四海遊龍型股票!!")
            elif self.three_flag:
                logger.info("股價已站上5日、10日、20日均線，為三陽開泰型股票!!")
            elif self.two_flag:
                logger.info("股價已站上5日、10日均線，為雙囍臨門型股票!!")    
            elif self.one_flag:
                logger.info("股價已站上5日均線，為一星報喜型股票!!")        
            elif self.four_dog:
                logger.info("股價已跌破5日、10日、20日、60日均線均線，為四腳朝天型股票!!")    
            elif self.three_dog:
                logger.info("股價已跌破5日、10日、20日均線，為三人成虎型股票!!")        
            elif self.two_dog:
                logger.info("股價已跌破5日、10日均線，為二竪作惡型股票!!")
            elif self.one_dog:
                logger.info("股價已跌破5日均線，為一敗塗地型股票!!")                            
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
        
        self.prev_day_close = self.stock_data['close'].astype(float).iloc[-2]
    
    def check_ShortMediumTerm_MAs(self, weekly_window=5):
        # 必要な列を抽出
        #data = self.stock_data[['Close', 'Volume', 'High', 'Low']].copy()
        
        # 移動平均線を計算
        self.calculate_ShortMediumTerm_moving_averages()
        
        self.stand_Up_ShortMediumTerm_trend() 
        
        if self.opt_verbose.lower() == 'on':
            # 判斷data值
            if self.mediumTerm_trend_flag:
                logger.info("股價已站上7日、28日、84日均線，為中期趨勢股票!!")
            elif self.shortTerm_trend_flag:
                logger.info("股價已站上3日、5日、7日、13日均線，為短期趨勢股票!!")
        
        self.close = self.stock_data['close'].astype(float).iloc[-1]
        self.open = self.stock_data['open'].astype(float).iloc[-1]
        self.high = self.stock_data['high'].astype(float).iloc[-1]
        self.low = self.stock_data['low'].astype(float).iloc[-1]
        self.volume = self.stock_data['volume'].astype(float).iloc[-1]
        self.volume_avg_weekly = self.stock_data['volume'].rolling(window=weekly_window).mean().astype(float).iloc[-1]
        
        self.prev_day_close = self.stock_data['close'].astype(float).iloc[-2]
    
    # ボリンジャーバンドを計算する関数
    def calculate_bollinger_bands(self, window=20):
        sma = self.stock_data['close'].rolling(window=window).mean()
        std = self.stock_data['close'].rolling(window=window).std()
        self.stock_data['Bollinger Middle'] = sma
        self.stock_data['Bollinger Upper'] = sma + (std * 2)
        self.stock_data['Bollinger Lower'] = sma - (std * 2)

        if self.opt_verbose.lower() == 'on':
            logger.info(f"calculate_bollinger_bands window={window}, BB_Middle: {self.stock_data['Bollinger Middle'].astype(float).iloc[-1]}, \
                    BB_Upper: {self.stock_data['Bollinger Upper'].astype(float).iloc[-1]},BB_Lower: {self.stock_data['Bollinger Lower'].astype(float).iloc[-1]}")
        
    # RSIを計算する関数
    def calculate_RSI(self, window=14):
        delta = self.stock_data['close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)

        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()

        rs = avg_gain / avg_loss
        self.stock_data['RSI'] = 100 - (100 / (1 + rs))

        if self.opt_verbose.lower() == 'on':
            logger.info(f"calculate_RSI window={window}, RSI: {self.stock_data['RSI'].astype(float).iloc[-1]}")
        
    def calculate_MACD(self, period1=12, period2=26, period3=9):
        """Default is set to 12 and 26 exponential moving average for macd
        9 period units for signal"""
        # ewm = exponential weighted mean from pandas
        ema1 = self.stock_data['close'].ewm(span=period1, adjust=False).mean()   
        ema2 = self.stock_data['close'].ewm(span=period2, adjust=False).mean()
        macd_line = ema1 - ema2
        macd_signal = self.stock_data['close'].ewm(span=period3, adjust=False).mean()

        self.stock_data['MACD'] = macd_line
        self.stock_data['MACD Signal'] = macd_signal
        self.stock_data['MACD Histogram'] = macd_line - macd_signal
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f"calculate_MACD period1={period1}, period2={period2}, period3={period3}")        
            logger.info(f"MACD: {self.stock_data['MACD'].astype(float).iloc[-1]}, \
                        MACD Signal={self.stock_data['MACD Signal'].astype(float).iloc[-1]}, \
                        MACD Histogram={self.stock_data['MACD Histogram'].astype(float).iloc[-1]}")
                        
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
        elif self.two_dog:
            self.stock_MA_status = 'two_dog'
            return
        elif self.one_dog:
            self.stock_MA_status = 'one_dog'
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
            
    def filter_ShortMediumTerm_MAs(self):
        if self.shortTerm_trend_flag:
            self.shortmediumTerm_trend_MA_status = 'ShortTerm_trend'
            return
        elif self.mediumTerm_trend_flag:
            self.shortmediumTerm_trend_MA_status = 'MediumTerm_trend'
            return
        else:
            self.shortmediumTerm_trend_MA_status = 'NA' 