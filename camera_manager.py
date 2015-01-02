#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

import subprocess
import constants as CONSTS

class CameraManager(object):
    DEBUG = True
    LOGTAG = "CameraManager"

    @staticmethod
    def takeStill():
    	print "CameraManager :: Taking Still"
        subprocess.call(CONSTS.SCRIPT_TAKE_CAMERA_STILL, shell=True)

    @staticmethod
    def recordVideo():
    	print "CameraManager :: Taking Video"
    	subprocess.call(CONSTS.SCRIPT_TAKE_CAMERA_VIDEO, shell=True)

