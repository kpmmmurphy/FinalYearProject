#!/usr/bin/env python

#MQ7 Carbon Dioxide Sensor 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

import ctypes
from sensor import Sensor
          
class MQ7(Sensor):
    __name         = "MQ7 Carbon Dioxide"
    __adcChannelNo = 1
    __lib = None

    def __init__(self, lib):
        self.__lib = lib
    	#Setup args for ctypes
    	self.__lib.MQ7_newInstance.argtypes = [ctypes.c_char_p, ctypes.c_int]

        #Setup return types for ctypes
    	self.__lib.MQ7_initPins.restype  = None
    	self.__lib.MQ7_readValue.restype = ctypes.c_int
    	self.__lib.MQ7_test.restype      = ctypes.c_int 
    	

    	self.obj = self.__lib.MQ7_newInstance(self.__name, self.__adcChannelNo)
    	self.initPins()

    def initPins(self):
        self.__lib.MQ7_initPins(self.obj)

    def readValue(self):
        return self.__lib.MQ7_readValue(self.obj) 

    def getName(self):
        return self.__name

    def test(self):
        print self.__lib.Mq7_test()

    


