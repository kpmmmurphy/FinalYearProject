#!/usr/bin/env python

#Author : Kevin Murphy
#Date   : 16 - Dec - 14
#
#API class handling all http requests

import requests
from threading import Timer
from configurable import Configurable
import constants as CONSTS

from sensor_factory   import SensorFactory
from sensor_manager   import SensorManager

class APIManager(Configurable):
    DEBUG  = True
    LOGTAG = "APIManager"

    __sensorManager = None

    #Configurables
    __systemConfigRequestRate = CONSTS.REQUEST_RATE_SYSTEM_CONFIG
    __sensorValueUploadRate   = CONSTS.REQUEST_RATE_UPLOAD_SENSOR_VALUES
    __cameraImageUploadRate   = CONSTS.REQUEST_RATE_UPLOAD_CAMERA_IMAGE

    def __init__(self, sensorManager):
        if self.DEBUG:
            print self.LOGTAG, " :: Created"

        if sensorManager is not None:
            self.__sensorManager = sensorManager

    def configure(self, config):
    	if self.DEBUG:
    	    print self.LOGTAG, ":: Configuring"
        
        if config is not None:
            apiConfig = config[CONSTS.JSON_KEY_API_CONFIG_OBJ]
            self.setSensorValueUploadRate(apiConfig[CONSTS.JSON_KEY_API_SENSOR_VALUE_UPLOAD_RATE])
            self.setSystemConfigRequestRate(apiConfig[CONSTS.JSON_KEY_API_SYSTEM_CONFIG_REQUEST_RATE])
            self.setCameraImageUploadRate(apiConfig[CONSTS.JSON_KEY_API_CAMERA_IMAGE_UPLOAD_RATE])

    #---------API CALLS-----------------------------
    def getSystemConfig(self):
    	if self.DEBUG:
    		print self.LOGTAG, " :: Requesting System Configuration"

        configResponse = requests.post(CONSTS.API_URL_CS1 + CONSTS.API_URL_MANAGER, data=CONSTS.REQUEST_PAYLOAD_CONFIG_GET)	
        
        if self.DEBUG:
            print self.LOGTAG, " :: New Config -> ", configResponse.content

        return configResponse.content

    def uploadSensorValues(self):
        if self.DEBUG:
            print self.LOGTAG, " :: Sending Sensor Values"

        payload = CONSTS.REQUEST_PAYLOAD_UPLOAD_SENSOR_VALUES
        payload[CONSTS.JSON_KEY_REQUEST_SENSOR_VALUES] = self.__sensorManager.getSensorValues()
        
        if self.DEBUG: 
            print self.LOGTAG, " :: Uploading -> " , payload

        sendResponse = requests.post(CONSTS.API_URL_CS1 + CONSTS.API_URL_MANAGER, data=payload)
        
        if sendResponse.status_code == requests.codes.ok:
            print self.LOGTAG, " :: Uploading Sensor Values Completed Successfully"
        else:
            print self.LOGTAG, " :: ERROR:Uploading Sensor Values Failed -> status_code:", sendResponse.status_code

    def uploadImage(self):
        if self.DEBUG:
            print self.LOGTAG, " :: Uploading Camera Image"

        payload = CONSTS.REQUEST_PAYLOAD_UPLOAD_CAMERA_IMAGE
        #Should select latest image dynamically 
        camera_image   = {CONSTS.JSON_KEY_REQUEST_FILE : open(CONSTS.DIR_CAMERA + "img.png", 'rb')}
        
        imageUploadResponse = requests.post(CONSTS.API_URL_CS1 + CONSTS.API_URL_MANAGER, data=payload, files=camera_image)
        
        if imageUploadResponse.status_code == requests.codes.ok:
            print self.LOGTAG, " :: Uploading Image Completed Successfully"
        else:
            print self.LOGTAG, " :: ERROR:Uploading Image Failed -> status_code:", sendResponse.status_code

    def test(self):
    	cs1_test = requests.get("http://cs1.ucc.ie/~kpm2/fyp/api/test.txt")	
    	print cs1_test.content

    #-------Polling Calls---------------------------
    def startPolling_SysConfig(self):
        timer = Timer(self.getSystemConfigRequestRate(), self.getSystemConfig,())
        timer.start()

    def startPolling_UploadSensorValues(self):
        timer = Timer(self.getSensorValueUploadRate(), self.uploadSensorValues,())
        timer.start()

    def startPolling_UploadCameraStill(self):
        timer = Timer(self.getCameraImageUploadRate(), self.uploadImage,())
        timer.start()

    #------Getters and Setters-------------------------
    def getSensorValueUploadRate(self):
        return self.__sensorValueUploadRate

    def setSensorValueUploadRate(self, newRate):
        self.getSensorValueUploadRate() = newRate

    def getSystemConfigRequestRate(self):
        return self.__systemConfigRequestRate

    def setSystemConfigRequestRate(self, newRate):
        self.getSystemConfigRequestRate() = newRate

    def getCameraImageUploadRate(self):
        return self.__cameraImageUploadRate

    def setCameraImageUploadRate(self, newRate):
        self.getCameraImageUploadRate() = newRate

sensorFactory   = SensorFactory()
sensorManager   = SensorManager(sensorFactory.getSensors(), None) 
apiManager = APIManager(sensorManager=sensorManager)
#apiManager.getSystemConfig()
apiManager.uploadSensorValues()


