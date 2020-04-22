# -*- coding: utf-8 -*-
import os,sys
import re
import zipfile
import glob
from logger import logger

def unzip(filename):
    list_Of_FileNames = []

    with zipfile.ZipFile(filename, "r") as zf:
        zf.extractall(path=os.path.dirname(filename))
        
        list_Of_FileNames = zf.namelist()

        #showFileNames_InZipFile_zip(list_Of_FileNames)

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

# Contend of ret_list_ZipFolderFileNames
'''
202003051550/
202003051550/chariotlog.txt
202003051550/P0-Client1_Bidirectional_result_1st.csv
202003051550/P0-Client1_Bidirectional_result_1st.tst
202003051550/P0-Client1_Rx_result_1st.csv
202003051550/P0-Client1_Rx_result_1st.tst
202003051550/P0-Client1_Tx_result_1st.csv
202003051550/P0-Client1_Tx_result_1st.tst    
'''
def parse_ZipFolder_TxtCsvFiles(re_pattern,list_ZipFolderFileNames):
    ret_list = []
    
    #msg = "list_ZipFolderFileNames:{} in parse_ZipFolder_TxtCsvFiles"
    #logger.info(msg.format(list_ZipFolderFileNames))

    for zipfolderfilename in list_ZipFolderFileNames:
        if re.search(re_pattern, zipfolderfilename):
            ret_list.append(zipfolderfilename)
            
    #msg = "ret_list:{} in parse_ZipFolder_TxtCsvFiles"
    #logger.info(msg.format(ret_list))

    return ret_list

# Get below contens
'''
202003051550/
202003051550/chariotlog.txt
202003051550/P0-Client1_Bidirectional_result_1st.csv
202003051550/P0-Client1_Rx_result_1st.csv
202003051550/P0-Client1_Tx_result_1st.csv
'''
def get_ZipFolder_TxtCsvFiles(list_ZipFolderFileNames):
    # filter by regular expression 
    re_exp_zipfolder = r'\/$'
    re_exp_txtfile = r'\.txt$'
    re_exp_csvfile = r'\.csv$'

    list_zipfolder = parse_ZipFolder_TxtCsvFiles(re_exp_zipfolder, list_ZipFolderFileNames)
    list_txtfiles = parse_ZipFolder_TxtCsvFiles(re_exp_txtfile, list_ZipFolderFileNames)
    list_csvfiles = parse_ZipFolder_TxtCsvFiles(re_exp_csvfile, list_ZipFolderFileNames)
    
    #re_list_zipfolder_txtfiles_csvfiles = list_txtfiles + list_csvfiles
    re_list_zipfolder_txtfiles_csvfiles = list_zipfolder + list_txtfiles + list_csvfiles

    return re_list_zipfolder_txtfiles_csvfiles

'''
http://wiki.alarmchang.com/index.php?title=Python_%E4%BD%BF%E7%94%A8_zipfile_%E5%B0%87%E6%95%B4%E5%80%8B%E7%9B%AE%E9%8C%84%E9%83%BD%E5%A3%93%E8%B5%B7%E4%BE%86
'''

def Achive_Folder_To_ZIP(sFilePath, dest = ""):
    """
    input : Folder path and name
    output: using zipfile to ZIP folder
    """
    if (dest == ""):
        zf = zipfile.ZipFile(sFilePath + '.ZIP', mode='w')
    else:
        zf = zipfile.ZipFile(dest, mode='w')
 
    #os.chdir(sFilePath)
    #print sFilePath
    msg = "sFilePath:{}"
    logger.info(msg.format(sFilePath))

    strdirname=os.path.dirname(sFilePath)
    strbasename=os.path.basename(sFilePath)
    #msg = "strdirname:{}"
    #logger.info(msg.format(strdirname))
    #msg = "strbasename:{}"
    #logger.info(msg.format(strbasename))
    
    os.chdir(strdirname)

    msg = "Achive_Folder:{}.zip"
    logger.info(msg.format(sFilePath))

    #for root, folders, files in os.walk(".\\"):
    for root, folders, files in os.walk( os.path.join('.', strbasename) ):
        for sfile in files:
            '''Achive_Folder_To_ZIP:.\Client1-W1_Bidirectional_result_1st.csv'''
            #aFile = os.path.join(root, sfile)
            aFile = os.path.join(strbasename, sfile)

            #print aFile
            #msg = "Achive_Folder_To_ZIP:{}"
            #logger.info(msg.format(aFile))

            zf.write(aFile)
    zf.close()    

def Achive_noFolder_To_ZIP(sFilePath, dest = ""):
    """
    input : Folder path and name
    output: using zipfile to ZIP folder
    """
    if (dest == ""):
        zf = zipfile.ZipFile(sFilePath + '.ZIP', mode='w')
    else:
        zf = zipfile.ZipFile(dest, mode='w')
 
    #os.chdir(sFilePath)
    #print sFilePath
    msg = "Achive_Folder:{}.zip"
    logger.info(msg.format(sFilePath))

    for root, folders, files in os.walk(sFilePath):
        for sfile in files:
            aFile = os.path.join(root, sfile)
            #print aFile
            msg = "Achive_Folder_To_ZIP:{}"
            logger.info(msg.format(aFile))

            zf.write(aFile)
    zf.close()

def get_list_Folder_under_Directory(targetPath):
    list_folders = []

    if os.path.isdir(targetPath):
        for root, folders, files in os.walk(targetPath):            
            for folder in folders:
                list_folders.append(folder)
    
    for folder in list_folders:
        msg = "folder:{} under Target Path:{}"
        logger.info(msg.format(folder, targetPath))

    msg = "{} folders under Target Path:{}"
    logger.info(msg.format(len(list_folders), targetPath))
    
    return list_folders    
