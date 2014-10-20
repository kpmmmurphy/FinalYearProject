#!/bin/sh

#Sets up Pip and Django
sudo easy_install pip==1.4.1

sudo pip install Django

#Prints the version of Django 
python -c "import django; print(django.get_version())"

#Creates Django Project with the name FYP
sudo python /usr/local/lib/python2.7/dist-packages/django/bin/django-admin.py startproject FYP
