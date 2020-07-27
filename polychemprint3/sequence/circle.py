# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:52:17 2020

@author: Yilong Chang
"""

from polychemprint3.axes import axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class circle(sequenceSpec):
    """Implemented print sequence for circle."""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes: axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """*Initializes circle object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """
        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "circle", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "a circle", "", "current positon of nozzle is center"),
            "creationDate": seqParam("Creation Date",
                                     "16/11/2019", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Yilong Chang", "", ""),
            "owner": seqParam("Owner", "PCP_1DCore", "", "default: PCP_Core"),
            "printSpd": seqParam("Printing Speed", "60", "", ""),
            "radius": seqParam("Radius", "10", "mm", ""),
            "step": seqParam("Steps in x and y", "0.5", "mm", "smaller value lead to rounder circle"),
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
            radius = self.dictParams.get("radius").value
            step = self.dictParams.get("step").value
            toolOnValue = self.dictParams.get("toolOnVal").value
            cmds.append("tool.setValue(" + str(toolOnValue) + ")")

            # move one radius away from center
            cmds.append(("axes.move(\"G1 F" + str(printSpd)
                         + " X" + str(radius) + "\\n" + "\")"))
            self.cmdList.append("tool.engage()")

            part = 1
            quadrant = 1;
            while part < 5:

                # print first quadrant
                if quadrant == 1:
                    count = 0
                    while count < int(radius):
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " Y" + str(step) + "\\n" + "\")"))
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " X-" + str(step) + "\\n" + "\")"))
                        count += float(step)
                    quadrant = 2
                    part += 1

                    # print second quadrant
                elif quadrant == 2:
                    count = 0
                    while count < int(radius):
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " X-" + str(step) + "\\n" + "\")"))
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " Y-" + str(step) + "\\n" + "\")"))
                        count += float(step)

                    quadrant = 3
                    part += 1

                # print third quadrant
                elif quadrant == 3:
                    count = 0
                    while count < int(radius):
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " Y-" + str(step) + "\\n" + "\")"))
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " X" + str(step) + "\\n" + "\")"))
                        count += float(step)

                    quadrant = 4
                    part += 1

                # print forth quadrant
                elif quadrant == 4:
                    count = 0
                    while count < int(radius):
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " Y" + str(step) + "\\n" + "\")"))
                        cmds.append(("axes.move(\"G1 F" + str(printSpd)
                                     + " X" + str(step) + "\\n" + "\")"))
                        count += float(step)

                    quadrant = 5
                    part += 1

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
