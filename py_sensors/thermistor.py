#!/usr/bin/env python

#Thermistor Sensor 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

import ctypes
from sensor import Sensor

class Thermistor(Sensor):
    __name         = "Thermistor"
    __adcChannelNo = 0
    __lib = None
    
    def __init__(self, lib):
    	self.__lib = lib

        #Setup arg for ctypes
    	self.__lib.Thermistor_newInstance.argtypes = [ctypes.c_char_p, ctypes.c_int]

        #Setup return types for ctypes
    	self.__lib.Thermistor_initPins.restype  = None
    	self.__lib.Thermistor_readValue.restype = ctypes.c_int
	self.__lib.Thermistor_test.restype      = ctypes.c_int 
    	
    	self.obj = self.__lib.Thermistor_newInstance(self.__name, self.__adcChannelNo)
    	self.initPins()

    def initPins(self):
        self.__lib.Thermistor_initPins(self.obj)

    def readValue(self):
        return self.__lib.Thermistor_readValue(self.obj) 

    def getName(self):
        return self.__name

    def test(self):
        print self.__lib.Thermistor_test()

    


