from .logger_setup import *
from .yahooFinance import *

import time,re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSS:
    def __init__(self, gs_json, config_json):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(gs_json, scope)
        #key = SAC.from_json_keyfile_name(gs_json, scopes)
        self.gc = gspread.authorize(credentials)        
        self.config_json = config_json
        
    def open_GSworksheet(self, gspread_sheet, work_sheet):
        gss_client_worksheet = self.gc.open(gspread_sheet).worksheet(work_sheet)
        self.gss_client_worksheet=gss_client_worksheet    

    def update_GSpreadworksheet_from_yfiances(self,row_count, str_delay_sec):
        list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
        
        while len(list_Gworksheet_rowvalue) > 0:
            stkidx = str(list_Gworksheet_rowvalue[1])
            logger.info(f'stock index from Google sheet: {stkidx}')
            
            # delay delay_sec secs
            # 2018/8/13 prevent ErrorCode:429, Exhaust Resoure
            #print ("Delay ", str_delay_sec, "secs to prevent Google Error Code:429, Exhaust Resoure")
            time.sleep(int(str_delay_sec))

            get_asset_from_yfinance_ticker(self.config_json, stkidx)
            
            row_count += 1
            list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)