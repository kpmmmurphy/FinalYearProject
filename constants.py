#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 9 - Oct - 14
#
#Global Constants "Holder"

#File Locations
CONFIGURATION_DEFAULT = "./config/default_config.json"

#SQL-----------------------------------------
COLLECTION_RATE_DEFAULT     = 15
COLLECTION_PRIORITY_DEFAULT = 1

#Test - Local - Database Credentials
TESTING_SQL    =  True
TEST_DB_NAME   = 'TEST'
TEST_DB_USER   = 'root'
TEST_DB_PASSWD = 'kevinmurphy'

#Production - CS1 - Database Credentials
DB_HOST   = 'csgate.ucc.ie'
DB_NAME   = '2015_kpm2'
DB_USER   = 'kpm2'
DB_PASSWD = 'shiegeib'
DB_PORT   = 80
SQL_DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

#SENSORS------------------------------------
SENSOR_DEFAULT_VALUE = -1

PROBE_RATE_DEFAULT = 10
PRIORITY_DEFAULT = 1

#SENSOR Names - Also used as SQL Table names
SENSOR_THERMISTOR    = "temperature"
SENSOR_MQ7           = "carbon_monoxide"
SENSOR_MQ2           = "flammable_gas"
SENSOR_MOTION        = "motion"

#JSON Keys -----------------------------------
#--Sensors
JSON_KEY_SENSORS_ARRAY     = "sensors"
JSON_KEY_SENSOR_NAME       = "name"
JSON_KEY_SENSOR_PRIORITY   = "priority"
JSON_KEY_SENSOR_PROBE_RATE = "probe_rate"
JSON_KEY_SENSOR_IS_ACTIVE  = "is_active"
JSON_KEY_SENSOR_ALERT_THRESHOLD  = "alert_threshold"

#--Collection
JSON_KEY_COLLECTION_OBJ      = "collection"
JSON_KEY_COLLECTION_PRIORITY = "collection_priority"
JSON_KEY_COLLECTION_RATE     = "collection_rate"

#ALERTING-----------------------------------
ALERT_THRESHOLD_DEFAULT_THERMISTOR = 50
ALERT_THRESHOLD_DEFAULT_MQ7        = 50
ALERT_THRESHOLD_DEFAULT_MOTION     = 1
ALERT_THRESHOLD_DEFAULT_MQ2        = 50