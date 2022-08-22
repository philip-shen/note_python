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
    Created     : 2020-06-08 16:25:53
    Origin      : https://github.com/nngogol/async-desktop-chat
    pip install : pip install pysimplegui websockets

'''

import asyncio, json, websockets, datetime, time, sys, uuid
from collections import namedtuple
#from general_variables import PORT
import logging
import socket

#logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logging.basicConfig(level=logging.INFO, 
                    format= '[%(asctime)s] - [line:%(lineno)d] - <%(threadName)s %(thread)d>' +
                    '- <Process %(process)d> - %(levelname)s: %(message)s'
)

class User(object):
    def __init__(self, name, ws, uuid):
        self.name = name
        self.ws = ws
        self.uuid = uuid
        self.curr_ascii_img = ''
USERS = set()

Message = namedtuple('Message', 'time author_name text'.split(' '))
STATE = {
    "messages_board": [],
    "video_frames" : {}
}

def mk_uuid4(): return str(uuid.uuid4())

def state_event():
    global STATE
    if not STATE['messages_board']:
        return 
    return json.dumps({"type": "new_public_messages", 'messages_board' : STATE['messages_board']})

def get_available_name(websocket):
    global USERS
    names = [user.name for user in USERS]
    remote_address= websocket.remote_address[0]
    logging.info('\n remote_address: {}; remote_port: {}'.format(\
                    remote_address,  websocket.remote_address[1]) )
    
    #myname = f'user#{str(len(USERS)+0)}'
    myname = 'user#{}_{}'.format(str(len(USERS)+0), remote_address)
    for i in range(10_000_000):
        if myname not in names: break
        myname = 'user#{}_{}'.format(str(len(USERS)+i), remote_address )
    return myname

async def notify_state():
    global USERS, STATE

    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        if message:
            await asyncio.wait([user.ws.send(message) for user in USERS])
            logging.info('\n message from core server: {}'.format(message) )
            return
        #print('no messages to sent')
        logging.info('\n no messages to sent...')
        

    else:
        USERS = set()
        STATE['messages_board'] = []

def get_user_names(): return [user.name for user in USERS]

async def notify_users(skip_user=None):
    global USERS
    if not USERS: return 

    users_with_himself = USERS - set([skip_user]) if skip_user else USERS
    
    if len(users_with_himself) != 0: # asyncio.wait doesn't accept an empty list

        message_json = {'type': 'new_user_state', "users": get_user_names() }
        message = json.dumps(message_json)
        #print('I will send messages to: ', ','.join(message_json['users']))
        logging.info('\n I will send messages to: {}; \n message from srv: {}'.format(\
                        ','.join(message_json['users']),message ) )
        
        await asyncio.wait([ user.ws.send(message)
                             for user in users_with_himself])

async def notify_users_msg(msg, skip_user=None):
    global USERS
    if not USERS: return 

    users_with_himself = USERS - set([skip_user]) if skip_user else USERS
    
    if len(users_with_himself) != 0: # asyncio.wait doesn't accept an empty list
        message = json.dumps(msg)
        logging.info('\n message from core server: {}'.format(message ) )
        await asyncio.wait([ user.ws.send(message)
                             for user in users_with_himself])

    # for i in USERS:
    #                     await i.ws.send(json.dumps(data))

async def register(user):
    global USERS
    USERS.add(user)
    await notify_users()

async def unregister(user):
    global USERS
    
    if len(USERS) == 1 and list(USERS)[0] == user:
        USERS = set()
        STATE['messages_board'] = []
    if len(USERS) > 1:
        for auser in USERS: # set([i for id_, websocket in USERS if id_ == name]):
            if auser.name == user.name:
                USERS.remove(user)
                await notify_users()
                break

    #print(f'No users left.' if not USERS else f'# {len(USERS)} users online: ' + ', '.join(get_user_names()))
    logging.info('\n No users left.' if not USERS else \
                '\n {} users online: {}'.format (len(USERS), ', '.join(get_user_names()) ) )

async def on_ws_connected(websocket, path):
    # register(websocket) sends user_event() to websocket

    # add user to a list
    curr_user = User(get_available_name(websocket), websocket, mk_uuid4())
    
    logging.info('\n \'type\' : \'get-your-name\', \'name\' : {}'.format(curr_user.name ) )
    await websocket.send(json.dumps({'type' : 'get-your-name', 'name' : curr_user.name}))
    await register(curr_user)

    try:
        # show public board
        state = state_event()
        if state:
            await websocket.send(state)

        # READ messages from user
        # this for loop is live "infinite while true" loop.
        # It will end, end connection is dropped.

        async for message in websocket:
            data = json.loads(message)
            logging.info('\n data for core server: {}'.format(data ) )

            if data["action"] == "exit":
                # EXITING MESSAGE from user
                await curr_user.ws.send(json.dumps({'type': 'exit'}))
                await websocket.close()
                break

            ##################################################################################
            #                                                      _   _                     #
            #                                                     | | (_)                    #
            #     _   _ ___  ___ _ __    ___  _ __   ___ _ __ __ _| |_ _  ___  _ __  ___     #
            #    | | | / __|/ _ \ '__|  / _ \| '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \/ __|    #
            #    | |_| \__ \  __/ |    | (_) | |_) |  __/ | | (_| | |_| | (_) | | | \__ \    #
            #     \__,_|___/\___|_|     \___/| .__/ \___|_|  \__,_|\__|_|\___/|_| |_|___/    #
            #                                | |                                             #
            #                                |_|                                             #
            ##################################################################################
            elif data["action"] == "change-my-name":
                new_name = data["new_name"]

                # if there are user with name like our user wants:
                # -(stratergy)->  modify name a little bit
                # -(stratergy)-> ✔say no (all users must have uniq name)
                # -(stratergy)->  say yes (all users are identified by uuid on a server)
                filtered_users = [user_name for user_name in get_user_names() if user_name == new_name]
                if filtered_users:
                    await curr_user.ws.send(json.dumps({'type': 'change-my-name', 'status': 'no', 'message': 'name is taken'}))
                    continue

                curr_user.name = new_name
                await curr_user.ws.send( json.dumps({'type': 'change-my-name', 'status': 'ok', 'new_name': new_name}) )
                await notify_users(curr_user)

            ############################################################################
            #     _            _                                                       #
            #    | |          | |                                                      #
            #    | |_ _____  _| |_   _ __ ___   ___  ___ ___  __ _  __ _  ___  ___     #
            #    | __/ _ \ \/ / __| | '_ ` _ \ / _ \/ __/ __|/ _` |/ _` |/ _ \/ __|    #
            #    | ||  __/>  <| |_  | | | | | |  __/\__ \__ \ (_| | (_| |  __/\__ \    #
            #     \__\___/_/\_\\__| |_| |_| |_|\___||___/___/\__,_|\__, |\___||___/    #
            #                                                       __/ |              #
            #                                                      |___/               #
            ############################################################################
            elif data["action"] == "post-public-message":
                # This is "user to users" message
                STATE["messages_board"].append(
                    Message(time=time.time(),
                            author_name=curr_user.name,
                            text=data["text"]) )
                await notify_state()

            elif data["action"] == "send-a-pm":
                # This is "user to user" message
                # Don't record messages in servers logs
                target_user_name = data["which_user_name"]
                message_eater = [user for user in USERS if user.name == target_user_name][0]
                await message_eater.ws.send(json.dumps({'type': 'pm_message',
                                    'text': data["text"],
                                    'author': curr_user.name}))


            #                 _ _   _
            #                (_|_) (_)
            #   __ _ ___  ___ _ _   _ _ __ ___   __ _  __ _  ___
            #  / _` / __|/ __| | | | | '_ ` _ \ / _` |/ _` |/ _ \
            # | (_| \__ \ (__| | | | | | | | | | (_| | (_| |  __/
            #  \__,_|___/\___|_|_| |_|_| |_| |_|\__,_|\__, |\___|
            #                                          __/ |
            #                                         |___/
            # ON
            elif data["action"] == "update_my_ascii_frame": curr_user.curr_ascii_img = data["ascii_img"]
            # OFF
            elif data["action"] == "close_my_ascii_frame":  curr_user.curr_ascii_img = ''
            # SEND
            elif data["action"] == "view_ascii_frame":
                target_user_name = data["which_user_name"]
                message_eater = [user for user in USERS if user.name == target_user_name][0]
                ascii_img = message_eater.curr_ascii_img
                if ascii_img:
                    await curr_user.ws.send(json.dumps({'type': 'view_ascii_frame', 'status' : 'ok', 'ascii_img': ascii_img}))
                else:
                    await curr_user.ws.send(json.dumps({'type': 'view_ascii_frame', 'status' : 'empty'}))
            #   ___ __ _ _ ____   ____ _ ___
            #  / __/ _` | '_ \ \ / / _` / __|
            # | (_| (_| | | | \ V / (_| \__ \
            #  \___\__,_|_| |_|\_/ \__,_|___/

            elif data["action"] == "update_public_canvas":
                data['type'] = data['action']
                
                # forwarding
                await notify_users_msg(data)
                

            else:
                logging.info("\n unsupported event: {}".format(data))
        logging.info('\n Connection with user {} is done.'.format(curr_user.name) )
    except Exception as e:
        logging.info('\n Error with user:{} {}>'.format(curr_user.name, e) )
    logging.info('\n Unregistering user {}'.format(curr_user.name))
    await unregister(curr_user)
    logging.info('\n Bye, {}!'.format(curr_user.name) )

def get_local_ip_add():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return local_ip

def main(host_ip, host_port):
    #global PORT
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(websockets.serve(on_ws_connected, "localhost", PORT))
    loop.run_until_complete(websockets.serve(on_ws_connected, host_ip, host_port))
    
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        logging.info(f"{e.__class__.__name__} received")
    except Exception as e:
        logging.info(' Exception: {}...'.format(e))

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            logging.info(' Usage: python3 server.py <port>')
            sys.exit(1)
        else:
            host_port = int(sys.argv[1])
            host_ip= get_local_ip_add()
            logging.info('Server host_ip: {}; host_port: {}'.format(host_ip, host_port) )

            main(host_ip, host_port)
    except KeyboardInterrupt:
        logging.info(' Shutting down the server...')