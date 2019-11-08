# -*- coding: utf-8 -*-
"""
The *PCP_SerialDevice* Abstract Base Class specifies the interface for all 
Serial Device objects that PCP will use (extruders/lasers/etc)

| First created on Sun Oct 20 00:03:21 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""
from abc import ABC, abstractmethod
import serial

class serialDeviceSpec(ABC):
################### Construct/Destruct METHODS ###########################
    def __init__(self, devAddress, baudRate, commsTimeOut, verbose, **kwargs):
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
        self.ser = serial.Serial()
        super().__init__(**kwargs)
     
    @abstractmethod
    def checkIfSerialConnectParamsSet(self):
        """*Goes through connection parameters and sees if all are set*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   True if all parameters are set, false if any unset 
        """
        connectParam = [self.devAddress,self.firmwareVers,self.baudRate]
        return 'unset' not in connectParam
        
    @abstractmethod
    def startSerial(self):
        """*Creates pySerial device*
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, "Terminated successfully"]
        |   [-1, "Error: Tool could not be stopped + error text"]
        """
        pass
    
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
    def handShakeSerial(self):
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
    def __writeSerial__(self,text):
        """*Writes text to serial device*
        
        | *Parameters* 
        |   text, the string to send
        
        | *Returns*
        |   [1, 'Text Sent + text'] if succesfull 2-way communication
        |   [0, 'Write Failed + Error'] if exception caught
        """
        pass
    
    @abstractmethod
    def writeSerialCommand(self,command):
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
