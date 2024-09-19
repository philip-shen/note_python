'''
[BUG] aiodns needs a SelectorEventLoop on Windows? #729 
https://github.com/nathom/streamrip/issues/729

Had the same issue on a new install. I found out that aiohttp 3.10.0 on Windows is the issue. Downgrade it to 3.9.5
pip3 install aiohttp==3.9.5
'''
import asyncio
import os, sys, time
import argparse
import pathlib
import json, re, pickle

# Import
from yahoo_finance_async import OHLC, Interval, History
import twseotc_stocks.lib_misc as lib_misc
from insider.logger_setup import *

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.'.format( time_consumption)#msg = 'Time duration: {:.3f} seconds.'
    logger.info(msg)

def query_twse_tpex_ticker(path_pickle_stock_id, opt_verbose= 'OFF'):
    with open(path_pickle_stock_id, "rb") as f:
        #with open("data/steady_growth.pickle", "rb") as f:
        #with open("data/ETF.pickle", "rb") as f:    
        TICKER_LIST = pickle.load(f)

    return TICKER_LIST

async def main(json_data: dict, opt_verbose='OFF'):    
    list_path_pickle_ticker= json_data["twse_otc_id_pickle"]
    dict_twse_tpex_ticker_cpn_name = query_twse_tpex_ticker(list_path_pickle_ticker[0])
    
    for ticker, cpn_name in dict_twse_tpex_ticker_cpn_name.items():
        #logger.info('\n ticker: {}; cpn_name: {}'.format(key, value) )    
        ##### 上市公司 or ETF or 正2 ETF
        if bool(re.match('[0-9][0-9][0-9][0-9].TW$', ticker)) or \
            bool(re.match('00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('00[0-9][0-9][0-9]L.TW$', ticker)):
                target_ticker = ticker        
                stock_name = cpn_name
            
                result = await OHLC.fetch(target_ticker, interval=Interval.TWO_MINUTE, history=History.DAY)
                # Do something with the result                
                #for temp_dict in result["candles"]:
                #    for key, value in temp_dict.items():
                #        logger.info('\n key: {}; value: {}'.format(key, value) )

        logger.info(f"ticker: {target_ticker}; stock name: {stock_name}")    
        if opt_verbose.lower() == 'on':
            logger.info(f'result["candles"]: {result["candles"]}')
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='stock indicator')
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
    
    json_path_file = pathlib.Path(strdirname)/json_file
    
    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )    
        est_timer(t0)
        sys.exit()

    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f)  
        
    opt_verbose= 'OFF'
    
    # Fetch coroutine
    asyncio.run(main(json_data=json_data))
    
    est_timer(t0)