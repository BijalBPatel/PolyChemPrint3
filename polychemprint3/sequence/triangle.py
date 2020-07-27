# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 17:31:47 2020

@author: Yilong Chang
"""

from polychemprint3.axes import axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import math
import logging


class triangle(sequenceSpec):
    """Implemented print sequence for circle."""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes: axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """*Initializes triangle object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """
        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "triangle", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "a triangle", "", "current positon of nozzle is center"),
            "creationDate": seqParam("Creation Date",
                                     "16/11/2019", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Yilong Chang", "", ""),
            "owner": seqParam("Owner", "PCP_1DCore", "", "default: PCP_Core"),
            "printSpd": seqParam("Printing Speed", "60", "", ""),
            "baseline": seqParam("Baseline length", "10", "mm", ""),
            "adjacent": seqParam("Adjacent line length", "20", "mm", ""),
            "angle": seqParam("Formed angle", "60", "degree", "have to less than 180 degree"),
            "step": seqParam("Steps in x and y", "0.5", "mm", "smaller value lead to better precision"),

            "toolOnVal": seqParam("Tool ON Value", "100", tool.units,
                                  "Depends on tool loaded"),
            "toolOffVal": seqParam("Tool OFF Value", "000", tool.units,
                                   "Depends on tool loaded")}

        # Pass values to parent
        super().__init__(axes, tool, self.dictParams, **kwargs)

        ################### Sequence Actions ###################################

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
            baseline = self.dictParams.get("baseline").value
            step = self.dictParams.get("step").value
            adjacent = self.dictParams.get("adjacent").value
            angle = self.dictParams.get("angle").value
            toolOnValue = self.dictParams.get("toolOnVal").value
            cmds.append("tool.setValue(" + str(toolOnValue) + ")")
            self.cmdList.append("tool.engage()")

            # calculation
            CalStep = float(step)
            CalBaseline = float(baseline)
            CalAdjacent = float(adjacent)
            CalAngle = math.radians(float(angle))
            xstep = CalStep * math.cos(CalAngle)
            ystep = CalStep * math.sin(CalAngle)
            AdjacentX = CalAdjacent * math.cos(CalAngle)
            thirdLineX = CalBaseline - AdjacentX
            AdjacentY = CalAdjacent * math.sin(CalAngle)
            thirdLineY = AdjacentY

            # print baseline
            cmds.append(("axes.move(\"G1 F" + str(printSpd)
                         + " X" + str(baseline) + "\\n" + "\")"))

            if float(angle) != 90:

                # pirnt thrid line
                count = 0
                while count < thirdLineY:
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " Y" + str(ystep) + "\\n" + "\")"))
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X-" + str(xstep) + "\\n" + "\")"))
                    count += ystep

                count = 0

                if thirdLineX < CalBaseline:
                    while count < thirdLineY:
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " X-" + str(xstep) + "\\n" + "\")"))
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " Y-" + str(ystep) + "\\n" + "\")"))
                        count += ystep

                elif thirdLineX >= CalBaseline:
                    while count < thirdLineY:
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " X" + str(xstep) + "\\n" + "\")"))
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " Y-" + str(ystep) + "\\n" + "\")"))
                        count += ystep
            else:
                count = 0
                xstep = CalBaseline / (CalAdjacent + CalBaseline) * CalStep
                ystep = CalAdjacent / (CalAdjacent + CalBaseline) * CalStep
                while count < thirdLineY:
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " Y" + str(step) + "\\n" + "\")"))
                    cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                 + " X-" + str(step) + "\\n" + "\")"))
                    count += ystep

                cmds.append(("axes.move(\"G1 F" + str(printSpd)
                             + " Y-" + str(adjacent) + "\\n" + "\")"))

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
