'''
Handling large JSON files without fully loading them into memory
https://medium.com/@lakshmi_priya_ramisetty/handling-large-json-files-without-fully-loading-them-into-memory-ce3d020a3f82

'''
import os, sys, time
import pandas as pd
import argparse
import json
import pathlib
import ijson

import twseotc_stocks.lib_misc as lib_misc
from insider.logger_setup import *


strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

def est_timer(start_time):
    time_consumption, h, m, s= lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.'.format( time_consumption)#msg = 'Time duration: {:.3f} seconds.'
    logger.info(msg)
    
'''
Prefix: , Event: map_key, Value: start_end_date
Prefix: start_end_date, Event: start_array, Value: None
Prefix: start_end_date.item, Event: start_array, Value: None
Prefix: start_end_date.item.item, Event: string, Value: 20241101
Prefix: start_end_date.item.item, Event: string, Value: 20251112
Prefix: start_end_date.item, Event: end_array, Value: None
Prefix: start_end_date, Event: end_array, Value: None
'''
def process_large_json(file_path):
    # Open the large JSON file
    with open(file_path, 'rb') as file:
        # Use ijson to parse the file incrementally
        parser = ijson.parse(file)

        # Iterate over the parsing events
        for prefix, event, value in parser:
            # Process the events as needed
            # 'prefix' tells you the location in the JSON structure
            # 'event' tells you what kind of event (e.g., 'start_map', 'end_map', 'string', 'number')
            # 'value' is the actual data value for events that have data (e.g., 'string', 'number')
            #print(f"Prefix: {prefix}, Event: {event}, Value: {value}")
            logger.info(f"Prefix: {prefix}, Event: {event}, Value: {value}")
            
def process_json_specific_values(file_path, argument):
    #logger.info(f"key_item: {key_item}")
    key_item = f"{argument.conf_key_item}.item"
    # Open the large JSON file    
    with open(file_path, 'rb') as file:
        for keyitem_value in ijson.items(file, key_item):
            logger.info(f"Original Key: {key_item} Value: {keyitem_value}")
'''
A Practical Guide to JSON Parsing with Python
https://www.zyte.com/blog/json-parsing-with-python/
'''
def update_json_specific_values(file_path, argument):
    with open(file_path, encoding="utf-8") as f:
        json_data = json.load(f)  
        
    more_json_string = "{{\"{}\":[[\"{}\", \"{}\"]]}}".format(argument.conf_key_item,\
                                                argument.conf_item_start_date, argument.conf_item_end_date)
    
    logger.info(f"more_json_string: {more_json_string}")
    
    more_json_data = json.loads(more_json_string)
    json_data.update(more_json_data)    
    
    logger.info('Update Key: {}; Vaule: {}'.format(f"{argument.conf_key_item}", json_data[f"{argument.conf_key_item}"]) )
    
    # Saves the dictionary named data as a JSON object to the file data.json
    with open(file_path, "w") as f:
        json.dump(json_data, f)
'''
number of self.ret_listOfFileNames:25 in walk_in_dir

['d:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_200ma.json','d:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf0052.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00735.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00770.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00830.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00875.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00893.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00902.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00909.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00911.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00923.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00927.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00947.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00951.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00954.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf009805.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_etf00981A.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_gSheet.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_nasdaq100.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_sp500.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_tpex_volatility.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_twse_200ma.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_twse_etf.json', 
'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_twse_top300.json', 'd:\\projects\\note_python\\Chart_Trend\\StockInsider\\test_update_json\\config_twse_volatility.json']
'''
def update_json_path_specific_values(argument, json_path, arg_file_type='config_*.json'):
    arg_opt_verbose= 'OFF'
    ith = 0
    local_query_all_files_in_dir = \
                lib_misc.Query_all_files_in_dir(dir_path=json_path, file_type=arg_file_type, \
                                                opt_verbose=arg_opt_verbose)
    local_path_json_files = local_query_all_files_in_dir.walk_in_dir()
    
    logger.info(f"number of local_path_json_files:{len(local_path_json_files)} in walk_in_dir")
    
    if arg_file_type.lower() == "on":
        logger.info(f'local_path_json_files: {local_path_json_files}' )
    
    for local_path_json in local_path_json_files:
        ith +=1
        logger.info(f'Update {ith}th path_json_file: \n                                                                             {local_path_json}' )
        process_json_specific_values(local_path_json, argument)
        update_json_specific_values(local_path_json, argument)   
        
if __name__ == '__main__':
    # python test_change_json_start_end_date.py --conf_json_fully_path "d:/projects/note_python/Chart_Trend/StockInsider/test_update_json/" 
    # --conf_item_start_date "20241101" --conf_item_end_date "20251124"
    
    parser = argparse.ArgumentParser(description='change json start end date')
    parser.add_argument('--conf_json_fully_path', type=str, default="", help='Config file path of json')
    parser.add_argument('--conf_key_item', type=str, default="start_end_date", help='Config Key item')
    parser.add_argument("--conf_item_start_date", type=str, default='20241101', help='search start date ex. \'20241101\'')
    parser.add_argument("--conf_item_end_date", type=str, default='20251124', help='search end date ex. \'20241124\'')
    
    args = parser.parse_args()
    
    logger_set(strdirname)
    
    json_file = "_data.json"

    #json_path = pathlib.Path(strdirname)/"test_update_json"
    json_path_file = pathlib.Path(strdirname)/json_file
    json_path = args.conf_json_fully_path
    
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    
    # Replace with the path to your large JSON file
    #process_large_json(file_path)    
    #process_json_specific_values(json_path_file, args)
    #update_json_specific_values(json_path_file, args)
    
    update_json_path_specific_values(args, json_path)
    
    est_timer(t0)