# https://gist.github.com/tuxmartin/e64d2132061ffef7e031
import socket

UDP_IP = "::1"  # localhost
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print("UDP target IP:", UDP_IP) 
print("UDP target port:", UDP_PORT) 
print("message:", MESSAGE) 

sock = socket.socket(socket.AF_INET6, # Internet
					socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))