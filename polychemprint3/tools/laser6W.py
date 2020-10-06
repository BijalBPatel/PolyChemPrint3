# -*- coding: utf-8 -*-
"""
Implements the Tool base class for Danny's arduino-uno controlled 6W LASER.

| First created on Wed Feb 12 2020
| Revised: 12/02/2020
| Author: Bijal Patel

"""

from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.utility.serialDeviceSpec import serialDeviceSpec
import serial
import io
import time
import logging


class laser6W(serialDeviceSpec, toolSpec):
    """Implements the Tool base class for Danny's 6W LASER."""

    ### Construct/Destruct METHODS
    def __init__(self,
                 name="BlueLASER6W",
                 units="percent",
                 devAddress="/dev/ttyACM1",
                 baudRate=115200,
                 commsTimeOut=0.1,
                 __verbose__=1,
                 **kwargs):
        """*Initializes Tool Object*.

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

    def activate(self):
        """*Makes required connections and returns status bool*.

        Returns
        -------
        bool
            True if ready to use
            False if not ready
        """
        passed = False
        # Start Serial Device
        [status, message] = self.startSerial()
        print("\t\t\t")
        print(message)
        if status == 1:
            # Try initial handshake
            [status, message] = self.handShakeSerial()
            print("\t\t\t" + message)
            if status == 1:
                passed = True
            # Turn on Laser at minimum Power
            self.__writeSerial__("on\n")
            self.__writeSerial__("2" + '\n')
        return passed

    def deactivate(self):
        """*Closes communication and returns status bool*.

        Returns
        -------
        bool
            True if deactivated
            False if not deactivated
        """
        passed = False
        # Stop Serial Device
        [status, message] = self.stopSerial()
        self.__writeSerial__("off\n")
        print("\t\t\t" + message)
        if status == 1:
            passed = True

        return passed
        pass

    ### Dispensing
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
                self.__writeSerial__("2" + '\n')
                # Laser is always on now
                self.dispenseStatus = 1
                return [1, "Dispense On"]
            else:
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
                self.__writeSerial__("2" + '\n')
                self.dispenseStatus = 0
                return [1, "Dispense Off"]

            else:
                return [0, "Error: Dispense already off"]
        except Exception as inst:
            return [-1, 'Failed disengaging dispense ' + inst.__str__()]

    def setValue(self, value):
        """*Set Laser PWM value in percent 1-100*.

        Parameters
        ----------
        value: String
            New value of pressure out of 100

        Returns
        -------
        [output of writeSerialCommand]
        [-1, "Error: value could not be set for LASER + error text"]
        """
        try:
            return self.__writeSerial__(value + '\n')
        except Exception as inst:
            return [-1, "Error: Value could not be set for LASER"
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
            if self.dispenseStatus:
                return [1, "Tool On"]
            else:
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
            True if all parameters are set, false if any unset
        """
        connectParam = [self.devAddress, self.baudRate]
        return 'unset' not in connectParam

    def startSerial(self):
        """*Creates and connects pySerial device*.

        Returns
        -------
        [1, "Connected Succesfully to Serial Device"]
        [0, 'Not all connection parameters set']
        [-1, "Error: Could not connect to serial device: + error text"]
        """
        if self.checkIfSerialConnectParamsSet():
            # Try to connect, catch errors and return to user
            try:
                self.ser = serial.Serial(port=self.devAddress,
                                         baudrate=self.baudRate,
                                         bytesize=serial.EIGHTBITS,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         timeout=1,
                                         xonxoff=False,
                                         rtscts=False,
                                         dsrdtr=False,
                                         writeTimeout=2
                                         )
                # Use ser for writing
                # Use sReader for buffered read
                self.sReader = io.TextIOWrapper(io.BufferedReader(self.ser))

                # Clear initial garbage text in output buffer
                self.ser.reset_output_buffer()

                time.sleep(0.25)
                lineIn = self.sReader.readlines()
                linesIn = [lineIn]

                # keep reading until empty
                while lineIn:
                    time.sleep(0.25)
                    lineIn = self.sReader.readlines()
                    linesIn.append(lineIn)

            except Exception as inst:
                return [-1, 'Failed Creating pySerial... ' + inst.__str__()]

        else:  # Not all params were set
            return [0, 'Not all connection parameters set']

        # Try initial handshake
        handShakeResponse = self.handShakeSerial()
        if handShakeResponse[0] == 1:
            return [1, linesIn]
        else:
            return [-2, handShakeResponse[1]]

    def stopSerial(self):
        """*Terminates communication*.

        Returns
        -------
        [1, "Terminated successfully"]
        [-1, "Error: Tool could not be stopped + error text"]
        """
        try:
            self.ser.write(chr(4))  # End of transmission code
            print("Closing Laser...\n")
            time.sleep(3)
            self.ser.close()
            print("Closed Laser!\n")
            return [1, "Terminated successfully"]
        except Exception as inst:
            return [0, 'Error on closing Serial Device: ' + self.name
                    + ' : ' + inst.__str__()]

    ################### Communication METHODS ###############################

    def handShakeSerial(self):
        """*Perform communications handshake with Tool*.

        Returns
        -------
        [1, "Handshake Successful"]
        [0, 'Handshake Failed, Received: + message received']
            if unexpected input received
        [-1, "Error: Handshake with Tool Failed + error text"]
        """
        try:
            return [1, "No Handshake Function"]
        except Exception as inst:
            logging.exception(inst)
            return [-1, 'Error on handshake with Serial Device: '
                    + self.name + ' : ' + inst.__str__()]

    def __writeSerial__(self, text):
        """*Writes text to serial device*.

        Parameters
        ----------
        text: String
            message to send

        Returns
        -------
        [1, 'Text Sent + text'] if successful 2-way communication
        [0, 'Write Failed + Error'] if exception caught
        """
        if self.checkIfSerialConnectParamsSet() == 1:
            try:
                self.ser.write(text.encode('utf-8'))
                if self.__verbose__:
                    print('\tCommand Sent to LASER: ' + text)
                return [1, 'Command Sent' + text]
            except Exception as inst:
                return [0, 'Error on write to Serial Device: '
                        + self.name + ' : ' + inst.__str__()]
        else:
            return [0, 'Error on write to Serial Device: '
                    + self.name + ' : ' + 'serial parameters unset']

    def readTime(self):
        """*Reads in from serial device until timeout*.

        Returns
        -------
        [1, inp String of all text read in, empty string if nothing]
        [0, 'Read failed + Error' if exception caught]
        """
        inp = ''  # input string
        ins = ''  # read in
        tEnd = time.time() + self.commsTimeOut

        try:  # Reads input until timeout
            while time.time() < tEnd:
                ins = self.ser.readline().decode('utf-8').rstrip()
                if ins != "":
                    inp += ins
            inp = inp.strip  # removes any newlines

            if self.__verbose__:
                print('\tReceived from Serial Device: ' + self.name
                      + ' : ' + str(inp) + '\n')
            return inp
        except Exception as inst:
            return [0, 'Error on read from Serial Device: ' + self.name
                    + ' : ' + inst.__str__()]

    ##########################################################################
    ### PCP_BasicLogger METHODS
    ##########################################################################

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
