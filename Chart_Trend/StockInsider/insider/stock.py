from typing import Optional
import re
import pickle

import requests
from requests.exceptions import Timeout
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

from insider.logger_setup import *

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
            return e

    def get_start_end_date_data(self):
        """Uses yfinance to get data, returns a Pandas DataFrame object
        Index: Date
        Columns: Open, High, Low, Close, Adj Close, Volume
        """
        try:
            self.data = yf.download(
                tickers=self.ticker,
                start=self.start_date, 
                end=self.end_date,
                interval=self.interval)
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
        
        # Exponential_moving_averages
        EMA5 = self.stock_data['EMA_5'].iloc[-1] if not self.stock_data['EMA_5'].isnull().values.all() else 0
        EMA10 = self.stock_data['EMA_10'].iloc[-1] if not self.stock_data['EMA_10'].isnull().values.all() else 0
        EMA20 = self.stock_data['EMA_20'].iloc[-1] if not self.stock_data['EMA_20'].isnull().values.all() else 0
        EMA60 = self.stock_data['EMA_60'].iloc[-1] if not self.stock_data['EMA_60'].isnull().values.all() else 0
        
        four_Expon_MAs = EMA5 and EMA10 and EMA20 and EMA60
        three_Expon_MAs = EMA5 and EMA10 and EMA20
        two_Expon_MAs = EMA5 and EMA10
        one_Expon_MAs = EMA5
        
        self.four_E_flag = True if not four_MAs and \
                            (four_Expon_MAs and max(stock_price, EMA5, EMA10, EMA20, EMA60) == stock_price) else False
        self.three_E_flag = True if not three_MAs and \
                            (three_Expon_MAs and max(stock_price, EMA5, EMA10, EMA20) == stock_price) else False
        self.two_E_flag = True if not two_MAs and \
                            (two_Expon_MAs and max(stock_price, EMA5, EMA10) == stock_price) else False
        self.one_E_flag = True if not one_MAs and \
                            (one_Expon_MAs and max(stock_price, EMA5) == stock_price) else False
        
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
        
        #elif not self.four_flag and self.four_E_flag:
        elif self.four_E_flag:
            self.stock_MA_status = 'Expo_four_star'
            return
        #elif not self.three_flag and self.three_E_flag:
        elif self.three_E_flag:
            self.stock_MA_status = 'Expo_three_star'
            return  
        #elif not self.two_flag and self.two_E_flag:
        elif self.two_E_flag:
            self.stock_MA_status = 'Expo_two_star'    
            return  
        #elif not self.two_flag and self.one_E_flag:
        elif self.one_E_flag:
            self.stock_MA_status = 'Expo_one_star'    
            return
        else:
            self.stock_MA_status = 'NA'