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
dirnamedata= os.path.join(strdirname,"data")
dirnametest= os.path.join(strdirname,"test")

sys.path.append('libs')

from logger_setup import *
import lib_time
import lib_twse_otc

# Global Variable: Ticker List
with open("data/tickers.pickle", "rb") as f:
    TICKER_LIST = pickle.load(f)



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
    path_xlsx_stock_id= os.path.join(dirnamedata, 'twse_otc_id.xlsx')
    path_pickle_stock_id= os.path.join(dirnamedata, 'twse_otc_id.pickle')
    path_pickle_tickers= os.path.join(dirnamedata, 'tickers.pickle')
    path_xlsx_band_op= os.path.join(dirnamedata, 'band_op.xlsx')
    path_pickle_band_op= os.path.join(dirnamedata, 'band_op_202210.pickle')
    path_xlsx_business_cycle= os.path.join(dirnamedata, 'business_cycle.xlsx')
    path_pickle_business_cycle= os.path.join(dirnamedata, 'business_cycle.pickle')
    path_xlsx_steady_growth= os.path.join(dirnamedata, 'steady_growth.xlsx')
    path_pickle_steady_growth= os.path.join(dirnamedata, 'steady_growth_202210.pickle')
    path_xlsx_ETF= os.path.join(dirnamedata, 'ETF.xlsx')
    path_pickle_ETF= os.path.join(dirnamedata, 'ETF.pickle')

    """lib_twse_otc.query_twse_otc_code_00([str_twse_url, str_tpex_url], path_xlsx_stock_id, \
                                         path_pickle_stock_id, opt_verbose='OFF')"""
    
    """lib_twse_otc.query_twse_otc_info('4755.TW', period='2y')"""

    """lib_twse_otc.query_twse_otc_info_by_pickle(path_pickle_stock_id)"""
    

    """for key, value in dict_twse_otc_idx.items():
        print('{}: {}'.format(key, value))           

    for twse_otc_ticker in list_twse_otc_ticker:
        print('twse_otc_ticker: {}'.format(twse_otc_ticker))"""
    
    """_, list_twse_otc_ticker= lib_twse_otc.query_twse_otc_idx(path_xlsx_business_cycle, path_pickle_stock_id)
    lib_twse_otc.dump_pickle(path_pickle_business_cycle, list_twse_otc_ticker,opt_verbose)"""
    '''
    _, list_twse_otc_ticker= lib_twse_otc.query_twse_otc_idx(path_xlsx_band_op, path_pickle_stock_id)
    lib_twse_otc.dump_pickle(path_pickle_band_op, list_twse_otc_ticker,opt_verbose)
    
    _, list_twse_otc_ticker= lib_twse_otc.query_twse_otc_idx(path_xlsx_steady_growth, path_pickle_stock_id)
    lib_twse_otc.dump_pickle(path_pickle_steady_growth, list_twse_otc_ticker,opt_verbose)
    '''
    _, list_etf_ticker= lib_twse_otc.query_twse_otc_idx(path_xlsx_ETF, path_pickle_stock_id)
    lib_twse_otc.dump_pickle(path_pickle_ETF, list_etf_ticker, opt_verbose)
    
    time_consumption, h, m, s= lib_time.format_time(time.time() - t0)         
    msg = 'Time Consumption: {} seconds.'#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time_consumption))                                             