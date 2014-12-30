#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

#Import infrastructure modules
from sensor_factory   import SensorFactory
from sensor_manager   import SensorManager
from database_manager import DatabaseManager
from api_manager      import APIManager
from configuration_manager import ConfigurationManager

#Constants
DEBUG = True

def main():
    ##TODO
    # Configuration Manager/ Interface - @
    # System details configuration - naming etc 
    # Sensor Alerting and Info table - 1
    # AlertManager - 1 
    # Uploading Video?
    # Dropbox? / Google Drive? 
    # User Pairing System
    # Automated Setup
    # System Status readings
    # Rasberry as AP
    # Amazon Datastore
    # Push Notifications

    databaseManager = DatabaseManager()
    sensorFactory   = SensorFactory()
    sensorManager   = SensorManager(sensorFactory.getSensors(), databaseManager) 
    apiManager      = APIManager(sensorManager=sensorManager, configurationManager=None)
    configurationManager = ConfigurationManager({apiManager, databaseManager, sensorManager})
    #Api needs this to update configuration
    apiManager.setConfigManager(configurationManager)

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."

