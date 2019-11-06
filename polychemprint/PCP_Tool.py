# -*- coding: utf-8 -*-
"""
The *PCP_Tool* Abstract Base Class specifies the interface for all Tool objects (extruders/lasers/etc)

| First created on Sun Oct 20 00:03:21 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""

from abc import ABC, abstractmethod
from PCP_BasicLogger import PCP_BasicLogger

class PCP_Tool(PCP_BasicLogger,ABC):
################### Construct/Destruct METHODS ###########################
    def __init__(self, name, **kwargs):
        """*Initializes Tool Object*
        | *Parameters* 
        |   name, String - tool name
        
        | *Returns*
        |   none 
        """
        self.name = name
        super().__init__(**kwargs)
            
############################# Activate ### ############################### 
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
    def setValue(self, value):
        """*Set Tool value of a specified Tool parameter*
        | *Parameters* 
        |   value - the new value of the parameter
        
        | *Returns*
        |   [1, "Value Set succesfully"]
        |   [-1, "Error: Parameter could not be set for Tool + error text"]
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
        return super().writeLogSelf()
    
    @abstractmethod
    def loadLogSelf(self,jsonString):
        """*loads json log back into dict*
        
        | *Parameters* 
        |   jsonString, json string to be loaded back in
        
        | *Returns*
        |    none
        """
        super().loadLogSelf(jsonString)
    

        