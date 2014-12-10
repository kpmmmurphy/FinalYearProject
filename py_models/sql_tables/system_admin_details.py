#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 10 - Dec - 14

import constants as CONSTS
import peewee 
from peewee import *
import datetime
import database_manager as DatabaseManager

class System_Admin_Details(peewee.Model):
    class Meta:
        database = DatabaseManager().getDatabase()

    def save(self, *args, **kwargs):
        self.date_and_time = datetime.datetime.now()
        super(myModel, self).save(*args, **kwargs)

    #Define DB Fields
    last_name     = peewee.CharField()
    first_name    = peewee.CharField()
    device_id     = peewee.CharField()
    date_and_time = peewee.DateTimeField(formats=CONSTS.DATE_FORMAT)