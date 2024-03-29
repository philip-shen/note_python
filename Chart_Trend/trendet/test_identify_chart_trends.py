'''
refer alvarobartt/trendet
https://github.com/alvarobartt/trendet
Usage
'''
import trendet
import os, sys, time
import yfinance as yf
import pathlib
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import json
from sys import platform

sns.set(style='darkgrid') 

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")
sys.path.append('./_libs')

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
    parser = argparse.ArgumentParser(description='Plot chart trend.')
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
        est_timer()
        sys.exit()

    json_data = json.load(json_path_file.open())
    
    ticker = json_data["ticker"]
    # initialize Asset object 
    asset = Asset(ticker, period='1y', interval='1d')
    asset_info = asset.get_info()  # Information about the Company
    asset_df = asset.get_data()    # Historical price data
                
    res = trendet.identify_df_trends(df=asset_df, column='Close')

    res.reset_index(inplace=True)
    up_trend_color = json_data["up_trend_color"]
    down_trend_color = json_data["down_trend_color"]
    with plt.style.context('seaborn-v0_8-whitegrid'):
        plt.figure(figsize=(12, 6))
        plt.title(f"ticker: {ticker}")
    
        ax = sns.lineplot(x=res['Date'], y=res['Close'])

        labels = res['Up Trend'].dropna().unique().tolist()

        for label in labels:
            sns.lineplot(x=res[res['Up Trend'] == label]['Date'],
                        y=res[res['Up Trend'] == label]['Close'],
                        color=up_trend_color)

            ax.axvspan(res[res['Up Trend'] == label]['Date'].iloc[0],
                       res[res['Up Trend'] == label]['Date'].iloc[-1],
                       alpha=0.1,
                       color=up_trend_color)

        labels = res['Down Trend'].dropna().unique().tolist()

        for label in labels:
            sns.lineplot(x=res[res['Down Trend'] == label]['Date'],
                         y=res[res['Down Trend'] == label]['Close'],
                         color=down_trend_color)

            ax.axvspan(res[res['Down Trend'] == label]['Date'].iloc[0],
                        res[res['Down Trend'] == label]['Date'].iloc[-1],
                        alpha=0.1,
                        color=down_trend_color)

        plt.savefig(f"{image_save_path(json_data)}/{ticker}.jpg")
        logger.info(f"save image to {image_save_path(json_data)}/{ticker}.jpg")
        plt.show()
    
    est_timer(t0)    