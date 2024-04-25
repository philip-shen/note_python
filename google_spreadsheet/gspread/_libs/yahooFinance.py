from .logger_setup import *

import pickle, json
import yfinance as yf

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

def get_asset_from_yfinance_ticker(json_file, tw_tse_otc_stk_idx, opt_verbose='off', period='1y', interval='1d'):
    
    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f)  
        
    options = gen_ticker_dict(json_data, opt_verbose)
    
    ticker= get_ticker_from_stock_id(options, tw_tse_otc_stk_idx)
    logger.info(f"stock_id: {tw_tse_otc_stk_idx} == ticker: {ticker}")     
    
    # initialize Asset object 
    asset = Asset(ticker, period=period, interval=interval)
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