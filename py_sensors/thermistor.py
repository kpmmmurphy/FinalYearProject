#!/usr/bin/env python

#Thermistor Sensor 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

import ctypes
from sensor import Sensor
import constants as CONSTS

class Thermistor(Sensor):
    DEBUG = True

    __name         = CONSTS.SENSOR_THERMISTOR
    __adcChannelNo = 0
    __lib = None
    
    def __init__(self, lib, alertManager):
        if lib is None:
            if self.DEBUG:
                print self.getName().upper(), " :: Constructing -> without shared lib... "
        else:
            if self.DEBUG:
                print self.getName().upper(), " :: Constructing -> with shared lib... "
            super(Thermistor, self).__init__(alertManager)
            self.__lib = lib
            #Setup arg for ctypes
            self.__lib.Thermistor_newInstance.argtypes = [ctypes.c_char_p, ctypes.c_int]
            #Setup return types for ctypes
            self.__lib.Thermistor_initPins.restype  = None
            self.__lib.Thermistor_readValue.restype = ctypes.c_int
            self.__lib.Thermistor_test.restype      = ctypes.c_int 
            self.obj = self.__lib.Thermistor_newInstance(self.__name, self.__adcChannelNo)
            self.initPins()

        self.setAlertThreshold(CONSTS.ALERT_THRESHOLD_DEFAULT_THERMISTOR)

    def initPins(self):
        if self.__lib is not None:
            self.__lib.Thermistor_initPins(self.obj)

    def readValue(self):
        if self.__lib is None:
            self.setCurrentValue(self.test())
        else:    
            self.setCurrentValue(self.__lib.Thermistor_readValue(self.obj)) 
        
        self.react(self.getCurrentValue())
        return self.getCurrentValue()

    def react(self, value):
        if value >= self.getAlertThreshold():
            if self.DEBUG:
                print self.getName().upper(), " :: ALERT"

            if self.getAlertManager() is not None:
                self.getAlertManager().ringBuzzer()

    def getName(self):
        return self.__name

    def test(self):
        if self.__lib is None:
            return -1
        else:    
            return self.__lib.Thermistor_test()

    


