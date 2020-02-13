# -*- coding: utf-8 -*-
"""
Implements axes3DSpec as null axes (returns successful to all).

| First created on Sat Oct 19 20:39:58 2019
| Revised: 23/10/2019 14:06:59
| Author: Bijal Patel

"""

from polychemprint3.axes.axes3DSpec import Axes3DSpec
import logging


class nullAxes(Axes3DSpec):
    """Implementing axes3D for null case."""

    def __init__(self,
                 name='nullAxes',
                 posMode='relative',
                 __verbose__=0,):
        """*Initializes object with default params DOESNT ACTIVATE*.

        Parameters
        ----------
        name: String
            name of printer
        devAddress: String
            location of serial device for communication
        baudRate: String
            baudrate for serial communication
        commsTimeout: int
            how long to wait for serial device
        __verbose__: bool
            whether details should be printed to cmd line
        posMode: String
            Current active positioning mode, relative or absolute
        """
        kwargs = {'name': name,
                  'posMode': posMode,
                  '__verbose__': __verbose__}
        super().__init__(**kwargs)

    #########################################################################
    ### Axes3DSpecMethods
    #########################################################################
    def activate(self):
        """*Makes required connections and returns status bool*.

        Returns
        -------
        bool
            True if ready to use
            False if not ready
        """
        print("\t\tNull Axes Activated")
        return True

    def deactivate(self):
        """*Closes communication and returns status bool*.

        Returns
        -------
        bool
            True if closed succesfully
            False if failed
        """
        print("\t\tNull Axes Deactivated")
        return True

    def setPosMode(self, newPosMode):
        """*Sets positioning mode to relative or absolute*.

        Parameters
        ----------
        newPosMode: String
            Positioning mode to use for future move cmds
        """
        try:
            if newPosMode == 'relative':
                print("\t\tNull Axes in relative positioning mode")
                self.posMode = newPosMode
            elif newPosMode == 'absolute':
                print("\t\tNull Axes in absolute positioning mode")
                self.posMode = newPosMode
            else:
                print("Error setting position mode to axes")

        except Exception as inst:
            logging.exception(inst)
            print("Error setting position mode to axes")

    def move(self, gcodeString):
        """*Initializes Axes3D object*.

        Parameters
        ----------
        gCodeString: String
            Motion command in terms of Gcode G0/G1/G2/G3 supported

        | *Returns*
        |   none
        """
        print("\t\tNull Axes move Command: " + repr(gcodeString))
        pass

    def sendCmd(self, command):
        """*Writes command to axes device when ready*.

        Parameters
        ----------
        command: String
            to write to axes
        """
        print("\t\tNull Axes sent command: " + repr(command))
        pass

    def poll(self, command):
        """*Sends message to axes and parses response*.

        Parameters
        ----------
        command: String
            to write to axes

        Return
        ------
        String
            Response from axes
        """
        print("\t\tNull Axes returns nullResponse")
        return "nullresponse"

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
        print("\t\tNull Axes return null abs position")
        return["nullX", "nullY"]