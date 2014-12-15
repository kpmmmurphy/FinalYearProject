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
    ##TODO
    # Sensor Alerting and Info table - 1
    # Automated Setup
    # Rasberry as AP
    # API Class - 2
    # API Manager - 2
    # AlertManager - 1 
    # Configuration Manager/ Interface
    # User Pairing System
    # Multithreading
    # Change Schedular to threading.timer
    # Amazon Datastore
    # CS1 integration

    databaseManager = DatabaseManager()
    #databaseManager.createTables()

    sensorFactory   = SensorFactory()
    sensorManager   = SensorManager(sensorFactory.getSensors(), databaseManager) 

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."

