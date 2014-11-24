#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

import ctypes

#Import Sensors
from thermistor import Thermistor
from mq7 import MQ7
from motion_detector import MotionDetector

#Load .so c/c++ sensor library
LIB_PATH = "./sensors/libs/lib_SensorManager.so"
lib = ctypes.cdll.LoadLibrary(LIB_PATH)


def setupSensors():
    thermistor      = Thermistor(lib)
    mq7             = MQ7(lib)
    motion_detector = MotionDetector(lib)

def probeSensors():
    print thermistor.readValue()
    print mq7.readValue()
    print motion_detector.readvalue()

def main():
    setupSensors()
    probeSensors()

main()