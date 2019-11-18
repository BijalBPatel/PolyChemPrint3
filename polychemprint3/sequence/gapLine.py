# -*- coding: utf-8 -*-
"""
Predefined print sequence for gapLines.

| First created on 13/11/2019 14:41:31
| Revised:
| Author: Bijal Patel

"""
import sys
sys.path.append("../../")
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
import logging


class gapLine(sequenceSpec):
    """Implemented print sequence for gapLines."""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes, tool, verbose, **kwargs):
        """*Initializes gapLine object with default values*.

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
            name of sequence, e.g., gapLine
        creationDate
            date sequence first defined, e.g., 13/11/2019 13:33:28
        createdBy: String
            who created this sequence
        owner: String
            who owns this shape (default: PCP_Core))
        """
        # Create Params dict

        self.dictParams = {
            "name": seqParam("name", "gapLine", "",
                             "Change if modifying from default"),
            "creationDate": seqParam("Creation Date",
                                     "13/11/2019", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Electronics", "",
                              "default: PCP_Core"),
            "printSpd": seqParam("Printing Speed", "60", "", ""),
            "trvlSpd": seqParam("Travel Speed", "200", "", ""),
            "xLength": seqParam("X-Length", "10", "mm", "Total X Length"),
            "yLength": seqParam("Y-Length", "10", "mm", "Total Y Length"),
            "ySpacing": seqParam("Y-Spacing", "10", "mm", ""),
            "xGap": seqParam("X-Gap", "2", "mm", "Length of gap in X"),
            "Z-hop height": seqParam("Z-hop", "0", "",
                                     "Height to raise Z-axis for gap"),
            "toolOnVal": seqParam("Tool ON Value", "100", tool.units,
                                  "Depends on tool loaded"),
            "toolTrvlVal": seqParam("Tool Travel Value", "2", tool.units,
                                    "Depends on tool loaded"),
            "toolOffVal": seqParam("Tool OFF Value", "0", tool.units,
                                   "Depends on tool loaded")}

        self.cmdList = []

        # Pass values to parent
        nameString = self.dictParams.get("name").value
        descrip = "Repeatedly prints lines in X with a gap [tool raised]"
        super().__init__(nameString, descrip, axes, tool, verbose, **kwargs)

    ################### Sequence Actions ###################################
    def operateSeq(self):
        """*Performs print sequence*.

        Returns
        -------
        bool
            Whether sequence successfully completed or not
        """
        try:
            tool = self.tool
            axes = self.axes
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
        try:

            # Pull values for brevity
            printSpd = self.dictParams.get("printSpd").value
            trvlSpd = self.dictParams.get("printSpd").value
            xLength = self.dictParams.get("lineDir").value
            ySpacing = self.dictParams.get("pitch").value
            yLength = self.dictParams.get("length").value
            xGap = self.dictParams.get("numLines").value
            zHopHeight = self.dictParams.get("valInc").value
            toolOnValue = self.dictParams.get("toolOnVal").value
            toolOFFValue = self.dictParams.get("toolOnVal").value
            toolTrvLValue = self.dictParams.get("toolOnVal").value

            self.cmdList.append("tool.setValue(" + str(toolOnValue) + ")")
            self.cmdList.append("tool.engage()")

            count = 1
            # Print 1st line
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(length) + "\n" + "\")"))
            direct = 'forwardR'
            # Write as if printing X lines
            while (count < int(numLines)):
                if (direct == 'right'):
                    printSpd = eval(str(printSpd) + str(spdOp) + str(spdInc))
                    toolOnValue = eval(str(toolOnValue
                                           + str(valOp) + str(valInc)))
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
                    printSpd = eval(str(printSpd) + str(spdOp) + str(spdInc))
                    toolOnValue = eval(str(toolOnValue)
                                       + str(valOp) + str(valInc))
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
