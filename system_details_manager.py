#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 5 - Dec - 15

import json
from configurable import Configurable
import constants as CONSTS

class SystemDetailsManager(Configurable):
	DEBUG  = True
	LOGTAG = "SystemDetailsManager"

	__databaseManager = None	
	__name       = None
	__location   = None
	__gps_lat    = None
	__gps_lng    = None

	def __init__(self, databaseManager):
		super(SystemDetailsManager, self).__init__(CONSTS.JSON_KEY_SYSTEM_DETAILS_MANAGER_CONFIG)

		if self.DEBUG:
			print self.LOGTAG, " :: Created"
		self.__databaseManager = databaseManager

		self.setSystemDetails(self.__databaseManager.select_system_details())

	def configure(self, config):
		if self.DEBUG:
			print self.LOGTAG, ":: Configuring"

		if config is not None:
			try:
				sysDetailsConfig = config[self.getJsonConfigKey()]
				self.setName(sysDetailsConfig[CONSTS.JSON_KEY_SYSTEM_DETAILS_NAME])
				self.setLocation(sysDetailsConfig[CONSTS.JSON_KEY_SYSTEM_DETAILS_LOCATION])
				self.setGPSLat(sysDetailsConfig[CONSTS.JSON_KEY_SYSTEM_DETAILS_GPS_LAT])
				self.setGPSLng(sysDetailsConfig[CONSTS.JSON_KEY_SYSTEM_DETAILS_GPS_LNG])
				self.__databaseManager.insert_system_details(**self.getDetails())
			except KeyError:
				if self.DEBUG:
					print self.LOGTAG, " :: Config not present"

	def getDetails(self):
		return { CONSTS.JSON_KEY_SYSTEM_DETAILS_NAME     : self.getName(),
    	         CONSTS.JSON_KEY_SYSTEM_DETAILS_LOCATION : self.getLocation(),
    	         CONSTS.JSON_KEY_SYSTEM_DETAILS_GPS_LAT  : self.getGPSLat(),
    			 CONSTS.JSON_KEY_SYSTEM_DETAILS_GPS_LNG  : self.getGPSLng()}

	def setSystemDetails(self, systemDetails):
		self.setName(systemDetails.name)
		self.setLocation(systemDetails.location)
		self.setGPSLat(systemDetails.gps_lat)
		self.setGPSLng(systemDetails.gps_lng)

	def setName(self, name):
		self.__name = name

	def getName(self):
		return self.__name

	def setLocation(self, location):
		self.__location = location

	def getLocation(self):
		return self.__location

	def setIpAddress(self, ip_address):
		self.__ip_address = ip_address

	def getIpAddress(self):
		return self.__ip_address

	def setGPSLat(self, gps_lat):
		self.__gps_lat = gps_lat

	def getGPSLat(self):
		return self.__gps_lat

	def setGPSLng(self, gps_lng):
		self.__gps_lng = gps_lng

	def getGPSLng(self):
		return self.__gps_lng

	def toString(self):
		if self.DEBUG:
			print self.LOGTAG , json.dumps(self.getDetails())
		return self.getDetails()    