from .logger_setup import *
#from .yahooFinance import *

import time,re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSS:
    def __init__(self, gs_json, config_json, opt_verbose='OFF'):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(gs_json, scope)
        #key = SAC.from_json_keyfile_name(gs_json, scopes)
        self.gc = gspread.authorize(credentials)        
        self.config_json = config_json
        self.opt_verbose = opt_verbose
        
    def open_GSworksheet(self, gspread_sheet, work_sheet):
        gss_client_worksheet = self.gc.open(gspread_sheet).worksheet(work_sheet)
        self.gss_client_worksheet=gss_client_worksheet    

    def get_stkidx_cnpname(self, row_count, str_delay_sec):
        list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
        list_stkidx_cnpname = []
        
        while len(list_Gworksheet_rowvalue) > 0:
            cnpname = str(list_Gworksheet_rowvalue[0])
            stkidx = str(list_Gworksheet_rowvalue[1])
            if self.opt_verbose.lower() == 'on':
                logger.info(f'company name: {cnpname} stock index: {stkidx} from Google sheet')

            temp_dict = {
                'stkidx': stkidx,
                'cnpname': cnpname
            }
            list_stkidx_cnpname.append(temp_dict)
            # delay delay_sec secs
            # 2018/8/13 prevent ErrorCode:429, Exhaust Resoure
            #print ("Delay ", str_delay_sec, "secs to prevent Google Error Code:429, Exhaust Resoure")
            time.sleep(int(str_delay_sec))
            
            row_count += 1
            list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
        
        self.list_stkidx_cnpname_dicts = list_stkidx_cnpname
            
    def update_sheet_celllist(self, row_count, str_cellrange, list_cellvalue):
        # print("Cell Range string:", str_cellrange)
        cell_list = self.gss_client_worksheet.range(str_cellrange)

        # 2018/8/12 Solve by issue:483; https://github.com/burnash/gspread/issues/483
        # cell_list[0].value = stock_price_final
        # cell_list[1].value = stock_price_open
        # cell_list[2].value = stock_price_high
        # cell_list[3].value = stock_price_low

        cell_list[0].value = list_cellvalue[0]
        cell_list[1].value = list_cellvalue[1]
        cell_list[2].value = list_cellvalue[2]
        cell_list[3].value = list_cellvalue[3]
        # print("cell_list:", cell_list)
        self.gss_client_worksheet.update_cells(cell_list)
        
        # With label
        str_cmp_name = self.gss_client_worksheet.get('a{}'.format(row_count)).first()
        #logger.info(f"label C1: {val}")
        
        logger.info(f'Update Company: {str_cmp_name}, Close: {list_cellvalue[0]}, Open: {list_cellvalue[1]}, High: {list_cellvalue[2]}, Low: {list_cellvalue[3]}')
        
    def update_GSpreadworksheet_from_yfiances(self, row_count, str_delay_sec):
        list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
        
        while len(list_Gworksheet_rowvalue) > 0:
            stkidx = str(list_Gworksheet_rowvalue[1])
            if self.opt_verbose.lower() == 'on':
                logger.info(f'stock index from Google sheet: {stkidx}')
            
            # delay delay_sec secs
            # 2018/8/13 prevent ErrorCode:429, Exhaust Resoure
            #print ("Delay ", str_delay_sec, "secs to prevent Google Error Code:429, Exhaust Resoure")
            time.sleep(int(str_delay_sec))

            dict_stock_OHLC= get_asset_from_yfinance_ticker(self.config_json, stkidx, self.opt_verbose)
            stock_price_final = str(dict_stock_OHLC['close'])
            stock_price_open = str(dict_stock_OHLC['open'])
            stock_price_high = str(dict_stock_OHLC['high'])
            stock_price_low = str(dict_stock_OHLC['low'])
            
            # update by Cell Range
            str_range = 'D' + str(row_count) + ":" + 'G' + str(row_count)

            ## update cell content
            #2018/08/22 if final price doesn't exist    
            if bool(re.match(r'^-+-$',stock_price_final)) == False:
                list_cellvalue = ['{:.2f}'.format(float(stock_price_final)) , '{:.2f}'.format(float(stock_price_open)),
                                  '{:.2f}'.format(float(stock_price_high)), '{:.2f}'.format(float(stock_price_low)) ]
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'list_cellvalue: {list_cellvalue}')
                
                self.update_sheet_celllist(row_count, str_range, list_cellvalue)
            
            # delay delay_sec secs
            time.sleep(int(str_delay_sec))
            
            row_count += 1
            list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)