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


if __name__ == "__main__":
    t0 = time.time()

    args = sys.argv
    try:
        if(os.path.isdir(args[1])):
            ret_list_ZipFolder_TxtCsvFiles, ret_list_ZipFolderFileNames = walk_in_dir(args[1])
            
            #showFileNames_InZipFile_zip(ret_list_ZipFolderFileNames)
            #showFileNames_InZipFile_zip(ret_list_ZipFolder_TxtCsvFiles)
            
            opt_verbose='ON'
            #opt_verbose='OFF'
            
            # Panada can't parse csv file
            #local_csvdata_analysis = csvdata_analysis.PandasDataAnalysis(dirnamelog,\
            #                                            ret_list_ZipFolder_TxtCsvFiles,\
            #                                            opt_verbose)
            

            local_csvdata_analysis = csvdata_analysis.CSVDataAnalysis(dirnamelog,\
                                                        ret_list_ZipFolder_TxtCsvFiles,\
                                                        opt_verbose)
            #local_csvdata_analysis.read_CSVFile()
            #showFileNames_InZipFile_zip(local_csvdata_analysis.append_list_csv_foldername_filename_thruput)
            
            local_csvdata_analysis.read_TXTFile()
            showFileNames_InZipFile_zip(local_csvdata_analysis.append_list_txt_target_key_value)

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