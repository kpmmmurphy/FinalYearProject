#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 9 - Oct - 14
#
#Global Constants "Holder"

#SQL-----------------------------------------

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

#SENSOR Names - Also used as SQL Table names
SENSOR_THERMISTOR    = "temperature"
SENSOR_MQ7           = "carbon_monoxide"
SENSOR_MQ2           = "flammable_gas"
SENSOR_MOTION        = "motion"

SENSOR_DEFAULT_VALUE = -1

COLLECTION_RATE_DEFAULT     = 15
COLLECTION_PRIORITY_DEFAULT = 1