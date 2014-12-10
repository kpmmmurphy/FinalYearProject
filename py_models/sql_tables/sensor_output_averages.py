#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 10 - Dec - 14

import constants as CONSTS
import peewee 
from peewee import *
import datetime
import database_manager as DatabaseManager

class Sensor_Output_Averages(peewee.Model):
    class Meta: 
        database = DatabaseManager().getDatabase()

    def save(self, *args, **kwargs):
        self.date_and_time = datetime.datetime.now()
        super(myModel, self).save(*args, **kwargs)

    #Define DB fields
    date_and_time       = peewee.DateTimeField(formats=CONSTS.DATE_FORMAT)
    carbon_monoxide     = peewee.IntegerField()
    temperature         = peewee.IntegerField()
    flammable_gas       = peewee.IntegerField()
    motion              = peewee.IntegerField()
    
    