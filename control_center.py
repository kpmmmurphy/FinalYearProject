#!/usr/bin/env piython

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

from ctypes import cdll

LIB_PATH = "./sensors/libs/lib_SensorManager.so"

lib = cdll.LoadLibrary(LIB_PATH);

class Sensor(object):
    #Singleton Pattern
    __metaclass__ = SensorMeta

    _name = None
    _instance = None

    def getInstance(self):
        raise NotImplementedError('Subclass must override Constructor');

    def getName():
        raise NotImplementedError('Subclass must override getName')

    def readValue():
        raise NotImplementedError('Subclass must override readValue')

    def initPins():
        raise NotImplementedError('Subclass must override initPins');
            
class Thermistor(Sensor):
    _name = "Thermistor"
    _adcChannelNo = "0"
    _this = None

    def __init__(self):
        #if _instance is None:
	#    _instance = lib.Thermistor_new(_name, _adcChannelNo)
        #return _instance
        self.obj = lib.Thermistor_new(_name, _adcChannel)
        _this = self.obj
        
        #Setup return types for ctypes
        lib.Thermistor_initPins.restype  = None
	lib.Thermistor_readValue.restype = ctypes.c_int
	lib.Thermistor_test.restype      = ctypes.c_int 

    def initPins(_this):
        lib.Thermistor_initPiins(_this)

    def readValue(_this):
        lib.Thermistor_readValue(_this) 

    def getName(_this)
        return _name

    def test(_this):
        print lib.Thermistor_test(_this)

    

def main():
    thermistor = Thermistor() 
    print "Thermitor Test: \n"
    print thermistor.test()

