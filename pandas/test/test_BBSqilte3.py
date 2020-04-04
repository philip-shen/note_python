# 2018/08/31 Initial to use pandas, matplotlib,TAlib
# 2018/09/01 Using pandas to calculate MA
#            Calculate golden and dead MA
#            Add class PandasDataAnalysis
#            Slove  matplotlib to show Chinese charter
# 2018/09/02 Match '---' and '--' in close price by using regular express
#            Caluclate uprate and downrate by rolling max min of dataframe
# 2018/09/03 add def file1_updownrate_LastMonthYear()
# 2018/09/04 dtype of close price icluding '---' and '--' is object except float64
#            Save as test_SeymourTarget.py
#            Add def file1_updownrate_LastMonthYear()
# 2018/09/05 Add def get_tradedays_dfinfo () and def file2_updownrate_QuarterYear
#            in class PandasDataAnalysis
#            Save as test_SeymourTarget.py
# 2018/09/06 Debug output CSV dulplicated rows.
#            Add def file2_updownrate_threeYearoneYear in class PandasDataAnalysis
# 2018/09/14 Add def file1_call, file1_put, file2_call, file2_put nad percent2float
# 2018/09/15 Add def file3_call and file3_put
# 2018/10/28 Adapte from test_SeymourTarget.py
# 2019/09/30 Adapte from both test_crawl2sqlite3.py and test_SMTargetSqilte.py
#            BB--->Bollinger Band   
#########################################################################
from datetime import datetime, timedelta
import time, os, sys, re
import urllib.request
from lxml import html
import httplib2
from apiclient import discovery
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Flag:
    auth_host_name = 'localhost'
    noauth_local_webserver = False
    auth_host_port = [8080, 8090]
    logging_level = 'ERROR'

flags = Flag()


strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")

# Set logging directory
if not os.path.isdir('logs'):
    os.makedirs('logs')

sys.path.append(dirnamelib)

import excelRW as excelrw
import readConfig as readConfig
import googleDrive as google_drive
import dataAnalysis as data_analysis

N = 240
XMAX = 5
WINMA = 10
ALPHA = 2

def get_bollinger(data, winma=10, alpha=2):
    ser = pd.Series(data)
    ma = ser.rolling(winma).mean()
    std = ser.rolling(winma).std()
    lower = pd.Series(ma - alpha*std).fillna(method='bfill').values
    upper = pd.Series(ma + alpha*std).fillna(method='bfill').values
    return lower, upper

def get_alerts(data, lower, upper):
    low = np.argwhere(data < lower)
    high = np.argwhere(data > upper)
    return low, high

if __name__ == '__main__':
    
    configPath=os.path.join(strdirname,"config.ini")
    localReadConfig = readConfig.ReadConfig(configPath)
    
    stkidx_call_file01 = localReadConfig.get_SeymourExcel('stkidx_call_file01')
    stkidx_put_file01 = localReadConfig.get_SeymourExcel('stkidx_put_file01')
    stkidx_call_file02 = localReadConfig.get_SeymourExcel('stkidx_call_file02')
    stkidx_put_file02 = localReadConfig.get_SeymourExcel('stkidx_put_file02')
    stkidx_call_file03 = localReadConfig.get_SeymourExcel('stkidx_call_file03')
    stkidx_put_file03 = localReadConfig.get_SeymourExcel('stkidx_put_file03')
    stkidx_call_file04 = localReadConfig.get_SeymourExcel('stkidx_call_file04')
    stkidx_put_file04 = localReadConfig.get_SeymourExcel('stkidx_put_file04')

    str_color_ma = localReadConfig.get_SeymourExcel('color_ma05_ma20_ma30')
    list_color_ma = str_color_ma.split(',')
    str_candlestick_weekly_subfolder = localReadConfig.get_SeymourExcel("candlestick_weekly_subfolder")

    url_moneyhunter =localReadConfig.get_SeymourExcel('url_moneyhunterblog')#'http://twmoneyhunter.blogspot.com/'
    #2019/1/10(Thu) excute this code dosen't meet from Mon. to Fri unremak below.
    str_last_year_month_day = localReadConfig.get_SeymourExcel("last_year_month_day")
    str_first_year_month_day = localReadConfig.get_SeymourExcel("first_year_month_day")

    #2019/1/10(Thu) excute this code meet from Mon. to Fri unreamrk below.
    #str_last_year_month_day = datetime.date.today().strftime('%Y,%m,%d')# ex:2018,10,16 get today date form system
    #str_first_year_month_day = datetime.date.today().strftime('%Y,%m,%d')# ex:2018,10,16 get today date form system

    #2019/09/01 MoneyHuter blog webpage layout reversion, value of xpath changed
    #穩定成長，3;指數ETF, 4;債券ETF, 5;波段投機, 6;循環投資, 7;景氣循環, 8
    xpath_url_file01 = '//*[@id="LinkList1"]/div/ul/li[7]/a/@href'#循環投資
    xpath_url_file02 = '//*[@id="LinkList1"]/div/ul/li[6]/a/@href'#波段投機
    xpath_url_file03 = '//*[@id="LinkList1"]/div/ul/li[8]/a/@href'#景氣循環
    xpath_url_file04 = '//*[@id="LinkList1"]/div/ul/li[3]/a/@href'#穩定成長

    #Python urllib urlopen not working
    #https://stackoverflow.com/questions/25863101/python-urllib-urlopen-not-working
    ###########################################
    with urllib.request.urlopen(url_moneyhunter) as response:
        raw = response.read()
    html_doc = html.fromstring(raw)

    credential_dir = os.getcwd()

    localgoogle_drive = google_drive.GoogleDrivebyFileID(dirnamelog,flags)
    credentials = localgoogle_drive.get_credentials(credential_dir)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    fileid_file01 = localgoogle_drive.ggdrive_fileid(html_doc,xpath_url_file01)
    fileid_file02 = localgoogle_drive.ggdrive_fileid(html_doc,xpath_url_file02)
    fileid_file03 = localgoogle_drive.ggdrive_fileid(html_doc,xpath_url_file03)
    fileid_file04 = localgoogle_drive.ggdrive_fileid(html_doc,xpath_url_file04)

    list_xlsfile, excel_file01 = localgoogle_drive.check_xlsfile_MHunterblog_logfolder(service,fileid_file01,dirnamelog)#"循環投資追蹤股"
    list_xlsfile, excel_file02 = localgoogle_drive.check_xlsfile_MHunterblog_logfolder(service,fileid_file02,dirnamelog)#"波段投機追蹤股"
    list_xlsfile, excel_file03 = localgoogle_drive.check_xlsfile_MHunterblog_logfolder(service,fileid_file03,dirnamelog)#"景氣循環追蹤股"
    list_xlsfile, excel_file04 = localgoogle_drive.check_xlsfile_MHunterblog_logfolder(service,fileid_file04,dirnamelog)#"公用事業追蹤股"
    excel_file05 = localReadConfig.get_SeymourExcel("excelfile05") #"追蹤股_增加遞補"2018/11/10

    #"循環投資追蹤股" #"波段投機追蹤股" #"景氣循環追蹤股" #"公用事業追蹤股"#"追蹤股_增加遞補"
    #list_excel_file = [excel_file01,excel_file02,excel_file03,excel_file04]

    list_excel_file = [excel_file01,excel_file02,excel_file03,excel_file04,excel_file05]
    
    # Test class by excelRW.py
    # read each Excel file content ot get stock idx and name
    localexcelrw = excelrw.ExcelRW()

    # get all stock's idx and name from list_excel_file
    '''
    .
    .
    ['9937.0', '全國']
    ['9940.0', '信義']
    ['9941.0', '裕融']
    ['9942.0', '茂順']
    ['9943.0', '好樂迪']
    ['4126.0', '太醫']
    356
    '''
    # list_all_stockidxname=localexcelrw.get_all_stockidxname_SeymourExcel(dirnamelog,list_excel_file)
    #for stockidxname in list_all_stockidxname:
    #    print(stockidxname)
    #print(len(list_all_stockidxname))

    #2018/10/31 remark casuse purge jpg files in def plotCandlestickandMA() 
    #Delete prvious candle stick jpg files.
    ###############################
    str_candlestick_filepath=os.path.join(dirnamelog,str_candlestick_weekly_subfolder)
    localgoogle_drive = google_drive.GoogleCloudDrive(str_candlestick_filepath)
    re_exp = r'\.jpg$'
    
    #localgoogle_drive.purgelocalfiles(re_exp)

    # Initial to sqlite database code
    path_db = os.path.join(dirnamelog,'TWTSEOTCDaily.db')

    ###############################
    # excute file1 #"循環投機追蹤股"
    ###############################
    list_excel_Seymour = [excel_file01]
    list_stkidx_call_file01 = stkidx_call_file01.split(',')
    list_stkidx_put_file01 = stkidx_put_file01.split(',')    

    debug_verbose ='OFF'

    # get all stock's idx and name from file1 #"循環投機追蹤股"
    #list_all_stockidxname=localexcelrw.get_all_stockidxname_SeymourExcel(dirnamelog,list_excel_Seymour)
    '''
    9921 巨大
    9927 泰銘
    9939 宏全
    9945 潤泰新
    '''    
    #for list_stockidxname in list_all_stockidxname:
        # 20190721 cause StkIdx:1210.0, 價值比:38.16
        #          str-->float-->int-->str; '1210.0'-->1210.0-->1210-->'1210'
        #          str(int(float(list_row_value[0])))
    #    stock_idx= str(int(float(list_stockidxname[0])))
    #    stock_name= list_stockidxname[1]
        #print(stock_idx,stock_name)
        
        # get daily trade inof rom sqilte DB
    #    local_pdSqlA = data_analysis.PandasSqliteAnalysis(stock_idx,dirnamelog,path_db,str_first_year_month_day,debug_verbose)
    stock_idx= '1788'
    local_pdSqlA = data_analysis.PandasSqliteAnalysis(stock_idx,dirnamelog,path_db,str_first_year_month_day,debug_verbose)
    
    '''
              date    open    high     low   close stkidx CmpName
    241 2018-10-01  100.50  100.50   99.90  100.00   1788      杏昌
    242 2018-10-02  100.00  100.00  100.00  100.00   1788      杏昌
    243 2018-10-03  100.50  100.50   99.90   99.90   1788      杏昌
    ..         ...     ...     ...     ...     ...    ...     ...
    479 2019-10-01  104.00  104.00  102.50  103.00   1788      杏昌
    480 2019-10-02  104.00  104.00  103.00  103.50   1788      杏昌

    [240 rows x 7 columns]
    '''    
    # How to get the last N rows of a pandas DataFrame?
    # https://stackoverflow.com/questions/14663004/how-to-get-the-last-n-rows-of-a-pandas-dataframe   
    #print(local_pdSqlA.df.iloc[-240:])
    '''    
              date   close
    241 2018-10-01  100.00
    242 2018-10-02  100.00
    ..         ...     ...
    479 2019-10-01  103.00
    480 2019-10-02  103.50

    [240 rows x 2 columns]    
    '''    
    #print(local_pdSqlA.df[['date','close']].iloc[-240:])
    item = local_pdSqlA.df[['date','close']].copy()

    # Calculate 30 Day Moving Average, Std Deviation, Upper Band and Lower Band
    item['30Days_MA'] = item['close'].rolling(window=20).mean()
    
    # set .std(ddof=0) for population std instead of sample
    item['30Days_STD'] = item['close'].rolling(window=20).std() 
    
    item['Upper_Band'] = item['30Days_MA'] + (item['30Days_STD'] * 2)
    item['Lower_Band'] = item['30Days_MA'] - (item['30Days_STD'] * 2)

    '''    
              date   close  30Days_MA  30Days-STD  Upper_Band  Lower_Band
    241 2018-10-01  100.00     99.700    0.284697  100.269395   99.130605
    242 2018-10-02  100.00     99.720    0.291277  100.302553   99.137447
    ..         ...     ...        ...         ...         ...         ...
    479 2019-10-01  103.00    102.850    0.587143  104.024286  101.675714
    480 2019-10-02  103.50    102.875    0.604261  104.083522  101.666478

    [240 rows x 6 columns]    
    '''    
    #print(item.iloc[-240:])
    item = item.iloc[-100:].copy()

    # Simple 30 Day Bollinger Band 
    # set style, empty figure and axes
    plt.style.use('fivethirtyeight')
    #fig = plt.figure(figsize=(12,6))
    f1, ax = plt.subplots(figsize = (12,6))

    # Get index values for the X axis for facebook DataFrame
    x_axis = item.index.get_level_values(0)
    print(x_axis)
    
    # Plot Adjust Closing Price and Moving Averages
    ax.plot(x_axis, item['close'], color='blue', label = 'Close')
    ax.plot(x_axis, item['30Days_MA'], color='black', lw=2)
    
    # Plot shaded 21 Day Bollinger Band for Facebook
    #ax.fill_between(item['date'], item['Upper_Band'], item['Lower_Band'], color='grey')

    #plt.grid(True)
    plt.title(stock_idx)
    ax.yaxis.grid(True)
    plt.legend(loc='best')

    ax.xaxis_date()
    ax.autoscale_view()
    ax.grid()
    plt.show()

    '''    
    f1, ax = plt.subplots(figsize = (12,6))
    
    # Plotting Close 
    ax.plot(local_pdSqlA.df.iloc[-240:]['date'], local_pdSqlA.df.iloc[-240:]['close'], color = list_color_ma[0], label = 'Close')
    ax.set_xlabel('date')
    ax.set_ylabel('close price')
    
    #plt.grid(True)
    plt.title(stock_idx)
    ax.yaxis.grid(True)
    plt.legend(loc='best')

    ax.xaxis_date()
    ax.autoscale_view()
    ax.grid()
    plt.show()
    '''        



