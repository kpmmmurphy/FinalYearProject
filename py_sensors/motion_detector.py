#!/usr/bin/env python

#PIR Motion Detection Sensor 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

import ctypes
from sensor import Sensor

          
class MotionDetector(Sensor):
    __name         = "MotionDetector"
    __adcChannelNo = -1
    __lib = None

    def __init__(self, lib):
        if lib is None:
            print "Constructing ::", self.getName() , " Without shared lib... " 
        else:
            self.__lib = lib
        	#Setup args for ctypes
            self.__lib.MotionDetector_newInstance.argtypes = [ctypes.c_char_p, ctypes.c_int]
            #Setup return types for ctypes
            self.__lib.MotionDetector_initPins.restype  = None
            self.__lib.MotionDetector_readValue.restype = ctypes.c_int
            self.__lib.MotionDetector_test.restype      = ctypes.c_int 
        	
            self.obj = self.__lib.MotionDetector_newInstance(self.__name, self.__adcChannelNo)
            self.initPins()

    def initPins(self):
        if self.__lib is not None:
            self.__lib.MotionDetector_initPins(self.obj)

    def readValue(self):
        if self.__lib is None:
            return self.test()
        else:    
            return self.__lib.MotionDetector_readValue(self.obj) 

    def getName(self):
        return self.__name

    def test(self):
        if self.__lib is None:
            return -1
        else:
            return self.__lib.MotionDetector_test()

    


