# note_python_TCP UDP Srv Clinet
Take some note of TCP UDP Srv Clinet

# Table of Content

# 


# Reference
* [Python TCP several listen on several ports at once - Stack Overflow Mar 18, 2017](https://stackoverflow.com/questions/22468160/python-tcp-several-listen-on-several-ports-at-once)  
There is single-threaded approach (on the listening side anyway - actually handling the connections may still require multiple threads).

You should open all of your sockets up-front, and put them in a list.

Then, you should select on all of them, which will return when any one of them is ready to be accepted on.

Something like this (totally untested):
```
servers = [] 

for port in portlist:
    ds = ("0.0.0.0", port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ds)
    server.listen(1)

    servers.append(server)

while True:
    # Wait for any of the listening servers to get a client
    # connection attempt
    readable,_,_ = select.select(servers, [], [])
    ready_server = readable[0]

    connection, address = ready_server.accept()

    # Might want to spawn thread here to handle connection,
    # if it is long-lived  
```

* [how to create a UDP server that will listen on multiple ports in Mar 28, 2016](https://stackoverflow.com/questions/36262374/how-to-create-a-udp-server-that-will-listen-on-multiple-ports-in-python)  
```
import socket
import select

sockets = []

for port in range(33,128):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', port))
    sockets.append(server_socket)

empty = []
while True:
    readable, writable, exceptional = select.select(sockets, empty, empty)
    for s in readable:
         (client_data, client_address) = s.recvfrom(1024)
         print client_address, client_data
for s in sockets:
   s.close()
```

* []()  
```

```

* []()  
![alt tag]()

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3