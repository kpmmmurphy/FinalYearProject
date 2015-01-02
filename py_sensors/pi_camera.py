#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

import subprocess
from time import sleep
import datetime

class PiCamera(object):
    DEBUG = True
    LOGTAG = "PiCamera"

    @staticmethod
    def takeStill():
    	if self.DEBUG:
    		print self.LOGTAG, " :: Taking Still"
        subprocess.call(CONSTS.SCRIPT_TAKE_CAMERA_STILL, shell=True)

    @staticmethod
    def recordVideo():
    	if self.DEBUG:
    		print self.LOGTAG, " :: Taking Video"
    	subprocess.call(CONSTS.SCRIPT_TAKE_CAMERA_VIDEO, shell=True)

PiCamera.takeStill()
PiCamera.recordVideo()
