import twseotc_stocks.MySQL_Database as MD
from twseotc_stocks.logger_setup import *

import requests
from io import StringIO
import pandas as pd
import time


class Stocks_Crawl(MD.MySQL_Database):
    
    def __init__(self, timesleep=5, Crawl_flag = True, MySQL_flag = True, 
                 Fetch_stock_statistics_flag = True, **kwargs):
        
        super().__init__(**kwargs)      

        self.Crawl_flag = Crawl_flag
        self.MySQL_flag = MySQL_flag
        self.Fetch_stock_statistics_flag = Fetch_stock_statistics_flag

        ################# 上櫃公司價格資料
        self.url_tpex_stock = "http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d="
        # self.tpex_df_stocks = pd.DataFrame( data = [], 
        #                                     columns = ['Date', '證券代號', '證券名稱', 
        #                                                '成交股數', '成交筆數', 
        #                                                '成交金額', '開盤價', 
        #                                                '最高價', '最低價', 
        #                                                '收盤價', '漲跌(+/-)', 
        #                                                '漲跌價差' ])

        ################# 上櫃公司法人買賣資料
        self.url_tpex_df_institutional_investors = "https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&o=csv&se=EW&t=D&d="
        # self.tpex_df_institutional_investors = pd.DataFrame( data = [], 
        #                                                      columns = ['證券代號', '證券名稱', 
        #                                                                 '外陸資買進股數(不含外資自營商)', 
        #                                                                 '外陸資賣出股數(不含外資自營商)',
        #                                                                 '外陸資買賣超股數(不含外資自營商)', '外資自營商買進股數', 
        #                                                                 '外資自營商賣出股數', '外資自營商買賣超股數', 
        #                                                                 '投信買進股數','投信賣出股數', 
        #                                                                 '投信買賣超股數', '自營商買賣超股數', 
        #                                                                 '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)',
        #                                                                 '自營商買賣超股數(自行買賣)', '自營商買進股數(避險)',
        #                                                                 '自營商賣出股數(避險)', '自營商買賣超股數(避險)',
        #                                                                 '三大法人買賣超股數' ])

        ################# 上市公司價格資料
        
        self.url_stock = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='
        self.df_stocks = pd.DataFrame(data = [],
                                      columns = ['Date', '證券代號', '證券名稱', 
                                                 '成交股數', '成交筆數', 
                                                 '成交金額', '開盤價', 
                                                 '最高價', '最低價', 
                                                 '收盤價', '漲跌(+/-)', 
                                                 '漲跌價差' ])
        
        ################# 上市公司法人買賣資料
        '''
        https://raw.githubusercontent.com/litefunc/tse/master/%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA/%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA%E8%B2%B7%E8%B3%A3%E8%B6%85%E6%97%A5%E5%A0%B1.py
        
        def gen_url(type: str, input_date: str) -> str:
            return 'https://www.twse.com.tw/rwd/zh/fund/T86?response=json&date={}&selectType={}'.format(input_date, type)
        '''
        #'http://www.twse.com.tw/fund/T86?response=csv&date='
        self.url_institutional_investors = 'https://www.twse.com.tw/rwd/zh/fund/T86?response=csv&date='
        self.df_institutional_investors = pd.DataFrame( data = [], 
                                                        columns = ['證券代號', '證券名稱', 
                                                                    '外陸資買進股數(不含外資自營商)', 
                                                                    '外陸資賣出股數(不含外資自營商)',
                                                                    '外陸資買賣超股數(不含外資自營商)', '外資自營商買進股數', 
                                                                    '外資自營商賣出股數', '外資自營商買賣超股數', 
                                                                    '投信買進股數','投信賣出股數', 
                                                                    '投信買賣超股數', '自營商買賣超股數', 
                                                                    '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)',
                                                                    '自營商買賣超股數(自行買賣)', '自營商買進股數(避險)',
                                                                    '自營商賣出股數(避險)', '自營商買賣超股數(避險)',
                                                                    '三大法人買賣超股數'])

        ################# 上市櫃公司股票本益比, 股價淨值比, 殖利率, 股利年度

        self.df_statistics = pd.DataFrame( data = [], 
                                           columns = ["證券代號", "證券名稱", "本益比", "股價淨值比", "殖利率", "股利年度"])

        
        self.timesleep = timesleep
        
        if self.Crawl_flag:
            self.Crawl()
        elif self.Fetch_stock_statistics_flag:
            self.Fetch_stock_statistics()
        else:
            logger.info("The program is useless...END")

        # 爬蟲完要不要存進MySQL資料庫
        if self.MySQL_flag:

            # 存進去Database
            self.SaveIntoDatabase()

            # 爬蟲完，也如果有將資料存進MySQL，將資料庫關起來
            self.Close()
            
    

    # Change the date
    #############################################

    def date_changer(self, date):

        year = date[:4]
        year = str(int(year)-1911)
        month = date[4:6]
        day = date[6:]

        return year+"/"+month+"/"+day

    # CRAWLING
    #############################################
        
    def Crawl(self):
        
        # Start crawling data
        for date in self.dates:

            #print(date + " starts crawling")
            logger.info(f'{date} starts crawling')
            try:

                ################ 爬上櫃公司 ################
                
                if self.Flag_tpe_stocks:
                    
                    ROC_era_date = self.date_changer(date)

                    # 股價資訊
                    self.Crawl_method(url = self.url_tpex_stock, 
                                            date = ROC_era_date, 
                                            Date = date, 
                                            url_suffix='&s=0,asc,0', 
                                            Flag_tpex_stocks=True,
                                            Flag_tpex_insti_inv=False,
                                            Flag_stocks=False, 
                                            Flag_insti_inv=False)
                                            
                    # 三大法人資訊
                    self.Crawl_method(url = self.url_tpex_df_institutional_investors, 
                                            date = ROC_era_date, 
                                            Date = date, 
                                            url_suffix='&s=0,asc', 
                                            Flag_tpex_stocks=False,
                                            Flag_tpex_insti_inv=True,
                                            Flag_stocks=False, 
                                            Flag_insti_inv=False)

                    # 本益比, 股價淨值比, 殖利率(%), 股利年度

                    self.Crawl_PB_and_PE(ROC_era_date)

                ################ 爬上市公司 ################
                
                if self.Flag_tsw_stocks:

                    # 股價資訊
                    self.Crawl_method(url = self.url_stock, 
                                            date = date, 
                                            Date = date, 
                                            url_suffix='&type=ALL', 
                                            Flag_tpex_stocks=False,
                                            Flag_tpex_insti_inv=False,
                                            Flag_stocks=True, 
                                            Flag_insti_inv=False)
                                            
                    #爬上市公司三大法人資訊
                    self.Crawl_method(url = self.url_institutional_investors, 
                                            date = date, 
                                            Date = date, 
                                            url_suffix='&selectType=ALLBUT0999', 
                                            Flag_tpex_stocks=False,
                                            Flag_tpex_insti_inv=False,
                                            Flag_stocks=False, 
                                            Flag_insti_inv=True)

                    # 本益比, 股價淨值比, 殖利率(%), 股利年度

                    self.Crawl_PB_and_PE(date)

            except Exception as err:
                
                if type(err) == ValueError:
                    logger.info(str(err))
                    #print(date +" is holiday")

                elif type(err) == KeyError:
                    logger.info(str(err))
                    #print(date +" is holiday")
                else:
                    
                    #print("Error happens!! -> " + str(err))
                    logger.info(f"Error happens!! -> {str(err)}")
                    break

                                        
            time.sleep(self.timesleep)

        # 把所有資料concatenate起來

        self.ConcatData()
        

 
    # 抓取特定股票(使用者要抓的那支股票)
    #############################################

    def Get_specific_stock(self, df):

        if self.stock_name != '':
            
            df = df[df["證券名稱"].apply(lambda x:x.replace(" ", "") ) == self.stock_name]

        elif self.stock_num != '':

            df["證券代號"] = df["證券代號"].apply(lambda x:x.replace("=", "").replace('"', '').replace(" ", ""))
            df = df[df['證券代號'] == self.stock_num]

        return df
    
    # 重新命名col name, 確保一致
    #############################################

    def Rename_df_columns(self, df, Flag_tpex_stocks = False, Flag_tpex_insti_inv = False):

        tpex_stocks_rename_columns = {  "代號":"證券代號",
                                        "名稱":"證券名稱",
                                        "收盤 ":"收盤價",
                                        "漲跌":"漲跌價差",
                                        "開盤 ":"開盤價", 
                                        "最高 ":"最高價",
                                        "最低":"最低價",
                                        "成交股數  ":"成交股數",
                                        "成交金額(元)":"成交金額",
                                        "成交筆數 ":"成交筆數"}

        tpex_insti_inv_rename_columns = {   "代號":"證券代號", 
                                            "名稱":"證券名稱", 
                                            "外資及陸資(不含外資自營商)-買進股數":"外陸資買進股數(不含外資自營商)", 
                                            "外資及陸資(不含外資自營商)-賣出股數":"外陸資賣出股數(不含外資自營商)", 
                                            "外資及陸資(不含外資自營商)-買賣超股數":"外陸資買賣超股數(不含外資自營商)", 
                                            "外資自營商-買進股數":"外資自營商買進股數", 
                                            "外資自營商-賣出股數":"外資自營商賣出股數", 
                                            "外資自營商-買賣超股數":"外資自營商買賣超股數",
                                            "投信-買進股數":"投信買進股數",
                                            "投信-賣出股數":"投信賣出股數",
                                            "投信-買賣超股數":"投信買賣超股數",
                                            "自營商(自行買賣)-買進股數":"自營商買進股數(自行買賣)",
                                            "自營商(自行買賣)-賣出股數":"自營商賣出股數(自行買賣)",
                                            "自營商(自行買賣)-買賣超股數":"自營商買賣超股數(自行買賣)",
                                            "自營商(避險)-買進股數":"自營商買進股數(避險)",
                                            "自營商(避險)-賣出股數":"自營商賣出股數(避險)",
                                            "自營商(避險)-買賣超股數":"自營商買賣超股數(避險)",
                                            "自營商-買賣超股數":"自營商買賣超股數",
                                            "三大法人買賣超股數合計":"三大法人買賣超股數" }

        if Flag_tpex_stocks:  
            df.rename(columns=tpex_stocks_rename_columns, inplace = True)
        elif Flag_tpex_insti_inv:
            df.rename(columns=tpex_insti_inv_rename_columns, inplace = True)
        else:
            print("Error!!")

        return df

    # 開始爬蟲
    #############################################

    def Crawl_method(self, url, date, Date, url_suffix='', Flag_tpex_stocks=False, Flag_tpex_insti_inv=False,
                     Flag_stocks=False, Flag_insti_inv=False):
        
        # 下載股價
        r = requests.post( url + date + url_suffix)

        # 整理資料，變成表格
        
        if not Flag_tpex_stocks and not Flag_tpex_insti_inv and not Flag_stocks and not Flag_insti_inv:
            
            logger.info("Error...Crawling nothing, please set the flags right")
            return 0


        ######### 爬上櫃公司 #########

        if Flag_tpex_stocks:
            
            df = pd.read_csv(StringIO(r.text), header=2).dropna(how='all', axis=1).dropna(how='any')

            df = df.iloc[:, :11]
            #logger.info(f'df:\n{df}')
            
            df = self.Rename_df_columns(df, Flag_tpex_stocks = True, Flag_tpex_insti_inv = False)
            #logger.info(f'df:\n{df}')
            
            df = self.Get_specific_stock(df)
            logger.info(f'Get_specific_stock df:\n{df}')

            df.insert(0, "Date", Date)
            #logger.info(f'df:\n{df}')
            
            df.drop("均價 ", axis = "columns", inplace = True)
            
            df["漲跌(+/-)"] = df["漲跌價差"].values[0][0] if df["漲跌價差"].values[0][0] != "0" else "X"
            #logger.info(f'df:\n{df}')
            
            '''
            DataFrame' object has no attribute 'append'
            #self.df_stocks = self.df_stocks.append(df, ignore_index=True)
            '''
            # Correct way to append a new row to a DataFrame in pandas 2.0+
            self.df_stocks = pd.concat([self.df_stocks, df], ignore_index=True)
            logger.info(f'self.df_stocks:\n{self.df_stocks}')
            
        if Flag_tpex_insti_inv:

            df = pd.read_csv(StringIO(r.text.replace("=", "")), header = 1 ).dropna(how='all', axis=1).dropna(how='any')

            df.insert(0, "Date", Date)
            
            df.drop(columns=[ "自營商-買進股數", 
                              "自營商-賣出股數",
                              "外資及陸資-買進股數",
                              "外資及陸資-賣出股數",
                              "外資及陸資-買賣超股數"], inplace = True)

            df = self.Rename_df_columns(df, Flag_tpex_stocks = False, Flag_tpex_insti_inv = True)

            df = self.Get_specific_stock(df)
            logger.info(f'Get_specific_stock df:\n{df}')
            
            '''
            DataFrame' object has no attribute 'append'
            #self.df_institutional_investors = self.df_institutional_investors.append(df, ignore_index = True)
            '''
            self.df_institutional_investors = pd.concat([self.df_institutional_investors, df], ignore_index = True)
            logger.info(f'self.df_institutional_investors:\n {self.df_institutional_investors}')
            
        ######### 爬上市公司 #########

        if Flag_stocks:

            df = pd.read_csv(StringIO(r.text.replace("=", "")), 
                             header = ["證券代號" in l for l in r.text.split("\n")].index(True)-1 )
            
            #logger.info(f'df:\n{df}')
            df.insert(0, "Date", date)

            df = df.iloc[:, :12]

            df = self.Get_specific_stock(df)
            #logger.info(f'Get_specific_stock df:\n{df}')
            
            #self.df_stocks = self.df_stocks.append(df, ignore_index=True)
            self.df_stocks = pd.concat([self.df_stocks, df], ignore_index=True)
            logger.info(f'self.df_stocks:\n{self.df_stocks}')
            
        if Flag_insti_inv:
            '''
            Error happens!! -> Error tokenizing data. C error: Expected 1 fields in line 5, saw 5
            '''
            '''
            "113年05月02日 三大法人買賣超日報"
            "證券代號","證券名稱","外陸資買進股數(不含外資自營商)","外陸資賣出股數(不含外資自營商)","外陸資買賣超股數(不含外資自營商)","外資自營商買進股數","外資自營商賣出股數","外資自營商買賣超股數","投信買進股數","投信賣出股數","投信買賣超股數","自營商買賣超股數","自營商買進股數(自行買賣)","自營商賣出股數(自行買賣)","自營商買賣超股數(自行買賣)","自營商買進股數(避險)","自營商賣出股數(避險)","自營商買賣超股數(避險)","三大法人買賣超股數",
            "2618","長榮航          ","92,956,462","56,177,844","36,778,618","0","0","0","10,717,000","2,000","10,715,000","9,487,649","4,677,995","2,505,345","2,172,650","8,616,999","1,302,000","7,314,999","56,981,267",
            "3231","緯創            ","24,083,608","12,878,200","11,205,408","0","0","0","538,000","2,588,612","-2,050,612","-89,409","318,000","430,000","-112,000","458,645","436,054","22,591","9,065,387",
            '''
            #logger.info(f'r.text:\n{r.text}')                
            df = pd.read_csv(StringIO(r.text.replace("=", "")),
                             header = 1 ).dropna(how='all', axis=1).dropna(how='any')
            #logger.info(f'df:\n{df}')
            
            df.insert(0, "Date", date)

            df = self.Get_specific_stock(df)
            #logger.info(f'Get_specific_stock df:\n{df}')
            
            #self.df_institutional_investors = self.df_institutional_investors.append(df, ignore_index = True)
            self.df_institutional_investors = pd.concat([self.df_institutional_investors, df], ignore_index = True)
            logger.info(f'self.df_institutional_investors:\n {self.df_institutional_investors}')

    # 合併Date
    #############################################

    def ConcatData(self):

        # 將index reset 以免concat出現NaN值
        self.df_stocks.reset_index(drop=True, inplace=True)
        self.df_institutional_investors.reset_index(drop=True, inplace=True)
        self.df_statistics.reset_index(drop=True, inplace=True)
        
        #logger.info(f'self.df_stocks:\n{self.df_stocks}')
        #logger.info(f'self.df_institutional_investors:\n{self.df_institutional_investors}')
        #logger.info(f'self.df_statistics:\n{self.df_statistics}')

        self.df_stocks = pd.concat([self.df_stocks, self.df_institutional_investors.drop(columns=["Date", "證券代號", "證券名稱"]), 
                        self.df_statistics.drop(columns=["證券代號", "證券名稱"])], axis = 1)

        logger.info(f'self.df_stocks:\n{self.df_stocks}')
        
    # 將Date存進資料庫
    #############################################

    def SaveIntoDatabase(self):


        # creating column list for insertion
        cols = "`,`".join([str(i) for i in self.df_stocks.columns.tolist()])

        # Insert DataFrame recrds one by one.
        for i, row in self.df_stocks.iterrows():

            try:
                sql = "INSERT INTO `{}` (`".format(self.table_name) +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
                logger.info(f'sql:\n{sql}')
                self.cursor.execute(sql, tuple(row))

                # the connection is not autocommitted by default, so we must commit to save our changes
                self.db.commit()
                
            except Exception as err:
                
                logger.info(str(err))
                #print("This data already exists in this table, jumping...")
                continue
    

    # 抓取PB, PE
    #############################################

    def Crawl_PB_and_PE(self, date):

        """
        This function is for crwaling the PB, PE and Dividend yield statistics.
        """


        # 上櫃公司

        if self.Flag_tpe_stocks:
            
            url = "https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_download.php?l=zh-tw&d="+date+"&s=0,asc,0"

            r = requests.get(url)

            r = r.text.split("\n")

            df = pd.read_csv(StringIO("\n".join(r[3:-1]))).fillna(0)

            columns_title = ["股票代號", "名稱", "本益比", "股價淨值比", "殖利率(%)", "股利年度" ]

            df = df[columns_title]
            #logger.info(f'df:\n{df}')
            
            df.rename(columns = {"殖利率(%)":"殖利率", "股票代號":"證券代號", "名稱":"證券名稱"}, inplace = True)
            #logger.info(f'df:\n{df}')
            
            '''
            'int' object has no attribute 'replace'
            
            # Convert column 'A' to string
            df['A'] = df['A'].astype(str)
            '''
            '''
                 證券代號  證券名稱    本益比  股價淨值比   殖利率  股利年度
            0    1240  茂生農經  12.60   1.51  5.20   112
            1    1259    安心  14.35   1.02  2.43   112
            2    1264    德麥  16.45   3.53  4.67   112
            3    1268  漢來美食  20.63   3.08  4.46   112
            4    1336    台翰  14.17   0.88  2.08   112
            ..    ...   ...    ...    ...   ...   ...
            813  9949    琉園   0.00   2.84  0.00   112
            814  9950   萬國通   2.65   2.03  0.00   112
            815  9951    皇田  12.41   1.49  4.75   112
            816  9960   邁達康  10.73   1.44  6.28   112
            817  9962    有益  13.41   1.32  6.51   112

            [818 rows x 6 columns]
            '''
            df["證券代號"] = df["證券代號"].astype(str)
            
            df = self.Get_specific_stock(df)
            #logger.info(f'Get_specific_stock df:\n{df}')
            '''
            DataFrame' object has no attribute 'append'
            '''        
            #self.df_statistics = self.df_statistics.append(df, ignore_index=True)
            self.df_statistics = pd.concat([self.df_statistics, df], ignore_index=True)
            logger.info(f'self.df_statistics:\n{self.df_statistics}')
            
        # 上市公司

        if self.Flag_tsw_stocks:

            url = "https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date="+date+"&selectType=ALL"

            r = requests.get(url)

            r = r.text.split("\r\n")[:-13]

            df = pd.read_csv(StringIO("\n".join(r)), header=1).dropna(how="all", axis=1).apply(lambda x:x.replace("-", 0))

            columns_title = ["證券代號", "證券名稱", "本益比", "股價淨值比", "殖利率(%)", "股利年度" ]

            df = df[columns_title]

            df.rename(columns = {"殖利率(%)":"殖利率"}, inplace = True)

            df["證券代號"] = df["證券代號"].astype(str)            
            df = self.Get_specific_stock(df)
            #logger.info(f'Get_specific_stock df:\n{df}')
            
            #self.df_statistics = self.df_statistics.append(df, ignore_index=True)
            self.df_statistics = pd.concat([self.df_statistics, df], ignore_index=True)
            logger.info(f'self.df_statistics:\n{self.df_statistics}')

        