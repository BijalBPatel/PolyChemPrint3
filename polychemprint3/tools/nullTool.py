"""
Implements the Tool base class for a null Tool [no action, returns true].

| First created on 13/11/2019 13:33:28
| Revised: 17/10/20
| Author: Bijal Patel

"""

##############################################################################
# Imports
##############################################################################

from polychemprint3.tools.toolSpec import toolSpec


class nullTool(toolSpec):
    """Implements the toolSpec abstract base class for a null tool, a virtual hardware device that only writes to the
    terminal."""

    ###########################################################################
    # Construct/Destruct Methods
    ###########################################################################
    def __init__(self,
                 name="nullTool",
                 units="null",
                 devAddress="unset",
                 baudRate="unset",
                 commsTimeOut=0.5,
                 __verbose__=0,
                 **kwargs):
        """*Initializes nullTool Object*.

        Parameters
        ----------
        name: String
            Name of the tool
        units: String
            Units of the primary active value for the tool. E.g, kPa, %, etc.
        devAddress: Strong
            Device address on this computer
        baudRate: int
            Baud rate
        commsTimeOut: int
            How long to wait for serial device before timeout on reads
        verbose: bool
            Whether details should be printed to cmd line
        """
        self.dispenseStatus = 0  # off
        inputs = {"name": name,
                  "units": units,
                  "devAddress": devAddress,
                  "baudRate": baudRate,
                  "commsTimeOut": commsTimeOut,
                  "__verbose__": __verbose__}
        kwargs.update(inputs)
        super().__init__(**kwargs)

    ##########################################################################
    # PCP.tools.toolSpec methods
    ##########################################################################

    # toolSpec construct/destruct methods
    def activate(self):
        """To be called in main.py to load as active tool. Makes required serial connections and returns status as
        True/False.

        Returns
        -------
        bool
            True if tool serial connection made and tool is ready to use
            False if error generated and tool is not ready for use
        """
        print("\t\tNull Tool Says: Activated")
        return True

    def deactivate(self):
        """To be called in main.py to unload as active tool. Closes serial communication and returns status as
        True/False.

        Returns
        -------
        bool
            True if tool serial connection destroyed and tool is succesfully disabled.
            False if error generated and serial communication could not be suspended.
        """
        print("\t\tNull Tool Says: Deactivated")
        return True

    # PCP.tools.toolSpec Tool Action (Dispensing) Methods
    def engage(self):
        """Turn tool primary action on (dispense/LASER beam on, etc).

        Returns
        -------
        status : two-element list
            First element (int) indicates whether engage was successful (1), already on (0) or error (-1)\n
            Second element (String) provides text explanation.
        """
        try:
            if self.dispenseStatus == 0:
                self.dispenseStatus = 1
                print("\t\tNull Tool Says: Tool dispense turned on.")
                return [1, "Dispense On"]

            else:
                print("\t\tNull Tool Says: Error - Dispense already On")
                return [0, "Warning: Tool status already set to active."]
        except Exception as inst:
            return [-1, 'Failed engaging dispense ' + inst.__str__()]

    def disengage(self):
        """Turn tool primary action off (stops dispense/LASER beam off, etc).

        Returns
        -------
        status : two-element list
            First element (int) indicates whether disengage was successful (1), already off (0), or error (-1).\n
            Second element (String) provides text explanation.
        """
        try:
            if self.dispenseStatus == 1:
                self.dispenseStatus = 0
                print("\t\tNull Tool Says: Tool dispense turned off")
                return [1, "Dispense Off"]

            else:
                print("\t\tNull Tool Says: Error - Dispense already off")
                return [0, "Error: Dispense already off"]
        except Exception as inst:
            return [-1, 'Failed disengaging dispense ' + inst.__str__()]

    def setValue(self, value):
        """Set the primary tool action value (e.g., Laser power, extruder pressure, etc.).

        Parameters
        ----------
        value: String
            The new value of the parameter as a string, expressed at arbitrary precision/ without leading zeros.
            Conversion to hardware specific format occurs internally.
            e.g., (use 23.456 NOT 0234")

        Returns
        -------
        status : two-element list
            First element (int) indicates whether value setting was successful (1) or error (-1).\n
            Second element provides text explanation.
        """
        try:
            print("\t\tNull Tool Says: Value set: " + str(value))
            return [1, 'null mode: newVal Set']
        except Exception as inst:
            print("\t\tNull Tool Says: Error - Value not Set")
            return [-1, "Error: value could not be set"
                    + inst.__str__()]

    def getState(self):
        """Returns the current dispense/action state (on/off).

        Returns
        -------
        status : two-element list
            First element indicates whether tool is on(1) or off(0) or error(-1).\n
            Second element provides text explanation.
        """
        try:
            if self.dispenseStatus:
                print("\t\tNull Tool Says: Dispense status is: On")
                return [1, "Tool On"]
            else:
                print("\t\tNull Tool Says: Dispense status is: Off")
                return [0, "Tool Off"]
        except Exception as inst:
            return [-1, "Error: Tool activation state cannot be determined"
                    + inst.__str__()]

##############################################################################
# PCP.utility.loggerSpec methods
##############################################################################

    def writeLogSelf(self):
        """*Generates yaml string containing dict to be written to log file*.

        Returns
        -------
        logyaml: String
            log in yaml string format
        """
        return super().writeLogSelf()

    def loadLogSelf(self, yamlString):
        """*loads json log back into dict*.

        Parameters
        ----------
        yamlString: String
            yaml string to be loaded back in
        """
        super().loadLogSelf(yamlString)
