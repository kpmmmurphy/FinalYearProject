#!/usr/bin/env python

#Author : Kevin Murphy
#Date   : 9 - Oct - 14
#
#Global Constants "Holder"

#OS
RASP_PI = "raspberrypi"

#File Locations
CONFIGURATION_DEFAULT = "./config/default_config.json"

#SQL-----------------------------------------
COLLECTION_RATE_DEFAULT     = 15
COLLECTION_PRIORITY_DEFAULT = 1

#Test - Local - Database Credentials
TESTING_SQL = True
DB_NAME   = 'fyp'
DB_USER   = 'root'
DB_PASSWD_PI = '111314826'
DB_PASSWD_UBUNTU = 'kevinmurphy'

#Production - CS1 - Database Credentials
#DB_HOST   = 'https://csgate.ucc.ie'
#DB_HOST   = 'https://cs1.ucc.ie'
#DB_NAME   = '2015_kpm2'
#DB_USER   = 'kpm2'
#DB_PASSWD = 'shiegeib'
#DB_PORT   = 80
SQL_DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

#---SENSORS------------------------------------
SENSOR_DEFAULT_VALUE = -1

PROBE_RATE_DEFAULT = 10
PRIORITY_DEFAULT = 1

#SENSOR Names - Also used as SQL Table names
SENSOR_THERMISTOR    = "temperature"
SENSOR_MQ7           = "carbon_monoxide"
SENSOR_MQ2           = "flammable_gas"
SENSOR_MOTION        = "motion"

#---JSON Keys -----------------------------------
JSON_KEY_DEFAULT = "default"

#Database
JSON_KEY_DATABASE_MANAGER_CONFIG = "database_manager"

#Sensors
JSON_KEY_SENSORS_ARRAY     = "sensors"
JSON_KEY_SENSOR_NAME       = "name"
JSON_KEY_SENSOR_PRIORITY   = "priority"
JSON_KEY_SENSOR_PROBE_RATE = "probe_rate"
JSON_KEY_SENSOR_IS_ACTIVE  = "is_active"
JSON_KEY_SENSOR_ALERT_THRESHOLD  = "alert_threshold"

#Sensor Manager
JSON_KEY_SENSOR_MANAGER_CONFIG = "sensor_manager"
JSON_KEY_COLLECTION_PRIORITY   = "collection_priority"
JSON_KEY_COLLECTION_RATE       = "collection_rate"

#API
JSON_KEY_API_CONFIG = "api_manager"
JSON_KEY_API_SYSTEM_CONFIG_REQUEST_RATE = "sys_config_request_rate"
JSON_KEY_API_SENSOR_VALUE_UPLOAD_RATE   = "sensor_value_upload_rate"
JSON_KEY_API_CAMERA_IMAGE_UPLOAD_RATE   = "camera_image_upload_rate"

#Config Manager
JSON_KEY_CONFIG_MANAGER_CONFIG = "config_manager"

#Requests
JSON_KEY_REQUEST_SERVICE       = "service"
JSON_KEY_REQUEST_SENSOR_VALUES = "sensor_values"
JSON_KEY_REQUEST_FILE          = "file"     
JSON_KEY_CAMERA_STILL          = "camera_still"  

JSON_VALUE_REQUEST_SERVICE_GET_CONFIG           = "get_config"
JSON_VALUE_REQUEST_SERVICE_UPDATE_CONFIG        = "update_config"
JSON_VALUE_REQUEST_SERVICE_UPLOAD_SENSOR_VALUES = "upload_sensor_values"
JSON_VALUE_REQUEST_SERVICE_GET_SENSOR_VALUES    = "get_sensor_values"
JSON_VALUE_REQUEST_SERVICE_UPLOAD_CAMERA_STILL  = "upload_camera_still"

#---ALERTING-----------------------------------
ALERT_THRESHOLD_DEFAULT_THERMISTOR = 50
ALERT_THRESHOLD_DEFAULT_MQ7        = 50
ALERT_THRESHOLD_DEFAULT_MOTION     = 1
ALERT_THRESHOLD_DEFAULT_MQ2        = 50

#---SCRIPTS------------------------------------
SCRIPTS_DIR              = "./scripts/"
SCRIPTS_DIR_IMG          = "image/"
SCRIPTS_DIR_NETWORKING   = "networking/"
SCRIPTS_DIR_SETUP        = "setup/"
SCRIPT_TAKE_CAMERA_STILL = SCRIPTS_DIR + SCRIPTS_DIR_IMG + "take_camera_still.sh"

#DIRs
DIR_CAMERA = "./camera/"
DIR_CONFIG = "./config/"

#---API------------------------------------------
API_URL_CS1     = "http://cs1.ucc.ie/~kpm2/fyp/api/"
API_URL_MANAGER = "api_manager.php"

#Headers
REQUEST_DEFAULT_HEADERS = {'content-type': 'application/json'}

#Payloads
REQUEST_PAYLOAD_CONFIG_GET           = {JSON_KEY_REQUEST_SERVICE : JSON_VALUE_REQUEST_SERVICE_GET_CONFIG}
REQUEST_PAYLOAD_UPLOAD_SENSOR_VALUES = {JSON_KEY_REQUEST_SERVICE : JSON_VALUE_REQUEST_SERVICE_UPLOAD_SENSOR_VALUES}
REQUEST_PAYLOAD_UPLOAD_CAMERA_IMAGE  = {JSON_KEY_REQUEST_SERVICE : JSON_VALUE_REQUEST_SERVICE_UPLOAD_CAMERA_STILL}

#Request/Upload Rates
REQUEST_RATE_SYSTEM_CONFIG        = 60
REQUEST_RATE_UPLOAD_SENSOR_VALUES = 10
REQUEST_RATE_UPLOAD_CAMERA_IMAGE  = 60