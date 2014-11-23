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
	lib.Thermistor_new.argtypes = [ctypes.c_char_p, ctypes.c_int]
	lib.Thermistor_new.restype  = Thermistor
	if self.__instance is None:
	   print "New Instance of Thermistor\n" 
	   self.__instance = lib.Thermistor_new(self.__name, self.__adcChannelNo)

        #Setup return types for ctypes
	lib.Thermistor_initPins.restype  = None
	lib.Thermistor_readValue.restype = ctypes.c_int
	lib.Thermistor_test.restype      = ctypes.c_int 

    def getInstance(self):
        try:
            return self.__instance
        except AttributeError:
            #self._instance = self._decorated()
            return self.__instance

    def initPins(self):
        lib.Thermistor_initPins(_instance)

    def readValue(self):
        lib.Thermistor_readValue(_instance) 

    def getName(self):
        return self.__name

    def test(self):
        print lib.Thermistor_test()

    


thermistor = Thermistor() 
#thermistor.initPins()
#print thermistor.readValue()

