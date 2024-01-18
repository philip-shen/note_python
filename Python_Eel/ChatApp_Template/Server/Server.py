import socket
import threading
import pickle
import os, sys
from logger_setup import *

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]

class User:
    
    username = ""
    password = ""
    address = ""
    currentRoom = ""
    conn = None
    
    def __init__(self, username = "", password = "", address = "", currentRoom = "room_0000", conn = None):
        
        self.username = username
        self.password = password
        self.address = address
        self.currentRoom = currentRoom
        self.conn = conn
        

def encrypt(obj):
    obj = pickle.dumps(obj)
    return obj

def decrypt(obj):
    obj = pickle.loads(obj)
    return obj


def getMessageType(message):
    
    typ = message[0]
    
    return typ

#Meant for individual sockets only!
def sendMessage(socket,message,hidePrint = False):
    
    user = ClientSockets[socket]
    
    if hidePrint == False:  
        #print(f"Attempting to send message: {message} |TO| {user.username} at {user.address}")
        msg=f"Attempting to send message: {message} |TO| {user.username} at {user.address}"
        logger.info(msg)
    message = pickle.dumps(message)
    
    socket.send(message)
    
    
def sendRoomMessage(room,message):
    
    global MessageRooms
    
    if room in MessageRooms:
        
        users = MessageRooms[room]
        
        for user in users:
            
            try:
            
                #sendMessage(user.conn,message,True)
                sendMessage(user.conn, message)
                
            except Exception as e:
                
                #print("Unable to send message to ", user.username, " , removing user from the room.")
                #print(e)
                msg="Unable to send message to ", user.username, " , removing user from the room."
                logger.info(msg)

                MessageRooms[room].remove(user)
            
    
def sendLeftMessage(username, room):
    
    message = ["MESSAGE",{
        "Author": "CONSOLE",
        "Message" : f"{username} has left the room!",
        "Room" : room
        }]
    
    sendRoomMessage(room, message)



def CreateRoom(socket,room):

    global MessageRooms
    
    currentRoomName = ClientSockets[socket].currentRoom
    
    userName = ClientSockets[socket].username
    
    if room not in MessageRooms.keys():
        
        user = ClientSockets[socket]
        
        #Create Room with the user in it
        currentRoom = MessageRooms[currentRoomName]
    
        #print("Attempt to disconnect user from current room!")
        msg="Attempt to disconnect user from current room!"
        logger.info(msg)
        
        currentRoom.remove(user)
        
        
        MessageRooms[room] = [user]
        
        user.currentRoom = room
        
        #Message to User socket
        message = ["CONSOLE","NEWROOM",room]
        
        sendMessage(socket, message)
        
        #print(f"{userName} has joined {room}")
        msg=f"{userName} has joined {room}"
        logger.info(msg)

        #Send message to everyone in the room
        message = ["MESSAGE",{
            "Author": "CONSOLE",
            "Message" : f"{userName} has joined the room!",
            "Room" : room
            }]
        
        sendRoomMessage(room, message)
        msg=f"room: {room}; message: {message}"
        logger.info(msg)

    else:
        
        #Join the room if it already exists but has no members! (Somehow the room did not delete)
        
        if len(MessageRooms[room]) <= 0:
        
            ConnectToRoom(socket, room)
             

def ConnectToRoom(socket,room):
    
    global MessageRooms
    
    currentRoomName = ClientSockets[socket].currentRoom
    
    userName = ClientSockets[socket].username
    
    if room in MessageRooms.keys():
        
        currentRoom = MessageRooms[currentRoomName]
        
        user = ClientSockets[socket]
        
        #print("Attempt to disconnect user from current room!")
        msg="Attempt to disconnect user from current room!"
        logger.info(msg)

        currentRoom.remove(user)
        
        targetRoom = MessageRooms[room]
        
        targetRoom.append(user)
        user.currentRoom = room
        #print(f"Connected {userName} to {room}!")
        msg=f"Connected {userName} to {room}!"
        logger.info(msg)

        message = ["CONSOLE","NEWROOM",room]
        
        sendMessage(socket, message)
        
        #Send message to everyone in the room
        message = ["MESSAGE",{
            "Author": "CONSOLE",
            "Message" : f"{userName} has joined the room!",
            "Room" : room
            }]
        
        sendRoomMessage(room, message)
        msg=f"message: {message}"
        logger.info(msg)

    else:
        #Optional.
        #CreateRoom(socket,room)
        pass
    
def LeaveRoom(socket,roomName):
    
    global MessageRooms
    
    #Make sure this room exists!
    fallBackRoom = "room_0000"
    
    userName = ClientSockets[socket].username
    
    currentRoomName = ClientSockets[socket].currentRoom
    
    if roomName in MessageRooms.keys():
        
        roomToLeave = MessageRooms[roomName]
          
    
        if roomName != fallBackRoom:
        
            #currentRoom = MessageRooms[currentRoomName]
            
            user = ClientSockets[socket]
            
            #print("Attempt to disconnect user from current room!")
            msg="Attempt to disconnect user from current room!"
            logger.info(msg)

            if user in roomToLeave:
            
                roomToLeave.remove(user)
            
                sendLeftMessage(userName, roomName)
            
            
            if roomName == currentRoomName:
            
                targetRoom = MessageRooms[fallBackRoom]
                
                targetRoom.append(user)
                user.currentRoom = fallBackRoom
                
                #print(f"Connected {userName} to {fallBackRoom}!")
                msg=f"Connected {userName} to {fallBackRoom}!"
                logger.info(msg)

                message = ["CONSOLE","NEWROOM",fallBackRoom]
                
                sendMessage(socket, message)
                msg=f"message: {message}"
                logger.info(msg)
            
            
            if len(roomToLeave) <= 0 :
                
                #print("Deleting {0} since there are no members in that room!".format(roomName))
                msg="Deleting {0} since there are no members in that room!".format(roomName)
                logger.info(msg)
                
                MessageRooms.pop(roomName)                
            else:                
                sendLeftMessage(userName,roomToLeave)


#Function that handles individual clients
def HandleClient(conn, addr):
    
    global ClientSockets
    global MessageRooms
    
    #print("Getting connection request...")
    msg="Getting connection request..."
    logger.info(msg)

    Username = ""
    
    connected = True
    while connected:
        
        try:
        
            msg = conn.recv(MaxBytes)
            
            if msg == b'':
                connected = False
                break
            
            msg = decrypt(msg)
            logger.info(f"msg: {msg}")

            msgType = getMessageType(msg)
            
            if msgType == "CONNECT":
                
                Username = msg[1]
                
                user = User(
                    username=Username,
                    password ="",
                    address = addr,
                    currentRoom="room_0000",
                    conn = conn
                    )
                
                ClientSockets[conn] = user
            
                MessageRooms["room_0000"].append(user)
            
                message = ["CONSOLE","CONNECTED!"]
                
                #print(f"{Username} has connected to the server with IP {addr}")
                msg= f"{Username} has connected to the server with IP {addr}"
                logger.info(msg)

                sendMessage(conn, message)
                
                print("")
                
                #print("Sending welcome room message!")
                msg= "Sending welcome room message!"
                logger.info(msg)

                message = ["MESSAGE",{
                    "Author": "CONSOLE",
                    "Message" : f"{Username} has joined the room!",
                    "Room" : "room_0000"
                    }]
                
                sendRoomMessage("room_0000", message)
                
                #print("messages sent!")
                msg= f"messages: {message} sent!"
                logger.info(msg)
                
            elif msgType == "JOIN_ROOM":
                
                ConnectToRoom(conn,msg[1])
                
            elif msgType == "CREATE_ROOM":
                
                CreateRoom(conn, msg[1])
                
            elif msgType == "LEAVE_ROOM":
                
                LeaveRoom(conn,msg[1])
                
            elif msgType == "MESSAGE":
                
                currentRoom = ClientSockets[conn].currentRoom
                
                message = ["MESSAGE",{
                    "Author": Username,
                    "Message" : msg[1],
                    "Room" : currentRoom
                    }]
                
                sendRoomMessage(currentRoom, message)
                msg= f"messages: {message} sent!"
                logger.info(msg)

            elif msgType == "DISCONNECT":
                
                #print(f"{Username} has disconnected!")
                msg= f"{Username} has disconnected!"
                logger.info(msg)

                connected = False
                break
            
        except ConnectionError as e:
            
            #print("Connection error! Disconnecting User! Details: ",e)
            msg= f"Connection error! Disconnecting User! Details: {e}"
            logger.info(msg)
            connected = False
            
        except ConnectionAbortedError as e:
            
            #print("Connection aborted!", e)
            msg= "Connection aborted! {e}"
            logger.info(msg)
            connected = False
            
        except ConnectionRefusedError as e:
            
            #print("Connnection refused!",e)
            msg= "Connection refused! {e}"
            logger.info(msg)

        except Exception as e :
            
            #print(e)
            logger.info(e)
            connected = False
            
            
    clientUserObject = ClientSockets[conn]
    currentRoom = clientUserObject.currentRoom
    MessageRooms[currentRoom].remove(clientUserObject)
    ClientSockets.pop(conn)  
    
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    
    sendLeftMessage(Username,currentRoom)
    
    #print(ClientSockets)
    msg= f"ClientSockets: {ClientSockets}"
    logger.info(msg)

if __name__ == '__main__':
    logger_set(prevdirname)
    
    HOST = "0.0.0.0"#"192.168.3.192"
    PORT = 5050
    MaxBytes = 2097152

    #print("Initialising the Server...")
    msg="Initialising the Server..."
    logger.info(msg)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("Server Socket initialised successfully")
    msg=f"Server Socket:{serversocket} \ninitialised successfully"
    logger.info(msg)

    #print("Binding Host...")
    msg="Binding Host..."
    logger.info(msg)
    serversocket.bind((HOST, PORT))
    #print("Socket binded:{}:{}!".format(HOST, PORT))
    msg=f"Socket binded:{HOST}:{PORT}!"
    logger.info(msg)

    ClientSockets = {}

    #room_0000 refers to the public room!
    MessageRooms = {
        "room_0000" : []
    }

    
    serversocket.listen()
    #print("Server up and running!")
    msg="Server up and running!"
    logger.info(msg)

    while True:
        conn, addr = serversocket.accept()
        clientThread = threading.Thread(target=HandleClient, args=(conn,addr))
        clientThread.start()
    
        #print("Active Connections : {}".format(threading.active_count()-1))
        msg="Active Connections : {}".format(threading.active_count()-1)
        logger.info(msg)

    print("Shutting Down...")
    serversocket.close()