#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

from ctypes import cdll

lib = cdll.LoadLibrary("./sensors/libs/lib_SensorManager.so")


