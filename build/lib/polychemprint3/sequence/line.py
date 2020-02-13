# -*- coding: utf-8 -*-
"""
Predefined print sequence for simple lines.

| First created on 13/11/2019 14:41:31
| Revised:
| Author: Bijal Patel

"""

from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class line(sequenceSpec):
    """Implemented print sequence for single lines."""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes=nullAxes(), tool=nullTool(), **kwargs):
        """*Initializes line object with default values*.

        Parameters
        ----------
        axes: PCP_Axes object
            Axes object to send motion commands to
        tool: PCP_Tool
            Tool object to send dispense commands to
        verbose: bool
            level of detail to be printed to cmd line

        generic seq params
        ------------------
        name: String
            name of sequence, e.g., Plate
        creationDate
            date sequence first defined, e.g., 13/11/2019 13:33:28
        createdBy: String
            who created this sequence
        owner: String
            who owns this shape (default: PCP_Core))
        """
        # Create Params dict

        self.dictParams = {
            "name": seqParam("name", "Line", "",
                             "Change if modifying from default"),
            "creationDate": seqParam("Creation Date",
                                     "16/11/2019", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Core", "", "default: PCP_Core"),
            "printSpd": seqParam("Printing Speed", "60", "", ""),
            "lineDir": seqParam("Line direction", "X", "", "Along X or Y"),
            "length": seqParam("Line Length", "10", "mm", ""),
            "toolOnVal": seqParam("Tool ON Value", "100", tool.units,
                                  "Depends on tool loaded"),
            "toolOffVal": seqParam("Tool OFF Value", "000", tool.units,
                                   "Depends on tool loaded")}
        self.cmdList = []

        # Pass values to parent
        nameString = self.dictParams.get("name").value
        descrip = "Single line along X/Y axis"
        super().__init__(nameString, descrip, **kwargs)

    ################### Sequence Actions ###################################
    def operateSeq(self):
        """*Performs print sequence*.
        Parameters
        ----------
        tool: PCP_ToolSpec object
            tool to execute code with
        axes: PCP_Axes object
            axes to execute code with

        Returns
        -------
        bool
            Whether sequence successfully completed or not
        """
        try:
            for line in self.cmdList:
                eval(line)
            return True

        except KeyboardInterrupt:
            print("\tTerminated by User....")
            return False
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    def genSequence(self):
        """*Loads print sequence into a list into cmdList attribute*.

        Returns
        -------
        bool
            whether successfully reached the end or not
        """
        self.cmdList = []
        cmds = self.cmdList
        try:

            # Pull values
            printSpd = self.dictParams.get("printSpd").value
            lineDir = self.dictParams.get("lineDir").value
            length = self.dictParams.get("length").value
            toolOnValue = self.dictParams.get("toolOnVal").value

            cmds.append("tool.setValue(" + str(toolOnValue) + ")")
            self.cmdList.append("tool.engage()")

            # Print 1st line
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(length) + "\n" + "\")"))

            if lineDir == "Y":  # need to rotate coordinates in cmdList
                self.cmdList = [cmd.replace('X', 'Y') for cmd in self.cmdList]

            self.cmdList.append("tool.disengage()")
            return True

        except KeyboardInterrupt:
            print("\tgenSequence Terminated by User....")
            return False
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    ####################### Logging METHODS ###############################

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
