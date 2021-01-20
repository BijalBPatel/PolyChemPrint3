# -*- coding: utf-8 -*-
"""
Specifies modular pre-written motion and dispense sequences for common prints.

| First created on Sun Oct 20 00:08:15 2019
| Revised (dd/mm/yyyy): 01/18/2021 - BP
| Author: Bijal Patel

"""
import logging
import time
from abc import ABC, abstractmethod
from polychemprint3.axes.axes3DSpec import Axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.utility.loggerSpec import loggerSpec
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes


class sequenceSpec(loggerSpec, ABC):
    """Abstract Base Class for predefined print sequences."""

    # Construct/Destruct METHODS #############################################
    @abstractmethod
    def __init__(self, axes: Axes3DSpec = nullAxes(),
                 tool: toolSpec = nullTool(), dictParams: dict = None,
                 __verbose__: bool = 0, **kwargs):
        """*Initializes sequence object*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        dictParams: dict
        __verbose__: bool
        kwargs
        """

        # Pass in active axes/tool
        self.axes = axes
        self.tool = tool

        # Provide default values to dictParams if initialized without
        if dictParams is None:
            dictParams = {"name": seqParam("Sequence Name", "default",
                                           "default", "default"),
                          "description": seqParam("Sequence description",
                                                  "default", "default",
                                                  "default"),
                          "owner": seqParam("PCP_Default", "default",
                                            "default", "default"),
                          }

        self.dictParams = dictParams
        self.verbose = __verbose__
        # Unwrap parameter to get just the string name and description
        self.cmdList = []
        super().__init__(**kwargs)

    # Parameter Methods ######################################################
    def updateParams(self):
        pass

    # Sequence Actions ######################################################
    def operateSeq(self, **kwargs):
        """*Performs print sequence*.
        Returns
        -------
        bool
            Whether sequence successfully completed or not
        """
        axes = self.axes
        tool = self.tool

        try:
            for line in self.cmdList:
                eval(line)
            return True

        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    @abstractmethod
    def genSequence(self):
        """*Loads print sequence into a list into cmdList attribute*.

        Returns
        -------
        bool
            whether successfully reached the end or not
        """
        pass

    # Logging METHODS #######################################################
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


class seqParam:
    """Base Class for parameters used in sequences."""

    # Construct/Destruct METHODS #############################################
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
