#!/usr/bin/env python

#Author : Kevin Murphy
#Date   : 16 - Dec - 14
#
#API class handling all http requests

import requests
from configurable import Configurable
import constants as CONSTS

from sensor_factory   import SensorFactory
from sensor_manager   import SensorManager

class APIManager(Configurable):
    DEBUG  = True
    LOGTAG = "APIManager"

    __sensorManager = None

    def __init__(self, sensorManager):
        if self.DEBUG:
            print self.LOGTAG, " :: Created"

        if sensorManager is not None:
            self.__sensorManager = sensorManager

    def configure(self, value):
    	if self.DEBUG:
    	    print self.LOGTAG, ":: Configuring"

    def getSystemConfig(self):
    	if self.DEBUG:
    		print self.LOGTAG, " :: Requesting System Configuration"

        configResponse = requests.post(CONSTS.API_URL_CS1 + CONSTS.API_URL_MANAGER, data=CONSTS.REQUEST_PAYLOAD_CONFIG_GET)	
        if self.DEBUG:
            print configResponse.url
            print configResponse.content

    def sendSensorValues(self):
        if self.DEBUG:
            print self.LOGTAG, " :: Sending Sensor Values"
        payload = CONSTS.REQUEST_PAYLOAD_UPLOAD_SENSOR_VALUES
        payload[CONSTS.JSON_KEY_REQUEST_SENSOR_VALUES] = self.__sensorManager.getSensorValues()
        print payload
        #print CONSTS.REQUEST_PAYLOAD_UPLOAD_SENSOR_VALUES
        #sendResponse = requests.post(CONSTS.API_URL_CS1 + CONSTS.API_URL_MANAGER, data)

    def test(self):
    	cs1_test = requests.get("http://cs1.ucc.ie/~kpm2/fyp/api/test.txt")	
    	print cs1_test.content

sensorFactory   = SensorFactory()
sensorManager   = SensorManager(sensorFactory.getSensors(), None) 
apiManager = APIManager(sensorManager=sensorManager)
#apiManager.getSystemConfig()
apiManager.sendSensorValues()


