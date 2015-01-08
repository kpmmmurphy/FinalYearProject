#!/usr/bin/env python

#Peer model for wifi direct communtication management
#Author: Kevin Murphy
#Date  : 6 - Jan - 15

import constants as CONSTS

class Peer(object):

	def __init__(self, deviceID,ipAddress):
		self.__ipAddrees = ipAddress
		self.__deviceID  = deviceID

	def getIPAddress(self):
		return self.__ipAddrees

	def getDeviceID(self):
		return self.__deviceID

	def toString(self):
		print {CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_IP_ADDRESS : self.__ipAddrees,
	 		   CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_DEVICE_ID  : self.__deviceID}