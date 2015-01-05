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
from alert_manager import AlertManager
#Constants
DEBUG = True

def main():
    ##TODO
    # Configuration Manager/ Interface - @
    # System details configuration - naming etc 
    # Sensor Alerting and Info table - 1
    # AlertManager - 1 
    # Implement MQ2 in c
    # Uploading Video?
    # Dropbox? / Google Drive? 
    # User Pairing System
    # Automated Setup
    # System Status readings
    # Rasberry as AP
    # Amazon Datastore
    # Push Notifications
    # Data Truncation
    # Graphing on cs1

    #Mon
            #lights
            #Order sensors

    databaseManager = DatabaseManager()
    alertManager    = AlertManager()  
    sensorFactory   = SensorFactory(alertManager=alertManager)
    sensorManager   = SensorManager(sensorFactory.getSensors(), databaseManager) 
    apiManager      = APIManager(sensorManager=sensorManager)
    configurationManager = ConfigurationManager({apiManager, databaseManager, sensorManager, alertManager})
    configurationManager.writeoutConfiguration()
    #Api needs this to update configuration
    apiManager.setConfigManager(configurationManager)

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."
