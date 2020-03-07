# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import glob
from logger import logger

def unzip(filename):
    list_Of_FileNames = []

    with zipfile.ZipFile(filename, "r") as zf:
        zf.extractall(path=os.path.dirname(filename))
        
        list_Of_FileNames = zf.namelist()

    #delete_zip(filename)
    return list_Of_FileNames

def listOfFileNames_zip(zipObj):
    list_Of_FileNames = zipObj.namelist()

    return list_Of_FileNames    

def showFileNames_InZipFile_zip(list_FileNames):

    # Iterate over the file names
    for fileName in list_FileNames:
        #print("fileName of listOfFileNames: {}".format(fileName))
        msg = "fileName of listOfFileNames: {}"
        logger.info(msg.format(fileName))

def delete_zip(zip_file):
    os.remove(zip_file)


def walk_in_dir(dir_path):
    ret_listOfFileNames = []

    for filename in glob.glob(os.path.join(dir_path, "*.zip")):
        #print("filename: {}".format(filename))
        listOfFileNames = []

        msg = "fileName:{} in directory:{}"
        logger.info(msg.format(filename, dir_path))

        listOfFileNames = unzip(filename=os.path.join(dir_path,filename))
        #listOfFileNames = listOfFileNames_zip(ret_Objzip)

        showFileNames_InZipFile_zip(listOfFileNames)
        ret_listOfFileNames = ret_listOfFileNames.append(listOfFileNames)

    for dirname in (d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))):
        walk_in_dir(os.path.join(dir_path, dirname))
    
    return ret_listOfFileNames