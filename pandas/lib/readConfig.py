import os
import codecs
import configparser

#proDir=os.path.split(os.path.realpath(__file__))[0]
#configPath=os.path.join(proDir,"config.ini")

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

    def get_StockIdxInfo(self, name):
        value=self.cf.get("StockIdxInfo", name)
        return value

    def get_GSpread(self, name):
        value = self.cf.get("GSpredSheet", name)
        return value

    def get_GDrive(self, name):
        value = self.cf.get("GDrive", name)
        return value
        
    def get_WorkSheet_Amy1210(self,name):
        value = self.cf.get("WorkSheet_Amy1210", name)
        return value

    def get_SeymourExcel(self,name):
        value = self.cf.get("SeymourExcel", name)
        return value

    def get_MongoDB(self, name):
        value = self.cf.get("MONGODB", name)
        return value    