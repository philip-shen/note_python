from .logger_setup import *

import re
import pickle, json
import yfinance as yf
import requests
from requests.exceptions import Timeout
from io import StringIO
import pandas as pd

class Asset:
    """Class to initialize the stock, given a ticker, period and interval"""
    def __init__(self, ticker, period='1y', interval='1d'):
        self.ticker = ticker.upper()
        self.period = period
        self.interval = interval

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
        self.list_datastr_twse_tpex = json_data["lastest_datastr_twse_tpex"]
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
        
    def requests_twse_tpex_stock_idx(self):
        ##### 上市公司
        datestr = self.list_datastr_twse_tpex[0]#'20240801'
        r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
        # 整理資料，變成表格
        self.df_twse_website_info = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
        
        ##### 上櫃公司
        datestr = self.list_datastr_twse_tpex[1]#'113/08/01'
        r = requests.post('http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=' + datestr + '&s=0,asc,0')
        # 整理資料，變成表格
        self.df_tpex_website_info = pd.read_csv(StringIO(r.text), header=2).dropna(how='all', axis=1).dropna(how='any')
        
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
            self.Flag_tpex_stocks = self.check_stocks(self.df_tpex_website_info, check_name="名稱", check_num="代號")
            
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