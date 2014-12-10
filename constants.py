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

#SENSOR Names - Also used as SQL Table names
SENSOR_THERMISTOR    = "thermistor"
SENSOR_MQ7           = "carbon_monoxide"
SENSOR_FLAMMABLE_GAS = "flammable_gas"
SENSOR_MOTION        = "motion"