#!/usr/bin/env python

#WifiDirect Manager
#Author: Kevin Murphy
#Date  : 6 - Jan - 15

import json
import socket
import time
from threading import Timer
import netifaces
from configurable import Configurable
import constants as CONSTS

class WifiDirectManager(Configurable):
	DEBUG  = True
	LOGTAG = "WifiDirectManager"

	MCAST_GRP  = CONSTS.MULTICAST_GRP
	MCAST_PORT = CONSTS.MULTICAST_PORT

	__sensorManager = None

	__socket = None
	__sensorValueSendRate = CONSTS.WIFI_DIRECT_SENSOR_VALUE_SEND_RATE
	__testRate = 10

	def __init__(self, sensorManager):
		super(WifiDirectManager, self).__init__(CONSTS.JSON_KEY_WIFI_DIRECT_MANAGER)

		self.__sensorManager = sensorManager
		self.setupMulticastSocket()

		if self.__socket is not None:
			self.sendSensorValues()

		if self.DEBUG:
			print self.LOGTAG, " :: Created"

	def setupMulticastSocket(self):
		try:
			adds = netifaces.ifaddresses('wlan0')
			self.__ipAddress = adds[netifaces.AF_INET][0]['addr']
			self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			self.__socket.bind((self.__ipAddress, self.MCAST_PORT))
			self.__socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		except KeyError:
			if self.DEBUG:
				print self.LOGTAG, "Cannot detect Wlan0 IP Address" 

	def sendSensorValues(self):
		if self.__sensorManager is not None:
			self.sendData(self.__sensorManager.getSensorValues())
		timer = Timer(self.getSensorValueSendRate(), self.sendSensorValues,())
		timer.start()

	def test(self):
		self.sendData("This is a Test")
		timer = Timer(self.__testRate, self.test,())
		timer.start()

	def sendData(self, data):
		if self.__socket is not None:
			if self.DEBUG:
				print self.LOGTAG, " :: Multicasting Data -> ", data
			self.__socket.sendto(json.dumps(data), (self.MCAST_GRP, self.MCAST_PORT))

	def getSensorValueSendRate(self):
		return self.__sensorValueSendRate

	def setSensorValueSendRate(self, newRate):
		self.__sensorValueSendRate = newRate

	def configure(self, config):
		if self.DEBUG:
			print self.LOGTAG, ":: Configuring"

		if config is not None:
			try:
				wifiDirectConfig = config[self.getJsonConfigKey()]
				self.setSensorValueSendRate(wifiDirectConfig[CONSTS.JSON_KEY_WIFI_DIRECT_SENSOR_SEND_RATE])
			except KeyError:
				if self.DEBUG:
					print self.LOGTAG, " :: Config key not present"

	def toString(self):
		data = { CONSTS.JSON_KEY_WIFI_DIRECT_SENSOR_SEND_RATE : self.getSensorValueSendRate()}
 		
 		if self.DEBUG:
 			print self.LOGTAG , json.dumps(data)

 		return data