#!/usr/bin/env python

#Sensor Superclass 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

import json
import constants as CONSTS
from configurable import Configurable

class Sensor(Configurable):

    #Constants:
    DEBUG = True
    LOGTAG = "Sensor"

    #Private: 
    __alertManager = None
    __isActive  = True
    __probeRate = CONSTS.PROBE_RATE_DEFAULT
    __priority  = CONSTS.PRIORITY_DEFAULT
    __currentValue = -1
    __alertThreshold = None
    __previousValue = None
    __platauCount   = 0

    def __init__(self, alertManager):
        if alertManager is not None:
            self.setAlertManager(alertManager)
        
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

    def setAlertManager(self, alertManager):
        self.__alertManager = alertManager

    def getAlertManager(self):
        return self.__alertManager

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

    def calculateCurrentValue(self, latestValue):
        if self.__previousValue is None:
            self.__previousValue = latestValue

        #Catch: Will CO ever reach 0 if it spikes too hight
        valueDiff = latestValue - self.__previousValue
        calValue = max((self.getCurrentValue()) + (valueDiff), 0)
        if valueDiff < 0: 
            self.__platauCount += 1
            if self.__platauCount == 5:
                calValue = 0
                self.__platauCount = 0

        self.__previousValue = latestValue
        return calValue

    def configure(self, config):
        if config is None:
            config = self.toString()

        try:
            self.setActiveStatus(config[CONSTS.JSON_KEY_SENSOR_IS_ACTIVE])
            self.setProbeRate(config[CONSTS.JSON_KEY_SENSOR_PROBE_RATE])
            self.setPriority(config[CONSTS.JSON_KEY_SENSOR_PRIORITY])
            self.setAlertThreshold(config[CONSTS.JSON_KEY_SENSOR_ALERT_THRESHOLD])
        except KeyError:
                if self.DEBUG:
                    print self.LOGTAG, " :: Config not present"

        if self.DEBUG:
            print self.LOGTAG, " : ", self.getName().upper(), " -> New Config :: " , self.toString()

    def toString(self):
        data = { CONSTS.JSON_KEY_SENSOR_NAME : self.getName(), 
                 CONSTS.JSON_KEY_SENSOR_IS_ACTIVE : self.isActive(), 
                 CONSTS.JSON_KEY_SENSOR_PRIORITY : self.getPriority(), 
                 CONSTS.JSON_KEY_SENSOR_PROBE_RATE : self.getProbeRate(),
                 CONSTS.JSON_KEY_SENSOR_ALERT_THRESHOLD : self.getAlertThreshold()}
        
        if self.DEBUG:
            print self.getName() , json.dumps(data)

        return data    
