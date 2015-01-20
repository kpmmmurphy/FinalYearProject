#!/usr/bin/env python

#Author : Kevin Murphy
#Date   : 16 - Dec - 14
#
#API class handling all http requests

import requests
import json
import time
import os
from threading import Timer
from configurable import Configurable
import constants as CONSTS

from sensor_factory   import SensorFactory
from sensor_manager   import SensorManager

class APIManager(Configurable):
    DEBUG  = True
    LOGTAG = "APIManager"

    __sensorManager = None
    __configurationManager = None
    __polling = True

    #Configurables
    __systemConfigRequestRate = CONSTS.REQUEST_RATE_SYSTEM_CONFIG
    __sensorValueUploadRate   = CONSTS.REQUEST_RATE_UPLOAD_SENSOR_VALUES
    __cameraImageUploadRate   = CONSTS.REQUEST_RATE_UPLOAD_CAMERA_IMAGE

    def __init__(self, sensorManager):
        super(APIManager, self).__init__(CONSTS.JSON_KEY_API_CONFIG)

        if self.DEBUG:
            print self.LOGTAG, " :: Created"

        if sensorManager is not None:
            self.__sensorManager = sensorManager
            self.schedule_UploadSensorValues()
            self.schedule_UploadCameraStill()
            self.schedule_SysConfigCheck()
            self.schedule_UploadCameraVideo()

    def configure(self, config):
        if self.DEBUG:
            print self.LOGTAG, ":: Configuring"
        
        if config is not None:
            try:
                apiConfig = config[self.getJsonConfigKey()]
                self.setSensorValueUploadRate(apiConfig[CONSTS.JSON_KEY_API_SENSOR_VALUE_UPLOAD_RATE])
                self.setSystemConfigRequestRate(apiConfig[CONSTS.JSON_KEY_API_SYSTEM_CONFIG_REQUEST_RATE])
                self.setCameraImageUploadRate(apiConfig[CONSTS.JSON_KEY_API_CAMERA_IMAGE_UPLOAD_RATE])
            except KeyError:
                if self.DEBUG:
                    print self.LOGTAG, " :: Config not present"

    #---------API CALLS-----------------------------
    def getSystemConfig(self):
        configResponse = self.sendRequest(service=CONSTS.JSON_VALUE_REQUEST_SERVICE_GET_CONFIG, payload=None, filez=None)   
        if self.__polling:
            self.schedule_SysConfigCheck()

        if configResponse is not None and self.getConfigManager() is not None:
            self.getConfigManager().reconfigure(configResponse.content)


    def uploadSensorValues(self):
        self.sendRequest(service=CONSTS.JSON_VALUE_REQUEST_SERVICE_UPLOAD_SENSOR_VALUES, payload=self.__sensorManager.getSensorValues(), filez=None)
        if self.__polling:
            self.schedule_UploadSensorValues()

    def uploadImage(self):
        #Should select latest image dynamically 
        images = os.listdir(CONSTS.DIR_CAMERA_STILL)
        if len(images) > 0:
            camera_image = {CONSTS.JSON_KEY_CAMERA_STILL : (images[0], open(CONSTS.DIR_CAMERA_STILL + images[0], 'rb'), 'image/png')}
            self.sendRequest(service=None, payload=None, filez=camera_image)

        if self.__polling:
            self.schedule_UploadCameraStill()

    def uploadVideo(self):
        #Should select latest image dynamically 
        videos = os.listdir(CONSTS.DIR_CAMERA_VIDEO)
        if len(videos) > 0:
            camera_video = {CONSTS.JSON_KEY_CAMERA_STILL : (videos[0], open(CONSTS.DIR_CAMERA_VIDEO + videos[0], 'rb'), 'video/mp4')}
            self.sendRequest(service=None, payload=None, filez=camera_video)

        if self.__polling:
            self.schedule_UploadCameraVideo()

    #Purely for testing server side api 
    def getLatestSensorValues(self):
        valuesResponse = self.sendRequest(service=CONSTS.JSON_VALUE_REQUEST_SERVICE_GET_SENSOR_VALUES, payload=None, filez=None)
        return valuesResponse.content

    #Purely for testing server side api 
    def updateSystemConfig(self):
        file = open('config/test_config.json', 'r')
        configResponse = self.sendRequest(service=CONSTS.JSON_VALUE_REQUEST_SERVICE_UPDATE_CONFIG, payload=file.read(), filez=None)

        return configResponse.content

    def sendRequest(self, service, payload, filez):
        url = CONSTS.API_URL_CS1 + CONSTS.API_URL_MANAGER
        headers = CONSTS.REQUEST_DEFAULT_HEADERS

        if service is not None:
            headers[CONSTS.JSON_KEY_REQUEST_SERVICE] = service
        else:
            service = "file_uploading"

        if self.DEBUG:
            print self.LOGTAG, " :: Service -> ", service

        if self.DEBUG and payload is not None: 
            print self.LOGTAG, " :: Uploading -> " , payload

        try:
            if payload is not None:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
            elif filez is not None:
                response = requests.post(url, headers=None, files=filez)
            else:
                response = requests.post(url, headers=headers)
    
            if self.DEBUG and response.text != "" and response.text != None:
                print self.LOGTAG, " :: Response Content -> ", response.text, "\n"

            if self.DEBUG and response.status_code == requests.codes.ok:
                print self.LOGTAG, " :: ", service, " -> Completed Successfully"
            else:
                print self.LOGTAG, " :: ERROR: ",service, " -> status_code:", sendResponse.status_code
    
            return response
        except requests.ConnectionError:
            if self.DEBUG:
                print self.LOGTAG, ":: ConnectionError Thrown"

    #-------Polling Calls---------------------------
    def schedule_SysConfigCheck(self):
        timer = Timer(self.getSystemConfigRequestRate(), self.getSystemConfig,())
        timer.start()

    def schedule_UploadSensorValues(self):
        timer = Timer(self.getSensorValueUploadRate(), self.uploadSensorValues,())
        timer.start()

    def schedule_UploadCameraStill(self):
        timer = Timer(self.getCameraImageUploadRate(), self.uploadImage,())
        timer.start()

    def schedule_UploadCameraVideo(self):
        timer = Timer(self.getCameraImageUploadRate(), self.uploadVideo,())
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

    def getConfigManager(self):
        return self.__configurationManager

    def setConfigManager(self, configurationManager):
        self.__configurationManager = configurationManager

    def toString(self):
        data = { CONSTS.JSON_KEY_API_SENSOR_VALUE_UPLOAD_RATE   : self.getSensorValueUploadRate(), 
                 CONSTS.JSON_KEY_API_SYSTEM_CONFIG_REQUEST_RATE : self.getSystemConfigRequestRate(), 
                 CONSTS.JSON_KEY_API_CAMERA_IMAGE_UPLOAD_RATE   : self.getCameraImageUploadRate()}
        
        if self.DEBUG:
            print self.LOGTAG , json.dumps(data)

        return data    

'''
sensorFactory = SensorFactory()
sensorManager = SensorManager(sensorFactory.getSensors(), None) 
apiManager    = APIManager(sensorManager=sensorManager)
apiManager.getSystemConfig()
apiManager.updateSystemConfig()
apiManager.uploadSensorValues()
apiManager.uploadImage()
'''