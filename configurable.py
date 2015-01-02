#!/usr/bin/env python   

#A configuration interface, providing one method, configure 
#Author: Kevin Murphy
#Date  : 15 - Dec - 14

from abc import ABCMeta, abstractmethod 
import constants as CONSTS

class Configurable(object):
    __metaclass__ = ABCMeta
    __jsonConfigKey = CONSTS.JSON_KEY_DEFAULT

    def __init__(self, jsonKey):
    	self.setJsonConfigKey(jsonKey)

    @abstractmethod
    def configure(self, config):
        pass

    @abstractmethod
    def toString(self):
    	pass

    def setJsonConfigKey(self, jsonKey):
    	if jsonKey is not None:
    		self.__jsonConfigKey = jsonKey

    def getJsonConfigKey(self):
        return self.__jsonConfigKey



