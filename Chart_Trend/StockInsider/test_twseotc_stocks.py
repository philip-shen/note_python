'''
smalldan1022 /Taiwan-Stocks
https://github.com/smalldan1022/Taiwan-Stocks
台灣上市櫃公司爬蟲，分析盤後股票趨勢以及繪製K線圖、均線圖、三大法人成交量 
'''
import os, time, sys
import twseotc_stocks.Taiwan_Stocks as TS
import twseotc_stocks.lib_misc as lib_misc
from twseotc_stocks.logger_setup import *

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.'.format( time_consumption)#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg)

if __name__ == '__main__':
    logger_set(strdirname)
    
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    
    db_settings = { "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "YOUR-PASSWORD-HERE!!",
                "db": "YOUR-DATABASE-SCHEMA-NAME-HERE!!",
                "charset": "utf8" }

    # If you don't have the MySQL database, just simply set  <------ IMPORTANT MESSAGE
    db_settings = None                                     #<------ IMPORTANT MESSAGE
    MySQL_flag = False                                     #<------ IMPORTANT MESSAGE
    Fetch_stock_statistics_flag = False                    #<------ IMPORTANT MESSAGE

    # Crawl stock data, save data into MySQL, fetch data from MySQL
    stocks = TS.Taiwan_Stocks( db_settings = db_settings, Crawl_flag = True, MySQL_flag = MySQL_flag, 
                           Fetch_stock_statistics_flag = Fetch_stock_statistics_flag, timesleep = 5)

    # Draw plots
    stocks.draw_plots( D_5MA=True, D_10MA = True, D_20MA = True, D_60MA=True, D_IT=True, D_FI=True, D_DL=True, 
                   save_fig=False, fig_name="", save_path="")

    # Calculate the stock's dependency
    stocks.Dependency( IT_flag = True, IT_stocks_number = 50, FI_flag = True, FI_stocks_number = 100, 
                   DL_flag = True, DL_stocks_number = 4, date_interval = 3, value_date_interval = 2)

    stocks.Stand_Up_On_MAs()

    logger.info("\n  {}".format("(6) Closing the program")) 
    logger.info("----------------------------------------")   
    logger.info("\nProgram Finished...\n") 
    
    est_timer(t0)    