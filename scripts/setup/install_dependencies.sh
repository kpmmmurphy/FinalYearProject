#!/bin/bash

#Installs all needed dependencies

#Update
./update.sh

sudo python get-pip.py

sudo pip install requests

sudo pip install peewee

sudo apt-get install mysql-server python-mysqldb

sudo apt-get install python-picamera

sudo pip install psutil

sudo pip install netifaces