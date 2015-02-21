#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

import subprocess
import constants as CONSTS
import os
import sys
import signal
import subprocess
import time

class CameraManager(object):
    DEBUG = True
    LOGTAG = "CameraManager"

    @staticmethod
    def takeStill():
    	print "CameraManager :: Taking Still"
        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.
        pro = subprocess.Popen([CONSTS.SCRIPT_TAKE_CAMERA_STILL], 
                       shell=True, preexec_fn=os.setsid) 

        time.sleep(10)
        os.killpg(pro.pid, signal.SIGTERM)  # Send the signal to all the process groups

    @staticmethod
    def recordVideo():
    	print "CameraManager :: Taking Video"
        pro = subprocess.Popen([CONSTS.SCRIPT_TAKE_CAMERA_VIDEO], 
                       shell=True, preexec_fn=os.setsid) 

        time.sleep(40)
        os.killpg(pro.pid, signal.SIGTERM)  # Send the signal to all the process groups


    @staticmethod
    def startStream():
        print "CameraManager :: Starting Remote Stream"
        pro = subprocess.Popen([CONSTS.SCRIPT_START_REMOTE_STREAM], 
                       shell=True, preexec_fn=os.setsid) 

        time.sleep(30)
        os.killpg(pro.pid, signal.SIGTERM)

    @staticmethod
    def startLocalStream():
        print "CameraManager :: Starting Local Stream"
        pro = subprocess.Popen([CONSTS.SCRIPT_START_STREAM], 
                       shell=True, preexec_fn=os.setsid) 

        time.sleep(30)
        os.killpg(pro.pid, signal.SIGTERM)


