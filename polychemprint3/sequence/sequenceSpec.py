# -*- coding: utf-8 -*-
"""
Specifies modular pre-written motion and dispense sequences for common prints.

| First created on Sun Oct 20 00:08:15 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""
from abc import ABC, abstractmethod
from polychemprint3.utility.loggerSpec import loggerSpec


class sequenceSpec(loggerSpec, ABC):
    """Abstract Base Class for predefined print sequences."""

    ################### Construct/Destruct METHODS ###########################
    @abstractmethod
    def __init__(self, dictParams=None, __verbose__=0, **kwargs):
        """*Initializes sequence object*.

        Parameters
        ----------
        dictParams: dict
        __verbose__: bool
        kwargs
        axes: PCP_Axes object
            Axes object to send motion commands to
        tool: PCP_Tool
            Tool object to send dispense commands to
        verbose: bool
            level of detail to be printed to cmd line
        """
        # Provide default values to dictParams if initialized without

        if dictParams is None:
            dictParams = {"name": seqParam("Sequence Name", "default", "default", "default"),
                          "description": seqParam("Sequence description", "default", "default", "default"), }
        self.dictParams = dictParams
        self.verbose = __verbose__
        # Unwrap parameter to get just the string name and description
        self.nameString = self.dictParams.get("name").value
        self.descriptString = self.dictParams.get("description").value

        super().__init__(**kwargs)

    ################### Parameter Methods ###########################

    ################### Sequence Actions ###################################
    @abstractmethod
    def operateSeq(self, tool, axes):
        """*Performs print sequence*.

        Parameters
        ----------
        tool: PCP_ToolSpec object
            tool to execute code with
        axes: PCP_Axes object
            axes to execute code with

        Returns
        -------
        bool
            Whether sequence successfully completed or not
        """
        pass

    @abstractmethod
    def genSequence(self, tool, axes):
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


class seqParam:
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
