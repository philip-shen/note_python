# 3/28/2020 Convert Nested JSON to Pandas DataFrame and Flatten List in a Column 
# https://gist.github.com/rafaan/4ddc91ae47ea46a46c0b
########################################################

import json
from pandas.io.json import json_normalize
import pandas as pd

import os,sys,time,glob

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger
import csvdataAnalysis as csvdata_analysis

def walk_in_dir(dir_path):
    ret_listOfFileNames = []
    ret_list_ZipFolder_TxtCsvFiles =[]

    for filename in glob.glob(os.path.join(dir_path, "*.zip")):
        listOfFileNames = []

        msg = "fileName:{} in directory:{}"
        logger.info(msg.format(filename, dir_path))

        listOfFileNames = unzip(filename=os.path.join(dir_path,filename))
        
        #msg = "listOfFileNames:{} in walk_in_dir"
        #logger.info(msg.format(listOfFileNames))        

        ret_listOfFileNames.append(listOfFileNames)

        list_ZipFolder_TxtCsvFiles = get_ZipFolder_TxtCsvFiles(listOfFileNames)
        #ret_list_ZipFolder_TxtCsvFiles.append(list_ZipFolder_TxtCsvFiles)
        ret_list_ZipFolder_TxtCsvFiles += list_ZipFolder_TxtCsvFiles

        #showFileNames_InZipFile_zip(ret_listOfFileNames)
        
    for dirname in (d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d)) ):
        walk_in_dir(os.path.join(dir_path, dirname))
    
    return ret_list_ZipFolder_TxtCsvFiles,ret_listOfFileNames

if __name__ == "__main__":
    t0 = time.time()

    with open('config.json') as f:
        data = json.load(f)

    try:
        '''
        0th file_dut_3quest:..\logs\boommic_SWout\dut.3quest\Results
        1th file_dut_3quest:..\logs\Intermic_SWin\dut.3quest\Results
        '''
        for i,_3quest in enumerate(data["3Quest"]):
            msg = '{}th path_dut_3quest:{}'
            logger.info(msg.format(i, os.path.join(data["3Quest"][i]['dut']['path']+'.3quest', 'Results') ) )


            if(os.path.isdir(os.path.join(data["3Quest"][i]['dut']['path']+'.3quest', 'Results'))):
                
                opt_verbose='OFF'

    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])

    


    



    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     






    