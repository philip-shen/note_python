# 3/28/2020 Convert Nested JSON to Pandas DataFrame and Flatten List in a Column 
# https://gist.github.com/rafaan/4ddc91ae47ea46a46c0b
# 6/25/2020 Initial
# 7/7/2020 Merge  test_stort3Qdb.py and test_query3Qtable.py
########################################################

import json
from pandas.io.json import json_normalize
import pandas as pd

import os,sys,time,platform

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger
from libCSV import *
import csvdataAnalysis as csvdata_analysis
import db_sqlite as db_sqlite
#import func_split_3channel as func_split_3ch

def trim_all_noise_wav(data,opt_verbose='OFF'):
    ref_fpath_16K = data["trim_ref_info"]['ref_fpath_16K']
    ref_fpath_48K = data["trim_ref_info"]['ref_fpath_48K']
    add_key = 'dut'

    msg = 'data["trim_ref_info"][\'ref_fpath_16K\']: {}'
    logger.info(msg.format(data["trim_ref_info"]['ref_fpath_16K']))
    msg = 'data["trim_ref_info"][\'ref_fpath_48K\']: {}'
    logger.info(msg.format(data["trim_ref_info"]['ref_fpath_48K']))

    for i,_3quest in enumerate(data["3Quest"]):

        if (data["3Quest"][i]['label_dut'] != '' and data["3Quest"][i]['label_standmic'] != ''\
            and os.path.isfile(data["3Quest"][i]['mic_dut']) \
            and os.path.isfile(data["3Quest"][i]['mic_standmic'])):#bypass without labels and dut, standmic wav file
        
            #opt_verbose='ON'
            #opt_verbose='OFF'
        
            func_split_3ch.mkdir_folder(data["3Quest"][i]['path_dut'])

            msg = 'data["3Quest"][{}][\'mic_dut\']: {}'
            logger.info(msg.format(i,data["3Quest"][i]['mic_dut']))
            
            msg = 'data["3Quest"][{}][\'label_dut\']: {}'
            logger.info(msg.format(i,data["3Quest"][i]['label_dut']))
            
            start_time, end_time, label = func_split_3ch.load_label_file(data["3Quest"][i]['label_dut'])

            msg = 'data["3Quest"][{}][\'gain_dut\']: {}'
            logger.info(msg.format(i,data["3Quest"][i]['gain_dut']))
            
            msg = 'data["3Quest"][{}][\'channel_dut\']: {}'
            logger.info(msg.format(i,data["3Quest"][i]['channel_dut']))

            if (data["3Quest"][i]['channel_dut'] == 1):
                func_split_3ch.func_gen_dut_wav_from_mono(data["3Quest"][i]['path_dut'], \
                    ref_fpath_16K, ref_fpath_48K, \
                    data["3Quest"][i]['mic_dut'], \
                    start_time, label,  \
                    data["3Quest"][i]['gain_dut'], \
                    add_key, opt_verbose)

            elif (data["3Quest"][i]['channel_dut'] == 2):
                func_split_3ch.func_gen_dut_wav_from_stereo(data["3Quest"][i]['path_dut'], \
                    ref_fpath_16K, ref_fpath_48K, \
                    data["3Quest"][i]['mic_dut'], \
                    start_time, label, \
                    data["3Quest"][i]['gain_dut'], \
                    add_key, opt_verbose)

        
            #msg = 'data["3Quest"][{}][\'path_standmic\']: {}'
            #logger.info(msg.format(i,data["3Quest"][i]['path_standmic']))
            func_split_3ch.mkdir_folder(data["3Quest"][i]['path_standmic'])

            msg = 'data["3Quest"][{}][\'mic_standmic\']: {}'
            logger.info(msg.format(i,data["3Quest"][i]['mic_standmic']))
            
            msg = 'data["3Quest"][{}][\'label_standmic\']: {}'
            logger.info(msg.format(i,data["3Quest"][i]['label_standmic']))
            
            msg = 'data["3Quest"][{}][\'gain_standmic\']: {}'
            logger.info(msg.format(i,data["3Quest"][i]['gain_standmic']))
            
            start_time, end_time, label = func_split_3ch.load_label_file(data["3Quest"][i]['label_standmic'])

            func_split_3ch.func_gen_standmic_wav(data["3Quest"][i]['path_standmic'], \
                        ref_fpath_16K, ref_fpath_48K, \
                        data["3Quest"][i]['mic_standmic'], \
                        start_time, label, \
                        data["3Quest"][i]['gain_standmic'], \
                        opt_verbose)

        else:
            msg = 'Please check data["3Quest"][{}][\'mic_dut\']:{} if exist or not?'
            logger.info(msg.format(i, data["3Quest"][i]['mic_dut']))
        
            msg = 'Please check data["3Quest"][{}][\'mic_standmic\']:{} if exist or not?'
            logger.info(msg.format(i, data["3Quest"][i]['mic_standmic']))

def create3Qreport(data, local_time, opt_verbose='OFF'):
    for i,_3quest in enumerate(data["3Quest"]):

        # Check path if exists or not
        if(os.path.isdir(os.path.join(data["3Quest"][i]['path_dut']+'.3quest', 'Results'))):
            '''
            0th path_dut_3quest:..\logs\boommic_SWout\dut.3quest\Results
            1th path_dut_3quest:..\logs\Intermic_SWin\dut.3quest\Results
            '''

            path_dut_3quest_results = os.path.join(data["3Quest"][i]['path_dut']+'.3quest', 'Results')
            msg = '{}th path_dut_3quest_results:{}'
            logger.info(msg.format(i, path_dut_3quest_results) )

            file_type="*.csv"
            ret_list_3questFolder_CsvFiles = walk_in_dir(path_dut_3quest_results,file_type)

                
            local_csvdata_analysis = csvdata_analysis.CSVDataAnalysis(dirnamelog,\
                                                        path_dut_3quest_results,\
                                                        ret_list_3questFolder_CsvFiles
                                                        )
            local_csvdata_analysis.read_CSVFile()
            tmp_csv=local_csvdata_analysis.write_CSVFile_del1strow()
            # copy tmp.csv to output.csv of 3Quest Result Path 
            local_csvdata_analysis.copy_CSVFile_to3questResultPath(tmp_csv,\
                                                                    local_csvdata_analysis._3questfolder_csvfiles)            

            local_csvdata_analysis = csvdata_analysis.PandasDataAnalysis(dirnamelog,\
                                                        path_dut_3quest_results,\
                                                        ret_list_3questFolder_CsvFiles
                                                        )

            # get list of all background noise 3Quest value
            list_allnoises_3quest_values = local_csvdata_analysis.parse_CSVFile_02()

            # prepare dut_foldername, insert_date, insert_time
            path_dut = os.path.dirname(data["3Quest"][i]['path_dut'])
            str_split=os.path.split(path_dut)
            dut_foldername=str_split[1]
            insert_date = str(local_time.tm_year)+str("{:02d}".format(local_time.tm_mon) )+str("{:02d}".format(local_time.tm_mday))
            insert_time = str("{:02d}".format(local_time.tm_hour))+':'+str("{:02d}".format(local_time.tm_min))+':'+str("{:02d}".format(local_time.tm_sec))

            # Ready to store 3Quest data to DB
            if platform.system().lower() == 'windows': db_name_3quest = '3QuestDB.db'
            if platform.system().lower() == 'linux': db_name_3quest = '3QuestDB_tensor4.db'
            path_db = os.path.join(dirnamelog,db_name_3quest)

            if opt_verbose.lower() == "on":
                msg = "path_db: {}"
                logger.info(msg.format(path_db))    

            localdb_sqlite = db_sqlite.DB_sqlite(path_db,\
                                                dut_foldername,insert_date,insert_time,\
                                                path_dut,\
                                                opt_verbose)

            # create a database connection
            conn = localdb_sqlite.create_connection()
            
            if conn is not None:
                # create projects table                    
                localdb_sqlite.create_all_tables_3Quest(conn)
            else:
                print("Error! cannot create the database connection.")                            

            # Insert noise type data to DB  
            localdb_sqlite.insert_noise_file_tosqlite(localdb_sqlite, conn)

            # Insert dut path data to DB to prevent 3Quest data redundancy
            number_of_rows_3Quest_path = localdb_sqlite.insert_3quest_path_tosqlite(localdb_sqlite, conn)

            if number_of_rows_3Quest_path < 1:# Insert if not exists
                for list_noises_3quest_values in list_allnoises_3quest_values:

                    ''' 
                    INFO: list_noises_3quest_values:[['pub', 'pub', 'pub', 'pub'], ['SMOS', 'NMOS', 'GMOS', 'delta_SNR'], ['2.840550', '4.154481', '2.914813', '29.453750']]
                    INFO: list_noises_3quest_values:[['AVG', 'AVG', 'AVG', 'AVG'], ['SMOS', 'NMOS', 'GMOS', 'delta_SNR'], ['3.358136', '4.220144', '3.328679', '24.638061']]
                    ''' 
                    #Insert list_noises_3quest_values data into sqlite
                    localdb_sqlite.insert_csv_data_tosqlite(list_noises_3quest_values, \
                                                                localdb_sqlite, \
                                                                conn)

                # create dataframe by SQL for excel report
                localdb_sqlite.query_3quest_table(localdb_sqlite, conn)

                # write dataframe to excel
                localdb_sqlite.write_to_excel()                                            
                
            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()        

def test_create3Qreport_wonobgn_reAverage(data, local_time, opt_verbose='OFF'):
    for i,_ in enumerate(data["3Quest"]):

        # Check path if exists or not
        if(os.path.isdir(os.path.join(data["3Quest"][i]['path_dut']+'.3quest', 'Results'))):


            # prepare dut_foldername, insert_date, insert_time
            path_dut = os.path.dirname(data["3Quest"][i]['path_dut'])
            str_split=os.path.split(path_dut)
            dut_foldername=str_split[1]
            #insert_date = str(local_time.tm_year)+str("{:02d}".format(local_time.tm_mon) )+str("{:02d}".format(local_time.tm_mday))
            insert_date = '20200713'
            insert_time = str("{:02d}".format(local_time.tm_hour))+':'+str("{:02d}".format(local_time.tm_min))+':'+str("{:02d}".format(local_time.tm_sec))

            # Ready to store 3Quest data to DB
            if platform.system().lower() == 'windows': db_name_3quest = '3QuestDB.db'
            if platform.system().lower() == 'linux': db_name_3quest = '3QuestDB_tensor4.db'
            path_db = os.path.join(dirnamelog,db_name_3quest)

            if opt_verbose.lower() == "on":
                msg = "path_db: {}"
                logger.info(msg.format(path_db))    

            localdb_sqlite = db_sqlite.DB_sqlite(path_db,\
                                                dut_foldername,insert_date,insert_time,\
                                                path_dut,\
                                                opt_verbose)

            # create a database connection
            conn = localdb_sqlite.create_connection()
            
            if conn is not None:
                # create projects table                    
                localdb_sqlite.create_all_tables_3Quest(conn)
            else:
                print("Error! cannot create the database connection.")                            

            # Insert noise type data to DB  
            #localdb_sqlite.insert_noise_file_tosqlite(localdb_sqlite, conn)

            # Insert dut path data to DB to prevent 3Quest data redundancy
            #number_of_rows_3Quest_path = localdb_sqlite.insert_3quest_path_tosqlite(localdb_sqlite, conn)

            #if number_of_rows_3Quest_path < 1:# Insert if not exists
            #    for list_noises_3quest_values in list_allnoises_3quest_values:

            #        ''' 
            #        INFO: list_noises_3quest_values:[['pub', 'pub', 'pub', 'pub'], ['SMOS', 'NMOS', 'GMOS', 'delta_SNR'], ['2.840550', '4.154481', '2.914813', '29.453750']]
            #        INFO: list_noises_3quest_values:[['AVG', 'AVG', 'AVG', 'AVG'], ['SMOS', 'NMOS', 'GMOS', 'delta_SNR'], ['3.358136', '4.220144', '3.328679', '24.638061']]
            #        ''' 
                    #Insert list_noises_3quest_values data into sqlite
            #        localdb_sqlite.insert_csv_data_tosqlite(list_noises_3quest_values, \
            #                                                    localdb_sqlite, \
            #                                                    conn)

                # create dataframe by SQL for excel report
            #    localdb_sqlite.query_3quest_table_nobgnOnly(localdb_sqlite, conn)
            #    localdb_sqlite.query_3quest_table_withoutnobgn(localdb_sqlite, conn)

                # write dataframe to excel
                #localdb_sqlite.write_to_excel()                                            

            # test purpose
            localdb_sqlite.query_3quest_table_nobgnOnly(localdb_sqlite, conn)
            localdb_sqlite.query_3quest_table_withoutnobgn(localdb_sqlite, conn)    
            
            path_report_excel = os.path.join(path_dut, dut_foldername+'.xlsx')
            
            df_3quest_table_excel= localdb_sqlite.df_query_3quest_table_noise.iloc [0:11, 1:8]
            localdb_sqlite.write_to_excel_fromdata(path_report_excel,df_3quest_table_excel)



            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()    

def create3Qreport_wonobgn_reAverage(data, local_time, opt_verbose='OFF'):
    for i,_3quest in enumerate(data["3Quest"]):

        # Check path if exists or not
        if(os.path.isdir(os.path.join(data["3Quest"][i]['path_dut']+'.3quest', 'Results'))):
            '''
            0th path_dut_3quest:..\logs\boommic_SWout\dut.3quest\Results
            1th path_dut_3quest:..\logs\Intermic_SWin\dut.3quest\Results
            '''

            path_dut_3quest_results = os.path.join(data["3Quest"][i]['path_dut']+'.3quest', 'Results')
            msg = '{}th path_dut_3quest_results:{}'
            logger.info(msg.format(i, path_dut_3quest_results) )

            file_type="*.csv"
            ret_list_3questFolder_CsvFiles = walk_in_dir(path_dut_3quest_results,file_type)

                
            local_csvdata_analysis = csvdata_analysis.CSVDataAnalysis(dirnamelog,\
                                                        path_dut_3quest_results,\
                                                        ret_list_3questFolder_CsvFiles
                                                        )
            local_csvdata_analysis.read_CSVFile()
            tmp_csv=local_csvdata_analysis.write_CSVFile_del1strow()
            # copy tmp.csv to output.csv of 3Quest Result Path 
            local_csvdata_analysis.copy_CSVFile_to3questResultPath(tmp_csv,\
                                                                    local_csvdata_analysis._3questfolder_csvfiles)            

            local_csvdata_analysis = csvdata_analysis.PandasDataAnalysis(dirnamelog,\
                                                        path_dut_3quest_results,\
                                                        ret_list_3questFolder_CsvFiles
                                                        )

            # get list of all background noise 3Quest value
            list_allnoises_3quest_values = local_csvdata_analysis.parse_CSVFile_02()

            # prepare dut_foldername, insert_date, insert_time
            path_dut = os.path.dirname(data["3Quest"][i]['path_dut'])
            str_split=os.path.split(path_dut)
            dut_foldername=str_split[1]
            insert_date = str(local_time.tm_year)+str("{:02d}".format(local_time.tm_mon) )+str("{:02d}".format(local_time.tm_mday))
            insert_time = str("{:02d}".format(local_time.tm_hour))+':'+str("{:02d}".format(local_time.tm_min))+':'+str("{:02d}".format(local_time.tm_sec))

            # Ready to store 3Quest data to DB
            if platform.system().lower() == 'windows': db_name_3quest = '3QuestDB.db'
            if platform.system().lower() == 'linux': db_name_3quest = '3QuestDB_tensor4.db'
            path_db = os.path.join(dirnamelog,db_name_3quest)

            if opt_verbose.lower() == "on":
                msg = "path_db: {}"
                logger.info(msg.format(path_db))    

            localdb_sqlite = db_sqlite.DB_sqlite(path_db,\
                                                dut_foldername,insert_date,insert_time,\
                                                path_dut,\
                                                opt_verbose)

            # create a database connection
            conn = localdb_sqlite.create_connection()
            
            if conn is not None:
                # create projects table                    
                localdb_sqlite.create_all_tables_3Quest(conn)
            else:
                print("Error! cannot create the database connection.")                            

            # Insert noise type data to DB  
            localdb_sqlite.insert_noise_file_tosqlite(localdb_sqlite, conn)

            # Insert dut path data to DB to prevent 3Quest data redundancy
            number_of_rows_3Quest_path = localdb_sqlite.insert_3quest_path_tosqlite(localdb_sqlite, conn)

            if number_of_rows_3Quest_path < 1:# Insert if not exists
                for list_noises_3quest_values in list_allnoises_3quest_values:

                    ''' 
                    INFO: list_noises_3quest_values:[['pub', 'pub', 'pub', 'pub'], ['SMOS', 'NMOS', 'GMOS', 'delta_SNR'], ['2.840550', '4.154481', '2.914813', '29.453750']]
                    INFO: list_noises_3quest_values:[['AVG', 'AVG', 'AVG', 'AVG'], ['SMOS', 'NMOS', 'GMOS', 'delta_SNR'], ['3.358136', '4.220144', '3.328679', '24.638061']]
                    ''' 
                    #Insert list_noises_3quest_values data into sqlite
                    localdb_sqlite.insert_csv_data_tosqlite(list_noises_3quest_values, \
                                                                localdb_sqlite, \
                                                                conn)

                # create dataframe by SQL for excel report
                localdb_sqlite.query_3quest_table_nobgnOnly(localdb_sqlite, conn)
                localdb_sqlite.query_3quest_table_withoutnobgn(localdb_sqlite, conn)    
            
                path_report_excel = os.path.join(path_dut, dut_foldername+'.xlsx')
            
                # write dataframe to excel
                df_3quest_table_excel= localdb_sqlite.df_query_3quest_table_noise.iloc [0:11, 1:8]
                localdb_sqlite.write_to_excel_fromdata(path_report_excel,df_3quest_table_excel)
                
            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()        
