#!/usr/bin/env python

#Buzzer!! 
#Author: Kevin Murphy
#Date  : 3 - Jan - 15

try:
    import RPi.GPIO as GPIO
except ImportError:
	print "RPi.GPIO not found, proceeding without"
import time

class Buzzer(object):

	@staticmethod
	def buzz():
		sleep_time = 0.2

		#set up GPIO using BCM numbering
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.OUT)
		
		GPIO.output(18, True)
		time.sleep(sleep_time)
		GPIO.output(18, False)
		time.sleep(sleep_time)
		GPIO.output(18, True)
		time.sleep(sleep_time)
		GPIO.output(18, False)
		GPIO.cleanup()
