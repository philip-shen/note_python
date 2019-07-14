# note_DHCPv6
Take some note of DHCP python

# Table of Content
[Installation](#installation)  
[Installation dnspython](#installation-dnspython)  
[Change to root and then excute](#change-to-root-and-then-excute)  

# Installation  
[Installation](https://dhcpy6d.ifw-dresden.de/documentation/installation/)  
```
    Python from http://www.python.org
        Python 2.7 comes as default on Debian 7/8 and Redhat/CentOS 6/7
        python-2.7.6p0 on OpenBSD 5.5
        python27 on FreeBSD and NetBSD

    dnspython from http://www.dnspython.org
        python-dnspython in Debian
        python-dns in Redhat/CentOS EPEL repository
        py-dnspython in OpenBSD
        py27-dnspython in FreeBSD
        py27-dns in NetBSD
```
# Installation dnspython  
[dnspython](http://www.dnspython.org/)  
[rthalley/dnspython](https://github.com/rthalley/dnspython)  
[Index of dnspython/kits/1.16.0](http://www.dnspython.org/kits/1.16.0/)  
```
Notices
Python 2.x support ended with the release of 1.16.0. dnspython 2.0.0 and later only support Python 3.4 and later.

The ChangeLog has been discontinued. Please see the git history for detailed change information.
```
# Change to root and then excute  
```
$ sudo su

# source /home/philshen/virtualenv/dhcpy6d/bin/activate

# pip2 list
DEPRECATION: Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date. A future version of pip will drop support for Python 2.7.
Package    Version
---------- -------
dnspython  1.16.0
pip        19.1.1
setuptools 41.0.1
wheel      0.33.4
```
![alt tag](https://i.imgur.com/RdWEcED.jpg)  


# Troubleshooting

# Reference
* [HenriWahl/dhcpy6d ](https://github.com/HenriWahl/dhcpy6d)  
```
Dhcpy6d is an open source server for DHCPv6, the DHCP protocol for IPv6.
Its development is driven by the need to be able to use the existing IPv4 infrastructure in coexistence with IPv6. In a dualstack scenario, the existing DHCPv4 most probably uses MAC addresses of clients to identify them. This is not intended by RFC 3315 for DHCPv6, but also not forbidden. Dhcpy6d is able to do so in local network segments and therefore offers a pragmatical method for parallel use of DHCPv4 and DHCPv6, because existing client management solutions could be used further.

At the moment it runs on [Open|Net|Free]BSD, MacOS X and Linux, tested with Debian 8 + 9 and CentOS 7.
```
* [niccokunzmann/python_dhcp_server](https://github.com/niccokunzmann/python_dhcp_server)  
```
This is a purely Python DHCP server that does not require any additional libraries or installs other that Python 3.

It was testet under Ubuntu 14 with Python and Windows 7. It does not use any operating system specific Python functions, so it should work when Python 3 works.
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