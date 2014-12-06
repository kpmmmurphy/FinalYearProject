#!/usr/bin/env python

#Manages Sensor Inputs
#Author: Kevin Murphy
#Date  : 18 - Oct - 14

import time
import sched

#Import infrastructure modules
from sensor_factory import SensorFactory

#Constants
DEBUG = True

def probeSensor(sched, sensor):
    if sensor.isActive():
        sensorValue = sensor.readValue()
        if DEBUG:
            print sensor.getName() , " :: " , sensorValue

        sched.enter(sensor.getProbeRate(), sensor.getPriority(), probeSensor,(sched, sensor))

        return sensorValue

def main():
    sensorFactory = SensorFactory() 
    
    schedular = sched.scheduler(time.time, time.sleep)	
    for sensor in sensorFactory.getSensors():
        sensor.toString()
        sensor.configure()
        schedular.enter(sensor.getProbeRate(), sensor.getPriority(), probeSensor, (schedular, sensor))
   
    schedular.run()

try:
    main()
except KeyboardInterrupt, SystemExit:
    print "KeyboardInterrupted..."

