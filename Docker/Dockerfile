FROM centos:7
MAINTAINER "Josh Coyle" <jcoyle4@msudenver.edu>
RUN yum install -y epel-release 
RUN yum install -y npm 
RUN yum install -y python-pip
RUN pip install --upgrade pip
RUN pip install SQLALCHEMY
RUN pip install wheel
RUN yum install -y unzip
RUN yum install -y git
RUN yum install -y python-GeoIP
RUN yum install -y python-geojson
RUN yum install -y pyOpenSSL
RUN yum install -y screen
RUN useradd honeypotUser
RUN su honeypotUser
RUN git clone https://github.com/gdejohn/honeypot.git honeypot
RUN cd honeypot/httpServer && npm update
RUN mv honeypot ./home/honeypotUser
