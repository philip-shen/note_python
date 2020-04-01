import os,sys,time
import codecs
import configparser
import json
import pandas as pd
from logger import logger
import re


class ReadConfig:
    def __init__(self,configPath):
        self.configPath=configPath

        #fd = open(self.configPath)
        fd = open(self.configPath, encoding='utf-8')
        data = fd.read()
        
        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        #self.cf.read(self.configPath)
        self.cf.read(self.configPath,encoding='utf-8')

    def get_Server_Param(self, name):
        value = self.cf.get("Server_Param", name)
        return value
    
    def get_Client_Param(self, name):
        value = self.cf.get("Client_Param", name)
        return value

class ReadJSON:
    def __init__(self, path_json_file, opt_verbose='OFF'):
        self.path_json_file = path_json_file
        self.opt_verbose = opt_verbose

        try:
            with open(self.path_json_file) as f:
                data = json.load(f)

            df = pd.DataFrame(data)
            self.df = df

            if self.opt_verbose.lower() == "on":
                msg = "self.df: {}"
                logger.info(msg.format(self.df))

        except IOError:
            msg = 'IOError: Couldn\'t open: {}'
            logger.info(msg.format(self.path_json_file))        

    def get_list_zip_folder_folderbackup(self):
        
        list_path_zip_folder = []
        list_path_zip_folder_backup = []
        # Read column name from df to act as key
        # https://stackoverflow.com/questions/19482970/get-list-from-pandas-dataframe-column-headers/19483602#19483602
        ##############################################
        for column_name in self.df.columns.values.tolist():
            # Python os.path.join() on a list
            #https://stackoverflow.com/questions/14826888/python-os-path-join-on-a-list
            #os.path.join("c:/","home","foo","bar","some.txt")
            path_zip_folder = os.path.join(self.df[column_name][0]["driver"], 
                                            self.df[column_name][0]["folder"], 
                                            self.df[column_name][0]["folder_zip"])

            path_zip_folder_backup = os.path.join(self.df[column_name][0]["driver"], 
                                            self.df[column_name][0]["folder"], 
                                            self.df[column_name][0]["folder_zip_backup"])

            list_path_zip_folder.append(path_zip_folder)
            list_path_zip_folder_backup.append(path_zip_folder_backup)

            if self.opt_verbose.lower() == "on":
                msg = "path_zip_folder: {}"
                logger.info(msg.format(path_zip_folder))
                msg = "path_zip_folder_backup: {}"
                logger.info(msg.format(list_path_zip_folder_backup))

        #if self.opt_verbose.lower() == "on":
        msg = "list_path_zip_folder: {}"
        logger.info(msg.format(list_path_zip_folder))
        msg = "list_path_zip_folder_backup: {}"
        logger.info(msg.format(list_path_zip_folder_backup))

        '''
        list_path_zip_folder: ['f:/ChamberWirelessPerformanceTest\\TestResultTemp', 
        'f:/DHCPNATThroughputTest\\TestResultTemp', 'f:/L2TPNATThroughputTest\\TestResultTemp', 
        'f:/PPPOENATThroughputTest\\TestResultTemp', 'f:/PPTPNATThroughputTest\\TestResultTemp', 
        'f:/STATICIPNATThroughputTest\\TestResultTemp']

        list_path_zip_folder_backup: ['f:/ChamberWirelessPerformanceTest\\The latest Test Result', 
        'f:/DHCPNATThroughputTest\\The latest Test Result', 'f:/L2TPNATThroughputTest\\The latest Test Result', 
        'f:/PPPOENATThroughputTest\\The latest Test Result', 'f:/PPTPNATThroughputTest\\The latest Test Result', 
        'f:/STATICIPNATThroughputTest\\The latest Test Result']
        '''
        self.list_path_zip_folder = list_path_zip_folder
        self.list_path_zip_folder_backup = list_path_zip_folder_backup

        return list_path_zip_folder, list_path_zip_folder_backup
    
    def parse_ZipFolder_Files(self,re_pattern,list_path_zipfolder):
        ret_list = []        

        for path_zipfolder in list_path_zipfolder:
            # check if folder or not
            if os.path.isdir(path_zipfolder):

                if self.opt_verbose.lower() == "on":
                    msg = "path_zipfolder: {}"
                    logger.info(msg.format(path_zipfolder))

                #get zip files under folder
                for filename in os.listdir(path_zipfolder):
                    if re.search(re_pattern, filename):
                        ret_list.append(os.path.join(path_zipfolder,filename)) 

                    if self.opt_verbose.lower() == "on":
                        msg = "parse_ZipFolder_Files: {}"
                        logger.info(msg.format(os.path.join(path_zipfolder,filename)))
        
        return ret_list

    def get_list_zipfiles_under_zip_folders(self):    
        re_exp_zipfile = r'\.zip$'
        list_zipfiles_under_zip_folders = []

        '''
        bouble nested list

        list_zipfiles_under_zip_folders: 
        [['f:/ChamberWirelessPerformanceTest\\TestResultTemp\\5G_DIR-1750_v1.01b08_MacBook.zip', 'f:/ChamberWirelessPerformanceTest\\TestResultTemp\\2-4G_DIR-1750_v1.01b08_AC88.zip'], 
        ['f:/DHCPNATThroughputTest\\TestResultTemp\\DHCP_DIR-1750_1.01b08__AX200.zip', 'f:/DHCPNATThroughputTest\\TestResultTemp\\DHCP_DIR-1750_1.01b08__AC8260.zip'], 
        ['f:/L2TPNATThroughputTest\\TestResultTemp\\L2TP_v1.00b11_Macbook.zip', 'f:/L2TPNATThroughputTest\\TestResultTemp\\L2TP_DIR-1750_1.01b08_5G.zip'], 
        ['f:/PPPOENATThroughputTest\\TestResultTemp\\PPPoE_DIR1750_v1.01b08_MacBook.zip', 'f:/PPPOENATThroughputTest\\TestResultTemp\\PPPoE_DIR1750_v1.01b08_AX200.zip'], 
        ['f:/PPTPNATThroughputTest\\TestResultTemp\\PPTP_DIR-1750_1.01b08_AC8260.zip', 'f:/PPTPNATThroughputTest\\TestResultTemp\\PPTP_DIR-1750_1.01b08_AC88.zip'], 
        ['f:/STATICIPNATThroughputTest\\TestResultTemp\\StaticIP_DIR1750_v1.01b08_AX200.zip', 'f:/STATICIPNATThroughputTest\\TestResultTemp\\StaticIP_DIR1750_v1.01b08_AC8260.zip']]
        '''
        #for path_zip_folder in self.list_path_zip_folder:
            # check if folder or not
        #    if os.path.isdir(path_zip_folder):
                
        #        if self.opt_verbose.lower() == "on":
        #            msg = "path_zip_folder: {}"
        #            logger.info(msg.format(path_zip_folder))

                #get zip files under folder
        #       ret_list = self.parse_ZipFolder_Files(re_exp_zipfile, path_zip_folder)

        #       list_zipfiles_under_zip_folders.append(ret_list)

        #self.list_zipfiles_under_zip_folders = list_zipfiles_under_zip_folders
        
        '''        
        list_zipfiles_under_zip_folders: 
        ['f:/ChamberWirelessPerformanceTest\\TestResultTemp\\5G_DIR-1750_v1.01b08_MacBook.zip', 'f:/ChamberWirelessPerformanceTest\\TestResultTemp\\2-4G_DIR-1750_v1.01b08_AC88.zip', 
        'f:/DHCPNATThroughputTest\\TestResultTemp\\DHCP_DIR-1750_1.01b08__AX200.zip', 'f:/DHCPNATThroughputTest\\TestResultTemp\\DHCP_DIR-1750_1.01b08__AC8260.zip', 
        'f:/L2TPNATThroughputTest\\TestResultTemp\\L2TP_v1.00b11_Macbook.zip', 'f:/L2TPNATThroughputTest\\TestResultTemp\\L2TP_DIR-1750_1.01b08_5G.zip', 
        'f:/PPPOENATThroughputTest\\TestResultTemp\\PPPoE_DIR1750_v1.01b08_MacBook.zip', 'f:/PPPOENATThroughputTest\\TestResultTemp\\PPPoE_DIR1750_v1.01b08_AX200.zip',
        'f:/PPTPNATThroughputTest\\TestResultTemp\\PPTP_DIR-1750_1.01b08_AC8260.zip', 'f:/PPTPNATThroughputTest\\TestResultTemp\\PPTP_DIR-1750_1.01b08_AC88.zip', 
        'f:/STATICIPNATThroughputTest\\TestResultTemp\\StaticIP_DIR1750_v1.01b08_AX200.zip', 'f:/STATICIPNATThroughputTest\\TestResultTemp\\StaticIP_DIR1750_v1.01b08_AC8260.zip']
        '''
        #get zip files under folder
        self.list_zipfiles_under_zip_folders = self.parse_ZipFolder_Files(re_exp_zipfile, self.list_path_zip_folder)
        
        #self.list_zipfiles_under_zip_folders = list_zipfiles_under_zip_folders

        #if self.opt_verbose.lower() == "on":
        msg = "list_zipfiles_under_zip_folders: {}"
        logger.info(msg.format(self.list_zipfiles_under_zip_folders))        
