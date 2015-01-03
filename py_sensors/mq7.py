#!/usr/bin/env python

#MQ7 Carbon Dioxide Sensor 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

import ctypes
from sensor import Sensor
import constants as CONSTS
          
class MQ7(Sensor):
    DEBUG = True

    __name         = CONSTS.SENSOR_MQ7
    __adcChannelNo = 1
    __lib = None

    __previousValue = None

    def __init__(self, lib):
        if lib is None:
            if self.DEBUG:
                print self.getName().upper(), " :: Constructing -> without shared lib... "
        else:
            if self.DEBUG:
                print self.getName().upper(), " :: Constructing -> with shared lib... "
            self.__lib = lib
    	    #Setup args for ctypes
            self.__lib.MQ7_newInstance.argtypes = [ctypes.c_char_p, ctypes.c_int]
    
            #Setup return types for ctypes
            self.__lib.MQ7_initPins.restype  = None
            self.__lib.MQ7_readValue.restype = ctypes.c_int
            self.__lib.MQ7_test.restype      = ctypes.c_int 
            self.obj = self.__lib.MQ7_newInstance(self.__name, self.__adcChannelNo)
    	    self.initPins()

        self.setAlertThreshold(CONSTS.ALERT_THRESHOLD_DEFAULT_MQ7)

    def initPins(self):
        if self.__lib is not None:
            self.__lib.MQ7_initPins(self.obj)

    def readValue(self):
        if self.__lib is None:
            latestValue = self.test()
        else:        
            #self.setCurrentValue(self.__lib.MQ7_readValue(self.obj)) 
            latestValue = self.__lib.MQ7_readValue(self.obj) 

        self.setCurrentValue(self.calculateCurrentValue(latestValue))
        self.react(self.getCurrentValue())

        return self.getCurrentValue()

    def react(self, value):
        if value >= self.getAlertThreshold():
            if self.DEBUG:
                print self.getName().upper(), " :: ALERT"

    def getName(self):
        return self.__name

    def calculateCurrentValue(self, latestValue):
        if self.__previousValue is None:
            self.__previousValue = latestValue
            
        return max((self.getCurrentValue()) + (latestValue - self.__previousValue), 0)

    def test(self):
        #If __lib is set, then test the .so file, other wise produce a default test value -1
        if self.__lib is None:
            return -1
        else:
            return self.__lib.Mq7_test()

    


