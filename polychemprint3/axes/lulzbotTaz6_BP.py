# -*- coding: utf-8 -*-
"""
Implements axes3DSpec for lulzbot taz 6 with modified firmware.

| First created on Sat Oct 19 20:39:58 2019
| Revised: 23/10/2019 14:06:59
| Author: Bijal Patel

"""
import serial
import time
from colorama import Fore, Style
from polychemprint3.utility.serialDeviceSpec import serialDeviceSpec
from polychemprint3.axes.axes3DSpec import Axes3DSpec
import logging
import textwrap


class lulzbotTaz6_BP(serialDeviceSpec, Axes3DSpec):
    """Implemented interface for Lulzbot Taz 6 with BP modified firmware."""

    def __init__(self,
                 name='LulzbotTaz6',
                 posMode='relative',
                 devAddress="/dev/ttyACM0",
                 baudRate=115200,
                 commsTimeOut=0.01,
                 __verbose__=1,
                 firmwareVers='BP'):
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
        firmwareVers: String
            version of marlin firmware to validate against in handshake
            unique to this implementation to make sure
            people use modified firmware
        __verbose__: bool
            whether details should be printed to cmd line
        posMode: String
            Current active positioning mode, relative or absolute
        """
        self.firmwareVers = firmwareVers
        kwargs = {'name': name,
                  'posMode': posMode,
                  'devAddress': devAddress,
                  'baudRate': baudRate,
                  'commsTimeOut': commsTimeOut,
                  '__verbose__': __verbose__}
        super().__init__(**kwargs)

    #########################################################################
    # Axes3DSpecMethods
    #########################################################################
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
        print("\t\t" + message)
        if status == 1:
            # Try initial handshake
            [hshake, hmessage] = self.handShakeSerial()
            print("\t\t" + hmessage)
            if hshake == 1:
                passed = True

        return passed

    def deactivate(self):
        """*Closes communication and returns status bool*.

        Returns
        -------
        bool
            True if closed succesfully
            False if failed
        """
        passed = False
        # Stop Serial Device
        [status, message] = self.stopSerial()
        print("\t\t\t" + message)
        if status == 1:
            passed = True

        return passed

    def setPosMode(self, newPosMode):
        """*Sets positioning mode to relative or absolute*.

        Parameters
        ----------
        newPosMode: String
            Positioning mode to use for future move cmds
        """
        try:
            if newPosMode == 'relative':
                self.writeReady("G91\n")
                self.posMode = newPosMode
            elif newPosMode == 'absolute':
                self.writeReady("G90\n")
                self.posMode = newPosMode
            else:
                print("Error setting position mode to axes")

        except Exception as inst:
            logging.exception(inst)
            print("Error setting position mode to axes")

    def move(self, gcodeString):
        """*Moves axes by set amount*.

        Parameters
        ----------
        gCodeString: String
            Motion command in terms of Gcode G0/G1/G2/G3 supported

        | *Returns*
        |   none
        """
        self.writeReady(gcodeString)

    def sendCmd(self, command):
        """*Writes command to axes device when ready*.

        Parameters
        ----------
        command: String
            to write to axes

        Returns
        -------
        String
            Response from axes
        """
        return self.writeReady(command)

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
        return self.writeReady(command)

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
        self.writeReady('M114\n')
        m114Call = self.waitReady()
        m114Split = m114Call.split(' ')
        x = m114Split[0][2:]
        y = m114Split[1][2:]
        return [x, y]

    def setPosZero(self):
        """*Sets current axes position to absolute (0,0,0)*.
                """
        self.writeReady('G92 X0 Y0 Z0\n')
    #########################################################################
    # SerialDevice Methods
    #########################################################################
    def startSerial(self):
        """*Creates pySerial device*.

        Returns
        -------
        [1, "Serial Device Started successfully"]
            started succesfully
        [-1, 'Failed Creating pySerial...']
            could not start
        """
        if self.checkIfSerialConnectParamsSet():
            # Try to connect, catch errors and return to user
            try:
                self.ser = serial.Serial(port=self.devAddress,
                                         baudrate=self.baudRate,
                                         timeout=0.5)

                # Use ser for read/write

                # Clear initial garbage text in output buffer
                self.ser.reset_output_buffer()
                i = 1
                while i < 10:
                    time.sleep(1)
                    print("\t\t\t(%d/10) Waiting for Printer to initialize..."
                          % i)
                    i += 1
                print("\t\tInitial Read from Taz6: ")
                # keep reading until empty
                self.readTime()
                return [1, "Serial Device Started successfully"]
            except Exception as inst:
                return [-1, 'Failed Creating pySerial... ' + inst.__str__()]

        else:  # Not all params were set
            return [0, 'Not all connection parameters set']

    def stopSerial(self):
        """*Closes serial devices*.

        Returns
        -------
        [1, "Terminated successfully"]
            started succesfully
        [-1, "Error: Serial Device could not be stopped + error text"]
        """
        try:
            self.ser.close()
            self.sReader.close()
            return [1, "Terminated successfully"]
        except Exception:
            return [-1, "Error: Serial Device could not be stopped"]

    def handShakeSerial(self):
        """*Perform communications handshake with serial device*.

        Returns
        -------
        [1, "Handshake Successful"]
            success occured
        [0, 'Handshake Failed, Rcvd + message received']
            failure occured
        [-1, "Error: Handshake with Tool Failed + error text"]
            Error received
        """
        try:
            readInput = self.sendCmd("M115\n")
            wrongVers = self.firmwareVers not in readInput
            if wrongVers:
                return [-1, 'Hanshake Failed: Wrong Firmware Version']
            else:
                return [1, 'Handshake Success']
        except Exception as inst:
            logging.exception(inst)
            return [-1, 'Error on Handshake: ' + inst.__str__()]

    def __writeSerial__(self, command):
        """*Writes text to serial device*.

        Parameters
        ----------
        text: String
            message to send

        Returns
        -------
        [1, 'Text Sent + text']
            succesfull 2-way communication
        [-1, 'Write Failed + Error']
            Exception caught
        """
        try:
            self.ser.write(command.encode('utf-8'))
            if self.__verbose__:
                print('\t\t\tCommand Sent:> ' + command.rstrip())
            return [1, 'Command Sent' + command]
        except Exception as inst:
            return [-1, 'Error on Write: ' + inst.__str__()]
            print("writerror")

    def readTime(self):
        """*Reads in from serial device until timeout*.

        Returns
        -------
        String
            All text read in, empty string if nothing
        """
        inp = ''  # input string
        ins = ''  # read in
        tEnd = time.time() + self.commsTimeOut

        # Reads input until timeout
        while time.time() < tEnd:
            print(Fore.LIGHTYELLOW_EX
                  + "\t\t\tWaiting on taz..." + Style.RESET_ALL)
            ins = self.ser.readline().decode('utf-8').rstrip()
            if ins != "":
                if self.__verbose__:
                    print(textwrap.fill("Rcvd:< " + ins, width=60,
                                        initial_indent='\t\t\t',
                                        subsequent_indent='\t\t\t'))
                inp += ins
                tEnd += self.commsTimeOut
        return inp

    #########################################################################
    # Unique Methods
    #########################################################################
    def waitReady(self):
        """*Looks for "ok" in input, waits indefinitely*.

        Returns
        -------
        String
            All text read in, empty string if nothing
        """
        notReady = True
        i = 0  # loop increments0
        allIn = ""
        while notReady:
            inp = self.readTime()  # read buffer
            if 'ok' in inp:
                notReady = False
            else:
                if i % 10 == 0 and self.__verbose__:
                    print(Fore.LIGHTYELLOW_EX
                          + "\t\t\tWaiting for Axes to acknowledge "
                          + "last command")
            allIn += inp
        return allIn

    def writeReady(self, command):
        """*Sends command only after rece0iving ok message*.

        | *Parameters*
        |   command, string to write to axes

        | *Returns*
        |   inp, String read in
        """
        self.__writeSerial__(command)
        imp = self.waitReady()
        return imp
