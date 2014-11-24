#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

import ctypes

#Import Sensors
from py_sensors.thermistor import Thermistor
from py_sensors.mq7 import MQ7
from py_sensors.motion_detector import MotionDetector

#Load .so c/c++ sensor library
LIB_PATH = "./sensors/libs/lib_SensorManager.so"
sensorLib = ctypes.cdll.LoadLibrary(LIB_PATH)

#Global Sensors
thermistor      = None
mq7             = None
motion_detector = None

#Creates sensor objects
def setupSensors():
    #Using the Global keyword to allow initialization of global variables
    global thermistor 
    global mq7
    global motion_detector

    thermistor      = Thermistor(sensorLib)
    mq7             = MQ7(sensorLib)
    motion_detector = MotionDetector(sensorLib)

def probeSensors():
    print thermistor.readValue()
    print mq7.readValue()
    print motion_detector.readValue()

def main():
    setupSensors()
    probeSensors()

main()
