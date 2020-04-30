"""
Implements the Tool base class for a null Tool [no action, returns true].

| First created on 13/11/2019 13:33:28
| Revised: 13/11/2019 13:33:28
| Author: Bijal Patel

"""

##############################################################################
##################### Imports
##############################################################################

from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.utility.serialDeviceSpec import serialDeviceSpec


class nullTool(toolSpec, serialDeviceSpec):
    """Implements the Tool base class for a null Tool (no action)."""

    ###########################################################################
    ### Construct/Destruct METHODS
    ###########################################################################
    def __init__(self,
                 name="nullTool",
                 units="null",
                 devAddress="unset",
                 baudRate="unset",
                 commsTimeOut=0.5,
                 __verbose__=0,
                 **kwargs):
        """*Initializes T_UltimusExtruder Object*.

        Parameters
        ----------
        name: String
            tool name
        units: String
            units for value
        devAddress: Strong
            device address on this computer
        baudRate: int
            baud rate
        commsTimeOut: int
            how long to wait for serial device before timeout on reads
        verbose: bool
            whether details should be printed to cmd line
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
    ### toolSpec METHODS
    ##########################################################################

    def activate(self):
        """*Makes required connections and returns status bool*.

        Returns
        -------
        bool
            True if ready to use
            False if not ready
        """
        print("\t\tNull Tool Activated")
        return True

    def deactivate(self):
        """*Closes communication and returns status bool*.

        Returns
        -------
        bool
            True if ready to use
            False if not ready
        """
        print("\t\tNull Tool Deactivated")
        return True

    ############################# Activate METHODS ###########################
    def engage(self):
        """*Toggles Dispense on*.

        Returns
        -------
        [1, "Dispense On"]
        [0, "Error: Dispense Already On"]
        [-1, 'Failed engaging dispense ' + inst.__str__()]
        """
        try:
            if self.dispenseStatus == 0:
                self.dispenseStatus = 1
                print("\t\tNull Tool Dispense On")
                return [1, "Dispense On"]

            else:
                print("\t\tNull Tool Error: Dispense already On")
                return [0, "Error: Dispense Already On"]
        except Exception as inst:
            return [-1, 'Failed engaging dispense ' + inst.__str__()]

    def disengage(self):
        """*Toggles Dispense off*.

        Returns
        -------
        [1, "Dispense Off"]
        [0, "Error: Dispense already off"]
        [-1, 'Failed engaging dispense ' + inst.__str__()]
        """
        try:
            if self.dispenseStatus == 1:
                self.dispenseStatus = 0
                print("\t\tNull Tool Dispense Off")
                return [1, "Dispense Off"]

            else:
                print("\t\tNull Tool Error: Dispense already Off")
                return [0, "Error: Dispense already off"]
        except Exception as inst:
            return [-1, 'Failed disengaging dispense ' + inst.__str__()]

    ############################# Value METHODS ###########################

    def setValue(self, newVal):
        """*Set Value*.

        Parameters
        ----------
        pressureVal: String
            New value to set

        Returns
        -------
        [output of writeSerialCommand]
        [-1, "Error: Pressure could not be set for Extruder + error text"]
        """
        try:
            print("\t\tNull Tool Value set: " + str(newVal))
            return [1, 'null mode: newVal Set']
        except Exception as inst:
            print("\t\tNull Tool Error: Value not Set")
            return [-1, "Error: value could not be set"
                    + inst.__str__()]

    def getState(self):
        """*Returns active state of tool*.

        | *Parameters*
        |   none

        | *Returns*
        |   [1, "Tool On"]
        |   [0, "Tool Off"]
        |   [-1, "Error: Tool activation state cannot be determined + Error]
        """
        try:
            if self.dispenseStatus():
                print("\t\tNull Tool Dispense On")
                return [1, "Tool On"]
            else:
                print("\t\tNull Tool Dispense Off")
                return [0, "Tool Off"]
        except Exception as inst:
            return [-1, "Error: Tool activation state cannot be determined"
                    + inst.__str__()]

    ##########################################################################
    ### PCP_SerialDevice METHODS
    ##########################################################################

    def checkIfSerialConnectParamsSet(self):
        """*Goes through connection parameters and sees if all are set*.

        Returns
        -------
        bool
            True
        """
        return True

    def startSerial(self):
        """*Creates and connects pySerial device*.

        Returns
        -------
        [1, "Connected Succesfully to Serial Device"]
        """
        return [1, "Connected Succesfully to Serial Device"]

    def stopSerial(self):
        """*Terminates communication*.

        Returns
        -------
        [1, "Terminated successfully"]
        """
        return [1, "Terminated successfully"]

    ################### Communication METHODS ###############################

    def handShakeSerial(self):
        """*Perform communications handshake with Tool*.

        Returns
        -------
        [1, "Handshake Successful"]
        """
        return [1, "Handshake Successful"]

    def __writeSerial__(self, text):
        """*Writes text to serial device*.

        Parameters
        ----------
        text: String
            message to send

        Returns
        -------
        [1, 'Text Sent + text']
        """
        print("\tNull Tool Write:" + text)
        return [1, 'Text Sent + text']

    def writeSerialCommand(self, cmdString):
        """*Writes dlcommand to serial device*.

        Parameters
        ----------
        cmdString, String
            the string to send

        Returns
        -------
        [1, 'Command Sent: ' + cmdString + 'Received: ' + rcvd]
            if exception
        """
        print("\tNull Tool Write:" + cmdString)
        return [1, 'Command Sent: ' + cmdString + '\n Received: '
                + "Null tool - no receive"]

    def readTime(self):
        """*Reads in from serial device until timeout*.

        Returns
        -------
        [1, inp String of all text read in, empty string if nothing]
        """
        print('\tReceived from Serial Device: ' + 'Null device input')

##############################################################################
########################## PCP_BasicLogger METHODS ###########################
##############################################################################

    def writeLogSelf(self):
        """*Generates json string containing dict to be written to log file*.

        Returns
        -------
        logJson: String
            log in json string format
        """
        return super().writeLogSelf()

    def loadLogSelf(self, jsonString):
        """*loads json log back into dict*.

        Parameters
        ----------
        jsonString: String
            json string to be loaded back in
        """
        super().loadLogSelf(jsonString)
