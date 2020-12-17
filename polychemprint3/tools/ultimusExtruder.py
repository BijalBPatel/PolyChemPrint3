"""
Implements the Tool base class for Nordson EFD Ultimus V Extruder.

| First created on Sun Oct 20 00:03:21 2019
| Revised: 10/17/20
| Author: Bijal Patel

"""

##############################################################################
# Imports
##############################################################################
import numpy as np

from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.utility.serialDeviceSpec import serialDeviceSpec
import serial
import io
import time
import logging


class ultimusExtruder(serialDeviceSpec, toolSpec):
    """Implements the toolSpec abstract base class for the Nordson EFD Ultimus V Extruder."""

    ###########################################################################
    ### Construct/Destruct METHODS
    ###########################################################################
    def __init__(self,
                 name="T_UltimusExtruder",
                 units="kPa",
                 devAddress="/dev/ttyS0",
                 baudRate=115200,
                 commsTimeOut=0.1,
                 __verbose__=1,
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
    # PCP.tools.toolSpec methods
    ##########################################################################

    def activate(self):
        """To be called in main.py to load as active tool. Makes required serial connections and returns status as
               True/False.

               Returns
               -------
               bool
                   True if tool serial connection made and tool is ready to use
                   False if error generated and tool is not ready for use
        """
        passed = False
        print("\t\t\t" + "Activating Ultimus Extruder.")

        # Start Serial Device
        [status, message] = self.startSerial()
        print("\t\t\t" + message)

        if status == 1:
            # Try initial handshake
            status, message = self.handShakeSerial()
            print("\t\t\t" + message)
            if status == 1:
                passed = True
            print("\t\t\t" + "Ultimus Extruder Activated Successfully!")
        else:
            print("\t\t\t" + "Ultimus Extruder Failed to Activate!")
        return passed

    def deactivate(self):
        """To be called in main.py to unload as active tool. Closes serial communication and returns status as
          True/False.

          Returns
          -------
          bool
              True if tool serial connection destroyed and tool is succesfully disabled.
              False if error generated and serial communication could not be suspended.
        """
        passed = False
        # Stop Serial Device
        [status, message] = self.stopSerial()
        print("\t\t\t" + message)
        if status == 1:
            passed = True
        return passed

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
                self.writeSerialCommand("DI")
                self.dispenseStatus = 1
                return [1, "Dispense turned on."]

            else:
                return [0, "Warning: Dispense should already be on."]
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
                self.writeSerialCommand("DI")
                self.dispenseStatus = 0
                return [1, "Dispense turned off."]

            else:
                return [0, "Warning: Dispense should already be off."]
        except Exception as inst:
            return [-1, 'Failed disengaging dispense ' + inst.__str__()]

    def setValue(self, pressureVal):
        """Set the extruder output pressure

        Parameters
        ----------
        pressureVal: String
            The new value of the pressure as a string, expressed at arbitrary precision/ without leading zeros.
            Conversion to hardware specific format occurs internally.
            e.g., (use 23.456 NOT 0234")

        Returns
        -------
        status : two-element list
            First element (int) indicates whether value setting was successful (1) or error (-1).\n
            Second element provides text explanation.
        """
        print("\t\tSetting Value for UltimusExtruder...")
        try:
            pressureVal = self.pressureRecode(pressureVal)
            return self.writeSerialCommand("PS  " + pressureVal)
        except Exception as inst:
            return [-1, "Error: Pressure could not be set for Extruder"
                    + inst.__str__()]
        print("\t\tValue Set Successfully for UltimusExtruder!")

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
            if self.dispenseStatus == 1:
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
        [1, "Connected Successfully to Serial Device"]
        [0, 'Not all connection parameters set']
        [-1, "Error: Could not connect to serial device: + error text"]
        """
        if not self.checkIfSerialConnectParamsSet():
            return [0, 'Not all connection parameters set']
        else:
            # Try to connect, catch errors and return to user
            try:
                self.ser = serial.Serial(port=self.devAddress,
                                         baudrate=self.baudRate,
                                         bytesize=serial.EIGHTBITS,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         timeout=0,
                                         xonxoff=False,
                                         rtscts=False,
                                         dsrdtr=False,
                                         writeTimeout=2
                                         )
                portstatus = self.ser.isOpen()
                return [1, "\tInstantiated PySerial Object... port open = " + str(portstatus) + "."]

                # Use ser for writing
                # Use sReader for buffered read
                # sReader = io.TextIOWrapper(io.BufferedReader(self.ser))

                # Clear initial garbage text in output buffer
                # self.ser.reset_output_buffer()
                # time.sleep(0.25)

                # lineIn = sReader.readlines()
                # linesIn = [lineIn]

                # keep reading until empty
                # while lineIn != []:
                #    time.sleep(0.25)
                #    lineIn = sReader.readlines()
                #    linesIn.append(lineIn)

            except Exception as inst:
                return [-1, 'Failed Creating pySerial... ' + str(inst)]

    def stopSerial(self):
        """*Terminates communication*.

        Returns
        -------
        [1, "Terminated successfully"]
        [-1, "Error: Tool could not be stopped + error text"]
        """
        try:
            self.ser.write(chr(0x04).encode())  # End of transmission code
            print("\t\tClosing UltimusV...")
            time.sleep(3)
            self.ser.close()
            print("\t\tClosed UltimusV!\n")
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
            if self.__verbose__:
                print("\t\t\tAttempting handshake with UltimusV...")

            # send ENQ
            self.__writeSerial__(chr(0x05))

            # read response, see if matches acknowledge
            readIn = self.readTime(3)[1]
            if chr(6) in readIn:
                return [1, "Handshake Successful, Received ACK"]
            else:
                return [0, "Handshake Failed, Received: " + readIn]
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
        if self.checkIfSerialConnectParamsSet():
            try:
                self.ser.write(text.encode())
                print('\t\t\t\tCommand Sent to Extruder: ' + text)
                return [1, 'Command Sent' + text]
            except Exception as inst:
                return [0, 'Error on write to Serial Device: '
                        + self.name + ' : ' + inst.__str__()]
        else:
            return [0, 'Error on write to Serial Device: '
                    + self.name + ' : ' + 'serial parameters unset']

    def writeSerialCommand(self, cmdString):
        """*Writes dlcommand to serial device*.

        Parameters
        ----------
        cmdString
            the string to send

        Returns
        -------
        [1, 'Command Sent: ' + cmdString + 'Received: ' + rcvd]
        [0, "Error sending cmd : " + self.name + ' : ' + Error']
            if exception
        """
        try:
            # package command string
            self.__writeSerial__(chr(0x05))
            self.__writeSerial__(self.pack(cmdString))

            # receive A0 or A2
            received = self.readTime(self.commsTimeOut)[1]
            if "A2" in received:
                return [0, "Error sending command to Serial Device: "
                        + self.name + ' : ' + 'received A2']

            else:
                if "A0" in received:  # send ACK
                    self.__writeSerial__(chr(0x04))
                    return [1, 'Command Sent Successfully: ' + cmdString + '-> Received Confirmation: '
                            + received]
                else:
                    self.__writeSerial__(chr(0x04).encode())  # end transmission
                    return [0, "Unexpected return from Serial Device: "
                            + self.name + ' : ' + received]

        except Exception as inst:
            return [0, 'Error on sending command to Serial Device: '
                    + self.name + ' : ' + str(inst)]

    def readTime(self, timeout):
        """*Reads in from serial device until timeout*.

        Returns
        -------
        [1, inp String of all text read in, empty string if nothing]
        [0, 'Read failed + Error' if exception caught]
        """
        inp = ''  # full input string
        ins = ''  # read in during one time interval
        tEnd = time.time() + timeout

        try:  # Reads input until timeout
            while time.time() < tEnd:
                ins = self.ser.readline().decode().rstrip()
                if ins != "":
                    inp += ins
            inp = inp.strip()  # removes any newlines

            if self.__verbose__:
                print('\t\t\t\tReceived from Serial Device: ' + self.name
                      + ' : ' + inp)
            return [1, inp]
        except Exception as inst:
            return [0, 'Error on read from Serial Device: ' + self.name
                    + ' : ' + str(inst)]

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

    ##########################################################################
    ### Unique METHODS
    ##########################################################################
    def decToHex(self, num, bits):
        """*Converts number from decimal to 2s compliment hexadecimal*.

        Logic: subtract hex value from 0 and output least significant byte
        Parameters
        ----------
        num: int
            decimal number to convert
        bits: int
            number of bits [python int = 32 bits]

        Returns
        -------
        String
            number in 2s compliment hexadecimal
        """
        if num < 0:
            return hex((1 << bits) + num)
        else:
            return hex(num)

    def calc_checkSum(self, checkString):
        """*Calculates checksum and returns as string of length 2*.

        Logic: subtract hex value from 0 and output least significant byte
        | *Parameters*
        |   checkString, string to compute checksum from

        | *Returns*
        |    Capitalized hex string of length 2
        """
        checkTotal = 0
        for char in checkString:
            checkTotal -= int(hex(ord(char)), 16)
        # convert to hex string
        hexTotal = self.decToHex(checkTotal, 32).upper()
        return hexTotal[-2:]

    def pack(self, cmdString):
        """*Packages a command packet*.

        | Proper syntax of command packet: STX + DataString + Checksum + ETX
        | Datastring = NumBytes + CommandName + Command Data

        Parameters
        ----------
        cmdString: String
            input command string, first 4 char are cmdName, rest are data

        Returns
        -------
        String
            packaged command string to send to extruder
        """
        cmdName = cmdString[0:4]
        cmdData = cmdString[4:]

        # Create NumBytesField
        # hex number of format 0x# or 0x##
        nBytes = len(cmdName + cmdData)
        # convert to hex string remove 0x and add leading 0 if nBytes < 16
        if nBytes < 16:
            nBytes = hex(nBytes)[2:].upper()
            nBytes = '0' + nBytes
        else:
            nBytes = hex(nBytes)[2:].upper()

        # create Data string
        dataString = nBytes + cmdName + cmdData

        # Calculate Checksum
        checkSum = self.calc_checkSum(dataString)

        # Add Start/End transmission characters and return
        return chr(2) + dataString + checkSum + chr(3)

    def unpack(self, packetIn):
        """*Unpacks a command packet for cmd name and value*.

        Parameters
        ----------
        packetIn: String
            data packet from extruder - STX + DataString + Checksum + ETX

        Returns
        -------
        String: cmdName
            command name
        String: cmdVal
            command value [can be empty string]
        """
        packetIn = packetIn.rstrip()  # remove any trailing/leading whitespace

        # Remove STX, numBytes, remove Checksum,ETX
        dataString = packetIn[3, -3]

        # Pull cmd name from start of string
        cmdName = dataString[0:4]
        cmdVal = dataString[4:]

        # return strings
        return cmdName, cmdVal

    def pressureRecode(self, presStr):
        """Converts string from user-readible value to the 4 char format of the Ultimus Extruder.

        Parameters
        ----------
        presStr: String
            Pressure value to transmit as a string of arbitrary precision and length.

        Returns
        -------
        presRft :String
            Pressure value reformatted as 4 char sequence expected by Ultimus Extruder
        """

        # Convert input string to an int to remove any leading/trailing zeros
        presRft = float(presStr)

        # Round to tenths place, multiply by 10, and cast as int to remove trailing zero
        presRft = int(np.around(presRft, decimals=1) * 10)

        # Convert to string and pad with zeros if needed
        presRft = str(presRft)

        if len(presRft) > 4:
            return "0000"
        while len(presRft) < 4:
            presRft = "0" + presRft

        return presRft
