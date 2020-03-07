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

            if re.search(re_exp_csvfile, zipfolder_txtcsvfiles):#check if csv file
                self.csv_dirfolderdata = '{}\{}'.format(self.dirnamelog,zipfolder_txtcsvfiles);#..\logs/202003051550/chariotlog.txt

                if self.opt_verbose.lower() == "on":
                    msg = "csv_dirfolderdata:{}"
                    logger.info(msg.format(self.csv_dirfolderdata))

                with open(self.csv_dirfolderdata) as csvfile:
                    #rows = csv.reader(csvfile)
                    # Read CSV file line-by-line python
                    # https://stackoverflow.com/questions/52937859/read-csv-file-line-by-line-python
                    rows = csvfile.readlines()
                    #print(len(rows)) 

                    for row in rows:
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
                            
                            #print(len(list_row), list_row)
                            #print(len(list_row), list_row[0], list_row[1])
                            
                            if 'All Pairs' in list_row[1]:
                                if self.opt_verbose.lower() == "on":
                                    #msg = "list_row[0]:{}"
                                    #logger.info(msg.format(list_row[0]))
                                    #msg = "list_row[1]:{}"
                                    #logger.info(msg.format(list_row[1]))
                                    
                                    msg = "Throughput Avg.(Mbps):{}, Throughput Min.(Mbps):{} ,Throughput Max.(Mbps):{}"
                                    logger.info(msg.format(list_row[9], list_row[10], list_row[11]))

    def read_TXTFile(self):

        re_exp_zipfolder = r'\/$'    
        re_exp_txtfile = r'\.txt$'

        for zipfolder_txtcsvfiles in self.list_zipfolder_txtcsvfiles:
            if self.opt_verbose.lower() == "on":
                msg = "zipfolder_txtcsvfiles:{}"
                logger.info(msg.format(zipfolder_txtcsvfiles))

            if re.search(re_exp_txtfile, zipfolder_txtcsvfiles):#check if txt file
                self.csv_dirfolderdata = '{}\{}'.format(self.dirnamelog,zipfolder_txtcsvfiles);#..\logs/202003051550/chariotlog.txt                                
