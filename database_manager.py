#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 9 - Dec - 14

import peewee 
from peewee import *
import datetime
import random

from py_models.sql_tables import current_day_sensor_output as Current

class DatabaseManager(object):
    DEBUG     =  True

    #Test Database Credentials
    TEST           =  True
    TEST_DB_NAME   = 'TEST'
    TEST_DB_USER   = 'root'
    TEST_DB_PASSWD = 'kevinmurphy'

    #Production Database Credentials
    DB_HOST   = 'csgate.ucc.ie'
    DB_NAME   = '2015_kpm2'
    DB_USER   = 'kpm2'
    DB_PASSWD = 'shiegeib'
    DB_PORT   = 80

    #Private:
    __db       = None

    def __init__(self):
        if self.TEST:
            self.__db = peewee.MySQLDatabase(self.TEST_DB_NAME, user=self.TEST_DB_USER, passwd=self.TEST_DB_PASSWD)            
        else:
            self.__db = peewee.MySQLDatabase(self.DB_NAME, host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWD)

    #Creates the Tables
    def create_tables(self):
        try:
            current_day_sensor_output.create_table()
        except peewee.OperationalError:
            print "Current Day Sensor_Output Table Already Exists"
        
        '''
        try: 
            Sensor_Output_Averages.create_table()
        except peewee.OperationalError:
            print "Sensor output Averages Table Already Exists"
    
        try:
            System_Details.create_table()
        except peewee.OperationalError:
            print "System_Details Table Already Exists"
    
        try: 
            System_Admin_Details.create_table()
        except peewee.OperationalError:
            print "System_Admin_Details Table Already Exists"
        '''

    #Insert functions
    def insert_sensor_output(self, mq7_output, temperature_output, flammable_gas_output, motion_output):
        sensor_output = current_day_sensor_output(mq7_carbon_monoxide = mq7_output,
                                                  temperature         = temperature_output, 
                                                  flammable_gas       = flammable_gas_output,
                                                  motion              = motion_output)
        sensor_output.save()
        if self.DEBUG:
            print "Sensor Data Inserted.."
    
    #Test Functions
    def insert_test_data(self, simulated_output_level):
        sensor_output = None
        mq7_min       = None
        mq7_max       = None
        temp_min      = None
        temp_max      = None
        flammable_min = None
        flammable_max = None
        motion_min     = None
        motion_max     = None
        
        if(simulated_output_level == "NORMAL"):
            mq7_min       = 0 
            mq7_max       = 10
            temp_min      = 21 
            temp_max      = 27 
            flammable_min = 0
            flammable_max = 0
            motion_min     = 0
            motion_max     = 0
        elif(simulated_output_level == "EARLY_SIGNS"):
            mq7_min       = 10   
            mq7_max       = 150
            temp_min      = 27  
            temp_max      = 40  
            flammable_min = 10
            flammable_max = 150
            motion_min     = 10
            motion_max     = 150
        elif(simulated_output_level == "RED_ALERT"):
            mq7_min       = 150 
            mq7_max       = 400
            temp_min      = 40
            temp_max      = 80
            flammable_min = 150
            flammable_max = 400
            motion_min     = 150
            motion_max     = 400
            
        insert_sensor_output(mq7_output           = random.randint(mq7_min, mq7_max),
                             temperature_output   = random.randint(temp_min, temp_max),
                             flammable_gas_output = random.randint(flammable_min,flammable_max),
                             motion_output         = random.randint(motion_min, motion_max))
    
    def createTables(self):
        #Main Section
        self.create_tables()
        if self.DEBUG:
            self.insert_test_data("NORMAL")
            self.insert_test_data("EARLY_SIGNS")
            self.insert_test_data("RED_ALERT")    

    def getDatabase(self):
        return self.__db        
    
    
    
    