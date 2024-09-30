'''
解决json解析报错：Expecting value: line 1 column 1 (char 0)
https://blog.csdn.net/weixin_44011294/article/details/115439034
'''
#--coding:utf-8--
import gspread
import os, sys, time
import json
import argparse, pathlib

import _libs.lib_misc as lib_misc
from _libs.logger_setup import *
import _libs.googleSS as googleSS
import _libs.yahooFinance as yahooFinance

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.\n'.format( time_consumption)#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='demo how to update Google Sheet')
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
        msg = 'Please check config json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )    
        est_timer(t0)
        sys.exit()
            
    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f)  
        
    gspreadsheet = json_data["gSpredSheet"]
    list_worksheet_spread = json_data["worksheet_gSpredSheet"]
    list_delay_sec = json_data["int_delay_sec"]     
    
    logger.info(f'Read row data from {gspreadsheet}')
    
    opt_verbose = 'OFF'
    # Declare GoogleSS() from googleSS.py
    localGoogleSS=googleSS.GoogleSS(json_gsheet, json_file, opt_verbose)
    
    # for accelerate get twse tpex idx purpose   
    local_stock= yahooFinance.Stock(json_data)        
        
    for worksheet_spread in list_worksheet_spread:
        t1 = time.time()
        localGoogleSS.open_GSworksheet(gspreadsheet, worksheet_spread)
        
        logger.info(f'Read row data of WorkSheet: {worksheet_spread} from {gspreadsheet}')
        #inital row count value 2
        inital_row_num = 2
        
        # 20240929 remark
        # Cause Erro: Expecting value: line 1 column 1 (char 0)
        dict_stock_price_OHLC= localGoogleSS.update_GSpreadworksheet_from_yfiances(inital_row_num, list_delay_sec,
                                                                                   local_pt_stock= local_stock)
        
        #dict_stock_price_OHLC= localGoogleSS.update_GSpreadworksheet_from_pstock(inital_row_num, list_delay_sec,
        #                                                                           local_pt_stock= local_stock)
        
        
        est_timer(t1)

    est_timer(t0)        