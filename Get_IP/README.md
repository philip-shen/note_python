# note of_Get IP
Take some note of IP address

# Table of Content

# 
[[python] 取得主機IP 201710](http://gienmin.blogspot.com/2017/10/pythoniperf-socket.html)  
## 第一種方式取得system上的ip  
```
import os
import socket
""" 判斷是否為linux system """
if os.name != 'nt':
import fcntl
import struct
""" 取得裝至上的訊息 """
def get_interface_ip(ifname):
     get_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(get_s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith('127.') and os.name != 'nt':
    interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0", "ath0", "ath1", "ppp0",]
    for ifname in interfaces:
      try:
        ip = get_interface_ip(ifname)
        break
      except IOError:
        pass
    return ip  
```
## 第二種，進行對外連線來取得當前網卡的ip  
```
import socket
def getIP():
  myname = socket.getfqdn(socket.gethostname())
  get_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  get_s.connect(('8.8.8.8', 0))

  ip = ('hostname: %s, localIP: %s') % (myname, get_s.getsockname()[0])
  return ip  
```

# Reference



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