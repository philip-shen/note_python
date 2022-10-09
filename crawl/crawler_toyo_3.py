"""
https://github.com/SuYenTing/104job_data_analyst_analysis
https://github.com/SuYenTing/Python-web-crawler
"""
"""
https://github.com/it-jia/job104_spider
"""

import time, sys
import datetime
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import json

from logger_setup import *
import lib_mongo_atlas

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)

# 確認是否有正常連線
def CheckConnect(url, params, headers):
    try:
        response = requests.get(url, params=params, headers=headers)#requests.get(url, headers=headers)
        checkSuccess = True
        return response, checkSuccess
    except Exception as e:
        print('下載失敗!')
        response = None
        checkSuccess = False
        return response, checkSuccess

def search_params(keyword, page, filter_params=None, sort_type='符合度', is_sort_asc=False, opt_verbose= 'OFF'):
    """搜尋職缺"""
    url, params= '', ''

    url = 'https://www.104.com.tw/jobs/search/'#'https://www.104.com.tw/jobs/search/list'
    query = f'ro=0&kwop=7&keyword={keyword}&expansionType=area,spec,com,job,wf,wktm&mode=s&jobsource=2018indexpoc'
    if filter_params:
        # 加上篩選參數，要先轉換為 URL 參數字串格式
        query += ''.join([f'&{key}={value}' for key, value, in filter_params.items()])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'Referer': 'https://www.104.com.tw/jobs/search/',
    }

    # 加上排序條件
    sort_dict = {
        '符合度': '1',
        '日期': '2',
        '經歷': '3',
        '學歷': '4',
        '應徵人數': '7',
        '待遇': '13',
    }
    sort_params = f"&order={sort_dict.get(sort_type, '1')}"
    sort_params += '&asc=1' if is_sort_asc else '&asc=0'
    query += sort_params

    params = f'{query}&page={page}'

    if opt_verbose.lower() == 'on':
        msg = '\n url: {};\n query: {}'
        logger.info(msg.format(url, query))

    return url, params

def filter_jobelement(in_info, opt_verbose= 'OFF'):
    # 轉為soup格式
    soup = BeautifulSoup(in_info, 'html.parser')

    # 取得搜尋返回結果
    jobList = soup.select('article.b-block--top-bord')
    # 取得職缺公布時間
    jobAnnounceDate = [elem.select('span.b-tit__date')[0].text.replace('\n', '').strip() for elem in jobList]
    # 取得職缺名稱
    jobTitles = [elem.select('a.js-job-link')[0].text for elem in jobList]
    # 取得職缺公司名稱
    jobCompanyName = [elem.select('a')[1].text.replace('\n', '').strip() for elem in jobList]
    # 取得職缺公司頁面資訊連結
    jobCompanyUrl = ['https:' + elem.select('a')[1]['href'] for elem in jobList]
    # 取得職缺公司所屬產業類別
    jobCompanyIndustry = [elem.select('li')[2].text for elem in jobList]
    # 取得待遇資訊
    jobSalary = [elem.select('div.job-list-tag.b-content')[0].select('span')[0].text for elem in jobList]

    # 整理其他工作資訊(工作地點, 年資要求, 學歷要求)
    jobOtherInfo = [elem.select('ul.b-list-inline.b-clearfix.job-list-intro.b-content')[0] for elem in jobList]
    # 取得工作地點
    jobLocation = [elem.select('li')[0].text for elem in jobOtherInfo]
    # 取得年資要求
    jobRqYear = [elem.select('li')[1].text for elem in jobOtherInfo]
    # 取得學歷要求
    jobRqEducation = [elem.select('li')[2].text for elem in jobOtherInfo]

    # 取得職缺網址資訊
    jobDetailUrl = ['https:' + elem.select('a')[0]['href'] for elem in jobList]

    # 迴圈職缺網址資訊取得更詳細資訊
    jobContent = list()
    jobCategory = list()
    jobRqDepartment = list()
    jobSpecialty = list()
    jobOthers = list()
    for i, iJobDetailUrl in enumerate(jobDetailUrl):

        print('目前正在爬取第' + str(page) + '頁連結，當前頁面連結下載進度: ' + str(i+1) + ' / ' + str(len(jobDetailUrl)))

        # 詳細資訊需透過額外的ajax爬取
        iUrl = 'https://www.104.com.tw/job/ajax/content/' + re.search('job/(.*)\?', iJobDetailUrl).group(1)

        # 設定header
        headers = {
            'Referer': iJobDetailUrl,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                          '(KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
        }

        # 取得網頁資料
        # 防呆機制
        checkSuccess = False
        tryNums = 0
        while not checkSuccess:
            response, checkSuccess = CheckConnect(iUrl, None, headers)#CheckConnect(iUrl, headers)
            if not checkSuccess:  # 若爬取失敗 則暫停120秒
                if tryNums == 5:  # 若已重新爬取累計5次 則放棄此次程式執行
                    break
                tryNums += 1
                print('本次下載失敗 程式暫停120秒')
                time.sleep(120)

        # 防呆機制: 若累積爬取資料失敗 則終止此次程式
        if tryNums == 5:
            print('下載失敗次數累積5次 結束程式')
            break

        # 取得網頁資料
        response = response.json()

        # 判斷是否有error: 職務不存在
        if response.get('error'):

            jobContent.append('')
            jobCategory.append('')
            jobRqDepartment.append('')
            jobSpecialty.append('')
            jobOthers.append('')

        else:

            # 取得工作內容
            jobContent.append(response['data']['jobDetail']['jobDescription'])
            # 取得職務類別
            jobCategory.append(','.join([elem['description'] for elem in response['data']['jobDetail']['jobCategory']]))
            # 取得科系要求
            jobRqDepartment.append(','.join(response['data']['condition']['major']))
            # 取得擅長工具
            jobSpecialty.append(','.join([elem['description'] for elem in response['data']['condition']['specialty']]))
            # 取得其他條件
            jobOthers.append(response['data']['condition']['other'])

        # 暫停秒數避免爬太快
        time.sleep(3)

    # 組合資訊成資料表並儲存
    iOutputDf = pd.DataFrame({'jobAnnounceDate': jobAnnounceDate,
                              'jobTitles': jobTitles,
                              'jobCompanyName': jobCompanyName,
                              'jobCompanyUrl': jobCompanyUrl,
                              'jobCompanyIndustry': jobCompanyIndustry,
                              'jobContent': jobContent,
                              'jobCategory': jobCategory,
                              'jobSalary': jobSalary,
                              'jobLocation': jobLocation,
                              'jobRqYear': jobRqYear,
                              'jobRqEducation': jobRqEducation,
                              'jobRqDepartment': jobRqDepartment,
                              'jobSpecialty': jobSpecialty,
                              'jobOthers': jobOthers,
                              'jobDetailUrl': jobDetailUrl})

    return iOutputDf                              

if __name__ == "__main__":
    logger_set(strdirname)

    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    if len(sys.argv) != 2:
        msg = 'Please input config json file!!! '
        logger.info(msg)
        sys.exit()

    json_file= sys.argv[1]

    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )
        sys.exit()
    
    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f)  

    opt_verbose='ON'

    client, db, collection= lib_mongo_atlas.mongodb_conn(json_data, opt_verbose)

    # 爬蟲參數設定
    # 搜尋關鍵詞
    keyword = json_data["opt_keyword"];#'python '
    # 搜尋最大頁數
    maxPage = json_data["maxPage"]

    filter_params = {
        'area': json_data["opt_area"],  # (地區) 6001001000, 台北市,6001002000,新北市,6001005000,桃園市, 6001006000,新竹縣市
        's9': '1', #'1,2,4,8',  # (上班時段) 日班,夜班,大夜班,假日班
        # 's5': '0',  # 0:不需輪班 256:輪班
        # 'wktm': '1',  # (休假制度) 週休二日
        'isnew': '30',  # (更新日期) 0:本日最新 3:三日內 7:一週內 14:兩週內 30:一個月內
        # 'jobexp': '1,3,5,10,99',  # (經歷要求) 1年以下,1-3年,3-5年,5-10年,10年以上
        # 'newZone': '1,2,3,4,5',  # (科技園區) 竹科,中科,南科,內湖,南港
        # 'zone': '16',  # (公司類型) 16:上市上櫃 5:外商一般 4:外商資訊
        # 'wf': '1,2,3,4,5,6,7,8,9,10',  # (福利制度) 年終獎金,三節獎金,員工旅遊,分紅配股,設施福利,休假福利,津貼/補助,彈性上下班,健康檢查,團體保險
        # 'edu': '1,2,3,4,5,6',  # (學歷要求) 高中職以下,高中職,專科,大學,碩士,博士
        # 'remoteWork': '1',  # (上班型態) 1:完全遠端 2:部分遠端
        # 'excludeJobKeyword': '科技',  # 排除關鍵字
        # 'kwop': '1',  # 只搜尋職務名稱
        'jobcat': json_data["opt_jobcat"] # '2009003000,2007000000'"des":"品保／品管類人員" "des":"軟體／工程類人員"
    }

    # 迴圈搜尋結果頁數
    outputDf = pd.DataFrame()
    for page in range(1, maxPage+1):

        # 設定header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                      '(KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
        }

        url, search_param= search_params(keyword, page, filter_params, opt_verbose= 'On' )

        # 取得網頁資料
        # 防呆機制
        checkSuccess = False
        tryNums = 0
        while not checkSuccess:
            response, checkSuccess = CheckConnect(url, search_param, headers)
            if not checkSuccess:   # 若爬取失敗 則暫停120秒
                if tryNums == 5:   # 若已重新爬取累計5次 則放棄此次程式執行
                    break
                tryNums += 1
                print('本次下載失敗 程式暫停120秒')
                time.sleep(120)

        # 防呆機制: 若累積爬取資料失敗 則終止此次程式
        if tryNums == 5:
            print('下載失敗次數累積5次 結束程式')
            break

        # 確認是否已查詢到底
        if '搜尋條件無符合工作機會' in response.text:
            print('搜尋結果已到底 無工作職缺資訊可下載 爬蟲終止!')
            break


        iOutputDf= filter_jobelement(response.text)                          
        outputDf = pd.concat([outputDf, iOutputDf])

    # 加入本次搜尋資訊
    outputDf.insert(0, 'maxPage', maxPage, True)
    outputDf.insert(0, 'keyword', keyword, True)
    now = datetime.datetime.now()
    outputDf.insert(0, 'searchTime', now.strftime('%Y-%m-%d %H:%M:%S'), True)

    # 刪除jobAnnounceDate為空值之列(代表該筆資料屬於104廣告職缺 與搜尋職缺較不相關)
    outputDf = outputDf[outputDf.jobAnnounceDate != '']

    # 輸出csv檔案
    fileName = now.strftime('%Y%m%d_%H%M%S') + '104人力銀行_'+ keyword+ json_data["opt_area"]+ '_爬蟲搜尋結果.csv'
    #fileName = '104人力銀行_' + keyword + '_爬蟲搜尋結果'+ now.strftime('%Y%m%d')+'.csv'
    if json_data["opt_out_csv"].lower() == 'on':
        outputDf.to_csv(fileName, encoding='utf-8-sig')
    
    """
    Convert a Pandas DataFrame to a dictionary
    https://stackoverflow.com/questions/26716616/convert-a-pandas-dataframe-to-a-dictionary

    >>> df = pd.DataFrame({'a': ['red', 'yellow', 'blue'], 'b': [0.5, 0.25, 0.125]})
    >>> df
            a      b
    0     red  0.500
    1  yellow  0.250
    2    blue  0.125

    >>> df.to_dict('records')
    [{'a': 'red', 'b': 0.5}, 
    {'a': 'yellow', 'b': 0.25}, 
    {'a': 'blue', 'b': 0.125}]
    """

    if json_data["opt_out_mongodb"].lower() == 'on':
        lib_mongo_atlas.mongodb_insert_many(db, collection, outputDf.to_dict('records'), ordered=False, opt_verbose='OFF')

    """if opt_verbose.lower() == 'on':
        #msg = 'outputDf: {}'
        #logger.info(msg.format( outputDf))

        msg = 'outputDf.to_dict(\'records\'): {}'
        logger.info(msg.format( outputDf.to_dict('records')))
    """
    client.close()
    
    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))