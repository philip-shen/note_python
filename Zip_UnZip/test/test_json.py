# 3/2//2020 Convert Nested JSON to Pandas DataFrame and Flatten List in a Column 
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

df = pd.DataFrame(data)   

#normalized_df = pd.json_normalize(df["WiFi_ThroughputTest"])
#normalized_df.columns = normalized_df.columns.map(lambda x: x.split(".")[-1])

'''column is a string of the column's name.
for each value of the column's element (which might be a list),
duplicate the rest of columns at the corresponding row with the (each) value.
'''

def flattenColumn(input, column):
    column_flat = pd.DataFrame([[i, c_flattened] for i, y in input[column].apply(list).iteritems() for c_flattened in y], columns=['I', column])
    column_flat = column_flat.set_index('I')
    return input.drop(column, 1).merge(column_flat, left_index=True, right_index=True)
    
#new_df = flattenColumn(normalized_df, 'column_name')

msg = 'df: {}'
logger.info(msg.format( df))

'''
df["WiFi_ThroughputTest"]: 
0    {'description': 'Wireless_PerformanceTest', 'd...
1    {'AC_88': {'model': 'ac88', 'description': 'AS...
2    {'DWA_192': {'model': 'dwa192', 'description':...
3    {'AC_8260': {'model': 'ac8260', 'description':...
4    {'MACBOOK': {'model': 'macbook', 'description'...
5    {'AX_200': {'model': 'ax200', 'description': '...
Name: WiFi_ThroughputTest, dtype: object
'''
msg = 'df["WiFi_ThroughputTest"]: {}'
logger.info(msg.format( df["WiFi_ThroughputTest"]))

'''
df["WiFi_ThroughputTest"][0]: 
{'description': 'Wireless_PerformanceTest', 
'driver': 'd', 
'folder': 'DHCPNATThroughputTest', 
'folder_zip': 
'TestResultTemp', 
'folder_zip_backup': 'The latest Test Result'}
'''
msg = 'df["WiFi_ThroughputTest"][0]: {}'
logger.info(msg.format( df["WiFi_ThroughputTest"][0]))

'''
df["WiFi_ThroughputTest"][0]["description"]: Wireless_PerformanceTest
'''
msg = 'df["WiFi_ThroughputTest"][0]["description"]: {}'
logger.info(msg.format( df["WiFi_ThroughputTest"][0]["description"]))

'''
df["WiFi_ThroughputTest"][1]["AC_88"]["wlan_ip_address"]: 192.168.0.101
'''
msg = 'df["WiFi_ThroughputTest"][1]["AC_88"]["wlan_ip_address"]: {}'
logger.info(msg.format( df["WiFi_ThroughputTest"][1]["AC_88"]["wlan_ip_address"]))


