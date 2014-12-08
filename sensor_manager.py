#!/usr/bin/env python   

#Manages sensor configuration and probing 
#Author: Kevin Murphy
#Date  : 7 - Dec - 14

import sched
import time

class SensorManager(object):
    DEBUG = True
    LOGTAG = "SensorManager"
    __sensors = []
    __schedular = None

    def __init__(self, sensors):
        if self.DEBUG:
            print self.LOGTAG , " Created..."

        self.__schedular = sched.scheduler(time.time, time.sleep)
        if sensors is not None:
            self.setSensors(sensors)

        self.startProbing()

    #def updateConfigurations(self):

    #Starts all sensors probing depending on current configuration
    def startProbing(self):
        for sensor in self.getSensors():
            if self.DEBUG:
                sensor.toString()

            self.__schedular.enter(sensor.getProbeRate(), sensor.getPriority(), self.probeSensor, (sensor,))
   
        self.__schedular.run()

    #Stops all sensors probing
    def stopProbing(self):
        for sensor in self.getSensors():
            sensor.setActiveStatus(False)

    def probeSensor(self, sensor):
        if sensor.isActive():
            sensor.setCurrentValue(sensor.readValue())
            if self.DEBUG:
                print sensor.getName() , " :: " , sensor.getCurrentValue()

            self.__schedular.enter(sensor.getProbeRate(), sensor.getPriority(), self.probeSensor,(sensor))

    def setSensors(self, sensors):
        self.__sensors = sensors

    def getSensors(self):
        return self.__sensors
