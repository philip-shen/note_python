# https://gist.github.com/Lothiraldan/3951784

import socket

ANY = "0.0.0.0"
SENDERPORT = 32000
MCAST_ADDR = "237.252.249.227"
MCAST_PORT = 1600

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
    socket.IPPROTO_UDP)
sock.bind((ANY, 0))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#sock.sendto('Hi', (MCAST_ADDR, MCAST_PORT))

#https://stackoverflow.com/questions/33003498/typeerror-a-bytes-like-object-is-required-not-str
sock.sendto('Hi'.encode(), (MCAST_ADDR, MCAST_PORT))