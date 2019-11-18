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
    def __init__(self, nameString, descrip, axes, tool, verbose, **kwargs):
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
        self.nameString = nameString
        self.descrip = descrip
        self.axes = axes
        self.tool = tool
        self.verbose = verbose
        super().__init__(**kwargs)

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

    @abstractmethod
    def genSequence(self):
        """*Loads print sequence into a list into cmdList attribute*.

        Returns
        -------
        bool
            whether successfully reached the end or not
        """
        pass

    ####################### Logging METHODS ###############################
    @abstractmethod
    def writeLogSelf(self):
        """*Generates log string containing dict to be written to log file*.

        Returns
        -------
        String
            log in string format
        """
        return super().writeLogSelf()

    @abstractmethod
    def loadLogSelf(self, logString):
        """*loads log back into dict*.

        Parameters
        ----------
        logString: String
            log string to be loaded back in

        """
        super().loadLogSelf(logString)


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
