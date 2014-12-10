#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 10 - Dec - 14

import constants as CONSTS
import peewee 
from peewee import *
import datetime
import database_manager as DatabaseManager

class Current_Day_Sensor_Output(peewee.Model):

    class Meta:
        database = DatabaseManager().getDatabase()

    def save(self, *args, **kwargs):
        self.date_and_time = datetime.datetime.now()
        super(Current_Day_Sensor_Output, self).save(*args, **kwargs)

    #Define DB fields
    date_and_time       = peewee.DateTimeField(formats=CONSTS.SQL_DATE_FORMAT)
    carbon_monoxide     = peewee.IntegerField()
    temperature         = peewee.IntegerField()
    flammable_gas       = peewee.IntegerField()
    motion              = peewee.IntegerField()