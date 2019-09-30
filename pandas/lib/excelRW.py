## 2018/08/17 Initial
## 2018/08/18 Add CSV format
## 2018/08/23 Add def get_stockidxname_SeymourExcel(),def get_stockidx_SeymourExcel()
##                def get_all_stockidx_SeymourExcel() from test_crawl.py
## 2018/09/06 Add value of column 'PBR'  in def readExcel()
## 2018/10/27 Add exception handling in def readExcel(self,dir_execlfile)  
## 2019/07/20 Add get_all_stockidxname_SeymourExcel, get_stockname_SeymourExcel and get_all_stockname_SeymourExcel    
#################################################################
import xlrd
import xlwt
import xlutils.copy
import csv
import os

class ExcelRW:

    def readExcel(self,dir_execlfile):
        try:
            data = xlrd.open_workbook(dir_execlfile)    # 打開一個Excel表格
            table = data.sheets()[0]               # 打開Excel表格的第一張表
            nrows = table.nrows                    # 獲取每張表的行數
        except FileNotFoundError as fnf_error:
            print(fnf_error)

        list_rtu_row_values=[]
        for row in range(nrows):              # 遍歷每一行
            #print(table.row_values(row))          # 獲取每行的值
            #if table.row_values(row)[11] != "合理價格": # 排除第一行後，獲取每行合理價格的值
            if table.row_values(row)[10] != "價值比": # 排除第一行後，獲取每行價格比的值
                #print(str(table.row_values(row)[1]).strip('.0'), table.row_values(row)[2], table.row_values(row)[11])
                '''
                list_row_values=[str(table.row_values(row)[1])[0:4], table.row_values(row)[2], 
                                    table.row_values(row)[10],#column "價值比"
                                    table.row_values(row)[4]]#column 'PBR'
                '''
                #2019/02/16 Add 現金殖利率 by 低波固收操作模式
                #2019/02/19 Correct from 現金殖利率 to 現金股利
                #list_row_values=[str(table.row_values(row)[1])[0:4], table.row_values(row)[2], 
                
                #2019/07/20 Cause 低波固收追蹤股 contnet of '代碼' column excexx 4 digits
                
                list_row_values=[str(table.row_values(row)[1]), table.row_values(row)[2], 
                                    table.row_values(row)[10],#column "價值比"
                                    table.row_values(row)[4],#column 'PBR'
                                    #table.row_values(row)[8]]#column '現金殖利率'
                                    table.row_values(row)[7]]#column '現金股利'

                list_rtu_row_values.append(list_row_values)
                #print(list_rtu_row_values,list_row_values)

        return list_rtu_row_values

    def writeCSVbyTable(self,dir_csvfile,list_table):
        # 開啟輸出的 CSV 檔案
        with open(dir_csvfile, 'w', newline='') as csvfile:
            # 建立 CSV 檔寫入器
            writer = csv.writer(csvfile, delimiter=',')
            # 寫入二維表格
            writer.writerows(list_table)

    def writeCSVbyRow(self,dir_csvfile,list_row):
        # 開啟輸出的 CSV 檔案
        with open(dir_csvfile, 'w', newline=',') as csvfile:
            # 建立 CSV 檔寫入器
            writer = csv.writer(csvfile, delimiter=' ')
            # 寫入一列資料
            writer.writerow(list_row)

    def get_stockidxname_SeymourExcel(self,dirnamelog,excelfname):

        print('將讀取Excel file:', excelfname, '的資料')
        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excelfname)
        list_row_value_price=self.readExcel(dirlog_ExcelFile)

        list_rtu_stockidxname=[]

        # Get  stock idx and company name from Excel files
        for list_row_value in list_row_value_price:
            list_stockidx_name=[list_row_value[0],list_row_value[1]]
            list_rtu_stockidxname.append(list_stockidx_name)
        
        return list_rtu_stockidxname

    def get_all_stockidxname_SeymourExcel(self,dir_log,list_excel_files):
        list_rtu_all_stockidx_stockidxname=[]

        for excel_file in list_excel_files:
            list_stockidx_stockidxname = self.get_stockidxname_SeymourExcel(dir_log,excel_file)
            list_rtu_all_stockidx_stockidxname.extend(list_stockidx_stockidxname)

        return list_rtu_all_stockidx_stockidxname    

    def get_stockidx_SeymourExcel(self,dirnamelog,excelfname):

        print('將讀取Excel file:', excelfname, '的資料')
        #logging.error('將讀取Excel file: {}'.format(excelfname))

        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excelfname)
        list_row_value_price=self.readExcel(dirlog_ExcelFile)
        
        list_rtu_stockidx=[]

        # Get  stock idx from Excel files
        for list_row_value in list_row_value_price:
            list_stockidx=[list_row_value[0]]
            list_rtu_stockidx.append(list_stockidx)

        return list_rtu_stockidx

    def get_all_stockidx_SeymourExcel(self,dir_log,list_excel_files):

        list_rtu_all_stockidx=[]

        for excel_file in list_excel_files:
            list_stockidx=self.get_stockidx_SeymourExcel(dir_log,excel_file)
            list_rtu_all_stockidx.extend(list_stockidx)

        return list_rtu_all_stockidx

    def get_stockname_SeymourExcel(self,dirnamelog,excelfname):

        print('將讀取Excel file:', excelfname, '的資料')
        # Excel file including path
        dirlog_ExcelFile=os.path.join(dirnamelog,excelfname)
        list_row_value_price=self.readExcel(dirlog_ExcelFile)

        list_rtu_stockidxname=[]

        # Get company name from Excel files
        for list_row_value in list_row_value_price:
            list_stockidx_name=[list_row_value[1]]
            list_rtu_stockidxname.append(list_stockidx_name)
        
        return list_rtu_stockidxname    

    def get_all_stockname_SeymourExcel(self,dir_log,list_excel_files):    

        list_rtu_all_stockname=[]

        for excel_file in list_excel_files:
            list_stockname=self.get_stockname_SeymourExcel(dir_log,excel_file)
            list_rtu_all_stockname.extend(list_stockname)

        return list_rtu_all_stockname