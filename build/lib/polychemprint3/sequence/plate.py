# -*- coding: utf-8 -*-
"""Predefined print sequence for plates.

| First created on 13/11/2019 14:41:31
| Revised:
| Author: Bijal Patel

"""

from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class plate(sequenceSpec):
    """Implemented print sequence for plates."""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes=nullAxes(), tool=nullTool(), **kwargs):
        """*Initializes plate object with default values*.

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
            "name": seqParam("name", "Plate", "",
                             "Change if modifying from default"),
            "creationDate": seqParam("Creation Date",
                                     "13/11/2019", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Core", "", "default: PCP_Core"),
            "printSpd": seqParam("Printing Speed", "60", "", ""),
            "lineDir": seqParam("Line direction", "X", "", "Along X or Y"),
            "pitch": seqParam("Center-to-Center Spacing", "1", "mm", ""),
            "length": seqParam("Line Length", "10", "mm", ""),
            "numLines": seqParam("Number of lines", "5", "mm", ""),
            "toolOnVal": seqParam("Tool ON Value", "100", tool.units,
                                  "Depends on tool loaded"),
            "valInc": seqParam("Value Increment", "0", "", ""),
            "valOp": seqParam("Value Operation", "+", "", ""),
            "spdInc": seqParam("Speed Increment", "0", "", ""),
            "spdOp": seqParam("Speed Operation", "+", "", "")}

        self.cmdList = []

        # Pass values to parent
        nameString = self.dictParams.get("name").value
        descrip = "Regularly spaced meanderlines along X/Y axis"
        super().__init__(nameString, descrip, **kwargs)

    ################### Sequence Actions ###################################
    def operateSeq(self, tool, axes):
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

    def genSequence(self, tool, axes):
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
            pitch = self.dictParams.get("pitch").value
            length = self.dictParams.get("length").value
            numLines = self.dictParams.get("numLines").value
            toolOnValue = self.dictParams.get("toolOnVal").value
            valInc = self.dictParams.get("valInc").value
            valOp = self.dictParams.get("valOp").value
            spdInc = self.dictParams.get("spdInc").value
            spdOp = self.dictParams.get("spdOp").value
            self.cmdList.append("tool.setValue(" + str(toolOnValue) + ")")
            self.cmdList.append("tool.engage()")

            count = 1
            # Print 1st line
            cmds.append(("axes.move(\"G1 F" + str(printSpd)
                         + " X" + str(length) + "\n" + "\")"))
            direct = 'forwardR'
            # Write as if printing X lines
            while (count < int(numLines)):
                if (direct == 'right'):
                    printSpd = eval(str(printSpd) + str(spdOp) + str(spdInc))
                    toolOnValue = eval(str(toolOnValue
                                           + str(valOp) + str(valInc)))
                    cmds.append("tool.setValue("
                                + str(toolOnValue) + ")")
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(length) + "\n" + "\")"))
                    direct = 'forwardR'
                    count += 1
                elif (direct == 'forwardR'):
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " Y-" + str(pitch) + "\n" + "\")"))
                    direct = 'left'
                elif (direct == 'left'):
                    printSpd = eval(str(printSpd) + str(spdOp) + str(spdInc))
                    toolOnValue = eval(str(toolOnValue)
                                       + str(valOp) + str(valInc))
                    cmds.append("tool.setValue("
                                + str(toolOnValue) + ")")
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X-" + str(length) + "\n" + "\")"))
                    direct = 'forwardR'
                    count += 1
                elif (direct == 'forwardL'):
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " Y-" + str(pitch) + "\n" + "\")"))
                    direct = 'right'

            if lineDir == "Y":  # need to rotate coordinates in cmdList
                # First map Y onto W
                cmds = [cmd.replace('Y', 'W') for cmd in cmds]
                # Then map X onto Y
                cmds = [cmd.replace('X', 'Y') for cmd in cmds]
                # Then map W onto X
                cmds = [cmd.replace('W', 'X') for cmd in cmds]

            cmds.append("tool.disengage()")
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
