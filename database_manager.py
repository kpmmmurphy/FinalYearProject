#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 9 - Dec - 14

import peewee 
from peewee import *
import datetime
import random
import socket
import constants as CONSTS
from configurable import Configurable

class DatabaseManager(Configurable):
    DEBUG = True
    TEST  = True
    LOGTAG = "DatabaseManager"

    #Private:
    __db = None

    def __init__(self):
        super(DatabaseManager, self).__init__(CONSTS.JSON_KEY_DATABASE_MANAGER_CONFIG)
        __db = self.loadDatabase()
        self.createTables()

    def configure(self, config):
        pass

    #Creates the Tables
    @staticmethod
    def create_tables():
        try:
            Current_Day_Sensor_Output.create_table()
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
    def insert_sensor_output(self, carbon_monoxide, temperature, flammable_gas, motion):

        sensor_output = Current_Day_Sensor_Output(carbon_monoxide = carbon_monoxide,
                                                  temperature     = temperature, 
                                                  flammable_gas   = flammable_gas,
                                                  motion          = motion)
        sensor_output.save()

        if self.DEBUG:
            print self.LOGTAG, " :: Sensor Data Inserted.."
   
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
            
        self.insert_sensor_output(carbon_monoxide = random.randint(mq7_min, mq7_max),
                                  temperature     = random.randint(temp_min, temp_max),
                                  flammable_gas   = random.randint(flammable_min,flammable_max),
                                  motion          = random.randint(motion_min, motion_max))
    
    def createTables(self):
        #Main Section
        self.create_tables()
        if self.DEBUG:
            self.insert_test_data("NORMAL")
            self.insert_test_data("EARLY_SIGNS")
            self.insert_test_data("RED_ALERT")    

    def getDatabase(self):
        return self.__db  
    
    @staticmethod
    def loadDatabase():
        db = None
        if CONSTS.TESTING_SQL:
            #Local
            db = peewee.MySQLDatabase(CONSTS.DB_NAME, user=CONSTS.DB_USER, passwd=CONSTS.DB_PASSWD)            
        else:
            #CS1
            db = peewee.MySQLDatabase(CONSTS.DB_NAME, host=CONSTS.DB_HOST, port=CONSTS.DB_PORT, user=CONSTS.DB_USER, passwd=CONSTS.DB_PASSWD)

        return db

    def toString(self):
        pass

#MODELS------------------------------------------------------- 
class BaseModel(peewee.Model):
    class Meta:    
        database = DatabaseManager.loadDatabase()

class Current_Day_Sensor_Output(BaseModel):
    
    def save(self, *args, **kwargs):
        self.date_and_time = datetime.datetime.now()
        super(Current_Day_Sensor_Output, self).save(*args, **kwargs)

    #Define DB fields
    date_and_time       = peewee.DateTimeField(formats=CONSTS.SQL_DATE_FORMAT)
    carbon_monoxide     = peewee.IntegerField()
    temperature         = peewee.IntegerField()
    flammable_gas       = peewee.IntegerField()
    motion              = peewee.IntegerField()

class Sensor_Output_Averages(BaseModel):

    def save(self, *args, **kwargs):
        self.date_and_time = datetime.datetime.now()
        super(myModel, self).save(*args, **kwargs)

    #Define DB fields
    date_and_time       = peewee.DateTimeField(formats=CONSTS.SQL_DATE_FORMAT)
    carbon_monoxide     = peewee.IntegerField()
    temperature         = peewee.IntegerField()
    flammable_gas       = peewee.IntegerField()
    motion              = peewee.IntegerField()

class System_Admin_Details(BaseModel):

    def save(self, *args, **kwargs):
        self.date_and_time = datetime.datetime.now()
        super(myModel, self).save(*args, **kwargs)

    #Define DB Fields
    last_name     = peewee.CharField()
    first_name    = peewee.CharField()
    device_id     = peewee.CharField()
    date_and_time = peewee.DateTimeField(formats=CONSTS.SQL_DATE_FORMAT)

class System_Details(BaseModel):

    #Define DB Fields
    name              = peewee.CharField()
    location          = peewee.CharField()
    ip_address        = peewee.CharField()
    gps_coords_aprrox = peewee.CharField()   
