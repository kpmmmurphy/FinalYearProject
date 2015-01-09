#!/usr/bin/env python

#Peer model for wifi direct communtication management
#Author: Kevin Murphy
#Date  : 6 - Jan - 15

import constants as CONSTS

class Peer(object):

	def __init__(self, deviceID, ipAddress, timeStamp, socket):
		self.__ipAddrees = ipAddress
		self.__deviceID  = deviceID
		self.__timeStamp = timeStamp
		self.__socket    = socket

	def getIPAddress(self):
		return self.__ipAddrees

	def getDeviceID(self):
		return self.__deviceID

	def getTimeStamp(self):
		return self.__timeStamp

	def getSocket(self):
		return self.__socket

	def toString(self):
		print {CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_IP_ADDRESS : self.getIPAddress(),
	 		   CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_DEVICE_ID  : self.getDeviceID(),
	 		   CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_TIMESTAMP  : self.getTimeStamp()}