# -*- coding: utf-8 -*-
"""
Parameterized code for reading in a gcode file for 3D printing and reprocessing for PCP3

| First created on 05/14/2020 18:16:00
| Revised: 11/11/21
| Author: Bijal Patel

"""
import re
from datetime import datetime
from polychemprint3.utility.fileHandler import fileHandler
from polychemprint3.axes.axes3DSpec import Axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkfilebrowser import askopendirname, askopenfilenames, asksaveasfilename

import logging


class GCodeFile3DSlicer(sequenceSpec):
    """Sequence template for importing 3D GCODE motion commands and tool
    triggers into PCP Recipe framework"""

    # CONSTRUCT/DESTRUCT METHODS ###
    def __init__(self, axes: Axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """Initializes GCodeFile object with parameters for this sequence.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """
        # Get current Date

        dateStr = str(datetime.date(datetime.now()))
        currentDate = dateStr[-5:-3] + '\\' + dateStr[-2:] + '\\' + dateStr[:4]

        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "GCodeFile3DSlicer", "", ""),
            "description": seqParam("Sequence Description",
                                    "Adapts 3D GCode with triggered dispense", "", ""),
            "creationDate": seqParam("Creation Date",
                                     currentDate, "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Advanced", "", "default: PCP_Core"),
            "filePath": seqParam("GCodeFilePath", "PathUnset", "",
                                 "Full File Path to target GCode File"),
            "Ton": seqParam("Tool on Value", "5", "", "Tool value when dispensing"),
            "Toff": seqParam("Tool off Value", "0", "",
                             "Tool value when not dispensing"),
            "Ttrv": seqParam("Tool travel Value", "0", "",
                             "Tool value during travel moves"),
        }

        # Pass values to parent
        super().__init__(axes, tool, self.dictParams, **kwargs)

    # UNIQUE METHODS ###

    def importFromGFile(self):
        """Attempts to read line by line from GcodeFile at GCodeFilePath into memory"""
        try:
            GFilePath = self.dictParams.get("filePath").value
            print("GFP:" + GFilePath)
            GFile = fileHandler(fullFilePath=GFilePath)
            while not GFile.testFileIO('r'):
                print("\tError opening file... retry selecting GCodeFile:")
                tkWindow = tk.Tk()
                GFilePath = askopenfilenames(parent=tkWindow, initialdir='/', initialfile='tmp',
                                             filetypes=[("GCode Files", "*.gcode|*.txt"), ("All files", "*")])[0]
                self.dictParams.get("filePath").value = str(GFilePath)
                GFile.fullFilePath = str(GFilePath)

            # At this point we have a working file

            [readStatus, readList] = GFile.readFullFile()
            if readStatus:
                return readList
            else:
                print("Error reading from file")
                return False
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    def processGCode(self, GLines):
        """Attempts to filter line by line from GLines to remove garbage and substitute values"""
        try:
            cleanGlines = []
            garbageFlags = ["%", "(", "M", ";"]
            for line in GLines:
                if line == "":
                    pass
                elif line[0] in garbageFlags:
                    pass
                else:
                    cleanGlines.append(line)
            procGLines = []
            for line in cleanGlines:
                # Break line into blocks
                blocks = re.split('[ (]', line)

                direct = ["X", "Y", "Z", "I", "J", "K"]

                cmdStr = ""  # G etc cmd
                motionStr = ""  # XYZIJK
                feedStr = ""  # F

                for block in blocks:
                    if block == "":
                        pass
                    elif block[0] in direct:  # motion string
                        motionStr = motionStr + block + " "
                    elif block[0] == "G":  # Cmd string
                        cmdStr = cmdStr + block + " "
                    elif block[0] == "F":  # Feed string
                        feedStr = feedStr + block + " "
                    else:
                        pass  # Throw away anything else
                # Reconstruct String
                procGLines.append(cmdStr + feedStr + motionStr)
            return procGLines

        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    def insertToolCode(self, procGlines):
        toolOnValue = self.dictParams.get("Ton").value
        tooltrvValue = self.dictParams.get("Toff").value
        toolOffValue = self.dictParams.get("Ttrv").value
        try:
            fullLines = []
            lastGval = "G1"
            for line in procGlines:
                #print(line)
                if line.__contains__("G1"):
                    gVal = "G1"
                elif line.__contains__("G0"):
                    gVal = "G0"
                else:
                    gVal = lastGval
                #print("Current GVal: " + gVal + ", Last GVal: " + lastGval)
                # if currently on travel move, and last was extrude move
                if gVal == "G0" and lastGval == "G1":
                    fullLines.append("tool.setValue(" + str(tooltrvValue) + ")")
                    fullLines.append(line)
                    #print("Flag")
                # if currently on extrude move and last was travel move
                elif gVal == "G1" and lastGval == "G0":
                    fullLines.append("tool.setValue(" + str(toolOnValue) + ")")
                    fullLines.append(line)
                else:
                    fullLines.append(line)
                lastGval = gVal
            fullLines.append("tool.setValue(" + str(toolOffValue) + ")")
            return fullLines
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    # SEQUENCE METHODS ###

    def genSequence(self):
        """*Loads print sequence into a list into cmdList attribute*.

        Returns
        -------
        bool
            whether successfully reached the end or not
        """

        # pull tool off value
        toolOffValue = self.dictParams.get("Ttrv").value

        self.cmdList = []
        cmds = self.cmdList
        try:
            print("\t\tAttempting to read GCode File into RAM...")
            GLines = self.importFromGFile()
            if GLines:
                print("\t\tGCode File read into RAM successfully!")
                print("\t\tAttempting to parse GCode and convert to Python...")
                filteredGLines = self.processGCode(GLines)
                if filteredGLines:
                    print("\t\tGCode Parsed Successfully!")
                    print("\t\tAdding Tool On/Off/Travel commands...")
                    fullGlines = self.insertToolCode(filteredGLines)
                    if fullGlines:
                        print("\t\tTool Commands added successfully!")
                        print("\t\tLoading Python Commands!")

                        # Pre-Sequence
                        # Add line for abs positioning
                        cmds.append("axes.setPosMode(\"absolute\")")
                        cmds.append("tool.setValue(" + str(toolOffValue) + ")")
                        cmds.append("tool.engage()")

                        for line in fullGlines:
                            if line.__contains__("tool"):
                                cmds.append(line)
                            else:
                                cmdStr = "axes.move(\"" + line + "\")"
                                cmds.append(cmdStr)

                        # Post-Sequence
                        cmds.append("tool.disengage()")
                        cmds.append("axes.setPosMode(\"relative\")")  # Add line to return to relative positioning

                        #print(*cmds, sep = "\n")

                        print("\t\tLoading complete!")
                        return True

            return False

        except KeyboardInterrupt:
            print("\tgenSequence Terminated by User....")
            return False
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    # LOGGING METHODS ###

    def writeLogSelf(self):
        """*Generates log string containing dict to be written to log file*.

        Returns
        -------
        String
            log in string format
        """
        return super().writeLogSelf()

    def loadLogSelf(self, logString):
        """*loads log back into dict*.

        Parameters
        ----------
        logString: String
            log string to be loaded back in

        """
        super().loadLogSelf(logString)
