import os,sys,time
import numpy as np
import json
from pandas.io.json import json_normalize

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

#import func_split_3channel
import scipy.io.wavfile
import func_split_3channel as func_split_3ch
from logger import logger
from lib_creat3Qreport import *


if __name__ == "__main__":
    
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))


    with open('config.json') as f:
        data = json.load(f)

    opt_verbose='ON'

    trim_all_noise_wav(data,opt_verbose)
    
    if opt_verbose.lower() == "on":
        msg = 'running test_run_3pqss.py'
        logger.info(msg.format())    
        
    os.system('./test_run_3pqss.py')

    create3Qreport(data, local_time, opt_verbose)

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     