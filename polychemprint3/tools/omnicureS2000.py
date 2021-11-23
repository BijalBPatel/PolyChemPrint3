"""
Implements the Tool base class for Excelitas/Lumen Dynamics Omnicure S2000.

| First created on 211122
| Revised:
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
import crcmod.predefined


class omnicureS2000(serialDeviceSpec, toolSpec):
    """Implements the toolSpec abstract base class for the Excelitas/Lumen Dynamics Omnicure S2000."""

    ### CONSTRUCT/DESTRUCT METHODS

    def __init__(self,
                 name="T_OmnicureS2000",
                 units="percent",
                 devAddress="/dev/ttyUSB0",
                 baudRate=19200,
                 commsTimeOut=0.1,
                 __verbose__=1,
                 **kwargs):
        """*Initializes Omnicure S2000 Object*.

        Parameters
        ----------
        name: String
            tool name
        units: String
            units for value
        devAddress: String
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
        print("\t\t\t" + "Activating Omnicure S2000.")

        # Start Serial Device
        [status, message] = self.startSerial()
        print("\t\t\t" + message)

        if status == 1:
            # Try initial handshake several times
            tryCounter = 1
            notDone = True
            while (tryCounter < 3 and notDone):
                status, message = self.handShakeSerial()
                print("\t\t\t" + message)
                if status == 1:
                    passed = True
                    notDone = False
                    print("\t\t\t" + "Omnicure S2000 Activated Successfully!")
                else:
                    tryCounter += 1
                    print("\t\t\t" + "Omnicure S2000 Failed to Activate!")
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
        print("\t\t\t" + "Deactivating Omnicure S2000.")

        if self.dispenseStatus == 1:
            print("\t\t\t" + "!!!UV Shutter is detected as OPEN. For safety, shutter will be closed before disconnecting.")
            self.disengage()

        # Send disconnect command to Omnicure
        status, message = self.writeSerialCommand("DCON")
        if "CLOSE" in message:
            closeStatus = 1
        else:
            closeStatus = 0

        # Stop Serial Device
        [status, message] = self.stopSerial()
        if status & closeStatus == 1:
            passed = True

        if passed == 1:
            print("\t\t\t" + "Omnicure S2000 Deactivated Successfully!")
        else:
            print("\t\t\t" + "Omnicure S2000 Failed to Deactivate!")
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
                self.writeSerialCommand("OPN")
                self.dispenseStatus = 1
                return [1, "UV Shutter Opened."]

            else:
                return [0, "Warning: UV Shutter should already be on."]
        except Exception as inst:
            return [-1, 'Failed engaging UV Shutter ' + inst.__str__()]

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
                self.writeSerialCommand("CLS")
                self.dispenseStatus = 0
                return [1, "UV Shutter Closed."]

            else:
                self.writeSerialCommand("CLS")
                return [0, "Warning: UV Shutter should already be off."]
        except Exception as inst:
            return [-1, 'Failed disengaging UV Shutter ' + inst.__str__()]


    def setValue(self, intVal):
        """Set the Omnicure Output Intensity

        Parameters
        ----------
        intVal: String
            The new value of the output iris opening/level/irradiance as a string.
            Conversion to specific format occurs internally.

        Returns
        -------
        status : two-element list
            First element (int) indicates whether value setting was successful (1) or error (-1).\n
            Second element provides text explanation.
        """
        print("\t\tSetting Value for Omnicure...")
        try:
            errText = ""
            # 1 for iris opening %, 2 for level-set mode, 3 for irradiance mode
            operatingMode = 1

            intVal = intVal.rstrip()
            setSuccess = False

            if operatingMode == 1: # uncalibrated iris mode
                # Force to nearest integer
                if intVal.isdigit():
                    intVal = int(intVal)
                else:
                    print("\t\t\t!!!Rounding intensity value to nearest integer")
                    intVal = round(float(intVal))

                # Manual says 0 < val <= 100, needs to be integer
                if intVal == 0:
                    intVal = 1
                    print("\t\t\tSetpoint too low, reset to minimum value of 1")
                elif intVal > 100:
                    intVal = 100
                    print("\t\t\tSetpoint too high, reset to maximum value of 100")
                else:
                    pass
                [writeStatus, response] = self.writeSerialCommand("SIL" + str(intVal))
                if "Received" in response:
                    setSuccess = True

            elif operatingMode == 2: # level set mode
                [writeStatus, response] = self.writeSerialCommand("SPW" + str(intVal))
                if "Received" in response:
                    setSuccess = True
            elif operatingMode == 3: # irradiance mode
                [writeStatus, response] = self.writeSerialCommand("SIR" + str(intVal))
                if "Received" in response:
                    setSuccess = True
            else:
                print("Error in omnicureS2000 setValue code")

            if setSuccess == True:
                print("\t\tValue Set Successfully for OmnicureS2000!")
            else:
                print("Omnicure Value Set Error: " + repr(response))

        except Exception as inst:
            return [-1, "Error: Intensity could not be set for Extruder"
                    + inst.__str__()]


    def getState(self):
        """Returns active state of tool [software record only].

        Returns
        -------
            [1, "Tool On"]
            [0, "Tool Off"]
            [-1, "Error: Tool activation state cannot be determined + Error]
        """
        try:
            if self.dispenseStatus == 1:
                return [1, "Tool On"]
            else:
                return [0, "Tool Off"]
        except Exception as inst:
            return [-1, "Error: Tool activation state cannot be determined"
                    + inst.__str__()]

    ### PCP_SerialDevice METHODS

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
                                         writeTimeout=0.2
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
        """Terminates serial port.

        Returns
        -------
        [1, "Terminated successfully"]
        [-1, "Error: Tool could not be stopped + error text"]
        """
        try:
            print("\t\t\t\tClosing Tool Serial Port...")
            self.ser.close()
            print("\t\t\t\tClosed Tool Serial Port!")
            return [1, "Terminated successfully"]
        except Exception as inst:
            return [0, 'Error on closing Serial Device: ' + self.name
                    + ' : ' + inst.__str__()]

    ################### Communication METHODS ###############################

    def handShakeSerial(self):
        """Perform communications handshake with Tool.

        Returns
        -------
        [1, "Handshake Successful"]
        [0, 'Handshake Failed, Received: + message received']
            if unexpected input received
        [-1, "Error: Handshake with Tool Failed + error text"]
        """
        try:
            if self.__verbose__:
                print("\t\t\tAttempting handshake with Tool...")

            # send  CONN request and  read response
            readIn = self.writeSerialCommand("CONN")[1]

            # see if matches acknowledge
            if "READY" in readIn.upper():
                return [1, "Handshake Successful, Received Ready Response"]
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
                self.ser.write("\r".encode())
                print('\t\t\t\tCommand Sent to Omnicure: ' + repr(text))
                return [1, 'Command Sent' + text]
            except Exception as inst:
                print(inst.__str__())
                return [0, 'Error on write to Serial Device: '
                        + self.name + ' : ' + inst.__str__()]
        else:
            return [0, 'Error on write to Serial Device: '
                    + self.name + ' : ' + 'serial parameters unset']

    def writeSerialCommand(self, cmdString):
        """Writes packaged command to serial device and receives response [doesnt validate]

        Parameters
        ----------
        cmdString
            the string to send

        Returns
        -------
        [1, Received Text]
        [0, "Error sending cmd : " + self.name + ' : ' + Error']
            if exception
        """
        try:
            # package command string
            self.__writeSerial__(self.pack(cmdString))

            received = self.readTime(self.commsTimeOut)
            return [1, received[1]]

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
                ins = self.ser.readline().decode()
                if ins != "":
                    inp += ins
            #inp = inp.strip()  # removes any newlines

            if self.__verbose__:
                print('\t\t\t\tReceived from Serial Device ' + self.name
                      + ' : ' + repr(inp))
            return [1, inp]
        except Exception as inst:
            return [0, 'Error on read from Serial Device ' + self.name
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

    ### UNIQUE METHODS

    def calcCRC8Maxim(self, checkString):
        """Calculates the CRC-8 value using the MAXIM standard, expresses as hexadecimal, and returns as string of length 2.

        Parameters
        ----------
        checkString, string to compute CRC-8-Maxim value from

        Returns
        -------
        capitalized string of length 2 containing hexadecimal CRC8 Value
        """

        # Notes for figuring out this part
        # Omnicure manual has example C++ code for manual calculation
        # Instead, pulled two examples "CONN" -> 0x18, "READY" -> 0x0A
        # Use online calculator to figure out which CRC-8 Algorithm they implemented
        # https: // crccalc.com /
        # CRC-8/MAXIM gives correct values
        # Googled "CRC Python Packages" until I found one that implements CRC-8 MAXIM
        # http://crcmod.sourceforge.net/crcmod.predefined.html

        encodedString = checkString.encode()
        crc8_func = crcmod.predefined.mkCrcFun('crc-8-maxim')
        hexCRC8 = hex(crc8_func(encodedString))

        crc8String = str(hexCRC8)[2:].upper()
        if len(crc8String) < 2:
            crc8String = "0" + crc8String
        return crc8String

    def pack(self, cmdString):
        """Packages a command packet to send to the Omnicure S2000 over RS232
        Proper syntax of command packet: CommandString + CRC-8 + Newline

        Parameters
        ----------
        cmdString: String
            input command string as per Omnicure user manual section 16

        Returns
        -------
        String
            packaged command string to send to omnicure
        """

        # Calculate CRC-8 Value
        crc8String = self.calcCRC8Maxim(cmdString)

        # Compose output string and return
        outString = cmdString + crc8String
        return outString

    def unpack(self, packetIn):
        """Unpacks a command packet for cmd name and value*.

        Parameters
        ----------
        packetIn: String
            data packet from omnicure: String + CRC8 Value [1 byte] + newline char

        Returns
        -------
        dataString: response
            response text from omnicure
        """
        packetIn = packetIn.rstrip()  # remove any trailing/leading whitespace

        # Remove CRC8 Value without validating
        dataString = packetIn[:-2]

        # return string
        return dataString
