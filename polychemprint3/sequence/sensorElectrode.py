# -*- coding: utf-8 -*-
"""Predefined print sequence for interleaving electrodes for sensors.

| First created on (dd/mm/yyyy): 20/01/2021
| Revised (dd/mm/yyyy):
| Author: Bijal Patel

"""
from polychemprint3.axes.axes3DSpec import Axes3DSpec

from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging

from polychemprint3.tools.toolSpec import toolSpec


class sensorElectrode(sequenceSpec):
    """Implemented print sequence for gapLines."""

    # Construct/Destruct METHODS #############################################
    def __init__(self, axes: Axes3DSpec = nullAxes(),
                 tool: toolSpec = nullTool(), **kwargs):
        """Initializes sensorElectrode object.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """

        # Create Params dict
        self.dictParams = {
            "name": seqParam("Sequence Name", "sensorElectrode", "", ""),
            "description": seqParam("Sequence Description",
                                    "Electrode with interleaving fingers, "
                                    "constant channel length, long axis = "
                                    "X", "", "sensorElectrode.py"),
            "creationDate": seqParam("Creation Date",
                                     "21/01/2021", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Electronics", "",
                              ""),
            "printSpd": seqParam("Printing Speed", "60", "mm/min", ""),
            "trvlSpd": seqParam("Travel Speed", "200", "mm/min", ""),
            "linewidth": seqParam("linewidth", "0.7", "mm",
                                  "Width of each printed line"),
            "leadIns": seqParam("lead-ins", "3", "mm",
                                "Length of lead-in electrodes"),
            "xOverlap": seqParam("x-overlap", "1.230", "mm",
                                 "x-length of overlap between 'fingers'"),
            "channlength": seqParam("channellength", "0.5", "mm",
                                    "Distance between electrode 'fingers'"),
            "Z-hop height": seqParam("Z-hop", "1", "",
                                     "Height to raise Z-axis during travel "
                                     "moves"),
            "toolOnVal": seqParam("Tool ON Value", "100", tool.units,
                                  "Depends on tool loaded"),
            "toolTrvlVal": seqParam("Tool Travel Value", "0", tool.units,
                                    "Depends on tool loaded"),
            "toolOffVal": seqParam("Tool OFF Value", "0", tool.units,
                                   "Depends on tool loaded"),
            "cleanSteps": seqParam("cleanSteps", "F", "T/F",
                                   "Allow nozzle cleaning between strokes?")}

        # Pass values to parent
        super().__init__(axes, tool, self.dictParams, **kwargs)

    # Sequence Actions #######################################################
    def genSequence(self):
        """Generates the list of python commands to execute for this sequence.

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
            linewidth = float(self.dictParams.get("linewidth").value)
            leadIns = float(self.dictParams.get("leadIns").value)
            xOverlap = float(self.dictParams.get("xOverlap").value)
            channlength = float(self.dictParams.get("channlength").value)
            zHop = self.dictParams.get("Z-hop height").value
            toolOnVal = self.dictParams.get("toolOnVal").value
            toolTrvlVal = self.dictParams.get("toolTrvlVal").value
            toolOffVal = self.dictParams.get("toolOffVal").value
            cleanSteps = self.dictParams.get("cleanSteps").value

            # Calculated Values - Note: stored as floats
            # Absolute positions, s = start, e = end
            [x1e, y1e] = [leadIns + linewidth / 2, 0]
            [x2sa, y2sa] = [leadIns + xOverlap + channlength,
                            channlength + linewidth]
            [x2ea, y2ea] = [leadIns + linewidth / 2, channlength + linewidth]
            [x2eb, y2eb] = [leadIns + linewidth / 2,
                            0 - channlength - linewidth]
            [x2ec, y2ec] = [leadIns + xOverlap + channlength,
                            0 - channlength - linewidth]
            [x3s, y3s] = [2 * (leadIns + linewidth + channlength) + xOverlap,
                          0]
            [x3e, y3e] = [leadIns + linewidth + channlength + linewidth / 2, 0]
            [x4sa, y4sa] = [leadIns + linewidth + channlength + linewidth / 2,
                            2 * (linewidth + channlength)]
            [x4ea, y4ea] = [
                leadIns + linewidth + 2 * channlength + linewidth / 2
                + xOverlap, 2 * (linewidth + channlength)]
            [x4eb, y4eb] = [
                leadIns + linewidth + 2 * channlength + linewidth / 2
                + xOverlap, 2 * (-linewidth - channlength)]
            [x4ec, y4ec] = [leadIns + linewidth + channlength + linewidth / 2,
                            2 * (-linewidth - channlength)]

            # Booleans
            cleanSteps = cleanSteps.lower() == 't'

            # Set current position to absolute zero
            self.cmdList.append("axes.setPosMode(\"absolute\")")
            self.cmdList.append("axes.setPosZero()")

            # 0 Engage tool with off value
            self.cmdList.append("tool.setValue(" + str(toolOnVal) + ")")
            self.cmdList.append("tool.engage()")

            # 1 Print stroke one
            self.cmdList.append("tool.setValue(" + str(toolOnVal) + ")")
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(x1e)
                                 + " Y" + str(y1e)
                                 + "\\n" + "\")"))

            # Move to stroke two and optionally clean
            self.cmdList.append("tool.setValue(" + str(toolTrvlVal) + ")")
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " Z" + str(zHop) + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " X" + str(x2sa)
                                 + " Y" + str(y2sa)
                                 + "\\n" + "\")"))
            if cleanSteps:
                self.cmdList.append("tool.disengage()")
                self.cmdList.append(("axes.move(\"G1 F2000" + " Z20"
                                     + "\\n" + "\")"))
                self.cmdList.append("input('Enter any key when "
                                    "ready for next stroke to "
                                    "begin')")
                self.cmdList.append("tool.setValue(" + str(toolTrvlVal) + ")")
                self.cmdList.append("tool.engage()")
                self.cmdList.append(("axes.move(\"G1 F2000" + " Z2"
                                     + "\\n" + "\")"))
                self.cmdList.append(("axes.move(\"G1 F500" + " Z0"
                                     + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " Z0" + "\\n" + "\")"))
            # 2 Print stroke two
            self.cmdList.append("tool.setValue(" + str(toolOnVal) + ")")
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(x2ea)
                                 + " Y" + str(y2ea)
                                 + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(x2eb)
                                 + " Y" + str(y2eb)
                                 + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(x2ec)
                                 + " Y" + str(y2ec)
                                 + "\\n" + "\")"))

            # Move to stroke three and optionally clean
            self.cmdList.append("tool.setValue(" + str(toolTrvlVal) + ")")
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " Z" + str(zHop) + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " X" + str(x3s)
                                 + " Y" + str(y3s)
                                 + "\\n" + "\")"))
            if cleanSteps:
                self.cmdList.append("tool.disengage()")
                self.cmdList.append(("axes.move(\"G1 F2000" + " Z20"
                                     + "\\n" + "\")"))
                self.cmdList.append("input('Enter any key when "
                                    "ready for next stroke to "
                                    "begin')")
                self.cmdList.append("tool.setValue(" + str(toolTrvlVal) + ")")
                self.cmdList.append("tool.engage()")
                self.cmdList.append(("axes.move(\"G1 F2000" + " Z2"
                                     + "\\n" + "\")"))
                self.cmdList.append(("axes.move(\"G1 F500" + " Z0"
                                     + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " Z0" + "\\n" + "\")"))
            # 3 Print stroke three
            self.cmdList.append("tool.setValue(" + str(toolOnVal) + ")")
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(x3e)
                                 + " Y" + str(y3e)
                                 + "\\n" + "\")"))

            # Move to stroke four and optionally clean
            self.cmdList.append("tool.setValue(" + str(toolTrvlVal) + ")")
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " Z" + str(zHop) + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " X" + str(x4sa)
                                 + " Y" + str(y4sa)
                                 + "\\n" + "\")"))
            if cleanSteps:
                self.cmdList.append("tool.disengage()")
                self.cmdList.append(("axes.move(\"G1 F2000" + " Z20"
                                     + "\\n" + "\")"))
                self.cmdList.append("input('Enter any key when "
                                    "ready for next stroke to "
                                    "begin')")
                self.cmdList.append("tool.setValue(" + str(toolTrvlVal) + ")")
                self.cmdList.append("tool.engage()")
                self.cmdList.append(("axes.move(\"G1 F2000" + " Z2"
                                     + "\\n" + "\")"))
                self.cmdList.append(("axes.move(\"G1 F500" + " Z0"
                                     + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " Z0" + "\\n" + "\")"))
            # 4 Print stroke four
            self.cmdList.append("tool.setValue(" + str(toolOnVal) + ")")
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(x4ea)
                                 + " Y" + str(y4ea)
                                 + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(x4eb)
                                 + " Y" + str(y4eb)
                                 + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X" + str(x4ec)
                                 + " Y" + str(y4ec)
                                 + "\\n" + "\")"))

            # Move to origin and disengage
            self.cmdList.append("tool.setValue(" + str(toolTrvlVal) + ")")
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " Z" + str(zHop) + "\\n" + "\")"))
            self.cmdList.append(("axes.move(\"G1 F" + str(trvlSpd)
                                 + " X0"
                                 + " Y0"
                                 + "\\n" + "\")"))
            self.cmdList.append("tool.setValue(" + str(toolOffVal) + ")")
            self.cmdList.append("tool.disengage()")

            return True
        except KeyboardInterrupt:
            print("\tgenSequence Terminated by User....")
            return False
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    # Logging METHODS #######################################################

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
