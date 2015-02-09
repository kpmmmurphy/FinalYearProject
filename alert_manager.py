#!/usr/bin/env python

#Alerting Manager handles contact with Buzzer and Camera, eventually LEDS 
#Author: Kevin Murphy
#Date  : 4 - Jan - 15

import json
from configurable import Configurable
import constants as CONSTS
from py_sensors.buzzer import Buzzer
from camera_manager import CameraManager
from pn_manager import PNManager

class AlertManager(Configurable):
    DEBUG  = True
    LOGTAG = "AlertManager"

    __buzzerOn   = True
    __pushOn     = True
    __lockdownOn = False
    __cameraOn   = True
    __videoMode  = False

    def __init__(self):
    	super(AlertManager, self).__init__(CONSTS.JSON_KEY_ALERT_MANAGER_CONFIG)

        if self.DEBUG:
            print self.LOGTAG, " :: Created"

    def configure(self, config):
        if self.DEBUG:
            print self.LOGTAG, ":: Configuring"

        if config is not None:
            try:
                alertConfig = config[self.getJsonConfigKey()]
                self.setBuzzerStatus(alertConfig[CONSTS.JSON_KEY_ALERT_BUZZER_ON])
                self.setCameraStatus(alertConfig[CONSTS.JSON_KEY_ALERT_CAMERA_ON])
                self.setVideoMode(alertConfig[CONSTS.JSON_KEY_ALERT_VIDEO_MODE])
                self.setPushStatus(alertConfig[CONSTS.JSON_KEY_ALERT_PUSH_ON])
                self.setLockdownStatus(alertConfig[CONSTS.JSON_KEY_ALERT_LOCKDOWN_ON])
            except KeyError:
                if self.DEBUG:
                    print self.LOGTAG, " :: Config key not present"

    def ringBuzzer(self):
    	if self.getBuzzerStatus():
    		Buzzer.buzz()

    def activateCamera(self):
    	if self.getCameraStatus():
    		if self.getVideoMode():
    			CameraManager.recordVideo()
    		else:
    			CameraManager.takeStill()

    def sendPush(self, sensor, value):
        if self.getPushStatus():
            if sensor == CONSTS.SENSOR_MOTION and not self.getLockdownStatus():
                #Do nothing when motion is detected
                pass
            else:
                data = {"sensor" : sensor, "value" : value}
                pnManager = PNManager()
                pnManager.sendJsonPush(data)

    def setBuzzerStatus(self, isOn):
    	self.__buzzerOn = isOn

    def getBuzzerStatus(self):
    	return self.__buzzerOn

    def setPushStatus(self, isOn):
        self.__pushOn = isOn

    def getPushStatus(self):
        return self.__pushOn

    def setLockdownStatus(self, isOn):
        self.__lockdownOn = isOn

    def getLockdownStatus(self):
        return self.__lockdownOn

    def setCameraStatus(self, isOn):
    	self.__cameraOn = isOn

    def getCameraStatus(self):
    	return self.__cameraOn

    def setVideoMode(self, isOn):
    	self.__videoMode = isOn

    def getVideoMode(self):
    	return self.__videoMode

    def toString(self):
		data = { CONSTS.JSON_KEY_ALERT_BUZZER_ON  : self.getBuzzerStatus(), 
                 CONSTS.JSON_KEY_ALERT_CAMERA_ON  : self.getCameraStatus(), 
                 CONSTS.JSON_KEY_ALERT_PUSH_ON    : self.getPushStatus(),
                 CONSTS.JSON_KEY_ALERT_LOCKDOWN_ON : self.getLockdownStatus(),
                 CONSTS.JSON_KEY_ALERT_VIDEO_MODE  : self.getVideoMode()}
 		
 		if self.DEBUG:
 			print self.LOGTAG , json.dumps(data)

 		return data