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
	__configManager = None

	__currentPeers = {}

	__multicastSocket = None
	__ipAddress = None
	__sensorValueSendRate = CONSTS.WIFI_DIRECT_SENSOR_VALUE_SEND_RATE
	__configSendRate      = CONSTS.WIFI_DIRECT_CONFIG_SEND_RATE
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

		#sendConfigThread = threading.Thread(target=self.sendConfig, args=())
		#sendConfigThread.start()

		peerPacketThread = threading.Thread(target=self.listenForPeerPacket, args=())
		peerPacketThread.start()

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
		#Socket must be connected to the wlan0 interface's IP address
		#Bind to our default Multicast Port.
		multicastSocket.bind((multicastGroup, multicastPort))
		multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicastGroup)+socket.inet_aton(inetIP))
		multicastSocket.setblocking(True)	
		return multicastSocket

	def listenOnMulticastSocket(self, multicastSocket):
		if multicastSocket is not None:
			while True:
				if self.DEBUG:
					print self.LOGTAG, " :: Waiting to Recveive Packet..."

				rawPacket = multicastSocket.recv(1024)
				packet    = json.loads(rawPacket)

				if self.DEBUG:
					print self.LOGTAG, " :: Received Packet ->", json.dumps(packet)

				try:
					service = packet[CONSTS.JSON_KEY_WIFI_DIRECT_SERVICE]
					payload = packet[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD]
					if service == CONSTS.JSON_VALUE_WIFI_DIRECT_CONNECT:
						self.addPeer(payload)
				except KeyError:
					if self.DEBUG:
						print self.LOGTAG, " :: Exception thrown -> KeyError"

	def createSocket(self, bindToIP, connectToIP):
		newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		newSocket.setblocking(True)

		if bindToIP is not None:
			#For receiving 
			newSocket.bind((bindToIP, CONSTS.DEFAULT_SERVER_PORT))
			newSocket.listen(5)
		elif connectToIP is not None:
			#For sending
			#newSocket.bind((self.__ipAddress, CONSTS.DEFAULT_PORT))
			newSocket.connect((connectToIP, CONSTS.DEFAULT_PORT))

		return newSocket

	def sendSensorValues(self):
		if self.__sensorManager is not None:
			sensorValues = self.__sensorManager.getSensorValues()
			packet = {}
			payload = {}
			packet[CONSTS.JSON_KEY_WIFI_DIRECT_SERVICE] = CONSTS.JSON_VALUE_WIFI_DIRECT_CURRENT_SENSOR_VALUES 
			payload[CONSTS.JSON_VALUE_WIFI_DIRECT_CURRENT_SENSOR_VALUES] = sensorValues;
			packet[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD] = payload

			for deviceID, peer in self.__currentPeers.iteritems():
				if self.DEBUG:
					print self.LOGTAG, " :: Sending Sensor values to DeviceID -> ", deviceID 
				peer.sendPacket(json.dumps(packet))

		timer = threading.Timer(self.getSensorValueSendRate(), self.sendSensorValues,())
		timer.start()

	def sendConfig(self):
		if self.__configManager is not None:
			config = self.getConfigManager().getConfig()
			packet = self.createPacket(service=CONSTS.JSON_VALUE_WIFI_DIRECT_CONFIG, payload=config)

			for deviceID, peer in self.__currentPeers.iteritems():
				if self.DEBUG:
					print self.LOGTAG, " :: Sending Config to DeviceID ->", deviceID 
				peer.sendPacket(json.dumps(packet))

		timer = threading.Timer(self.getConfigSendRate(), self.sendConfig,())
		timer.start()

	def listenForPeerPacket(self):
		peerSocket  = self.createSocket(self.__ipAddress, None)
		conn, addr = peerSocket.accept()
		while True:
			rawPacket = conn.recv(10240)
			packet    = json.loads(rawPacket)

			if self.DEBUG:
				print self.LOGTAG, " Packet Recieved -> ", rawPacket

			service = packet[CONSTS.JSON_KEY_WIFI_DIRECT_SERVICE]
			payload = packet[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD]
			if service == CONSTS.JSON_VALUE_WIFI_DIRECT_CONFIG:
				if self.DEBUG:
					print self.LOGTAG, " :: Config from Peer"
					self.getConfigManager().reconfigure(json.dumps(payload[CONSTS.JSON_VALUE_WIFI_DIRECT_CONFIG]))

	def addPeer(self, payload):
		try:
			session      = payload[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_SESSION]
			peerIP       = session[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_IP_ADDRESS]
			peerDeviceID = session[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_DEVICE_ID]
			timeStamp    = session[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_TIMESTAMP]

			peer = Peer(ipAddress=peerIP, deviceID=peerDeviceID, timeStamp=timeStamp)

			if self.DEBUG:
				print self.LOGTAG, " :: Added new Peer -> ", peer.toString()

			self.__currentPeers[peerDeviceID] = peer

			#Send the response ACK
			responsePacket = {}
			payload        = {}
			responsePacket[CONSTS.JSON_KEY_WIFI_DIRECT_SERVICE] = CONSTS.JSON_VALUE_WIFI_DIRECT_PAIRED
			payload[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_STATUS_CODE] = CONSTS.JSON_VALUE_WIFI_DIRECT_STATUS_CODE_SUCCESS
			responsePacket[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD] = payload
			if self.DEBUG:
				print self.LOGTAG, " :: Sending Response -> ", responsePacket

			peer.sendPacket(json.dumps(responsePacket))

			#Send Peer Current Sys Config
			config = self.getConfigManager().getConfig()
			packet = self.createPacket(service=CONSTS.JSON_VALUE_WIFI_DIRECT_CONFIG, payload=config)
			peer.sendPacket(json.dumps(packet))
			
			if self.DEBUG:
				print self.LOGTAG, " :: Current Peers -> ", self.printPeers()

		except KeyError:
			if self.DEBUG:
				print self.LOGTAG, " :: Exception thrown -> KeyError"

	def printPeers(self):
		for deviceID, peer in self.__currentPeers.iteritems():
			peer.toString()

	def createPacket(self, service, payload):
		_packet  = {}
		_payload = {}

		_packet[CONSTS.JSON_KEY_WIFI_DIRECT_SERVICE]   = service 
		_payload[service] = payload
		_packet[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD]   = _payload
		return _packet

	def getSensorValueSendRate(self):
		return self.__sensorValueSendRate

	def setSensorValueSendRate(self, newRate):
		self.__sensorValueSendRate = newRate

	def getConfigSendRate(self):
		return self.__configSendRate 

	def getConfigManager(self):
		return self.__configManager

	def setConfigManager(self, configManager):
		self.__configManager = configManager 

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