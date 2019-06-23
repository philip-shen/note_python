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
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger
from common import *
from readConfig import *
import ipaddress 


def download_many(localReadConfig):
    '''多进程，按进程数 并行 下载所有图片
    使用concurrent.futures.ProcessPoolExecutor()
    Executor.map()使用Future而不是返回Future，它返回迭代器，
    迭代器的__next__()方法调用各个Future的result()方法，因此我们得到的是各个Future的结果，而非Future本身

    注意Executor.map()限制了download_one()只能接受一个参数，所以images是字典构成的列表
    '''
    server_port = localReadConfig.get_Server_Param('Server_Port')
    server_protocol = localReadConfig.get_Server_Param('Server_Protocol')

    server_params = []
    for port in server_port.split(','):
        srv_param = {
            'port': port,
            'protocol': server_protocol
        }
        server_params.append(srv_param)

    # with语句将调用executor.__exit__()方法，而这个方法会调用executor.shutdown(wait=True)方法，它会在所有进程都执行完毕前阻塞主进程
    with futures.ProcessPoolExecutor(max_workers=16) as executor:  # 不指定max_workers时，进程池中进程个数默认为os.cpu_count()
        # executor.map()效果类似于内置函数map()，但download_one()函数会在多个进程中并行调用
        # 它的返回值res是一个迭代器<itertools.chain object>，我们后续可以迭代获取各个被调用函数的返回值
        res = executor.map(server_siteone, server_params)  # 传一个序列

    return len(list(res))  # 如果有进程抛出异常，异常会在这里抛出，类似于迭代器中隐式调用next()的效果

def download_many_udp(localReadConfig):
    server_ip = localReadConfig.get_Server_Param('Server_IP')
    server_port = localReadConfig.get_Server_Param('Server_Port')
    server_protocol = localReadConfig.get_Server_Param('Server_Protocol')

    server_params = []
    for port in server_port.split(','):
        srv_param = {
            'host': server_ip,
            'port': port,
            'protocol': server_protocol
        }
        server_params.append(srv_param)    

    with futures.ProcessPoolExecutor(max_workers=16) as executor:
        res = executor.map(server_siteone_socket_udp, server_params)

    return len(list(res))

def download_many_udp_ipv6(localReadConfig):
    server_ip = localReadConfig.get_Server_Param('Server_IP')
    server_port = localReadConfig.get_Server_Param('Server_Port')
    server_protocol = localReadConfig.get_Server_Param('Server_Protocol')

    server_params = []
    for port in server_port.split(','):
        srv_param = {
            'host': server_ip,
            'port': port,
            'protocol': server_protocol
        }
        server_params.append(srv_param)    

    with futures.ProcessPoolExecutor(max_workers=16) as executor:
        res = executor.map(server_siteone_socket_udp_ipv6, server_params)

    return len(list(res))

def download_many_udp_multicast(localReadConfig):
    server_ip = localReadConfig.get_Server_Param('Server_IP')
    server_port = localReadConfig.get_Server_Param('Server_Port')
    server_protocol = localReadConfig.get_Server_Param('Server_Protocol')

    server_params = []
    for port in server_port.split(','):
        srv_param = {
            'host': server_ip,
            'port': port,
            'protocol': server_protocol
        }
        server_params.append(srv_param)    

    with futures.ProcessPoolExecutor(max_workers=16) as executor:
        res = executor.map(server_siteone_socket_udp_mutlicast, server_params)

    return len(list(res))

def download_many_udp_multicast_ipv6(localReadConfig):
    server_ip = localReadConfig.get_Server_Param('Server_IP')
    server_port = localReadConfig.get_Server_Param('Server_Port')
    server_protocol = localReadConfig.get_Server_Param('Server_Protocol')

    server_params = []
    for port in server_port.split(','):
        srv_param = {
            'host': server_ip,
            'port': port,
            'protocol': server_protocol
        }
        server_params.append(srv_param)    

    with futures.ProcessPoolExecutor(max_workers=16) as executor:
        res = executor.map(server_siteone_socket_udp_mutlicast_ipv6, server_params)

    return len(list(res))

if __name__ == '__main__':
    t0 = time.time()

    str_inifile = 'config.ini'
    if len(sys.argv) == 1:
        str_inifile = 'config.ini'
    else: 
        str_inifile = sys.argv[1]

    localReadConfig = ReadConfig(str_inifile)
    server_ip = localReadConfig.get_Server_Param('Server_IP')
    server_protocol = localReadConfig.get_Server_Param('Server_Protocol')

    if server_protocol == 'tcp':
        count = download_many(localReadConfig)
    elif (server_protocol == 'udp' and ipaddress.ip_address(server_ip).version == 4 \
                                    and not ipaddress.ip_address(server_ip).is_multicast): 
        count = download_many_udp(localReadConfig)

    elif (server_protocol == 'udp' and ipaddress.ip_address(server_ip).version == 6 \
                                    and not ipaddress.ip_address(server_ip).is_multicast):  
        count = download_many_udp_ipv6(localReadConfig)
    
    elif (server_protocol == 'udp' and ipaddress.ip_address(server_ip).version == 4 \
                                    and ipaddress.ip_address(server_ip).is_multicast): 
        count = download_many_udp_multicast(localReadConfig)        

    elif (server_protocol == 'udp' and ipaddress.ip_address(server_ip).version == 6\
                                    and ipaddress.ip_address(server_ip).is_multicast): 
        count = download_many_udp_multicast_ipv6(localReadConfig)

    else:  
        exit

    msg = '{} flags downloaded in {:.2f} seconds.'
    logger.info(msg.format(count, time.time() - t0))    