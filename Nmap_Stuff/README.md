# Purpose
Take note of Nmap Stuffs  

# Table of Contents  
[rainmap-lite](#rainmap-lite)  
    [Docker container for Rainmap Lite.]()

[Scantron](#scantron)  
[NmaptoCSV](#nmaptocsv)  

# rainmap-lite  
[ cldrn/rainmap-lite](https://github.com/cldrn/rainmap-lite)  
*Rainmap Lite - Responsive web based interface that allows users to launch Nmap scans from their mobiles/tablets/web browsers!* 
```
Rainmap Lite - Responsive web application that allows users to launch Nmap scans from their mobiles/tablets/web browsers!

Unlike it's predecessor [1], Rainmap-lite does not require special services (RabbitMQ, PostgreSQL, Celery, supervisor, etc) to make it easy to install on any server. You simply need to install the Django application and add the cron polling task to set up a new scanning server. Nmap scans on the road for everyone!

[1] Rainmap - https://nmap.org/rainmap/
```
## Features 

 * Easily launch Nmap scans with a few clicks.
 * Responsive interface runs smoothly from your phone/tablet.
 * Reports delivered by email in all formats.
 * View reports from your web browser.
 * Schedule scans.
 * Dozens of scanning profiles to choose from.
 * Easy to install/set up.
 * Share results with your team.

## Installation instructions  
[INSTALL](https://github.com/cldrn/rainmap-lite/wiki/INSTALL)  
###  Docker container for Rainmap Lite.
[RaiNmap Container 30/08/2016](http://jerrygamblin.com/2016/08/30/rainmap-container/)
```
Running it is as simple as:
docker run -ti -p 8080:8080 --name rainmap jgamblin/rainmap
Then access:
http://yourip:8080/console 
```
You can now run a ton of nmap scans and get the results emailed to you and your team:  
![alt tag](https://i2.wp.com/jerrygamblin.com/wp-content/uploads/2016/08/Screen-Shot-2016-08-30-at-7.47.54-PM.png?resize=768%2C484&ssl=1)  
![alt tag](https://i1.wp.com/jerrygamblin.com/wp-content/uploads/2016/08/Screen-Shot-2016-08-30-at-7.53.10-PM.png?ssl=1)  
#### Here is the DockerFile:  
[jgamblin/rainmap ](https://hub.docker.com/r/jgamblin/rainmap/)  
```
FROM ubuntu:latest
RUN apt-get update && apt-get install sqlite3 git nmap python-pip  -y
RUN pip install --upgrade pip
RUN pip install lxml
RUN pip install Django
RUN git clone https://github.com/cldrn/rainmap-lite
WORKDIR /rainmap-lite/rainmap-lite/
ADD  run.sh /rainmap-lite/rainmap-lite/run.sh
RUN chmod 777 /rainmap-lite/rainmap-lite/run.sh
CMD ./run.sh
```
#### Here is the run.sh:  
```
#!/bin/bash
sed -i "s/8000/8080/g" "nmaper-cronjob.py"
echo What is your public IP address?
read ip
sed -i "s/127.0.0.1/$ip/g" "nmaper-cronjob.py"
echo What is your SMTP user name?
read user
sed -i "s/youremail@gmail.com/$user/g" "nmaper-cronjob.py"
echo What is your SMTP password?
read pass
sed -i "s/yourpassword/$pass/g" "nmaper-cronjob.py"
echo What is your SMTP address?
read smtp
sed -i "s/smtp.gmail.com/$smtp/g" "nmaper-cronjob.py"
python manage.py migrate
python manage.py loaddata nmapprofiles
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8080 &
while true
do
python nmaper-cronjob.py
sleep 15
done
```

# Scantron  
[rackerlabs/scantron](https://github.com/rackerlabs/scantron)  
## Overview  
```
Scantron is a distributed nmap scanner comprised of two components. The first is a Master node that consists of a web front end used for scheduling scans and storing nmap scan targets and results. The second component is an agent that pulls scan jobs from Master and conducts the actual nmap scanning. A majority of the application's logic is purposely placed on Master to make the agent(s) as "dumb" as possible. All nmap target files and nmap results reside on Master and are shared through a network file share (NFS) leveraging SSH tunnels. The agents call back to Master periodically using a REST API to check for scan tasks and provide scan status updates.
```
![alt tag](https://raw.githubusercontent.com/rackerlabs/scantron/master/img/scheduled_scans.png)
```
Scantron is coded for Python3.6+ exclusively and leverages Django for the web front-end, Django REST Framework as the API endpoint, PostgreSQL as the database, and comes complete with Ubuntu-focused Ansible playbooks for smooth deployments. Scantron has been tested on Ubuntu 18.04 and may be compatible with other operating systems. Scantron's inspiration comes from:
    dnmap
    Minions
    rainmap svn / rainmap github
    rainmap-lite
```
```
Scantron relies heavily on utilizing SSH port forwards (-R / -L) as an umbilical cord to the agents. Either an SSH connection from Master --> agent or agent --> Master is acceptable and may be required depending on different firewall rules, but tweaking the port forwards and autossh commands will be necessary. If you are unfamiliar with these concepts, there are some great overviews and tutorials out there:
```
## Architecture Diagram  
![alt tag](https://github.com/rackerlabs/scantron/blob/master/img/scantron_architecture_overview.png)  


# NmaptoCSV  
[maaaaz/nmaptocsv](https://github.com/maaaaz/nmaptocsv)  
```
Description

A simple python script to convert Nmap output to CSV
```

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
