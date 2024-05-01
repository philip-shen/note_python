import os, sys, time
import datetime

from turtle_trading import DataFrameLoader
from turtle_trading.position_sizing import getn, getunits
from turtle_trading.entries import getentry, addunits
from turtle_trading.entries import addunits
from turtle_trading.stops import getstops
from turtle_trading.exits import getexit

import turtle_trading.lib_misc as lib_misc
from turtle_trading.logger_setup import *

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.\n'.format( time_consumption)#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg)

if __name__ == '__main__':
    logger_set(strdirname)
    
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    
    ticker = '2330.TW'
    dataframe = DataFrameLoader(ticker)
    date = '2024-04-30'#datetime.date(2024, 4, 30)
    
    logger.info(f"Price of {date}: {dataframe.get_price(date)}")
    
    """ using the position_sizing module """
    N_value = getn(dataframe, date=date)
    position_sizes = getunits(dataframe=dataframe, account=1000000, date=date)

    logger.info(f'N_value: {N_value}')
    logger.info(f'position_sizes: {position_sizes}')
    
    """ using the entries module """
    logger.info(getentry(dataframe=dataframe, system=1)) 
    logger.info(getentry(dataframe=dataframe, system=2)) 

    logger.info(addunits(orig_breakout=310, orig_n=2.50)) 
    logger.info(addunits(orig_breakout=310, orig_n=2.50, number_of_units=6))

    """ using the stops module """
    units = addunits(orig_breakout=28.30, orig_n=1.20) # >>> [28.3, 28.9, 29.5, 30.1]

    getstops(stop_system="regular", unit_list=units, orig_n=1.20) # >>> [27.7, 27.7, 27.7, 27.7]
    getstops(stop_system="whipsaw", unit_list=units, orig_n=1.20) # >>> [27.7, 28.3, 28.9, 29.5]


    gapped_units = [28.3, 28.9, 29.5, 30.8]

    getstops(stop_system="regular", unit_list=gapped_units, orig_n=1.20) # >>> [27.7, 27.7, 27.7, 28.4]
    getstops(stop_system="whipsaw", unit_list=gapped_units, orig_n=1.20) # >>> [27.7, 28.3, 28.9, 30.2]

    """ using the exist module """
    getexit(dataframe=dataframe, system=1, pos_direction=True) # >>> True

    getexit(dataframe=dataframe, system=1, pos_direction=True, date=datetime.date(2023, 11, 10)) # >>> False

    est_timer(t0)