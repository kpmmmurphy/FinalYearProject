#!/usr/bin/env python

#Author : Kevin Murphy
#Date   : 16 - Dec - 14
#
#API class handling all http requests

import requests
from configurable import Configurable
import constants as CONSTS

class APIManager(Configurable):
    DEBUG  = True
    LOGTAG = "APIManager"

    def __init__(self):
		if self.DEBUG:
			print self.LOGTAG, " :: Created"

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

    def test(self):
    	cs1_test = requests.get("http://cs1.ucc.ie/~kpm2/fyp/api/test.txt")	
    	print cs1_test.content

apiManager = APIManager()
apiManager.getSystemConfig()


