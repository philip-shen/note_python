# 7/6/2020 Initial
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
                                       
if __name__ == "__main__":
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))         

    args = sys.argv
    
    with open('config.json') as f:
        data = json.load(f)

    try:

        for i,_3quest in enumerate(data["3Quest"]):            

            # Check path if exists or not
            if(os.path.isdir(os.path.join(data["3Quest"][i]['path_dut']+'.3quest', 'Results'))):
                
                opt_verbose='ON'
                #opt_verbose='OFF'

                path_dut = os.path.dirname(data["3Quest"][i]['path_dut'])
                str_split=os.path.split(path_dut)
                dut_foldername=str_split[1]
                insert_date = '20200705'
                insert_time = '20200705'

                # Ready to store 3Quest data to DB
                if platform.system().lower() == 'windows': db_name_3quest = '3QuestDB.db'
                if platform.system().lower() == 'linux': db_name_3quest = '3QuestDB_tensor4.db'
                path_db = os.path.join(dirnamelog,db_name_3quest)

                localdb_sqlite = db_sqlite.DB_sqlite(path_db,\
                                                    dut_foldername,insert_date,insert_time,\
                                                    path_dut,\
                                                    opt_verbose)

                # create a database connection
                conn = localdb_sqlite.create_connection()

                # create dataframe by SQL
                localdb_sqlite.query_3quest_report(localdb_sqlite, conn)

                # We can also close the connection if we are done with it.
                # Just be sure any changes have been committed or they will be lost.
                conn.close()        

    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])                            

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     