#!/usr/bin/env python3
import os,sys
import time
from functools import partial
from multiprocessing import Pool
from concurrent import futures

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"log")
sys.path.append(dirnamelib)

from logger import logger
from common import *
from readConfig import *

def download_many(localReadConfig):
    
    remote_server_ip = localReadConfig.get_Client_Param('Remote_Server_IP')
    client_port = localReadConfig.get_Client_Param('Client_Port')
    client_protocol = localReadConfig.get_Client_Param('Client_Protocol')

    client_params = []
    for port in client_port.split(','):
        client_param = {
            'port': port,
            'protocol': client_protocol,
            'remote_server_ip': remote_server_ip
        }
        client_params.append(client_param)

    with futures.ProcessPoolExecutor(max_workers=16) as executor:  
        res = executor.map(client_siteone, client_params)  
                            
    return len(list(res))    

def download_many_udp(localReadConfig):
    
    remote_server_ip = localReadConfig.get_Client_Param('Remote_Server_IP')
    client_port = localReadConfig.get_Client_Param('Client_Port')
    client_protocol = localReadConfig.get_Client_Param('Client_Protocol')

    client_params = []
    for port in client_port.split(','):
        client_param = {
            'port': port,
            'protocol': client_protocol,
            'remote_server_ip': remote_server_ip
        }
        client_params.append(client_param)

    with futures.ProcessPoolExecutor(max_workers=16) as executor:  
        res = executor.map(client_siteone_udp, client_params)  
                            
    return len(list(res))

if __name__ == '__main__':
    t0 = time.time()
    
    str_inifile = 'config.ini'
    if len(sys.argv) == 1:
        str_inifile = 'config.ini'
    else: 
        str_inifile = sys.argv[1]

    localReadConfig = ReadConfig(str_inifile)
    client_protocol = localReadConfig.get_Client_Param('Client_Protocol')

    if client_protocol == 'tcp':
        count = download_many(localReadConfig)
    elif client_protocol == 'udp':
        count = download_many_udp(localReadConfig)
    else:  
        exit

    msg = '{} flags downloaded in {:.2f} seconds.'
    logger.info(msg.format(count, time.time() - t0)) 