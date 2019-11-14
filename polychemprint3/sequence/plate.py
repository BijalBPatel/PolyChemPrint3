# -*- coding: utf-8 -*-
"""
Predefined print sequence for plates.

| First created on 13/11/2019 14:41:31
| Revised:
| Author: Bijal Patel

"""
import sys
sys.path.append("../../")
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.axes.Axes3D import axes3D
import logging


class plate(sequenceSpec):
    """Implemented print sequence for plates."""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes, tool, verbose, **kwargs):
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
                                     "13/11/2019", "dd/mm/yyyy", ""),
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

        super().__init__(axes, tool, verbose, **kwargs)

    ################### Sequence Actions ###################################
    def operateSeq(self):
        """*Performs print sequence*.

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
        try:

            # Pull values
            printSpd = self.dictParams.get("printSpd").value,
            lineDir = self.dictParams.get("lineDir").value,
            pitch = self.dictParams.get("pitch").value,
            length = self.dictParams.get("length").value,
            numLines = self.dictParams.get("numLines").value,
            toolOnValue = self.dictParams.get("toolOnValue").value,
            valInc = self.dictParams.get("valInc").value,
            valOp = self.dictParams.get("valOp").value,
            spdInc = self.dictParams.get("spdInc").value,
            spdOp = self.dictParams.get("spdOp").value

            self.cmdList.append("tool.setValue(" + str(toolOnValue) + ")")
            self.cmdList.append("tool.engage()")

            count = 1
            # Print 1st line
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(length) + "\n" + "\")"))

            direct = 'forwardR'

            # Write as if printing X lines
            while (count < numLines):
                if (direct == 'right'):
                    printSpd = eval(str(printSpd) + spdOp + str(spdInc))
                    toolOnValue = eval(str(toolOnValue + valOp + str(valInc)))
                    self.cmdList.append("tool.setValue("
                                        + str(toolOnValue) + ")")
                    self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                         + " X" + str(length) + "\n" + "\")"))
                    direct = 'forwardR'
                    count += 1
                elif (direct == 'forwardR'):
                    self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                         + " Y-" + str(pitch) + "\n" + "\")"))
                    direct = 'left'
                elif (direct == 'left'):
                    printSpd = eval(str(printSpd) + spdOp + str(spdInc))
                    toolOnValue = eval(str(toolOnValue + valOp + str(valInc)))
                    self.cmdList.append("tool.setValue("
                                        + str(toolOnValue) + ")")
                    self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                         + " X-" + str(length) + "\n" + "\")"))
                    direct = 'forwardR'
                    count += 1
                elif (direct == 'forwardL'):
                    self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                         + " Y-" + str(pitch) + "\n" + "\")"))
                    direct = 'right'

            if lineDir == "Y":  # need to rotate coordinates in cmdList
                # First map Y onto W
                self.cmdList = [cmd.replace('Y', 'W') for cmd in self.cmdList]
                # Then map X onto Y
                self.cmdList = [cmd.replace('X', 'Y') for cmd in self.cmdList]
                # Then map W onto X
                self.cmdList = [cmd.replace('W', 'X') for cmd in self.cmdList]

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
        """*Generates json string containing dict to be written to log file*.

        Returns
        -------
        String
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
