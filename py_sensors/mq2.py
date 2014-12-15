#!/usr/bin/env python

#MQ2 Flammable Gas Sensor 
#Author: Kevin Murphy
#Date  : 14 - Dec - 14

import ctypes
from sensor import Sensor
import constants as CONSTS
          
class MQ2(Sensor):
    __name         = CONSTS.SENSOR_MQ2
    __adcChannelNo = 2
    __lib = None

    def __init__(self, lib):
        if lib is None:
            print "Constructing ::", self.getName() , " Without shared lib... "
        else:
            self.__lib = lib
    	    #Setup args for ctypes
            self.__lib.MQ2_newInstance.argtypes = [ctypes.c_char_p, ctypes.c_int]
    
            #Setup return types for ctypes
            self.__lib.MQ2_initPins.restype  = None
            self.__lib.MQ2_readValue.restype = ctypes.c_int
            self.__lib.MQ2_test.restype      = ctypes.c_int 
        	   
            self.obj = self.__lib.MQ2_newInstance(self.__name, self.__adcChannelNo)
    	    self.initPins()

    def initPins(self):
        if self.__lib is not None:
            self.__lib.MQ2_initPins(self.obj)

    def readValue(self):
        if self.__lib is None:
            self.__currentValue = self.test()
        else:        
            self.__currentValue = self.__lib.MQ2_readValue(self.obj) 

        return self.__currentValue

    def getName(self):
        return self.__name

    def test(self):
        #If __lib is set, then test the .so file, other wise produce a default test value -1
        if self.__lib is None:
            return -1
        else:
            return self.__lib.MQ2_test()

    


