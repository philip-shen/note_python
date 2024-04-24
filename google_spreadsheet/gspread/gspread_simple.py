import gspread
import os, sys, time
import json
import argparse, pathlib
from oauth2client.service_account import ServiceAccountCredentials

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

import _libs.lib_misc
from _libs.logger_setup import *

# (1) Google Spread Sheetsにアクセス
def connect_gspread(jsonf, url, key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    if url != "" and key == "":
        SPREADSHEET_URL = url
        worksheet = gc.open_by_url(SPREADSHEET_URL).sheet1
    elif url == "" and key != "":
        SPREADSHEET_KEY = key
        worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
        
    return gc, worksheet

def est_timer(start_time):
    time_consumption, h, m, s= _libs.lib_misc.format_time(time.time() - start_time)         
    msg = 'Time Consumption: {}.'.format( time_consumption)#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg)

def demo_01(gworksheet):
    #(2) Google Spread Sheets上の値を更新
    #(２−１)あるセルの値を更新（行と列を指定）
    logger.info(f"update cell")
    gworksheet.update_cell(1,1,"test1")
    gworksheet.update_cell(2,1,1)
    gworksheet.update_cell(3,1,2)

    #(２−２)あるセルの値を更新（ラベルを指定）
    gworksheet.update_acell('C1','test2')
    gworksheet.update_acell('C2',1)
    gworksheet.update_acell('C3',2)

    #(2-3)ある範囲のセルの値を更新
    logger.info(f"update range 'E1:G3'")
    ds= gworksheet.range('E1:G3')
    ds[0].value = 1
    ds[1].value = 2
    ds[2].value = 3
    ds[3].value = 4
    ds[4].value = 5
    ds[5].value = 6
    ds[6].value = 7
    ds[7].value = 8
    ds[8].value = 9
    ws.update_cells(ds)

    #Selecting a Worksheet
    # Most common case: Sheet1
    #worksheet = sh.sheet1
    
    # With label
    val = gworksheet.get('c1').first()
    logger.info(f"label C1: {val}")
    
    # With coords
    val = gworksheet.cell(1, 3).value
    logger.info(f"cell (1,3): {val}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='demo simple Google Sheet function')
    parser.add_argument('--conf', type=str, default='config.json', help='Config json')
    args = parser.parse_args()
    
    logger_set(strdirname)
    
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    
    json_file= args.conf
    json_path_file = pathlib.Path(strdirname)/json_file
    
    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )    
        est_timer(t0)
        sys.exit()

    # ここでjsonfile名と2-2で用意したkeyを入力
    spread_sheet_key = ""#"1wObUaahWG-vgb72xya_6SLEC8XHTiVBOZlTDnC7efc4"
    spread_sheet_url = "https://docs.google.com/spreadsheets/d/1wObUaahWG-vgb72xya_6SLEC8XHTiVBOZlTDnC7efc4/edit#gid=0"
    sh, ws = connect_gspread(json_path_file, spread_sheet_url, spread_sheet_key)

    #demo_01(ws)
    
    est_timer(t0)    