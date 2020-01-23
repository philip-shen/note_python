# Purpose  
Take note of DHCP Client Test 

# Table of Contents  
[01. DHCPTest-python](#01-dhcptest-python )  
[02. DHCP client testing tool ](#02-dhcp-client-testing-tool)  


# 01. DHCPTest-python  
[ dyninc /DHCPTest-python](https://github.com/dyninc/DHCPTest-python/blob/master/dhcp_test.py)  

## Install libpcap-dev  
[apt - How to install libpcap-dev on Ubuntu 18.10? Feb 1, 2019](https://askubuntu.com/questions/1114719/how-to-install-libpcap-dev-on-ubuntu-18-10)  

So I need to install libpcap0.8:  
```
sudo apt install libpcap0.8
```

It worked, so now all I need to do:  
```
sudo apt install libpcap0.8-dev
```
## Install pypcap  
[pynetwork /pypcap ](https://github.com/pynetwork/pypcap)  

Installation from sources 
```
$ pip install -r requirements-devel.txt
```

Please clone the sources and run:  
```
$ python setup.py install
```

# 02. DHCP client testing tool  
[DHCP client testing tool April 23, 2013](http://www.networkers-online.com/blog/2013/04/dhcp-client-testing-tool/)  
[ saravana815 /dhtest](https://github.com/saravana815/dhtest)  

*On VMWare available*  
*On WSL inavailable*

```
dhtest - linux dhcp client simulation tool. It can simulate hundreds of dhcp
  client from a linux machine. Linux root login is needed because the tool requires 
  layer2 raw socket for sending and receiving dhcp packets.
```

```
$ make
        gcc    -c -o dhtest.o dhtest.c
        gcc    -c -o functions.o functions.c
        gcc dhtest.o functions.o -o dhtest
```

![alt tag](https://i.imgur.com/BY3munR.jpg)  

![alt tag](https://i.imgur.com/Zzx6czn.jpg)  

# Troubleshooting


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
