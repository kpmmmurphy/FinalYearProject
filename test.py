#!/usr/bin/env python

#WifiDirect Manager
#Author: Kevin Murphy
#Date  : 6 - Jan - 15

import json
import socket
import time
import struct
import threading 
import netifaces
import subprocess
import os
from model.peer import Peer
from configurable import Configurable
import constants as CONSTS
from camera_manager import CameraManager

class FileCopier(object):

	def transferFileFromDir(self, dir):
		files = os.listdir(dir)
		images = [img for img in files if img.endswith('.py')]
		print "Nums :: ", images

dir = "."
fileCopier = FileCopier().transferFileFromDir(dir)