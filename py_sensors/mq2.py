#!/usr/bin/env python

#MQ2 Flammable Gas Sensor 
#Author: Kevin Murphy
#Date  : 14 - Dec - 14

import ctypes
from sensor import Sensor
import constants as CONSTS
          
class MQ2(Sensor):
    DEBUG = True

    __name         = CONSTS.SENSOR_MQ2
    __adcChannelNo = 2
    __lib = None

    def __init__(self, lib, alertManager):
        if lib is None:
            if self.DEBUG:
                print self.getName().upper(), " :: Constructing -> without shared lib... "
        else:
            if self.DEBUG:
                print self.getName().upper(), " :: Constructing -> with shared lib... "
            super(MQ2, self).__init__(alertManager)
            self.__lib = lib
    	    #Setup args for ctypes
            self.__lib.MQ2_newInstance.argtypes = [ctypes.c_char_p, ctypes.c_int]
    
            #Setup return types for ctypes
            self.__lib.MQ2_initPins.restype  = None
            self.__lib.MQ2_readValue.restype = ctypes.c_int
            self.__lib.MQ2_test.restype      = ctypes.c_int 
        	   
            self.obj = self.__lib.MQ2_newInstance(self.__name, self.__adcChannelNo)
    	    self.initPins()

        self.setAlertThreshold(CONSTS.ALERT_THRESHOLD_DEFAULT_MQ2)

    def initPins(self):
        if self.__lib is not None:
            self.__lib.MQ2_initPins(self.obj)

    def readValue(self):
        if self.__lib is None:
            self.setCurrentValue(self.test())
        else:        
            self.setCurrentValue(self.__lib.MQ2_readValue(self.obj)) 
        
        self.react(self.getCurrentValue())
        return self.getCurrentValue()

    def react(self, value):
        if value >= self.getAlertThreshold():
            if self.DEBUG:
                print self.getName().upper(), " :: ALERT"

            if self.getAlertManager is not None:
                self.getAlertManager().ringBuzzer()

    def getName(self):
        return self.__name

    def test(self):
        #If __lib is set, then test the .so file, other wise produce a default test value -1
        if self.__lib is None:
            return -1
        else:
            return self.__lib.MQ2_test()

    


