#!/usr/bin/env python3

import os,time,sys
import pandas as pd
import numpy as np
import re
import csv
from shutil import copyfile

from logger import logger

class PandasDataAnalysis:
    def __init__(self,dirnamelog,dirname_3questlog,list_3questFolder_CsvFiles,opt_verbose='OFF'):
        
        self.dirnamelog = dirnamelog
        self.dirname_3questlog = dirname_3questlog
        self.list_3questfolder_csvfiles = list_3questFolder_CsvFiles
        self.opt_verbose = opt_verbose

    def read_CSVFile_02(self):

        re_exp_zipfolder = r'\/$'    
        re_exp_txtfile = r'\.txt$'
        re_exp_csvfile = r'\\[a-z][a-z][a-z][a-z][a-z][a-z].csv$';#..\logs\boommic_SWout\dut.3quest\Results\output.csv

        for _3questfolder_csvfiles in self.list_3questfolder_csvfiles:            

            if re.search(re_exp_csvfile, _3questfolder_csvfiles):#check if csv or txt file
                self._3questfolder_csvfiles = _3questfolder_csvfiles            

                '''
                _3questfolder_csvfiles:..\logs\boommic_SWout\dut.3quest\Results\output.csv                
                '''
                if self.opt_verbose.lower() == "on":
                    msg = "_3questfolder_csvfiles:{}"
                    logger.info(msg.format(_3questfolder_csvfiles))

                df_csv_3questfile = pd.read_csv(self._3questfolder_csvfiles, sep='\n',
                                            header = None, 
                                            delimiter=','
                                )
                df = df_csv_3questfile.copy()
                self.df = df    

                '''
                INFO: df_csv_3questfile:                                                   
                                                                  0          1          2          3          4          5   ...        45         46        47        48        49         50
                0                                                                                                            ...     nobgn      nobgn       AVG       AVG       AVG        AVG
                1                                               Type         xx         xx         xx         xx         xx  ...      GMOS  delta_SNR      SMOS      NMOS      GMOS  delta_SNR
                2  /home/philip.shen/3Quest/LuxShare/0623/Boommic...  -1.000000  -1.000000  -1.000000  -1.000000  -1.000000  ...  3.938181  10.014188  3.358136  4.220144  3.328679  24.638061

                [3 rows x 51 columns]
                '''
                '''
                INFO: df.columns: Int64Index([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
                                                17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                                                34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                                                50],
                                    dtype='int64')
                '''                
                '''                
                INFO: self.df[[7]]:          7
                            0       pub
                            1      SMOS
                            2  2.840550
                '''                
                if self.opt_verbose.lower() == "on":
                    msg = "df_csv_3questfile: {}"
                    logger.info(msg.format(df_csv_3questfile))

                    msg = "df.columns: {}"
                    logger.info(msg.format(self.df.columns))

                    msg = "len of df.columns: {}"
                    logger.info(msg.format(len(self.df.columns) ))

                    for columns_idx in range(7, len(self.df.columns)):
                        msg = "self.df[{}]: {}"
                        logger.info(msg.format(columns_idx, self.df[columns_idx] ))

                    msg = "self.df[[7]]:{}"
                    logger.info(msg.format(self.df[[7]] ))


    def read_CSVFile(self):

        re_exp_zipfolder = r'\/$'    
        re_exp_txtfile = r'\.txt$'
        re_exp_csvfile = r'\\[a-z][a-z][a-z][a-z][a-z][a-z].csv$';#..\logs\boommic_SWout\dut.3quest\Results\output.csv

        for _3questfolder_csvfiles in self.list_3questfolder_csvfiles:            

            if re.search(re_exp_csvfile, _3questfolder_csvfiles):#check if csv or txt file
                self._3questfolder_csvfiles = _3questfolder_csvfiles            

                '''
                _3questfolder_csvfiles:..\logs\boommic_SWout\dut.3quest\Results\output.csv                
                '''
                if self.opt_verbose.lower() == "on":
                    msg = "_3questfolder_csvfiles:{}"
                    logger.info(msg.format(_3questfolder_csvfiles))

                # get date and close from csv file
                # 3/7/2020 Error msg
                # pandas.errors.ParserError: Error tokenizing data. C error: Expected 1 fields in line 2, saw 4
                # Python Pandas Error tokenizing data 
                # https://stackoverflow.com/questions/18039057/python-pandas-error-tokenizing-data
                #
                # Pandas Skipping lines(Stop warnings from showing)
                # https://stackoverflow.com/questions/44680141/pandas-skipping-linesstop-warnings-from-showing
                               
                df_csv_3questfile = pd.read_csv(self._3questfolder_csvfiles, sep='\n',
                                            header = None, 
                                            index_col=False,
                                            error_bad_lines=False,
                                            warn_bad_lines=False                                            
                                )
                df = df_csv_3questfile.copy()
                self.df = df

                if self.opt_verbose.lower() == "on":
                    #msg = "CSV file Contents: {}"
                    #logger.info(msg.format(self.df))
                    
                    # Selecting a row of pandas series/dataframe by integer index
                    # https://stackoverflow.com/questions/16096627/selecting-a-row-of-pandas-series-dataframe-by-integer-index
                    '''
                    0   WB, run_case=132, group_num=16, sort_take_num=16
                    1     ,   ,   ,   ,   ,   ,   ,pub,pub,pub,pub,ro...
                    2  Type,xx,xx,xx,xx,xx,xx,SMOS,NMOS,GMOS,delta_SN...
                    3  /home/philip.shen/3Quest/LuxShare/Luxshare_062...
                    '''
                    
                    msg = "df_csv_3questfile: {}"
                    #logger.info(msg.format(df_csv_3questfile))
                    
                    '''                    
                     ❖ 資料選擇與篩選
                        可以透過下列方法選擇元素

                        中括號 [] 選擇元素
                        . 將變數當作屬性選擇
                        .loc .iloc 方法選擇
                        使用布林值篩選
                    '''
                    # Pandas 透過使用中括號 [] 與 .iloc 可以很靈活地從 data frame 中選擇想要的元素
                    # Python 在指定 0:1 時不包含 1，在指定 0:2 時不包含 2
                    #https://oranwind.org/python-pandas-ji-chu-jiao-xue/ 
                    
                    '''
                    self.df.iloc[1:4, :]:                                                    0
                    1     ,   ,   ,   ,   ,   ,   ,pub,pub,pub,pub,ro...
                    2  Type,xx,xx,xx,xx,xx,xx,SMOS,NMOS,GMOS,delta_SN...
                    3  /home/philip.shen/3Quest/LuxShare/0623/Boommic...
                    '''
                    msg = "self.df.iloc[1:4, :]: {}";#row 1~row 3：組的組名與人數  
                    self.df_3quest=self.df.iloc[1:4, :]
                    #logger.info(msg.format(self.df_3quest))

                    '''
                    df_csv_3questfile.index: RangeIndex(start=1, stop=4, step=1)
                    '''                    
                    msg = "df_csv_3questfile.index: {}"
                    self.df_3quest=self.df_3quest.index
                    #logger.info(msg.format(self.df_3quest))
                                        
                    # https://www.pythonf.cn/read/98780
                    '''
                    df_csv_3questfile.drop([0,2]):                                                    0
                    1     ,   ,   ,   ,   ,   ,   ,pub,pub,pub,pub,ro...
                    3  /home/philip.shen/3Quest/LuxShare/0623/Boommic...
                    '''
                    msg = "df_csv_3questfile.drop([0,2]): {}"
                    self.df_3quest=self.df.drop([0,2])
                    #logger.info(msg.format(self.df_3quest))                    

                    '''
                    df_csv_3questfile.drop([0,2]).columns: Int64Index([0], dtype='int64')
                    '''
                    msg = "df_3questfile.drop([0,2]).columns: {}"
                    self.df_3quest=self.df.drop([0,2]).columns
                    #logger.info(msg.format(self.df_3quest))                    

                    # Split a text column into two columns in Pandas DataFrame
                    # https://www.geeksforgeeks.org/split-a-text-column-into-two-columns-in-pandas-dataframe/

                    self.df_3quest=self.df.drop([0])
                    msg = "self.df_3quest[0]:\n{}"
                    logger.info(msg.format(self.df_3quest[0]))

                    #self.df_3quest[0].apply(lambda x: pd.Series( str(x).split(',') ))    
                    self.df_3quest[0].str.split(',', expand=True)                
                    msg = "\nSplitting column into many different columns :\n{}"
                    logger.info(msg.format(self.df_3quest))
                    
                    msg = "df_3questfile.columns: {}"
                    logger.info(msg.format(self.df_3quest.columns))                    

                    '''
                    self.df.iloc[3, 0]: 
                    /home/philip.shen/3Quest/LuxShare/0623/Boommic_SWout/dut,-1.000000,-1.000000,-1.000000,-1.000000,-1.000000,-1.000000,2.840550,4.154481,2.914813,29.453750,2.443025,4.164413,2.665425,32.881812,3.009269,4.283569,3.091669,33.826437,3.096144,4.268156,3.148156,34.712750,3.542413,4.314669,3.485562,37.809625,3.580419,4.189887,3.467494,19.377625,3.236650,4.173863,3.203125,17.238875,3.818250,4.232238,3.674519,16.904438,3.936700,4.056738,3.697850,14.161112,4.077944,4.363425,3.938181,10.014188,3.358136,4.220144,3.328679,24.638061
                    '''
                    msg = "self.df.iloc[3, 0]: {}"
                    self.df_3quest=self.df.iloc[3, 0]
                    #logger.info(msg.format(self.df_3quest))
                    

                    #df.iloc[:3, :]
                    
                    #msg = "self.df.drop[0]: {}"
                    #self.df_3quest=self.df.drop[0]
                    #logger.info(msg.format(self.df_3quest))
                    

                    # Pandas how to get a cell value and update it
                    # https://kanoki.org/2019/04/12/pandas-how-to-get-a-cell-value-and-update-it/
                    # How to get a value from a cell of a dataframe?
                    # https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
                    #msg = "Throughput Avg.(Mbps):{}, Throughput Min.(Mbps):{} ,Throughput Max.(Mbps):{}"
                    #logger.info(msg.format(self.df.iat[19,9], self.df.iat[19,10], self.df.iat[19,11]))


class CSVDataAnalysis:
    def __init__(self,dirnamelog,dirname_3questlog,list_3questFolder_CsvFiles,opt_verbose='OFF'):
        
        self.dirnamelog = dirnamelog
        self.dirname_3questlog = dirname_3questlog
        self.list_3questfolder_csvfiles = list_3questFolder_CsvFiles
        self.opt_verbose = opt_verbose
    
    def parse_CSVFile(self):
        #self.csv_dirfolderdata = '{}/{}'.format(self.dirname_ziplog,self.zipfolder_txtcsvfiles);#..\logs/202003051550/chariotlog.txt
        list_csv_foldername_filename_3quest = []

        '''
        self._3questfolder_csvfiles:..\logs\boommic_SWout\dut.3quest\Results\output.csv
        '''                    
        if self.opt_verbose.lower() == "on":
            msg = "self._3questfolder_csvfiles:{}"
            logger.info(msg.format(self._3questfolder_csvfiles))

        with open(self._3questfolder_csvfiles) as csvfile:
            #rows = csv.reader(csvfile)
            # Read CSV file line-by-line python
            # https://stackoverflow.com/questions/52937859/read-csv-file-line-by-line-python
            rows = csvfile.readlines()
            '''                    
            rows:['"WB, run_case=128, group_num=16, sort_take_num=16"\n', 
            '   ,   ,   ,   ,   ,   ,   ,pub,pub,pub,pub,road,road,road,road,crossroad,crossroad,crossroad,crossroad,train,train,train,train,car,car,car,car,cafeteria,cafeteria,cafeteria,cafeteria,mensa,mensa,mensa,mensa,callcenter,callcenter,callcenter,callcenter,voice_distractor,voice_distractor,voice_distractor,voice_distractor,nobgn,nobgn,nobgn,nobgn,AVG,AVG,AVG,AVG\n',
            'Type,xx,xx,xx,xx,xx,xx,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR,SMOS,NMOS,GMOS,delta_SNR\n', 
            '/home/philip.shen/3Quest/LuxShare/0623/Boommic_SWout/dut,-1.000000,-1.000000,-1.000000,-1.000000,-1.000000,-1.000000,2.840550,4.154481,2.914813,29.453750,2.443025,4.164413,2.665425,32.881812,3.009269,4.283569,3.091669,33.826437,3.096144,4.268156,3.148156,34.712750,3.542413,4.314669,3.485562,37.809625,3.580419,4.189887,3.467494,19.377625,3.236650,4.173863,3.203125,17.238875,3.818250,4.232238,3.674519,16.904438,3.936700,4.056738,3.697850,14.161112,4.077944,4.363425,3.938181,10.014188,3.358136,4.220144,3.328679,24.638061\n'
            ]; 
            in self._3questfolder_csvfiles:..\logs\boommic_SWout\dut.3quest\Results\output.csv
            '''
            if self.opt_verbose.lower() == "on":
                msg = "rows:{}; in self._3questfolder_csvfiles:{}"
                logger.info(msg.format(rows, self._3questfolder_csvfiles))
                #print(len(rows)) 

            # To Speed Up Search Cause line of Throughput in bottom
            # Traverse a list in reverse order in Python
            # https://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python
            #for row in reversed(rows):
            for row in rows:
                
                if ',' in row:# check rows if inculde ','
                    list_row = row.split(',')
                    '''
                    list_row:['"WB', ' run_case=128', ' group_num=16', ' sort_take_num=16"\n']
                    list_row:['   ', '   ', '   ', '   ', '   ', '   ', '   ', 'pub', 'pub', 'pub', 'pub', 'road', 'road', 'road', 'road', 'crossroad', 'crossroad', 'crossroad', 'crossroad', 'train', 'train', 'train', 'train', 'car', 'car', 'car', 'car', 'cafeteria', 'cafeteria', 'cafeteria', 'cafeteria', 'mensa', 'mensa', 'mensa', 'mensa', 'callcenter', 'callcenter', 'callcenter', 'callcenter', 'voice_distractor', 'voice_distractor', 'voice_distractor', 'voice_distractor', 'nobgn', 'nobgn', 'nobgn', 'nobgn', 'AVG', 'AVG', 'AVG', 'AVG\n']
                    list_row:['Type', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR', 'SMOS', 'NMOS', 'GMOS', 'delta_SNR\n']
                    list_row:['/home/philip.shen/3Quest/LuxShare/0623/Boommic_SWout/dut', '-1.000000', '-1.000000', '-1.000000', '-1.000000', '-1.000000', '-1.000000', '2.840550', '4.154481', '2.914813', '29.453750', '2.443025', '4.164413', '2.665425', '32.881812', '3.009269', '4.283569', '3.091669', '33.826437', '3.096144', '4.268156', '3.148156', '34.712750', '3.542413', '4.314669', '3.485562', '37.809625', '3.580419', '4.189887', '3.467494', '19.377625', '3.236650', '4.173863', '3.203125', '17.238875', '3.818250', '4.232238', '3.674519', '16.904438', '3.936700', '4.056738', '3.697850', '14.161112', '4.077944', '4.363425', '3.938181', '10.014188', '3.358136', '4.220144', '3.328679', '24.638061\n']
                    '''
                    if self.opt_verbose.lower() == "on":
                        msg = "list_row:{}"
                        logger.info(msg.format(list_row))

                    #for i,cell in enumerate(list_row):            

                    # Does Python have a string 'contains' substring method?
                    # https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
                    
    def write_CSVFile_del1strow(self):
        re_exp_csvfile = r'WB,'        
        
        '''
        WB, run_case=132, group_num=16, sort_take_num=16
        '''
        '''
        Deleting rows with Python in a CSV file        
        
        # https://stackoverflow.com/questions/29725932/deleting-rows-with-python-in-a-csv-file        
        '''
        '''
        csv.Error: iterator should return strings, not bytes
        https://stackoverflow.com/questions/8515053/csv-error-iterator-should-return-strings-not-bytes
        '''
        '''
        TypeError: a bytes-like object is required, not 'str' in python and CSV
        https://stackoverflow.com/questions/34283178/typeerror-a-bytes-like-object-is-required-not-str-in-python-and-csv
        '''
        tmp_csv = os.path.join(self.dirnamelog,'tmp.csv')
        with open(self._3questfolder_csvfiles, 'r') as inp, open(tmp_csv, 'w', newline='') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):        
                
                '''
                row in csv.reader(inp):['WB, run_case=128, group_num=16, sort_take_num=16']
                '''
                if self.opt_verbose.lower() == "on":
                    msg = "row in csv.reader(inp):{}"
                    logger.info(msg.format(row))

                '''
                How to convert list to string - Stack Overflow
                #https://stackoverflow.com/questions/5618878/how-to-convert-list-to-string
                '''                
                
                '''
                str_row:                     pubpubpubpubroadroadroadroadcrossroadcrossroadcrossroadcrossroadtraintraintraintraincarcarcarcarcafeteriacafeteriacafeteriacafeteriamensamensamensamensacallcentercallcentercallcentercallcentervoice_distractorvoice_distractorvoice_distractorvoice_distractornobgnnobgnnobgnnobgnAVGAVGAVGAVG    
                '''

                '''
                CSV in Python adding an extra carriage return, on Windows
                https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
                '''
                str_row = ''.join(row)
                if "WB," not in str_row:
                    
                    if self.opt_verbose.lower() == "on":
                        msg = "str_row:{}"
                        logger.info(msg.format(str_row))

                    writer.writerow(row)
        
        if os.path.isfile(tmp_csv):
            return tmp_csv 

    def copy_CSVFile_to3questResultPath(self,src,dst): 
        copyfile(src, dst)

    def read_CSVFile(self):

        re_exp_zipfolder = r'\/$'    
        re_exp_txtfile = r'\.txt$'
        re_exp_csvfile = r'\\[a-z][a-z][a-z][a-z][a-z][a-z].csv$';#..\logs\boommic_SWout\dut.3quest\Results\output.csv

        ret_list_csv_foldername_filename_3quest = []
        append_list_csv_foldername_filename_3quest = []

        for _3questfolder_csvfiles in self.list_3questfolder_csvfiles:
            self._3questfolder_csvfiles = _3questfolder_csvfiles            

            if re.search(re_exp_csvfile, _3questfolder_csvfiles):#check if csv file
                '''
                _3questfolder_csvfiles:..\logs\boommic_SWout\dut.3quest\Results\output.csv
                _3questfolder_csvfiles:..\logs\Intermic_SWin\dut.3quest\Results\output.csv    
                '''
                if self.opt_verbose.lower() == "on":
                    msg = "_3questfolder_csvfiles:{}"
                    logger.info(msg.format(self._3questfolder_csvfiles))

                #ret_list_csv_foldername_filename_3quest = self.parse_CSVFile()

                #append_list_csv_foldername_filename_3quest.append(ret_list_csv_foldername_filename_3quest)
        
        #self.append_list_csv_foldername_filename_3quest = \
        #    append_list_csv_foldername_filename_3quest;#asign class variable                    