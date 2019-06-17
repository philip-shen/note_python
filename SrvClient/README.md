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

* [Write a Multithreaded Server in Python ](https://www.techbeamers.com/python-tutorial-write-multithreaded-python-server/)  
```

```
* [Essentials of Python Socket Programming ](https://www.techbeamers.com/python-tutorial-essentials-of-python-socket-programming/)  
```

```
![alt tag](https://cdn.techbeamers.com/wp-content/uploads/2016/02/Python-Socket-Programming-WorkFlow.png)  


* [Multiple UDP listener on the same port ](https://gist.github.com/Lothiraldan/3951784)  

* [Asynchronous HTTP libraries benchmark for upcoming PyPy release 5 Mar 2017](https://github.com/squeaky-pl/zenchmarks)  

# Troubleshooting  
* [Python: cannot set socket option SO_REUSEPORT #1419 ](https://github.com/Microsoft/WSL/issues/1419)  

* ['SO_REUSEPORT' is not defined on Windows 7 2012](https://stackoverflow.com/questions/13637121/so-reuseport-is-not-defined-on-windows-7)  
```
You need to set SO_BROADCAST option on each socket:

s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

SO_REUSEPORT is not standard and usually means same thing as SO_REUSEADDR where supported.
```
* [Socket options SO_REUSEADDR and SO_REUSEPORT, how do they differ? Do they mean the same across all major operating systems? Jan 17 2013](https://stackoverflow.com/questions/14388706/socket-options-so-reuseaddr-and-so-reuseport-how-do-they-differ-do-they-mean-t?rq=1)  
```

```
* [TypeError: a bytes-like object is required, not 'str' Mar 19, 2018](https://stackoverflow.com/questions/33003498/typeerror-a-bytes-like-object-is-required-not-str)  
```
This code is probably good for Python 2. But in Python 3, this will cause an issue, something related to bit encoding. I was trying to make a simple TCP server and encountered the same problem. Encoding worked for me. Try this with sendto command.

clientSocket.sendto(message.encode(),(serverName, serverPort))

Similarly you would use .decode() to receive the data on the UDP server side, if you want to print it exactly as it was sent.
```

* [Python: Socket programming server-client application using threads 2017/08/23](https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/)  

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