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
    list_all_stockidxname=localexcelrw.get_all_stockidxname_SeymourExcel(dirnamelog,list_excel_file)
    #for stockidxname in list_all_stockidxname:
    #    print(stockidxname)
    #print(len(list_all_stockidxname))

    #2018/10/31 remark casuse purge jpg files in def plotCandlestickandMA() 
    #Delete prvious candle stick jpg files.
    ###############################
    str_candlestick_filepath=os.path.join(dirnamelog,str_candlestick_weekly_subfolder)
    localgoogle_drive = google_drive.GoogleCloudDrive(str_candlestick_filepath)
    re_exp = r'\.jpg$'
    
    localgoogle_drive.purgelocalfiles(re_exp)

    # Initial to sqlite database code
    path_db = os.path.join(dirnamelog,'TWTSEOTCDaily.db')

    ###############################
    # excute file1 #"循環投機追蹤股"
    ###############################
    list_excel_Seymour = [excel_file01]
    list_stkidx_call_file01 = stkidx_call_file01.split(',')
    list_stkidx_put_file01 = stkidx_put_file01.split(',')    

    
    



