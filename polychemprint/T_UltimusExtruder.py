"""
The *T_UltimusExtruder* Class implements the Tool base class to handle 
control of a Nordson EFD Ultimus V Extruder

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

from PCP_Tool import PCP_Tool
from PCP_SerialDevice import PCP_SerialDevice
import serial
from time import time

class T_UltimusExtruder(PCP_SerialDevice, PCP_Tool):
##############################################################################
###################### Construct/Destruct METHODS ############################
##############################################################################
    def __init__(self,name="unset", devAddress="unset", baudRate="unset", 
                 commsTimeOut=0.5, verbose=0,**kwargs):
        """*Initializes T_UltimusExtruder Object*
        | *Parameters* All default to "unset"
        |   name, String - tool name
        |   devAddress - device address on this computer
        |   baudRate - baud rate
        |   commsTimeOut - how long to wait for serial device before timeout on reads
        |   verbose - whether details should be printed to cmd line 
        
        | *Returns*
        |   none 
        """
        super().__init__(name=name, devAddress=devAddress,baudRate=baudRate,
             commsTimeOut=commsTimeOut, verbose=verbose, **kwargs)

    
    def stop(self):
        """*Turns off Tool object and terminates communication*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Terminated successfully"]
        |   [-1, "Error: Tool could not be stopped + error text"]
        """
        pass

##############################################################################
######################### PCP_TOOL METHODS ###################################
##############################################################################           
    def handshakeTool(self):
        """*Perform communications handshake with Tool*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Handshake Successful"]
        |   [-1, "Error: Handshake with Tool Failed + error text"]
        """
        pass
    
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
    
    
############################# Activate METHODS ############################### 
    
    def engage(self):
        """*Activate tool (dispense/LASER on, etc)*
        | *Parameters* 
        |   none
    
        | *Returns*
        |   [1, "Tool Engaged"]
        |   [-1, "Error: Tool could not be engaged"]
        """
        pass

   
    def disengage(self) :
        """*Deactivates tool (stops dispense/LASER off, etc)*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Tool Disengaged"]
        |   [-1, "Error: Tool could not be disengaged"]
        """
        pass
    
   
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
        
############################################################################## 
######################## PCP_SerialDevice METHODS ############################
##############################################################################
        
    def stopSerial(self):
        """*Terminates communication*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Terminated successfully"]
        |   [-1, "Error: Tool could not be stopped + error text"]
        """
        pass
    
     
    def handshakeSerial(self):
        """*Perform communications handshake with Tool*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Handshake Successful"]
        |   [0, 'Handshake Failed, Received: + message received'] if unexpected input received
        |   [-1, "Error: Handshake with Tool Failed + error text"]
        """
        pass      
       
    def write(self,command):
        """*Writes command to serial device*
        
        | *Parameters* 
        |   command, the string to send
        
        | *Returns*
        |   [1, 'Command Sent + command'] if succesfull 2-way communication
        |   [0, 'Write Failed + Error'] if exception caught
        """
        
        pass
    
    def readTime(self):
        """*Reads in from serial device until timeout*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   inp String of all text read in, empty string if nothing
        """
        pass

        
    def waitReady(self):
        """*Checks if taz is ready to receive new command by 
        Looking for "ok" in input*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, inp] String read in while waiting if successful
        |   [-1, "WaitReady Failed + Error"] if error
        """
        pass
        
    def writeReady(self,command):
        """*Writes when ready*
        
        | *Parameters* 
        |   command, string to write to axes
        
        | *Returns*
        |   [1, "String written"] If success
        |   [-1, "writeReady Failed + Error"] if error
        """
        pass
        
    
##############################################################################
########################## PCP_BasicLogger METHODS ########################### 
##############################################################################
    
    def writeLogSelf(self):
        """*Generates json string containing dict to be written to log file*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |    logJson, log in json string format
        """
        return super().writeLogSelf()
    
    
    def loadLogSelf(self,jsonString):
        """*loads json log back into dict*
        
        | *Parameters* 
        |   jsonString, json string to be loaded back in
        
        | *Returns*
        |    none
        """
        super().loadLogSelf(jsonString)
 
########################## Unique METHODS #################################### 
        