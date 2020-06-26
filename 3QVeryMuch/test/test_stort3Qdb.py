# 3/28/2020 Convert Nested JSON to Pandas DataFrame and Flatten List in a Column 
# https://gist.github.com/rafaan/4ddc91ae47ea46a46c0b
# 6/25/2020 Initial
########################################################

import json
from pandas.io.json import json_normalize
import pandas as pd

import os,sys,time

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

# 2020/06/25 Initial to sqlite test code
sql_create_table_3Quest_pub = """ CREATE TABLE IF NOT EXISTS _3Quest_pub (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """
sql_create_table_3Quest_road = """ CREATE TABLE IF NOT EXISTS _3Quest_road (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """
sql_create_table_3Quest_crossroad = """ CREATE TABLE IF NOT EXISTS _3Quest_crossroad (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """
sql_create_table_3Quest_train = """ CREATE TABLE IF NOT EXISTS _3Quest_train (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """
sql_create_table_3Quest_car = """ CREATE TABLE IF NOT EXISTS _3Quest_car (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                     
sql_create_table_3Quest_cafeteria = """ CREATE TABLE IF NOT EXISTS _3Quest_cafeteria (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                     
sql_create_table_3Quest_mensa = """ CREATE TABLE IF NOT EXISTS _3Quest_mensa (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                                            
sql_create_table_3Quest_callcenter = """ CREATE TABLE IF NOT EXISTS _3Quest_callcenter (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                                           
sql_create_table_3Quest_voice_distractor = """ CREATE TABLE IF NOT EXISTS _3Quest_voice_distractor (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                                               
sql_create_table_3Quest_nobgn = """ CREATE TABLE IF NOT EXISTS _3Quest_nobgn (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                                     
sql_create_table_3Quest_AVG = """ CREATE TABLE IF NOT EXISTS _3Quest_AVG (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                                                                                                                               
if __name__ == "__main__":
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))         

    with open('config.json') as f:
        data = json.load(f)

    try:
        
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

                opt_verbose='ON'
                #opt_verbose='OFF'
                
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
                
                # Ready to store 3Quest data to DB
                path_db = os.path.join(dirnamelog,'3QuestDB.db')

                localdb_sqlite = db_sqlite.DB_sqlite(path_db)
                # create a database connection
                conn = localdb_sqlite.create_connection()
            
                if conn is not None:
                    # create projects table
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_pub)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_road)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_crossroad)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_train)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_car)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_cafeteria)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_mensa)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_callcenter)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_voice_distractor)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_nobgn)
                    localdb_sqlite.create_table(conn, sql_create_table_3Quest_AVG)
                    
                else:
                    print("Error! cannot create the database connection.")                            

                strdirname = os.path.dirname(data["3Quest"][i]['path_dut'])
                str_split=os.path.split(strdirname)
                dut_foldername=str_split[1]
                insert_date = str(local_time.tm_year)+'/'+str(local_time.tm_mon)+'/'+str(local_time.tm_mday)
                insert_time = str(local_time.tm_hour)+':'+str(local_time.tm_min)+':'+str(local_time.tm_sec)

                # We can also close the connection if we are done with it.
                # Just be sure any changes have been committed or they will be lost.
                conn.close()        

    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     





    