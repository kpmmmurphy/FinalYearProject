#!/usr/bin/env python   

#Factroy for creating Sensor Singletons
#Author: Kevin Murphy
#Date  : 5 - Dec - 14

import os
import ctypes
import socket
import subprocess
import constants as CONSTS

#Import Sensors
from py_sensors.thermistor import Thermistor
from py_sensors.mq7 import MQ7
from py_sensors.mq2 import MQ2
from py_sensors.motion_detector import MotionDetector

class SensorFactory(object):
    #Constants
    DEBUG  = True
    LOGTAG = "SensorFactory"

    LIB_PATH  = "./sensors/libs/lib_SensorManager.so"
    __sensorLib = None

    #Singletons
    __mq7            = None
    __thermistor     = None
    __motionDetector = None
    __mq2            = None

    #Sensor Holder
    __sensors = []

    def __init__(self):
        if self.DEBUG:
            print self.LOGTAG , " :: Created..."

        if socket.gethostname() == CONSTS.RASP_PI:
            subprocess.call("gpio load spi", shell=True)
            self.__sensorLib = ctypes.cdll.LoadLibrary(self.LIB_PATH)

        self.createAllSensors()

    def createAllSensors(self):
        self.getInstance_MQ7()
        self.getInstance_MQ2()
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

    def getInstance_MQ2(self):
        if self.__mq2 is None:
            if self.__sensorLib is None:
               self.__mq2 = MQ2(lib=None)
            else:
<<<<<<< HEAD
               #self.__mq2 = MQ2(lib=self.__sensorLib)
               self.__mq2 = MQ2(lib=None)
=======
               self.__mq2 = MQ2(lib=self.__sensorLib)
               self.__mq2 = MQ2(lib=None)

>>>>>>> d45039e... Fixed the mess I made for myself after coding on the Pi for the first time in weeks
            self.__sensors.append(self.__mq2)

        return self.__mq2

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
