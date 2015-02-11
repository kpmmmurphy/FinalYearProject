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

##---TODO
#FEB
#--- Direct Images
#Video // Streaming, local?
#System Stat Manager
#Galileo?....

#Constants
DEBUG = True

def main():
    databaseManager = DatabaseManager()
    alertManager    = AlertManager()  
    sensorFactory   = SensorFactory(alertManager=alertManager)
    sensorManager   = SensorManager(sensorFactory.getSensors(), databaseManager) 
    apiManager      = APIManager(sensorManager=sensorManager)
    systemDetailsManager = SystemDetailsManager(databaseManager=databaseManager)
    wifiDirectManager = WifiDirectManager(sensorManager=sensorManager, databaseManager=databaseManager)
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
