from _libs.logger_setup import *
from _libs.yahooFinance import *
from _libs.lib_misc import *
from _libs.stock import *

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

    def update_sheet_celllist(self, row_count, str_cellrange, list_cellvalue):
        # print("Cell Range string:", str_cellrange)
        cell_list = self.gss_client_worksheet.range(str_cellrange)

        '''
        update_cells throwing AttributeError for simple update #483 
        https://github.com/burnash/gspread/issues/483 
        # 2018/8/12 Solve by issue:483; 
        '''
        '''
        Exception requests.exceptions.JSONDecodeError is raised in APIError constructor #1504 
        https://github.com/burnash/gspread/issues/1504  Aug 9
        
        make next release #1516  May 18 2024    
        https://github.com/burnash/gspread/issues/1516
        '''        
        cell_list[0].value = list_cellvalue[0]
        cell_list[1].value = list_cellvalue[1]
        cell_list[2].value = list_cellvalue[2]
        cell_list[3].value = list_cellvalue[3]
        cell_list[4].value = list_cellvalue[4]
        # print("cell_list:", cell_list)
        self.gss_client_worksheet.update_cells(cell_list)
        
        # With label
        str_cmp_name = self.gss_client_worksheet.get('a{}'.format(row_count)).first()
        #logger.info(f"label C1: {val}")
        
        logger.info(f'Update Company: {str_cmp_name}, MA_Status: {list_cellvalue[0]},Close: {list_cellvalue[1]}, Open: {list_cellvalue[2]}, High: {list_cellvalue[3]}, Low: {list_cellvalue[4]}')
    
    # Checking if a number is prime
    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False            
        return True
        
    def     update_GSpreadworksheet_from_yfiances(self, row_count, str_delay_sec, local_pt_stock):
        list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
            
        while len(list_Gworksheet_rowvalue) > 0:
            stkidx = str(list_Gworksheet_rowvalue[1])
            if self.opt_verbose.lower() == 'on':
                logger.info(f'stock index from Google sheet: {stkidx}')
            
            local_pt_stock.check_twse_tpex_us_stocks(stkidx)            
            logger.info(f"stock_id: {stkidx} == ticker: {local_pt_stock.ticker}")     
    
            # delay delay_sec secs
            # 2018/8/13 prevent ErrorCode:429, Exhaust Resoure
            #print ("Delay ", str_delay_sec, "secs to prevent Google Error Code:429, Exhaust Resoure")
            #time.sleep(float(str_delay_sec))
            local_stock_indicator = stock_indicator(ticker=local_pt_stock.ticker)
            
            if bool(re.match('[1-9][0-9][0-9][0-9].T(W|WO)$', local_pt_stock.ticker)):
                if self.is_prime(int(stkidx)):
                    random_timer(0, int(str_delay_sec))
                    logger.info(f'prime: {int(stkidx)}')                 
                
            local_stock_indicator.check_MAs_status()            
            local_stock_indicator.filter_MAs_status()
            
            ''' reduce yahoo finance request
            dict_stock_OHLC= get_asset_from_yfinance_ticker(local_pt_stock.ticker, self.opt_verbose)
            stock_price_final = str(dict_stock_OHLC['close'])
            stock_price_open = str(dict_stock_OHLC['open'])
            stock_price_high = str(dict_stock_OHLC['high'])
            stock_price_low = str(dict_stock_OHLC['low'])
            '''
            stock_price_final = str(local_stock_indicator.close)
            
            # update by Cell Range
            #str_range = 'D' + str(row_count) + ":" + 'G' + str(row_count)
            str_range = 'C' + str(row_count) + ":" + 'G' + str(row_count)

            ## update cell content
            #2018/08/22 if final price doesn't exist    
            if bool(re.match(r'^-+-$',stock_price_final)) == False:
                # add stock MA status
                list_cellvalue = [local_stock_indicator.stock_MA_status,
                                  '{:.2f}'.format(float(local_stock_indicator.close)) , '{:.2f}'.format(float(local_stock_indicator.open)),
                                  '{:.2f}'.format(float(local_stock_indicator.high)), '{:.2f}'.format(float(local_stock_indicator.low)) ]
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'list_cellvalue: {list_cellvalue}')
                
                self.update_sheet_celllist(row_count, str_range, list_cellvalue)
            
            # delay delay_sec secs
            random_timer(1, 2)
                        
            row_count += 1
            list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
            
    def update_GSpreadworksheet_from_pstock(self, row_count, str_delay_sec, local_pt_stock):
        list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
        start_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        end_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        
        while len(list_Gworksheet_rowvalue) > 0:
            stkidx = str(list_Gworksheet_rowvalue[1])
            if self.opt_verbose.lower() == 'on':
                logger.info(f'stock index from Google sheet: {stkidx}')
            
            local_pt_stock.check_twse_tpex_us_stocks(stkidx)            
            logger.info(f"stock_id: {stkidx} == ticker: {local_pt_stock.ticker}")             
            target_ticker = local_pt_stock.ticker
           # for random timer purpose
            if bool(re.match('[1-9][0-9][0-9][0-9].T(W|WO)$', target_ticker)):
                
                local_stock_indicator = stock_indicator_pstock(ticker=target_ticker, interval="1d", \
                                                                startdate= start_date, enddate= end_date)
                
                if self.is_prime(int(local_pt_stock.ticker.split('.')[0])):
                    random_timer(0, float(str_delay_sec))
                    logger.info(f'prime: {int(stkidx)}') 
                    #logger.info(f'prime: {int(target_ticker.split(".")[0])}')                 
                    
                local_stock_indicator.pstock_interval_startdate_enddate()
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'local_stock_indicator.stock_data: \n{local_stock_indicator.stock_data}')
                    
                             
                