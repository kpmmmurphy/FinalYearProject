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

class SensorManager(object):
    LOGTAG = "SensorManager"
    __sensors = []

    def __init__(self):
        print self.LOGTAG , "Created..."

    def addSensors(sensors):
        self.__sensors = sensors


class SensorFactory(object):
    #Constants
    LOGTAG = "SensorFactory"
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
        print self.LOGTAG , "Created..."

        if os.name is not self.PC_OS:
            self.__sensorLib = ctypes.cdll.LoadLibrary(self.LIB_PATH)

        self.createAllSensors()

    def createAllSensors(self):
        self.getInstance_MQ7()
        self.getInstance_Thermistor()
        self.getInstance_MotionDetector()

    def getSensors(self):
        return self.__sensors

    def getInstance_MQ7(self):
        if self.__mq7 is None:
            if self.__sensorLib is None:
               self.__mq7 = MQ7(lib=None)
            else:
               self.__mq7 = MQ7(lib=self.__sensorLib)

            self.__sensors.append(self.__mq7)

        return self.__mq7

    def getInstance_Thermistor(self):
        if self.__thermistor is None:
            if self.__sensorLib is None:
               self.__thermistor = Thermistor(lib=None)
            else:
               self.__thermistor = Thermistor(lib=self.__sensorLib)

            self.__sensors.append(self.__thermistor)

        return self.__thermistor

    def getInstance_MotionDetector(self):
        if self.__motionDetector is None:
            if self.__sensorLib is None:
               self.__motionDetector = MotionDetector(lib=None)
            else:
               self.__motionDetector = MotionDetector(lib=self.__sensorLib)

            self.__sensors.append(self.__motionDetector) 
        
        return self.__motionDetector
