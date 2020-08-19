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
from lib_creat3Qreport import *


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
    opt_verbose='ON'

    try:
        
        #create3Qreport(data,local_time, opt_verbose)
        test_create3Qreport_wonobgn_reAverage(data,local_time, opt_verbose)
        #create3Qreport_wonobgn_reAverage(data,local_time, opt_verbose)

    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     
    