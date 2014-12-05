#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

import os
import ctypes
import time
import sched

#Import Sensors
from py_sensors.thermistor import Thermistor
from py_sensors.mq7 import MQ7
from py_sensors.motion_detector import MotionDetector

#Constants
DEBUG = True

#Global Sensors
thermistor      = None
mq7             = None
motion_detector = None

class SensorFactory(object):
    #Constants
    PC_OS     = "posix"
    LIB_PATH  = "./sensors/libs/lib_SensorManager.so"
    __sensorLib = None

    #Singletons
    __mq7            = None
    __thermistor     = None
    __motionDetector = None

    #Sensor Holder
    __sensors = []

    def __init__(self):
        print "SensorFactory Created..."
        
        if os.name is not self.PC_OS:
            self.__sensorLib = ctypes.cdll.LoadLibrary(self.LIB_PATH)

        self.createAllSensors()

    def createAllSensors(self):
        self.newInstance_MQ7()
        self.newInstance_Thermistor()
        self.newInstance_MotionDetector()

    def getSensors(self):
        return self.__sensors

    def newInstance_MQ7(self):
        if self.__mq7 is None:
            if self.__sensorLib is None:
               self.__mq7 = MQ7(lib=None)
            else:
               self.__mq7 = MQ7(lib=self.__sensorLib)

            self.__sensors.append(self.__mq7)

        return self.__mq7

    def newInstance_Thermistor(self):
        if self.__thermistor is None:
            if self.__sensorLib is None:
               self.__thermistor = Thermistor(lib=None)
            else:
               self.__thermistor = Thermistor(lib=self.__sensorLib)

            self.__sensors.append(self.__thermistor)

        return self.__thermistor

    def newInstance_MotionDetector(self):
        if self.__motionDetector is None:
            if self.__sensorLib is None:
               self.__motionDetector = MotionDetector(lib=None)
            else:
               self.__motionDetector = MotionDetector(lib=self.__sensorLib)

            self.__sensors.append(self.__motionDetector) 
        return self.__motionDetector



def probeSensor(sched, sensor):
    if sensor.isActive():
        sensorValue = sensor.readValue()
        if DEBUG:
            print sensor.getName() , " :: " , sensorValue

        sched.enter(sensor.getProbeRate(), sensor.getPriority(), probeSensor,(sched, sensor))

        return sensorValue

def main():
    sensorFactory = SensorFactory() 
    
    schedular = sched.scheduler(time.time, time.sleep)	
    for sensor in sensorFactory.getSensors():
        schedular.enter(sensor.getProbeRate(), sensor.getPriority(), probeSensor, (schedular, sensor))
   
    schedular.run()

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."

