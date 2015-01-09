#!/usr/bin/env python

#WifiDirect Manager
#Author: Kevin Murphy
#Date  : 6 - Jan - 15

import json
import socket
import time
import struct
import threading 
import netifaces
from model.peer import Peer
from configurable import Configurable
import constants as CONSTS

class WifiDirectManager(Configurable):
	DEBUG  = True
	LOGTAG = "WifiDirectManager"

	MCAST_GRP  = CONSTS.MULTICAST_GRP
	MCAST_PORT = CONSTS.MULTICAST_PORT

	__sensorManager = None

	__currentPeers = {}

	__multicastSocket = None
	__sensorValueSendRate = CONSTS.WIFI_DIRECT_SENSOR_VALUE_SEND_RATE
	__testRate = 10

	def __init__(self, sensorManager):
		super(WifiDirectManager, self).__init__(CONSTS.JSON_KEY_WIFI_DIRECT_MANAGER)

		if self.DEBUG:
			print self.LOGTAG, " :: Created"

		self.__sensorManager = sensorManager
		self.getIPAddress()

		self.__multicastSocket = self.createMulticatSocket(self.__ipAddress, CONSTS.MULTICAST_GRP, CONSTS.MULTICAST_PORT)
		multicastThread        = threading.Thread(target=self.listenOnMulticastSocket,args=(self.__multicastSocket,))
		multicastThread.start()

		sendSensorValuesThread = threading.Thread(target=self.sendSensorValues, args=())
		sendSensorValuesThread.start()

		#self.setupSendMulticastSocket()

		#if self.__multicastSocket is not None:
		#	self.sendSensorValues()

	def getIPAddress(self):
		try:
			adds = netifaces.ifaddresses('wlan0')
			self.__ipAddress = adds[netifaces.AF_INET][0]['addr']
			if self.DEBUG:
				print self.LOGTAG, " :: IP Address ->", self.__ipAddress
		except KeyError:
			if self.DEBUG:
				print self.LOGTAG, "Cannot detect Wlan0 IP Address" 

	def createMulticatSocket(self, inetIP, multicastGroup, multicastPort):
		multicastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		multicastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#self.__multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		#mreq = struct.pack("4sL", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)
		#self.__multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

		#Socket must be connected to the wlan0 interface's IP address
		multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicastGroup)+socket.inet_aton(inetIP))
		#Bind to our default Multicast Port.
		multicastSocket.bind((multicastGroup, multicastPort))
		return multicastSocket

	def listenOnMulticastSocket(self, multicastSocket):
		if multicastSocket is not None:
			while True:
				if self.DEBUG:
					print self.LOGTAG, " :: Waiting to Recveive Packet..."

				rawPacket = multicastSocket.recv(10240)
				packet    = json.loads(rawPacket)

				#packet = json.loads('{"payload":{"DEBUG":true,"device_id":"e1cadbafc6804e3f","ip_address":"192.168.42.2","connected":false},"service":"connect"}')
				
				if self.DEBUG:
					time.sleep(2)
					print self.LOGTAG, " :: Received Packet ->", json.dumps(packet)

				try:
					service = packet[CONSTS.JSON_KEY_WIFI_DIRECT_REQUEST_SERVICE]
					payload = packet[CONSTS.JSON_KEY_WIFI_DIRECT_REQUEST_PAYLOAD]
					if service == CONSTS.JSON_VALUE_WIFI_DIRECT_CONNECT:
						self.addPeer(payload)
				except KeyError:
					if self.DEBUG:
						print self.LOGTAG, " :: Exception thrown -> KeyError"

	def createSocket(self, bindToIP, connectToIP):
		#newSocket = socket.socket(self.__ipAddress, socket.SOCK_STREAM)
		newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		if bindToIP is not None:
			#For receiving 
			newSocket.bind((bindToIP, CONSTS.DEFAULT_PORT))
			newSocket.listen(5)
		elif connectToIP is not None:
			#For sending
			newSocket.bind((self.__ipAddress, CONSTS.DEFAULT_PORT))
			newSocket.connect((connectToIP, CONSTS.DEFAULT_PORT))

		return newSocket

	def sendSensorValues(self):
		if self.__sensorManager is not None:
			sensorValues = self.__sensorManager.getSensorValues()

			if self.DEBUG:
				print self.LOGTAG, " :: Sending Sensor Values"

			for deviceID, peer in self.__currentPeers.iteritems():
				if self.DEBUG:
					print self.LOGTAG, " :: Sending to DeviceID", deviceID 
				peer.getSocket().send(sensorValues)

		timer = threading.Timer(self.getSensorValueSendRate(), self.sendSensorValues,())
		timer.start()

	def test(self):
		self.sendData("This is a Test")
		timer = Timer(self.__testRate, self.test,())
		timer.start()

	def sendData(self, socket, data):
		if socket is not None:
			if self.DEBUG:
				print self.LOGTAG, " :: Multicasting Data -> ", data
			self.socket.sendto(json.dumps(data), (self.MCAST_GRP, self.MCAST_PORT))

	def addPeer(self, payload):
		try:
			peerIP       = payload[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_IP_ADDRESS]
			peerDeviceID = payload[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_DEVICE_ID]
			timeStamp    = payload[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_TIMESTAMP]
			peerSocket   = self.createSocket(bindToIP=None, connectToIP=peerIP)       

			peer = Peer(ipAddress=peerIP, deviceID=peerDeviceID, timeStamp=timeStamp, socket=peerSocket)

			if self.DEBUG:
				print self.LOGTAG, " :: Added new Peer -> ", peer.toString()

			self.__currentPeers[peerDeviceID] = peer
			
			if self.DEBUG:
				print self.LOGTAG, " :: Current Peers -> ", self.printPeers()

		except KeyError:
			if self.DEBUG:
				print self.LOGTAG, " :: Exception thrown -> KeyError"

	def printPeers(self):
		for deviceID, peer in self.__currentPeers.iteritems():
			peer.toString()

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

