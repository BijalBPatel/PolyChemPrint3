# -*- coding: utf-8 -*-
"""
The *Axes3D* class contains all data and methods related to controlling 3D printer axes

| First created on Sat Oct 19 20:39:58 2019
| Revised: 23/10/2019 14:06:59
| Author: Bijal Patel
  
Attributes
----------------
    :name: axes name [printer name]
    :devAddress: location of device on local system
    :firmwareVers: Firmware meant to be used with [for special GCode cmds]
    
Methods
----------------
    :param: args
    :param: args
        
"""
import serial
import io

from time import time
from PCP_SerialDevice import PCP_SerialDevice

class Axes3D(PCP_SerialDevice):
    def __init__(self, devAddress="unset",firmwareVers="unset", baudRate="unset", commsTimeOut=0.5, verbose =0):
        """*Initializes Axes3D object*
        
        | *Parameters* All default to "unset"
        |   devAddress - device address on this computer
        |   firmwareVers - version of the firmware loaded on the printer
        |   baudRate - baud rate
        |   commsTimeOut - how long to wait for serial device
        |   verbose - whether details should be printed to cmd line
        
        | *Returns*
        |   none 
        """
        self.devAddress = devAddress
        self.firmwareVers = firmwareVers
        self.baudRate = baudRate
        self.verbose = verbose
        self.commsTimeOut = commsTimeOut
    
    def checkIfConnectParamsSet(self):
        """*Goes through connection parameters and sees if all are set*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   True if all parameters are set, false if any unset 
        """
        connectParam = [self.devAddress,self.firmwareVers,self.baudRate]
        return 'unset' not in connectParam
           
        
        
    def connectToAxesHardware(self):
        """*Attempts to connect to Hardware and send an initial handshake*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, [list of read lines] if succesfully able to connect and handshake
        |   [0, 'Not all connection param set'] if not all connection param set
        |   [-1, 'Failed Creating pySerial'] if failed creating pyserial device
        |   [-2, 'Failed Handshake'] if handshake failed
        """
        
        if self.checkIfConnectParamsSet():
            #Try to connect, catch errors and return to user
            try:
                self.ser = serial.Serial(port = self.devAddress,\
                                         baudrate = self.baudRate,\
                                         bytesize = serial.EIGHTBITS,\
                                         parity = serial.PARITY_NONE,\
                                         stopbits = serial.STOPBITS_ONE,\
                                         timeout = 1,\
                                         xonxoff = False,\
                                         rtscts = False,\
                                         dsrdtr = False,\
                                         writeTimeout = 2
                                         )
                #Use ser for writing
                #Use sReader for buffered read
                
                self.sReader = io.TextIOWrapper(io.BufferedReader(self.ser))
                
                #Clear initial garbage text in output buffer
                self.ser.reset_output_buffer()
                
                time.sleep(0.25) 
                lineIn = self.sReader.readlines();
                linesIn = [lineIn]
                
                #keep reading until empty
                while lineIn != []:
                    time.sleep(0.25)    
                    lineIn = self.sReader.readlines();
                    linesIn.extend(lineIn)                    
                
            except Exception as inst:
                return [-1, 'Failed Creating pySerial... ' + inst.__str__]
            
        else: #Not all params were set
            return [0, 'Not all connection parameters set']
            
        #Try initial handshake
        handShakeResponse = self.handShake()
        if (handShakeResponse[0]==1):
            return [1,linesIn]
        else:
            return [-2,handShakeResponse[1]]        
        
    def handShake(self):
        """*Attempts to 'handshake' with printer* - see if correct firmware version returned
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   [1, 'Handshake Success'] if succesfull 2-way communication
        |   [0, 'Handshake Failed, Received: + message received'] if unexpected input received
        |   [-1, 'Handshake failed, Error: + errortext] if exception raised or not correct firmware vers
        """
        try:
            self.ser.write(b"M115\n")
            readInput = self.sReader.readlines()
            print(readInput);
            wrongVers = (-1 == readInput[0].find(self.firmwareVers))
            if (wrongVers):
                return [-1,'Wrong Firmware Version DO NOT CONTINUE']
            else:
                return [1, 'Handshake Success']
        except Exception as inst:
            return [-1, 'Error on Handshake: ' + inst.__str__]
        
       
    def write(self,command):
        """*Writes command to serial device*
        
        | *Parameters* 
        |   command, the string to send
        
        | *Returns*
        |   [1, 'Command Sent + command'] if succesfull 2-way communication
        |   [0, 'Write Failed + Error'] if exception caught
        """
        try:
            self.ser.write(command)
            if (self.verbose):
                print('\tCommand Sent: ' + command)
            return [1,'Command Sent' + command]
        except Exception as inst:
            return [-1, 'Error on Handshake: ' + inst.__str__]
    
    def readTime(self):
        """*Reads in from serial device until timeout*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   inp String of all text read in, empty string if nothing
        """
        inp = '' #input string
        ins = '' #read in
        tEnd = time() + self.commsTimeOut
	
        #Reads input until timeout
        while (time() < tEnd):
            ins = self.ser.read();
            if (ins != ""):
                inp += ins;
                
        inp = inp.strip #removes any newlines
        if self.verbose:
            print('\tReceived    : ' + inp + '\n'); 
        return (inp);

        
    def waitReady(self):
        """*Checks if taz is ready to receive new command by Looking for "ok" in input*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |   inp, String read in while waiting
        """
        notReady = True
        i = 0 #loop increments
        while (notReady):
            inp = self.readTime() #read buffer
            if (i%10==0 and self.verbose):
                print('\tWaiting for axes... ... ...\n')
            if ('ok' in inp):
                notReady = False
        return inp
        
    def writeReady(self,command):
        """*Writes when ready*
        
        | *Parameters* 
        |   command, string to write to axes
        
        | *Returns*
        |   none
        """
        self.write(command)
        self.waitReady()

    
    def getAbsPosXY(self):
        """*Gets the current position (absolute) from taz and returns XYZ coordinates*
        
        | *Parameters* 
        |   command, string to write to axes
        
        | *Returns*
        |   [X, Y] X and Y positions as strings
        """
    
        self.writeReady('M114\n')
        m114Call = self.waitReady()
        m114Split = m114Call.split(' ')
        x = m114Split[0][2:]
        y = m114Split[1][2:]
        return[x,y]
        
    def goToABSXY(self,xAbs,yAbs):
        """*Moves carriage to provided absolute X,Y coordinates*
        
        returns to relative positioning at end
        
        | *Parameters* 
        |   xAbs, absolute x position to go to
        |   yAbs, absolute y position to go to
        
        | *Returns*
        |    none
        """
        self.writeReady('G90\n') #set abs positioning
        #Move rapidly to target position
        self.writeReady('G1 F2000 X' + xAbs + ' Y' + yAbs + '\n')
        self.writeReady('G91\n') #return to relative positioning
        
    def stop(self):
        """*Closes serial devices*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |    none
        """
        self.ser.close()
        self.sReader.close()
        
    def writeLogSelf(self):
        """*Generates json string containing dict to be written to log file*
        
        | *Parameters* 
        |   none
        
        | *Returns*
        |    logJson, log in json string format
        """
        return json.dumps(self.__dict__)
    
    def loadLogSelf(self,jsonString):
        """*loads json log back into dict*
        
        | *Parameters* 
        |   logJson, json string to be loaded back in
        
        | *Returns*
        |    none
        """
        self.__dict__ = json.loads(jsonString)
        