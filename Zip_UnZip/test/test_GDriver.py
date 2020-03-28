
import json
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
import readConfig 

json_file='config.json'
opt_verbose='ON'
#opt_verbose='OFF'

# Read zip files name under specific folders key:"folder_zip"
# Read column name from df to act as key
local_readConfig_readjson = readConfig.ReadJSON(json_file,opt_verbose)
local_readConfig_readjson.get_list_zip_folder_folderbackup()

local_readConfig_readjson.get_list_zipfiles_under_zip_folders()

## Upolad zip files to Google Driver
## Move zip files to key:"folder_zip_backup"