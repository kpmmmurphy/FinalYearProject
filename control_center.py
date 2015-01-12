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

    ##TODO
    # Info table - 1
    # Implement MQ2 in c
    # Uploading Video?
    # Dropbox? / Google Drive? 
    # User Pairing System
    # Automated Setup
    # System Status readings
    # Amazon Datastore
    # Push Notifications
    # Data Truncation
    # Graphing on cs1

    #Wed
    #Wifi Direct Manager - Wireshark
    #APP
    #System Stat Manager
    #PAcket format, service and payload.. /'s could be a problem
    #Implement socket for config/other android client packets

def main():
    databaseManager = DatabaseManager()
    alertManager    = AlertManager()  
    sensorFactory   = SensorFactory(alertManager=alertManager)
    sensorManager   = SensorManager(sensorFactory.getSensors(), databaseManager) 
    apiManager      = APIManager(sensorManager=sensorManager)
    systemDetailsManager = SystemDetailsManager(databaseManager=databaseManager)
    wifiDirectManager = WifiDirectManager(sensorManager=sensorManager)
    configurationManager = ConfigurationManager({apiManager, databaseManager, sensorManager, 
                                                 alertManager, systemDetailsManager, wifiDirectManager})
    #configurationManager.writeoutConfiguration()
    #Api and WifiDirectManager both need to update configuration
    apiManager.setConfigManager(configurationManager)
    wifiDirectManager.setConfigManager(configurationManager)

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."
