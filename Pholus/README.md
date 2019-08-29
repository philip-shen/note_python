# Purpose
Take note of Pholus  

# Table of Contents  


# Troubleshooting


# Reference
* [An Attack-in-Depth Analysis of  multicast DNS and DNS Service Discovery 14th April 2017](https://www.secfu.net/papers-presentations/)  
```
Multicast DNS and DNS Service Discovery are two protocols used for Zero Configuration Networking purposes from several devices and various vendors. Due to their objective of assisting Zero Configuration Networking, these protocols, which assume a “cooperating participants” environment, have some inherent weaknesses, like the “generous” broadcasting of a lot of information, and the use of easily “spoofable” messages. While these problems have been identified and related research has been published, a complete and in-depth threat analysis of all the potential attacking vectors has not been presented yet. This paper aims at filling this gap by providing a thorough study of the attack surface of these two protocols. By following closely the RFC specifications, potential attack vectors and specific testing scenarios are identified, which are examined using real life implementations. Specifically, these attacks are tested against popular devices, implementations and Operating Systems by using a tool specifically developed for this purpose, both for IPv4 and IPv6 environments. As it is shown, if this “cooperating participants” environment cannot be guaranteed, the usage of such protocols should highly be reconsidered. Finally, specific countermeasures suitable for mitigating the identified threats are also proposed.
```
* [Linux Avahi Daemon Tutorial With Examples 28/11/2018](https://www.poftut.com/linux-avahi-daemon-tutorial-examples/)  
Installing Avahi
```
$ sudo apt install avahi-daemon
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_58988718ef656.png) 

Starting Avahi
```
$ /etc/init.d/avahi-daemon start
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_5898878a33364.png) 
OR  
```
$ sudo systemctl start avahi-daemon
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_58988895ec9b8.png)  
Stopping Avahi  
```
$ /etc/init.d/avahi-daemon stop
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_589888185b3ca.png) 

OR  
```
$ sudo systemctl stop avahi-daemon
```

Enable Avahi Daemon  
```
$ sudo systemctl enable avahi-daemon
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_58988fb19a66b.png) 

Disable Avahi Daemon 
```
$ sudo systemctl disable avahi-daemon
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_58988fcb0a341.png)  
Configuration Files  
```
Avahi configuration files resides in /etc/avahi . Avahi daemon configuration file is named avahi-daemon.conf . 
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_58988c45c8c08.png) 
Add Host  
```
Adding host to the DNS service of avahi is like adding host Linux hosts file. Add following line into the host file like in the screenshot and than restart avahi daemon.
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_58988cee3da3f.png)  
Add Service  
```
Adding services is harder than adding hosts. There is an xml configuration file used to describe services and this file will be put into /etc/avahi/services/ directory. Following service configuration file defines ftp file which is  served from tcp 21 port.
```
```
<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name>FTP file sharing</name>
  <service>
    <type>_ftp._tcp</type>
    <port>21</port>
  </service>
</service-group>
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_58988ed74e7b5.png)  


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
