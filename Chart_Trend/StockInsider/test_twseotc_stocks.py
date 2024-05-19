'''
smalldan1022 /Taiwan-Stocks
https://github.com/smalldan1022/Taiwan-Stocks
台灣上市櫃公司爬蟲，分析盤後股票趨勢以及繪製K線圖、均線圖、三大法人成交量 
'''
import os, platform, time, sys
import json
import pathlib
import argparse

import twseotc_stocks.Taiwan_Stocks as TS
import twseotc_stocks.lib_misc as lib_misc
from twseotc_stocks.logger_setup import *
import insider.googleSS as googleSS

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.'.format( time_consumption)#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg)

def image_save_path(json_data):
    images_path= ''
    if platform == "linux" or platform == "linux2":
        home = os.path.expanduser("~")
        images_path= pathlib.Path(f'{home}/{json_data["images_folder"]}')
    elif platform == "darwin":
        pass
    elif platform == "win32":
        images_path= pathlib.Path(f'{json_data["images_folder"]}')
    
    return images_path    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='plot stock chart volume trend')
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

    # Declare GoogleSS() from googleSS.py
    localGoogleSS=googleSS.GoogleSS(json_gsheet, json_file, opt_verbose)
    
    for worksheet_spread in list_worksheet_spread:
        t1 = time.time()
        localGoogleSS.open_GSworksheet(gspreadsheet, worksheet_spread)
        
        logger.info(f'Read row data of WorkSheet: {worksheet_spread} from {gspreadsheet}')
        #inital row count value 2
        inital_row_num = 2
        
        localGoogleSS.get_stkidx_cnpname(inital_row_num, str_delay_sec)
        
        for dict_stkidx_cnpname in localGoogleSS.list_stkidx_cnpname_dicts:
            #logger.info(f'stock index: {dict_stkidx_cnpname["stkidx"]}; company name: {dict_stkidx_cnpname["cnpname"]}')
            image_fname_path= f'{image_save_path(json_data)}/{dict_stkidx_cnpname["cnpname"]}_MAs.jpg'
            logger.info(f'export image to {image_save_path(json_data)}/{dict_stkidx_cnpname["cnpname"]}_MAs.jpg')

            if dict_stkidx_cnpname["stkidx"] is None:
                pass#twse_two_idx = "^TWII"
            else:
                twse_two_idx = dict_stkidx_cnpname["stkidx"]     
                
    
            # Crawl stock data, save data into MySQL, fetch data from MySQL
            stocks = TS.Taiwan_Stocks( stock_name = "", stock_num = twse_two_idx, \
                                    db_settings = db_settings, Crawl_flag = True, MySQL_flag = MySQL_flag, 
                                    Fetch_stock_statistics_flag = Fetch_stock_statistics_flag, timesleep = 5)

            # Draw plots
            stocks.draw_plots( D_5MA=True, D_10MA = True, D_20MA = True, D_60MA=True, D_IT=True, D_FI=True, D_DL=True, 
                       save_fig=False, fig_name="", save_path="")

            # Calculate the stock's dependency
            #stocks.Dependency( IT_flag = True, IT_stocks_number = 50, FI_flag = True, FI_stocks_number = 100, 
            #           DL_flag = True, DL_stocks_number = 4, date_interval = 3, value_date_interval = 2)

            #stocks.Stand_Up_On_MAs()

            logger.info("  {}".format("(6) Closing the program")) 
            logger.info("----------------------------------------")   
            logger.info("Program Finished...\n") 
    
    est_timer(t0)    