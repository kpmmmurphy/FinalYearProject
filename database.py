#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 21 - Oct - 14

##TODO===========================================
##Fix Dates



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
    date_and_time       = peewee.DateField(default=datetime.datetime.now)
    mq7_carbon_monoxide = peewee.IntegerField()
    temperature         = peewee.IntegerField()
    flammable_gas       = peewee.IntegerField()
    smoke               = peewee.IntegerField()

class Sensor_Output_Averages(peewee.Model):
    class Meta: 
        database = db

    #Define DB fields
    date_and_time       = peewee.DateField(default=datetime.datetime.now)
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
    date_and_time = peewee.DateField(default=datetime.datetime.now)

#Creates the Tables
def create_tables():
    try: 
        Sensor_Output_Averages.create_table()
    except peewee.OperationalError:
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

#Insert functions
def insert_sensor_output(mq7_output, temperature_output, flammable_gas_output, smoke_output):
    sensor_output = Current_Day_Sensor_Output(mq7_carbon_monoxide = mq7_output,
                                              temperature         = temperature_output, 
                                              flammable_gas       = flammable_gas_output,
                                              smoke               = smoke_output)
    sensor_output.save()
    print "Sensor Data Inserted.."

#Test Functions
def insert_test_data(simulated_output_level):
    sensor_output = None
    mq7_min       = None
    mq7_max       = None
    temp_min      = None
    temp_max      = None
    flammable_min = None
    flammable_max = None
    smoke_min     = None
    smoke_max     = None
    
    if(simulated_output_level == "NORMAL"):
        mq7_min       = 0 
        mq7_max       = 10
        temp_min      = 21 
        temp_max      = 27 
        flammable_min = 0
        flammable_max = 0
        smoke_min     = 0
        smoke_max     = 0
    elif(simulated_output_level == "EARLY_SIGNS"):
        mq7_min       = 10   
        mq7_max       = 150
        temp_min      = 27  
        temp_max      = 40  
        flammable_min = 10
        flammable_max = 150
        smoke_min     = 10
        smoke_max     = 150
    elif(simulated_output_level == "RED_ALERT"):
        mq7_min       = 150 
        mq7_max       = 400
        temp_min      = 40
        temp_max      = 80
        flammable_min = 150
        flammable_max = 400
        smoke_min     = 150
        smoke_max     = 400
        
    insert_sensor_output(mq7_output           = random.randint(mq7_min, mq7_max),
                         temperature_output   = random.randint(temp_min, temp_max),
                         flammable_gas_output = random.randint(flammable_min,flammable_max),
                         smoke_output         = random.randint(smoke_min, smoke_max))

#Main Section
create_tables()
insert_test_data("NORMAL")
insert_test_data("EARLY_SIGNS")
insert_test_data("RED_ALERT")
