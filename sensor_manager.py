#!/usr/bin/env python   

#Manages sensor configuration and probing 
#Author: Kevin Murphy
#Date  : 7 - Dec - 14

import sched
import time
import database_manager as Database_Manager

class SensorManager(object):
    DEBUG  = True
    LOGTAG = "SensorManager"

    DEFAULT_COLLECTION_RATE     = 15
    DEFAULT_COLLECTION_PRIORITY = 1

    __sensors   = {}
    __schedular = None

    __collectionRate     = DEFAULT_COLLECTION_RATE
    __collectionPriority = DEFAULT_COLLECTION_PRIORITY

    def __init__(self, sensors):
        if self.DEBUG:
            print self.LOGTAG , " Created..."

        self.__schedular = sched.scheduler(time.time, time.sleep)
        if sensors is not None:
            self.setSensors(sensors)

        self.startProbing() 

    #PROBING SENSORS------------------------------------------------------
    #Starts all sensors probing depending on current configuration
    def startProbing(self):
        for name, sensor in self.getSensors().iteritem():
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
        self.__schedular.enter(self.__collectionRate, sensor.__collectionPriority, self.collectData,())

    def collectData(self):
        #Decouple sensor outputs somehow :s 
        mq7_output = sensor[]
        temperature_output
        flammable_gas_output
        smoke_output
        Database_Manager.getInstance().insert_sensor_output(mq7_output, temperature_output, flammable_gas_output, smoke_output)
        self.__schedular.enter(self.__collectionRate, sensor.__collectionPriority, self.collectData,())


    def setSensors(self, sensors):
        for sensor in sensors:
            self.__sensors[sensor.getName()] = sensor

    def getSensors(self):
        return self.__sensors
