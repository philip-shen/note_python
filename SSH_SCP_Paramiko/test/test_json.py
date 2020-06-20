# 3/28/2020 Convert Nested JSON to Pandas DataFrame and Flatten List in a Column 
# https://gist.github.com/rafaan/4ddc91ae47ea46a46c0b
########################################################

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

with open('config.json') as f:
    data = json.load(f)

'''
data["SSH_Client"][0]: {'hostname': '192.168.0.104', 'port': 22, 'username': 'test', 'password': '123456'}
data["SSH_Client"][0]["hostname"]: 192.168.0.104
'''
msg = 'data["SSH_Client"][0]: {}'
logger.info(msg.format(data["SSH_Client"][0]))

msg = 'data["SSH_Client"][0]["hostname"]: {}'
logger.info(msg.format(data["SSH_Client"][0]["hostname"]))

'''
data["SCP_Param"][0]: {'01_dut': {'remote_path': 'ac88', 'local_path': 'ASUS_AC_88(4*4)', 'recursive': 'True', 'preserve_times': 'True'}, '01_standmic': {'remote_path': 'ac88', 'local_path': 'ASUS_AC_88(4*4)', 'recursive': 'True', 'preserve_times': 'True'}}
data["SCP_Param"][0]["01_dut"]: {'remote_path': 'ac88', 'local_path': 'ASUS_AC_88(4*4)', 'recursive': 'True', 'preserve_times': 'True'}
'''
msg = 'data["SCP_Param"][0]: {}'
logger.info(msg.format(data["SCP_Param"][0]))

msg = 'data["SCP_Param"][0]["01_dut"]: {}'
logger.info(msg.format(data["SCP_Param"][0]["01_dut"]))

'''
data["SCP_Param"][1]: {'02_dut': {'remote_path': 'ac88', 'local_path': 'ASUS_AC_88(4*4)', 'recursive': 'True', 'preserve_times': 'True'}, '02_standmic': {'remote_path': 'ac88', 'local_path': 'ASUS_AC_88(4*4)', 'recursive': 'True', 'preserve_times': 'True'}}
data["SCP_Param"][1]["02_standmic"]: {'remote_path': 'ac88', 'local_path': 'ASUS_AC_88(4*4)', 'recursive': 'True', 'preserve_times': 'True'}
'''
msg = 'data["SCP_Param"][1]: {}'
logger.info(msg.format(data["SCP_Param"][1]))

msg = 'data["SCP_Param"][1]["02_standmic"]: {}'
logger.info(msg.format(data["SCP_Param"][1]["02_standmic"]))