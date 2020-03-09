# -*- coding: utf-8 -*-
import os,sys,time

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger
from libZip import *
from readConfig import *
import csvdataAnalysis as csvdata_analysis
import db_sqlite as db_sqlite

# 2020/03/08 Initial to sqlite test code
sql_create_Chariot_CSV_Throughput_table = """ CREATE TABLE IF NOT EXISTS Chariot_CSV_Throughput (
                                                                    id integer PRIMARY KEY,
                                                                    csv_foldername text NOT NULL,
                                                                    csv_filename text,
                                                                    throughput_avg text,
                                                                    throughput_min text,
                                                                    throughput_max text   
                                            ); """

'''
INFO: fileName of listOfFileNames: [['202003061318'], ['PPPOENAT'], ['30010061'], ['DIR-1950'], ['A1'], ['v1.01b08'], ['802.11AC'], ['5'], 
                                  ['149'], ['CA'], ['YES'], ['90'], ['Cameo'], ['Client1']]

INFO: fileName of listOfFileNames: [['202003061038'], ['Chamber1'], ['30010061'], ['DIR-1950'], ['A1'], ['1.01b08'], ['802.11AC'], ['5'], 
                                  ['256QAM'], ['149'], ['CA'], ['YES'], ['90'], ['Cameo'], ['Client5']]
'''

# modulation text, #not moddulation column
sql_create_Chariot_Log_table = """ CREATE TABLE IF NOT EXISTS Chariot_Log (
                                                        id integer PRIMARY KEY,
                                                        csv_foldername text NOT NULL,
                                                        test_method text,
                                                        case_number text,
                                                        model text,
                                                        hw text,
                                                        fw text,
                                                        wireless_mode text,
                                                        frequency text,                                                                    
                                                        channel text,
                                                        country_code txt,
                                                        encryption txt,
                                                        antenna_degree txt,
                                                        test_vendor txt,
                                                        test_client text
                                            ); """

if __name__ == "__main__":
    t0 = time.time()

    args = sys.argv
    try:
        if(os.path.isdir(args[1])):
            ret_list_ZipFolder_TxtCsvFiles, ret_list_ZipFolderFileNames = walk_in_dir(args[1])
            dirname_ziplog = args[1]
            #showFileNames_InZipFile_zip(ret_list_ZipFolderFileNames)
            #showFileNames_InZipFile_zip(ret_list_ZipFolder_TxtCsvFiles)
            
            opt_verbose='ON'
            #opt_verbose='OFF'
            
            # Panada can't parse csv file
            #local_csvdata_analysis = csvdata_analysis.PandasDataAnalysis(dirnamelog,\
            #                                            ret_list_ZipFolder_TxtCsvFiles,\
            #                                            opt_verbose)
            

            local_csvdata_analysis = csvdata_analysis.CSVDataAnalysis(dirnamelog,\
                                                        dirname_ziplog,\
                                                        ret_list_ZipFolder_TxtCsvFiles,\
                                                        opt_verbose)
            local_csvdata_analysis.read_CSVFile()
            showFileNames_InZipFile_zip(local_csvdata_analysis.append_list_csv_foldername_filename_thruput)
            
            
            local_csvdata_analysis.read_TXTFile()
            #showFileNames_InZipFile_zip(local_csvdata_analysis.append_list_all_txt_row_target_key_value)
            showFileNames_InZipFile_zip(local_csvdata_analysis.append_list_all_txt_row_value)
            
            #print("len of local_csvdata_analysis.append_list_all_txt_row_value: {}".\
            #        format(len(local_csvdata_analysis.append_list_all_txt_row_value) ))            
            path_db = os.path.join(dirnamelog,'WiFiPerformance.db')

            localdb_sqlite = db_sqlite.DB_sqlite(path_db)
            # create a database connection
            conn = localdb_sqlite.create_connection()
            
            if conn is not None:
                # create projects table
                localdb_sqlite.create_table(conn, sql_create_Chariot_CSV_Throughput_table)
                localdb_sqlite.create_table(conn, sql_create_Chariot_Log_table)
            else:
                print("Error! cannot create the database connection.")                            

            #Insert CSV foldername_filename_thruput data into sqlite
            localdb_sqlite.insert_csv_data_tosqlite(local_csvdata_analysis.append_list_csv_foldername_filename_thruput, \
                                                    localdb_sqlite,conn)
            
            #localdb_sqlite.delete_table_chariot_csv_throughput_all(conn) 
            #localdb_sqlite.delete_table_chariot_csv_throughput(conn, '12') 

            #Insert Chariot log foldername_filename_thruput data into sqlite
            localdb_sqlite.insert_chariot_log_tosqlite(local_csvdata_analysis.append_list_all_txt_row_value, \
                                                    localdb_sqlite,conn)

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()    

        else:
            unzip(os.path.join(args[1]))
            name, _ = os.path.splitext(args[1])
            if (os.path.isdir(name)):
                walk_in_dir(name)
                
    except IndexError:
        print('IndexError: Usage "python %s ZIPFILE_NAME" or "python %s DIR_NAME"' % (args[0], args[0]))
    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     