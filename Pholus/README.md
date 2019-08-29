# Purpose
Take note of Pholus  

# Table of Contents  
* [Installation](#installation)  

# Installation  
[Chiron Installation guide](https://github.com/philip-shen/note_python/tree/master/Chiron#installation)  

# Troubleshooting


# Reference
* [An Attack-in-Depth Analysis of  multicast DNS and DNS Service Discovery 14th April 2017](https://www.secfu.net/papers-presentations/)  
```
Multicast DNS and DNS Service Discovery are two protocols used for Zero Configuration Networking purposes 
from several devices and various vendors. Due to their objective of assisting Zero Configuration Networking,
these protocols, which assume a “cooperating participants” environment, have some inherent weaknesses, like
the “generous” broadcasting of a lot of information, and the use of easily “spoofable” messages. 
While these problems have been identified and related research has been published, a complete and in-depth threat analysis of all the potential attacking vectors has not been presented yet. 
This paper aims at filling this gap by providing a thorough study of the attack surface of these two protocols.
By following closely the RFC specifications, potential attack vectors and specific testing scenarios are identified, which are examined using real life implementations. 
Specifically, these attacks are tested against popular devices, implementations and Operating Systems by using a tool specifically developed for this purpose, both for IPv4 and IPv6 environments. 
As it is shown, if this “cooperating participants” environment cannot be guaranteed, the usage of such protocols should highly be reconsidered. 
Finally, specific countermeasures suitable for mitigating the identified threats are also proposed.
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
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">```

<service-group>
  <name>FTP file sharing</name>
  <service>
    <type>_ftp._tcp</type>
    <port>21</port>
  </service>
</service-group>
```
![alt tag](https://www.poftut.com/wp-content/uploads/2017/02/img_58988ed74e7b5.png)  

* [IPv6 Properties of Windows Server 2019 / Windows 10 (1809) mDNS June 12, 2019](https://insinuator.net/2019/06/ipv6-properties-of-windows-server-2019-windows-10-1809/)  
```
mDNS

To my surprise mDNS was enabled and active, as can be observed from the system’s actual network traffic. Not sure when Microsoft introduced this as part of their IPv6 stack – this article talks about “new mDNS functionality” and describes a registry key to, maybe, control the behavior (wasn’t tested by myself) and this post seems to indicate it was actually introduced in Win 10 1809 (also there’s a mention of another registry key called EnableMulticast which, afaik, is the one managed by GPOs for controlling LLMNR) – but in any case I’m not sure I like this one. H.D. Moore just tweeted how mDNS can be used for recon purposes on the local link and Antonios Atlasis had released an mDNS attack tool called Pholus in 2017 (after this Troopers #TR17 talk on “An Attack-in-Depth Analysis of multicast DNS and DNS Service Discovery”).
Suffice to say that I don’t really see a need why Windows 2019 Server has mDNS enabled by default.
```

* [LLMNR on Windows vs. Zeroconf vs. Bonjour Jul 31, 2012](https://stackoverflow.com/questions/11741062/llmnr-on-windows-vs-zeroconf-vs-bonjour)  

```
Link-Local Multicast Name Resolution (LLMNR) is a Microsoft tech for service discovery based on multicast DNS. Is it compatible with Bonjour/Zeroconf? If so, where's the API? The service discovery, I take it, is somehow rolled into vanilla DNS resolution (gethostbyname()?), but what about service advertisement?
```
```
LLMNR solves a small subset of the problems that mDNS tackles, as set out in this post. In short, it's not compatible with Bonjour.
```

* [Link-Local Multicast Name Resolution The Cable Guy - November 2006](https://docs.microsoft.com/en-us/previous-versions//bb878128(v=technet.10))  

```
Introduction

IPv4 hosts can use NetBIOS over TCP/IP (NetBT) to resolve computer names to IPv4 addresses for neighboring hosts by broadcasting a NetBIOS Name Query Request message to the local subnet broadcast address. The node that owns the queried name sends back a unicast NetBIOS Name Query Response message to the requestor and the name is resolved. However, NetBT only works over IPv4, not IPv6. Additionally, IT administrators can disable NetBT in an environment in which DNS is exclusively used for name resolution. With NetBT disabled on a network without DNS servers, you must add entries to the Hosts file to resolve names.

LLMNR allows name resolution on networks where a DNS server is not present or practical. A good example is the temporary subnet formed by a group of computers that form an ad hoc IEEE 802.11 wireless network. With LLMNR, hosts in the ad hoc wireless network can resolve each other computer names without having to configure one of the computers as a DNS server and the other computers with the IP address of the computer acting as the DNS server.

LLMNR messages use a similar format as DNS messages that are defined in RFC 1035 and use a different port than DNS messages. LLMNR Name Query Request messages in Windows Vista are sent to UDP port 5355. LLMNR Name Query Response messages are sent from UDP port 5355. The LLMNR resolver cache is separate from the DNS resolver cache.
```
```
Note

RFC 4795 also describes how LLMNR messages can be sent and received over TCP. However, TCP-based LLMNR messages are not supported in Windows Vista.

For LLMNR messages sent over IPv6, a querying host (a requestor) sends an LLMNR Name Query Request message to the link-local scope IPv6 multicast address of FF02::1:3. For LLMNR messages sent over IPv4, a querying host sends a LLMNR Name Query Request message to the IPv4 multicast address of 224.0.0.252. In both cases, the multicast address is scoped to prevent a multicast-enabled router from forwarding the query message beyond the subnet on which it was initially sent.
```
```
Note

RFC 4795 uses the term sender for the requesting host.

All IPv6-based LLMNR hosts listen on the IPv6 multicast address FF02::1:3 and instruct their Ethernet network adapters to listen for Ethernet frames with the destination multicast address of 33-33-00-01-00-03. All IPv4-based LLMNR hosts listen on the IPv4 multicast address 224.0.0.252 instruct their Ethernet network adapters to listen for Ethernet frames with the destination multicast address of 01-00-5E-00-00-FC.

The typical LLMNR message exchange for a name query consists of a multicast query and, if a host on the subnet is authoritative for the requested name, a unicast response to the requestor. Windows Vista-based LLMNR hosts neither send nor respond to unicast queries.

In contrast to DNS servers, LLMNR hosts are authoritative for specific names that have been assigned to them, rather than for a portion of the DNS namespace beginning at the assigned name. Using DNS terminology, LLMNR hosts are only authoritative for the zone apexes corresponding to their assigned names (the term zone is used loosely here because LLMNR hosts are not DNS servers that store zones). For example, an LLMNR node that has been assigned the name office.example.com is not also authoritative for all names that begin with office.example.com.
```
LLMNR Message Structure  
![alt tag](https://docs.microsoft.com/en-us/previous-versions//images/bb878128.cg110601%28en-us%2ctechnet.10%29.gif)  

* [Rushyo/VindicateTool: LLMNR/NBNS/mDNS Spoofing Feb 13, 2018 ](https://github.com/Rushyo/VindicateTool)  
```
What is Vindicate?

Vindicate is a tool which detects name service spoofing, often used by IT network attackers to steal credentials (e.g. Windows Active Directory passwords) from users. It's designed to detect the use of hacking tools such as Responder, Inveigh, NBNSpoof, and Metasploit's LLMNR, NBNS, and mDNS spoofers, whilst avoiding false positives. This can allow a Blue Team to quickly detect and isolate attackers on their network. It takes advantage of the Windows event log to quickly integrate with an Active Directory network, or its output can be piped to a log for other systems.

There's a diagram explaining spoofing attacks and how Vindicate works on the wiki.

Requires .NET Framework 4.5.2
```
```
What is LLMNR/NBNS/mDNS spoofing and why do I need to detect it?

    pentest.blog: What is LLMNR & WPAD and How to Abuse Them During Pentest ?
    Aptive Consulting: LLMNR / NBT-NS Spoofing Attack Network Penetration Testing
    GracefulSecurity: Stealing Accounts: LLMNR and NBT-NS Spoofing

TL;DR - Attackers might be stealing all sorts of credentials on your network (everything from Active Directory credentials to personal email accounts to database passwords) from right under your nose and you may be completely unaware it's happening.
```
[How it works 10 Dec 2017](https://github.com/Rushyo/VindicateTool/wiki/How-it-works)  
![alt tag](https://camo.githubusercontent.com/3be1fa5f8119e512da4ecb004e9c07b9a9dc9045/68747470733a2f2f692e696d6775722e636f6d2f3066445a6670352e706e67)  


* [Serverless DNS pdf slide](https://meetings.ripe.net/ripe-55/presentations/strotmann-mdns.pdf)  

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
