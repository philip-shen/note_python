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
import ipaddress 

def download_many(localReadConfig):
    
    remote_server_ip = localReadConfig.get_Client_Param('Remote_Server_IP')
    client_port = localReadConfig.get_Client_Param('Client_Port')
    client_protocol = localReadConfig.get_Client_Param('Client_Protocol')
    test_duration = localReadConfig.get_Client_Param('Test_Duration')

    client_params = []
    for port in client_port.split(','):
        client_param = {
            'port': port,
            'protocol': client_protocol,
            'remote_server_ip': remote_server_ip,
            'test_duration' : test_duration
        }
        client_params.append(client_param)

    with futures.ProcessPoolExecutor(max_workers=16) as executor:  
        res = executor.map(client_siteone, client_params)  
                            
    return len(list(res))    

def download_many_continuous(localReadConfig):
    
    remote_server_ip = localReadConfig.get_Client_Param('Remote_Server_IP')
    client_port = localReadConfig.get_Client_Param('Client_Port')
    client_protocol = localReadConfig.get_Client_Param('Client_Protocol')
    test_duration = localReadConfig.get_Client_Param('Test_Duration')

    client_params = []
    for port in client_port.split(','):
        client_param = {
            'port': port,
            'protocol': client_protocol,
            'remote_server_ip': remote_server_ip,
            'test_duration' : test_duration
        }
        client_params.append(client_param)

    with futures.ProcessPoolExecutor(max_workers=16) as executor:  
        res = executor.map(client_siteone_continuous, client_params)  
                            
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

def download_many_socket_udp(localReadConfig):
    
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
        res = executor.map(client_siteone_socket_udp, client_params)  
                            
    return len(list(res))

def download_many_socket_udp_continuous(localReadConfig):
    remote_server_ip = localReadConfig.get_Client_Param('Remote_Server_IP')
    client_port = localReadConfig.get_Client_Param('Client_Port')
    client_protocol = localReadConfig.get_Client_Param('Client_Protocol')
    test_duration = localReadConfig.get_Client_Param('Test_Duration')

    client_params = []
    for port in client_port.split(','):
        client_param = {
            'port': port,
            'protocol': client_protocol,
            'remote_server_ip': remote_server_ip,
            'test_duration' : test_duration
        }
        client_params.append(client_param)

    with futures.ProcessPoolExecutor(max_workers=16) as executor:  
        res = executor.map(client_siteone_socket_udp_continuous, client_params)  
                            
    return len(list(res))

def download_many_socket_udp_ipv6(localReadConfig):
    
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
        res = executor.map(client_siteone_socket_udp_ipv6, client_params)  
                            
    return len(list(res))

def download_many_socket_udp_ipv6_continuous(localReadConfig):
    
    remote_server_ip = localReadConfig.get_Client_Param('Remote_Server_IP')
    client_port = localReadConfig.get_Client_Param('Client_Port')
    client_protocol = localReadConfig.get_Client_Param('Client_Protocol')
    test_duration = localReadConfig.get_Client_Param('Test_Duration')

    client_params = []
    for port in client_port.split(','):
        client_param = {
            'port': port,
            'protocol': client_protocol,
            'remote_server_ip': remote_server_ip,
            'test_duration' : test_duration
        }
        client_params.append(client_param)

    with futures.ProcessPoolExecutor(max_workers=16) as executor:  
        res = executor.map(client_siteone_socket_udp_ipv6_continuous, client_params)  
                            
    return len(list(res))

def download_many_socket_udp_multicast(localReadConfig):
    
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
        res = executor.map(client_siteone_socket_udp_mutlicast, client_params)  
                            
    return len(list(res))

def download_many_socket_udp_multicast_ipv6(localReadConfig):
    
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
        res = executor.map(client_siteone_socket_udp_mutlicast_ipv6, client_params)  
                            
    return len(list(res))    

if __name__ == '__main__':
    t0 = time.time()
    
    str_inifile = 'config.ini'
    if len(sys.argv) == 1:
        str_inifile = 'config.ini'
    else: 
        str_inifile = sys.argv[1]

    localReadConfig = ReadConfig(str_inifile)
    remote_server_ip = localReadConfig.get_Client_Param('Remote_Server_IP')   
    client_protocol = localReadConfig.get_Client_Param('Client_Protocol')
    
    if client_protocol == 'tcp':
        #count = download_many(localReadConfig)

        """Error msg
        2019-06-30 13:33:27,856 - common.py[line:428] - <MainThread -1219938560>- <Process 23772> - INFO: Connecting to 127.0.0.1:25:tcp
        2019-06-30 13:33:27,856 - common.py[line:432] - <MainThread -1219938560>- <Process 23772> - INFO: unable to send cookie to server: 
        2019-06-30 13:33:27,857 - common.py[line:428] - <MainThread -1219938560>- <Process 23773> - INFO: Connecting to 127.0.0.1:80:tcp
        2019-06-30 13:33:27,857 - common.py[line:432] - <MainThread -1219938560>- <Process 23773> - INFO: unable to send cookie to server: 
        2019-06-30 13:33:30,861 - common.py[line:428] - <MainThread -1219938560>- <Process 23772> - INFO: Connecting to 127.0.0.1:25:tcp
        2019-06-30 13:33:30,861 - common.py[line:432] - <MainThread -1219938560>- <Process 23772> - INFO: unable to send cookie to server: 
        2019-06-30 13:33:30,862 - common.py[line:428] - <MainThread -1219938560>- <Process 23773> - INFO: Connecting to 127.0.0.1:80:tcp
        2019-06-30 13:33:30,862 - common.py[line:432] - <MainThread -1219938560>- <Process 23773> - INFO: unable to send cookie to server: 
        2019-06-30 13:33:33,866 - common.py[line:428] - <MainThread -1219938560>- <Process 23772> - INFO: Connecting to 127.0.0.1:25:tcp
        2019-06-30 13:33:33,866 - common.py[line:432] - <MainThread -1219938560>- <Process 23772> - INFO: unable to send cookie to server: 
        2019-06-30 13:33:33,867 - common.py[line:428] - <MainThread -1219938560>- <Process 23773> - INFO: Connecting to 127.0.0.1:80:tcp
        2019-06-30 13:33:33,867 - common.py[line:432] - <MainThread -1219938560>- <Process 23773> - INFO: unable to send cookie to server: 

        2019-06-30 13:23:45,502 - common.py[line:428] - <MainThread -1219238144>- <Process 23492> - INFO: Connecting to 2001:b011:20e0:32ec:20c:29ff:fed5:be92:80:tcp
        2019-06-30 13:23:45,502 - common.py[line:432] - <MainThread -1219238144>- <Process 23492> - INFO: unable to connect to server: 
        2019-06-30 13:23:46,684 - common.py[line:428] - <MainThread -1219238144>- <Process 23493> - INFO: Connecting to 2001:b011:20e0:32ec:20c:29ff:fed5:be92:25:tcp
        2019-06-30 13:23:46,685 - common.py[line:432] - <MainThread -1219238144>- <Process 23493> - INFO: unable to send cookie to server: 
        2019-06-30 13:23:48,506 - common.py[line:428] - <MainThread -1219238144>- <Process 23492> - INFO: Connecting to 2001:b011:20e0:32ec:20c:29ff:fed5:be92:80:tcp
        2019-06-30 13:23:48,507 - common.py[line:432] - <MainThread -1219238144>- <Process 23492> - INFO: unable to connect to server: 
        2019-06-30 13:23:49,689 - common.py[line:428] - <MainThread -1219238144>- <Process 23493> - INFO: Connecting to 2001:b011:20e0:32ec:20c:29ff:fed5:be92:25:tcp
        2019-06-30 13:23:49,690 - common.py[line:432] - <MainThread -1219238144>- <Process 23493> - INFO: unable to send cookie to server: 
        """
        count = download_many_continuous(localReadConfig)
    
    elif (client_protocol == 'udp' and ipaddress.ip_address(remote_server_ip).version == 4 \
                                    and not ipaddress.ip_address(remote_server_ip).is_multicast): 
        
        #count = download_many_socket_udp(localReadConfig)
        count = download_many_socket_udp_continuous(localReadConfig)

    elif (client_protocol == 'udp' and ipaddress.ip_address(remote_server_ip).version == 6\
                                    and not ipaddress.ip_address(remote_server_ip).is_multicast): 
        
        #count = download_many_socket_udp_ipv6(localReadConfig)
        count = download_many_socket_udp_ipv6_continuous(localReadConfig)
    
    elif (client_protocol == 'udp' and ipaddress.ip_address(remote_server_ip).version == 4 \
                                    and ipaddress.ip_address(remote_server_ip).is_multicast):
        count = download_many_socket_udp_multicast(localReadConfig)        

    elif (client_protocol == 'udp' and ipaddress.ip_address(remote_server_ip).version == 6 \
                                    and ipaddress.ip_address(remote_server_ip).is_multicast):
        count = download_many_socket_udp_multicast_ipv6(localReadConfig)            
    else:  
        exit

    msg = '{} flags downloaded in {:.2f} seconds.'
    logger.info(msg.format(count, time.time() - t0)) 