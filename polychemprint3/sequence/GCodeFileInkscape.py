# -*- coding: utf-8 -*-
"""
Parameterized code for reading in a gcode file and reprocessing for PCP3

| First created on 2020/05/14 18:16:00
| Revised: 2020/12/17
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
from tkfilebrowser import askopenfilenames

import logging


class GCodeFileInkscape(sequenceSpec):
    """Sequence template for importing GCODE motion commands and tool
    triggers into PCP Recipe framework

    """

    # Construct/Destruct Methods #############################################
    def __init__(self, axes: Axes3DSpec = nullAxes(),
                 tool: toolSpec = nullTool(), **kwargs):
        """*Initializes GCodeFile object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec.Axes3DSpec
            The set of axes that commands will be sent to.
        tool: toolSpec.toolSpec
            The tool that commands will be sent to.
        """
        # Get current Date
        dateStr = str(datetime.date(datetime.now()))
        currentDate = dateStr[-5:-3] + '\\' + dateStr[-2:] + '\\' + dateStr[:4]

        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "GCodeFileInkscape", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "Imported from GCodeFile", "", ""),
            "creationDate": seqParam("Creation Date",
                                     currentDate, "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Advanced", "", ""),
            "filePath": seqParam("GCodeFilePath", "PathUnset", "",
                                 "Full File Path to target GCode File"),
            "feedRate": seqParam("Printing Speed", "60", "mm/min",
                                 ""),
            "trvRate": seqParam("Travel Speed", "61", "mm/min",
                                ""),
            "zRate": seqParam("Z Movement Speed", "62", "mm/min",
                              ""),
            "Zhop": seqParam("Z hop height", "2", "mm",
                             ""),
            "Ton": seqParam("Tool on Value", "5", "",
                            "Tool value when dispensing"),
            "Toff": seqParam("Tool off Value", "5", "",
                             "Tool value when not dispensing"),
            "Ttrv": seqParam("Tool travel Value", "5", "",
                             "Tool value during travel moves"),
        }

        # Pass values to parent
        super().__init__(axes, tool, self.dictParams, **kwargs)

    # Unique Methods  ########################################################

    def importFromGFile(self):
        """Attempts to read line by line from GcodeFile at GCodeFilePath
        and return the read lines as a list.

        Returns
        -------
        bool
            True if read from file without an error.
        list of str
            A list containing each line read in as a separate str element.
        """
        try:
            GFilePath = self.dictParams.get("filePath").value
            print("GFP:" + GFilePath)
            GFile = fileHandler(fullFilePath=GFilePath)
            while not GFile.testFileIO('r'):
                print("\tError opening file... retry selecting GCodeFile:")
                tkWindow = tk.Tk()
                GFilePath = askopenfilenames(parent=tkWindow, initialdir='/',
                                             initialfile='tmp',
                                             filetypes=[("GCode Files",
                                                         "*.gcode|*.txt"),
                                                        ("All files", "*")])[0]
                self.dictParams.get("filePath").value = str(GFilePath)
                GFile.fullFilePath = str(GFilePath)
            return GFile.readFullFile()
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)

    def processGCode(self, GLines):
        """Parses each line in Glines to remove unusable commands and
        reconstitutes motion, feed strings with the rates the user provides
        in the CLI.

        Returns
        -------
        procGlines: list of str
            A list of GCode lines processed to remove garbage and include
            user-specified feeds, z height.

        """
        try:
            # First strip lines that we don't need to read in from GCode File
            cleanGlines = []
            garbageFlags = ["%", "(", "M"]  # Comments etc.
            for line in GLines:
                if line == "":
                    pass
                elif line[0] in garbageFlags:
                    pass
                else:
                    cleanGlines.append(line)
            # Now parse GCode into blocks and substitute user provided
            # values where possible
            procGLines = []
            for line in cleanGlines:
                # Break line into blocks
                blocks = re.split('[ (]', line)
                direct = ["X", "Y", "I", "J", "K"]
                cmdStr = ""  # G etc cmd
                motionStr = ""  # XYZIJK
                feedStr = ""  # F

                # pull values to substitute in from the sequence's dictionary.
                Zheight = str(self.dictParams.get("Zhop").value)
                printSpd = str(self.dictParams.get("feedRate").value)
                zSpd = str(self.dictParams.get("zRate").value)
                trvSpd = str(self.dictParams.get("trvRate").value)

                # Go through each block and substitute in user-provided
                # values for speeds, zheight
                for block in blocks:
                    if block == "":
                        pass
                    # motion string in the XY plane
                    elif block[0] in direct:
                        motionStr = motionStr + block + " "
                    # motion string in Z, eligible for # substitution
                    elif block[0] == "Z":
                        if block.__contains__("Z3"):
                            # i.e. a raised (non-printing) step.
                            motionStr = motionStr + "Z" + Zheight + " "
                        else:  # Should be Z0 for printing step
                            motionStr = motionStr + block + " "
                    elif block[0] == "G":  # Cmd string
                        if block[0:3] == "G00":  # Travel Move
                            cmdStr = cmdStr + block + " "
                            feedStr = "F" + trvSpd + " "
                        else:
                            cmdStr = cmdStr + block + " "
                    elif block[0] == "F":  # Feed string
                        if block.__contains__("F9999"):
                            feedStr = feedStr + "F" + printSpd + " "
                        elif block.__contains__("F9998"):
                            feedStr = feedStr + "F" + zSpd + " "
                        else:  # Should never happen
                            feedStr = feedStr + "F" + printSpd + " "
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
        """Augments procGlines with tool on/off/trv values based on the z-carriage height.

        Returns
        -------
        fullLines: list of str
            The combined list of Gcode and tool commands.
        """
        Zheight = str(self.dictParams.get("Zhop").value)
        toolOnValue = self.dictParams.get("Ton").value
        tooltrvValue = self.dictParams.get("Ttrv").value
        toolOffValue = self.dictParams.get("Toff").value
        try:
            fullLines = []  # This list will include tool commands.
            lastZval = "Z0"
            for line in procGlines:
                if line.__contains__("Z" + Zheight):  # Line is at Z > 0
                    zVal = Zheight
                elif line.__contains__("Z0"):  # Line is for Z = 0
                    zVal = "Z0"
                else:  # Shouldn't ever get here
                    zVal = lastZval
                if zVal == Zheight and lastZval == "Z0":  # This is a raise/travel move
                    fullLines.append(
                        "tool.setValue(" + str(tooltrvValue) + ")")
                    fullLines.append(line)
                elif zVal == "Z0" and lastZval == Zheight:  # This is a lower/ print move
                    fullLines.append(line)
                    fullLines.append("tool.setValue(" + str(toolOnValue) + ")")
                else:  # Shouldn't ever get here
                    fullLines.append(line)
                lastZval = zVal  # Tell the next loop where the Z axis stopped
            # At the end of all commands, set the tool to the off value
            fullLines.append("tool.setValue(" + str(toolOffValue) + ")")
            return fullLines
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    # sequenceSpec Methods ############################################################################################

    def genSequence(self):
        """*Loads print sequence into a list into cmdList attribute*.

        Returns
        -------
        bool
            Whether successfully reached the end or not.
        """

        self.cmdList = []
        cmds = self.cmdList
        toolOffValue = self.dictParams.get("Ttrv").value

        try:
            print("\t\tAttempting to read GCode File into RAM...")
            [readStatus, GLines] = self.importFromGFile()
            if readStatus:
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

                        # Pre-Sequence #######################################
                        # Set to absolute positioning mode and set current position as 0,0,0
                        cmds.append("axes.setPosMode(\"absolute\")")
                        cmds.append("axes.setPosZero()")
                        # Engage tool at off pressure
                        cmds.append("tool.setValue(" + str(toolOffValue) + ")")
                        cmds.append("tool.engage()")
                        # Main Sequence ######################################
                        for line in fullGlines:
                            if line.__contains__("tool"):
                                cmds.append(line)
                            else:
                                cmdStr = "axes.move(\"" + line + "\\n\")"
                                cmds.append(cmdStr)

                        # Post-Sequence #####################################
                        cmds.append("tool.disengage()")
                        cmds.append(
                            "axes.setPosMode(\"relative\")")  # Add line to return to relative positioning
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

    # loggerSpec METHODS ##############################################################################################

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
