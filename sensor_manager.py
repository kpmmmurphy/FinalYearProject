#!/usr/bin/env python   

#Manages sensor configuration and probing 
#Author: Kevin Murphy
#Date  : 7 - Dec - 14

import sched
import thread
from threading import Timer
import time
import json
from database_manager import DatabaseManager 
import constants as CONSTS
from configurable import Configurable

class SensorManager(Configurable):
    DEBUG  = False
    USING_TIMER  = True 
    LOGTAG = "SensorManager"

    __sensors   = {}
    __schedular = None
    __databaseManager = None

    __collectionRate     = CONSTS.COLLECTION_RATE_DEFAULT
    __collectionPriority = CONSTS.COLLECTION_PRIORITY_DEFAULT

    def __init__(self, sensors, database_manager):
        if self.DEBUG:
            print self.LOGTAG , " :: Created..."

        self.__schedular = sched.scheduler(time.time, time.sleep)

        if database_manager is not None:
            self.setDatabaseManager(database_manager)
            self.startCollecting()

        if sensors is not None:
            self.setSensors(sensors)
            self.configure(None)
            self.startProbing()

        self.__schedular.run()

    #PROBING SENSORS------------------------------------------------------
    #Starts all sensors probing depending on current configuration
    def startProbing(self):
        if self.DEBUG:
            print self.LOGTAG, " :: Starting Sensor Probing.."

        for name, sensor in self.getSensors().iteritems():
            if self.DEBUG:
                sensor.toString()
            
            if self.USING_TIMER:
                timer = Timer(sensor.getProbeRate(), self.probeSensor,(sensor,))
                timer.start()
            else:
                self.__schedular.enter(sensor.getProbeRate(), sensor.getPriority(), self.probeSensor, (sensor,))
                
    #Stops all sensors probing
    def stopProbing(self):
        for name, sensor in self.getSensors().iteritem():
            sensor.setActiveStatus(False)

    def probeSensor(self, sensor):
        if sensor.isActive():
            sensor.readValue()
            if self.DEBUG:
                print sensor.getName() , " :: " , sensor.getCurrentValue()

            if self.USING_TIMER:
                timer = Timer(sensor.getProbeRate(), self.probeSensor, (sensor,))
                timer.start()
            else:    
                self.__schedular.enter(sensor.getProbeRate(), sensor.getPriority(), self.probeSensor,(sensor,))

    #COLLECTING DATA-----------------------------------------------------
    def startCollecting(self):
        if self.DEBUG:
            print self.LOGTAG, " :: Starting Data Collection"
        
        if self.USING_TIMER:
            timer = Timer(self.__collectionRate, self.collectData, ())
            timer.start()
        else:
            self.__schedular.enter(self.__collectionRate, self.__collectionPriority, self.collectData,())

    def collectData(self):
        self.getDatabaseManager().insert_sensor_output(**self.getSensorValues())

        if self.DEBUG:
            print self.LOGTAG, " :: Entering Data in DB"
        
        if self.USING_TIMER:
            timer = Timer(self.__collectionRate, self.collectData, ())
            timer.start()
        else:
            self.__schedular.enter(self.__collectionRate, self.__collectionPriority, self.collectData,())
    
    def setSensors(self, sensors):
        for sensor in sensors:
            self.__sensors[sensor.getName()] = sensor

    def getSensors(self):
        return self.__sensors

    def getSensorValues(self):
        sensorValues = {}
        for name, sensor in self.getSensors().iteritems():
            sensorValues[name] = sensor.getCurrentValue()
        return sensorValues

    def setDatabaseManager(self, database_manager):
        self.__databaseManager = database_manager

    def getDatabaseManager(self):
        return self.__databaseManager

    def getCollectionRate(self):
        return self.__collectionRate

    def setCollectionRate(self, value):
        if value is not None:
            self.__collectionRate = value

    def getCollectionPriority(self):
        return self.__collectionPriority

    def setCollectionPriority(self, value):
        if value is not None:
            self.__collectionPriority = value

    def configure(self, config):
        if self.DEBUG:
            print self.LOGTAG, " :: Updating Configuration"

        if config is None:
            config_data = open(CONSTS.CONFIGURATION_DEFAULT)
            config      = json.load(config_data)

        #Collection Config
        collectionConfig  = config[CONSTS.JSON_KEY_COLLECTION_OBJ]
        self.setCollectionRate(collectionConfig[CONSTS.JSON_KEY_COLLECTION_RATE])
        self.setCollectionPriority(collectionConfig[CONSTS.JSON_KEY_COLLECTION_PRIORITY])
        
        #Sensors Config
        for sensorConfig in config[CONSTS.JSON_KEY_SENSORS_ARRAY]:
            self.getSensors()[sensorConfig[CONSTS.JSON_KEY_SENSOR_NAME]].configure(sensorConfig)
        
        if config_data is not None:
            config_data.close()

        



