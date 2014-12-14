#!/usr/bin/env python   

#Manages sensor configuration and probing 
#Author: Kevin Murphy
#Date  : 7 - Dec - 14

import sched
import time
from database_manager import DatabaseManager 
import constants as CONSTS

class SensorManager(object):
    DEBUG  = True
    LOGTAG = "SensorManager"

    __sensors   = {}
    __schedular = None
    __databaseManager = None

    __collectionRate     = CONSTS.COLLECTION_RATE_DEFAULT
    __collectionPriority = CONSTS.COLLECTION_PRIORITY_DEFAULT

    def __init__(self, sensors, database_manager):
        if self.DEBUG:
            print self.LOGTAG , " Created..."

        self.__schedular = sched.scheduler(time.time, time.sleep)

        if sensors is not None:
            self.setSensors(sensors)

        if database_manager is not None:
            self.setDatabaseManager(database_manager)

        self.startCollecting()
        self.startProbing()

    #PROBING SENSORS------------------------------------------------------
    #Starts all sensors probing depending on current configuration
    def startProbing(self):
        if self.DEBUG:
            print "Starting Sensor Probing.."

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
            print "Starting Data Collection..."
        
        self.__schedular.enter(self.__collectionRate, self.__collectionPriority, self.collectData,())

    def collectData(self):
        #mq7_output           = sensor[CONSTS.SENSOR_MQ7].getCurrentValue()
        #temperature_output   = sensor[CONSTS.SENSOR_THERMISTOR].getCurrentValue()
        #flammable_gas_output = sensor[CONSTS.SENSOR_FLAMMABLE_GAS].getCurrentValue()
        #motion_output        = sensor[CONSTS.MOTION].getCurrentValue()

        #DatabaseManager.getInstance().insert_sensor_output(mq7_output, temperature_output, flammable_gas_output, smoke_output)
        self.getDatabaseManager().insert_sensor_output(**self.getSensorValues())

        if self.DEBUG:
            print "/---Entering Data in DB---/"

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
