#!/usr/bin/env python

#Factroy for creating Sensor Singletons
#Author: Kevin Murphy
#Date  : 5 - Dec - 14

import os
import ctypes

#Import Sensors
from py_sensors.thermistor import Thermistor
from py_sensors.mq7 import MQ7
from py_sensors.motion_detector import MotionDetector

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