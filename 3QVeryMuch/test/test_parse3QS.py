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

if __name__ == "__main__":
    t0 = time.time()

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
                                                        ret_list_3questFolder_CsvFiles,\
                                                        opt_verbose)

                #local_csvdata_analysis.read_CSVFile()
                local_csvdata_analysis.read_CSVFile_02()                                                                                


    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     





    