# 3/28/2020 Initial
# 
########################################################
import json
import pandas as pd

import os,sys,time
from pydrive.drive import GoogleDrive

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger
import readConfig 
import googleDrive as google_drive

if __name__ == "__main__":
    t0 = time.time()

    json_file='config.json'
    #opt_verbose='ON'
    opt_verbose='OFF'

    # Read column name from df to act as key
    local_readConfig_readjson = readConfig.ReadJSON(json_file,opt_verbose)
    # Read zip files name under specific folders key:"folder_zip" and key:"folder_zip_backup"    
    local_readConfig_readjson.get_list_zip_folder_folderbackup()

    # Read zip files name under specific folders key:"folder_zip"
    local_readConfig_readjson.get_list_zipfiles_under_zip_folders()    

    opt_verbose='ON'
    #opt_verbose='OFF'
    
    ## Upolad zip files to Google Driver
    str_client_credentials = 'client_secrets_zipupload.json'
    str_dir_client_credentials = os.path.join(strdirname,str_client_credentials)
    print(str_dir_client_credentials)

    localgoogle_drive = google_drive.GoogleCloudDrive()
    gauth = localgoogle_drive.GDriveAuth(str_client_credentials)
    
    #Make GoogleDrive instance with Authenticated GoogleAuth instance
    drive = GoogleDrive(gauth)



    ## Move zip files to key:"folder_zip_backup"

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     