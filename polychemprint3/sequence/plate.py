# -*- coding: utf-8 -*-
"""Predefined print sequence for plates.

| First created on 13/11/2019 14:41:31
| Revised:
| Author: Bijal Patel

"""

from polychemprint3.axes.axes3DSpec import Axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class plate(sequenceSpec):
    """Implemented print sequence for plates."""

    # Construct/Destruct METHODS ######################################################################################
    def __init__(self, axes: Axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """*Initializes gapLine object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """
        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "plate", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "Meanderline plate with adjustable parameters and speed/value screening",
                                    "", "plate.py"),
            "creationDate": seqParam("Creation Date",
                                     "13/11/2019", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Simple2D", "", ""),
            "printSpd": seqParam("Printing Speed", "60", "", ""),
            "lineDir": seqParam("Line direction", "X", "", "Along X or Y"),
            "pitch": seqParam("Line Pitch", "1", "mm", ""),
            "length": seqParam("Line Length", "10", "mm", ""),
            "numLines": seqParam("Number of lines", "5", "mm", ""),
            "toolOnVal": seqParam("Tool ON Value", "100", tool.units,
                                  "Depends on tool loaded"),
            "valInc": seqParam("Value Increment", "0", "", ""),
            "valOp": seqParam("Value Operation", "+", "", ""),
            "spdInc": seqParam("Speed Increment", "0", "", ""),
            "spdOp": seqParam("Speed Operation", "+", "", "")}

        # Pass values to parent
        super().__init__(axes, tool, self.dictParams, **kwargs)

    # sequenceSpec Methods ###########################################################################################
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
            pitch = self.dictParams.get("pitch").value
            length = self.dictParams.get("length").value
            numLines = self.dictParams.get("numLines").value
            toolOnValue = self.dictParams.get("toolOnVal").value
            valInc = self.dictParams.get("valInc").value
            valOp = self.dictParams.get("valOp").value
            spdInc = self.dictParams.get("spdInc").value
            spdOp = self.dictParams.get("spdOp").value

            # Relative Positioning
            cmds.append("axes.setPosMode(\"relative\")")

            cmds.append("tool.setValue(\"" + str(toolOnValue) + "\")")
            cmds.append("tool.engage()")

            count = 1

            # Print 1st line
            cmds.append(("axes.move(\"G1 F" + str(printSpd)
                         + " X" + str(length) + "\\n" + "\")"))
            direct = 'forwardR'
            # Write as if printing X lines
            while count < int(numLines):
                if direct == 'right':
                    printSpd = eval(str(printSpd) + str(spdOp) + str(spdInc))
                    toolOnValue = eval(str(toolOnValue)
                                       + str(valOp) + str(valInc))
                    cmds.append("tool.setValue(\""
                                + str(toolOnValue) + "\")")
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(length) + "\\n" + "\")"))
                    direct = 'forwardR'
                    count += 1
                elif direct == 'forwardR':
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " Y-" + str(pitch) + "\\n" + "\")"))
                    direct = 'left'
                elif direct == 'left':
                    printSpd = eval(str(printSpd) + str(spdOp) + str(spdInc))
                    toolOnValue = eval(str(toolOnValue)
                                       + str(valOp) + str(valInc))
                    cmds.append("tool.setValue(\""
                                + str(toolOnValue) + "\")")
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X-" + str(length) + "\\n" + "\")"))
                    direct = 'forwardL'
                    count += 1
                elif direct == 'forwardL':
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " Y-" + str(pitch) + "\\n" + "\")"))
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

    # loggerSpec Methods #############################################################################################

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
