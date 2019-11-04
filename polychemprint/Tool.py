# -*- coding: utf-8 -*-
"""
The *Tool_TEMPLATE* class provides the skeleton of the implementation of the PCP_Tool Abstract Class

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

class Tool(ABC):
################### Construct/Destruct METHODS ###########################
    def __init__(self,name):
        """*Initializes Tool Object*
        | *Parameters* 
        |   name, String - tool name
        
        | *Returns*
        |   none 
        """
        self.name = name
        
        
    
    @abstractmethod
    def stop(self):
        """*Turns off Tool object and terminates communication*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Terminated successfully"]
        |   [-1, "Error: Tool could not be stopped + error text"]
        """
        pass
    
####################### Communication METHODS ###############################        
    @abstractmethod
    def handshake(self):
        """*Perform communications handshake with Tool*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Handshake Successful"]
        |   [-1, "Error: Handshake with Tool Failed + error text"]
        """
        pass
    
    @abstractmethod
    def setValue(self,param, value):
        """*Set Tool value of a specified Tool parameter*
        | *Parameters* 
        |   param - name of the parameter to set
        |   value - the new value of the parameter
        
        | *Returns*
        |   [1, "Value Set succesfully"]
        |   [-1, "Error: Parameter could not be set for Tool + error text"]
        """
        pass
    
    
####################### Activate METHODS ############################### 
    @abstractmethod
    def engage(self):
        """*Activate tool (dispense/LASER on, etc)*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Tool Engaged"]
        |   [-1, "Error: Tool could not be engaged"]
        """
        pass
    
    @abstractmethod
    def disengage(self) :
        """*Deactivates tool (stops dispense/LASER off, etc)*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Tool Disengaged"]
        |   [-1, "Error: Tool could not be disengaged"]
        """
        pass
    
    @abstractmethod
    def getState(self):
        """*Returns active state of tool*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Tool On"]
        |   [0, "Tool Off"]
        |   [-1, "Error: Tool activation state cannot be determined + Error]
        """
        pass
    
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
    

        