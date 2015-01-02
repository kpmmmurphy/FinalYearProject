#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

try:
    import picamera
except ImportError:
    pass

from time import sleep
import datetime

class PiCamera(object):
    DEBUG = True
    LOGTAG = "PiCamera"

    @staticmethod
    def takeStill():
        camera = picamera.PiCamera()
        imageName = str(datetime.datetime.now().time()) + ".png"
        camera.capture(imageName)

    @staticmethod
    def recordVideo(duration):
    	camera = picamera.PiCamera()
    	camera.start_recording('video.h264')
    	sleep(duration)
    	camera.stop_recording()

PiCamera.takeStill()
PiCamera.recordVideo(5)
