# note of Flent(FLExible Network Tester)
Take some note of Flent

# Table of Content

# Flent: The FLExible Network Tester  
Flent is a Python wrapper to run multiple simultaneous netperf/iperf/ping instances and aggregate the results. It was previously known as 'netperf-wrapper'. See the web site for the main documentation: https://flent.org.  

[Flent: The FLExible Network Tester](https://flent.org/contents.html)  

# Reference  
* [Test The Strength Of Your Network With Flent - TechJunkie Oct 26, 2017](https://www.techjunkie.com/test-strength-network-flent/)  
```
RRU
RRUL stands for Realtime Response Under Load.  
```
![alt tag](https://i2.wp.com/www.techjunkie.com/wp-content/uploads/2017/10/flent-rrul-torrent.jpg?resize=690%2C453&ssl=1)  
```
RTT
The RTT, or Round Trip Transfer tests are actually a lot like the RRUL tests. 
They don’t rely on the target being under a load. Instead, they just measure the time 
it takes for a UDP request to complete the circuit and return to the client. They do include ping as well.
```
![alt tag](https://i1.wp.com/www.techjunkie.com/wp-content/uploads/2017/10/flent-rtt-fair.jpg?resize=690%2C455&ssl=1)  
```
TCP

The TCP tests are standard TCP. 
They measure basic TCP requests like you were visiting a website or checking your email. 
Chances are, these tests won’t put nearly as much stress on your network, 
but they may give you a better picture of what regular traffic looks like.
```
![alt tag](https://i0.wp.com/www.techjunkie.com/wp-content/uploads/2017/10/flent-tcp12-to-wired.jpg?resize=690%2C361&ssl=1)  
```
UDP Flood
The UDP flood tests are actually RTT tests, but they send a deluge of UDP packets 
at the target machine at once. They don’t respond or adapt to the flow of traffic, just send. 
They can be useful for testing how the target machine will respond in the face of a bug or an attack.
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