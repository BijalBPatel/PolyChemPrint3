# -*- coding: utf-8 -*-
"""
Specifies 3D Axes classes, implementations are for specific printers/stages.

| First created on Sat Oct 19 20:39:58 2019
| Revised: 23/10/2019 14:06:59
| Author: Bijal Patel

"""

from abc import ABC, abstractmethod
from polychemprint3.utility.loggerSpec import loggerSpec


class Axes3DSpec(loggerSpec, ABC):
    """Abstract Base Class for 3D Axes."""

    @abstractmethod
    def __init__(self, name, __verbose__=0, posMode='absolute', **kwargs):
        """*Initializes Axes3D object*.

        Parameters
        ----------
        name: String
            name of axes3D device
        __verbose__: bool
            level of detail to be printed to cmd line
        posMode: String
            Current active positioning mode, relative or absolute
        """
        self.name = name
        self.posMode = posMode
        self.__verbose__ = __verbose__
        super().__init__(**kwargs)

    @abstractmethod
    def activate(self):
        """*Makes required connections and returns status bool*.

        Returns
        -------
        bool
            True if ready to use
            False if not ready
        """
        pass

    @abstractmethod
    def deactivate(self):
        """*Closes communication and returns status bool*.

        Returns
        -------
        bool
            True if ready to use
            False if not ready
        """
        pass

    @abstractmethod
    def setPosMode(self, newPosMode):
        """*Sets positioning mode to relative or absolute*.

        Parameters
        ----------
        newPosMode: String
            Positioning mode to use for future move cmds
        """

    @abstractmethod
    def move(self, gcodeString):
        """*Moves to the specified gcodeString position*.

        Parameters
        ----------
        gCodeString: String
            Motion command in terms of Gcode G0/G1/G2/G3 supported
        """
        pass

    @abstractmethod
    def sendCmd(self, command):
        """*Writes command to axes device when ready*.

        Parameters
        ----------
        command: String
            to write to axes
        """
        pass

    @abstractmethod
    def poll(self, command):
        """*Sends message to axes and returns response*.

        Parameters
        ----------
        command: String
            to write to axes

        Return
        ------
        String
            Response from axes
        """
        pass

    @abstractmethod
    def getAbsPosXY(self):
        """*Gets the current position (absolute) and return XY positions*.

        Parameters
        ----------
        command: String
            Gcode to write to axes

        Returns
        -------
        String
            [X, Y] X and Y positions as strings
        """
        pass

    @abstractmethod
    def setPosZero(self):
        """*Sets the current position (absolute) to (0,0,0)*.
        """
        pass