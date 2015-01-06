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
from system_details_manager import SystemDetailsManager
from wifi_direct_manager import WifiDirectManager

#Constants
DEBUG = True

def main():
    ##TODO
    # Info table - 1
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

    #Tues
    #Get dongle working
    #Pi as AP
    #Wifi Direct
    #System Stat Manager

    databaseManager = DatabaseManager()
    alertManager    = AlertManager()  
    sensorFactory   = SensorFactory(alertManager=alertManager)
    sensorManager   = SensorManager(sensorFactory.getSensors(), databaseManager) 
    wifiDirectManager = WifiDirectManager(sensorManager=sensorManager)
    apiManager      = APIManager(sensorManager=sensorManager)
    systemDetailsManager = SystemDetailsManager(databaseManager=databaseManager)
    configurationManager = ConfigurationManager({apiManager, databaseManager, sensorManager, 
                                                 alertManager, systemDetailsManager, wifiDirectManager})
    configurationManager.writeoutConfiguration()
    #Api needs this to update configuration
    apiManager.setConfigManager(configurationManager)

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."
