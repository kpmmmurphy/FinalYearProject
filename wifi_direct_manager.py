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
import subprocess
from model.peer import Peer
from configurable import Configurable
import constants as CONSTS
from camera_manager import CameraManager

class WifiDirectManager(Configurable):
	DEBUG  = True
	LOGTAG = "WifiDirectManager"

	MCAST_GRP  = CONSTS.MULTICAST_GRP
	MCAST_PORT = CONSTS.MULTICAST_PORT

	__sensorManager = None
	__configManager = None
	__databaseManager = None

	__currentPeers = {}

	__multicastSocket = None
	__ipAddress = None
	__sensorValueSendRate = CONSTS.WIFI_DIRECT_SENSOR_VALUE_SEND_RATE
	__configSendRate      = CONSTS.WIFI_DIRECT_CONFIG_SEND_RATE
	__testRate = 10

	def __init__(self, sensorManager, databaseManager):
		super(WifiDirectManager, self).__init__(CONSTS.JSON_KEY_WIFI_DIRECT_MANAGER)

		if self.DEBUG:
			print self.LOGTAG, " :: Created"

		self.__sensorManager   = sensorManager
		self.__databaseManager = databaseManager

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

	def sendPacketToAllPeers(self, packet):
		for deviceID in self.__currentPeers.keys():
			if self.DEBUG:
				print self.LOGTAG, " :: Sending Packet to DeviceID -> ", deviceID 
			self.sendPacketToPeer(self.__currentPeers[deviceID], packet)


	def sendSensorValues(self):
		if self.__sensorManager is not None:
			sensorValues = self.__sensorManager.getSensorValues()
			minMaxValues = self.__databaseManager.select_current_day_max_min_sensor_values()
			payload = {}
			if minMaxValues is not None:
				payload = dict(sensorValues.items() + minMaxValues.items())
			else:
				payload = sensorValues.items()

			self.sendPacketToAllPeers(self.createPacket(service=CONSTS.JSON_VALUE_WIFI_DIRECT_CURRENT_SENSOR_VALUES, payload=payload))

		timer = threading.Timer(self.getSensorValueSendRate(), self.sendSensorValues,())
		timer.start()

	def sendConfig(self):
		if self.__configManager is not None:
			config = self.getConfigManager().getConfig()
			self.sendPacketToAllPeers(self.createPacket(service=CONSTS.JSON_VALUE_WIFI_DIRECT_CONFIG, payload=config))

		timer = threading.Timer(self.getConfigSendRate(), self.sendConfig,())
		timer.start()

	def listenForPeerPacket(self):
		peerSocket  = self.createSocket(self.__ipAddress, None)
		while True:
			conn, addr = peerSocket.accept()
			rawPacket = conn.recv(10240)
			packet    = json.loads(rawPacket)

			service = None
			payload = None

			if self.DEBUG:
				print self.LOGTAG, " Packet Recieved -> ", rawPacket

			try:
				service = packet[CONSTS.JSON_KEY_WIFI_DIRECT_SERVICE]

				try:
					payload  = packet[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD]
				except KeyError:
					if self.DEBUG:
						print self.LOGTAG, " :: KeyError -> No Payload Supplied"

				if payload is not None and service == CONSTS.JSON_VALUE_WIFI_DIRECT_CONFIG:
					if self.DEBUG:
						print self.LOGTAG, " :: Config from Peer"
					self.getConfigManager().reconfigure(json.dumps(payload[CONSTS.JSON_VALUE_WIFI_DIRECT_CONFIG]))
				elif service == CONSTS.JSON_VALUE_WIFI_DIRECT_GET_GRAPH_DATA:
					if self.DEBUG:
						print self.LOGTAG, " :: Peer Requested Graphing Values"
					currentHourVals       = self.__databaseManager.select_current_hour_sensor_values()
					currentDayAggHourVals = self.__databaseManager.select_agg_hour_current_day_sensor_values()
					aggDayVals            = self.__databaseManager.select_agg_day_sensor_values()

					self.sendPacketToAllPeers(self.createPacket(service=CONSTS.JSON_VALUE_WIFI_DIRECT_GRAPH_DATA_CUR_HOUR, payload=currentHourVals))
					self.sendPacketToAllPeers(self.createPacket(service=CONSTS.JSON_VALUE_WIFI_DIRECT_GRAPH_DATA_CUR_DAY_AGG_HOUR, payload=currentDayAggHourVals))
					self.sendPacketToAllPeers(self.createPacket(service=CONSTS.JSON_VALUE_WIFI_DIRECT_GRAPH_DATA_AGG_DAY, payload=aggDayVals))
				elif service == CONSTS.JSON_VALUE_WIFI_DIRECT_REQUEST_STREAM:
					if self.DEBUG:
						print self.LOGTAG, " :: Peer Requested Local Stream"
					CameraManager.startLocalStream()
				elif service == CONSTS.JSON_VALUE_WIFI_DIRECT_REQUEST_IMAGE:
					CameraManager.takeStill()
					
			except KeyError:
				if self.DEBUG:
						print self.LOGTAG, " :: KeyError -> No Service Supplied"

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
			payload = {}
			payload[CONSTS.JSON_KEY_WIFI_DIRECT_PAYLOAD_STATUS_CODE] = CONSTS.JSON_VALUE_WIFI_DIRECT_STATUS_CODE_SUCCESS
			responsePacket = self.createPacket(service=CONSTS.JSON_VALUE_WIFI_DIRECT_PAIRED, payload=payload)

			if self.DEBUG:
				print self.LOGTAG, " :: Sending Response -> ", responsePacket

			self.sendPacketToPeer(peer, responsePacket)

			#Send Peer Current Sys Config
			config = self.getConfigManager().getConfig()
			packet = self.createPacket(service=CONSTS.JSON_VALUE_WIFI_DIRECT_CONFIG, payload=config)

			self.sendPacketToPeer(peer, packet)
			
			if self.DEBUG:
				print self.LOGTAG, " :: Current Peers -> ", self.printPeers()

		except KeyError:
			if self.DEBUG:
				print self.LOGTAG, " :: Exception thrown -> KeyError"

	def printPeers(self):
		for peerID in self.__currentPeers.keys():
			self.__currentPeers[peerID].toString()

	def removePeer(self, peer):
		if self.DEBUG:
			print self.LOGTAG, " :: Removing Peer -> ", peer.getDeviceID()
		del self.__currentPeers[peer.getDeviceID()]

	def sendPacketToPeer(self, peer, packet):
		accepted = peer.sendPacket(packet)
		if not accepted:
			self.removePeer(peer)

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
