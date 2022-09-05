# Data Source
import yfinance as yf
import pickle
import pandas as pd
import requests
import numpy as np
import os, sys, time


strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")
dirname_test_wav= os.path.join(strdirname,"test_wav")
dirnametest= os.path.join(strdirname,"test")

sys.path.append('libs')

from logger_setup import *
import audio
import lib_twse_otc

# Global Variable: Ticker List
with open("data/tickers.pickle", "rb") as f:
    TICKER_LIST = pickle.load(f)

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

    
if __name__ == '__main__':
    logger_set(strdirname)
    
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))         

    opt_verbose='ON'
    #opt_verbose='OFF'
    
    str_twse_url= 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    str_tpex_url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
    path_xlsx_stock_id= os.path.join(dirnamelog, 'twse_otc_id.xlsx')
    path_pickle_stock_id= os.path.join(dirnamelog, 'twse_otc_id.pickle')
    #lib_twse_otc.query_twse_otc_code_00([str_twse_url, str_tpex_url], \
    #                            path_xlsx_stock_id, path_pickle_stock_id, opt_verbose)
    
    df_from_pkl = pd.read_pickle(path_pickle_stock_id)
    print(df_from_pkl)

    """
    asset = Asset(ticker='4755.TW', period='1y', interval='1d')
    asset_info = asset.get_info() 
    asset_info = asset.get_info()  # Information about the Company
    asset_df = asset.get_data()    # Historical price data
    
    # Check in terminal for n_clicks and status
    print('asset_df: {}'.format(asset_df))
    """


    #for i, j in asset_info.items():
    #    print( 'Metric: {}, Value: {}'.format( i, j)) 

    #for i in range(len(TICKER_LIST)):
    #    print( '\"label\": {}; \"value\": {}'.format( str(TICKER_LIST[i]), str(TICKER_LIST[i]) )) 
    
                                        
    time_consumption, h, m, s= audio.format_time(time.time() - t0)         
    msg = 'Time Consumption: {} seconds.'#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time_consumption))                                             