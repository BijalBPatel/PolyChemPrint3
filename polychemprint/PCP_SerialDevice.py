# -*- coding: utf-8 -*-
"""
The *PCP_SerialDevice* Abstract Base Class specifies the interface for all 
Serial Device objects that PCP will use (extruders/lasers/etc)

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
------------
    :param test: args
    :param test: args

Outputs
---------
    :None: Everything output to terminal window, no return value

"""
from abc import ABC, abstractmethod

class PCP_SerialDevice(ABC):
################### Construct/Destruct METHODS ###########################
    def __init__(self, devAddress, baudRate, commsTimeOut, verbose,**kwargs):
        """*Initializes Tool Object*
        | *Parameters* 
        |   name, String - tool name
        
        | *Returns*
        |   none 
        """
        #self.name = name
        self.devAddress = devAddress
        self.baudRate = baudRate
        self.commsTimeOut = commsTimeOut
        self.verbose = verbose
        super().__init__(**kwargs)
        
        
    
    @abstractmethod
    def stopSerial(self):
        """*Terminates communication*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Terminated successfully"]
        |   [-1, "Error: Tool could not be stopped + error text"]
        """
        pass
    
####################### Communication METHODS ###############################        
    @abstractmethod
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
       
    @abstractmethod
    def write(self,command):
        """*Writes command to serial device*
        
        | *Parameters* 
        |   command, the string to send
        
        | *Returns*
        |   [1, 'Command Sent + command'] if succesfull 2-way communication
        |   [0, 'Write Failed + Error'] if exception caught
        """
        pass
    
    @abstractmethod
    def readTime(self):
        """*Reads in from serial device until timeout*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   inp String of all text read in, empty string if nothing
        """
        pass

    @abstractmethod   
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
    
    @abstractmethod   
    def writeReady(self,command):
        """*Writes when ready*
        
        | *Parameters* 
        |   command, string to write to axes
        
        | *Returns*
        |   [1, "String written"] If success
        |   [-1, "writeReady Failed + Error"] if error
        """
        pass