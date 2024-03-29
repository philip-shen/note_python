import os, sys, time
import pickle, json
import pathlib
import argparse
from insider import StockInsider
import yfinance as yf
import difflib
from sys import platform

from insider.stock import Stock

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

sys.path.append('./insider')
from logger_setup import *
import lib_misc

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

def local_func_trial(json_data):
    options = gen_ticker_dict(json_data)
    
    for stock_id in json_data["stock_indexes"]:
        ticker= get_ticker_from_stock_id(options, stock_id)
        logger.info(f"stock_id: {stock_id} == ticker: {ticker}")     
    
        # initialize Asset object 
        asset = Asset(ticker, period='1y', interval='1d')
        asset_info = asset.get_info()  # Information about the Company
        asset_df = asset.get_data()    # Historical price data    
        #logger.info(f"asset_df: \n{asset_df}")

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='describe image content with Claude 3')
    parser.add_argument('--conf', type=str, default='config.json', help='Config json')
    args = parser.parse_args()
    
    logger_set(strdirname)
    
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    
    json_file= args.conf
    json_path_file = pathlib.Path(strdirname)/json_file
    
    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )    
        est_timer(t0)
        sys.exit()

    json_data = json.load(json_path_file.open())
    
    #local_func_trial(json_data)
    #lib_stock_trial(json_data)
    
    
    for stk_idx in json_data["stock_indexes"]:
        t0 = time.time()
        image_fname_path= f"{image_save_path(json_data)}/{stk_idx}.jpg"
        logger.info(f'export image to {image_save_path(json_data)}/{stk_idx}.jpg')
        
        si = StockInsider(stock_idx = stk_idx, code= None, fname_twse_otc_id_pickle = json_data["twse_otc_id_pickle"])
        df_stock_data= si.show_data()
        df_stock_data.reset_index(inplace=True)
        #si.plot_boll(head= df_stock_data.__len__(), n=6, verbose=True)
        chart_figure= si.plot_bbiboll(head= df_stock_data.__len__(), n=6, m=6, verbose=True)

        si._export_image(chart_figure, image_fname_path)
        
        est_timer(t0)    
    '''
    # Renaming columns using a dictionary
    df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)
    '''    
    '''
    df_stock_data.rename(columns={"Date": "day", "Open": "open", "High": "high", 
                                  "Low": "low", "Close": "close", "Adj Close": "adj close", 
                                  "Volume":"volume"}, inplace=True)    
    logger.info(f" {df_stock_data.keys()}" )
    logger.info(f"df_stock_data: \n{df_stock_data}")
    ''' 
    est_timer(t0)    