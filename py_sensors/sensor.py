#!/usr/bin/env python

#Sensor Superclass 
#Author: Kevin Murphy
#Date  : 24 - Nov - 14

class Sensor(object):

    def __init__(self):
        raise NotImplementedError('Subclass must override Constructor')

    def initPins(self):
        raise NotImplementedError('Subclass must override initPins')

    def readValue(self):
        raise NotImplementedError('Subclass must override readValue')

    def getName(self):
        raise NotImplementedError('Subclass must override getName')