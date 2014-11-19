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
    def getInstance():
        if _instance is None:
	    _instance = lib.Thermistor_new(_name, _adcChannelNo0)

            print('{a} {b}', getName(), "New Instance")

    def getName(self)
        return lib.Thermistor_getName(self.obj);

def main():
    SensorManager.


