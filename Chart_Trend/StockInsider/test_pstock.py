'''
[BUG] aiodns needs a SelectorEventLoop on Windows? #729 
https://github.com/nathom/streamrip/issues/729

Had the same issue on a new install. I found out that aiohttp 3.10.0 on Windows is the issue. Downgrade it to 3.9.5
pip3 install aiohttp==3.9.5
'''
'''
To get Bars there are a couple of arguments that can be specified:

    interval: one of 1m, 2m, 5m, 15m, 30m, 1h, 1d, 5d, 1mo, 3mo, defaults to None
    period: one of 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max, defaults to None
    start: Any date/datetime supported by pydnatic, defaults to None
    end: Any date/datetime supported by pydnatic, defaults to None
    events: one of div, split, div,splits, defaults to div,splits
    include_prepost: Bool, include Pre and Post market bars, default to False

'''

import asyncio
import os, sys, time
import argparse
import pathlib
import json, re, pickle

# Import
from pstock import Bars, BarsMulti
import twseotc_stocks.lib_misc as lib_misc
from insider.logger_setup import *
from insider.stock import *

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
'''
INFO: HTTP Request: GET https://query2.finance.yahoo.com/v8/finance/chart/2330.TW?interval=1h&events=div%2Csplits&includePrePost=false&period1=1717372800&period2=1726790400 "HTTP/1.1 200 OK"
INFO: ticker: 2330.TW; stock name: 台積電
INFO: bars.df:
                         date   open   high    low  close  adj_close     volume        interval
0   2024-06-03 01:00:00+00:00  839.0  847.0  837.0  847.0      847.0        0.0 0 days 01:00:00
1   2024-06-03 02:00:00+00:00  847.0  853.0  846.0  852.0      852.0  5924046.0 0 days 01:00:00
2   2024-06-03 03:00:00+00:00  853.0  853.0  850.0  851.0      851.0  2344066.0 0 days 01:00:00
3   2024-06-03 04:00:00+00:00  851.0  851.0  848.0  849.0      849.0  3034463.0 0 days 01:00:00
4   2024-06-03 05:00:00+00:00  849.0  852.0  849.0  850.0      850.0  2087760.0 0 days 01:00:00
..                        ...    ...    ...    ...    ...        ...        ...             ...
371 2024-09-19 02:00:00+00:00  938.0  950.0  938.0  949.0      949.0  7523344.0 0 days 01:00:00
372 2024-09-19 03:00:00+00:00  950.0  952.0  947.0  952.0      952.0  6381810.0 0 days 01:00:00
373 2024-09-19 04:00:00+00:00  952.0  952.0  949.0  952.0      952.0  4122869.0 0 days 01:00:00
374 2024-09-19 05:00:00+00:00  951.0  955.0  951.0  955.0      955.0  4916511.0 0 days 01:00:00
375 2024-09-19 05:30:00+00:00  960.0  960.0  960.0  960.0      960.0        0.0 0 days 01:00:00
'''
def pstock_main(json_data: dict, opt_verbose='OFF'):    
    list_path_pickle_ticker= json_data["twse_otc_id_pickle"]
    dict_twse_tpex_ticker_cpn_name = query_twse_tpex_ticker(list_path_pickle_ticker[0])
    
    for idx, list_start_end_date in enumerate(json_data["start_end_date"]):
        startdate = date_changer_twse(list_start_end_date[0])
        #for yfinance purpose
        enddate = date_changer_twse_yfinance_end_date(list_start_end_date[-1])

        logger.info(f'start_date: {startdate}; end_date: {date_changer_twse(list_start_end_date[-1])}') 
            
        for ticker, cpn_name in dict_twse_tpex_ticker_cpn_name.items():
            #logger.info('\n ticker: {}; cpn_name: {}'.format(key, value) )    
            ##### 上市公司 or ETF or 正2 ETF
            if bool(re.match('[0-9][0-9][0-9][0-9].TW$', ticker)) or \
                bool(re.match('00[0-9][0-9][0-9].TW$', ticker)) or bool(re.match('00[0-9][0-9][0-9]L.TW$', ticker)):
                    target_ticker = ticker        
                    stock_name = cpn_name

                    #bars = asyncio.run(Bars.get(target_ticker, start=startdate, end=enddate))
                    bars = asyncio.run(Bars.get(target_ticker, period="1d", interval="1m"))
                    bars.df.reset_index(inplace=True)

            logger.info(f"ticker: {target_ticker}; stock name: {stock_name}")    
            if opt_verbose.lower() == 'on':
                logger.info(f'bars.df:\n{bars.df}')
    
    
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
        
    opt_verbose= 'ON'
    
    # Fetch coroutine
    pstock_main(json_data=json_data, opt_verbose=opt_verbose)
    
    est_timer(t0)