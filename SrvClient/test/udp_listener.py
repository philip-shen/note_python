# https://gist.github.com/Lothiraldan/3951784

import socket

# Socket part
ANY = "0.0.0.0"
MCAST_ADDR = "237.252.249.227"
MCAST_PORT = 1600
#create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

#allow multiple sockets to use the same PORT number
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

#https://stackoverflow.com/questions/13637121/so-reuseport-is-not-defined-on-windows-7
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#Bind to the port that we know will receive multicast data
sock.bind((ANY, MCAST_PORT))

#tell the kernel that we are a multicast socket
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)

#Tell the kernel that we want to add ourselves to a multicast group
#The address for the multicast group is the third param
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
    socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))

while True:
    try:
        data, addr = sock.recvfrom(1024)
        #print ("Data, addr", data, addr)
        
        #https://stackoverflow.com/questions/33003498/typeerror-a-bytes-like-object-is-required-not-str
        print ("Data, addr", data.decode(), addr)
        
    except socket.error:
        pass