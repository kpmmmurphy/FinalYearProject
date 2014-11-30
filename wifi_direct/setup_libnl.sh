#!/bin/bash
#Sets up libnl needed by nl80211 driver

#tar -zxvf libnl-3.2.25.tar.gz

#Install flex and bison, needed for libnl configuration
#sudo apt-get install flex bison

sudo ./libnl-3.2.25/configure --prefix=/usr --sysconfdir=/etc --disable-static && make

sudo make install
