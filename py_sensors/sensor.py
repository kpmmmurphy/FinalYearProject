#!/usr/bin/env python

#Sensor Superclass 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

import json

class Sensor(object):

    #Constants:
    DEBUG = True
    DEFAULT_PROBE_RATE = 10
    DEFAULT_PRIORITY   = 1

    #JSON Keys
    NAME       = "name"
    PRIORITY   = "priority"
    PROBE_RATE = "probe_rate"
    IS_ACTIVE  = "is_active"

    #Private: 
    __isActive  = True
    __probeRate = DEFAULT_PROBE_RATE
    __priority  = DEFAULT_PRIORITY
    __currentValue = -1

    def __init__(self):
        raise NotImplementedError('Subclass must override Constructor')

    def initPins(self):
        raise NotImplementedError('Subclass must override initPins')

    def readValue(self):
        raise NotImplementedError('Subclass must override readValue')

    def setCurrentValue(self, newValue):
        self.__currentValue = newValue

    def getCurrentValue(self):
        return self.__currentValue

    def getName(self):
        raise NotImplementedError('Subclass must override getName')

    def setPriority(self, priority):
        self.__priority = priority

    def getPriority(self):
        return self.__priority

    def isActive(self):
        return self.__isActive

    def setActiveStatus(self, isActive):
        self.__isActive = isActive

    def setProbeRate(self, probeRate):
        self.__probeRate = probeRate

    def getProbeRate(self):
    	return self.__probeRate

    def configure(self, config):
        if config is None:
            config = self.toString()

        if self.DEBUG:
            print "Current Config :: " , config

        jsonConfig = json.loads(config)

        self.setActiveStatus(jsonConfig[self.IS_ACTIVE])
        self.setProbeRate(jsonConfig[self.PROBE_RATE])
        self.setPriority(jsonConfig[self.PRIORITY])

    def toString(self):
        data = { self.NAME : self.getName(), self.IS_ACTIVE : self.isActive(), self.PRIORITY : self.getPriority(), self.PROBE_RATE : self.getProbeRate()}
        data_string = json.dumps(data)
        
        if self.DEBUG:
            print self.getName() , data_string

        return data_string    
