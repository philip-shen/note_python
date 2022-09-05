from IPython.core.display import HTML
from pyquery import PyQuery as pq
import pandas as pd
import scrapy
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
import pickle

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