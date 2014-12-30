#!/usr/bin/env python

#Author : Kevin Murphy
#Date   : 29 - Dec - 14
#
#Configures all configurable classes

import json
import constants as CONSTS
from configurable import Configurable

class ConfigurationManager(Configurable):
	DEBUG  = True
	LOGTAG = "ConfigurationManager"

	__configurables = {}

	def __init__(self, configurables):
		super(ConfigurationManager, self).__init__(CONSTS.JSON_KEY_CONFIG_MANAGER_CONFIG)
		
		if self.DEBUG:
			print self.LOGTAG, " :: Created"

		if configurables is not None:
			self.setConfigurables(configurables)

	def configure(self, config):
		if self.DEBUG:
			print self.LOGTAG, " :: Updating Configuration"

	def reconfigure(self, config):
		if self.DEBUG:
			print self.LOGTAG, " :: Reconfiguring System"

		for item in self.getConfigurables():
			item.configure(json.loads(config))

	def writeoutConfiguration(self):
		config = {}
		for item in self.getConfigurables():
			config[item.getJsonConfigKey()] = item.toString()
			if item.getJsonConfigKey() == CONSTS.JSON_KEY_SENSOR_MANAGER_CONFIG:
				config[CONSTS.JSON_KEY_SENSORS_ARRAY] = item.sensorsToString()

		obj = open(CONSTS.DIR_CONFIG + "config.json", 'wb')
		obj.write(json.dumps(config))
		obj.close()

		return config

	def setConfigurables(self, configurables):
		self.__configurables = configurables

	def getConfigurables(self):
		return self.__configurables

	def toString(self):
		return ""