# 2020/04/12 Initial 
######################################################

'''
http://wiki.alarmchang.com/index.php?title=Python_%E4%BD%BF%E7%94%A8_zipfile_%E5%B0%87%E6%95%B4%E5%80%8B%E7%9B%AE%E9%8C%84%E9%83%BD%E5%A3%93%E8%B5%B7%E4%BE%86
'''

import zipfile
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


 
 
if __name__ == "__main__":
    t0 = time.time()

    args = sys.argv
    try:
        if(os.path.isdir(args[1])):
            targetPath = args[1]  
            
            list_folder_under_targetPath = \
                get_list_Folder_under_Directory(targetPath)

            for folder_under_targetPath in list_folder_under_targetPath:
                #"d:\project\DIR1950\Chariot_Thruput\v1.01b12_toDLab\202004081607" 
                Achive_Folder_To_ZIP(os.path.join(targetPath,folder_under_targetPath), \
                   #"d:\project\DIR1950\Chariot_Thruput\v1.01b12_toDLab\202004081607.zip" 
                   "{}\{}.zip".format(targetPath, folder_under_targetPath) )

    except IndexError:
        print('IndexError: Usage "python %s DIR_NAME"' % ( args[0]))
    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))        