import os, sys, time
import pickle, json
import pathlib
import argparse
from insider import StockInsider
import yfinance as yf
import difflib
from sys import platform

import requests
from requests.exceptions import Timeout
import pandas as pd
from io import StringIO

from insider.stock import Stock
import insider.lib_misc as lib_misc
from insider.logger_setup import *
import insider.googleSS as googleSS

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

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
        
def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.'.format( time_consumption)#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg)

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
    
def gen_ticker_dict(json_data):
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

def local_func_trial(json_data, period='1y', interval='1d'):
    options = gen_ticker_dict(json_data)
    
    for stock_id in json_data["stock_indexes"]:
        ticker= get_ticker_from_stock_id(options, stock_id)
        logger.info(f"stock_id: {stock_id} == ticker: {ticker}")     
    
        # initialize Asset object 
        asset = Asset(ticker, period=period, interval=interval)
        asset_info = asset.get_info()  # Information about the Company
        asset_df = asset.get_data()    # Historical price data    
        logger.info(f"asset_df: \n{asset_df}")
        asset_df.reset_index(inplace=True)
        logger.info(f"asset_df['Close']: {asset_df['Close']}")

def lib_stock_trial(json_data):
    
    for stk_idx in json_data["stock_indexes"]:
        local_stock = Stock(stock_idx = stk_idx, code= None, fname_twse_otc_id_pickle = json_data["twse_otc_id_pickle"])
    
        df_stock_data= local_stock.show_data()
        #logger.info(f"df_stock_data: \n{df_stock_data}")
        local_stock.plot(head = df_stock_data.__len__(), verbose = False)
    
def image_save_path(json_data):
    if platform == "linux" or platform == "linux2":
        home = os.path.expanduser("~")
        images_path= pathlib.Path(f'{home}/{json_data["images_folder"]}')
    elif platform == "darwin":
        pass
    elif platform == "win32":
        images_path= pathlib.Path(f'{json_data["images_folder"]}')
    
    return images_path    

### waste 3~4 sec to request so move main routine
def requests_twse_tpex_stock_idx(json_data):
    ##### 上市公司
    datestr = json_data["lastest_datastr_twse_tpex"][0]#'20240801'
    r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
    # 整理資料，變成表格
    df_twse_website_info = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
        
    ##### 上櫃公司
    datestr = json_data["lastest_datastr_twse_tpex"][1]#'113/08/01'
    r = requests.post('http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=' + datestr + '&s=0,asc,0')
    # 整理資料，變成表格
    df_tpex_website_info = pd.read_csv(StringIO(r.text), header=2).dropna(how='all', axis=1).dropna(how='any')
        
    logger.info("Request TWSE and TPEX Stock index..")
    
    return [df_twse_website_info, df_tpex_website_info]
    
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
    json_gsheet= args.gspred_json
    
    json_path_file = pathlib.Path(strdirname)/json_file
        
    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )    
        est_timer(t0)
        sys.exit()

    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f)  
        
    gspreadsheet = json_data["gSpredSheet"]
    list_worksheet_spread = json_data["worksheet_gSpredSheet"]
    str_delay_sec = json_data["str_delay_sec"]     
    
    logger.info(f'Read stock ticker from {gspreadsheet}')
    
    opt_verbose = 'ON'
    # Declare GoogleSS() from googleSS.py
    localGoogleSS=googleSS.GoogleSS(json_gsheet, json_file, opt_verbose)
    
    for worksheet_spread in list_worksheet_spread:
        t1 = time.time()
        localGoogleSS.open_GSworksheet(gspreadsheet, worksheet_spread)
        
        logger.info(f'Read row data of WorkSheet: {worksheet_spread} from {gspreadsheet}')
        #inital row count value 2
        inital_row_num = 2
        
        localGoogleSS.get_stkidx_cnpname(inital_row_num, str_delay_sec)
        list_df_twse_tpex_stock_idx = requests_twse_tpex_stock_idx(json_data)
            
        for dict_stkidx_cnpname in localGoogleSS.list_stkidx_cnpname_dicts:
            
            if dict_stkidx_cnpname["stkidx"] is None:
                #twse_two_idx = "^TWII"
                twse_two_idx = dict_stkidx_cnpname["stkidx"]     
            else:
                twse_two_idx = dict_stkidx_cnpname["stkidx"]     
            
            si = StockInsider( code= None, \
                                stock_idx= twse_two_idx, list_df_twse_tpex_stock_info= list_df_twse_tpex_stock_idx, json_data = json_data)            
            df_stock_data= si.show_data()
            df_stock_data.reset_index(inplace=True)
            
            image_ema_fname_path= f'{image_save_path(json_data)}/{dict_stkidx_cnpname["cnpname"]}_EMA.jpg'
            logger.info(f'export EMA image to {image_save_path(json_data)}/{dict_stkidx_cnpname["cnpname"]}_EMA.jpg')
            
            chart_ema_figure= si.plot_ema(head= df_stock_data.__len__(), ns=None, verbose=True)
            si._export_image(chart_ema_figure, image_ema_fname_path, scale= 2, 
                             width= json_data["width_height"][0], height= json_data["width_height"][1])
            
            #logger.info(f'stock index: {dict_stkidx_cnpname["stkidx"]}; company name: {dict_stkidx_cnpname["cnpname"]}')
            image_fname_path= f'{image_save_path(json_data)}/{dict_stkidx_cnpname["cnpname"]}.jpg'
            logger.info(f'export image to {image_save_path(json_data)}/{dict_stkidx_cnpname["cnpname"]}.jpg')
            #si.plot_boll(head= df_stock_data.__len__(), n=6, verbose=True)
            chart_figure= si.plot_bbiboll(head= df_stock_data.__len__(), n=6, m=6, verbose=True)

            si._export_image(chart_figure, image_fname_path, scale= 2, 
                             width= json_data["width_height"][0], height= json_data["width_height"][1])

            est_timer(t1)    
    
    est_timer(t0)    