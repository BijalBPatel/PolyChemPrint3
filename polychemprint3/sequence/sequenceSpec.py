# -*- coding: utf-8 -*-
"""
Specifies modular pre-written motion and dispense sequences for common prints.

| First created on Sun Oct 20 00:08:15 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""
import sys
sys.path.append("../../")
from abc import ABC, abstractmethod
from polychemprint3.utility.loggerSpec import loggerSpec


class sequenceSpec(loggerSpec, ABC):
    """Abstract Base Class for predefined print sequences."""

    ################### Construct/Destruct METHODS ###########################
    @abstractmethod
    def __init__(self, axes, tool, verbose, **kwargs):
        """*Initializes sequence object*.

        Parameters
        ----------
        axes: PCP_Axes object
            Axes object to send motion commands to
        tool: PCP_Tool
            Tool object to send dispense commands to
        verbose: bool
            level of detail to be printed to cmd line
        """
        self.axes = axes
        self.tool = tool
        self.verbose = verbose
        super().__init__(self.name, **kwargs)

    ################### Parameter Methods ###########################
    def stringParams(self):
        """*Turns paramList into a formatted string*.

        Returns
        -------
        String
            Formatted String containing table of param and current values
        """
        outString = ""
        for param in self.paramList:
            outString += "\t%-40s|  %-25s\n" % (self.name, self.value)

    ################### Sequence Actions ###################################
    @abstractmethod
    def operateSeq(self):
        """*Performs print sequence*.

        Returns
        -------
        bool
            Whether sequence successfully completed or not
        """
        pass

    ####################### Logging METHODS ###############################
    @abstractmethod
    def writeLogSelf(self):
        """*Generates json string containing dict to be written to log file*.

        Returns
        -------
        String
            log in json string format
        """
        return super().writeLogSelf()

    @abstractmethod
    def loadLogSelf(self, jsonString):
        """*loads json log back into dict*.

        Parameters
        ----------
        jsonString: String
            json string to be loaded back in

        """
        super().loadLogSelf(jsonString)


class seqParam():
    """Base Class for parameters used in sequences."""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, name, value, unit, helpString):
        """*Initializes parameter object*.

        Parameters
        ----------
        name: String
            name of parameter (e.g., length)
        value
            value of parameter (e.g., 20)
        unit
            unit value is measured in (e.g., mm)
        helpString: String
            Description of any limits/ bounds on the value (e.g., <30)
        """
        self.name = name
        self.value = value
        self.unit = unit
        self.helpString = helpString
