#!/bin/bash

#Installs all needed dependencies

#Update
./update.sh

sudo python get-pip.py

sudo pip install requests

sudo pip install peewee

sudo apt-get install mysql-server python-mysqldb
