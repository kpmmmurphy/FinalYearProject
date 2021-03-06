#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 9 - Dec - 14

import peewee 
from peewee import *
import datetime
import random
import socket
import constants as CONSTS
import json
from configurable import Configurable

class DatabaseManager(Configurable):
    DEBUG = True
    TEST  = True
    LOGTAG = "DatabaseManager"

    #Aliases
    __max_co   = "max_carbon_monoxide"
    __min_co   = "min_carbon_monoxide"
    __avg_co   = "avg_carbon_monoxide"
    __max_flam = "max_flammable_gas"
    __min_flam = "min_flammable_gas"
    __avg_flam = "avg_flammable_gas"
    __max_temp = "max_temperature"
    __min_temp = "min_temperature"
    __avg_temp = "avg_temperature"
    __precentage_motion = "precentage_motion"
    __motion = "motion"

    #Private:
    __db = None

    def __init__(self):
        super(DatabaseManager, self).__init__(CONSTS.JSON_KEY_DATABASE_MANAGER_CONFIG)
        __db = self.loadDatabase()

    def configure(self, config):
        pass

    #Creates the Tables
    def create_tables(self):
        try:
            Current_Day_Sensor_Output.create_table()
        except peewee.OperationalError:
            print "DatabaseManager :: Exception -> Current Day Sensor_Output Table Already Exists"

        try:
            System_Details.create_table()
            self.insert_system_details(CONSTS.SYSTEM_NAME_DEFAULT, CONSTS.SYSTEM_LOCATION_DEFAULT, 
                                       CONSTS.SYSTEM_GPS_LAT_DEFAULT, CONSTS.SYSTEM_GPS_LNG_DEFAULT)
        except peewee.OperationalError:
            print "DatabaseManager :: Exception -> System_Details Table Already Exists"

        '''
        try: 
            Sensor_Output_Averages.create_table()
        except peewee.OperationalError:
            print "Sensor output Averages Table Already Exists"

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

    def insert_system_details(self, name, location, gps_lat, gps_lng):

        system_details = System_Details(name     = name,
                                        location = location, 
                                        gps_lat  = gps_lat,
                                        gps_lng  = gps_lng)
        system_details.save()

        if self.DEBUG:
            print self.LOGTAG, " :: Updated System Details.."

    #Select methods
    def select_system_details(self):
        systemDetails = System_Details.select().order_by(System_Details.id.desc())
        return systemDetails[0]

    def select_current_day_max_min_sensor_values(self):
        minMaxVals = None
        today = datetime.datetime.now()
        max_min_values = Current_Day_Sensor_Output.select(fn.Max(Current_Day_Sensor_Output.carbon_monoxide).alias(self.__max_co),
                                                          fn.Min(Current_Day_Sensor_Output.carbon_monoxide).alias(self.__min_co),
                                                          fn.Max(Current_Day_Sensor_Output.flammable_gas).alias(self.__max_flam),
                                                          fn.Min(Current_Day_Sensor_Output.flammable_gas).alias(self.__min_flam),
                                                          fn.Max(Current_Day_Sensor_Output.temperature).alias(self.__max_temp),
                                                          fn.Min(Current_Day_Sensor_Output.temperature).alias(self.__min_temp),
                                                          (fn.SUM(Current_Day_Sensor_Output.motion)/fn.COUNT(Current_Day_Sensor_Output.motion)*100).alias(self.__precentage_motion)
                                                          ).where(Current_Day_Sensor_Output.date_and_time.between(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1)))
        max_min_values = max_min_values[0]
        try: 
            minMaxVals = { self.__max_co   : max_min_values.max_carbon_monoxide, self.__min_co   : max_min_values.min_carbon_monoxide,
                           self.__max_flam : max_min_values.max_flammable_gas,   self.__min_flam : max_min_values.min_flammable_gas, 
                           self.__max_temp : max_min_values.max_temperature,     self.__min_temp : max_min_values.min_temperature,
                           self.__precentage_motion : int(float(max_min_values.precentage_motion))}
        except TypeError:
            if self.DEBUG:
                print self.LOGTAG, " :: Max/Min values type error",

        return minMaxVals

    def select_current_hour_sensor_values(self):
        currentDayValues = []
        now = datetime.datetime.now()
        cur_day_vals = Current_Day_Sensor_Output.select().dicts().where(Current_Day_Sensor_Output.date_and_time.between(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1)) & (Current_Day_Sensor_Output.date_and_time.hour == now.hour))
        for item in cur_day_vals:
            currentDayValues.append(item)
        return currentDayValues

    def select_agg_hour_current_day_sensor_values(self):
        aggHourValues = []
        today = datetime.datetime.now()
        agg_values = Current_Day_Sensor_Output.select(Current_Day_Sensor_Output.date_and_time,
                                                      fn.Max(Current_Day_Sensor_Output.carbon_monoxide).alias(self.__max_co),
                                                      fn.Min(Current_Day_Sensor_Output.carbon_monoxide).alias(self.__min_co),
                                                      fn.Avg(Current_Day_Sensor_Output.carbon_monoxide).alias(self.__avg_co),
                                                      fn.Max(Current_Day_Sensor_Output.flammable_gas).alias(self.__max_flam),
                                                      fn.Min(Current_Day_Sensor_Output.flammable_gas).alias(self.__min_flam),
                                                      fn.Avg(Current_Day_Sensor_Output.flammable_gas).alias(self.__avg_flam),
                                                      fn.Max(Current_Day_Sensor_Output.temperature).alias(self.__max_temp),
                                                      fn.Min(Current_Day_Sensor_Output.temperature).alias(self.__min_temp),
                                                      fn.Avg(Current_Day_Sensor_Output.temperature).alias(self.__avg_temp),
                                                     (fn.Sum(Current_Day_Sensor_Output.motion)/fn.Count(Current_Day_Sensor_Output.motion)*100).alias(self.__motion)
                                                     ).where(Current_Day_Sensor_Output.date_and_time.between(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1))).group_by(Current_Day_Sensor_Output.date_and_time.hour).dicts()
        for item in agg_values:
            aggHourValues.append(item)
        return aggHourValues

    def select_agg_day_sensor_values(self):
        aggDayValues = []
        today = datetime.datetime.now()
        agg_values = Current_Day_Sensor_Output.select(Current_Day_Sensor_Output.date_and_time,
                                                      fn.Max(Current_Day_Sensor_Output.carbon_monoxide).alias(self.__max_co),
                                                      fn.Min(Current_Day_Sensor_Output.carbon_monoxide).alias(self.__min_co),
                                                      fn.Avg(Current_Day_Sensor_Output.carbon_monoxide).alias(self.__avg_co),
                                                      fn.Max(Current_Day_Sensor_Output.flammable_gas).alias(self.__max_flam),
                                                      fn.Min(Current_Day_Sensor_Output.flammable_gas).alias(self.__min_flam),
                                                      fn.Avg(Current_Day_Sensor_Output.flammable_gas).alias(self.__avg_flam),
                                                      fn.Max(Current_Day_Sensor_Output.temperature).alias(self.__max_temp),
                                                      fn.Min(Current_Day_Sensor_Output.temperature).alias(self.__min_temp),
                                                      fn.Avg(Current_Day_Sensor_Output.temperature).alias(self.__avg_temp),
                                                     (fn.Sum(Current_Day_Sensor_Output.motion)/fn.Count(Current_Day_Sensor_Output.motion)*100).alias(self.__motion)
                                                     ).group_by(Current_Day_Sensor_Output.date_and_time.day).dicts()
        for item in agg_values:
            aggDayValues.append(item)
        return aggDayValues

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
    
    def getDatabase(self):
        return self.__db  
    
    @staticmethod
    def loadDatabase():
        db = None
        if CONSTS.TESTING_SQL:
            db_passwd = CONSTS.DB_PASSWD_PI
            if socket.gethostname() != CONSTS.RASP_PI:
                db_passwd = CONSTS.DB_PASSWD_UBUNTU
            db = peewee.MySQLDatabase(CONSTS.DB_NAME, user=CONSTS.DB_USER, passwd=db_passwd)            
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
    name       = peewee.CharField()
    location   = peewee.CharField()
    gps_lat    = peewee.CharField()   
    gps_lng    = peewee.CharField()  
