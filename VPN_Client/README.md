# Purpose  
Take note of VPN Client by Python  

# Table of Contents  
[VPN Client on GitHub](#vpn-client-on-github)  

[Building SoftEther VPN L2TP/IPSec PPTP Docker Container](#building-softether-vpn-l2tpipsec-pptp-docker-container)  
[]()  

# VPN Client on GitHub  
[ctrngk/l2tp-client - GitHub 26 Sep 2019](https://github.com/ctrngk/l2tp-client)  
```
script for l2tp (only pskshared secret) client tested on debian 8
```

[ut0mt8/l2tpclient: A proof of concept l2tp 'lac' client 26 Jun 2012](https://github.com/ut0mt8/l2tpclient)  
```
l2tpclient.py RMZ 2012

Naive implementation of a LAC (L2TP client) written in python.
It implement very partially RFC2661. 
Limited to only one tunnel and one session.
Relies on pppd for ppp connectivity.
Know to work with xl2tpd and Redback LNS implementation.
Tested on Linux, and OpenBSD 
(warning MTU on OpenBSD need to be at most 850, cause of the 1024 lentgh buffer hardcoded in the tty code, or patch your kernel)
```

[zentin26/python-vpn: A fully functioning IPsec/L2TP 2 Dec 2017](https://github.com/zentin26/python-vpn)  
```
A fully functioning IPsec/L2TP VPN server written with the Twisted framework.
```

[I want to connect a windows machine to a L2TP/ IPsec vpn using python Oct 9, 2019](https://stackoverflow.com/questions/58291948/i-want-to-connect-a-windows-machine-to-a-l2tp-ipsec-vpn-using-python)
```
You can use Add-VpnConnection and Set-VpnConnectionIPsecConfigurationin Windows PowerShell
```
```
PS C:\> Add-VpnConnection -Name "Contoso" -ServerAddress 176.16.1.2 -TunnelType "L2tp"
PS C:\> Set-VpnConnectionIPsecConfiguration 
-ConnectionName "Contoso" 
-AuthenticationTransformConstants None 
-CipherTransformConstants AES128 
-EncryptionMethod AES128 
-IntegrityCheckMethod SHA256 
-PfsGroup None 
-DHGroup ECP256 
-PassThru -Force
AuthenticationTransformConstants : None

CipherTransformConstants         : AES128

DHGroup                          : ECP256

IntegrityCheckMethod             : SHA256

PfsGroup                         : None

EncryptionMethod                 : AES128
```

# Building SoftEther VPN L2TP/IPSec PPTP Docker Container  
[Building SoftEther VPN L2TP/IPSec PPTP Docker Container May 12, 2019](https://netslovers.com/2019/05/12/building-softether-vpn-l2tp-ipsec-pptp-docker-container/) 

## Initialize Ubuntu Host Device and Set Up a Basic Firewall  
## Installs Docker, Docker Compose, and python pip – always latest version during deploy.  


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
