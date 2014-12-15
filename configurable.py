#!/usr/bin/env python   

#A configuration interface, providing one method, configure 
#Author: Kevin Murphy
#Date  : 15 - Dec - 14

from abc import ABCMeta, abstractmethod 

class Configurable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def configure(self, config):
        pass
