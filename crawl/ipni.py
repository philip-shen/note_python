'''
python 3.10

Internation Plant Name Index
'''

import time, sys
import csv
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import json
import argparse, pathlib

import _libs.lib_misc as lib_misc
from _libs.logger_setup import *

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.\n'.format( time_consumption)#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg)
'''
InsecureRequestWarning + MarkupResemblesLocatorWarning: Jan 15, 2024
https://stackoverflow.com/questions/77821731/insecurerequestwarning-markupresembleslocatorwarning
'''
'''
Python + BeautifulSoup: How to get ‘href’ attribute of ‘a’ element? May 6, 2017
https://stackoverflow.com/questions/43814754/python-beautifulsoup-how-to-get-href-attribute-of-a-element
'''
'''
【資料處理】Python Regex 的使用筆記 Oct 30, 2022
https://medium.com/@NeroHin/%E8%B3%87%E6%96%99%E8%99%95%E7%90%86-python-regex-%E7%9A%84%E4%BD%BF%E7%94%A8%E7%AD%86%E8%A8%98-c358ead21208
'''
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }
regex_zh = r'[\\u4e00-\\u9fff]+'#chinese chart

def filter_tableelement(txt_url, opt_verbose= 'OFF'):
    count = 0
    regex = r'/<a\s+(?:[^>]*?\s+)?href="([^"]*)"'
    url_head = "http://kplant.biodiv.tw/"
    list_rtu_urls = []
    response = requests.get(txt_url, verify=False, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Continue with your parsing here
        tags = soup.find_all(lambda tag: tag.name == 'a' and tag.get("href") and tag.text)

        for tag in tags:
            count += 1
            #escape header 14 lines
            if count < 14:
                continue
            
            #re.findall(regex, tag) # returns ['https://uibakery.io']
            txt_href = str(tag).strip().split('"')[1]
            # 先去除英文的情況(index.html)
            del_eng = re.sub('[a-zA-Z]+.', '', txt_href)
            if len(del_eng) == 0:
                continue
                        
            url_plant = url_head+txt_href            
            if opt_verbose.lower() == 'on':
                logger.info(f'del_eng: {del_eng}; lenght of tag: {len(del_eng.strip())}')                
                logger.info(f'tag: {tag}; lenght of tag: {len(str(tag).strip())}')
                logger.info(f'url_plant: {url_plant}' )
                
            list_rtu_urls.append(url_plant)            
            
        #if opt_verbose.lower() == 'on':
        #    logger.info(soup.prettify())
    else:
        logger.info(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    
    if opt_verbose.lower() == 'on':
        logger.info(f'len of list_rtu_urls: {len(list_rtu_urls)}; list_rtu_urls: {list_rtu_urls}')

    return list_rtu_urls
'''
Python爬蟲學習筆記(一) - Requests, BeautifulSoup, 正規表達式,API Dec 20, 2018
https://yanwei-liu.medium.com/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%B8%80-beautifulsoup-1ee011df8768
'''
def get_value_html_table(txt_html, opt_verbose= 'OFF'):
    soup = BeautifulSoup(txt_html, 'html.parser')
    text = soup.get_text(strip=True)
    
    if opt_verbose.lower() == 'on':
        logger.info(f'table value: {text}')

    return text
'''
如何正確在論文中使用動植物學名？
https://www.enago.tw/academy/how-to-write-scientific-names-in-a-research-paper-animals-plants/amp/
'''
def botanical_names(list_txt_urls, filters, opt_verbose= 'OFF'):
    list_idxs = []
    list_url_botanical_names = []

    for txt_url in list_txt_urls:
        
        response = requests.get(txt_url, verify=False, headers=headers)
        if opt_verbose.lower() == 'on':
            logger.info(f'txt_url: {txt_url}')
                
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for tr in soup.findAll("table"):
                for idx, td in enumerate(tr.find_all("td")):
                    #logger.info(f'idx: {idx}')
                    if td.attrs.get('style'):
                        #logger.info(f'filters["eng_names"]: {filters["eng_names"]}')                        
                        if filters['eng_names'] in td.text:
                            if opt_verbose.lower() == 'on':
                                logger.info(f'filters["eng_names"]: {filters["eng_names"]}; initial_idx: {idx}')
                            list_idxs.append(idx)

                        if filters['botanical_names'] in td.text:
                            if opt_verbose.lower() == 'on':
                                logger.info(f'filters["botanical_names"]: {filters["botanical_names"]}; initial_idx: {idx}')
                            list_idxs.append(idx)    

                        if filters['family_names'] in td.text:
                            if opt_verbose.lower() == 'on':
                                logger.info(f'filters["family_names"]: {filters["family_names"]}; initial_idx: {idx}')
                            list_idxs.append(idx)    
                    
            '''
            bypass 
            
            INFO: txt_url: http://kplant.biodiv.tw/小麥/小麥.htm
            INFO: 2
            '''
            #logger.info(tr.find_all("td").__len__())
            #logger.info(tr.find_all("td"))
            #logger.info(f'{filters["eng_names"]}: {tr.find_all("td")[list_idxs[0]+1]}')
            
            if tr.find_all("td").__len__() > 2:
                table_value_eng_names = get_value_html_table(str(tr.find_all("td")[list_idxs[0]+1]), opt_verbose)
                if opt_verbose.lower() == 'on':
                    logger.info(f'{filters["eng_names"]}: {table_value_eng_names.replace("  ", "")}')
            
                #logger.info(f'{filters["botanical_names"]}: {tr.find_all("td")[list_idxs[1]+1]}')
                table_value_botanical_names = get_value_html_table(str(tr.find_all("td")[list_idxs[1]+1]), opt_verbose)
                if opt_verbose.lower() == 'on':
                    logger.info(f'{filters["botanical_names"]}: {table_value_botanical_names.replace("  ", "")}')
            
                #logger.info(f'{filters["family_names"]}: {tr.find_all("td")[list_idxs[2]+1]}')            
        else:
            logger.info(f'txt_url: {txt_url}')
            logger.info(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            
        temp_dict={
            "url": txt_url,
            "eng_names": table_value_eng_names.replace("\xa0", "").replace("\r", "").replace("\n", ""),
            "botanical_names": table_value_botanical_names.replace("\r", "").replace("\n", "")
        }
        
        list_url_botanical_names.append(temp_dict)
        
    return list_url_botanical_names
'''
Python 輸出中文亂碼問題 Sep 1, 2020
https://medium.com/@kk_huang/python-%E8%BC%B8%E5%87%BA%E4%B8%AD%E6%96%87%E4%BA%82%E7%A2%BC%E5%95%8F%E9%A1%8C-c4a540b8401d

'''
def dict_to_csv(csv_file, in_list_dict, opt_verbose= 'OFF'):
    # Specify the field names (headers)
    csv_columns = in_list_dict[0].keys()
    try:
        with open(csv_file, 'w', encoding='utf-8') as csvfile:
            csvfile.write('\ufeff')
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in in_list_dict:
                writer.writerow(data)
    except IOError:
        logger.info("I/O error")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='demo how to crawl HTML Table format')
    parser.add_argument('--conf_json', type=str, default='config.json', help='Config json')
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
        msg = 'Please check config json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )    
        est_timer(t0)
        sys.exit()
            
    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f)  
    
    opt_verbose='ON'
    list_urls = json_data["urls_list"]
    list_plant_ulrs = []
     
    filter_params = {
        'eng_names': '英文名稱',
        'botanical_names': '學名',
        'family_names': '別名'
     }
    for url in list_urls:
        t1 = time.time()
        
        list_plant_ulrs = filter_tableelement(url, opt_verbose='OFF')
        #logger.info(f'lenght of list_plant_ulrs: {len(list_plant_ulrs)};\nlist_plant_ulrs: {list_plant_ulrs}')   
        
        list_dict_botanical_names= botanical_names(list_plant_ulrs, filter_params, opt_verbose='Off')
        
        '''
        temp=['http://kplant.biodiv.tw/一串紅/一串紅.htm','http://kplant.biodiv.tw/小麥/小麥.htm']#['http://kplant.biodiv.tw/一串紅/一串紅.htm','http://kplant.biodiv.tw/朱槿/朱槿.htm']
        list_dict_botanical_names= botanical_names(temp, filter_params, opt_verbose='On')
        '''
        est_timer(t1)

    logger.info(f'len of list_dict_botanical_names: {len(list_dict_botanical_names)};\nlist_dict_botanical_names: {list_dict_botanical_names}')
    
    csv_fname = pathlib.Path(dirnamelog)/'ipni.cvs'
    dict_to_csv(csv_fname, list_dict_botanical_names)
    
    est_timer(t0)        
        