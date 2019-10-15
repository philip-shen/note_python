# Purpose
Auto Test of WiFi Router Throughput Test by Selenium(via python) and Chariot(via Tcl)

# Table of Contents  
[Selenium implementation](#selenium-implementation)  
[Chariot Implementation](#chariot-implementation)  

[Reference](#reference)  
[cmdline argument parsing using tcl?](#cmdline-argument-parsing-using-tcl)  

# Selenium Implementation
[note_python/crawl_Selenium](https://github.com/philip-shen/note_python/tree/master/crawl_Selenium#system)  

# Chariot Implementation  
[note_Networking/Chariot_Thruput](https://github.com/philip-shen/note_Networking/tree/master/Chariot_Thruput)  

# Troubleshooting


# Reference
## cmdline argument parsing using tcl?  
[cmdline argument parsing using tcl? Jul 5, 2017](https://stackoverflow.com/questions/44917037/cmdline-argument-parsing-using-tcl)  

```
package require cmdline

set parameters {
    {s.arg ""   "Slot"}
    {p.arg ""   "Port"}
    {l.arg "100"   "Load"}
    {f.arg "256"   "Framesize"}
    {debug      "Turn on debugging, default=off"}
}
#set option(l) 100
set usage "- A simple script to demo cmdline parsing"

if {[catch {array set options [cmdline::getoptions ::argv $parameters $usage]}]} {
    puts [cmdline::usage $parameters $usage]
} else {
    parray options
}
#puts [array get options]
puts $options(l)
puts $options(f)
```
```
script Output:

C:\Tcl\bin>tclsh opt.tcl -s 1 -f 128
options(debug) = 0
options(f)     = 128
options(l)     = 100
options(p)     =
options(s)     = 1
100
128
```
[package for parsing argument in TCL Jun 21, 2014](https://stackoverflow.com/questions/24341141/package-for-parsing-argument-in-tcl)  
```
package require cmdline

set parameters {
    {server.arg ""   "Which server to search"}
    {debug           "Turn on debugging, default=off"}
}

set usage "- A simple script to demo cmdline parsing"
array set options [cmdline::getoptions ::argv $parameters $usage]
parray options
```
```
$ tclsh simple.tcl 
options(debug)  = 0
options(server) = 

$ tclsh simple.tcl -server google.com
options(debug)  = 0
options(server) = google.com

$ tclsh simple.tcl -server google.com -debug
options(debug)  = 1
options(server) = google.com

$ tclsh simple.tcl -help
simple - A simple script to demo cmdline parsing
 -server value        Which server to search <>
 -debug               Turn on debugging, default=off
 -help                Print this message
 -?                   Print this message

    while executing
"error [usage $optlist $usage]"
    (procedure "cmdline::getoptions" line 15)
    invoked from within
"cmdline::getoptions ::argv $parameters $usage"
    invoked from within
"array set options [cmdline::getoptions ::argv $parameters $usage]"
    (file "simple.tcl" line 11)
```


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
