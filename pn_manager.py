#!/usr/bin/env python

#Push Notification Manager handles GCM interaction
#Author: Kevin Murphy
#Date  : 4 - Jan - 15

import json
from configurable import Configurable
import constants as CONSTS
from gcm import GCM

class PNManager(object):
    DEBUG  = True
    LOGTAG = "PNManager"

    testData = {'param1': 'value1', 'param2': 'value2'}

    def __init__(self):
        self.__gcm = GCM(CONSTS.GCM_API_KEY)

        if self.DEBUG:
            print self.LOGTAG, " :: Created"

    def sendJsonPush(self, data):
        reg_ids = ['12', '34', '69']
        response = self.__gcm.json_request(registration_ids=reg_ids, data=self.testData)
        print response

pnManager = PNManager()
pnManager.sendJsonPush(None)