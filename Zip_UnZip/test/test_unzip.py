# -*- coding: utf-8 -*-
import os,sys
import time

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
            ret_listOfFileNames = walk_in_dir(args[1])
            print(ret_listOfFileNames)
            #showFileNames_InZipFile_zip(ret_listOfFileNames)

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