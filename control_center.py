#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

import ctypes
import time
import sched
import RPi.GPIO as GPIO

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

#Timing Values
PROBE_RATE_DEFAULT = 10
SENSOR_PRIORITY_DEFAULT = 1

#Creates sensor objects
def setupSensors():
    #Using the Global keyword to allow initialization of global variables
    global thermistor 
    global mq7
    global motion_detector

    thermistor      = Thermistor(sensorLib)
    mq7             = MQ7(sensorLib)
    motion_detector = MotionDetector(sensorLib)

def probeSensor(sched, sensor):
    global PROBE_RATE_DEFAULT
    global SENSOR_DEFAULT_PRIORITY

    global thermistor
    global mq7
    global motion_detector
    
    if sensor is thermistor.getName():
        print thermistor.readValue()
        sched.enter(PROBE_RATE_DEFAULT, 1, probeSensor,(sched, sensor))
    elif sensor is mq7.getName():
        print mq7.readValue()
        sched.enter(PROBE_RATE_DEFAULT, 1, probeSensor,(sched, sensor))
    elif sensor is motion_detector.getName():
        print motion_detector.readValue()
        sched.enter(PROBE_RATE_DEFAULT, 1, probeSensor,(sched, sensor)) 

def main():
    global PROBE_RATE_DEFAULT
    setupSensors()
    
    schedular = sched.scheduler(time.time, time.sleep)	
    schedular.enter(PROBE_RATE_DEFAULT, 1, probeSensor, (schedular, thermistor.getName()))
    schedular.enter(PROBE_RATE_DEFAULT, 1, probeSensor, (schedular, motion_detector.getName()))
    schedular.enter(PROBE_RATE_DEFAULT, 1, probeSensor, (schedular, mq7.getName()))

    schedular.run()
try:
    main()
except KeyboardInterrupt:
    print "Keyboard Interrupt.."
    GPIO.cleanup()
