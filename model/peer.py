#!/usr/bin/env python

#Peer model for wifi direct communtication management
#Author: Kevin Murphy
#Date  : 6 - Jan - 15

import constants as CONSTS
import socket

class Peer(object):

	__paired = False
	__lock = None 

	def __init__(self, deviceID, ipAddress, timeStamp):
		self.__ipAddrees = ipAddress
		self.__deviceID  = deviceID
		self.__timeStamp = timeStamp

	def getIPAddress(self):
		return self.__ipAddrees

	def getDeviceID(self):
		return self.__deviceID

	def getTimeStamp(self):
		return self.__timeStamp

	def sendPacket(self, packet):
		tmpSocket = self.createSocket(bindToIP=None, connectToIP=self.getIPAddress())
		tmpSocket.send(packet)
		tmpSocket.close()

	def toString(self):
		print {CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_IP_ADDRESS : self.getIPAddress(),
	 		   CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_DEVICE_ID  : self.getDeviceID(),
	 		   CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_TIMESTAMP  : self.getTimeStamp()}

	def createSocket(self, bindToIP, connectToIP):
		newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		if bindToIP is not None:
			#For receiving 
			newSocket.bind((bindToIP, CONSTS.DEFAULT_PORT))
			newSocket.listen(5)
		elif connectToIP is not None:
			#For sending
			newSocket.connect((connectToIP, CONSTS.DEFAULT_PORT))

		return newSocket