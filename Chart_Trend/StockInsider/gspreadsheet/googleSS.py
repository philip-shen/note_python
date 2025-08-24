from insider.logger_setup import *
from gspreadsheet.yahooFinance import *
from gspreadsheet.lib_misc import *
from gspreadsheet.stock import *
#from insider.stock import stock_indicator_pstock

import sys, time, re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSS:
    def __init__(self, gs_json, json_data ,opt_verbose='OFF'):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(gs_json, scope)
        #key = SAC.from_json_keyfile_name(gs_json, scopes)
        self.gc = gspread.authorize(credentials)
        self.json_data = json_data        
        self.opt_verbose = opt_verbose
        
        str_start_date = self.json_data["start_end_date"][0][0]
        str_end_date = self.json_data["start_end_date"][0][-1]
        logger.info(f"start_date: {str_start_date}; end_date: {str_end_date}")
        str_end_date = self.prev_next_date(str_end_date)[-1]#casue available end_date = end_data+1 
        
        self.start_date = datetime(int(str_start_date[:4]), int(str_start_date[4:6]), int(str_start_date[6:]))
        self.end_date =  datetime(int(str_end_date[:4]), int(str_end_date[4:6]), int(str_end_date[6:]))
        
    def open_GSworksheet(self, gspread_sheet, work_sheet):
        gss_client_worksheet = self.gc.open(gspread_sheet).worksheet(work_sheet)
        self.gss_client_worksheet=gss_client_worksheet    

    def get_stkidx_cnpname(self, row_count, list_delay_sec):
        list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
        list_stkidx_cnpname = []        
        dict_worksheet_spread = self.json_data["dict_worksheet_gSpredSheet"]
        
        if bool(re.match('^twse', self.json_data["lastest_datastr_twse_tpex"][3].lower())  ):
            worksheet_spread = dict_worksheet_spread["twse"]
        elif bool(re.match('^sp500', self.json_data["lastest_datastr_twse_tpex"][3].lower())  ):
            worksheet_spread = dict_worksheet_spread["sp500"]
        elif bool(re.match('^nasdaq100', self.json_data["lastest_datastr_twse_tpex"][3].lower())  ):
            worksheet_spread = dict_worksheet_spread["nasdaq100"]
        elif bool(re.match('^twse_etf', self.json_data["lastest_datastr_twse_tpex"][3].lower())  ):
            worksheet_spread = dict_worksheet_spread["twse_etf"]
                
        while len(list_Gworksheet_rowvalue) > 0:
            cnpname = str(list_Gworksheet_rowvalue[0])
            stkidx = str(list_Gworksheet_rowvalue[1])
            if self.opt_verbose.lower() == 'on':
                #logger.info(f'company name: {cnpname} stock index: {stkidx} from Google sheet: {self.json_data["gSpredSheet"]}')
                logger.info(f'company name: {cnpname} stock index: {stkidx} from Google sheet: {worksheet_spread}')

            temp_dict = {
                'stkidx': stkidx,
                'cnpname': cnpname
            }
            list_stkidx_cnpname.append(temp_dict)
            # delay delay_sec secs
            # 2018/8/13 prevent ErrorCode:429, Exhaust Resoure
            #print ("Delay ", str_delay_sec, "secs to prevent Google Error Code:429, Exhaust Resoure")
            #time.sleep(int(str_delay_sec))
            # delay delay_sec secs
            #random_timer(0, 0)
            
            row_count += 1
            try:
                list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
            except Exception as e:
                logger.info(f'Error: {e}')
                sys.exit(0)
            
        
        self.list_stkidx_cnpname_dicts = list_stkidx_cnpname
        
    def update_sheet_celllist(self, row_count, str_cellrange, list_cellvalue):
        # print("Cell Range string:", str_cellrange)
        try:                
            cell_list = self.gss_client_worksheet.range(str_cellrange)
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)
        
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
        for idx, cellvalue in enumerate(list_cellvalue):
            #logger.info(f'cell_list[{idx}].value= {cellvalue}')
            cell_list[idx].value = cellvalue
            #logger.info(f'cell_list[{idx}].value= {cell_list[idx].value}')
            
        try:
            self.gss_client_worksheet.update_cells(cell_list)
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)
        
        # With label
        try:
            str_cmp_name = self.gss_client_worksheet.get('a{}'.format(row_count)).first()
            #logger.info(f"label C1: {val}")
            #logger.info(f'Update cell_list:\n{cell_list}')
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)
        
    # Checking if a number is prime
    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False            
        return True
        
    def update_GSpreadworksheet_from_yfiances(self, row_count, list_delay_sec, local_pt_stock):
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
            
            #if bool(re.match('[1-9][0-9][0-9][0-9].T(W|WO)$', local_pt_stock.ticker)):
                #if self.is_prime(int(stkidx)):
                #    random_timer(0, list_delay_sec[-1])
                #    logger.info(f'prime: {int(stkidx)}')                 
                
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
            random_timer(list_delay_sec[0], list_delay_sec[-1])
            logger.info(f'row_count: {row_count}')
            
            row_count += 1                
            try:                
                list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
            except Exception as e:
                logger.info(f'Error: {e}')
                sys.exit(0)
    
    def update_GSpreadworksheet_yfiances_batch_update(self, inital_row_num, list_delay_sec, local_pt_stock):
        try:                
            self.get_stkidx_cnpname(inital_row_num, list_delay_sec)
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)
            
        twse_tpex_idx = ''
        list_all_stkidx_row_value = []
        
        for dict_stkidx_cnpname in self.list_stkidx_cnpname_dicts:     
                       
            if dict_stkidx_cnpname["stkidx"] is None:
                #twse_two_idx = "^TWII"
                twse_tpex_idx = dict_stkidx_cnpname["stkidx"]     
            else:
                twse_tpex_idx = dict_stkidx_cnpname["stkidx"]  
            
            #if bool(re.match('^2464', dict_stkidx_cnpname["stkidx"]) ):
            #        continue 
                
            local_pt_stock.check_twse_tpex_us_stocks(twse_tpex_idx)            
            logger.info(f"stock_id: {twse_tpex_idx} == ticker: {local_pt_stock.ticker}; cnp_name:{dict_stkidx_cnpname['cnpname']}")         
            
            local_stock_indicator = stock_indicator(ticker=local_pt_stock.ticker)
            local_stock_indicator.check_MAs_status()            
            local_stock_indicator.filter_MAs_status()
                            
            stock_price_final = str(local_stock_indicator.close)
            
            ## get each stkidx row value 
            if bool(re.match(r'^-+-$',stock_price_final)) == False:
                # add stock MA status
                list_cellvalue = [local_stock_indicator.stock_MA_status,
                                  '{:.2f}'.format(float(local_stock_indicator.close)) , '{:.2f}'.format(float(local_stock_indicator.open)),
                                  '{:.2f}'.format(float(local_stock_indicator.high)), '{:.2f}'.format(float(local_stock_indicator.low)) ]
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'list_cellvalue: {list_cellvalue}')

                list_all_stkidx_row_value.append(list_cellvalue)
        
        logger.info(f'len of list_all_stkidx_row_value: {list_all_stkidx_row_value.__len__()}')        
        
        # update by Cell Range
        str_gspread_range = 'C' + str(inital_row_num) + ":" + \
                            'G' + str(inital_row_num + self.list_stkidx_cnpname_dicts.__len__()-1)
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'list_all_stkidx_row_value: {list_all_stkidx_row_value}')
            logger.info(f'str_gspread_range: {str_gspread_range}')
        
        '''
        # Update multiple ranges at once
        worksheet.batch_update([{
                'range': 'A1:B2',
                'values': [['A1', 'B1'], ['A2', 'B2']],
        }, {
                'range': 'J42:K43',
                'values': [[1, 2], [3, 4]],
        }])
        '''
        try:                
            self.gss_client_worksheet.batch_update([
                                        {'range': str_gspread_range,
                                            'values': list_all_stkidx_row_value,
                                        },
                                    ])
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)
            
    '''
    http://yhhuang1966.blogspot.com/2022/09/python-yfinance.html

    download() 參數	 說明
    symbol	 股票代號 (字串), 美股例如  'AMD' (超微), 台股後面要加 '.tw', 例如 '0050.tw'
    start	 起始日期 YYYY-MM-DD (字串), 例如 '2022-08-22'
    end	 結束日期 YYYY-MM-DD (字串), 例如 '2022-09-06', 注意, 不包含此日資料
    period	 期間, 可用 d (日), mo(月), y(年), ytd, max(全部), 例如 5d (5 天), 3mo(三個月) 
    interval	 頻率, 可用 m(分), h(小時), d(日), wk(周), mo(月), 例如 1m(一分線)
    '''
    def prev_next_date(self, date):    
        curr_date_temp = datetime.strptime(date, '%Y%m%d')
        next_date = curr_date_temp + timedelta(days=1)
        next_date = str(next_date)
        prev_date = curr_date_temp - timedelta(days=1) 
        prev_date = str(prev_date)
        '''
        20240909, 
        2024-09-10 00:00:00
        '''    
        #logger.info(f'{date}, {next_date}')
    
        year = next_date[:4]
        #year = str(int(year))
        month = next_date[5:7]
        next_day = next_date[8:10]
        prev_date = prev_date[8:10]
        '''
        2024-09-10 00:00:00, 2024, 09, 10
        '''
        #logger.info(f'{next_date}, {year}, {month}, {next_day}')
    
        return [year+month+prev_date, year+month+next_day] 
        
    def update_GSpreadworksheet_from_pstock(self, row_count, list_delay_sec, local_pt_stock):
        list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
        
        end_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        start_date = self.prev_next_date(end_date)[0]
        
        while len(list_Gworksheet_rowvalue) > 0:
            stkidx = str(list_Gworksheet_rowvalue[1])
            if self.opt_verbose.lower() == 'on':
                logger.info(f'stock index from Google sheet: {stkidx}')
            
            local_pt_stock.check_twse_tpex_us_stocks(stkidx)            
            logger.info(f"stock_id: {stkidx} == ticker: {local_pt_stock.ticker}")             
            target_ticker = local_pt_stock.ticker
            local_stock_indicator_pstock = stock_indicator_pstock(ticker=target_ticker, period='1d', interval='1d', \
                                                                startdate= start_date, enddate= end_date)
            local_stock_indicator_pstock.pstock_interval_period()
            
            # for random timer purpose
            if bool(re.match('[1-9][0-9][0-9][0-9].T(W|WO)$', target_ticker)):                
                #if self.is_prime(int(stkidx)):
                #    random_timer(0, list_delay_sec[-1])
                #    logger.info(f'prime: {int(stkidx)}') 
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'local_stock_indicator.stock_data: \n{local_stock_indicator_pstock.stock_data}')
                
            local_stock_indicator_pstock.check_MAs_status()            
            local_stock_indicator_pstock.filter_MAs_status()    
                             
            stock_price_final = str(local_stock_indicator_pstock.close)
            
            # update by Cell Range
            #str_range = 'D' + str(row_count) + ":" + 'G' + str(row_count)
            str_range = 'C' + str(row_count) + ":" + 'G' + str(row_count)

            ## update cell content
            #2018/08/22 if final price doesn't exist    
            if bool(re.match(r'^-+-$',stock_price_final)) == False:
                # add stock MA status
                list_cellvalue = [local_stock_indicator_pstock.stock_MA_status,
                                  '{:.2f}'.format(float(local_stock_indicator_pstock.close)) , '{:.2f}'.format(float(local_stock_indicator_pstock.open)),
                                  '{:.2f}'.format(float(local_stock_indicator_pstock.high)), '{:.2f}'.format(float(local_stock_indicator_pstock.low)) ]
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'list_cellvalue: {list_cellvalue}')
                
                self.update_sheet_celllist(row_count, str_range, list_cellvalue)
            
            # delay delay_sec secs
            #time.sleep(float('5'))
            random_timer(list_delay_sec[0], list_delay_sec[-1])        
            
            row_count += 1
            list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)    

    def update_GSpreadworksheet_MA_status(self, row_count, list_MA_status):
        list_delay_sec= self.json_data["int_delay_sec"]
        list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)
        if self.opt_verbose.lower() == 'on':
                logger.info(f'list_Gworksheet_rowvalue: {list_Gworksheet_rowvalue}')
                
        while len(list_Gworksheet_rowvalue) > 0:
            str_date = str(list_Gworksheet_rowvalue[0])
            if self.opt_verbose.lower() == 'on':
                logger.info(f'A1 content from Google sheet: {str_date}')
            
            # update by Cell Range
            str_range = 'A' + str(row_count) + ":" + 'AO' + str(row_count)
            
            if self.opt_verbose.lower() == 'on':
                logger.info(f'str_range: {str_range}')
                #logger.info(f'list_MA_status:\n{list_MA_status}')
                
            self.update_sheet_celllist(row_count, str_range, list_MA_status)
            
            # delay delay_sec secs
            #random_timer(list_delay_sec[0], list_delay_sec[-1])        
            
            row_count += 1
            list_Gworksheet_rowvalue = self.gss_client_worksheet.row_values(row_count)    
    '''
    not from star_date to end_date
    '''
    def update_GSpreadworksheet_200MA_plan_batch_update(self, inital_row_num, local_pt_stock):
        list_delay_sec= self.json_data["int_delay_sec"]
        
        try:                
            self.get_stkidx_cnpname(inital_row_num, list_delay_sec)
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)
            
        twse_tpex_idx = ''
        list_all_stkidx_row_value = []    
        
        for dict_stkidx_cnpname in self.list_stkidx_cnpname_dicts:     
                       
            if dict_stkidx_cnpname["stkidx"] is None:
                #twse_two_idx = "^TWII"
                twse_tpex_idx = dict_stkidx_cnpname["stkidx"]     
            else:
                twse_tpex_idx = dict_stkidx_cnpname["stkidx"]  
            
            #if bool(re.match('^2464', dict_stkidx_cnpname["stkidx"]) ):
            #        continue 
                
            local_pt_stock.check_twse_tpex_us_stocks(twse_tpex_idx)            
            logger.info(f"stock_id: {twse_tpex_idx} == ticker: {local_pt_stock.ticker}; cnp_name:{dict_stkidx_cnpname['cnpname']}")         
            
            local_stock_indicator = stock_indicator(ticker=local_pt_stock.ticker, startdate= self.start_date, enddate= self.end_date)
            local_stock_indicator.check_MAs_status()            
            local_stock_indicator.filter_MAs_status()
            
            stock_price_final = str(local_stock_indicator.close)
            
            ## get each stkidx row value 
            if bool(re.match(r'^-+-$',stock_price_final)) == False:
                # add stock MA status
                list_cellvalue = [local_stock_indicator.stock_MA_status,
                                  '{:.2f}'.format(float(local_stock_indicator.close)) , '{:.2f}'.format(float(local_stock_indicator.open)),
                                  '{:.2f}'.format(float(local_stock_indicator.high)), '{:.2f}'.format(float(local_stock_indicator.low)),
                                  '{:.2f}'.format(local_stock_indicator.MA_5),
                                  '{:.2f}'.format(local_stock_indicator.MA_10),
                                  '{:.2f}'.format(local_stock_indicator.MA_20),
                                  '{:.2f}'.format(local_stock_indicator.MA_60),
                                  '{:.2f}'.format(local_stock_indicator.MA_200),]
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'list_cellvalue: {list_cellvalue}')

                list_all_stkidx_row_value.append(list_cellvalue)
        
        logger.info(f'len of list_all_stkidx_row_value: {list_all_stkidx_row_value.__len__()}')        
        
        # update by Cell Range
        str_gspread_range = 'C' + str(inital_row_num) + ":" + \
                            'L' + str(inital_row_num + self.list_stkidx_cnpname_dicts.__len__()-1)
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'list_all_stkidx_row_value:\n{list_all_stkidx_row_value}')
            #logger.info(f'str_gspread_range: {str_gspread_range}')
        
        '''
        # Update multiple ranges at once
        worksheet.batch_update([{
                'range': 'A1:B2',
                'values': [['A1', 'B1'], ['A2', 'B2']],
        }, {
                'range': 'J42:K43',
                'values': [[1, 2], [3, 4]],
        }])
        '''
        try:                
            self.gss_client_worksheet.batch_update([
                                        {'range': str_gspread_range,
                                            'values': list_all_stkidx_row_value,
                                        },
                                    ])
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)
    
    def update_GSpreadworksheet_etf_momentum_batch_update(self, local_dict_MAs_momentum_status, inital_row_num):
        # remark by disable casue below error msg
        # googleSS.py[line:69]- INFO: Error: APIError: [429]: Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:568901425663'.
        '''
        list_delay_sec= self.json_data["int_delay_sec"]
        try:                
            self.get_stkidx_cnpname(inital_row_num, list_delay_sec)
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)
        
        twse_tpex_idx = ''
        '''    
        
        list_all_stkidx_row_value = []                
        #logger.info(f'len of local_dict_MAs_momentum_status: {local_dict_MAs_momentum_status.__len__()}')
            
        for dict_ticker_MAs_momentum in local_dict_MAs_momentum_status:
            stock_price_final = str(dict_ticker_MAs_momentum["close"])            
                
            ## get each stkidx row value 
            if bool(re.match(r'^-+-$',stock_price_final)) == False:
                #logger.info(f'dict_ticker_MAs_momentum: {dict_ticker_MAs_momentum}')
                # add stock MA status
                list_cellvalue = [dict_ticker_MAs_momentum["ticker"],dict_ticker_MAs_momentum["stock_name"],\
                                '{:.2f}'.format(dict_ticker_MAs_momentum["open"]),'{:.2f}'.format(dict_ticker_MAs_momentum["close"]),\
                                '{:.2f}'.format(dict_ticker_MAs_momentum["high"]),'{:.2f}'.format(dict_ticker_MAs_momentum["low"]),\
                                '{:.2f}'.format(dict_ticker_MAs_momentum["prev_day_close"]),'{:.3f}'.format(dict_ticker_MAs_momentum["weight"]),\
                                '{:.1f}'.format(dict_ticker_MAs_momentum["volume"]), '{:.1f}'.format(dict_ticker_MAs_momentum["volume_avg_weekly"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["MA_3days"]), '{:.3f}'.format(dict_ticker_MAs_momentum["MA_5days"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["MA_7days"]), '{:.3f}'.format(dict_ticker_MAs_momentum["MA_13days"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["MA_28days"]), '{:.3f}'.format(dict_ticker_MAs_momentum["MA_84days"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["MA_10days"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["MA_20days"]), '{:.3f}'.format(dict_ticker_MAs_momentum["MA_60days"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["ShortTerm_BBband_Middle"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["ShortTerm_BBband_Upper"]),'{:.3f}'.format(dict_ticker_MAs_momentum["ShortTerm_BBband_Lower"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["MediumTerm_BBband_Middle"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["MediumTerm_BBband_Upper"]),'{:.3f}'.format(dict_ticker_MAs_momentum["MediumTerm_BBband_Lower"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["RSI"]), '{:.3f}'.format(dict_ticker_MAs_momentum["MACD"]),\
                                '{:.3f}'.format(dict_ticker_MAs_momentum["MACD_Signal"]),'{:.3f}'.format(dict_ticker_MAs_momentum["MACD_Histogram"]),\
                                dict_ticker_MAs_momentum["ShortMediumTerm_trend_flag"],\
                                dict_ticker_MAs_momentum["MAs_status"]    
                                ]
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'list_cellvalue: {list_cellvalue}')

                list_all_stkidx_row_value.append(list_cellvalue)
        
        logger.info(f'len of list_all_stkidx_row_value: {list_all_stkidx_row_value.__len__()}')      
        
        # update by Cell Range
        str_gspread_range = 'A' + str(inital_row_num) + ":" + \
                            'AE' + str(inital_row_num + list_all_stkidx_row_value.__len__()-1)
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'list_all_stkidx_row_value:\n{list_all_stkidx_row_value}')
         
        try:                
            self.gss_client_worksheet.batch_update([
                                        {'range': str_gspread_range,
                                            'values': list_all_stkidx_row_value,
                                        },
                                    ])
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)    
                                        
    def update_GSpreadworksheet_200MA_plan_from_pstock(self, inital_row_num, local_pt_stock):
        list_delay_sec= self.json_data["int_delay_sec"]        
        
        try:                
            self.get_stkidx_cnpname(inital_row_num, list_delay_sec)
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)
            
        twse_tpex_idx = ''
        list_all_stkidx_row_value = []    
        
        for dict_stkidx_cnpname in self.list_stkidx_cnpname_dicts:     
                       
            if dict_stkidx_cnpname["stkidx"] is None:
                #twse_two_idx = "^TWII"
                twse_tpex_idx = dict_stkidx_cnpname["stkidx"]     
            else:
                twse_tpex_idx = dict_stkidx_cnpname["stkidx"]  
                
            local_pt_stock.check_twse_tpex_us_stocks(twse_tpex_idx)            
            logger.info(f"stock_id: {twse_tpex_idx} == ticker: {local_pt_stock.ticker}")             
            target_ticker = local_pt_stock.ticker
            local_stock_indicator_pstock = stock_indicator_pstock(ticker=target_ticker, interval='1d', \
                                                                startdate= self.start_date, enddate= self.end_date)
            local_stock_indicator_pstock.pstock_interval_startdate_enddate()
            
            # for random timer purpose
            if bool(re.match('[1-9][0-9][0-9][0-9].T(W|WO)$', target_ticker)):                
                #if self.is_prime(int(stkidx)):
                #    random_timer(0, list_delay_sec[-1])
                #    logger.info(f'prime: {int(stkidx)}') 
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'local_stock_indicator.stock_data: \n{local_stock_indicator_pstock.stock_data}')
                
            local_stock_indicator_pstock.check_MAs_status()            
            local_stock_indicator_pstock.filter_MAs_status()    
                             
            stock_price_final = str(local_stock_indicator_pstock.close)
            
            ## update cell content
            #2018/08/22 if final price doesn't exist    
            if bool(re.match(r'^-+-$',stock_price_final)) == False:
                # add stock MA status
                list_cellvalue = [local_stock_indicator_pstock.stock_MA_status,
                                  '{:.2f}'.format(local_stock_indicator_pstock.close) , '{:.2f}'.format(local_stock_indicator_pstock.open),
                                  '{:.2f}'.format(local_stock_indicator_pstock.high), '{:.2f}'.format(local_stock_indicator_pstock.low),
                                  '{:.2f}'.format(local_stock_indicator_pstock.MA_5),
                                  '{:.2f}'.format(local_stock_indicator_pstock.MA_10),
                                  '{:.2f}'.format(local_stock_indicator_pstock.MA_20),
                                  '{:.2f}'.format(local_stock_indicator_pstock.MA_60),
                                  '{:.2f}'.format(local_stock_indicator_pstock.MA_200), ]
                
                if self.opt_verbose.lower() == 'on':
                    logger.info(f'list_cellvalue: {list_cellvalue}')
                
                list_all_stkidx_row_value.append(list_cellvalue)
        
        logger.info(f'len of list_all_stkidx_row_value: {list_all_stkidx_row_value.__len__()}')        
        
        # update by Cell Range
        str_gspread_range = 'C' + str(inital_row_num) + ":" + \
                            'L' + str(inital_row_num + self.list_stkidx_cnpname_dicts.__len__()-1)
        
        if self.opt_verbose.lower() == 'on':
            logger.info(f'list_all_stkidx_row_value:\n{list_all_stkidx_row_value}')
            #logger.info(f'str_gspread_range: {str_gspread_range}')
            
        try:                
            self.gss_client_worksheet.batch_update([
                                        {'range': str_gspread_range,
                                            'values': list_all_stkidx_row_value,
                                        },
                                    ])
        except Exception as e:
            logger.info(f'Error: {e}')
            sys.exit(0)    