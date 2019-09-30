# 2018/09/01 Add class PandasDataAnalysis from test_TALib.py
# 2018/09/06 Add def file1_updownrate_LastMonthYear()
#                def get_tradedays_dfinfo()
#                def file2_updownrate_QuarterYear()
#                def file3_updownrate_threeYearoneYear()
#            from test_TALib.py
# 2018/09/07 Add def plotMAchart(), def plotMA05MA20MA30() and 
#                def plotMACrossOver()   
# 2018/09/10 Add class PandasDA_Excel
# 2018/09/12 Add def MACrossOverDate_Interval_lastdate()
# 2018/09/15 Add def file1_main(), file1_call(), file1_put()
#                def file2_main(), file2_call(), file2_put()
#                def file3_main(), file3_call(), file3_put()
#                def percent2float() 
# 2018/0/917 Add def SeymourExcel01_call(),def SeymourExcel01_put()
#               def SeymourExcel02_call(),def SeymourExcel02_put() in class PandasDA_Excel 
# 2018/09/20 Add def plotCandlestickandMA() in class PandasDataAnalysis
#            Add def file_plotCandlestickMA
# 2018/09/21 Add def SeymourExcel03_call(), def SeymourExcel03_put()
#            add def compare_twoarrarys() in class PandasDA_Excel
# 2018/09/24 Add def file4_updownrate_YearQuarterMonth() in class PandasDataAnalysis
#            add file4_main(), file4_call() and file4_put()
#            Solve issue:TypeError: unsupported operand type(s) for -: 'str' and 'str'
# 2018/09/28 For uploading Google drive purpose: to creat candlestick_weeklyfolder in def plotCandlestickandMA()
# 2018/10/06 Add def buildup_output_csv
# 2018/10/27 Add class PandasSqliteAnalysis
# 2018/10/31 Add def purgelocalfiles() in def plotCandlestickandMA()   
########################################################
 
import talib
import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
# from matplotlib.finance import candlestick_ohlc
# finance module is no longer part of matplotlib
# see: https://github.com/matplotlib/mpl_finance
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.dates import num2date, DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pylab as mpl

from datetime import datetime, timedelta
import time
import os,sys, datetime
import re
import excelRW as excelrw
import googleDrive as google_drive
import sqlite3
from sqlite3 import Error

class PandasDataAnalysis:
    #2018/11/17 config font type to show TChinese
    #mpl.rcParams['font.sans-serif'] = ['SimHei'] #將預設字體改用SimHei字體for中文
        
    def __init__(self,stkidx,dirnamelog,dirdatafolder,str_first_year_month_day,opt_verbose='OFF'):
        FOLDER = dirdatafolder
        csv_datafolder = '{}/{}.csv'.format(FOLDER,stkidx)
        self.stkidx = stkidx
        self.dirnamelog = dirnamelog
        self.str_first_year_month_day = str_first_year_month_day
        self.opt_verbose = opt_verbose

        # get date, open, high, low, close price and volume from csv file
        ################## remark index_col = [0] ###############
        ## then 'date' become a column name \
        #          date    volume   open   high    low  close CmpName
        #0   2018-05-02   4715058  17.20  18.10  17.00  17.05      台航
        #1   2018-05-03    956738  16.85  16.95  16.65  16.85      台航
        #2   2018-05-04    612524  17.00  17.30  16.90  16.95      台航
        #3   2018-05-07    776401  17.15  17.25  16.70  16.75      台航

        # get date and close from csv file
        csv_stockfile = pd.read_csv(csv_datafolder, header = None, encoding = 'cp950', 
                            usecols = [0,3,4,5,6,9,10], #index_col = [0], 
                            names = ['date', 'open', 'high', 'low', 'close', 'Stkidx','CmpName'],
                            parse_dates = [0],
                            date_parser = lambda x:pd.datetime.strptime(x,'%Y/%m/%d'))
        df = csv_stockfile.copy()
        self.df = df
        #self.df.sort_index(ascending=1,inplace=True)
        # get row count after sort index
        #print("original row counts: {}".format(len(self.df.index)))

    def MACrossOver(self):
        # Get present time
        local_time = time.localtime(time.time())

        df_delduplicates = self.df.drop_duplicates()
        # get row count after delet duplicated row
        print("row counts after drop duplicated rows: {}".format(len(df_delduplicates.index)) )
        #print(df.duplicated().to_string())

        # sort pandas dataframe from one column
        df_delduplicates_sortasc = df_delduplicates.sort_values('date',ascending=1)
        # filter rows of pandas dataframe by timestamp column backward 90 days.
        df_delduplicates_back90D = df_delduplicates_sortasc.iloc[-90:,0:6]
        #print(df_delduplicates_back90D)

        # to add the calculated Moving Average as a new column to the right after 'Value'
        # to get 2 digitals after point by using np
        df_delduplicates_back90D['SMA_05'] = np.round(df_delduplicates_back90D['close'].rolling(window=5).mean(),2 )
        df_delduplicates_back90D['SMA_20'] = np.round(df_delduplicates_back90D['close'].rolling(window=20).mean(),2 )
        df_delduplicates_back90D['SMA_30'] = np.round(df_delduplicates_back90D['close'].rolling(window=30).mean(),2 )
        #print(df_delduplicates_back90D)

        # calculate SMA_05 Moving Average Crossover SMA_20
        previous_05 = df_delduplicates_back90D['SMA_05'].shift(1)
        previous_20 = df_delduplicates_back90D['SMA_20'].shift(1)
        crossing = (((df_delduplicates_back90D['SMA_05'] <= df_delduplicates_back90D['SMA_20']) & (previous_05 >= previous_20))
                    | ((df_delduplicates_back90D['SMA_05'] >= df_delduplicates_back90D['SMA_20']) & (previous_05 <= previous_20)))
        
        golden_crossing = ((df_delduplicates_back90D['SMA_05'] >= df_delduplicates_back90D['SMA_20']) 
                            & (previous_05 <= previous_20))
        dead_crossing = ((df_delduplicates_back90D['SMA_05'] <= df_delduplicates_back90D['SMA_20']) 
                            & (previous_05 >= previous_20))

        #crossing_dates = df_delduplicates_back90D.loc[crossing, 'date']
        #print(crossing_dates)
        crossing = df_delduplicates_back90D.loc[crossing]
        golden_crossing = df_delduplicates_back90D.loc[golden_crossing]
        dead_crossing = df_delduplicates_back90D.loc[dead_crossing]
        #print(crossing)
        print('MA Godlen CrossOver')
        print(golden_crossing)
        print('\n')
        print('MA Deaded CrossOver')
        print(dead_crossing)

        # Output CSV file including path
        filename_csv_macross=str(local_time.tm_mon)+str(local_time.tm_mday)+'_'+self.stkidx+'_'+"MACrossOver"+".csv"
        dirlog_csv_macross=os.path.join(self.dirnamelog,filename_csv_macross)
        golden_crossing.to_csv(dirlog_csv_macross, mode = 'w',sep=' ', header='Golden Crossing',encoding='cp950')
        dead_crossing.to_csv(dirlog_csv_macross, mode = 'a',sep=' ', header='Dead Crossing',encoding='cp950')

        # check both golden and dead MACrossOver is below 20 days
        timedelta_golden_crossing = self.MACrossOverDate_Interval_lastdate(golden_crossing)
        timedelta_dead_crossing = self.MACrossOverDate_Interval_lastdate(dead_crossing)
        if (timedelta_golden_crossing <= timedelta(days=20)).bool() | (timedelta_dead_crossing<= timedelta(days=16)).bool():
            #print('\n{} or {} <= 16 days.'.format(timedelta_golden_crossing,timedelta_dead_crossing))
            return 1
        else:
            #print('\n{} or {} > 16 days.'.format(timedelta_golden_crossing,timedelta_dead_crossing))    
            return 0

    # to calcualte interval days
    def MACrossOverDate_Interval_lastdate(self,df_macrossover):
        last_date = self.str_first_year_month_day.split(',')
        dt_last_date = datetime.datetime(int(last_date[0]), int(last_date[1]), int(last_date[2]))
        
        # get date of last row to calculate delta
        interval = dt_last_date - df_macrossover['date'].iloc[-1:]
        #if interval <= timedelta(15):
        #    print('{} from {} is {} day(s). '.format(dt_last_date.date(),i.date(),interval))
        #print('{} from {} is {} day(s). '.format(df_macrossover['date'].iloc[-1:],
        #                                        dt_last_date.date(),interval))
        return interval

    def file1_updownrate_LastMonthYear(self,valuerate):#"循環投資追蹤股"

        df_delduplicates_sortasc_tradeday = self.get_tradedays_dfinfo()
        # filter Pandas Dataframe rolling max min backward Month,Quarter,Year    
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).max()
        #df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).min()
        #df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).max()

        #calcuate raiserate_decreaserate
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_01D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['low'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['low'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_01D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['high'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['high'].astype(float) )
    
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float) )

        # 2018/08/31,0,0,---,---,---,---,---,0,4747,強生
        # 2018/09/03,0,0,---,---,---,---,---,0,4747,強生
        # 2018/09/04 last trade day maybe no trade happening, so forget assign date to index
        # Assigning an index column (and drop index column) to pandas dataframe to filter specific row
        #df_delduplicates_sortasc_tradeday_dateidx = df_delduplicates_sortasc_tradeday.set_index("date", drop = True)
        #print(df_delduplicates_sortasc_tradeday_dateidx)

        #df_delduplicates_sortasc_tradeday_dateidx_lastday = df_delduplicates_sortasc_tradeday_dateidx.loc[str_lastday,:]

        df_delduplicates_sortasc_tradeday_lastday = df_delduplicates_sortasc_tradeday.iloc[-1:,:]

        # flatten the lists then get its value like [['27.70']]-->27.7
        #list_temp = df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0]
        #print( list_temp)
        
        #list_rows_bothprices=[]
        #head_rows=["代碼","公司","市價","1Y下跌率","1M下跌率","Lastday下跌率",
                    #    "1Y上昇率","1M上昇率","Lastday上昇率",
                    #    "價格比","last trade day"]
        list_row_value_finalprice = [self.stkidx,
                                    df_delduplicates_sortasc_tradeday_lastday[['CmpName']].values.flatten()[0],
                                    df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0],
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_30D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_01D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_30D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_01D']].values.flatten()[0] *100),
                                    valuerate,
                                    df_delduplicates_sortasc_tradeday_lastday[['date']].values.flatten()[0]
                                    ]
        
        return list_row_value_finalprice
    # 2018/11/5 class GoogleSS def update_GSpreadworksheet_datafolderCSV() need
    #           nonetradeday dfinof
    def get_tradedaysANDnonetradeday_dfinfo(self):
        df_delduplicates = self.df.drop_duplicates()
        return df_delduplicates


    # delete dataframe of both duplicates and nonetradeday
    def get_tradedays_dfinfo(self):

        df_delduplicates = self.df.drop_duplicates()

        if self.opt_verbose.lower == 'on':
            # get row count after delet duplicated row
            print("row counts after drop duplicated rows: {}".format(len(df_delduplicates.index)) )

        # sort pandas dataframe from column 'date'
        df_delduplicates_sortasc = df_delduplicates.sort_values('date',ascending=1)

        # check clsoe price if includes '---' or '--' or not, but
        # 2018/09/04 dtype of close price icluding '---' and '--' is object except float64
        # convert value to string if value does have digitals
        if self.df['close'].dtype == np.object:
            # DataFrame filter close column by regex
            df_delduplicates_sortasc_nonetradeday = df_delduplicates_sortasc.loc[
                                                    df_delduplicates_sortasc['close'].str.contains(r'^-+-$')]
            if self.opt_verbose.lower == 'on':
                #print(df_delduplicates_sortasc_nonetradeday)
                print("row counts with none trade: {}".format(len(df_delduplicates_sortasc_nonetradeday)) )

            # df_delduplicates_sortasc['close'] exclude (r'^-+-$')
            df_delduplicates_sortasc_tradeday = df_delduplicates_sortasc[~df_delduplicates_sortasc['close'].str.contains(r'^-+-$')]
        elif self.df['close'].dtype == np.float64:
            df_delduplicates_sortasc_tradeday = df_delduplicates_sortasc

        if self.opt_verbose.lower == 'on':
            print("row counts with trade: {}".format(len(df_delduplicates_sortasc_tradeday)) )

        return df_delduplicates_sortasc_tradeday

    def file2_updownrate_QuarterYear(self,valuerate):#"波段投機追蹤股"

        df_delduplicates_sortasc_tradeday = self.get_tradedays_dfinfo()

        # filter Pandas Dataframe rolling max min backward Month,Quarter,Year    
        #df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).min()
        #df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).max()
        
        #calcuate raiserate_decreaserate
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_01D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['low'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['low'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_01D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['high'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['high'].astype(float) )
    
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float) )

        df_delduplicates_sortasc_tradeday_lastday = df_delduplicates_sortasc_tradeday.iloc[-1:,:]

        #list_rows_bothprices=[]
        #head_rows=["代碼","公司","市價","1Q上昇率","1Y下跌率","Lastday上昇率",
                    #    "1Q下跌率","1Y上昇率","Lastday下跌率",
                    #    "價格比","last trade day"]
        list_row_value_finalprice = [self.stkidx,
                                    df_delduplicates_sortasc_tradeday_lastday[['CmpName']].values.flatten()[0],
                                    df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0],
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_01D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_01D']].values.flatten()[0] *100),
                                    valuerate,
                                    df_delduplicates_sortasc_tradeday_lastday[['date']].values.flatten()[0]
                                    ]
        
        return list_row_value_finalprice

    def file3_updownrate_threeYearoneYear(self,pbr):#"景氣循環追蹤股"
        df_delduplicates_sortasc_tradeday = self.get_tradedays_dfinfo()

        # filter Pandas Dataframe rolling max min backward Quarter,Year, 3Year
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_730D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=730).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_730D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=730).max()

        #calcuate raiserate_decreaserate
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_730D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_730D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_730D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_730D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_730D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_730D'].astype(float) )
    
        df_delduplicates_sortasc_tradeday_lastday = df_delduplicates_sortasc_tradeday.iloc[-1:,:]

        #list_rows_bothprices=[]
        #head_rows=["代碼","公司","市價","3Y下跌率","1Y下跌率","1Q下跌率",
                    #    "3Y上昇率","1Y上昇率","1Q上昇率",
                    #    "PBR","last trade day"]
        list_row_value_finalprice = [self.stkidx,
                                    df_delduplicates_sortasc_tradeday_lastday[['CmpName']].values.flatten()[0],
                                    df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0],
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_730D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_730D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_60D']].values.flatten()[0] *100),
                                    pbr,
                                    df_delduplicates_sortasc_tradeday_lastday[['date']].values.flatten()[0]
                                    ]
        
        return list_row_value_finalprice
    
    def file4_updownrate_YearQuarterMonth(self,valuerate):#"公用事業追蹤股"

        df_delduplicates_sortasc_tradeday = self.get_tradedays_dfinfo()

        # filter Pandas Dataframe rolling max min backward Month,Quarter,Year    
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).max()

        #calcuate raiserate_decreaserate
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float) )

        df_delduplicates_sortasc_tradeday_lastday = df_delduplicates_sortasc_tradeday.iloc[-1:,:]

        #head_rows=["代碼","公司","市價","1Y下跌率(%)","1Q下跌率(%)","1M下跌率(%)",
        #            "1Y上昇率(%)","1Q上昇率(%)","1M上昇率(%)","價值比"]
        list_row_value_finalprice = [self.stkidx,
                                    df_delduplicates_sortasc_tradeday_lastday[['CmpName']].values.flatten()[0],
                                    df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0],
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_30D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_30D']].values.flatten()[0] *100),
                                    valuerate,
                                    df_delduplicates_sortasc_tradeday_lastday[['date']].values.flatten()[0]
                                    ]
        
        return list_row_value_finalprice

    def plotMAchart(self,list_ptr_df,list_label,str_title):
        plt.figure(figsize=(10,5))
        plt.plot(list_ptr_df[0], color='#DE5B49', label=list_label[0], alpha=0.8, linewidth=3)
        plt.plot(list_ptr_df[1], color='#324D5C', label=list_label[1], alpha=0.8, linewidth=3)
        plt.plot(list_ptr_df[2], color='#46B29D', label=list_label[2], alpha=0.8, linewidth=3)
        plt.legend(loc='upper left')
        plt.xlabel('date', color='c')
        plt.ylabel('value', color='c')
        plt.grid(True)
        plt.title(str_title)
        plt.tick_params(labelcolor='tab:orange')
        #plt.show()
        #可以存PNG、JPG、EPS、SVG、PGF、PDF
        #也可以選擇輸出的DPI
        plt.savefig('{}/{}.jpg'.format(self.dirnamelog,str_title), dpi=300)

    def plotMA05MA20MA30(self,data_frame,str_title):
        #在talib中，輸入輸出都需要用array，參數二則是你要選擇的n天，第三參數選擇均線的類型
        SMA_05 = talib.MA(np.array(data_frame.close), timeperiod=5, matype=0)
        SMA_20 = talib.MA(np.array(data_frame.close), timeperiod=20, matype=0)
        SMA_30 = talib.MA(np.array(data_frame.close), timeperiod=30, matype=0)

        #使用matplotlib繪圖之前先將array轉成DataFrame
        df_SMA_05 = pd.DataFrame(SMA_05, index = data_frame.index, columns = ['SMA05'])
        df_SMA_20 = pd.DataFrame(SMA_20, index = data_frame.index, columns = ['SMA20'])
        df_SMA_30 = pd.DataFrame(SMA_30, index = data_frame.index, columns = ['SMA30'])

        list_ptr_df = [df_SMA_05,df_SMA_20,df_SMA_30]
        list_label = ['SMA_05','SMA_20','SMA_30']
        self.plotMAchart(list_ptr_df,list_label,str_title)

    def plotMACrossOver(self):
        # have to sort column 'date'
        df_delduplicates_sortasc_tradeday = self.get_tradedays_dfinfo()

        #print(df_delduplicates.iloc[0,5])
        list_str = [df_delduplicates_sortasc_tradeday.iloc[0,5].astype(str) , df_delduplicates_sortasc_tradeday.iloc[0,6]]
        title = ''.join(list_str)#stkidx+CmpName

        # get last day value
        ts_endday = df_delduplicates_sortasc_tradeday[-1:].index.tolist()[0]
        # Pandas: Convert Timestamp to datetime.date
        dt_endday = pd.Timestamp(ts_endday).date()
        #print(dt_endday)

        #subtract 90 days
        dt_startdate = dt_endday - timedelta(days=90)
        print("Start Date:{} End Date:{}".format(dt_startdate,dt_endday))

        # Assigning an index column (and drop index column) to pandas dataframe to filter specific row
        # for matplotlib draw purpose
        df_delduplicates_sortasc_tradeday_dateidx = df_delduplicates_sortasc_tradeday.set_index("date", drop = True)
        #print(df_delduplicates_dateidx)

        #chose start position from startpos_idx    
        startpos_idx = -90
        #print(df_delduplicates_sortasc_tradeday_dateidx.iloc[startpos_idx:])
        self.plotMA05MA20MA30(df_delduplicates_sortasc_tradeday_dateidx.iloc[startpos_idx:], title)
    
    # plot Candlestick overlaps MA
    def plotCandlestickandMA(self,list_color_ma,str_candlestick_weeklysubfolder,str_buysell_opt = 'call'):
        # to get stock index 
        #for stkidx in df_file_stock_call[['代碼']].values.flatten():
            #print(stkidx)
            df_delduplicates_sortasc_tradeday = self.get_tradedays_dfinfo()
            #print(df_delduplicates_sortasc_tradeday)

            ##############################################################
            # Issue:
            #File "C:\ProgramData\Anaconda3\lib\site-packages\mpl_finance.py", line 288, in _candlestick
            #height = close - open
            #TypeError: unsupported operand type(s) for -: 'str' and 'str'
            ###############################################################
            # Solution: cast data to float
            df_delduplicates_sortasc_tradeday['open'] = df_delduplicates_sortasc_tradeday['open'].astype(float)
            df_delduplicates_sortasc_tradeday['high'] = df_delduplicates_sortasc_tradeday['high'].astype(float)
            df_delduplicates_sortasc_tradeday['low'] = df_delduplicates_sortasc_tradeday['low'].astype(float)
            df_delduplicates_sortasc_tradeday['close'] = df_delduplicates_sortasc_tradeday['close'].astype(float)
            
            # Converting date to pandas datetime format
            df_delduplicates_sortasc_tradeday['date'] = pd.to_datetime(df_delduplicates_sortasc_tradeday['date'])
            df_delduplicates_sortasc_tradeday['date'] = df_delduplicates_sortasc_tradeday['date'].apply(mdates.date2num)
            #print(df_delduplicates_sortasc_tradeday['date'])

            # Creating required data in new DataFrame OHLC
            df_ohlc= df_delduplicates_sortasc_tradeday[['date', 'open', 'high', 'low','close']].copy()
            
            # to add the calculated Moving Average as a new column to the right after 'Value'
            # to get 2 digitals after point by using np
            df_ohlc['SMA_05'] = np.round(df_ohlc['close'].rolling(window=5).mean(),2 )
            df_ohlc['SMA_20'] = np.round(df_ohlc['close'].rolling(window=20).mean(),2 )
            df_ohlc['SMA_30'] = np.round(df_ohlc['close'].rolling(window=30).mean(),2 )
    
            list_str = [df_delduplicates_sortasc_tradeday.iloc[-1,-2].astype(str) , 
                        df_delduplicates_sortasc_tradeday.iloc[-1,-1]]
            str_title = '_'.join(list_str)
            f1, ax = plt.subplots(figsize = (12,6))

            # In case you want to check for shorter timespan
            if len(df_ohlc) >= 180:
                df_ohlc =df_ohlc.tail(170)
            else:
                df_ohlc =df_ohlc.tail(len(df_ohlc))
        
            if self.opt_verbose.lower == 'on':
                print('Len of dataframe ohlc:{} '.format(len(df_ohlc)))
        
            # plot the candlesticks
            candlestick_ohlc(ax, df_ohlc.values, width=.6, colorup='red', colordown='green')
            #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) # e.g., 2018-09-12
            mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
            alldays = DayLocator()              # minor ticks on the days
            weekFormatter = DateFormatter('%Y-%m-%d')  # e.g., 2018-09-12; Jan 12
            #dayFormatter = DateFormatter('%d')      # e.g., 12

            ax.xaxis.set_major_locator(mondays)
            ax.xaxis.set_minor_locator(alldays)
            ax.xaxis.set_major_formatter(weekFormatter)
            #ax.xaxis.set_minor_formatter(dayFormatter)

            #plot_day_summary(ax, quotes, ticksize=3)

            # Plotting SMA columns
            ax.plot(df_ohlc['date'], df_ohlc['SMA_05'], color = list_color_ma[0], label = 'SMA05')
            ax.plot(df_ohlc['date'], df_ohlc['SMA_20'], color = list_color_ma[1], label = 'SMA20')
            ax.plot(df_ohlc['date'], df_ohlc['SMA_30'], color = list_color_ma[2], label = 'SMA30')

            #plt.grid(True)
            plt.title(str_title)
            ax.yaxis.grid(True)
            plt.legend(loc='best')

            ax.xaxis_date()
            ax.autoscale_view()
            # format the x-ticks with a human-readable date. 
            plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

            # In case you dont want to save image but just displya it
            #plt.show()

            # Check image sudfloder is existing or not
            candlestick_weeklyfolder = os.path.join(self.dirnamelog,str_candlestick_weeklysubfolder)
            if not os.path.isdir(candlestick_weeklyfolder):
                os.makedirs(candlestick_weeklyfolder) 

            # build filename of saving image
            str_stock_buysell = '_'.join([str_buysell_opt,str_title])
            #Delete prvious candle stick jpg files if exist.
            localgoogle_drive = google_drive.GoogleCloudDrive(candlestick_weeklyfolder)
            re_exp = r'{}.jpg$'.format(str_stock_buysell)
            localgoogle_drive.purgelocalfiles(re_exp)
            # Saving image    
            print('{}/{}.jpg would be saved.'.format(candlestick_weeklyfolder,str_stock_buysell))
            plt.savefig('{}/{}.jpg'.format(candlestick_weeklyfolder,str_stock_buysell), dpi=400)

class PandasSqliteAnalysis:
    def __init__(self,stkidx,dirnamelog,path_db,str_first_year_month_day,opt_verbose='OFF'):
        self.stkidx = stkidx
        self.dirnamelog = dirnamelog
        self.path_db = path_db
        self.str_first_year_month_day = str_first_year_month_day
        self.opt_verbose = opt_verbose

        # to filter clsoe price if includes '---' or '--' or not in WHERE

        # 2019/1/2 cause below case so can't filter clsoe price that includes '---' or '--'
        #"2019/01/02"	"0"	"0"	"---"	"---"	"---"	" ---"	"--- "	"0"	"5209"	"新鼎"
        
        # 2019/1/3 line 696, in file1_updownrate_LastMonthYear
        # df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).min()
        # ValueError: could not convert string to float: ' ---'
        # must filter  clsoe price if includes '---' or '--' or not in WHERE
        
        sql_query_TseOtcDaily_table = """ SELECT DISTINCT  
                                        trade_date AS date,
                                        open_price AS open,
                                        high_price AS high,
                                        low_price AS low,
                                        close_price AS close,
                                        stkidx,
                                        cmp_name AS CmpName
                                        FROM TseOtcDaily
                                        WHERE (
                                        stkidx LIKE {} AND
                                        close_price NOT LIKE '%-' 
                                        )  
                                        ORDER BY trade_date ASC; """.format(self.stkidx)

        sql_query_nonetrade_TseOtcDaily_table = """ SELECT DISTINCT  
                                        trade_date AS date,
                                        open_price AS open,
                                        high_price AS high,
                                        low_price AS low,
                                        close_price AS close,
                                        stkidx,
                                        cmp_name AS CmpName
                                        FROM TseOtcDaily
                                        WHERE (
                                        stkidx LIKE {}
                                        )  
                                        ORDER BY trade_date ASC; """.format(self.stkidx)                                
        # get date, open, high, low, close price and volume from TWTSEOTCDaily.db
        #           date    open    high     low   close stkidx cmp_name
        #235  2018/10/22   70.40   72.80   70.20   72.10   9951       皇田
        #236  2018/10/23   72.20   72.70   71.60   71.60   9951       皇田
        #237  2018/10/24   71.80   71.80   70.90   71.70   9951       皇田
        #238  2018/10/25   70.30   70.40   69.30   69.80   9951       皇田
        #239  2018/10/26   70.00   70.60   69.70   70.00   9951       皇田
        
        # create a database connection
        conn = sqlite3.connect(self.path_db)
        if conn is not None:
            # get date and close from TWTSEOTCDaily.db
            df_sql_stockfile = pd.read_sql_query(sql_query_TseOtcDaily_table, conn,
                                    parse_dates = ['date'])
            df = df_sql_stockfile.copy()
            #2019/1/3 add
            df_sql_nonetrade_stockfile = pd.read_sql_query(sql_query_nonetrade_TseOtcDaily_table, conn,
                                    parse_dates = ['date'])
            df_nonetrade = df_sql_nonetrade_stockfile.copy()

        else:
            print("Error! cannot create t he database connection.")

        self.df = df
        #2019/1/3 add
        self.df_nonetrade = df_nonetrade

        # close a database connection
        conn.close()
        
        #print(self.df)
        # get row count
        if self.opt_verbose.lower == 'on':
            #print(self.df)
            print(self.df['date'])
            print("original row counts: {}".format(len(self.df.index)))    
    
    # 2018/11/5 class GoogleSS def update_GSpreadworksheet_datafolderCSV() need
    #           nonetradeday dfinof
    def get_tradedaysANDnonetradeday_dfinfo(self):
        #2019/1/3
        df_nonetrade_delduplicates = self.df_nonetrade.drop_duplicates()
        return df_nonetrade_delduplicates

    # delete dataframe of both duplicates and nonetradeday
    # 2018/10/29 cause get_tradedays_dfinfo() can't get rid of nonetradeday
    def get_tradedays_dfinfo(self):

        df_delduplicates = self.df.drop_duplicates()

        if self.opt_verbose.lower == 'on':
            # get row count after delet duplicated row
            print("row counts after drop duplicated rows: {}".format(len(df_delduplicates.index)) )

        # sort pandas dataframe from column 'date'
        df_delduplicates_sortasc = df_delduplicates.sort_values('date',ascending=1)

        # check clsoe price if includes '---' or '--' or not, but
        # 2018/09/04 dtype of close price icluding '---' and '--' is object except float64
        # convert value to string if value does have digitals
        if self.df['close'].dtype == np.object:
            # DataFrame filter close column by regex
            df_delduplicates_sortasc_nonetradeday = df_delduplicates_sortasc.loc[
                                                    df_delduplicates_sortasc['close'].astype(str).str.contains(r'^-+-$')]
            print(df_delduplicates_sortasc_nonetradeday)
            
            if self.opt_verbose.lower == 'on':
                #print(df_delduplicates_sortasc_nonetradeday)
                print("row counts with none trade: {}".format(len(df_delduplicates_sortasc_nonetradeday)) )

            # df_delduplicates_sortasc['close'] exclude (r'^-+-$')
            df_delduplicates_sortasc_tradeday = df_delduplicates_sortasc[~df_delduplicates_sortasc['close'].str.contains(r'^-+-$')]
        elif self.df['close'].dtype == np.float64:
            df_delduplicates_sortasc_tradeday = df_delduplicates_sortasc

        if self.opt_verbose.lower == 'on':
            print("row counts with trade: {}".format(len(df_delduplicates_sortasc_tradeday)) )

        return df_delduplicates_sortasc_tradeday

    def file1_updownrate_LastMonthYear(self,valuerate):#"循環投資追蹤股"

        # get dataframe that is rid of both duplicates and nonetradeday

        # 2018/10/29 cause get_tradedays_dfinfo() can't get rid of nonetradeday
        #            update sql_query_TseOtcDaily_table in _init_() anatomy of where
        #df_delduplicates_sortasc_tradeday = self.get_tradedays_dfinfo()
        df_delduplicates_sortasc_tradeday = self.df

        # filter Pandas Dataframe rolling max min backward Month,Quarter,Year    
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).max()
        #df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).min()
        #df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).max()

        #calcuate raiserate_decreaserate
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_01D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['low'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['low'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_01D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['high'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['high'].astype(float) )
    
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float) )

        df_delduplicates_sortasc_tradeday_lastday = df_delduplicates_sortasc_tradeday.iloc[-1:,:]

        #head_rows=["代碼","公司","市價","1Y下跌率","1M下跌率","Lastday下跌率",
                    #    "1Y上昇率","1M上昇率","Lastday上昇率",
                    #    "價格比","last trade day"]
        list_row_value_finalprice = [self.stkidx,
                                    df_delduplicates_sortasc_tradeday_lastday[['CmpName']].values.flatten()[0],
                                    df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0],
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_30D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_01D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_30D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_01D']].values.flatten()[0] *100),
                                    valuerate,
                                    df_delduplicates_sortasc_tradeday_lastday[['date']].values.flatten()[0]
                                    ]
        
        if self.opt_verbose.lower == 'on':
            for row_value_finalprice in list_row_value_finalprice:
                print(row_value_finalprice)

        return list_row_value_finalprice

    def file2_updownrate_QuarterYear(self,valuerate):#"波段投機追蹤股"
        # 2018/10/29 cause get_tradedays_dfinfo() can't get rid of nonetradeday
        #            update sql_query_TseOtcDaily_table in _init_() anatomy of where    
        df_delduplicates_sortasc_tradeday = self.df

        # filter Pandas Dataframe rolling max min backward Month,Quarter,Year    
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).max()
        
        #calcuate raiserate_decreaserate
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_01D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['low'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['low'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_01D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['high'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['high'].astype(float) )
    
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float) )

        df_delduplicates_sortasc_tradeday_lastday = df_delduplicates_sortasc_tradeday.iloc[-1:,:]

        #list_rows_bothprices=[]
        #head_rows=["代碼","公司","市價","1Q上昇率","1Y下跌率","Lastday上昇率",
                    #    "1Q下跌率","1Y上昇率","Lastday下跌率",
                    #    "價格比","last trade day"]
        list_row_value_finalprice = [self.stkidx,
                                    df_delduplicates_sortasc_tradeday_lastday[['CmpName']].values.flatten()[0],
                                    df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0],
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_01D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_01D']].values.flatten()[0] *100),
                                    valuerate,
                                    df_delduplicates_sortasc_tradeday_lastday[['date']].values.flatten()[0]
                                    ]
        
        return list_row_value_finalprice

    def file3_updownrate_threeYearoneYear(self,pbr):#"景氣循環追蹤股"
        df_delduplicates_sortasc_tradeday = self.df

        # filter Pandas Dataframe rolling max min backward Quarter,Year, 3Year
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_730D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=730).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_730D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=730).max()

        #calcuate raiserate_decreaserate
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_730D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_730D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_730D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_730D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_730D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_730D'].astype(float) )
    
        df_delduplicates_sortasc_tradeday_lastday = df_delduplicates_sortasc_tradeday.iloc[-1:,:]

        #list_rows_bothprices=[]
        #head_rows=["代碼","公司","市價","3Y下跌率","1Y下跌率","1Q下跌率",
                    #    "3Y上昇率","1Y上昇率","1Q上昇率",
                    #    "PBR","last trade day"]
        list_row_value_finalprice = [self.stkidx,
                                    df_delduplicates_sortasc_tradeday_lastday[['CmpName']].values.flatten()[0],
                                    df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0],
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_730D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_730D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_60D']].values.flatten()[0] *100),
                                    pbr,
                                    df_delduplicates_sortasc_tradeday_lastday[['date']].values.flatten()[0]
                                    ]
        
        return list_row_value_finalprice

    def file4_updownrate_YearQuarterMonth(self,valuerate):#"公用事業追蹤股"
        # 2018/10/29 cause get_tradedays_dfinfo() can't get rid of nonetradeday
        #            update sql_query_TseOtcDaily_table in _init_() anatomy of where
        df_delduplicates_sortasc_tradeday = self.df

        # filter Pandas Dataframe rolling max min backward Month,Quarter,Year    
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).max()

        #calcuate raiserate_decreaserate
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float) )

        df_delduplicates_sortasc_tradeday_lastday = df_delduplicates_sortasc_tradeday.iloc[-1:,:]

        #head_rows=["代碼","公司","市價","1Y下跌率(%)","1Q下跌率(%)","1M下跌率(%)",
        #            "1Y上昇率(%)","1Q上昇率(%)","1M上昇率(%)","價值比"]
        list_row_value_finalprice = [self.stkidx,
                                    df_delduplicates_sortasc_tradeday_lastday[['CmpName']].values.flatten()[0],
                                    df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0],
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_30D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_30D']].values.flatten()[0] *100),
                                    valuerate,
                                    df_delduplicates_sortasc_tradeday_lastday[['date']].values.flatten()[0]
                                    ]
        
        return list_row_value_finalprice

    def file4_01_updownrate_YearQuarterMonth(self,valuerate,dividend):#"低波固收追蹤股"
        df_delduplicates_sortasc_tradeday = self.df

        # filter Pandas Dataframe rolling max min backward Month,Quarter,Year    
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_30D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=30).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_60D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=60).max()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_min_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).min()
        df_delduplicates_sortasc_tradeday.loc[:,'rolling_max_250D'] = df_delduplicates_sortasc_tradeday['close'].astype(float).rolling(window=250).max()

        #calcuate raiserate_decreaserate
        df_delduplicates_sortasc_tradeday.loc[:,'uprate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_30D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_30D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_30D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_60D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_60D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_60D'].astype(float) )

        df_delduplicates_sortasc_tradeday.loc[:,'uprate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_min_250D'].astype(float) )
        df_delduplicates_sortasc_tradeday.loc[:,'downrate_250D'] = ( (df_delduplicates_sortasc_tradeday['close'].astype(float)-
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float))/
                                                            df_delduplicates_sortasc_tradeday['rolling_max_250D'].astype(float) )

        #2019/02/19 add dividend_yield
        df_delduplicates_sortasc_tradeday.loc[:,'dividend_yield'] = ( dividend/df_delduplicates_sortasc_tradeday['close'].astype(float) )

        df_delduplicates_sortasc_tradeday_lastday = df_delduplicates_sortasc_tradeday.iloc[-1:,:]

        #head_rows=["代碼","公司","市價","1Y下跌率(%)","1Q下跌率(%)","1M下跌率(%)",
        #            "1Y上昇率(%)","1Q上昇率(%)","1M上昇率(%)","價值比","現金殖利率"]
        list_row_value_finalprice = [self.stkidx,
                                    df_delduplicates_sortasc_tradeday_lastday[['CmpName']].values.flatten()[0],
                                    df_delduplicates_sortasc_tradeday_lastday[['close']].values.flatten()[0],
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['downrate_30D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_250D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_60D']].values.flatten()[0] *100),
                                    "%.3f%%" %(df_delduplicates_sortasc_tradeday_lastday[['uprate_30D']].values.flatten()[0] *100),
                                    valuerate,
                                    dividend,
                                    "%.3f" %(df_delduplicates_sortasc_tradeday_lastday[['dividend_yield']].values.flatten()[0] *100),
                                    df_delduplicates_sortasc_tradeday_lastday[['date']].values.flatten()[0]
                                    ]
        
        return list_row_value_finalprice

    # plot Candlestick overlaps MA
    def plotCandlestickandMA(self,list_color_ma,str_candlestick_weeklysubfolder,str_buysell_opt = 'call'):
        
        # 2018/10/29 cause get_tradedays_dfinfo() can't get rid of nonetradeday
        #            update sql_query_TseOtcDaily_table in _init_() anatomy of where
        #df_delduplicates_sortasc_tradeday = self.get_tradedays_dfinfo()
        df_delduplicates_sortasc_tradeday = self.df

        ##############################################################
        # Issue:
        #File "C:\ProgramData\Anaconda3\lib\site-packages\mpl_finance.py", line 288, in _candlestick
        #height = close - open
        #TypeError: unsupported operand type(s) for -: 'str' and 'str'
        ###############################################################
        # Solution: cast data to float
        df_delduplicates_sortasc_tradeday['open'] = df_delduplicates_sortasc_tradeday['open'].astype(float)
        df_delduplicates_sortasc_tradeday['high'] = df_delduplicates_sortasc_tradeday['high'].astype(float)
        df_delduplicates_sortasc_tradeday['low'] = df_delduplicates_sortasc_tradeday['low'].astype(float)
        df_delduplicates_sortasc_tradeday['close'] = df_delduplicates_sortasc_tradeday['close'].astype(float)
            
        # Converting date to pandas datetime format
        df_delduplicates_sortasc_tradeday['date'] = pd.to_datetime(df_delduplicates_sortasc_tradeday['date'])
        df_delduplicates_sortasc_tradeday['date'] = df_delduplicates_sortasc_tradeday['date'].apply(mdates.date2num)
        #print(df_delduplicates_sortasc_tradeday['date'])

        # Creating required data in new DataFrame OHLC
        df_ohlc= df_delduplicates_sortasc_tradeday[['date', 'open', 'high', 'low','close']].copy()
            
        # to add the calculated Moving Average as a new column to the right after 'Value'
        # to get 2 digitals after point by using np
        df_ohlc['SMA_05'] = np.round(df_ohlc['close'].rolling(window=5).mean(),2 )
        df_ohlc['SMA_20'] = np.round(df_ohlc['close'].rolling(window=20).mean(),2 )
        df_ohlc['SMA_30'] = np.round(df_ohlc['close'].rolling(window=30).mean(),2 )

        # 2018/10/30 Error msg: line 752, in plotCandlestickandMA
        #            "list_str = [df_delduplicates_sortasc_tradeday.iloc[-1,-2].astype(str) ,
        #            AttributeError: 'str' object has no attribute 'astype'"
        #            then udate below   
        #list_str = [df_delduplicates_sortasc_tradeday.iloc[-1,-2].astype(str) , 
        list_str = [df_delduplicates_sortasc_tradeday.iloc[-1,-2], 
                    df_delduplicates_sortasc_tradeday.iloc[-1,-1]]
        str_title = '_'.join(list_str)
        f1, ax = plt.subplots(figsize = (12,6))

        # In case you want to check for shorter timespan
        if len(df_ohlc) >= 180:
            df_ohlc =df_ohlc.tail(170)
        else:
            df_ohlc =df_ohlc.tail(len(df_ohlc))
        
        if self.opt_verbose.lower == 'on':
            print('Len of dataframe ohlc:{} '.format(len(df_ohlc)))
        
        # plot the candlesticks
        candlestick_ohlc(ax, df_ohlc.values, width=.6, colorup='red', colordown='green')
        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) # e.g., 2018-09-12
        mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
        alldays = DayLocator()              # minor ticks on the days
        weekFormatter = DateFormatter('%Y-%m-%d')  # e.g., 2018-09-12; Jan 12
        #dayFormatter = DateFormatter('%d')      # e.g., 12

        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
        ax.xaxis.set_major_formatter(weekFormatter)
        
        #plot_day_summary(ax, quotes, ticksize=3)

        # Plotting SMA columns
        ax.plot(df_ohlc['date'], df_ohlc['SMA_05'], color = list_color_ma[0], label = 'SMA05')
        ax.plot(df_ohlc['date'], df_ohlc['SMA_20'], color = list_color_ma[1], label = 'SMA20')
        ax.plot(df_ohlc['date'], df_ohlc['SMA_30'], color = list_color_ma[2], label = 'SMA30')

        #plt.grid(True)
        plt.title(str_title)
        ax.yaxis.grid(True)
        plt.legend(loc='best')

        ax.xaxis_date()
        ax.autoscale_view()
        # format the x-ticks with a human-readable date. 
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

        # In case you dont want to save image but just displya it
        #plt.show()

        # Check image sudfloder is existing or not
        candlestick_weeklyfolder = os.path.join(self.dirnamelog,str_candlestick_weeklysubfolder)
        if not os.path.isdir(candlestick_weeklyfolder):
            os.makedirs(candlestick_weeklyfolder) 

        # build filename of saving image
        str_stock_buysell = '_'.join([str_buysell_opt,str_title])
        #Delete prvious candle stick jpg files if exist.
        localgoogle_drive = google_drive.GoogleCloudDrive(candlestick_weeklyfolder)
        re_exp = r'{}.jpg$'.format(str_stock_buysell)
        localgoogle_drive.purgelocalfiles(re_exp)
        # Saving image    
        print('{}/{}.jpg would be saved.'.format(candlestick_weeklyfolder,str_stock_buysell))
        plt.savefig('{}/{}.jpg'.format(candlestick_weeklyfolder,str_stock_buysell), dpi=400)    


class PandasDA_Excel:
    def __init__(self,dirnamelog,list_xlsfile):

        self.list_xlsfile = list_xlsfile
        self.dirnamelog = dirnamelog

    def diff_twodataframes(self):
        xls01_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[0])
        xls02_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[1])

        # get stkidx and CmpName from excel file
        xls01_Seymour = pd.read_excel(xls01_logfolder, encoding = 'cp950',
                            usecols = [1,2])
        
        df01 = xls01_Seymour.copy()
        
        # 2018/12/30 add exception handle
        try:
            xls02_Seymour = pd.read_excel(xls02_logfolder, encoding = 'cp950',
                            usecols = [1,2])
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            return

        df02 = xls02_Seymour.copy()
        
        #print(df)

        # get row count after sort index
        print("Lastest file row counts of {}: {}".format(self.list_xlsfile[0],len(df01.index)))
        print("Previous file row counts of {}: {}".format(self.list_xlsfile[1],len(df02.index)))

        pd_diff = pd.concat([df01,df02]).drop_duplicates(keep=False)
        print(pd_diff)
    
    def SeymourExce_filterbystockidx(self,list_stkidx,df_forfilter):
        
        # header of dataframe "代碼     名稱     價值比  一年回跌率   季漲升率  一個月漲升率"
        #Select rows whose column value is in a list:
        df_filterbystockidx = df_forfilter.loc[df_forfilter['代碼'].isin(list_stkidx)]
        print(df_filterbystockidx)

        return df_filterbystockidx
    
    def SeymourExcel01_call(self):
        xls01_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[0])
        
        # get "代碼	名稱 價值比 一年回跌率 季回跌率 一個月回跌率" from excel file
        df_xls = pd.read_excel(xls01_logfolder, encoding = 'cp950',
                             usecols = [1,2,10,19,20,21])    
        #print(df_xls)
        return df_xls
    
    def SeymourExcel01_put(self):
        xls01_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[0])
        
        # get "代碼	名稱 價值比 一年漲升率 季漲升率 一個月漲升率" from excel file
        df_xls = pd.read_excel(xls01_logfolder, encoding = 'cp950',
                             usecols = [1,2,10,23,24,25])    
        #print(df_xls)
        return df_xls

    def SeymourExcel02_call(self):
        xls01_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[0])
        
        # get "代碼	名稱 價值比 一年回跌率 季漲升率 一個月漲升率" from excel file
        df_xls = pd.read_excel(xls01_logfolder, encoding = 'cp950',
                             usecols = [1,2,10,19,24,25])    
        #print(df_xls)
        return df_xls 
    
    def SeymourExcel02_put(self):
        xls01_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[0])
        
        # get "代碼	名稱 價值比 季回跌率 一年漲升率 一個月漲升率" from excel file
        df_xls = pd.read_excel(xls01_logfolder, encoding = 'cp950',
                             usecols = [1,2,10,20,23,25])    
        #print(df_xls)
        return df_xls

    def SeymourExcel03_call(self):
        xls01_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[0])
        
        # get "代碼	名稱 PBR 三年回跌率 一年回跌率 季回跌率 一個月回跌率" from excel file
        df_xls = pd.read_excel(xls01_logfolder, encoding = 'cp950',
                             usecols = [1,2,4,18,19,20,21])    
        #print(df_xls)
        return df_xls

    def SeymourExcel03_put(self):
        xls01_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[0])
        
        # get "代碼	名稱 PBR 三年漲升率 一年漲升率 季漲升率 一個月漲升率" from excel file
        df_xls = pd.read_excel(xls01_logfolder, encoding = 'cp950',
                             usecols = [1,2,4,22,23,24,25])    
        #print(df_xls)
        return df_xls

    def SeymourExcel04_call(self):
        xls01_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[0])
        
        # get "代碼	名稱 價值比 一年回跌率 季回跌率 一個月回跌率" from excel file
        df_xls = pd.read_excel(xls01_logfolder, encoding = 'cp950',
                             usecols = [1,2,10,19,20,21])    
        #print(df_xls)
        return df_xls

    def SeymourExcel04_put(self):
        xls01_logfolder = '{}/{}'.format(self.dirnamelog,self.list_xlsfile[0])
        
        # get "代碼	名稱 價值比  一年漲升率 季漲升率 一個月漲升率" from excel file
        df_xls = pd.read_excel(xls01_logfolder, encoding = 'cp950',
                             usecols = [1,2,10,23,24,25])    
        #print(df_xls)
        return df_xls

    def compare_twoarrarys(self,df_base,df_comp):
        #cause different column indexs so flatten dataframe
        arr_stkidx_df_base = df_base[['名稱']].values#.flatten()
        arr_stkidx_df_comp = df_comp[['公司']].values#.flatten()
        #comparsion between two arrarys
        arr_diff = np.setdiff1d(arr_stkidx_df_base,arr_stkidx_df_comp)
        #print(arr_diff)
        #to get stock index by diff df_base btw df_file03_stock_call
        df_base_diff = df_base.loc[df_base['名稱'].isin(arr_diff)]
        #print(df_base_diff)

        return df_base_diff

# filter orinigal Seymour's Excel '波段投機追蹤股 - 20180928.xls'
#####################################################################
def buildup_output_csv(excel_Seymour,str_addition="bothprices"):
    filename_csv_bothprices = ''.join([datetime.date.today().strftime('%m%d'),\
                                   excel_Seymour.split(' ')[0],str_addition,".csv"])
    #print(filename_csv_bothprices)
    return filename_csv_bothprices

def file1_main(list_excel_Seymour,dirnamelog,dirdatafolder,str_first_year_month_day):#"循環投資追蹤股"
    # Get present time
    #local_time = time.localtime(time.time())

    localexcelrw = excelrw.ExcelRW()

    for excel_Seymour in list_excel_Seymour:
        print('將讀取Excel file:', excel_Seymour, '的資料')

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excel_Seymour)
        # Read values of each row
        list_row_value_price=localexcelrw.readExcel(dirlog_ExcelFile)

        # Output CSV file including path
        #filename_csv_bothprices=str(local_time.tm_mon)+str(local_time.tm_mday)+excel_Seymour[8:14]+"bothprices"+".csv"
        #filename_csv_belowprice=str(local_time.tm_mon)+str(local_time.tm_mday)+excel_Seymour[8:14]+"belowprice"+".csv"
        filename_csv_bothprices=buildup_output_csv(excel_Seymour,"bothprices")
        dirlog_csv_bothprices=os.path.join(dirnamelog,filename_csv_bothprices)
        #dirlog_csv_belowprice=os.path.join(dirnamelog,filename_csv_belowprice)

        # Declare output contents
        list_rows_bothprices=[]
        list_rows_belowprice=[]
        head_rows=["代碼","公司","市價","1Y下跌率(%)","1M下跌率(%)","Lastday下跌率(%)",
                    "1Y上昇率(%)","1M上昇率(%)","Lastday上昇率(%)","價值比"]
        list_rows_bothprices.append(head_rows)
        list_rows_belowprice.append(head_rows)

        dict_rows = {}
        # get  all CSV files name under data folder
        for list_row_value in list_row_value_price:
            # get key=idx value=價值比 to store in dict
            dict_rows[list_row_value[0]] = list_row_value[2]

        list_temp2 =[]#to store return list
        # by key=idx value=價值比
        for key,value in dict_rows.items():
            print("\nStkIdx:{}, 價值比:{}".format(key,value))
            local_pdDA = PandasDataAnalysis(key,dirnamelog,dirdatafolder,str_first_year_month_day)
            list_temp = local_pdDA.file1_updownrate_LastMonthYear(value)
            list_temp2.append(list_temp)
            #print(list_temp2)

        list_rows_bothprices.extend(list_temp2)

        #print(list_rows_bothprices)
        print("Output file(s): {}".format(dirlog_csv_bothprices))
        # Output results to CSV files
        localexcelrw.writeCSVbyTable(dirlog_csv_bothprices,list_rows_bothprices)      

    
    return dirlog_csv_bothprices

def file1_main_fromsqlite(list_excel_Seymour,dirnamelog,path_db,str_first_year_month_day,opt_verbose='OFF'):#"循環投資追蹤股"
    
    localexcelrw = excelrw.ExcelRW()

    for excel_Seymour in list_excel_Seymour:
        print('將讀取Excel file:', excel_Seymour, '的資料')

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excel_Seymour)
        # Read values of each row
        list_row_value_price=localexcelrw.readExcel(dirlog_ExcelFile)

        # Output CSV file including path
        filename_csv_bothprices=buildup_output_csv(excel_Seymour,"bothprices")
        dirlog_csv_bothprices=os.path.join(dirnamelog,filename_csv_bothprices)
        
        # Declare output contents
        list_rows_bothprices=[]
        list_rows_belowprice=[]
        head_rows=["代碼","公司","市價","1Y下跌率(%)","1M下跌率(%)","Lastday下跌率(%)",
                    "1Y上昇率(%)","1M上昇率(%)","Lastday上昇率(%)","價值比"]
        list_rows_bothprices.append(head_rows)
        list_rows_belowprice.append(head_rows)

        dict_rows = {}
        # get  all CSV files name under data folder
        # 20190721 cause StkIdx:1210.0, 價值比:38.16
        #          str-->float-->int-->str; '1210.0'-->1210.0-->1210-->'1210'
        #          str(int(float(list_row_value[0])))  
        for list_row_value in list_row_value_price:
            # get key=idx value=價值比 to store in dict
            # 20190721 cause StkIdx:1210.0, 價值比:38.16
            #dict_rows[list_row_value[0]] = list_row_value[2]
            dict_rows[str(int(float(list_row_value[0])))] = list_row_value[2]

        list_temp2 =[]#to store return list
        # by key=idx value=價值比
        for key,value in dict_rows.items():
            print("\nStkIdx:{}, 價值比:{}".format(key,value))
            # get daily trade inof rom sqilte DB
            local_pdSqlA = PandasSqliteAnalysis(key,dirnamelog,path_db,str_first_year_month_day,opt_verbose)
            list_temp = local_pdSqlA.file1_updownrate_LastMonthYear(value)
            list_temp2.append(list_temp)
            #print(list_temp2)

        list_rows_bothprices.extend(list_temp2)

        if opt_verbose.lower == 'on':
            print(list_rows_bothprices)

        print("Output file(s): {}".format(dirlog_csv_bothprices))
        # Output results to CSV files
        localexcelrw.writeCSVbyTable(dirlog_csv_bothprices,list_rows_bothprices)      
    
    return dirlog_csv_bothprices

# custom function taken from https://stackoverflow.com/questions/12432663/what-is-a-clean-way-to-convert-a-string-percent-to-a-float
def percent2float(x):
    return float(x.strip('%'))/100

# sorting stock to buy
def file1_call(str_dirlogcsv):#"循環投資追蹤股"
    
    # read daily csv file of 循環投資追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,3,4,5,9,10],
                        converters={'1Y下跌率(%)':percent2float,
                                    '1M下跌率(%)':percent2float,
                                    'Lastday下跌率(%)':percent2float} )#sep=',',
    
    # sort by below citeria
    df_csv_call = df_csv.sort_values(['1Y下跌率(%)','1M下跌率(%)','Lastday下跌率(%)','價值比'], ascending=[True, True, False, True])
    #df_csv_call = df_csv.sort_values(['1Y下跌率','1M下跌率','Lastday下跌率'], ascending=[False, False, False])
    #print(df_csv_call)

    # convert float to percentage
    df_csv_call['1Y下跌率(%)'] = df_csv_call[['1Y下跌率(%)']].values *100
    df_csv_call['1M下跌率(%)'] = df_csv_call[['1M下跌率(%)']].values *100
    df_csv_call['Lastday下跌率(%)'] = df_csv_call[['Lastday下跌率(%)']].values *100
    #print("%.3f%%" %(df_csv_call[['1Y下跌率']].values*100))
    #print(df_csv_call)

    #1. 技術滿足
    #   1. 一年回跌率 < -25%
    #   2. 一個月回跌率 < -10%
    #   3. 當日跌幅超過 2%
    #   4. 大盤季線下彎
    #   5. 價值比大於 60
    #2018/09/17 base from Seymour's Email adjust:
    #           1. 一年回跌率 < -30%
    #           2. 一個月回跌率 < -15%
    #           3. 當日跌幅超過 3%
    df_csv_call_stock=df_csv_call.loc[(df_csv_call['1Y下跌率(%)'] < -30) & 
                                      (df_csv_call['1M下跌率(%)'] < -15) ]#& 
    #                                  (df_csv_call['Lastday下跌率(%)'] < -3)]
    print('Stock to buy by {}'.format(str_dirlogcsv))
    print(df_csv_call_stock)

    # output *_buy.csv
    str_dirlogcsv_buy = re.sub(r"bothprices", "_buyranking", str_dirlogcsv)
    #str_dirlogcsv_buy = re.search(r"both+?", str_dirlogcsv)
    df_csv_call.to_csv(str_dirlogcsv_buy, encoding = 'cp950')

    str_dirlogcsv_buy_stock = re.sub(r"bothprices", "_buystock", str_dirlogcsv)
    df_csv_call_stock.to_csv(str_dirlogcsv_buy_stock, encoding = 'cp950')

    return df_csv_call_stock


# sorting stock to to sell
def file1_put(str_dirlogcsv):#"循環投資追蹤股"
    # read daily csv file of 循環投資追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,6,7,8,9,10],
                        converters={'1Y上昇率(%)':percent2float,
                                    '1M上昇率(%)':percent2float,
                                    'Lastday上昇率(%)':percent2float} )#sep=',',

    # sort by below citeria
    df_csv_put = df_csv.sort_values(['1Y上昇率(%)','1M上昇率(%)','Lastday上昇率(%)'], ascending=[False, False, False])

    # convert float to percentage
    df_csv_put['1Y上昇率(%)'] = df_csv_put[['1Y上昇率(%)']].values *100
    df_csv_put['1M上昇率(%)'] = df_csv_put[['1M上昇率(%)']].values *100
    df_csv_put['Lastday上昇率(%)'] = df_csv_put[['Lastday上昇率(%)']].values *100

    #1. 技術滿足
    #     1.1. 一年漲升率 > 35%
    #     1.2. 一個月漲升率 > 10%
    #     1.3. 當日漲幅超過 2%
    #     1.4. 大盤季線上彎
    df_csv_put_stock=df_csv_put.loc[(df_csv_put['1Y上昇率(%)'] > 35) & 
                                      (df_csv_put['1M上昇率(%)'] > 10) & 
                                      (df_csv_put['Lastday上昇率(%)'] > 2)]
    print('\nStock to sell by {}'.format(str_dirlogcsv))
    print(df_csv_put_stock)

    # output *_buy.csv
    str_dirlogcsv_sell = re.sub(r"bothprices", "_sellranking", str_dirlogcsv)
    #str_dirlogcsv_buy = re.search(r"both+?", str_dirlogcsv)
    df_csv_put.to_csv(str_dirlogcsv_sell, encoding = 'cp950')

    str_dirlogcsv_sell_stock = re.sub(r"bothprices", "_sellstock", str_dirlogcsv)
    df_csv_put_stock.to_csv(str_dirlogcsv_sell_stock, encoding = 'cp950')

    return df_csv_put_stock


def file2_main(list_excel_Seymour,dirnamelog,dirdatafolder,str_first_year_month_day):#"波段投機追蹤股"
    # Get present time
    #local_time = time.localtime(time.time())

    localexcelrw = excelrw.ExcelRW()

    for excel_Seymour in list_excel_Seymour:
        print('將讀取Excel file:', excel_Seymour, '的資料')

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excel_Seymour)
        # Read values of each row
        list_row_value_price=localexcelrw.readExcel(dirlog_ExcelFile)

        # Output CSV file including path
        #filename_csv_bothprices=str(local_time.tm_mon)+str(local_time.tm_mday)+excel_Seymour[8:14]+"bothprices"+".csv"
        #filename_csv_belowprice=str(local_time.tm_mon)+str(local_time.tm_mday)+excel_Seymour[8:14]+"belowprice"+".csv"
        filename_csv_bothprices=buildup_output_csv(excel_Seymour,'bothprices')
        dirlog_csv_bothprices=os.path.join(dirnamelog,filename_csv_bothprices)
        #dirlog_csv_belowprice=os.path.join(dirnamelog,filename_csv_belowprice)

        # Declare output contents
        list_rows_bothprices=[]
        list_rows_belowprice=[]
        head_rows=["代碼","公司","市價","1Q上昇率(%)","1Y下跌率(%)","Lastday上昇率(%)",
                    "1Q下跌率(%)","1Y上昇率(%)","Lastday下跌率(%)","價值比"]
        list_rows_bothprices.append(head_rows)
        list_rows_belowprice.append(head_rows)

        dict_rows = {}
        # get  all CSV files name under data folder
        for list_row_value in list_row_value_price:
            # get key=idx value=價值比 to store in dict
            dict_rows[list_row_value[0]] = list_row_value[2]
                
        list_temp2 =[]#to store return list
        # by key=idx value=價值比
        for key,value in dict_rows.items():
            print("\nStkIdx:{}, 價值比:{}".format(key,value))
            local_pdDA = PandasDataAnalysis(key,dirnamelog,dirdatafolder,str_first_year_month_day)
            list_temp = local_pdDA.file2_updownrate_QuarterYear(value)
            list_temp2.append(list_temp)
            #print(list_temp2)

        list_rows_bothprices.extend(list_temp2)

        #print(list_rows_bothprices)
        print("Output file(s): {}".format(dirlog_csv_bothprices))
        # Output results to CSV files
        localexcelrw.writeCSVbyTable(dirlog_csv_bothprices,list_rows_bothprices)
    
    return dirlog_csv_bothprices    

def file2_main_fromsqlite(list_excel_Seymour,dirnamelog,path_db,str_first_year_month_day,opt_verbose='OFF'):#"波段投機追蹤股"
    localexcelrw = excelrw.ExcelRW()

    for excel_Seymour in list_excel_Seymour:
        print('將讀取Excel file:', excel_Seymour, '的資料')

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excel_Seymour)
        # Read values of each row
        list_row_value_price=localexcelrw.readExcel(dirlog_ExcelFile)

        # Output CSV file including path
        filename_csv_bothprices=buildup_output_csv(excel_Seymour,'bothprices')
        dirlog_csv_bothprices=os.path.join(dirnamelog,filename_csv_bothprices)

        # Declare output contents
        list_rows_bothprices=[]
        list_rows_belowprice=[]
        head_rows=["代碼","公司","市價","1Q上昇率(%)","1Y下跌率(%)","Lastday上昇率(%)",
                    "1Q下跌率(%)","1Y上昇率(%)","Lastday下跌率(%)","價值比"]
        list_rows_bothprices.append(head_rows)
        list_rows_belowprice.append(head_rows)

        dict_rows = {}
        # get  all CSV files name under data folder
        # 20190721 cause StkIdx:1210.0, 價值比:38.16
        #          str-->float-->int-->str; '1210.0'-->1210.0-->1210-->'1210'
        #          str(int(float(list_row_value[0]))) 
        for list_row_value in list_row_value_price:
            # get key=idx value=價值比 to store in dict
            # 20190721 cause StkIdx:1210.0, 價值比:38.16
            #dict_rows[list_row_value[0]] = list_row_value[2]
            dict_rows[str(int(float(list_row_value[0])))] = list_row_value[2]
                
        list_temp2 =[]#to store return list
        # by key=idx value=價值比
        for key,value in dict_rows.items():
            print("\nStkIdx:{}, 價值比:{}".format(key,value))
            # get daily trade inof rom sqilte DB
            local_pdSqlA = PandasSqliteAnalysis(key,dirnamelog,path_db,str_first_year_month_day,opt_verbose)
            list_temp = local_pdSqlA.file2_updownrate_QuarterYear(value)
            list_temp2.append(list_temp)

        list_rows_bothprices.extend(list_temp2)

        #print(list_rows_bothprices)
        print("Output file(s): {}".format(dirlog_csv_bothprices))
        # Output results to CSV files
        localexcelrw.writeCSVbyTable(dirlog_csv_bothprices,list_rows_bothprices)
    
    return dirlog_csv_bothprices 

# sorting stock to buy
def file2_call(str_dirlogcsv):#"波段投機追蹤股"
    
    # read daily csv file of 波段投機追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,3,4,5,9,10],
                        converters={'1Q上昇率(%)':percent2float,
                                    '1Y下跌率(%)':percent2float,
                                    'Lastday上昇率(%)':percent2float} )#sep=',',
    # sort by below citeria
    df_csv_call = df_csv.sort_values(['1Q上昇率(%)','1Y下跌率(%)','Lastday上昇率(%)','價值比'], ascending=[False, True, False, True])

    # convert float to percentage
    df_csv_call['1Q上昇率(%)'] = df_csv_call[['1Q上昇率(%)']].values *100
    df_csv_call['1Y下跌率(%)'] = df_csv_call[['1Y下跌率(%)']].values *100
    df_csv_call['Lastday上昇率(%)'] = df_csv_call[['Lastday上昇率(%)']].values *100

    #進場訊號: 成長股回檔反轉向上
    #           1. 價值比 > 60
    #           2. 一年回跌率 < -25%
    #           3. 季漲升率突破 10%
    #2018/09/17 base from Seymour's Email adjust:
    #           1. 價值比 > 60
    #           2. 一年回跌率 < -30%
    #           3. 季漲升率突破 2%  
    df_csv_call_stock=df_csv_call.loc[(df_csv_call['1Y下跌率(%)'] < -30) & 
                                      (df_csv_call['1Q上昇率(%)'] > 2) & 
                                      (df_csv_call['價值比'] >= 60)]
    print('\nStock to buy by {}'.format(str_dirlogcsv))
    print(df_csv_call_stock)

    # output *_buy.csv
    str_dirlogcsv_buy = re.sub(r"bothprices", "_buyranking", str_dirlogcsv)
    df_csv_call.to_csv(str_dirlogcsv_buy, encoding = 'cp950')

    str_dirlogcsv_buy_stock = re.sub(r"bothprices", "_buystock", str_dirlogcsv)
    df_csv_call_stock.to_csv(str_dirlogcsv_buy_stock, encoding = 'cp950')

    return df_csv_call_stock                                 

# sorting stock to sell
def file2_put(str_dirlogcsv):#"波段投機追蹤股"
    
    # read daily csv file of 波段投機追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,6,7,8,9,10],
                        converters={'1Q下跌率(%)':percent2float,
                                    '1Y上昇率(%)':percent2float,
                                    'Lastday下跌率(%)':percent2float} )#sep=',',
    
    # sort by below citeria
    df_csv_put = df_csv.sort_values(['1Y上昇率(%)','1Q下跌率(%)','Lastday下跌率(%)'], ascending=[False, False, False])
    
    # convert float to percentage
    df_csv_put['1Y上昇率(%)'] = df_csv_put[['1Y上昇率(%)']].values *100
    df_csv_put['1Q下跌率(%)'] = df_csv_put[['1Q下跌率(%)']].values *100
    df_csv_put['Lastday下跌率(%)'] = df_csv_put[['Lastday下跌率(%)']].values *100

    #出場訊號:
    #1. 技術滿足: 高檔反轉向下
    #   1.1. 一年漲升率 > 35%
    #   1.2. 季回跌率破 -10%
     #2018/09/17 base from Seymour's Email adjust:
    #           1.1. 一年漲升率 > 40%
    #           1.2. 季回跌率破 -6%                                  
    df_csv_put_stock=df_csv_put.loc[(df_csv_put['1Y上昇率(%)'] > 40) & 
                                      (df_csv_put['1Q下跌率(%)'] > -10)]
    print('\nStock to sell by {}'.format(str_dirlogcsv))
    print(df_csv_put_stock)

    # output *_buy.csv
    str_dirlogcsv_sell = re.sub(r"bothprices", "_sellranking", str_dirlogcsv)
    df_csv_put.to_csv(str_dirlogcsv_sell, encoding = 'cp950')

    str_dirlogcsv_sell_stock = re.sub(r"bothprices", "_sellstock", str_dirlogcsv)
    df_csv_put_stock.to_csv(str_dirlogcsv_sell_stock, encoding = 'cp950')

    return df_csv_put_stock

def file3_main(list_excel_Seymour,dirnamelog,dirdatafolder,str_first_year_month_day):#"景氣循環追蹤股"
    # Get present time
    #local_time = time.localtime(time.time())

    localexcelrw = excelrw.ExcelRW()

    for excel_Seymour in list_excel_Seymour:
        print('將讀取Excel file:', excel_Seymour, '的資料')

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excel_Seymour)
        # Read values of each row
        list_row_value_price=localexcelrw.readExcel(dirlog_ExcelFile)

        # Output CSV file including path
        #filename_csv_bothprices=str(local_time.tm_mon)+str(local_time.tm_mday)+excel_Seymour[8:14]+"bothprices"+".csv"
        #filename_csv_belowprice=str(local_time.tm_mon)+str(local_time.tm_mday)+excel_Seymour[8:14]+"belowprice"+".csv"
        filename_csv_bothprices=buildup_output_csv(excel_Seymour,'bothprices')
        dirlog_csv_bothprices=os.path.join(dirnamelog,filename_csv_bothprices)
        #dirlog_csv_belowprice=os.path.join(dirnamelog,filename_csv_belowprice)

        # Declare output contents
        list_rows_bothprices=[]
        list_rows_belowprice=[]
        head_rows=["代碼","公司","市價","3Y下跌率(%)","1Y下跌率(%)","1Q下跌率(%)",
                    "3Y上昇率(%)","1Y上昇率(%)","1Q上昇率(%)","PBR"]
        list_rows_bothprices.append(head_rows)
        list_rows_belowprice.append(head_rows)

        dict_rows = {}
        # get  all CSV files name under data folder
        for list_row_value in list_row_value_price:
            # get key=idx value=PBR to store in dict
            dict_rows[list_row_value[0]] = list_row_value[3]

        list_temp2 =[]#to store return list
        # by key=idx value=PBR
        for key,value in dict_rows.items():
            print("\nStkIdx:{}, PBR:{}".format(key,value))
            local_pdDA = PandasDataAnalysis(key,dirnamelog,dirdatafolder,str_first_year_month_day)
            list_temp = local_pdDA.file3_updownrate_threeYearoneYear(value)
            list_temp2.append(list_temp)
            #print(list_temp2)    

        list_rows_bothprices.extend(list_temp2)

        #print(list_rows_bothprices)
        print("Output file(s): {}".format(dirlog_csv_bothprices))
        # Output results to CSV files
        localexcelrw.writeCSVbyTable(dirlog_csv_bothprices,list_rows_bothprices)    
    
    return dirlog_csv_bothprices

def file3_main_fromsqlite(list_excel_Seymour,dirnamelog,path_db,str_first_year_month_day,opt_verbose='OFF'):#"景氣循環追蹤股"
    
    localexcelrw = excelrw.ExcelRW()
    for excel_Seymour in list_excel_Seymour:
        print('將讀取Excel file:', excel_Seymour, '的資料')

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excel_Seymour)
        # Read values of each row
        list_row_value_price=localexcelrw.readExcel(dirlog_ExcelFile)

        # Output CSV file including path
        filename_csv_bothprices=buildup_output_csv(excel_Seymour,'bothprices')
        dirlog_csv_bothprices=os.path.join(dirnamelog,filename_csv_bothprices)
        
        # Declare output contents
        list_rows_bothprices=[]
        list_rows_belowprice=[]
        head_rows=["代碼","公司","市價","3Y下跌率(%)","1Y下跌率(%)","1Q下跌率(%)",
                    "3Y上昇率(%)","1Y上昇率(%)","1Q上昇率(%)","PBR"]
        list_rows_bothprices.append(head_rows)
        list_rows_belowprice.append(head_rows)

        dict_rows = {}
        # get  all CSV files name under data folder
        # 20190721 cause StkIdx:1210.0, 價值比:38.16
        #          str-->float-->int-->str; '1210.0'-->1210.0-->1210-->'1210'
        #          str(int(float(list_row_value[0]))) 
        for list_row_value in list_row_value_price:
            # get key=idx value=PBR to store in dict
            # 20190721 cause StkIdx:1210.0, 價值比:38.16
            #dict_rows[list_row_value[0]] = list_row_value[3]
            dict_rows[str(int(float(list_row_value[0])))] = list_row_value[3]            

        list_temp2 =[]#to store return list
        # by key=idx value=PBR
        for key,value in dict_rows.items():
            print("\nStkIdx:{}, PBR:{}".format(key,value))
            local_pdsql = PandasSqliteAnalysis(key,dirnamelog,path_db,str_first_year_month_day)
            list_temp = local_pdsql.file3_updownrate_threeYearoneYear(value)
            list_temp2.append(list_temp)
            #print(list_temp2)    

        list_rows_bothprices.extend(list_temp2)

        #print(list_rows_bothprices)
        print("Output file(s): {}".format(dirlog_csv_bothprices))
        # Output results to CSV files
        localexcelrw.writeCSVbyTable(dirlog_csv_bothprices,list_rows_bothprices)    
    
    return dirlog_csv_bothprices

# sorting stock to buy
def file3_call(str_dirlogcsv):#"景氣循環追蹤股"
    
    # read daily csv file of 景氣循環追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,3,4,5,9,10],
                        converters={'3Y下跌率(%)':percent2float,
                                    '1Y下跌率(%)':percent2float,
                                    '1Q下跌率(%)':percent2float} )#sep=',',

    # sort by below citeria
    df_csv_call = df_csv.sort_values(['3Y下跌率(%)','1Y下跌率(%)','1Q下跌率(%)','PBR'], ascending=[False, False, False, False])

    # convert float to percentage
    df_csv_call['3Y下跌率(%)'] = df_csv_call[['3Y下跌率(%)']].values *100
    df_csv_call['1Y下跌率(%)'] = df_csv_call[['1Y下跌率(%)']].values *100
    df_csv_call['1Q下跌率(%)'] = df_csv_call[['1Q下跌率(%)']].values *100

    #進場訊號: 景氣循環低點
    #         1. PBR < 1
    #         2. 三年回跌率 < -40%
    #         3. 一年回跌率 < -20%
    #         4. 5,20 日均線黃金交叉
    df_csv_call_stock=df_csv_call.loc[(df_csv_call['3Y下跌率(%)'] > -40) & 
                                      (df_csv_call['1Y下跌率(%)'] > -20) & 
                                      (df_csv_call['PBR'] <= 1)]
    print('\nStock to buy by {}'.format(str_dirlogcsv))
    print(df_csv_call_stock)

    # output *_buy.csv
    str_dirlogcsv_buy = re.sub(r"bothprices", "_buyranking", str_dirlogcsv)
    df_csv_call.to_csv(str_dirlogcsv_buy, encoding = 'cp950')

    str_dirlogcsv_buy_stock = re.sub(r"bothprices", "_buystock", str_dirlogcsv)
    df_csv_call_stock.to_csv(str_dirlogcsv_buy_stock, encoding = 'cp950') 

    return df_csv_call_stock

# sorting stock to sell
def file3_put(str_dirlogcsv):#"景氣循環追蹤股"
    
    # read daily csv file of 景氣循環追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,6,7,8,9,10],
                        converters={'3Y上昇率(%)':percent2float,
                                    '1Y上昇率(%)':percent2float,
                                    '1Q上昇率(%)':percent2float} )#sep=',',

    # sort by below citeria
    df_csv_put = df_csv.sort_values(['3Y上昇率(%)','1Y上昇率(%)','1Q上昇率(%)'], ascending=[False, False, False])

    # convert float to percentage
    df_csv_put['3Y上昇率(%)'] = df_csv_put[['3Y上昇率(%)']].values *100
    df_csv_put['1Y上昇率(%)'] = df_csv_put[['1Y上昇率(%)']].values *100
    df_csv_put['1Q上昇率(%)'] = df_csv_put[['1Q上昇率(%)']].values *100

    #出場訊號:
    #1. 技術滿足: 高檔反轉向下
    #       1.1. 三年漲升率 > 65%
    #       1.2. 一年漲升率 > 25%
    #       1.3. 5,20 日均線死亡交叉                               
    df_csv_put_stock=df_csv_put.loc[(df_csv_put['3Y上昇率(%)'] > 65) & 
                                      (df_csv_put['1Y上昇率(%)'] > 25)]
    print('\nStock to sell by {}'.format(str_dirlogcsv))
    print(df_csv_put_stock)

    # output *_buy.csv
    str_dirlogcsv_sell = re.sub(r"bothprices", "_sellranking", str_dirlogcsv)
    df_csv_put.to_csv(str_dirlogcsv_sell, encoding = 'cp950')

    str_dirlogcsv_sell_stock = re.sub(r"bothprices", "_sellstock", str_dirlogcsv)
    df_csv_put_stock.to_csv(str_dirlogcsv_sell_stock, encoding = 'cp950')

    return df_csv_put_stock

def file4_main(list_excel_Seymour,dirnamelog,dirdatafolder,str_first_year_month_day):#"公用事業追蹤股"
    # Get present time
    #local_time = time.localtime(time.time())

    localexcelrw = excelrw.ExcelRW()

    for excel_Seymour in list_excel_Seymour:
        print('將讀取Excel file:', excel_Seymour, '的資料')

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excel_Seymour)
        # Read values of each row
        list_row_value_price=localexcelrw.readExcel(dirlog_ExcelFile)

        # Output CSV file including path
        #filename_csv_bothprices=str(local_time.tm_mon)+str(local_time.tm_mday)+excel_Seymour[8:14]+"bothprices"+".csv"
        #filename_csv_belowprice=str(local_time.tm_mon)+str(local_time.tm_mday)+excel_Seymour[8:14]+"belowprice"+".csv"
        filename_csv_bothprices=buildup_output_csv(excel_Seymour,'bothprices')
        dirlog_csv_bothprices=os.path.join(dirnamelog,filename_csv_bothprices)
        #dirlog_csv_belowprice=os.path.join(dirnamelog,filename_csv_belowprice)

        # Declare output contents
        list_rows_bothprices=[]
        list_rows_belowprice=[]
        head_rows=["代碼","公司","市價","1Y下跌率(%)","1Q下跌率(%)","1M下跌率(%)",
                    "1Y上昇率(%)","1Q上昇率(%)","1M上昇率(%)","價值比"]
        list_rows_bothprices.append(head_rows)
        list_rows_belowprice.append(head_rows)

        dict_rows = {}
        # get  all CSV files name under data folder
        for list_row_value in list_row_value_price:
            # get key=idx value=價值比 to store in dict
            dict_rows[list_row_value[0]] = list_row_value[2]

        list_temp2 =[]#to store return list
        # by key=idx value=PBR
        for key,value in dict_rows.items():
            print("\nStkIdx:{}, 價值比:{}".format(key,value))
            local_pdDA = PandasDataAnalysis(key,dirnamelog,dirdatafolder,str_first_year_month_day)
            list_temp = local_pdDA.file4_updownrate_YearQuarterMonth(value)
            list_temp2.append(list_temp)
            #print(list_temp2)

        list_rows_bothprices.extend(list_temp2)

        #print(list_rows_bothprices)
        print("Output file(s): {}".format(dirlog_csv_bothprices))
        # Output results to CSV files
        localexcelrw.writeCSVbyTable(dirlog_csv_bothprices,list_rows_bothprices)
    
    return dirlog_csv_bothprices 

def file4_main_fromsqlite(list_excel_Seymour,dirnamelog,path_db,str_first_year_month_day,opt_verbose='OFF'):#"公用事業追蹤股"
    
    localexcelrw = excelrw.ExcelRW()
    for excel_Seymour in list_excel_Seymour:
        print('將讀取Excel file:', excel_Seymour, '的資料')

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excel_Seymour)
        # Read values of each row
        list_row_value_price=localexcelrw.readExcel(dirlog_ExcelFile)

        # Output CSV file including path
        filename_csv_bothprices=buildup_output_csv(excel_Seymour,'bothprices')
        dirlog_csv_bothprices=os.path.join(dirnamelog,filename_csv_bothprices)
        
        # Declare output contents
        list_rows_bothprices=[]
        list_rows_belowprice=[]
        head_rows=["代碼","公司","市價","1Y下跌率(%)","1Q下跌率(%)","1M下跌率(%)",
                    "1Y上昇率(%)","1Q上昇率(%)","1M上昇率(%)","價值比"]
        list_rows_bothprices.append(head_rows)
        list_rows_belowprice.append(head_rows)

        dict_rows = {}
        # get  all CSV files name under data folder
        # 20190721 cause StkIdx:1210.0, 價值比:38.16
        #          str-->float-->int-->str; '1210.0'-->1210.0-->1210-->'1210'
        #          str(int(float(list_row_value[0]))) 
        for list_row_value in list_row_value_price:
            # get key=idx value=價值比 to store in dict
            # 20190721 cause StkIdx:1210.0, 價值比:38.16
            #dict_rows[list_row_value[0]] = list_row_value[2]
            dict_rows[str(int(float(list_row_value[0])))] = list_row_value[2]

        list_temp2 =[]#to store return list
        # by key=idx value=PBR
        for key,value in dict_rows.items():
            print("\nStkIdx:{}, 價值比:{}".format(key,value))
            local_pdsql = PandasSqliteAnalysis(key,dirnamelog,path_db,str_first_year_month_day)
            list_temp = local_pdsql.file4_updownrate_YearQuarterMonth(value)
            list_temp2.append(list_temp)
            #print(list_temp2)
        list_rows_bothprices.extend(list_temp2)

        #print(list_rows_bothprices)
        print("Output file(s): {}".format(dirlog_csv_bothprices))
        # Output results to CSV files
        localexcelrw.writeCSVbyTable(dirlog_csv_bothprices,list_rows_bothprices)
    
    return dirlog_csv_bothprices

def file4_01_main_fromsqlite(list_excel_Seymour,dirnamelog,path_db,str_first_year_month_day,opt_verbose='OFF'):#"低波固收追蹤股"
    
    localexcelrw = excelrw.ExcelRW()
    for excel_Seymour in list_excel_Seymour:
        print('將讀取Excel file:', excel_Seymour, '的資料')

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excel_Seymour)
        # Read values of each row
        # 2019/02/19 add column '現金殖利率'
        list_row_value_price=localexcelrw.readExcel(dirlog_ExcelFile)

        # Output CSV file including path
        filename_csv_bothprices=buildup_output_csv(excel_Seymour,'bothprices')
        dirlog_csv_bothprices=os.path.join(dirnamelog,filename_csv_bothprices)
        
        # Declare output contents
        # 2019/02/19 add column '現金股利'(Dividend) '現金殖利率'(Dividend yield)
        list_rows_bothprices=[]
        list_rows_belowprice=[]
        head_rows=["代碼","公司","市價","1Y下跌率(%)","1Q下跌率(%)","1M下跌率(%)",
                    "1Y上昇率(%)","1Q上昇率(%)","1M上昇率(%)","價值比", "現金股利", "現金殖利率(%)"]
        list_rows_bothprices.append(head_rows)
        list_rows_belowprice.append(head_rows)

        list_temp2 =[]#to store return list
        # sort idx, value_ratio and dividend
        for list_row_value in list_row_value_price:
            # 20190721 cause StkIdx:1210.0, 價值比:38.16
            #          str-->float-->int-->str; '1210.0'-->1210.0-->1210-->'1210'
            #          str(int(float(list_row_value[0]))) 
            #idx = list_row_value[0]# idx
            idx = str(int(float(list_row_value[0])))
            value_ratio = list_row_value[2]# value_ratio
            dividend = list_row_value[4]# dividend

            print("\nStkIdx:{}, 價值比:{}, 現金股利:{}".format(idx,value_ratio,dividend))
            local_pdsql = PandasSqliteAnalysis(idx,dirnamelog,path_db,str_first_year_month_day)
            list_temp = local_pdsql.file4_01_updownrate_YearQuarterMonth(value_ratio,dividend)

            list_temp2.append(list_temp)

        list_rows_bothprices.extend(list_temp2)

        #print(list_rows_bothprices)
        print("Output file(s): {}".format(dirlog_csv_bothprices))
        # Output results to CSV files
        localexcelrw.writeCSVbyTable(dirlog_csv_bothprices,list_rows_bothprices)
    
    return dirlog_csv_bothprices

# sorting stock to buy
def file4_call(str_dirlogcsv):#"公用事業追蹤股"
    
    # read daily csv file of 公用事業追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,3,4,5,9,10],
                        converters={'1Y下跌率(%)':percent2float,
                                    '1Q下跌率(%)':percent2float,
                                    '1M下跌率(%)':percent2float} )#sep=',',
    # sort by below citeria
    df_csv_call = df_csv.sort_values(['1Y下跌率(%)','1Q下跌率(%)','1M下跌率(%)','價值比'], ascending=[False,  False, False, False])

    # convert float to percentage
    df_csv_call['1Y下跌率(%)'] = df_csv_call[['1Y下跌率(%)']].values *100
    df_csv_call['1Q下跌率(%)'] = df_csv_call[['1Q下跌率(%)']].values *100
    df_csv_call['1M下跌率(%)'] = df_csv_call[['1M下跌率(%)']].values *100

    #進場訊號: 成長股回檔反轉向上
    #           1. 價值比 > 80
    #           2. 5,20 日均線黃金交叉(圖形判斷)
    df_csv_call_stock=df_csv_call.loc[(df_csv_call['價值比'] >= 70)]
    print('\nStock to buy by {}'.format(str_dirlogcsv))
    print(df_csv_call_stock)

    # output *_buy.csv
    str_dirlogcsv_buy = re.sub(r"bothprices", "_buyranking", str_dirlogcsv)
    df_csv_call.to_csv(str_dirlogcsv_buy, encoding = 'cp950')

    str_dirlogcsv_buy_stock = re.sub(r"bothprices", "_buystock", str_dirlogcsv)
    df_csv_call_stock.to_csv(str_dirlogcsv_buy_stock, encoding = 'cp950')

    return df_csv_call_stock

# sorting stock to buy
def file4_01_call(str_dirlogcsv):#"低波固收追蹤股"
    
    # read daily csv file of 低波固收追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,3,4,5,9,10,11],
                        converters={'1Y下跌率(%)':percent2float,
                                    '1Q下跌率(%)':percent2float,
                                    '1M下跌率(%)':percent2float} )#sep=',',

    # sort by below citeria
    df_csv_call = df_csv.sort_values(['1Y下跌率(%)','1Q下跌率(%)','1M下跌率(%)','價值比','現金殖利率(%)'], 
                                    ascending=[False,  False, False, False, False])

    # convert float to percentage
    df_csv_call['1Y下跌率(%)'] = df_csv_call[['1Y下跌率(%)']].values *100
    df_csv_call['1Q下跌率(%)'] = df_csv_call[['1Q下跌率(%)']].values *100
    df_csv_call['1M下跌率(%)'] = df_csv_call[['1M下跌率(%)']].values *100
    '''
    進場訊號:
       1.建立基本持股: 存股
          1.1 價值比 > 60
             or
           1.2 殖利率 > 4%
       or
       2. 逢低加碼: 回檔買進. 每檔最多加碼二次. 每次加碼需間隔一個月以上. 規則是除了建立基本持股的兩項條件之一外, 
                    再加上以下幾項,.
           2.1 .  一年回跌率 < -15%
           2.2    一個月回跌率 < -6%
           2.3. 當日跌幅超過 1%
    '''
    #df_csv_call_stock=df_csv_call.loc[(df_csv_call['價值比'] >= 60)]
    df_csv_call_stock=df_csv_call.loc[(df_csv_call['現金殖利率(%)'] >= 4)]
    print('\nStock to buy by {}'.format(str_dirlogcsv))
    print(df_csv_call_stock)

    # output *_buy.csv
    str_dirlogcsv_buy = re.sub(r"bothprices", "_buyranking", str_dirlogcsv)
    df_csv_call.to_csv(str_dirlogcsv_buy, encoding = 'cp950')

    str_dirlogcsv_buy_stock = re.sub(r"bothprices", "_buystock", str_dirlogcsv)
    df_csv_call_stock.to_csv(str_dirlogcsv_buy_stock, encoding = 'cp950')

    return df_csv_call_stock                                

# sorting stock to sell
def file4_put(str_dirlogcsv):#"公用事業追蹤股"
    
    # read daily csv file of 公用事業追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,6,7,8,9,10],
                        converters={'1Y上昇率(%)':percent2float,
                                    '1Q上昇率(%)':percent2float,
                                    '1M上昇率(%)':percent2float} )#sep=',',
    # sort by below citeria
    df_csv_put = df_csv.sort_values(['1Y上昇率(%)','1Q上昇率(%)','1M上昇率(%)','價值比'], ascending=[True,  True, True, True])

    # convert float to percentage
    df_csv_put['1Y上昇率(%)'] = df_csv_put[['1Y上昇率(%)']].values *100
    df_csv_put['1Q上昇率(%)'] = df_csv_put[['1Q上昇率(%)']].values *100
    df_csv_put['1M上昇率(%)'] = df_csv_put[['1M上昇率(%)']].values *100
    
    #出場訊號:
    #1. 技術滿足: 高檔反轉向下
    #   1.1. 價值比 < 20
    #   1.2. 5,20 日均線死亡交叉(圖形判斷)
    df_csv_put_stock=df_csv_put.loc[df_csv_put['價值比'] <= 20]
    print('\nStock to sell by {}'.format(str_dirlogcsv))
    print(df_csv_put_stock)

    # output *_buy.csv
    str_dirlogcsv_sell = re.sub(r"bothprices", "_sellranking", str_dirlogcsv)
    df_csv_put.to_csv(str_dirlogcsv_sell, encoding = 'cp950')

    str_dirlogcsv_sell_stock = re.sub(r"bothprices", "_sellstock", str_dirlogcsv)
    df_csv_put_stock.to_csv(str_dirlogcsv_sell_stock, encoding = 'cp950')

    return df_csv_put_stock

# sorting stock to sell
def file4_01_put(str_dirlogcsv):#"低波固收追蹤股"
    
    # read daily csv file of 低波固收追蹤股
    # # pass to convertes param as a dict
    df_csv = pd.read_csv(str_dirlogcsv, encoding = 'cp950', engine='python',
                        #header = 0, 
                        index_col = False,
                        usecols = [0,1,2,6,7,8,9,10,11],
                        converters={'1Y上昇率(%)':percent2float,
                                    '1Q上昇率(%)':percent2float,
                                    '1M上昇率(%)':percent2float} )#sep=',',
    # sort by below citeria
    df_csv_put = df_csv.sort_values(['1Y上昇率(%)','1Q上昇率(%)','1M上昇率(%)','價值比','現金殖利率(%)'], 
                                    ascending=[True,  True, True, True, True])

    # convert float to percentage
    df_csv_put['1Y上昇率(%)'] = df_csv_put[['1Y上昇率(%)']].values *100
    df_csv_put['1Q上昇率(%)'] = df_csv_put[['1Q上昇率(%)']].values *100
    df_csv_put['1M上昇率(%)'] = df_csv_put[['1M上昇率(%)']].values *100

    '''
    出場訊號:
       1.價格遠高於價值: 沒有存股的價值
          1.1. 價值比 < 20
          1.2. 殖利率 < 3%
       or
       2. 停利
          2.1. 獲利超過 50%
    '''
    #df_csv_put_stock=df_csv_put.loc[df_csv_put['價值比'] < 20]
    df_csv_put_stock=df_csv_put.loc[df_csv_put['現金殖利率(%)'] <= 3]
    print('\nStock to sell by {}'.format(str_dirlogcsv))
    print(df_csv_put_stock)

    # output *_buy.csv
    str_dirlogcsv_sell = re.sub(r"bothprices", "_sellranking", str_dirlogcsv)
    df_csv_put.to_csv(str_dirlogcsv_sell, encoding = 'cp950')

    str_dirlogcsv_sell_stock = re.sub(r"bothprices", "_sellstock", str_dirlogcsv)
    df_csv_put_stock.to_csv(str_dirlogcsv_sell_stock, encoding = 'cp950')

    return df_csv_put_stock

# plot file01~04 candle stick and MA curve by each stock index
def file_plotCandlestickMA(df_file_stock_call,dirnamelog,dirdatafolder,str_first_year_month_day,
                            list_color_ma, str_candlestick_weeklysubfolder,str_buysell_opt):
    # to get stock index then plot Candlestick and MA cruve
    for stkidx in df_file_stock_call[['代碼']].values.flatten():
        localdata_analysis = PandasDataAnalysis(stkidx,dirnamelog,dirdatafolder,str_first_year_month_day)
        localdata_analysis.plotCandlestickandMA(list_color_ma,str_candlestick_weeklysubfolder,str_buysell_opt)

def file_plotCandlestickMA_fromsqlite(df_file_stock_call,dirnamelog,path_db,str_first_year_month_day,
                                        list_color_ma, str_candlestick_weeklysubfolder,str_buysell_opt):
    # to get stock index then plot Candlestick and MA cruve
    for stkidx in df_file_stock_call[['代碼']].values.flatten():
        localsql_analysis = PandasSqliteAnalysis(stkidx,dirnamelog,path_db,str_first_year_month_day)
        localsql_analysis.plotCandlestickandMA(list_color_ma,str_candlestick_weeklysubfolder,str_buysell_opt)                                    