#!/usr/bin/env python

#Peripheral
#Author: Kevin Murphy
#Date  : 28 - Feb - 15

import peer as Peer

class Peripheral(Peer):
	LOGTAG = "Peripheral"
	DEBUG  = True

	__currentReadings = None

	def getSensorReadings(self):
		return self.__currentReadings

	def setSensorReadings(self, readings):
		self.__currentReadings = readings
