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

    def __init__(self):
        self.__gcm = GCM(CONSTS.GCM_API_KEY)

        if self.DEBUG:
            print self.LOGTAG, " :: Created"

    def sendJsonPush(self, data):
        apiManager = APIManager(sensorManager=None)
        registration_ids = json.loads(apiManager.getPNRegIDs())
        response = self.__gcm.json_request(registration_ids=registration_ids[CONSTS.JSON_KEY_PN_MANAGER_REG_IDS], data=data)
        if self.DEBUG:
            print response

pnManager = PNManager()
testData = {'sensor': 'temperature', 'value': 50}
pnManager.sendJsonPush(testData)