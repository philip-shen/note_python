#!/usr/bin/env python3

import os,time,sys
import pandas as pd
import numpy as np
import re
import csv

from logger import logger

class PandasDataAnalysis:
    def __init__(self,dirnamelog,dirname_3questlog,list_3questFolder_CsvFiles,opt_verbose='OFF'):
        
        self.dirnamelog = dirnamelog
        self.dirname_3questlog = dirname_3questlog
        self.list_3questfolder_csvfiles = list_3questFolder_CsvFiles
        self.opt_verbose = opt_verbose

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
                    logger.info(msg.format(df_csv_3questfile))
                    
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
                    logger.info(msg.format(self.df_3quest))

                    '''
                    df_csv_3questfile.index: RangeIndex(start=1, stop=4, step=1)
                    '''                    
                    msg = "df_csv_3questfile.index: {}"
                    self.df_3quest=self.df_3quest.index
                    logger.info(msg.format(self.df_3quest))
                    
                    '''
                    df_noindex = pd.read_csv('./data/12/sample_pandas_normal.csv')
                    print(df_noindex)
                    #       name  age state  point
                    # 0    Alice   24    NY     64
                    # 1      Bob   42    CA     92
                    # 2  Charlie   18    CA     70
                    # 3     Dave   68    TX     70
                    # 4    Ellen   24    CA     88
                    # 5    Frank   30    NY     57

                    print(df_noindex.index)
                    # RangeIndex(start=0, stop=6, step=1)

                    如果是序列号，则无论原样指定数字值还是使用index属性，结果都将相同。

                    print(df_noindex.drop([1, 3, 5]))
                    #       name  age state  point
                    # 0    Alice   24    NY     64
                    # 2  Charlie   18    CA     70
                    # 4    Ellen   24    CA     88

                    print(df_noindex.drop(df_noindex.index[[1, 3, 5]]))
                    #       name  age state  point
                    # 0    Alice   24    NY     64
                    # 2  Charlie   18    CA     70
                    # 4    Ellen   24    CA     88

                    '''
                    # https://www.pythonf.cn/read/98780
                    '''
                    df_csv_3questfile.drop([0,2]):                                                    0
                    1     ,   ,   ,   ,   ,   ,   ,pub,pub,pub,pub,ro...
                    3  /home/philip.shen/3Quest/LuxShare/0623/Boommic...
                    '''
                    msg = "df_csv_3questfile.drop([0,2]): {}"
                    self.df_3quest=self.df.drop([0,2])
                    logger.info(msg.format(self.df_3quest))                    

                    '''
                    self.df.iloc[3, 0]: 
                    /home/philip.shen/3Quest/LuxShare/0623/Boommic_SWout/dut,-1.000000,-1.000000,-1.000000,-1.000000,-1.000000,-1.000000,2.840550,4.154481,2.914813,29.453750,2.443025,4.164413,2.665425,32.881812,3.009269,4.283569,3.091669,33.826437,3.096144,4.268156,3.148156,34.712750,3.542413,4.314669,3.485562,37.809625,3.580419,4.189887,3.467494,19.377625,3.236650,4.173863,3.203125,17.238875,3.818250,4.232238,3.674519,16.904438,3.936700,4.056738,3.697850,14.161112,4.077944,4.363425,3.938181,10.014188,3.358136,4.220144,3.328679,24.638061
                    '''
                    msg = "self.df.iloc[3, 0]: {}"
                    self.df_3quest=self.df.iloc[3, 0]
                    logger.info(msg.format(self.df_3quest))
                    
                    

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
                    
                            
                    #if 'All Pairs' in list_row[1]:
                    #    csv_foldername  = self.zipfolder_txtcsvfiles.split("/")[0]
                    #    csv_filename = self.zipfolder_txtcsvfiles.split("/")[1]
                    #    thruput_avg = list_row[9]
                    #    thruput_min = list_row[10]
                    #    thruput_max = list_row[11]

                    #    if self.opt_verbose.lower() == "on":
                            #msg = "list_row[0]:{}"
                            #logger.info(msg.format(list_row[0]))
                            #msg = "list_row[1]:{}"
                            #logger.info(msg.format(list_row[1]))                                    

                    #        msg = "CSV_FolderName:{}, CSV_FileName:{}"
                    #        logger.info(msg.format(csv_foldername, csv_filename))
                    #        msg = "Throughput Avg.(Mbps):{}, Throughput Min.(Mbps):{} ,Throughput Max.(Mbps):{}"
                    #        logger.info(msg.format(thruput_avg, thruput_min, thruput_max))

                    #    list_csv_foldername_filename_thruput.append(csv_foldername)
                    #    list_csv_foldername_filename_thruput.append(csv_filename)
                    #    list_csv_foldername_filename_thruput.append(thruput_avg)
                    #    list_csv_foldername_filename_thruput.append(thruput_min)
                    #    list_csv_foldername_filename_thruput.append(thruput_max)        

        #return list_csv_foldername_filename_thruput

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
                    logger.info(msg.format(_3questfolder_csvfiles))

                ret_list_csv_foldername_filename_3quest = self.parse_CSVFile()

                #append_list_csv_foldername_filename_3quest.append(ret_list_csv_foldername_filename_3quest)
        
        #self.append_list_csv_foldername_filename_3quest = \
        #    append_list_csv_foldername_filename_3quest;#asign class variable
    
    '''
    chariotlog.txt

    Test Method: PPPOENAT 
    Case Number: 30010061 
    Model: DIR-1950 
    HW: A1 
    FW: v1.01b08 
    Wireless Mode: 802.11AC 
    Frequency: 5 
    Channel: 149 
    Country Code: CA 
    Encryption: YES 
    Antenna Degree: 90 
    Test Vendor: Cameo 
    Test Client: Client1 
    '''
    def parse_targetkey_TXTFile(self, list_row):
        list_txt_target_key_value = []
        txt_value = ' ';#for insert sqlite purpose
        list_target_key=['Test Method', 'Case Number', 'Model',
                        'HW','FW', 'Wireless Mode',
                        'Frequency',  'Channel', #'Modulation', remark
                        'Country Code','Encryption', 'Antenna Degree', 
                        'Test Vendor','Test Client']

        for target_key in list_target_key:
            # String comparison in Python: is vs. ==
            # https://stackoverflow.com/questions/2988017/string-comparison-in-python-is-vs
            '''
            a = 19998989890
            b = 19998989889 +1
            >>> a is b
            False
            >>> a == b
            True

            is compares two objects in memory, 
            == compares their values. For example, you can see that small integers are cached by Python:
            c = 1
            b = 1
            >>> b is c
            True
            ''' 
            #if self.opt_verbose.lower() == "on":
            #    msg = "target_key:{}; row:{}"
            #    logger.info(msg.format(target_key, list_row))

            # Emulate a do-while loop in Python?
            # https://stackoverflow.com/questions/743164/emulate-a-do-while-loop-in-python
            '''
            while True:
                stuff()
                if fail_condition:
                    break
            '''
            '''
            stuff()
            while not fail_condition:
                stuff()
            '''
            
            if target_key == list_row[0]:
                if self.opt_verbose.lower() == "on":
                    msg = "target_key:{}; value:{}"
                    logger.info(msg.format(target_key, list_row[1]))

                # Remove all newlines from inside a string
                # https://stackoverflow.com/questions/13298907/remove-all-newlines-from-inside-a-string
                '''                  
                            strip only removes characters from the beginning and end of a string. You want to use replace:

                            str2 = str.replace("\n", "")
                '''
                '''
                            list_txt_target_key_value:['Country Code', ' CA \n']
                '''

                list_txt_target_key_value = [list_row[0], list_row[1].replace(" \n", "").replace(' ', "") ]
                txt_value = list_row[1].replace(" \n", "").replace(' ', "")
                #msg = "list_txt_target_key_value:{}"
                #logger.info(msg.format(list_txt_target_key_value))
            
        return list_txt_target_key_value, txt_value        

    def parse_TXTFile(self):
        self.txt_dirfolderdata = '{}\{}'.format(self.dirname_ziplog,self.zipfolder_txtcsvfiles);#..\logs/202003051550/chariotlog.txt                                
        list_txt_row_target_key_value = []
        txt_row_value = '';#for insert sqlite purpose

        append_list_txt_row_target_key_value = []
        append_txt_row_value = [];#for insert sqlite purpose

        if self.opt_verbose.lower() == "on":
            msg = "txt_dirfolderdata:{}"
            logger.info(msg.format(self.txt_dirfolderdata))
        '''
        Test Method: PPPOENAT 
        Case Number: 30010061 
        Model: DIR-1950 
        HW: A1 
        FW: v1.01b08 
        Wireless Mode: 802.11AC 
        Frequency: 5 
        Modulation: 256QAM
        Channel: 149 
        Country Code: CA 
        Encryption: YES 
        Antenna Degree: 90 
        Test Vendor: Cameo 
        Test Client: Client1 
        '''

        csv_foldername = self.zipfolder_txtcsvfiles.split('/')[0];#get csv_foldername value
        list_txt_row_target_key_value = ['CSV FolderName', csv_foldername];#assign key and value
        txt_row_value = csv_foldername;#assign value

        append_list_txt_row_target_key_value.append(list_txt_row_target_key_value)
        append_txt_row_value.append(txt_row_value);#for insert sqlite purpose

        if self.opt_verbose.lower() == "on":
            msg = "append_list_txt_row_target_key_value:{}"
            logger.info(msg.format(append_list_txt_row_target_key_value))
            msg = "append_txt_row_value:{}"
            logger.info(msg.format(append_txt_row_value))

        with open(self.txt_dirfolderdata) as txtfile:
            rows = txtfile.readlines()

            for row in rows:
                if ':' in row:# check rows if inculde ':'
                    list_row = row.split(':');# change to list

                    if len(list_row) >= 2:#Make sure inculde target_key and value

                        list_txt_row_target_key_value, txt_row_value = self.parse_targetkey_TXTFile(list_row)
                    
                        #if self.opt_verbose.lower() == "on":
                        #    msg = "list_txt_row_target_key_value:{}"
                        #    logger.info(msg.format(list_txt_row_target_key_value))

                        # Python check for NoneType not working
                        # https://stackoverflow.com/questions/20405628/python-check-for-nonetype-not-working
                        '''
                            In Python, | is a bitwise or. You want to use a logical or here:

                            if (cts is None) or (len(cts) == 0):
                                return
                        '''
                        # not None test in Python
                        # https://stackoverflow.com/questions/3965104/not-none-test-in-python     
                        '''     
                        if not (val is None):
                            # ...
                        '''                        
                        if len(list_txt_row_target_key_value) > 0 and \
                            len(txt_row_value) > 0:# prvent empty list

                            append_list_txt_row_target_key_value.append(list_txt_row_target_key_value)
                            append_txt_row_value.append(txt_row_value);#for insert sqlite purpose

                            if self.opt_verbose.lower() == "on":
                                #msg = "list_row[0]:{}; list_row[1]:{}"
                                #logger.info(msg.format(list_row[0], list_row[1]))
                                '''
                                append_list_txt_target_key_value:[['Test Method', ' Chamber 1'], ['Case Number', ' 30010061'], ['Model', ' DIR-1950'], 
                                ['HW', ' A1'], ['FW', ' 1.01b08'], ['Wireless Mode', ' 802.11AC'], ['Frequency', ' 5'],  ['Modulation', ' 256QAM'],
                                ['Channel', ' 149'], ['Country Code', ' CA'], ['Encryption', ' YES'], ['Antenna Degree', ' 90'], ['Test Vendor', ' Cameo'], 
                                ['Test Client', ' Client5']]
                                '''                            
                                msg = "append_list_txt_row_target_key_value:{}"
                                logger.info(msg.format(append_list_txt_row_target_key_value))
                                msg = "append_txt_row_value:{}"
                                logger.info(msg.format(append_txt_row_value))

        #self.append_list_txt_row_target_key_value = append_list_txt_row_target_key_value;#assign class variable
        
        return append_list_txt_row_target_key_value, append_txt_row_value    

    '''
            INFO: fileName of listOfFileNames: [['202003061318'], ['PPPOENAT'], ['30010061'], ['DIR-1950'], ['A1'], ['v1.01b08'], ['802.11AC'], ['5'], 
                                                ['149'], ['CA'], ['YES'], ['90'], ['Cameo'], ['Client1']]

            INFO: fileName of listOfFileNames: [['202003061038'], ['Chamber1'], ['30010061'], ['DIR-1950'], ['A1'], ['1.01b08'], ['802.11AC'], ['5'], 
                                                ['256QAM'], ['149'], ['CA'], ['YES'], ['90'], ['Cameo'], ['Client5']]
    '''

    def read_TXTFile(self):

        re_exp_zipfolder = r'\/$'    
        re_exp_txtfile = r'\.txt$'
        list_txt_foldername_filename_title = []
        list_all_txt_row_target_key_value = []
        list_all_txt_row_value = [];#for sqlite purpose
        
        append_list_all_txt_row_target_key_value = []
        append_list_all_txt_row_value = [];#for sqlite purpose


        for zipfolder_txtcsvfiles in self.list_zipfolder_txtcsvfiles:
            self.zipfolder_txtcsvfiles = zipfolder_txtcsvfiles

            if self.opt_verbose.lower() == "on":
                msg = "zipfolder_txtcsvfiles:{}"
                logger.info(msg.format(zipfolder_txtcsvfiles))

            if re.search(re_exp_txtfile, zipfolder_txtcsvfiles):#check if txt file
                list_all_txt_row_target_key_value, list_all_txt_row_value = self.parse_TXTFile()

                append_list_all_txt_row_target_key_value.append(list_all_txt_row_target_key_value)
                append_list_all_txt_row_value.append(list_all_txt_row_value);#for sqlite purpose

        # Insert an element at specific index in a list and return updated list
        # https://stackoverflow.com/questions/14895599/insert-an-element-at-specific-index-in-a-list-and-return-updated-list
        '''
        >>> a = [1, 2, 4]
        >>> print a
        [1, 2, 4]

        >>> print a.insert(2, 3)
        None

        >>> print a
        [1, 2, 3, 4]

        >>> b = a.insert(3, 6)
        >>> print b
        None

        >>> print a
        [1, 2, 3, 6, 4]
        '''
        #if self.opt_verbose.lower() == "on":
        #    msg = "len of append_list_all_txt_row_value:{}"
        #    logger.info(msg.format(len(append_list_all_txt_row_value)))
        
        self.append_list_all_txt_row_target_key_value = append_list_all_txt_row_target_key_value;#assign class variable
        self.append_list_all_txt_row_value = append_list_all_txt_row_value;#for sqlite purpose
                