#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

try:
    import picamera
except ImportError:
    pass

from time import sleep

class PiCamera(object):
	DEBUG = True
	LOGTAG = "PiCamera"
