#!/bin/bash

#Sets up Pip
sudo easy_install pip==1.4.1

#Install Virtual environment manager
sudo pip install virtualenv

#Create VirtualEnv
sudo virtualenv fyp

#Activeate VirtualEnv
. fyp/bin/activate

#Do not use sudo here, you are then the root user of the virtualenv
pip install django

#Prints the version of Django 
python -c "import django; print(django.get_version())"

#Creates Django Project with the name FYP
#sudo python /usr/local/lib/python2.7/dist-packages/django/bin/django-admin.py startproject FYP

#Set up MySQL Development clients
#sudo apt-get update

#sudo apt-get install python-dev

#sudo apt-get install python-MySQLdb
