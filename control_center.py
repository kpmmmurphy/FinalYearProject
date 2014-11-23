#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

import ctypes

LIB_PATH = "./sensors/libs/lib_SensorManager.so"

lib = ctypes.cdll.LoadLibrary(LIB_PATH)

class Sensor(object):

    def __init__(self):
        print "__Creating new Sensor__"

    def getInstance(self):
        raise NotImplementedError('Subclass must override Constructor')

    def getName(self):
        raise NotImplementedError('Subclass must override getName')

    def readValue(self):
        raise NotImplementedError('Subclass must override readValue')

    def initPins(self):
        raise NotImplementedError('Subclass must override initPins')
            
class Thermistor(Sensor):
    __name         = "Thermistor"
    __adcChannelNo = 0
    __instance     = None

    def __init__(self, *args, **kwargs):
	#Setup arg ctypes------------
	lib.Thermistor_newInstance.argtypes = [ctypes.c_char_p, ctypes.c_int]
	#lib.Thermistor_newInstance.restype  = Thermistor

        #Setup return types for ctypes
	lib.Thermistor_initPins.restype  = None
	lib.Thermistor_readValue.restype = ctypes.c_int
	lib.Thermistor_test.restype      = ctypes.c_int 
	

	self.obj = lib.Thermistor_newInstance(self.__name, self.__adcChannelNo)
	self.initPins()

    def getInstance(self):
        try:
            return self.__instance
        except AttributeError:
            self.obj = lib.Thermistor_newInstance(self.__name, self.__adcChannelNo)
	    selt.__instance = self.obj
	    self.initPins()
            return self.__instance

    def initPins(self):
        lib.Thermistor_initPins(self.obj)

    def readValue(self):
        return lib.Thermistor_readValue(self.obj) 

    def getName(self):
        return self.__name

    def test(self):
        print lib.Thermistor_test()

    


thermistor = Thermistor()
#thermistor.initPins()
print thermistor.readValue()

