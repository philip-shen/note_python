# Purpose
Take note about Python library of UPnP  

# Table of Contents  
[upnp_info](#upnpinfo)  
[port-forward](#port-forward)  

# upnp_info  
[tenable/upnp_info](https://github.com/tenable/upnp_info)  
```
Purpose

This script was written so that anyone can easily find the UPnP servers on their network. 
While tools like this have and do exist, none are as simple as downloading a file and executing it via Python.

Features

upnp_info.py discovers all UPnP servers within multicast range

$ python upnp_info.py 
[+] Discovering UPnP locations
[+] Discovery complete
[+] 11 locations found:
	-> http://192.168.0.254:49152/wps_device.xml
	-> http://192.168.1.217:49153/description.xml
	-> http://192.168.1.217:35848/rootDesc.xml
	-> http://192.168.1.217:32469/DeviceDescription.xml
	-> http://192.168.1.217:49152/tvdevicedesc.xml
	-> http://192.168.1.217:35439/rootDesc.xml
	-> http://192.168.1.251:49451/luaupnp.xml
	-> http://192.168.1.1:45973/rootDesc.xml
	-> http://192.168.1.1:1990/WFADevice.xml
	-> http://192.168.1.1:1901/root.xml
	-> http://192.168.1.217:8200/rootDesc.xml
```

# port-forward  
[gryphius/port-forward](https://github.com/gryphius/port-forward)  
```
./port-forward.py --help
usage: port-forward.py [-h] [-v] [-e EPORT] [-l IPORT] [-i LANIP] [-r ROUTER]
                       [-p PROTOCOL] [-d DESCRIPTION] [--disable] [-t TIME]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose output
  -e EPORT, --external-port EPORT
                        external port to open
  -l IPORT, --local-port IPORT
                        internal port (default: same as external)
  -i LANIP, --lan-ip LANIP
                        lan-ip where to forward the port, this computer if not
                        specified
  -r ROUTER, --router ROUTER
                        router ip to use. by default uses all discovered
                        routers
  -p PROTOCOL, --protocol PROTOCOL
                        TCP or UDP
  -d DESCRIPTION, --description DESCRIPTION
                        description for the rule
  --disable             disable a existing forwarding
  -t TIME, --time TIME  Duration of the rule
```

## Just show UPnP capable routers:  
```
./port-forward.py 
Found 2 UPnP routers:  192.168.1.1:49152 192.168.1.254:2189
No external port specified.
```

## Forward to a different local port for a few seconds only:  
```
./port-forward.py -e 1337 -v -t 30 -r 192.168.1.1  -l 9999 -d 'forward 1337 to 9999'
Discovering routers...
Found 2 UPnP routers:  192.168.1.1:49152 192.168.1.254:2189
port forward on 192.168.1.1 successful, 1337->192.168.1.22:9999
```

# Reference

[Exploring UPnP with Python July 5th, 2016](https://www.electricmonk.nl/log/2016/07/05/exploring-upnp-with-python/)  
```
UPnP uses a variety of different protocols to accomplish its goals:

    SSDP: Simple Service Discovery Protocol, for discovering UPnP devices on the local network.
    SCPD: Service Control Point Definition, for defining the actions offered by the various services.
    SOAP: Simple Object Access Protocol, for actually calling actions.
```

![alt tag](https://www.electricmonk.nl/log/wp-content/uploads/2012/10/upnp_overview.png)  

[UPnP router command-line control scripts](http://ssb22.user.srcf.net/setup/upnp.html)  

# Troubleshooting




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
