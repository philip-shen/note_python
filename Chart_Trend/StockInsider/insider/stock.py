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

    def __init__(self, code: str, stock_idx: str, fname_twse_otc_id_pickle: str, \
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
            self.period = period
            self.interval = interval
            self.fname_twse_otc_id_pickle= fname_twse_otc_id_pickle
            self.gen_ticker_dict()
            self.get_ticker_from_stock_idx()
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
        
    def get_ticker_from_stock_idx( self, opt_verbose='OFF'):    
        
        if opt_verbose.lower() == 'on':
            logger.info(f"options: {self.options}") 
    
        for option in self.options:
            if self.stock_idx+'.TW' in option["label"]:
                #logger.info(f"option['label']: {option['label']} == ticker: {ticker}") 
                self.ticker= option["label"]
                return
            elif self.stock_idx+'.TWO' in option["label"]:
                #logger.info(f"option['label']: {option['label']} == ticker: {ticker}")     
                self.ticker=  option["label"]
                return
            elif "^" in self.stock_idx.lower():
                self.ticker=  self.stock_idx
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
