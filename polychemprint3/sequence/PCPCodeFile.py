# -*- coding: utf-8 -*-
"""
Parameterized code for reading and executing a PCPcode file [series of python lines]

| First created on 2021/11/23
| Revised:
| Author: Bijal Patel

"""
import re
from datetime import datetime
from polychemprint3.utility.fileHandler import fileHandler
from polychemprint3.axes.axes3DSpec import Axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.tools.nullTool2 import nullTool2
from polychemprint3.tools.nullTool3 import nullTool3
from polychemprint3.axes.nullAxes import nullAxes

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkfilebrowser import askopenfilenames

import logging


class PCPCodeFile(sequenceSpec):
    """Sequence for importing PCPcode for motion commands and tool
    triggers

    """

    # Construct/Destruct Methods #############################################
    def __init__(self, axes: Axes3DSpec = nullAxes(),
                 tool: toolSpec = nullTool(), tool2: toolSpec = nullTool2(), tool3: toolSpec = nullTool3(), **kwargs):
        """*Initializes PCPCodeFile object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec.Axes3DSpec
            The set of axes that commands will be sent to.
        tool: toolSpec.toolSpec
            A tool that commands will be sent to.
        tool2: toolSpec.toolSpec
            A tool that commands will be sent to.
        tool3: toolSpec.toolSpec
            A tool that commands will be sent to.
        """
        # Get current Date
        dateStr = str(datetime.date(datetime.now()))
        currentDate = dateStr[-5:-3] + '\\' + dateStr[-2:] + '\\' + dateStr[:4]

        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "PCPCodeFile", "",
                             ""),
            "description": seqParam("Sequence Description",
                                    "Importing a PCPCode file", "", ""),
            "creationDate": seqParam("Creation Date",
                                     currentDate, "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Advanced", "", ""),
            "filePath": seqParam("PCPCodeFilePath", "PathUnset", "",
                                 "Full File Path to target PCPCode File"),
        }

        # Pass values to parent
        super().__init__(axes, tool, self.dictParams, **kwargs)


    # Unique Methods  ########################################################

    def importFromPCPFile(self):
        """Attempts to read line by line from PCPCodeFile at PCPCodeFilePath
        and directly load the read lines into cmdlist

        Returns
        -------
        bool
            True if read from file without an error.
        list
            list of read in commands as strings
        """
        try:
            PCPFilePath = self.dictParams.get("filePath").value
            print("PCPFilePath:" + PCPFilePath)
            PCPFile = fileHandler(fullFilePath=PCPFilePath)
            while not PCPFile.testFileIO('r'):
                print("\tError opening file... retry selecting PCPCodeFile:")
                tkWindow = tk.Tk()
                PCPFilePath = askopenfilenames(parent=tkWindow, initialdir='/',
                                             initialfile='tmp',
                                             filetypes=[("PCPCode Files",
                                                         "*.PCP|*.txt"),
                                                        ("All files", "*")])[0]
                self.dictParams.get("filePath").value = str(PCPFilePath)
                PCPFile.fullFilePath = str(PCPFilePath)

            status, inList = PCPFile.readFullFile()
            return status, inList

        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)

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

        try:
            print("\t\tAttempting to read PCPCode File into RAM...")
            [readStatus, PCPLines] = self.importFromPCPFile()
            if readStatus:
                print("\t\tPCPCode File read into RAM successfully!")
                print("\t\tAttempting to load commands...")
                for line in PCPLines:
                    if line:
                        cmds.append(line)
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
