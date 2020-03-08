#!/usr/bin/env python3

import os,time,sys
import pandas as pd
import numpy as np
import re
import csv

from logger import logger

class PandasDataAnalysis:
    def __init__(self,dirnamelog,list_ZipFolder_TxtCsvFiles,opt_verbose='OFF'):
        #FOLDER = csv_dirfolder
        #self.csv_dirfolderdata = '{}/{}.csv'.format(dirnamelog,csv_dirfolder)
        self.dirnamelog = dirnamelog
        self.list_zipfolder_txtcsvfiles = list_ZipFolder_TxtCsvFiles
        self.opt_verbose = opt_verbose        

    def read_CSVFile(self):

        re_exp_zipfolder = r'\/$'    
        re_exp_txtfile = r'\.txt$'
        re_exp_csvfile = r'\.csv$'

        for zipfolder_txtcsvfiles in self.list_zipfolder_txtcsvfiles:
            if self.opt_verbose.lower() == "on":
                msg = "zipfolder_txtcsvfiles:{}"
                logger.info(msg.format(zipfolder_txtcsvfiles))

            if re.search(re_exp_csvfile, zipfolder_txtcsvfiles):#check if csv or txt file
                self.csv_dirfolderdata = '{}/{}'.format(self.dirnamelog,zipfolder_txtcsvfiles);#..\logs/202003051550/chariotlog.txt

                if self.opt_verbose.lower() == "on":
                    msg = "csv_dirfolderdata:{}"
                    logger.info(msg.format(self.csv_dirfolderdata))

                # get date and close from csv file
                # 3/7/2020 Error msg
                # pandas.errors.ParserError: Error tokenizing data. C error: Expected 1 fields in line 2, saw 4
                # Python Pandas Error tokenizing data 
                # https://stackoverflow.com/questions/18039057/python-pandas-error-tokenizing-data
                #
                # Pandas Skipping lines(Stop warnings from showing)
                # https://stackoverflow.com/questions/44680141/pandas-skipping-linesstop-warnings-from-showing
                '''
                0                                 PRODUCT INFORMATION
                1        Product Type,Version,Build Level,Export Time
                2              IxChariot,6.70 ,44,03/06/2020 10:44:55
                3                                             SUMMARY
                4   Filename,Run Start Time,Run End Time,Elapsed T...
                5   D:\ChamberWirelessPerformanceTest\TestResultTe...
                6                                         RUN OPTIONS
                7   Filename,End Type,Duration,Reporting Type,Auto...
                8   D:\ChamberWirelessPerformanceTest\TestResultTe...
                9                               ENDPOINT PAIR SUMMARY
                10  Filename,Pair,Timing Records,Network Protocol,...
                11  D:\ChamberWirelessPerformanceTest\TestResultTe...
                12  D:\ChamberWirelessPerformanceTest\TestResultTe...
                13  D:\ChamberWirelessPerformanceTest\TestResultTe...
                14  D:\ChamberWirelessPerformanceTest\TestResultTe...
                15  D:\ChamberWirelessPerformanceTest\TestResultTe...
                16  D:\ChamberWirelessPerformanceTest\TestResultTe...
                17                                     GROUP AVERAGES
                18  Filename,Group Name,Timing Records,Transaction...
                19  D:\ChamberWirelessPerformanceTest\TestResultTe...
                '''
                '''
                0,1,2,3,4,5,6,7,8,9,10,11,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                Filename,         ,Throughput Avg.(Mbps),Throughput Min.(Mbps),Throughput Max.(Mbps)

                usecols = [0,9,10,11], #index_col = [0], 
                names = ['filename', 'throughput_avg', 'throughput_min','throughput_max']
                '''
                csv_thruputfile = pd.read_csv(self.csv_dirfolderdata, sep='\n',
                                            header = None, 
                                             index_col=False,
                                            error_bad_lines=False,
                                            warn_bad_lines=False                                            
                                )
                df = csv_thruputfile.copy()
                self.df = df

                if self.opt_verbose.lower() == "on":
                    #msg = "CSV file Contents: {}"
                    #logger.info(msg.format(self.df))
                    
                    # Selecting a row of pandas series/dataframe by integer index
                    # https://stackoverflow.com/questions/16096627/selecting-a-row-of-pandas-series-dataframe-by-integer-index
                    '''
                    INFO: Row of Throughput:                                                     0
                    19  D:\ChamberWirelessPerformanceTest\TestResultTe...

                    Can't find thruput value
                    '''
                    msg = "Row of Throughput: {}"
                    self.df_Throughput=self.df.iloc[-1:]
                    logger.info(msg.format(self.df_Throughput))
                    

                    # Pandas how to get a cell value and update it
                    # https://kanoki.org/2019/04/12/pandas-how-to-get-a-cell-value-and-update-it/
                    # How to get a value from a cell of a dataframe?
                    # https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
                    #msg = "Throughput Avg.(Mbps):{}, Throughput Min.(Mbps):{} ,Throughput Max.(Mbps):{}"
                    #logger.info(msg.format(self.df.iat[19,9], self.df.iat[19,10], self.df.iat[19,11]))


class CSVDataAnalysis:
    def __init__(self,dirnamelog,list_ZipFolder_TxtCsvFiles,opt_verbose='OFF'):
        
        self.dirnamelog = dirnamelog
        self.list_zipfolder_txtcsvfiles = list_ZipFolder_TxtCsvFiles
        self.opt_verbose = opt_verbose
    
    def parse_CSVFile(self):
        self.csv_dirfolderdata = '{}\{}'.format(self.dirnamelog,self.zipfolder_txtcsvfiles);#..\logs/202003051550/chariotlog.txt
        list_csv_foldername_filename_thruput = []

        if self.opt_verbose.lower() == "on":
            msg = "csv_dirfolderdata:{}"
            logger.info(msg.format(self.csv_dirfolderdata))

        with open(self.csv_dirfolderdata) as csvfile:
            #rows = csv.reader(csvfile)
            # Read CSV file line-by-line python
            # https://stackoverflow.com/questions/52937859/read-csv-file-line-by-line-python
            rows = csvfile.readlines()
            #print(len(rows)) 

            # To Speed Up Search Cause line of Throughput in bottom
            # Traverse a list in reverse order in Python
            # https://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python
            for row in reversed(rows):

                if ',' in row:# check rows if inculde ','
                    list_row = row.split(',')
                    #for row in rows:
                    # Does Python have a string 'contains' substring method?
                    # https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
                    '''
                        ['D:\\ChamberWirelessPerformanceTest\\TestResultTemp\\202003061038\\P0-Client5_Rx_result_1st.tst', 
                        'All Pairs',
                        '500.000000     ',
                        '500.000000     ',
                        '5000000000.000000',
                        '0.000000       ',
                        '',
                        '', 
                        '',
                        '353.273',
                        '22.982',
                        '94.229', '     4.435', '     0.287', '     1.178', '     1.358', 
                        '     0.849', '     3.481', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 
                        '', '', '', '', '', '', '', '', '', '']
                    '''
                            
                    if 'All Pairs' in list_row[1]:
                        csv_foldername  = self.zipfolder_txtcsvfiles.split("/")[0]
                        csv_filename = self.zipfolder_txtcsvfiles.split("/")[1]
                        thruput_avg = list_row[9]
                        thruput_min = list_row[10]
                        thruput_max = list_row[11]

                        if self.opt_verbose.lower() == "on":
                            #msg = "list_row[0]:{}"
                            #logger.info(msg.format(list_row[0]))
                            #msg = "list_row[1]:{}"
                            #logger.info(msg.format(list_row[1]))                                    

                            msg = "CSV_FolderName:{}, CSV_FileName:{}"
                            logger.info(msg.format(csv_foldername, csv_filename))
                            msg = "Throughput Avg.(Mbps):{}, Throughput Min.(Mbps):{} ,Throughput Max.(Mbps):{}"
                            logger.info(msg.format(thruput_avg, thruput_min, thruput_max))

                        list_csv_foldername_filename_thruput.append(csv_foldername)
                        list_csv_foldername_filename_thruput.append(csv_filename)
                        list_csv_foldername_filename_thruput.append(thruput_avg)
                        list_csv_foldername_filename_thruput.append(thruput_min)
                        list_csv_foldername_filename_thruput.append(thruput_max)        

        return list_csv_foldername_filename_thruput

    def read_CSVFile(self):

        re_exp_zipfolder = r'\/$'    
        re_exp_txtfile = r'\.txt$'
        #re_exp_csvfile = r'\.csv$'
        re_exp_csvfile = r'\_[0-9][a-z][a-z].csv$';#_1st.csv, _2nd.csv, _3rd.csv

        ret_list_csv_foldername_filename_thruput = []
        append_list_csv_foldername_filename_thruput = []

        for zipfolder_txtcsvfiles in self.list_zipfolder_txtcsvfiles:
            self.zipfolder_txtcsvfiles = zipfolder_txtcsvfiles

            if self.opt_verbose.lower() == "on":
                msg = "zipfolder_txtcsvfiles:{}"
                logger.info(msg.format(zipfolder_txtcsvfiles))

            if re.search(re_exp_csvfile, zipfolder_txtcsvfiles):#check if csv file
                ret_list_csv_foldername_filename_thruput = self.parse_CSVFile()

                append_list_csv_foldername_filename_thruput.append(ret_list_csv_foldername_filename_thruput)

        
        self.append_list_csv_foldername_filename_thruput = \
            append_list_csv_foldername_filename_thruput;#asign class variable
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
        self.txt_dirfolderdata = '{}\{}'.format(self.dirnamelog,self.zipfolder_txtcsvfiles);#..\logs/202003051550/chariotlog.txt                                
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
                