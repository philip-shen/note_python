from IPython.core.display import HTML
from pyquery import PyQuery as pq
import pandas as pd
import scrapy
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
import pickle
import openpyxl, difflib

from logger_setup import *

"""
本國上市證券國際證券辨識號碼一覽表
https://isin.twse.com.tw/isin/C_public.jsp?strMode=2
本國上櫃證券國際證券辨識號碼一覽表
https://isin.twse.com.tw/isin/C_public.jsp?strMode=4
"""


__all__ = [
    'query_twse_otc_code_00',
    'StockCodeSpider',
    'query_twse_otc_code_01',
    'query_twse_otc_info',
    'query_twse_otc_info_by_pickle',
    'query_twse_otc_idx',
    'dump_pickle',
]
"""
[Python] 抓取證券編碼一覽表
https://jerrynest.io/python-twse-stock-list/
"""
def query_twse_otc_code_01(str_url, opt_verbose= 'OFF'):
    #url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    res = requests.get(str_url, verify = False)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    table = soup.find("table", {"class" : "h4"})
    c = 0
    for row in table.find_all("tr"):
        data = []
        for col in row.find_all('td'):
            col.attrs = {}
            data.append(col.text.strip().replace('\u3000', ''))
        
        if len(data) == 1:
            pass # title 股票, 上市認購(售)權證, ...
        else:
            #print(data)
            if opt_verbose.lower() == 'on':
                logger.info(data )


"""
07.爬股票代號、產業別 
https://ithelp.ithome.com.tw/articles/10203803
"""
columns = ['dtype', 'code', 'name', '國際證券辨識號碼', '上市日', '市場別', '產業別', 'CFI']
"""
How do I select rows from a DataFrame based on column values?
https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values
"""
"""
How to convert a dataframe to a dictionary
https://stackoverflow.com/questions/18695605/how-to-convert-a-dataframe-to-a-dictionary
"""
"""
Save Python Dictionary to a Pickle File
https://datascienceparichay.com/article/save-python-dictionary-to-a-pickle-file/
"""
"""
How to Convert Pandas Index to a List (With Examples)
https://www.statology.org/pandas-index-to-list/
"""

def query_twse_otc_code_00(list_str_url, path_xlsx_stock_id, path_pickle_stock_id, opt_verbose= 'OFF'):
    
    items = []
    for url in list_str_url:
        response_dom = pq(url)
        for tr in response_dom('.h4 tr:eq(0)').next_all().items():
            if tr('b'):
                dtype = tr.text()
            else:
                row = [td.text() for td in tr('td').items()]
                code, name = row[0].split('\u3000')
                items.append(dict(zip(columns, [dtype, code, name, *row[1: -1]])))

    dict_data=  {}
    data_temp= pd.DataFrame()
    data= pd.DataFrame(items)
    #data.to_excel(path_xlsx_stock_id, sheet_name='twse_otc_id', index=False, header=True)
    data_temp= data.loc[data['dtype'] == '股票'].copy()
    data_temp= data_temp[['code', 'name', '國際證券辨識號碼', '市場別']].copy()
    data_temp.loc[data_temp['市場別'] == '上市', 'code']= data_temp['code']+'.TW'
    data_temp.loc[data_temp['市場別'] == '上櫃', 'code']= data_temp['code']+'.TWO'
    data_temp.to_excel(path_xlsx_stock_id, sheet_name='twse_otc_id', index=False, header=True)
    dict_data= dict(zip(data_temp.code, data_temp.name))
    list_data= data_temp['code'].values.tolist()

    if opt_verbose.lower() == 'on':
        for key, value in dict_data.items():
            logger.info('\n key: {}; value: {}'.format(key, value) )
    
    # save dictionary to pickle file
    with open(path_pickle_stock_id, 'wb') as file:
        #pickle.dump(dict_data, file, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(list_data, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    #data_temp.to_pickle(path_pickle_stock_id)

    HTML(data.head().to_html())

class StockCodeSpider(scrapy.Spider):
    str_twse_url= 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    str_tpex_url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
    name = 'stock_code'
    start_urls = [str_twse_url, str_tpex_url]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'MONGODB_COLLECTION': name,
        'MONGODB_ITEM_CACHE': 1000,
        'MONGODB_DROP': True
    }

    def parse(self, response):
        for tr in response.dom('.h4 tr:eq(0)').next_all().items():
            if tr('b'):
                dtype = tr.text()
            else:
                row = [td.text() for td in tr('td').items()]
                code, name = row[0].split('\u3000')
                yield dict(zip(columns, [dtype, code, name, *row[1: -1]]))

"""
Python — 透過Yahoo Finance API抓取台股歷史
https://aronhack.medium.com/python-%E9%80%8F%E9%81%8Eyahoo-finance-api%E6%8A%93%E5%8F%96%E5%8F%B0%E8%82%A1%E6%AD%B7%E5%8F%B2%E8%B3%87%E6%96%99-a97feb373e8f            
"""
        
def twse_idx():
    link = 'https://quality.data.gov.tw/dq_download_json.php?nid=11549&md5_url=bb878d47ffbe7b83bfc1b41d0b24946e'
    r = requests.get(link)
    data = pd.DataFrame(r.json())
    
    data.to_csv('./data' + '/stock_id.csv', index=False, header = True)

"""
爬取台股清單並且寫入 Datebase
May 10, 2021
https://medium.com/%E5%B7%A5%E7%A8%8B%E9%9A%A8%E5%AF%AB%E7%AD%86%E8%A8%98/%E7%88%AC%E5%8F%96%E5%8F%B0%E8%82%A1%E6%B8%85%E5%96%AE%E4%B8%A6%E4%B8%94%E5%AF%AB%E5%85%A5-datebase-87c6d3f1348b
"""
def twse_otc_idx(str_url, opt_verbose='OFF'):
    # 抓取股票資訊
    #url = "https://histock.tw/stock/rank.aspx?p=all"
    user_agent = UserAgent()
    headers = {'user-agent': user_agent.random}

    # 獲取 html 資訊
    res = requests.get(str_url, headers = headers)
    
    tmp = BeautifulSoup(res.text, 'lxml').select_one('#CPHB1_gv')
    df = pd.read_html(tmp.prettify())[0]
    # 優化一下欄位名稱
    df.columns = ['stock_no', 'stock_name', 'price', 'ud', 'udp', 'ud_w', 'amp','open', 'high', 'low', 'price_y', 'vol', 'vol_p']
    # 新增欄位註記資料更新時間
    df["etl_date"] = datetime.now()

    return df

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

def query_twse_otc_info(ticker, period='1y', interval='1d', opt_verbose='OFF'):
    asset = Asset(ticker, period, interval)
    asset_info = asset.get_info()  # Information about the Company
    asset_df = asset.get_data()    # Historical price data
    
    # Check in terminal for n_clicks and status
    print('asset_df: {}'.format(asset_df))

def query_twse_otc_info_by_pickle(path_pickle_tickers, period='1y', interval='1d', opt_verbose='OFF'):
    with open(path_pickle_tickers, "rb") as f:
        list_ticker= pickle.load(f)
    
    for ticker in list_ticker:
        asset = Asset(ticker, period, interval)
        asset_info = asset.get_info()  # Information about the Company
        asset_df = asset.get_data()    # Historical price data
    
        # Check in terminal for n_clicks and status
        #print('asset_df: {}'.format(asset_df))
        logger.info( '\n ticker: {}'.format(ticker) )
        logger.info( 'asset_df: \n {}'.format(asset_df) )
"""
PythonでExcel操作（読み込み編）
https://qiita.com/adgjmptw0/items/e21bef0e773fc0e3e47f

PythonでExcel操作（読み書き編集編）
https://qiita.com/adgjmptw0/items/afbf2a0c26e993249ae2
"""
"""
Python - difference between two strings
https://stackoverflow.com/questions/17904097/python-difference-between-two-strings
"""
def query_twse_otc_idx(path_xlsx, path_pickle, opt_verbose='OFF'):
    wb = openpyxl.load_workbook(path_xlsx)

    ws= wb["Sheet1"]
    list_value= []
    dict_value_ticker, list_twse_otc_ticker= {}, []

    for row in ws.iter_rows(min_row=2, min_col=2, max_row=130, max_col=2):        
        for c in row:
            if str(c.value).lower() != 'none':list_value.append(c.value) 
        
    with open(path_pickle, "rb") as f:
        list_ticker = pickle.load(f)

    for value in list_value:
        for ticker in list_ticker:
            output_list = [li for li in difflib.ndiff(str(value), str(ticker)) if li[0] != ' ']
            if output_list== ['+ .', '+ T', '+ W'] or output_list== ['+ .', '+ T', '+ W', '+ O']:
                
                if opt_verbose.lower() == 'on':
                    logger.info('value: {}; ticker: {}'.format(value, ticker) )
                
                dict_value_ticker.update( {'{}'.format(value): '{}'.format(ticker)} )
                list_twse_otc_ticker.append(ticker)

    if opt_verbose.lower() == 'on':
        logger.info('list_value: {}'.format(list_value) )
        
        for ticker in list_ticker:
            logger.info('ticker: {}'.format(ticker))
    
    return dict_value_ticker, list_twse_otc_ticker

def dump_pickle(path_pickle, out_pickle_cont, opt_verbose='OFF'):
    with open(path_pickle, 'wb') as f:
        pickle.dump(out_pickle_cont, f)

    with open(path_pickle, 'rb') as f:
        new_pickle_cont = pickle.load(f)

    if opt_verbose.lower() == 'on':
        logger.info('\n output_pickle: {}'.format(path_pickle) )
        logger.info('\n new_pickle_cont: {}'.format(new_pickle_cont) )