'''
Python：基金持股爬蟲 
https://clover59.blogspot.com/2024/03/python.html

Python：台股ETF爬蟲 
https://clover59.blogspot.com/2024/04/pythonetf.html

Python：台股ETF爬蟲(２)持股頁面 
https://clover59.blogspot.com/2024/04/pythonetf_16.html
'''
'''
MoneyDJ ETF網站爬蟲程式 (ETF Website Scraper)
此程式用於抓取 MoneyDJ 理財網站上的 ETF 相關資訊，包括：

https://raw.githubusercontent.com/odindino/ETFcrawler/refs/heads/main/moneydj-scraper.py
'''

import os, sys, time
import pandas as pd
import argparse
import pathlib
import requests
from requests.exceptions import Timeout
import json, re, pickle
from bs4 import BeautifulSoup
from io import StringIO

import twseotc_stocks.lib_misc as lib_misc
from insider.logger_setup import *
from insider.moneydj_scraper import *
from top300_stock_etf_momentum_indicator import *

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.'.format( time_consumption)#msg = 'Time duration: {:.3f} seconds.'
    logger.info(msg)

'''
    和淨值頁面https://www.moneydj.com/ETF/X/Basic/Basic0007.xdjhtm?etfid=00981A.TW
    就是差在淨值頁面網址是Basic0003，持股頁面是Basic0007B。
'''
# 取得持股明細
def get_etf_holds_MoneyDJ(ticker):
    url = f'https://www.moneydj.com/ETF/X/Basic/Basic0003.xdjhtm?etfid={ticker}'
    url = re.sub('[B|b]asic0003', 'Basic0007B', url)
    response = requests.get(url)
    response.encoding = 'utf-8'
    web_content = response.text
    soup = BeautifulSoup(web_content, 'lxml')
    # 取出表格文字屬性 
    update_str = soup.find('div', id='ctl00_ctl00_MainContent_MainContent_sdate3').text
    data = soup.find_all('table', id='ctl00_ctl00_MainContent_MainContent_stable3')[0]
    #data = soup.select_one("#ctl00_ctl00_MainContent_MainContent_stable3")
    
    # 將 HTML 字串包裝在 StringIO 物件
    df2 = data.prettify()  
    df2 = StringIO(df2)
    lst = pd.read_html(df2)    
    df = lst[0]
    df = df.reset_index(drop=True)
    logger.info(f'{df}')
    
    return df, update_str

def csv_fromMoneyDJ_pickle(ticker, json_data, opt_verbose= 'OFF'):
           
    # 建立爬蟲器實例 (Create scraper instance)
    scraper = ETFScraper(opt_verbose)
    
    # 獲取所有數據 (Get all data)
    #"etf00981A" #'00981A.TW'
    ticker_for_MoneyDJ = ticker.lower().replace('etf', '').upper()+'.TW' 
    data = scraper.get_all_data(etf_code= ticker_for_MoneyDJ)

    # 顯示基本資訊 (Display basic information)
    logger.info("\n基本資訊 (Basic Information):")
    logger.info(pd.DataFrame([data['basic_info']]))

    # 顯示持股資訊 (Display holdings information)
    logger.info("\n持股資訊 (Holdings Information):")
    holdings = data.get('holdings', {})
    for holding_type in ['holdings_by_region', 'holdings_by_sector', 'top_holdings', 'all_holdings']:
        df = holdings.get(holding_type)
        if df is not None and not df.empty:
            logger.info(f"{holding_type}:")
            logger.info(f'\n{df}')
        else:
            logger.info(f"\n{holding_type}: 無資料 (No data)")
    
    df_all_holdings = holdings.get('all_holdings')
    now_datetime = datetime.strftime(datetime.now(), '%Y%m%d')
    pickle_csvfname = f'{ticker}Components_{now_datetime}.csv'
    # 去除所有字符串类型列里的换行符和前后空格
    df = df_all_holdings.apply(lambda col: col.str.replace('\r\n', '').str.strip() if col.dtype == 'object' else col)
    df.to_csv(pickle_csvfname, sep=',', na_rep='NULL', index=False)
    
    dict_path_pickle_ticker= json_data["dict_twse_otc_us_id_pickle"]
    json_data["lastest_datastr_twse_tpex"][0] = "csv"
    json_data["lastest_datastr_twse_tpex"][-1] = pickle_csvfname
    if json_data["lastest_datastr_twse_tpex"][0].lower() == "csv":        
        store_twse_tpex_ticker_weight_ration_fromCSV(ticker, json_data, dict_path_pickle_ticker, path_csv_stock_id= '', opt_verbose= 'On')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='stock indicator')
    parser.add_argument('--conf_json', type=str, default='config.json', help='Config json')
    #parser.add_argument('--gspred_json', type=str, default='xxxx.json', help='Google Sheet Certi json')
    
    args = parser.parse_args()
    
    logger_set(strdirname)
    
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    
    json_file= args.conf_json
    json_gsheet= None#args.gspred_json
    
    json_path_file = pathlib.Path(strdirname)/json_file
    
    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )    
        est_timer(t0)
        sys.exit()

    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f)  
        
    opt_verbose= 'OFF'
    # 指定要查詢的ETF代碼 (Specify ETF code to query)
    #"etf00981A" #'00981A.TW'
    #ticker = json_data["lastest_datastr_twse_tpex"][1].lower().replace('etf', '').upper()+'.TW'
    #csv_fromMoneyDJ_pickle(ticker,json_data)
    
    if json_data["lastest_datastr_twse_tpex"][1].__len__() > 1:
        for ticker in json_data["lastest_datastr_twse_tpex"][1]:
            csv_fromMoneyDJ_pickle(ticker, json_data, opt_verbose)
    
    est_timer(t0)    