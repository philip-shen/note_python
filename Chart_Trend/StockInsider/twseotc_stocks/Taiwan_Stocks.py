import twseotc_stocks.Stocks_Draw as SD
from twseotc_stocks.logger_setup import *

import re
from io import StringIO
from datetime import date
from dateutil.rrule import rrule, DAILY
import pandas as pd


class Taiwan_Stocks(SD.Stocks_Draw):

    #def __init__(self, **kwargs):
    def __init__(self, stock_name: str, stock_num: str, json_data: dict, list_df_twse_tpex_stock_info: list, **kwargs):
        
        # Get all the settings done 
        self.stock_name = stock_name
        self.stock_num = stock_num
        self.table_name = ""
        self.dates = []
        self.time_calculate(json_data["start_end_date"][0], json_data["start_end_date"][1])

        # Check whether it is a tpe or tsw stock
        self.Flag_tpe_stocks = False
        self.Flag_tsw_stocks = False
        self.df_twse_website_info = list_df_twse_tpex_stock_info[0]
        self.df_tpex_website_info = list_df_twse_tpex_stock_info[1]            
        self.Control_Check_stocks()
        
        super().__init__(**kwargs)

    def time_calculate(self, start_time, end_time):
        
        start_year = int( start_time[:4] )
        end_year = int( end_time[:4] )
        start_month = int( start_time[4:6] )
        end_month = int( end_time[4:6] )
        start_day = int( start_time[6:] )
        end_day = int( end_time[6:] )
        
        #時間抓取設定
        start_date = date(start_year, start_month, start_day)
        end_date = date(end_year, end_month, end_day)

        for dt in rrule(DAILY, dtstart=start_date, until=end_date):
            self.dates.append(dt.strftime("%Y%m%d"))

    
    def Stocks_settings(self):

        # 股票類型設定

        # print("----請輸入想要抓取的股票名稱或股票代碼，擇一即可----")
        # print("\n----Enter the stock name or the stock number----")
        
        # stock_name = input("請輸入股票名稱:")
        #self.stock_name = input("\nEnter the stock name: ")

        if self.stock_num == '':
            print("\n  {}".format("(1) Enter the stock name or number"))
            print("----------------------------------------")
            # stock_num = input("請輸入股票代碼:")
            self.stock_num = input("Enter the stock number: ")
            if self.stock_num == '':
                # print("沒有輸入任何股票名稱或代碼!\n")
                assert self.stock_name != "" or self.stock_num != '' , "Please enter the stock name or number!!"

            logger.info(f'self.stock_num: {self.stock_num}')
            
        # 時間抓取設定        
        # print("""請輸入想要抓取的時間區間，輸入格式為\n20210102 -> 起始時間\n20210228 -> 結束時間""")
        # start_time = input("請輸入起始時間:")
        # end_time = input("請輸入結束時間:")
        # print("\n----Please enter the date interval----\nThe format is...\nstart time -> 20210102\nend time -> 20210228")
        print("\n  {}".format("(2) Please enter the date interval"))
        print("----------------------------------------")
        print("\n{:^39}".format("The Date Format"))
        print("########################################")
        print("#{:^38}#".format("start time -> 20210101"))
        print("#{:^38}#".format("End time   -> 20210228"))
        print("########################################")
        start_time = input("\nEnter the start time: ")
        end_time = input("Enter the end time:   ")

        logger.info(f'start_time: {start_time}; end_time: {end_time}')
        
        # Get the date, format -> 20210104
        self.time_calculate(start_time, end_time)


    ##############################################
    
    def Check_stocks(self, df, check_name, check_num):
        if df[df[check_name]==self.stock_name].empty and df[df[check_num]==self.stock_num].empty:
            return False

        else:
            if self.stock_name != "" and self.stock_num != '':
                # assert df[df[check_name] == self.stock_name][check_num].values[0] == self.stock_num, "股票名稱與股票代號不符!! 請重新輸入!!"
                assert df[df[check_name] == self.stock_name][check_num].values[0] == self.stock_num, "The stock name is inconsistent with the stock number!! Please enter again!!"
                
            if not self.stock_name:
                self.stock_name = df[df[check_num] == self.stock_num][check_name].values[0]
            if not self.stock_num:
                self.stock_num = df[df[check_name] == self.stock_name][check_num].values[0]
            
            logger.info("Pass checking... Starts analyzing stocks..")

            return True
        
    def Control_Check_stocks(self):


        logger.info("  {}".format("(3) Starts checking"))
        logger.info("----------------------------------------")
        logger.info("Checking the stock name and number...")


        ##### 上市公司
        self.Flag_tsw_stocks = self.Check_stocks(self.df_twse_website_info, check_name="證券名稱", check_num="證券代號")
        
        if self.Flag_tsw_stocks:
            self.ticker = self.stock_num+'.TW' 
            logger.info(f"ticker: {self.ticker}")
            return
        
        ##### 上櫃公司
        if not self.Flag_tsw_stocks:
            self.Flag_tpe_stocks = self.Check_stocks(self.df_tpex_website_info, check_name="名稱", check_num="代號")
            
            if self.Flag_tpe_stocks:
                self.ticker = self.stock_num+'.TWO' 
                logger.info(f"ticker: {self.ticker}")
                return
            
        # assert Flag_tpex_stocks or Flag_tsw_stocks, "非上市上櫃公司!"
        #assert self.Flag_tpex_stocks or self.Flag_twse_stocks, "Not Listed company!"
        if "^" in self.stock_num.lower():
                self.ticker=  self.stock_num
                logger.info(f"ticker: {self.ticker}")
                return
            
        if bool(re.match('^[a-zA-Z]+$', self.stock_num)):
                self.ticker=  self.stock_num
                logger.info(f"ticker: {self.ticker}")
                return
        #DE000SL0EC48.SG
        if bool(re.match('^[a-zA-Z]+(\d{1,3}.)?.+', self.stock_num)):
                self.ticker=  self.stock_num
                logger.info(f"ticker: {self.ticker}")
                return
                
        raise ValueError(
            f"{self.stock_num} cannot map yfinance ticker index ."
        )
        
        '''
        # Set the table_name
        self.table_name = self.stock_name 
        
        # assert Flag_tpe_stocks or Flag_tsw_stocks, "非上市上櫃公司!"
        assert self.Flag_tpe_stocks or self.Flag_tsw_stocks, "Not Listed company!"
        '''