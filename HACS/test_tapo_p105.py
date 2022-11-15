import asyncio
import argparse
import os, sys, time
import json
import re
from logger_setup import *

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

from plugp100 import TapoApiClient, TapoApiClientConfig, LightEffect

'''
How can I get the arp table from a windows machine using python?

https://stackoverflow.com/questions/59857314/how-can-i-get-the-arp-table-from-a-windows-machine-using-python
'''
def show_Windows_arp_table(target_mac_add, opt_verbose='OFF'):
    with os.popen('arp -a') as f:
        data = f.read()

    for line in re.findall('([-.0-9]+)\s+([-0-9a-f]{17})\s+(\w+)',data):
        if line[1].lower() == target_mac_add.lower():
            
            #192.168.3.9 00-e0-d8-1b-a8-ee 3
            #print(line[0], line[1], len(line))    
            if opt_verbose.lower() == 'on':
                msg = '\n target_mac_add: {}; target_ip_add: {}'.format(line[1], line[0] )
                logger.info(msg)
                #print(line[1].__Type__)

            return str(line[0])

async def main(ip_add, email, passwd):
    # create generic tapo api
    config = TapoApiClientConfig(ip_add, email, passwd)
    sw = TapoApiClient.from_config(config)
    await sw.login()
    await sw.on()
    await sw.set_brightness(100)
    state = await sw.get_state()
    print(state.get_unmapped_state())

    '''
    # light effect example
    await sw.set_light_effect(LightEffect.rainbow())
    state = await sw.get_state()
    print(state.get_unmapped_state())
    '''


'''
Simplest async/await example possible in Python
https://stackoverflow.com/questions/50757497/simplest-async-await-example-possible-in-python
'''
if __name__ == "__main__":
    logger_set(strdirname)

    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec)
    print(msg)

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--opt', action='store')
    parser.add_argument('-c', '--conf', action='store')   
    results = parser.parse_args()

    with open(results.conf, encoding= 'utf-8') as f:
        json_data= json.load(f)

    tapo_ip_add= ''    
    if results.opt.lower() == 'mac_add':
        tapo_ip_add= show_Windows_arp_table(json_data["mac_add"], opt_verbose= 'on')
    elif results.opt.lower() == 'ip_add':
        tapo_ip_add= json_data["ip_add"]
    
    email_add= json_data["email_add"]
    passwd= json_data["passwd"]
    
    loop = asyncio.get_event_loop()
    tasks = [
    loop.create_task(main(tapo_ip_add, email_add, passwd))
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    #loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()
    
    msg = 'Time consumption: {:.2f} secs.'.format(time.time() - t0 )
    print(msg)