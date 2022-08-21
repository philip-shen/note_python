#!/usr/bin/python3

'''
    Public/Private chat for N users.
    
    Main things are:
    - GET a public board with messages
    - POST messages to this public board
    - GET a public list of currently connected users
    - SENT private messages to selected user
    - CHANGE name

    Author      : nngogol
    Created     : 2020-06-08 16:25:51
    Origin      : https://github.com/nngogol/async-desktop-chat
    pip install : pip install pysimplegui websockets

'''
import json, datetime, time, sys, os
import asyncio,  websockets,  uuid
from collections import namedtuple
from general_variables import PORT
import PySimpleGUI as sg

'''
import logging

logging.basicConfig(level=logging.INFO, 
                    format= '[%(asctime)s] - [line:%(lineno)d] - <%(threadName)s %(thread)d>' +
                    '- <Process %(process)d> - %(levelname)s: %(message)s'
)
'''

global_message_queue = asyncio.Queue()
global_websock = None
GLOBAL_my_name = ''

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)

dirnamelog=os.path.join(strdirname,"logs")
dirnametest=os.path.join(strdirname, 'test')
dirnamelib=os.path.join(strdirname,"libs")
dirnamekonf=os.path.join(strdirname,"konf")

sys.path.append(dirnamelib)
from logger import *
from lib_srv_client import get_host_port_globalserver, format_time

def today_date(): return datetime.datetime.now().strftime('%m-%d %H:%M:%S')
enable_print = True
def my_print(*args):
    if enable_print:
        print(*args)


def ui():
    '''

        return a PySimpleGUI layout

    '''
    global GLOBAL_my_name

    T_css = dict(font=("Helvetica", 12))

    users         = sg.Listbox([], size=(30-5, 16), enable_events=True, key='users')
    message_board = sg.ML(         size=(50-5, 15), key='messages_board')
    pm_board      = sg.ML(         size=(30-5, 16), key='pm_board')

    users_column = sg.Col([ [sg.T('Users:', **T_css)], [users]])
    message_board_column = sg.Col([
            [sg.T('Message board', **T_css)], [message_board]
           ,[sg.I(key='message', size=(15, 1)), sg.B('▲ Public', key='public-msg'), sg.B('▲ User', disabled=True, key='private-msg')]
    ])
    pm_column = sg.Col([[sg.T('PM messages', **T_css)], [pm_board] ])

    layout = [
        [sg.T('Your name'), sg.Input(GLOBAL_my_name, **T_css, disabled=True, use_readonly_for_disable=True, size=(30, 1), key='my_name'), sg.B('Change my name...', key='change-my-name')],
        [users_column, message_board_column, pm_column]
    ]
    return layout


async def gui_application():
    global global_message_queue, global_websock
    global GLOBAL_my_name
    while not GLOBAL_my_name:
        await asyncio.sleep(0.1)
        break
    
    try:
        window = sg.Window('Chat', ui(), finalize=True)
    except Exception as e:
        raise e
    
    while True:
        event, values = window(timeout=20)
        await asyncio.sleep(0.00001)
        if event in ('Exit', None): break
        if '__TIMEOUT__' != event: my_print(event)#, values)         # print event name
        
        # print(event)

        #=============
        # read a queue
        #=============
        try:
            if not global_message_queue.empty():
                while not global_message_queue.empty():
                    item = await global_message_queue.get()

                    my_print(f'Handle message ▼▼▼')
        
                    if not item or item is None:
                        my_print('Bad queue item', item)
                        break
                    
                    elif item['type'] == 'get-your-name':
                        my_name = item['name']
                        window['my_name'](my_name)
                        values['my_name'] = my_name
                        my_print(f'❄❄❄ my will be {my_name}')
                        global_message_queue.task_done(); my_print('Task done -=-=- (get-your-name)')

                    elif item['type'] == 'new_public_messages':
                        if item['messages_board']:
                            my_print('❄❄❄ new_public_messages')
    
                            mess = sorted(item['messages_board'], key=lambda x: x[0])
                            messages = '\n'.join(    [ '{}: {}'.format(m[1], m[2]) for m in mess]    )
    
                            # update board
                            window['messages_board'].update(messages)
                            global_message_queue.task_done(); my_print('Task done -=-=- (new_public_messages)')

                    elif item['type'] == 'new_user_state':
                        my_print('\n', '❄❄❄ new_user_state')
                        
                        my_name_val = values['my_name']
                        users_ = item['users']
                        filtered_users = [user_name for user_name in item['users'] if user_name != my_name_val]
                        window['users'].update(values=filtered_users)
                        
                        my_print('''my_name:   {}\nall_users: {}\nfiltered: {}\n'''.format(my_name_val, ','.join(users_), ','.join(filtered_users)))
                        global_message_queue.task_done(); my_print('Task done -=-=- (new_user_state)')

                    elif item['type'] == 'pm_message':
                        my_print('\n', '❄❄❄ pm_message')
                        
                        params = today_date(), item['author'], item['text']
                        window['pm_board'].print("{}  {: <30} : {}".format(*params))
                        global_message_queue.task_done(); my_print('Task done -=-=- (pm_message)')

                    elif item['type'] == 'change-my-name':
                        if item['status'] == 'ok':
                            new_name = item['new_name']
                            window['my_name'](new_name)
                            my_print('\n', '❄❄❄ change-my-name', f'\nnew name will be: {new_name}')

                        elif item['status'] == 'no':
                            sg.Popup(item['message'])

                        global_message_queue.task_done(); my_print('Task done -=-=- (change-my-name)')

                    elif item['type'] == 'exit':
                        my_print('\n', '❄❄❄ exit')
                        global_message_queue.task_done(); my_print('Task done exit -=-=- (exit)')
                        break
                    my_print(f'▲▲▲')

        except Exception as e: my_print(e, '-'*30)


        # if event == 'users' and values['users']:
        if values['users']:
            window['private-msg'](disabled=False)

        if event == 'change-my-name':
            new_name = sg.PopupGetText('New Name')
            if new_name:
                await global_websock.send(json.dumps({'action': 'change-my-name', "new_name": new_name}))

        if event == 'public-msg':
            message = json.dumps({'action': 'post-public-message', "text": values['message']})

            my_print(f"let's send public\nI will send: {message}")
            await global_websock.send(message)

            # clear GUI text element
            window['message']('')
        
        if event == 'private-msg':
        
            # validate
            if not values['users']:
                window['message'].update('Please, select the user first.')
                continue
        
            if not values['message'].strip():
                window['message'].update('Please, type a non-empty message.')
                continue
            
            my_print("Let's send pm")
            text = values['message']
            which_user_name = values['users'][0]
            message = json.dumps({
                'action': 'send-a-pm',
                "which_user_name": which_user_name,
                'text': text})

            my_print(f'I will send: {message}')
            await global_websock.send(message)

            # clear GUI text element
            window['pm_board'].print("{}  {: <30} : {}".format(today_date(), 'to:' + which_user_name, text))
            window['message']('')

    #
    # CLOSE
    #
    # -> psg close
    window.close()

    # -> websocket close
    if global_websock and not global_websock.closed:
        await global_websock.send(json.dumps({'action': 'exit'})) # disconnect me

async def cli_app(json_data, opt_verbose='OFF'):
    global global_message_queue, global_websock
    global GLOBAL_my_name
    while not GLOBAL_my_name:
        await asyncio.sleep(0.1)
        break

    while True:
        await asyncio.sleep(0.00001)
        #if event in ('Exit', None): break
        #if '__TIMEOUT__' != event: my_print(event)#, values)         # print event name
        # print(event)

        #=============
        # read a queue
        #=============
        try:
            if not global_message_queue.empty():
                while not global_message_queue.empty():
                    item = await global_message_queue.get()

                    logger.info('\n item: {}'.format(item) )

                    #my_print(f'Handle message ▼▼▼')
                    logger.info('\n Handle message ▼▼▼')
        
                    if not item or item is None:
                        #my_print('Bad queue item', item)
                        logger.info('\n Bad queue item: {}'.format(item) )
                        break
                    
                    elif item['type'] == 'get-your-name':
                        my_name = item['name']
                        #window['my_name'](my_name)
                        #values['my_name'] = my_name
                        my_print(f'❄❄❄ my will be {my_name}')
                        global_message_queue.task_done(); my_print('Task done -=-=- (get-your-name)')

                    elif item['type'] == 'new_public_messages':
                        if item['messages_board']:
                            my_print('❄❄❄ new_public_messages')
    
                            mess = sorted(item['messages_board'], key=lambda x: x[0])
                            messages = '\n'.join(    [ '{}: {}'.format(m[1], m[2]) for m in mess]    )
    
                            # update board
                            window['messages_board'].update(messages)
                            global_message_queue.task_done(); my_print('Task done -=-=- (new_public_messages)')

                    elif item['type'] == 'new_user_state':
                        #my_print('\n', '❄❄❄ new_user_state')
                        logging.info('\n ❄❄❄ new_user_state' )

                        my_name_val = json_data["my_name"]#;values['my_name']
                        users_ = item['users']
                        filtered_users = [user_name for user_name in item['users'] if user_name != my_name_val]
                        #window['users'].update(values=filtered_users)
                        
                        #my_print('''my_name:   {}\nall_users: {}\nfiltered: {}\n'''.format(my_name_val, ','.join(users_), ','.join(filtered_users)))
                        logging.info('\n my_name: {};\n all_users: {};\n filtered: {}'.format(\
                                        my_name_val, ','.join(users_), ','.join(filtered_users)) )
                        global_message_queue.task_done(); #my_print('Task done -=-=- (new_user_state)')
                        logging.info('\n Task done -=-=- (new_user_state)' )

                    elif item['type'] == 'pm_message':
                        my_print('\n', '❄❄❄ pm_message')
                        
                        params = today_date(), item['author'], item['text']
                        window['pm_board'].print("{}  {: <30} : {}".format(*params))
                        global_message_queue.task_done(); my_print('Task done -=-=- (pm_message)')

                    elif item['type'] == 'change-my-name':
                        if item['status'] == 'ok':
                            new_name = item['new_name']
                            window['my_name'](new_name)
                            my_print('\n', '❄❄❄ change-my-name', f'\nnew name will be: {new_name}')

                        elif item['status'] == 'no':
                            sg.Popup(item['message'])

                        global_message_queue.task_done(); my_print('Task done -=-=- (change-my-name)')

                    elif item['type'] == 'exit':
                        my_print('\n', '❄❄❄ exit')
                        global_message_queue.task_done(); my_print('Task done exit -=-=- (exit)')
                        break
                    my_print(f'▲▲▲')

        except Exception as e: my_print(e, '-'*30)

async def websocket_reading(host_ip, host_port):
    #global PORT, global_message_queue, global_websock, GLOBAL_my_name
    global global_message_queue, global_websock, GLOBAL_my_name
    try:
        # connect to a server
        #a_ws = await websockets.connect(f"ws://localhost:{PORT}")
        a_ws = await websockets.connect(f"ws://{host_ip}:{host_port}")
        global_websock = a_ws
        GLOBAL_my_name = json.loads(await a_ws.recv())['name']
        logger.info('\n Rec GLOBAL_my_name: {} from a_ws: {}'.format(GLOBAL_my_name, a_ws) )
        # # send "hello world" message
        #await a_ws.send(json.dumps({'action': 'post-public-message', "text": 'hello'}))
        dict_msg= {'action': 'change-my-name', 'new_name': 'audacity_srv'}
        await a_ws.send(json.dumps(dict_msg))

        # read messages, till you catch STOP message
        async for result in a_ws:
            json_msg = json.loads(result)
            logger.info('\n json_msg of result: {}'.format(json_msg) )

            # exit
            if json_msg['type'] == 'exit':
                break

            # put in global message queue
            await global_message_queue.put(json_msg)
    
        # close socket
        try: await a_ws.close()
        except Exception as e: print('Exception. cant close ws:', e)


    except Exception as e:
        #print('Exception. ws died: ', e)
        logger.info('\n Exception. ws died: {}'.format(e) )

async def websocket_transmit(dict_msg):
    global global_message_queue, global_websock, GLOBAL_my_name

    logger.info('\n TX: {} to core server '.format(dict_msg) )
    await global_websock.send(json.dumps( dict_msg ))

async def client(srv_ip, srv_port):
    await asyncio.wait([websocket_reading(srv_ip, srv_port), gui_application()])

async def cli_client(srv_ip, srv_port, json_data, dict_msg):
    await asyncio.wait([websocket_reading(srv_ip, srv_port), cli_app(json_data), \
                        websocket_transmit(dict_msg) ])

def main(srv_ip, srv_port, json_data, dict_msg):
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(client(srv_ip, srv_port))
    loop.run_until_complete(cli_client(srv_ip, srv_port, json_data, dict_msg))
    loop.close()

if __name__ == '__main__':
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))         
    
    if len(sys.argv) != 2:
        msg = 'Please input config json file!!! '
        logger.info(msg)
        sys.exit()

    json_file= sys.argv[1]

    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )
        sys.exit()
    
    with open(json_file, encoding="utf-8") as f:
        json_data = json.load(f) 

    opt_verbose='ON'
    #opt_verbose='OFF'
    
    
    cmd_srv_kconf= 'cmd_global_srv_3p187.csv'
    host_ip, host_port= get_host_port_globalserver(os.path.join(dirnamekonf, cmd_srv_kconf), opt_verbose)
    dict_msg= {'action': 'change-my-name', 'new_name': 'audacity_srv'}
    main(host_ip, host_port, json_data, dict_msg)
    #print('ended')

    time_consumption, h, m, s= format_time(time.time() - t0)         
    msg = 'Time Consumption: {} seconds.'#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time_consumption))     