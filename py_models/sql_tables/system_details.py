#!/usr/bin/env python
#Author : Kevin Murphy
#Date   : 10 - Dec - 14

import constants as CONSTS
import peewee 
from peewee import *
import datetime
import database_manager as DatabaseManager

class System_Details(peewee.Model):
    class Meta:
        database = DatabaseManager().getDatabase()

    #Define DB Fields
    ip_address        = peewee.CharField()
    gps_coords_aprrox = peewee.CharField()