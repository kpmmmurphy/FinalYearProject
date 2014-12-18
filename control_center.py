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
    # Configuration Manager/ Interface - @
    # Sensor Alerting and Info table - 1
    # AlertManager - 1 
    # API Manager - 2 -> TEST
    # CS1 integration / Configurable DB??
    # Camera Stills, and Video?
    # Dropbox? / Google Drive? 
    # User Pairing System
    # Automated Setup
    # System Status readings
    # Rasberry as AP
    # Amazon Datastore
    # Push Notifications

    databaseManager = DatabaseManager()
    #databaseManager.createTables()

    sensorFactory   = SensorFactory()
    sensorManager   = SensorManager(sensorFactory.getSensors(), databaseManager) 

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."

