#!/usr/bin/env python

#Author : Kevin Murphy
#Date   : 16 - Dec - 14
#
#API class handling all http requests

import requests
import json
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
        configResponse = self.sendRequest(CONSTS.JSON_VALUE_REQUEST_SERVICE_GET_CONFIG, payload=None, filez=None)
        return configResponse.content

    def updateSystemConfig(self):
        file = open('config/test_config.json', 'r')
        configResponse = self.sendRequest(CONSTS.JSON_VALUE_REQUEST_SERVICE_UPDATE_CONFIG, payload=file.read(), filez=None)
        return configResponse.content

    def uploadSensorValues(self):
        self.sendRequest(CONSTS.JSON_VALUE_REQUEST_SERVICE_UPLOAD_SENSOR_VALUES, payload=self.__sensorManager.getSensorValues(), filez=None)

    def getLatestSensorValues(self):
        valuesResponse = self.sendRequest(CONSTS.JSON_VALUE_REQUEST_SERVICE_GET_SENSOR_VALUES, payload=None, filez=None)
        return valuesResponse.content

    def uploadImage(self):
        #Should select latest image dynamically 
        camera_image = {CONSTS.JSON_KEY_REQUEST_FILE : ('camera_still', open(CONSTS.DIR_CAMERA + "img.png", 'rb'))}
        r = self.sendRequest(CONSTS.JSON_VALUE_REQUEST_SERVICE_UPLOAD_CAMERA_STILL, None, filez=camera_image)

    def sendRequest(self, service, payload, filez):
        if self.DEBUG:
            print self.LOGTAG, " :: ", service

        url = CONSTS.API_URL_CS1 + CONSTS.API_URL_MANAGER
        headers = CONSTS.REQUEST_DEFAULT_HEADERS

        if service is not None:
            headers[CONSTS.JSON_KEY_REQUEST_SERVICE] = service

        if self.DEBUG and payload is not None: 
            print self.LOGTAG, " :: Uploading -> " , payload

        if payload is not None:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
        elif filez is not None:
            response = requests.post(url, headers=headers, files=filez)
        else:
            response = requests.post(url, headers=headers)

        if self.DEBUG:
            print self.LOGTAG, " -> Response Content :: ", response.content

        if response.status_code == requests.codes.ok:
            print self.LOGTAG, " :: ", service, " Completed Successfully"
        else:
            print self.LOGTAG, " :: ERROR: ",service, " -> status_code:", sendResponse.status_code

        return response

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
        self.__sensorValueUploadRate = newRate

    def getSystemConfigRequestRate(self):
        return self.__systemConfigRequestRate

    def setSystemConfigRequestRate(self, newRate):
        self.__systemConfigRequestRate = newRate

    def getCameraImageUploadRate(self):
        return self.__cameraImageUploadRate

    def setCameraImageUploadRate(self, newRate):
        self.__cameraImageUploadRate = newRate

sensorFactory = SensorFactory()
sensorManager = SensorManager(sensorFactory.getSensors(), None) 
apiManager    = APIManager(sensorManager=sensorManager)
#apiManager.getSystemConfig()
#apiManager.updateSystemConfig()
#apiManager.getLatestSensorValues()
apiManager.uploadImage()

