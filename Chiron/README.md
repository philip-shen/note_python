# note of Chiron
Take some note of Chiron

# Table of Content
[Installation](#installation)  

# Installation  
## Step 1 Budilup Virtualenv for Chiron  
```
$ virtualenv -p /usr/bin/python2.7 virtualenv/chiron
Running virtualenv with interpreter /usr/bin/python2.7
Already using interpreter /usr/bin/python2.7
New python executable in /home/test/virtualenv/chiron/bin/python2.7
Also creating executable in /home/test/virtualenv/chiron/bin/python
Installing setuptools, pip, wheel...
done.
```
## Step 2 Activate Virtualenv of Chiron  
```
~$ source /home/test/virtualenv/chiron/bin/activate
```
## Step 3 Make sure Virtualenv of Chiron   
```
(chiron) test@ubuntu:~$ pip
pip     pip2    pip2.7  pip3    pip3.6
(chiron) test@ubuntu:~$ pip2.7 list
DEPRECATION: Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date. A future version of pip will drop support for Python 2.7.
Package    Version
---------- -------
pip        19.1.1
setuptools 41.0.1
wheel      0.33.4

```
## Step 4 Make sure Python Verion if 2.7   
```
(chiron) test@ubuntu:~$ python -V
Python 2.7.12
```

## Step 5 pip Install Scapy   
* [Scapy Latest release](https://scapy.readthedocs.io/en/latest/installation.html#latest-release)
```
(chiron) test@ubuntu:~$ pip2 install --pre scapy[basic]
Collecting scapy[basic]
.
.
.
Building wheels for collected packages: scapy, simplegeneric, scandir
  Building wheel for scapy (setup.py) ... done
  Stored in directory: /home/test/.cache/pip/wheels/f9/3d/ce/a4af7de0fc68d6b773c91eefad410ced54ca44498e074e276a
  Building wheel for simplegeneric (setup.py) ... done
  Stored in directory: /home/test/.cache/pip/wheels/a9/28/53/f24776b4c5bcbe91aaf1f1e247bd6fadd17191aa12fac63902
  Building wheel for scandir (setup.py) ... done
  Stored in directory: /home/test/.cache/pip/wheels/91/95/75/19c98a91239878abbc7c59970abd3b4e0438a7dd5b61778335
Successfully built scapy simplegeneric scandir
Installing collected packages: simplegeneric, decorator, pygments, backports.shutil-get-terminal-size, ptyprocess, pexpect, wcwidth, six, prompt-toolkit, scandir, pathlib2, pickleshare, enum34, ipython-genutils, traitlets, ipython, scapy
Successfully installed backports.shutil-get-terminal-size-1.0.0 decorator-4.4.0 enum34-1.1.6 ipython-5.8.0 ipython-genutils-0.2.0 pathlib2-2.3.4 pexpect-4.7.0 pickleshare-0.7.5 prompt-toolkit-1.0.16 ptyprocess-0.6.0 pygments-2.4.2 scandir-1.10.0 scapy-2.4.3rc4 simplegeneric-0.8.1 six-1.12.0 traitlets-4.3.2 wcwidth-0.1.7
```
## Step 6 pip Install other modules   
```
(chiron) test@ubuntu:~$ pip2 install netaddr
(chiron) test@ubuntu:~$ pip2 install crypto
(chiron) test@ubuntu:~$ pip2 install matplotlib
(chiron) test@ubuntu:~$ pip2 install graphviz
```
## Step 7 Check all Modules Installation  
```
~$ pip list -l
DEPRECATION: Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date. A future version of pip will drop support for Python 2.7.
Package                            Version
---------------------------------- --------
backports.shutil-get-terminal-size 1.0.0
certifi                            2019.6.16
chardet                            3.0.4
crypto                             1.4.1
decorator                          4.4.0
enum34                             1.1.6
graphviz                           0.11.1
idna                               2.8
ipython                            5.8.0
ipython-genutils                   0.2.0
Naked                              0.1.31
netaddr                            0.7.19
pathlib2                           2.3.4
pexpect                            4.7.0
pickleshare                        0.7.5
pip                                19.1.1
prompt-toolkit                     1.0.16
ptyprocess                         0.6.0
Pygments                           2.4.2
PyYAML                             5.1.2
requests                           2.22.0
scandir                            1.10.0
scapy                              2.4.3rc4
setuptools                         41.0.1
shellescape                        3.4.1
simplegeneric                      0.8.1
six                                1.12.0
traitlets                          4.3.2
urllib3                            1.25.3
wcwidth                            0.1.7
wheel                              0.33.4
```

# Reference
* []()  
```
  
```

* []()  
```

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