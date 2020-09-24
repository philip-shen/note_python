Table of Contents
=================

   * [note_python_TCP UDP Srv Clinet](#note_python_tcp-udp-srv-clinet)
   * [Chat-App-using-Socket-Programming-and-Tkinter](#chat-app-using-socket-programming-and-tkinter)
      * [Server on Windows and Client on Linux](#server-on-windows-and-client-on-linux)
      * [Server on Windows and Client on Windows](#server-on-windows-and-client-on-windows)
      * [File Download Location](#file-download-location)
   * [SimpleChatApp](#simplechatapp)
      * [Now, first start the server from multiChatServer.py](#now-first-start-the-server-from-multichatserverpy)
      * [Then, run the below to start one client from multiChatClient.py](#then-run-the-below-to-start-one-client-from-multichatclientpy)
   * [Pingpong Socket](#pingpong-socket)
      * [No Module Named ServerSocket](#no-module-named-serversocket)
   * [Tkinter Countdown Timer](#tkinter-countdown-timer)
   * [mcjoin - tiny multicast testing tool](#mcjoin---tiny-multicast-testing-tool)
   * [Reference](#reference)
   * [Troubleshooting](#troubleshooting)
      * [OSError: [WinError 10065] A socket operation was attempted to an unreachable host](#oserror-winerror-10065-a-socket-operation-was-attempted-to-an-unreachable-host)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# note_python_TCP UDP Srv Clinet
Take some note of TCP UDP Srv Clinet


# Chat-App-using-Socket-Programming-and-Tkinter  
*Can work successfully*  

[Samjith888 /Chat-App-using-Socket-Programming-and-Tkinter ](https://github.com/Samjith888/Chat-App-using-Socket-Programming-and-Tkinter) 

## Server on Windows and Client on Linux  
<img src="https://i.imgur.com/zkDuolP.jpg" width="700" height="500">

## Server on Windows and Client on Windows  
<img src="https://i.imgur.com/BbDLWCd.jpg" width="700" height="500">

## File Download Location  
<img src="https://i.imgur.com/ae8zUJH.jpg" width="500" height="300">


![chat_screenshot1](https://user-images.githubusercontent.com/39676803/63266288-41c3ea00-c2ad-11e9-80e8-cd0b41a48e34.PNG)


![chat_screenshot2](https://user-images.githubusercontent.com/39676803/63266312-51433300-c2ad-11e9-9e5d-23a23941da79.PNG)


![chat_screenshot3](https://user-images.githubusercontent.com/39676803/63265898-46d46980-c2ac-11e9-8b8f-0af9d288e3c7.PNG)


![chat_screenshot4](https://user-images.githubusercontent.com/39676803/63265915-5358c200-c2ac-11e9-9b90-2b4d68695789.PNG)


# SimpleChatApp  
[ KetanSingh11 /SimpleChatApp ](https://github.com/KetanSingh11/SimpleChatApp)  
## Now, first start the server from multiChatServer.py  
```
python3 multiChatServer.py
```
## Then, run the below to start one client from multiChatClient.py
```
python3 multiChatClient.py
```

```
System Requirements :

    Python 3.6 or greater
    Threading (inbuild in Python Standard Library)
    Sockets (inbuild in Python Standard Library)

**Build on __WINDOWS 7__. Tested on __Windows__ and __Linux__ also. 
```
<img src="https://i.imgur.com/a1zrKXS.png" width="800" height="350">

# Pingpong Socket  
[kirthiprakash /pingpong](https://github.com/kirthiprakash/pingpong)   
```
python2 only
```

## No Module Named ServerSocket  
[No Module Named ServerSocket Feb 19 '16](https://stackoverflow.com/questions/13329761/no-module-named-serversocket)  
```
The right name is SocketServer in Python2 and socketserver in Python3.
```

[Build a Chatroom App with Python ](https://medium.com/python-in-plain-english/build-a-chatroom-app-with-python-458fc435025a)  

<img src="https://miro.medium.com/max/1800/1*EjcHnH1pQP3U-aj-QnLQcw.png" width="800" height="0">

# Tkinter Countdown Timer  
[ターミナルから起動できる簡易タイマーをつくった posted at Dec 09, 2016](https://qiita.com/horoyoi_mixed_fruit/items/a5867d919e8ecb91ba20)  

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F140269%2F74f4858f-c942-51a8-c195-2733ca222ce4.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=0a5a7fc4ad9cc1095a8caa3c3f5fb790" width="600" height="500">


# mcjoin - tiny multicast testing tool  
[mcjoin](https://github.com/troglobit/mcjoin)  

[usage](https://github.com/troglobit/mcjoin#usage)  
```
 $ mcjoin -h
    
    Usage: mcjoin [-dhjqsv] [-c COUNT] [-i IFNAME] [-p PORT] [-r SEC] [-t TTL]
                  [[SOURCE,]GROUP0 .. [SOURCE,]GROUPN | [SOURCE,]GROUP+NUM]
    
    Options:
      -c COUNT     Exit after COUNT number of received and/or sent packets
      -d           Debug output
      -h           This help text
      -i IFNAME    Interface to use for multicast groups, default eth0
      -j           Join groups, default unless acting as sender
      -p PORT      UDP port number to listen to, default: 1234
      -q           Quiet mode
      -r SEC       Do a join/leave every SEC seconds
      -s           Act as sender, sends packets to select groups
      -t TTL       TTL to use when sending multicast packets, default 1
      -v           Display program version
    
    Bug report address: https://github.com/troglobit/mcjoin/issues
    Project homepage: https://github.com/troglobit/mcjoin/
```

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

```

```
* [Essentials of Python Socket Programming ](https://www.techbeamers.com/python-tutorial-essentials-of-python-socket-programming/)  
```

```
![alt tag](https://cdn.techbeamers.com/wp-content/uploads/2016/02/Python-Socket-Programming-WorkFlow.png)  


* [Multiple UDP listener on the same port ](https://gist.github.com/Lothiraldan/3951784)  

* [Asynchronous HTTP libraries benchmark for upcoming PyPy release 5 Mar 2017](https://github.com/squeaky-pl/zenchmarks)

* [Python server ipv6 UDP program Mar 10, 2016](https://stackoverflow.com/questions/34272372/python-server-ipv6-udp-program)  


# Troubleshooting  
## OSError: [WinError 10065] A socket operation was attempted to an unreachable host  
* [Python - bind error on multicast bind on windows Mar 10, 2013](https://stackoverflow.com/questions/15322242/python-bind-error-on-multicast-bind-on-windows)  

As noted by Carl Cerecke in the comments of the [PYMOTW Multicast article](https://pymotw.com/2/socket/multicast.html#comment-763199034), 
the use of socket.INADDR_ANY in Windows will bind to the default multicast address and 
if you have more than one interface Windows has the potential to pick the wrong one.

In order to get around this, you can explicitly specify the interface you want to receive multicast messages from:
```
group = socket.inet_aton(multicast_group)
iface = socket.inet_aton('192.168.1.10') # listen for multicast packets on this interface.
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, group+iface)
```
You can get a list of interfaces using the following:
```
socket.gethostbyname_ex(socket.gethostname()) 
# ("PCName", [], ["169.254.80.80", "192.168.1.10"])
```
In the above example, we would likely want to skip over the first 169.254 link-local address and 
select the desired 192.168.1.10 address.
```
socket.gethostbyname_ex(socket.gethostname())[2][1]
# "192.168.1.10"
```



* [C++ Builder XE4 > Indy > UDP通信 > Send() > 「モジュールXXXのアドレスXXXでアドレスXXXに対する読取り違反が起きました」 > 「#Socketエラー #10065ホストへのルートが存在しません」](https://qiita.com/7of9/items/8c406dae8d26773736ad)  
[エラー概要](https://qiita.com/7of9/items/8c406dae8d26773736ad#%E3%82%A8%E3%83%A9%E3%83%BC%E6%A6%82%E8%A6%81)  

[エラー詳細](https://qiita.com/7of9/items/8c406dae8d26773736ad#%E3%82%A8%E3%83%A9%E3%83%BC%E8%A9%B3%E7%B4%B0)  
```
```

[対処](https://qiita.com/7of9/items/8c406dae8d26773736ad#%E5%AF%BE%E5%87%A6)  
Send()をする部分をtry, catchで対処する  
```
while(!Terminated) {
    try {
        Form1->IdUDPClient->Send(acmd, m_enqSJIS);
    } catch (Exception &exc) {
        // 以下の条件で発生するエラーの対処
        // A. 起動してから一度もEthernetケーブルを挿していない
        // B. 特定のPC(Window 7のうち特定のPC)において発生する
        if (exc.ClassName() == L"EIdSocketError") {
            continue;
        }
    }

    // 正常な場合の処理 (省略)
}
```


* [vcrpyでAPIと連携するプログラムのテストを楽にする Mar 27, 2017](https://qiita.com/Asayu123/items/fbb605ed514bc4b413c8)  
```
======================================================================
ERROR: test_get_todo_by_title (tests.test_sample_api_client.TestSampleApiClient)
----------------------------------------------------------------------
Traceback (most recent call last):
 ~ 省略 ~
OSError: [WinError 10065] 到達できないホストに対してソケット操作を実行しようとしました。

----------------------------------------------------------------------
Ran 1 test in 21.026s

FAILED (errors=1)
```
[問題点](https://qiita.com/Asayu123/items/fbb605ed514bc4b413c8#%E5%95%8F%E9%A1%8C%E7%82%B9)  
```
単体テストは、プログラムの単体での正当性を確認するものですが、このようなテスト実装では結合先(APIサーバ)や通信経路の影響を受けてしまいます。
他にも、別のユーザが、同じタイトルのtodoを投稿すると、ヒット件数が２件になり、実装自体が正常にも関わらずテストが失敗するようになってしまいます。

この問題を回避する方法としてよくあるものは、モックを作成し、下位モジュールをモックで置換し、戻り値を常に固定にしてしまうことです。(本記事では詳細は割愛します)
しかし、モックを作成するとなると、下位モジュールの戻り値を、連携するAPIやリソース毎に定義し管理する必要があり、連携する数が増えると大変な作業になります。 
```

[解決法](https://qiita.com/Asayu123/items/fbb605ed514bc4b413c8#%E8%A7%A3%E6%B1%BA%E6%B3%95)  
```
前置きが長くなりましたが、この問題を解決する手段として、"vcrpy"というライブラリを紹介します。
このライブラリを用いると、APIサーバに対して行われたHTTPリクエスト/レスポンスをファイルに記録し再生できるようになり、モックの作成の手間が省けるようになります。
```

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


