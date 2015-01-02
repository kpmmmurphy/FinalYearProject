#!/usr/bin/env python

#PIR Motion Detection Sensor 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

import ctypes
import subprocess
from sensor import Sensor
import constants as CONSTS
          
class MotionDetector(Sensor):
    DEBUG = True

    __name         = CONSTS.SENSOR_MOTION
    __adcChannelNo = -1
    __lib = None

    def __init__(self, lib):
        if lib is None:
            if self.DEBUG:
                print self.getName().upper(), " :: Constructing -> without shared lib... "
        else:
            if self.DEBUG:
                print self.getName().upper(), " :: Constructing -> with shared lib... "
            self.__lib = lib
        	#Setup args for ctypes
            self.__lib.MotionDetector_newInstance.argtypes = [ctypes.c_char_p, ctypes.c_int]
            #Setup return types for ctypes
            self.__lib.MotionDetector_initPins.restype  = None
            self.__lib.MotionDetector_readValue.restype = ctypes.c_int
            self.__lib.MotionDetector_test.restype      = ctypes.c_int 
        	
            self.obj = self.__lib.MotionDetector_newInstance(self.__name, self.__adcChannelNo)
            self.initPins()

        self.setAlertThreshold(CONSTS.ALERT_THRESHOLD_DEFAULT_MOTION)

    def initPins(self):
        if self.__lib is not None:
            self.__lib.MotionDetector_initPins(self.obj)

    def readValue(self):
        if self.__lib is None:
            self.setCurrentValue(self.test())
        else:    
            self.setCurrentValue(self.__lib.MotionDetector_readValue(self.obj)) 
        
        self.react(self.getCurrentValue())
        return self.getCurrentValue()

    def react(self, value):
        if value >= self.getAlertThreshold():
            print self.getName().upper(), " :: ALERT"
            subprocess.call(CONSTS.SCRIPT_TAKE_CAMERA_STILL, shell=True)

    def getName(self):
        return self.__name

    def test(self):
        if self.__lib is None:
            return -1
        else:
            return self.__lib.MotionDetector_test()

    


