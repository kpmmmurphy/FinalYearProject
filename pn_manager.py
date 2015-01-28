#!/usr/bin/env python

#Push Notification Manager handles GCM interaction
#Author: Kevin Murphy
#Date  : 4 - Jan - 15

import json
from configurable import Configurable
import constants as CONSTS
from gcm import GCM
from api_manager import APIManager

class PNManager(object):
    DEBUG  = True
    LOGTAG = "PNManager"

    testData = {'param1': 'value1', 'param2': 'value2'}

    def __init__(self):
        self.__gcm = GCM(CONSTS.GCM_API_KEY)

        if self.DEBUG:
            print self.LOGTAG, " :: Created"

    def sendJsonPush(self, data):
        apiManager = APIManager(sensorManager=None)
        response = self.__gcm.json_request(registration_ids=apiManager.getPNRegIDs(), data=self.testData)
        if self.DEBUG:
            print response

pnManager = PNManager()
pnManager.sendJsonPush(None)