#!/usr/bin/env python

#Sensor Superclass 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

import json
import constants as CONSTS
from configurable import Configurable

class Sensor(Configurable):

    #Constants:
    DEBUG = False

    #Private: 
    __isActive  = True
    __probeRate = CONSTS.PROBE_RATE_DEFAULT
    __priority  = CONSTS.PRIORITY_DEFAULT
    __currentValue = -1
    __alertThreshold = None

    def __init__(self):
        raise NotImplementedError('Subclass must override Constructor')

    def initPins(self):
        raise NotImplementedError('Subclass must override initPins')

    def readValue(self):
        raise NotImplementedError('Subclass must override readValue')

    def react(self, value):
        raise NotImplementedError('Subclass must override react')

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

    def getAlertThreshold(self):
        return self.__alertThreshold

    def setAlertThreshold(self, newThreshold):
        self.__alertThreshold = newThreshold

    def configure(self, config):
        if config is None:
            config = self.toString()

        self.setActiveStatus(config[CONSTS.JSON_KEY_SENSOR_IS_ACTIVE])
        self.setProbeRate(config[CONSTS.JSON_KEY_SENSOR_PROBE_RATE])
        self.setPriority(config[CONSTS.JSON_KEY_SENSOR_PRIORITY])
        self.setAlertThreshold(config[CONSTS.JSON_KEY_SENSOR_ALERT_THRESHOLD])

        if self.DEBUG:
            print "New Config :: " , self.toString()

    def toString(self):
        data = { CONSTS.JSON_KEY_SENSOR_NAME : self.getName(), 
                 CONSTS.JSON_KEY_SENSOR_IS_ACTIVE : self.isActive(), 
                 CONSTS.JSON_KEY_SENSOR_PRIORITY : self.getPriority(), 
                 CONSTS.JSON_KEY_SENSOR_PROBE_RATE : self.getProbeRate(),
                 CONSTS.JSON_KEY_SENSOR_ALERT_THRESHOLD : self.getAlertThreshold()}
        
        if self.DEBUG:
            print self.getName() , json.dumps(data)

        return data    
