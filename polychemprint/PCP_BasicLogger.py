# -*- coding: utf-8 -*-
"""
The *PCP_BasicLogger* Abstract Base Class specifies the interface for all classes to write themselves to log and read in

| First created on Sun Oct 20 00:03:21 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

Inputs
---------
    :param test: args
    :param test: args
    
Methods
---------
    :param: args
    :param test: args
    
Attributes
-----------
    :param test: args
    :param test: args
    
Outputs
---------
    :None: Everything output to terminal window, no return value
    
"""

from abc import ABC, abstractmethod
import json

class PCP_BasicLogger(ABC):
    def __init__(self,**kwargs):
        pass
        #kill extra args here
            
####################### Logging METHODS ############################### 
    @abstractmethod
    def writeLogSelf(self):
        """*Generates json string containing dict to be written to log file*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |    logJson, log in json string format
        """
        return json.dumps(self.__dict__)
    
    @abstractmethod
    def loadLogSelf(self,jsonString):
        """*loads json log back into dict*
        
        | *Parameters* 
        |   jsonString, json string to be loaded back in
        
        | *Returns*
        |    none
        """
        self.__dict__ = json.loads(jsonString)