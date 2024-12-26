'''
zipline 銘柄を売買する関数
https://qiita.com/NT1123/items/a0b3a779f05d62096354
'''

from zipline.api import order, record, symbol,set_benchmark
import pandas as pd
from datetime import datetime
import zipline
import pytz  # timezoneの設定 https://narito.ninja/blog/detail/81/
from trading_calendars import get_calendar #各取引所のカレンダーを取り込む
from collections import OrderedDict
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


###### (1)初期設定 #######
HDIR="xxxxxxxxxxxxxxxxxx"#銘柄データcsvファイルが格納されているディレクトリを指定する。
data=OrderedDict() #順序付き辞書に順番を持たせる。
tickers=["n1570","n7752"]  #銘柄名を指定する。


###### (2)csvファイルから銘柄の株価を読み込む ######

for ticker in tickers:
    DIR=HDIR + ticker +".csv" #読み込む銘柄(csvファイル)を指定する。
    data[ticker]= pd.read_csv(DIR, index_col=0,parse_dates=True) #csvファイルを読み込む。

###### (3)データセットを用意する。 ###########

panel=pd.Panel(data)  #3次元配列panelに銘柄データを入れる。
panel.major_axis=panel.major_axis.tz_localize(pytz.utc) #時刻をUTCゾーンにする。(便宜的にUTCゾーンにしないとエラーになる)


###### (4) トレードアルゴリズムの記述　#########

def initialize(contect):
    set_benchmark(symbol("n1570")) #銘柄n1570をベンチマークに指定する。


def handle_data(context,data):
    order(symbol("n1570"),1) #毎日大引けで1株購入する。
    record(N1570=data.current(symbol("n1570"),"price")) #銘柄n1570のclose値を記録する。


###### (5) バックテストを実施する　#########    
    
#開始日時と終了日時を指定する    
starttime=datetime(2020,2,4,0,0,0,0,pytz.utc)
endtime=datetime(2020,2,8,0,0,0,0,pytz.utc)    
    
#バックテストを実行する。(毎日大引けで銘柄n1570を1株購入する。)
perf=zipline.run_algorithm(start=starttime,
                            end=endtime,
                            initialize=initialize,
                            capital_base=1000000, #スタート時のアセットを指定する。
                            handle_data= handle_data,
                            data=panel,
                            trading_calendar=get_calendar('XTKS') #東京証券取引所のカレンダーを読み込む
                           )

dat0=pd.DataFrame(perf,columns=["N1570","ending_cash","ending_exposure"])

dat0.to_csv("C:/Users/fdfpy/anaconda3/backtestresult/dat0.csv")
print(dat0)