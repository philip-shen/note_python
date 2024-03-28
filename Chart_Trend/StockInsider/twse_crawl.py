import re
import csv
import time
import requests
import argparse
from datetime import datetime, timedelta

from os import mkdir
from os.path import isdir


class TWSE_Crawler:

    def __init__(self, filename = "", dst = "data"):
        
        if not isdir(dst):
            mkdir(dst)
        self.dst = dst
    	
        self.stock_list = ""
        if filename:
            self.stock_list = self._load_list(filename)
        
        print("Stock list: ", self.stock_list)

    def _clean_row(self, row):
        for index, content in enumerate(row):
            row[index] = re.sub(",", "", content.strip()) # clean commas and spaces
        return row

    def _record(self, stock_id, row):
        
        with open('{}/{}.csv'.format(self.dst, stock_id), 'a') as f:
            cw = csv.writer(f, lineterminator = '\n')
            cw.writerow(row)

    def _get_tse_data(self, date):
        
        date_str = '{0}{1:02d}{2:02d}'.format(date[0], date[1], date[2])
        url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX'

        query_params = {
            'date': date_str,
            'response': 'json',
            'type': 'ALL',
            '_': str(round(time.time() * 1000) - 500)
        }

        page = requests.get(url, params = query_params)        
        content = page.json()
        date_str2 = '{0:04d}/{1:02d}/{2:02d}'.format(date[0], date[1], date[2])
        idx = 0
        
        print(format(date))
        try:       
            for curr_idx, data in enumerate(content['data9'], 1):
                
                stock_id = data[0].strip()
                if not self.stock_list or stock_id in self.stock_list:
                    idx += 1
                    sign = '-' if data[9].find('green') > 0 else ''
                    row = self._clean_row([date_str2,
                                           data[2],          
        								   data[4],          
        								   data[5],         
        								   data[6],          
        								   data[7],         
        								   data[8],          
        								   sign + data[10],
        								   data[3],         
                    ])
                    self._record(stock_id, row)
        except KeyError:
            print("Cannot access data on {}...".format(date_str))
            return


    def get_data(self, date):
        self._get_tse_data(date)
			
    def _load_list(self, filename):
        print("Load {}...".format(filename))
        with open(filename, "r") as f:
            reader = csv.reader(f)
            
            output = []
            for row in reader:
                output.append(row[0])
        return output
                 
def main():

	# add parser
    parser = argparse.ArgumentParser(description = 'TWSE Crawler')
    parser.add_argument('-d', '--day', default = [], type = int, nargs = '*', help = 'YYYY MM DD; if blank, use today as default.')
    parser.add_argument('-a', '--all', action = 'store_true', help = "Back to 2004/2/11.")
    parser.add_argument('-f', '--filename', type = str, nargs = '*', help = 'Assign the file for stock list.')
    args = parser.parse_args()

    first_day = datetime.today()
    
    if len(args.day) == 0:
        last_day = first_day
    elif len(args.day) == 3:
        last_day = datetime(args.day[0], args.day[1], args.day[2])
    elif args.all:
        last_day = datetime(2004, 2, 11) # first trading day of twse data: 2004/02/11
    else:
        return
        
    if args.filename:
        crawler = TWSE_Crawler(args.filename[0]) # create a new crawler
    else:
        print('No stock list. We will collect all stock data available.')
        crawler = TWSE_Crawler("")        

    
    while first_day >= last_day:
        crawler.get_data((first_day.year, first_day.month, first_day.day))
        first_day -= timedelta(1)
        time.sleep(5)
    
    print("Done.")

if __name__ == '__main__':
    main()
