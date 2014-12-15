#!/usr/bin/env python   

#Manages sensor configuration and probing 
#Author: Kevin Murphy
#Date  : 7 - Dec - 14

import sched
import time
import json
from database_manager import DatabaseManager 
import constants as CONSTS
from configurable import Configurable

class SensorManager(Configurable):
    DEBUG  = True
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

        if sensors is not None:
            self.setSensors(sensors)
            self.configure(None)
            self.startProbing()


        if database_manager is not None:
            self.setDatabaseManager(database_manager)
            self.startCollecting()


    #PROBING SENSORS------------------------------------------------------
    #Starts all sensors probing depending on current configuration
    def startProbing(self):
        if self.DEBUG:
            print self.LOGTAG, " :: Starting Sensor Probing.."

        for name, sensor in self.getSensors().iteritems():
            if self.DEBUG:
                sensor.toString()

            self.__schedular.enter(sensor.getProbeRate(), sensor.getPriority(), self.probeSensor, (sensor,))
   
        self.__schedular.run()

    #Stops all sensors probing
    def stopProbing(self):
        for name, sensor in self.getSensors().iteritem():
            sensor.setActiveStatus(False)

    def probeSensor(self, sensor):
        if sensor.isActive():
            sensor.setCurrentValue(sensor.readValue())
            if self.DEBUG:
                print sensor.getName() , " :: " , sensor.getCurrentValue()

            self.__schedular.enter(sensor.getProbeRate(), sensor.getPriority(), self.probeSensor,(sensor,))

    #COLLECTING DATA-----------------------------------------------------
    def startCollecting(self):
        if self.DEBUG:
            print self.LOGTAG, " :: Starting Data Collection"
        
        self.__schedular.enter(self.__collectionRate, self.__collectionPriority, self.collectData,())

    def collectData(self):
        #mq7_output           = sensor[CONSTS.SENSOR_MQ7].getCurrentValue()
        #temperature_output   = sensor[CONSTS.SENSOR_THERMISTOR].getCurrentValue()
        #flammable_gas_output = sensor[CONSTS.SENSOR_FLAMMABLE_GAS].getCurrentValue()
        #motion_output        = sensor[CONSTS.MOTION].getCurrentValue()

        #DatabaseManager.getInstance().insert_sensor_output(mq7_output, temperature_output, flammable_gas_output, smoke_output)
        self.getDatabaseManager().insert_sensor_output(**self.getSensorValues())

        if self.DEBUG:
            print self.LOGTAG, " :: Entering Data in DB"

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

        



