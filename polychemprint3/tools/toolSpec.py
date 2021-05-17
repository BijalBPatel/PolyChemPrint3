# -*- coding: utf-8 -*-
"""Contains toolSpec Abstract Base Class.

| First created on Sun Oct 20 00:03:21 2019
| Revised: 10/17/2020
| Author: Bijal Patel

"""

# Imports ####################################################################
from abc import ABC, abstractmethod
from polychemprint3.utility.loggerSpec import loggerSpec


class toolSpec(loggerSpec, ABC):
    """Abstract Base Class for all dispensing/writing tool drivers."""

    # Construct/Destruct Methods #############################################
    def __init__(self, name, units, __verbose__, **kwargs):
        """Initializes Tool Object.

        Parameters
        ----------
        name: String
            Name of tool.
        units: String
            Units of the primary active value for the tool. E.g, kPa, %, etc.
        """
        self.name = name
        self.units = units
        self.__verbose__ = __verbose__

        super().__init__(**kwargs)

    @abstractmethod
    def activate(self):
        """To be called in main.py to load as active tool. Makes required
        serial connections and returns status as True/False.

        Returns
        -------
        bool
            True if tool serial connection made and tool is ready to use
            False if error generated and tool is not ready for use
        """
        pass

    @abstractmethod
    def deactivate(self):
        """To be called in main.py to unload as active tool. Closes serial
        communication and returns status as True/False.

        Returns
        -------
        bool
            True if tool serial connection destroyed and tool disabled.
            False if error generated and serial communication not suspended.
        """
        pass

    # Tool Action (Dispensing) Methods #######################################
    @abstractmethod
    def engage(self):
        """Turn tool primary action on (dispense/LASER beam on, etc).

        Returns
        -------
        status : two-element list
            First element (int) indicates whether engage was successful (1),
            already on (0) or error (-1)
            Second element (String) provides text explanation.
        """
        pass

    @abstractmethod
    def disengage(self):
        """Turn tool primary action off (stops dispense/LASER beam off, etc).

        Returns
        -------
        status : two-element list
            First element (int) indicates whether disengage was successful (1),
            already off (0), or error (-1).
            Second element (String) provides text explanation.
        """
        pass

    @abstractmethod
    def setValue(self, value):
        """Set the primary tool action value (e.g., Laser power,
        extruder pressure, etc.).

        Parameters
        ----------
        value: String
            The new value of the parameter as a string, expressed at
            arbitrary precision/ without leading zeros.
            Conversion to hardware specific format occurs internally.
            e.g., (use 23.456 NOT 0234")

        Returns
        -------
        status : two-element list
            First element (int) indicates whether value setting
            was successful (1) or error (-1).
            Second element provides text explanation.
        """
        pass

    @abstractmethod
    def getState(self):
        """Returns the current dispense/action state (on/off).

        Returns
        -------
        status : two-element list
            First element indicates whether tool is on(1), off(0) or error(-1).
            Second element provides text explanation.
        """
        pass

    # Logging methods #########################################################
    @abstractmethod
    def writeLogSelf(self):
        """Generates yaml string containing __dict__ to be written to log file.

        Returns
        -------
        String
            log in yaml string format
        """
        return super().writeLogSelf()

    @abstractmethod
    def loadLogSelf(self, yamlString):
        """Loads yaml log back into __dict__.

        Parameters
        ----------
        yamlString: String
            yaml string to be loaded back in

        """
        super().loadLogSelf(yamlString)
