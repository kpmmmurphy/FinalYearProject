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

		adds = netifaces.ifaddresses('wlan0')
		self.__ipAddress = adds[netifaces.AF_INET][0]['addr']

		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.__socket.bind((self.__ipAddress, self.MCAST_PORT))
		self.__socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		self.test()

		if self.DEBUG:
            print self.LOGTAG, " :: Created"

    def sendSensorValues(self):
    	self.sendData(sensorManager.getSensorValues())
    	timer = Timer(self.getSensorValueSendRate(), self.sendSensorValues,())
        timer.start()

    def test(self):
    	self.sendData("This is a Test")
    	timer = Timer(self.__testRate, self.test,())
        timer.start()

    def sendData(self, data):
    	self.__socket.sendto(data, (self.MCAST_GRP, self.MCAST_PORT))

    def getSensorValueSendRate(self):
    	return self.__sensorValueSendRate

    def setSensorValueSendRate(self, newRate):
    	self.__sensorValueSendRate = newRate

    def configure(self, config):
    	pass

    def toString(self):
    	pass

