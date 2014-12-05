#!/usr/bin/env python

#Sensor Superclass 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

class Sensor(object):

    #Constants:
    DEFAULT_PROBE_RATE = 10
    DEFAULT_PRIORITY   = 1

    #Private: 
    __isActive = True
    __probeRate = DEFAULT_PROBE_RATE
    __priority  = DEFAULT_PRIORITY

    def __init__(self):
        raise NotImplementedError('Subclass must override Constructor')

    def initPins(self):
        raise NotImplementedError('Subclass must override initPins')

    def readValue(self):
        raise NotImplementedError('Subclass must override readValue')

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