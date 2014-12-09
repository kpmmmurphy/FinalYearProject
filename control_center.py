#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

#Import infrastructure modules
from sensor_factory   import SensorFactory
from sensor_manager   import SensorManager
from database_manager import DatabaseManager

#Constants
DEBUG = True

def main():
    DatabaseManager.getInstance().createTables()
    sensorFactory = SensorFactory()
    sensorManager = SensorManager(sensorFactory.getSensors())

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."

