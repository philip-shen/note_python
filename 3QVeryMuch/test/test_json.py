# 3/28/2020 Convert Nested JSON to Pandas DataFrame and Flatten List in a Column 
# https://gist.github.com/rafaan/4ddc91ae47ea46a46c0b
########################################################
#!/usr/bin/env python3

import json
from pandas.io.json import json_normalize
import pandas as pd

import os,sys,time

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger

t0 = time.time()
local_time = time.localtime(t0)
msg = 'Start Time is {}/{}/{} {}:{}:{}'
logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                        local_time.tm_hour,local_time.tm_min,local_time.tm_sec))

with open('config.json') as f:
    data = json.load(f)

'''
data["3Quest"]: [{'dut': {'path': '01/3q01/dut'}, 'standmic': {'path': '01/3q01/standmic'}}, {'dut': {'path': '02/3q02/dut'}, 'standmic': {'path': '02/3q02/standmic'}}]
'''
'''
msg = 'data["3Quest"]: {}'
logger.info(msg.format(data["3Quest"]))
'''

'''
data["3Quest"][0]: {'dut': {'path': 'ac88'}, 'standmic': {'path': 'ac88'}}
data["3Quest"][1]: {'dut': {'path': 'ac88'}, 'standmic': {'path': 'ac88'}}
'''
'''
for i,_3quest in enumerate(data["3Quest"]):
    msg = 'data["3Quest"][{}]: {}'
    logger.info(msg.format(i,data["3Quest"][i]))
'''

'''
data["3Quest"][0]['dut']['path']: ..\logs\boommic_SWout\dut
data["3Quest"][0]['standmic']['path']: ..\logs\boommic_SWout\standmic
0th file_dut_3quest:..\logs\boommic_SWout\dut.3quest\Results\output.csv
strdirname: ..\logs\boommic_SWout
str_split: ('..\\logs', 'boommic_SWout')
prevdirname: boommic_SWout
data["3Quest"][1]['dut']['path']: ..\logs\Intermic_SWin\dut
data["3Quest"][1]['standmic']['path']: ..\logs\Intermic_SWin\standmic
1th file_dut_3quest:..\logs\Intermic_SWin\dut.3quest\Results\output.csv
strdirname: ..\logs\Intermic_SWin
str_split: ('..\\logs', 'Intermic_SWin')
prevdirname: Intermic_SWin
'''

'''
for i,_3quest in enumerate(data["3Quest"]):
    msg = 'data["3Quest"][{}][\'dut\'][\'path\']: {}'
    logger.info(msg.format(i,data["3Quest"][i]['dut']['path']))
    msg = 'data["3Quest"][{}][\'standmic\'][\'path\']: {}'
    logger.info(msg.format(i,data["3Quest"][i]['standmic']['path']))
    msg = '{}th file_dut_3quest:{}'
    logger.info(msg.format(i, os.path.join(data["3Quest"][i]['dut']['path']+'.3quest', 'Results','output.csv') ) )

    strdirname=os.path.dirname(data["3Quest"][i]['standmic']['path'])
    str_split=os.path.split(strdirname)
    prevdirname=str_split[-1]
    msg = 'strdirname: {}'
    logger.info(msg.format(strdirname))
    msg = 'str_split: {}'
    logger.info(msg.format(str_split))
    msg = 'prevdirname: {}'
    logger.info(msg.format(prevdirname))
'''
'''
data["trim_ref_info"]['ref_fpath_16K']: src_wav/3quest_clean_16K_AudicatyExport.wav
data["trim_ref_info"]['ref_fpath_48K']: src_wav/3quest_clean_48K.wav
'''
for i,trim_ref_info in enumerate(data["trim_ref_info"]):
    msg = 'data["trim_ref_info"][\'ref_fpath_16K\']: {}'
    logger.info(msg.format(data["trim_ref_info"]['ref_fpath_16K']))
    msg = 'data["trim_ref_info"][\'ref_fpath_48K\']: {}'
    logger.info(msg.format(data["trim_ref_info"]['ref_fpath_48K']))

'''
data["3Quest"][22]['path_dut']: D:/project/3Quest/Logitech/logitech_0702_noise-18dB_debussy-debug-0701/dut
data["3Quest"][22]['mic_dut']: D:/project/3Quest/Logitech/logitech_0702_noise-18dB_debussy-debug-0701/dut.wav
data["3Quest"][22]['label_dut']: ../lib/3Quest_update_jimmy_standmic_Label.txt
data["3Quest"][22]['gain_dut']: 1.0
data["3Quest"][22]['path_standmic']: D:/project/3Quest/Logitech/logitech_0702_noise-18dB_debussy-debug-0701/standmic
data["3Quest"][22]['mic_standmic']: D:/project/3Quest/Logitech/logitech_0702_noise-18dB_debussy-debug-0701/standmic.wav
data["3Quest"][22]['label_standmic']: ../lib/3Quest_update_jimmy_standmic_Label.txt
data["3Quest"][22]['gain_standmic']: 1.0
'''
for i,_3quest in enumerate(data["3Quest"]):

    if (data["3Quest"][i]['label_dut'] != '' and data["3Quest"][i]['label_standmic'] != ''):
        msg = 'data["3Quest"][{}][\'path_dut\']: {}'
        logger.info(msg.format(i,data["3Quest"][i]['path_dut']))
        msg = 'data["3Quest"][{}][\'mic_dut\']: {}'
        logger.info(msg.format(i,data["3Quest"][i]['mic_dut']))
        msg = 'data["3Quest"][{}][\'label_dut\']: {}'
        logger.info(msg.format(i,data["3Quest"][i]['label_dut']))
        msg = 'data["3Quest"][{}][\'gain_dut\']: {}'
        logger.info(msg.format(i,data["3Quest"][i]['gain_dut']))
        msg = 'data["3Quest"][{}][\'channel_dut\']: {}'
        logger.info(msg.format(i,data["3Quest"][i]['channel_dut']))
        msg = 'data["3Quest"][{}][\'path_standmic\']: {}'
        logger.info(msg.format(i,data["3Quest"][i]['path_standmic']))
        msg = 'data["3Quest"][{}][\'mic_standmic\']: {}'
        logger.info(msg.format(i,data["3Quest"][i]['mic_standmic']))
        msg = 'data["3Quest"][{}][\'label_standmic\']: {}'
        logger.info(msg.format(i,data["3Quest"][i]['label_standmic']))
        msg = 'data["3Quest"][{}][\'gain_standmic\']: {}'
        logger.info(msg.format(i,data["3Quest"][i]['gain_standmic']))

print('running test_run_3pqss.py')
os.system('./test_run_3pqss.py')

msg = 'Time duration: {:.2f} seconds.'
logger.info(msg.format( time.time() - t0))             