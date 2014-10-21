#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 21 - Oct - 14

import peewee
from peewee import *
import random

#Database Credentials
DB_NAME   = 'TEST'
DB_USER   = 'root'
DB_PASSWD = 'kevinmurphy'

#Configuration details
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

db = MySQLDatabase(DB_NAME, user=DB_USER, passwd=DB_PASSWD)

class Current_Day_Sensor_Output(peewee.Model):
    class Meta:
        database = db

    #Define DB fields
    date_and_time       = peewee.DateField(DATE_FORMAT)
    mq7_carbon_monoxide = peewee.IntegerField()
    temperature         = peewee.IntegerField()
    flammable_gas       = peewee.IntegerField()
    smoke               = peewee.IntegerField()

class Sensor_Output_Averages(peewee.Model):
    class Meta: 
        database = db

    #Define DB fields
    date_and_time       = peewee.DateField(DATE_FORMAT)
    mq7_carbon_monoxide = peewee.IntegerField()
    temperature         = peewee.IntegerField()
    flammable_gas       = peewee.IntegerField()
    smoke               = peewee.IntegerField()


class System_Details(peewee.Model):
    class Meta:
        database = db

    #Define DB Fields
    ip_address        = peewee.CharField()
    gps_coords_aprrox = peewee.CharField()

class System_Admin_Details(peewee.Model):
    class Meta:
        database = db

    #Define DB Fields
    last_name     = peewee.CharField()
    first_name    = peewee.CharField()
    device_id     = peewee.CharField()
    date_and_time = peewee.DateField(DATE_FORMAT)

#Creates the Tables
def create_tables():
    try: 
        Sensor_Output_Averages.createTable()
    except peewee.OperationError:
        print "Sensor output Averages Table Already Exists"

    try:
        Current_Day_Sensor_Output.create_table()
    except peewee.OperationalError:
        print "Current Day Sensor_Output Table Already Exists"

    try:
        System_Details.create_table()
    except peewee.OperationalError:
        print "System_Details Table Already Exists"

    try: 
        System_Admin_Details.create_table()
    except peewee.OperationalError:
        print "System_Admin_Details Table Already Exists"

#Test Functions
def insert_test_data():
    sensor_output = Sensor_Output(mq7_carbon_monoxide=random.randint(100, 10000), 
                                temperature=random.randint(0, 34),
                                flammable_gas=random.randint(100, 10000),
                                smoke=random.randint(100, 100000))
    sensor_output.save()

    print "Inserting Random Sensor Data..."

#Main Section
create_tables()
insert_test_data()
