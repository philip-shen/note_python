FROM centos:6.8

ADD ./conf/nginx.repo /etc/yum.repos.d/

# nginx & python
RUN yum localinstall -y http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
RUN yum install -y https://centos6.iuscommunity.org/ius-release.rpm
RUN yum install -y nginx-1.10.1
RUN yum install -y make gcc
RUN yum install -y libxml2-devel
RUN yum install -y python35u python35u-libs python35u-devel python35u-pip
RUN yum clean all

RUN ln -s /usr/bin/python3.5 /usr/bin/python3
RUN unlink /usr/bin/python
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3.5 /usr/bin/pip

RUN pip install uwsgi

# setting nginx
COPY conf/nginx.conf /etc/nginx/nginx.conf
ADD conf/default.conf /etc/nginx/conf.d/default.conf
RUN usermod -u 1000 nginx

EXPOSE 80

ADD ./conf/start.sh /tmp/start.sh

CMD /bin/sh /tmp/start.sh