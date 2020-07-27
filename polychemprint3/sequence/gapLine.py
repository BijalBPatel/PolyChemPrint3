# -*- coding: utf-8 -*-
"""Predefined print sequence for gapLines.

| First created on 13/11/2019 14:41:31
| Revised: 5/3/20
| Author: Bijal Patel

"""
from polychemprint3.axes import axes3DSpec

from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging

from polychemprint3.tools.toolSpec import toolSpec


class gapLine(sequenceSpec):
    """Implemented print sequence for gapLines."""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes: axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """*Initializes gapLine object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """

        # Create Params dict
        self.dictParams = {
            "name": seqParam("Sequence Name", "gapLine", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "Lines in X-direction with a gap where tool raises", "", "gapLine.py"),
            "creationDate": seqParam("Creation Date",
                                     "13/11/2019", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Electronics", "",
                              "default: PCP_1DCore"),
            "printSpd": seqParam("Printing Speed", "60", "mm/min", ""),
            "trvlSpd": seqParam("Travel Speed", "200", "mm/min", ""),
            "xSegLength": seqParam("x-seglength", "10", "mm", "Length of each X segment"),
            "xGap": seqParam("X-Gap", "2", "mm", "Length of gap in X"),
            "numRows": seqParam("numRows", "3", "mm", "Number of lines to print"),
            "ySpacing": seqParam("Y-Spacing", "3", "mm", "Spacing (in y) between lines"),
            "Z-hop height": seqParam("Z-hop", "1", "",
                                     "Height to raise Z-axis for gap"),
            "toolOnVal": seqParam("Tool ON Value", "100", tool.units,
                                  "Depends on tool loaded"),
            "toolTrvlVal": seqParam("Tool Travel Value", "0", tool.units,
                                    "Depends on tool loaded"),
            "toolOffVal": seqParam("Tool OFF Value", "0", tool.units,
                                   "Depends on tool loaded")}

        # Pass values to parent
        super().__init__(axes, tool, self.dictParams, **kwargs)

    ################### Sequence Actions ###################################
    def genSequence(self):
        """*Generates the list of python commands to execute for this sequence (shape)*.

        Returns
        -------
        bool
            whether successfully reached the end or not
        """
        self.cmdList = []
        try:
            # Pull values for brevity (all as strings)
            printSpd = self.dictParams.get("printSpd").value
            trvlSpd = self.dictParams.get("trvlSpd").value
            xSegLength = self.dictParams.get("xSegLength").value
            xGap = self.dictParams.get("xGap").value
            ySpacing = self.dictParams.get("ySpacing").value
            numRows = self.dictParams.get("numRows").value
            zHop = self.dictParams.get("Z-hop height").value
            toolOnVal = self.dictParams.get("toolOnVal").value
            toolTrvlVal = self.dictParams.get("toolTrvlVal").value
            toolOffVal = self.dictParams.get("toolOffVal").value

            # Calculated Values
            totalX = 2 * float(xSegLength) + float(xGap)

            # Set relative positioning mode
            self.cmdList.append("axes.setPosMode(\"relative\")")

            # Enter loop for each gap-line row
            rowCount = 1

            # 0 Engage tool with off value
            self.cmdList.append("tool.setValue(" + str(toolOffVal) + ")")
            self.cmdList.append("tool.engage()")

            while rowCount <= int(numRows):

                # 1 Move LR while printing
                self.cmdList.append("tool.setValue(" + str(toolOnVal) + ")")
                self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " X" + str(xSegLength) + "\\n" + "\")"))

                # 2 Lift/Stop Tool
                self.cmdList.append("tool.setValue(" + str(toolTrvlVal) + ")")
                self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                     + " Z" + str(zHop) + "\\n" + "\")"))

                # 3 Move across gap and lower
                self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                     + " X" + str(xGap) + "\\n" + "\")"))

                self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                     + " Z-" + str(zHop) + "\\n" + "\")"))

                # 4 Move LR while printing
                self.cmdList.append("tool.setValue(" + str(toolOnVal) + ")")
                self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " X" + str(xSegLength) + "\\n" + "\")"))

                # Increment row count
                rowCount += 1

                # 5 Travel to next line start position [if not last line]
                if rowCount != numRows:
                    self.cmdList.append("tool.setValue(" + str(toolTrvlVal) + ")")
                    self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                         + " Z" + str(zHop) + "\\n" + "\")"))
                    self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                         + " Y-" + str(ySpacing) + "\\n" + "\")"))
                    self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                         + " X-" + str(totalX) + "\\n" + "\")"))
                    self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                         + " Z-" + str(zHop) + "\\n" + "\")"))

                else:
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
