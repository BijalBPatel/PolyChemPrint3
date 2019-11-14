# -*- coding: utf-8 -*-
"""Interface for all Serial Device objects (extruders/lasers/axes/etc).

| First created on Sun Oct 20 00:03:21 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel
"""
import sys
sys.path.append("../../")
from abc import ABC, abstractmethod
import serial


class serialDeviceSpec(ABC):
    """Abstract Base Class for all objects using serial device."""

################### Construct/Destruct METHODS ###########################
    def __init__(self, devAddress, baudRate, commsTimeOut, verbose, **kwargs):
        """*Initializes Tool Object*.

        Parameters
        ----------
        name : String
            device name
        """
        self.devAddress = devAddress
        self.baudRate = baudRate
        self.commsTimeOut = commsTimeOut
        self.verbose = verbose
        self.ser = serial.Serial()
        super().__init__(**kwargs)

    @abstractmethod
    def checkIfSerialConnectParamsSet(self):
        """*Goes through connection parameters and sees if all are set*.

        Returns
        -------
        bool
            True if all parameters are set, false if any unset
        """
        connectParam = [self.devAddress, self.firmwareVers, self.baudRate]
        return 'unset' not in connectParam

    @abstractmethod
    def startSerial(self):
        """*Creates pySerial device*.

        Returns
        -------
        [1, "Terminated successfully"]
            started succesfully
        [-1, "Error: Tool could not be stopped + error text"]
            could not start
        """
        pass

    @abstractmethod
    def stopSerial(self):
        """*Terminates communication*.

        Returns
        -------
        [1, "Terminated successfully"]
            started succesfully
        [-1, "Error: Tool could not be stopped + error text"]
            could not start
        """
        pass

####################### Communication METHODS ###############################
    @abstractmethod
    def handShakeSerial(self):
        """*Perform communications handshake with Tool*.

        Returns
        -------
        [1, "Handshake Successful"]
            success occured
        [0, 'Handshake Failed, Rcvd + message received']
            failure occured
        [-1, "Error: Handshake with Tool Failed + error text"]
            Error received
        """
        pass

    @abstractmethod
    def __writeSerial__(self, text):
        """*Writes text to serial device*.

        Parameters
        ----------
        text: String
            message to send

        Returns
        -------
        [1, 'Text Sent + text']
            succesfull 2-way communication
        [-1, 'Write Failed + Error']
            Exception caught
        """
        pass

    @abstractmethod
    def readTime(self):
        """*Reads in from serial device until timeout*.

        Returns
        -------
        String
            All text read in, empty string if nothing
        """
        pass
