#!/usr/bin/env python3

import os,time,sys
import sys
import iperf3
import socket 
import struct
import threading 

from logger import logger

def server_siteone(parms):
    server = iperf3.Server()
    server.port = parms['port']
    server.protocol = parms['protocol']

    #print('Running server: {0}:{1}'.format(server.bind_address, server.port))
    logger.info('Running server: {0}:{1}:{2}'.format(server.bind_address, server.port, server.protocol))

    while True:
        try:
            result = server.run()

            if result.error:
                #print(result.error)
                logger.info(result.error)
            else:
                print('')
                
                logger.info('Test results from {0}:{1} to {2}'.format(result.remote_host,
                                                    result.remote_port,result.local_port))
                
                logger.info('  started at         {0}'.format(result.time))
                logger.info('  bytes received     {0}'.format(result.received_bytes))

                logger.info('Average transmitted received in all sorts of networky formats:')

                logger.info('  bits per second      (bps)   {0}'.format(result.received_bps))
                logger.info('  Kilobits per second  (kbps)  {0}'.format(result.received_kbps))
                logger.info('  Megabits per second  (Mbps)  {0}'.format(result.received_Mbps))
                logger.info('  KiloBytes per second (kB/s)  {0}'.format(result.received_kB_s))
                logger.info('  MegaBytes per second (MB/s)  {0}'.format(result.received_MB_s))

        except KeyboardInterrupt:
            pass     

def client_siteone(parms):
    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = parms['remote_server_ip']
    client.port = parms['port']
    client.protocol = parms['protocol']
    client.duration = int(parms['test_duration'])

    logger.info('Connecting to {0}:{1}:{2}'.format(client.server_hostname, client.port, client.protocol))
    result = client.run()

    if result.error:
        logger.info(result.error)
    else:
        print('')
        logger.info('Test completed:')
        logger.info('  started at         {0}'.format(result.time))
        logger.info('  bytes transmitted  {0}'.format(result.sent_bytes))
        logger.info('  retransmits        {0}'.format(result.retransmits))
        logger.info('  avg cpu load       {0}%\n'.format(result.local_cpu_total))

        logger.info('Average transmitted data in all sorts of networky formats:')
        logger.info('  bits per second      (bps)   {0}'.format(result.sent_bps))
        logger.info('  Kilobits per second  (kbps)  {0}'.format(result.sent_kbps))
        logger.info('  Megabits per second  (Mbps)  {0}'.format(result.sent_Mbps))
        logger.info('  KiloBytes per second (kB/s)  {0}'.format(result.sent_kB_s))
        logger.info('  MegaBytes per second (MB/s)  {0}'.format(result.sent_MB_s))

def client_siteone_udp(parms):
    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = parms['remote_server_ip']
    client.port = parms['port']
    client.protocol = parms['protocol']

    logger.info('Connecting to {0}:{1}:{2}'.format(client.server_hostname, client.port, client.protocol))
    result = client.run()

    if result.error:
        logger.info(result.error)
    else:
        print('')
        logger.info('Test completed:')
        logger.info('  started at         {0}'.format(result.time))
        logger.info('  bytes transmitted  {0}'.format(result.bytes))
        logger.info('  jitter (ms)        {0}'.format(result.jitter_ms))
        logger.info('  avg cpu load       {0}%\n'.format(result.local_cpu_total))

        logger.info('Average transmitted data in all sorts of networky formats:')
        logger.info('  bits per second      (bps)   {0}'.format(result.bps))
        logger.info('  Kilobits per second  (kbps)  {0}'.format(result.kbps))
        logger.info('  Megabits per second  (Mbps)  {0}'.format(result.Mbps))
        logger.info('  KiloBytes per second (kB/s)  {0}'.format(result.kB_s))
        logger.info('  MegaBytes per second (MB/s)  {0}'.format(result.MB_s))        

#https://subscription.packtpub.com/book/networking_and_servers/9781786463999/1/ch01lvl1sec24/writing-a-simple-udp-echo-client-server-application

def server_siteone_socket_udp(parms):
    """ A simple echo server """ 
    server_host = parms['host']
    server_port = parms['port']
    server_protocol = parms['protocol']
    data_payload = 2048

    # Create a UDP socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    # Bind the socket to the port(type int) 
    server_address = (server_host, int(server_port)) 
    
    logger.info("Starting up echo server on %s port %s" % server_address) 

    sock.bind(server_address) 

    while True: 
        try:
            #print ("  ")                
            logger.info("Waiting to receive message from client") 
            data, address = sock.recvfrom(data_payload) 
     
            logger.info("received %s bytes from %s to port: %s" % (len(data), address, server_port)) 
            logger.info("Data: %s" %data) 
     
            if data: 
                sent = sock.sendto(data, address) 
                logger.info("sent %s bytes back to %s" % (sent, address)) 

        except KeyboardInterrupt:
            pass        

def client_siteone_socket_udp(parms):
    client_server_hostname = parms['remote_server_ip']
    client_port = parms['port']
    client_protocol = parms['protocol']
    data_payload = 2048

    """ A simple echo client """ 
    # Create a UDP socket 
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
 
    server_address = (client_server_hostname, int(client_port)) 
    logger.info("Connecting to %s port %s" % server_address) 
    
    try: 
        # Send data 
        message = "Test message. This will be echoed" 
        logger.info("Sending %s" % message) 
        sent = sock.sendto(message.encode('utf-8'), server_address) 
 
        # Receive response 
        data, server = sock.recvfrom(data_payload) 
        logger.info("received %s" % data)
    
    finally: 
        logger.info("Closing connection to the server") 
        sock.close()                   

    
# https://gist.github.com/Lothiraldan/3951784
ANY = "0.0.0.0"
def server_siteone_socket_udp_mutlicast(parms):
    # Socket part
    server_host = parms['host']
    server_port = parms['port']
    server_protocol = parms['protocol']
    
    #MCAST_ADDR = "237.252.249.227"
    #MCAST_PORT = 1600
    #create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    #allow multiple sockets to use the same PORT number
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    
    # Bind the socket to the port(type int) 
    server_address = (server_host, int(server_port)) 
    logger.info("Starting up Multicast server on %s port %s" % server_address) 

    #Bind to the port that we know will receive multicast data
    #sock.bind((ANY, int(server_port)))    
    sock.bind(server_address)

    #tell the kernel that we are a multicast socket
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)

    #Tell the kernel that we want to add ourselves to a multicast group
    #The address for the multicast group is the third param
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(server_host) + socket.inet_aton(ANY))

    while True:
        try:
            logger.info("Waiting to receive message from client")        
            data, addr = sock.recvfrom(1024)

            logger.info("received %s bytes from %s to port: %s" % (len(data), addr, server_port)) 
            
            #https://stackoverflow.com/questions/33003498/typeerror-a-bytes-like-object-is-required-not-str
            logger.info ("Data: {}, addr: {}".format(data.decode(), addr))
        
        except socket.error:
            pass
        except KeyboardInterrupt:
            pass                        

def client_siteone_socket_udp_mutlicast(parms):
    # Socket part
    client_server_hostname = parms['remote_server_ip']
    client_port = parms['port']
    client_protocol = parms['protocol']

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP)
    sock.bind((ANY, 0))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = (client_server_hostname, int(client_port)) 
    logger.info("Connecting to %s port %s" % server_address) 

    message = "Test message. It will be Mutlicast"
    logger.info("Sending %s" % message) 
                 
    #https://stackoverflow.com/questions/33003498/typeerror-a-bytes-like-object-is-required-not-str
    sock.sendto(message.encode(), (client_server_hostname, int(client_port)) )


# https://gist.github.com/tuxmartin/e64d2132061ffef7e031
def server_siteone_socket_udp_ipv6(parms):
    """ A simple echo server """ 
    server_host = parms['host']
    server_port = parms['port']
    server_protocol = parms['protocol']
    data_payload = 2048

    # Create a UDP socket 
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) 

    # Bind the socket to the port(type int) 
    server_address = (server_host, int(server_port)) 
    
    logger.info("Starting up UDP echo server on %s port %s" % server_address) 

    sock.bind(server_address) 

    while True: 
        try:
            #print ("  ")                
            logger.info("Waiting to receive message from client") 
            data, address = sock.recvfrom(data_payload) 
     
            logger.info("received %s bytes from %s to port: %s" % (len(data), address, server_port)) 
            logger.info("Data: %s" %data) 
     
            if data: 
                sent = sock.sendto(data, address) 
                logger.info("sent %s bytes back to %s" % (sent, address)) 

        except KeyboardInterrupt:
            pass    

def client_siteone_socket_udp_ipv6(parms):
    client_server_hostname = parms['remote_server_ip']
    client_port = parms['port']
    client_protocol = parms['protocol']
    data_payload = 2048

    """ A simple echo client """ 
    # Create a UDP socket 
    sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM) 
 
    server_address = (client_server_hostname, int(client_port)) 
    logger.info("Connecting to %s port %s" % server_address) 
    
    try: 
        # Send data 
        message = "Test message. This will be echoed" 
        logger.info("Sending %s" % message) 
        sent = sock.sendto(message.encode('utf-8'), server_address) 
 
        # Receive response 
        data, server = sock.recvfrom(data_payload) 
        logger.info("received %s" % data)
    
    finally: 
        logger.info("Closing connection to the server") 
        sock.close()             

def server_siteone_socket_udp_mutlicast_ipv6(parms):
    # Socket part
    server_host = parms['host']
    server_port = parms['port']
    server_protocol = parms['protocol']
    
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(server_host, None)[0]

    # Create a socket
    #sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    #allow multiple sockets to use the same PORT number
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # Bind the socket to the port(type int) 
    server_address = (server_host, int(server_port)) 
    logger.info("Starting up Multicast server on %s port %s" % server_address) 

    #Bind to the port that we know will receive multicast data
    sock.bind(server_address)

    #tell the kernel that we are a multicast socket
    #sock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL, 255)

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    #Tell the kernel that we want to add ourselves to a multicast group
    #The address for the multicast group is the third param 
    mreq = group_bin + struct.pack('@I', 0)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    while True:
        try:
            logger.info("Waiting to receive message from client")        
            data, addr = sock.recvfrom(1024)

            logger.info("received %s bytes from %s to port: %s" % (len(data), addr, server_port)) 
            
            #https://stackoverflow.com/questions/33003498/typeerror-a-bytes-like-object-is-required-not-str
            logger.info ("Data: {}, addr: {}".format(data.decode(), addr))
        
        except socket.error:
            pass 
        except KeyboardInterrupt:
            pass                        

MYTTL = 1 # Increase to reach other networks
def client_siteone_socket_udp_mutlicast_ipv6(parms):
    # Socket part
    client_server_hostname = parms['remote_server_ip']
    client_port = parms['port']
    client_protocol = parms['protocol']

    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(client_server_hostname, None)[0]

    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    #sock.bind((ANY, 0))

    # Set Time-to-live (optional)
    ttl_bin = struct.pack('@i', MYTTL)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = (client_server_hostname, int(client_port)) 
    logger.info("Connecting to %s port %s" % server_address) 

    message = "Test message. It will be Mutlicast"
    logger.info("Sending %s" % message) 
                 
    #https://stackoverflow.com/questions/33003498/typeerror-a-bytes-like-object-is-required-not-str
    sock.sendto(message.encode(), (client_server_hostname, int(client_port)) )

def func():
    pass

def continuous_clock_timer(duration_sec):
    #print('Timer start，press"Enter" button to calcuate interval，Press "Ctrl+C" to escape timer.')
    #in_value = input()
    #if in_value == 'exit':
    #    return
    print('Start Time Duratin:{} sec(s)!!!'.format(duration_sec))
    start_time = time.time()
    last_time = start_time
    total_time = round(time.time() - start_time, 2)
    lap_num = 1
    try:
        while True:
            if total_time > duration_sec:
                print('Duratin:{}sec(s) End Timer!!!'.format(duration_sec))
                break

            lap_time = round(time.time() - last_time, 2)
            total_time = round(time.time() - start_time, 2)
            print("{}: {} {}".format(lap_num, total_time, lap_time))
            
            timer = threading.Timer(0,func)
            timer.start()
            time.sleep(2) ## 等待2s
            timer.cancel()##停止定時器
            #print("5s到了定時器退出")

            lap_num += 1
            last_time = time.time()
        
    except KeyboardInterrupt:
        print('\nEnd Timer!!!')
        exit()    

def client_siteone_continuous(parms):
    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = parms['remote_server_ip']
    client.port = parms['port']
    client.protocol = parms['protocol']
    test_duration = parms['test_duration']

    #print('Start Time Duratin:{} sec(s)!!!'.format(test_duration))
    logger.info('Start Time Duratin:{} sec(s)!!!'.format(test_duration))
    start_time = time.time()
    last_time = start_time
    total_time = round(time.time() - start_time, 2)
    lap_num = 1
    try:
        while True:
            if total_time > int(test_duration):
                #print('Duratin:{}sec(s) End Timer!!!'.format(test_duration))
                logger.info('Duratin:{}sec(s) End Timer!!!'.format(test_duration))
                break

            lap_time = round(time.time() - last_time, 2)
            total_time = round(time.time() - start_time, 2)
            
            # Start iperf client traffic
            logger.info('Connecting to {0}:{1}:{2}'.format(client.server_hostname, client.port, client.protocol))
            result = client.run()

            if result.error:
                logger.info(result.error)
            else:
                print('')
                logger.info('Test completed:')
                logger.info('  started at         {0}'.format(result.time))
                logger.info('  bytes transmitted  {0}'.format(result.sent_bytes))
                logger.info('  retransmits        {0}'.format(result.retransmits))
                logger.info('  avg cpu load       {0}%\n'.format(result.local_cpu_total))

                logger.info('Average transmitted data in all sorts of networky formats:')
                logger.info('  bits per second      (bps)   {0}'.format(result.sent_bps))
                logger.info('  Kilobits per second  (kbps)  {0}'.format(result.sent_kbps))
                logger.info('  Megabits per second  (Mbps)  {0}'.format(result.sent_Mbps))
                logger.info('  KiloBytes per second (kB/s)  {0}'.format(result.sent_kB_s))
                logger.info('  MegaBytes per second (MB/s)  {0}'.format(result.sent_MB_s))

            # End iperf client traffic

            timer = threading.Timer(0,func)
            timer.start()
            time.sleep(3) ## 等待2s
            timer.cancel()##停止定時器

            lap_num += 1
            last_time = time.time()
        
    except KeyboardInterrupt:
        #print('\nEnd Timer!!!')
        logger.info('\nEnd Timer!!!')
        exit()

def client_siteone_socket_udp_continuous(parms):
    client_server_hostname = parms['remote_server_ip']
    client_port = parms['port']
    client_protocol = parms['protocol']
    data_payload = 2048
    test_duration = parms['test_duration']

    #print('Start Time Duratin:{} sec(s)!!!'.format(test_duration))
    logger.info('Start Time Duratin:{} sec(s)!!!'.format(test_duration))
    start_time = time.time()
    last_time = start_time
    total_time = round(time.time() - start_time, 2)
    lap_num = 1
    try:
        while True:
            if total_time > int(test_duration):
                #print('Duratin:{}sec(s) End Timer!!!'.format(test_duration))
                logger.info('Duratin:{}sec(s) End Timer!!!'.format(test_duration))
                break

            lap_time = round(time.time() - last_time, 2)
            total_time = round(time.time() - start_time, 2)
            #print("{}: {} {}".format(lap_num, total_time, lap_time))

            # Start client traffic
            """ A simple echo client """ 
             # Create a UDP socket 
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
 
            server_address = (client_server_hostname, int(client_port)) 
            logger.info("Connecting to %s port %s" % server_address) 
    
            try: 
                # Send data 
                message = "Test message. This will be echoed" 
                logger.info("Sending %s" % message) 
                sent = sock.sendto(message.encode('utf-8'), server_address) 
 
                # Receive response 
                data, server = sock.recvfrom(data_payload) 
                logger.info("received %s" % data)
    
            finally: 
                logger.info("Closing connection to the server") 
                sock.close()   
            # End client traffic

            timer = threading.Timer(0,func)
            timer.start()
            time.sleep(3) ## 等待2s
            timer.cancel()##停止定時器

            lap_num += 1
            last_time = time.time()
        
    except KeyboardInterrupt:
        #print('\nEnd Timer!!!')
        logger.info('\nEnd Timer!!!')
        exit()

def client_siteone_socket_udp_ipv6_continuous(parms):
    client_server_hostname = parms['remote_server_ip']
    client_port = parms['port']
    client_protocol = parms['protocol']
    data_payload = 2048
    test_duration = parms['test_duration']

    logger.info('Start Time Duratin:{} sec(s)!!!'.format(test_duration))
    start_time = time.time()
    last_time = start_time
    total_time = round(time.time() - start_time, 2)
    lap_num = 1
    try:
        while True:
            if total_time > int(test_duration):
                #print('Duratin:{}sec(s) End Timer!!!'.format(test_duration))
                logger.info('Duratin:{}sec(s) End Timer!!!'.format(test_duration))
                break

            lap_time = round(time.time() - last_time, 2)
            total_time = round(time.time() - start_time, 2)
            #print("{}: {} {}".format(lap_num, total_time, lap_time))

            # Start client traffic
            """ A simple echo client """ 
            # Create a UDP socket 
            sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM) 
 
            server_address = (client_server_hostname, int(client_port)) 
            logger.info("Connecting to %s port %s" % server_address) 
    
            try: 
                # Send data 
                message = "Test message. This will be echoed" 
                logger.info("Sending %s" % message) 
                sent = sock.sendto(message.encode('utf-8'), server_address) 
 
                # Receive response 
                data, server = sock.recvfrom(data_payload) 
                logger.info("received %s" % data)
    
            finally: 
                logger.info("Closing connection to the server") 
                sock.close()
            # End client traffic

            timer = threading.Timer(0,func)
            timer.start()
            time.sleep(3) ## 等待2s
            timer.cancel()##停止定時器

            lap_num += 1
            last_time = time.time()
        
    except KeyboardInterrupt:
        #print('\nEnd Timer!!!')
        logger.info('\nEnd Timer!!!')
        exit()