# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 17:22:27 2020

@author: Yilong Chang
"""

from polychemprint3.axes import axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class rectangle(sequenceSpec):
    """Implemented print sequence for rectangle."""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes: axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """*Initializes rectangle object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """
        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "rectangle", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "a rectangle with length in x and width in y", "", ""),
            "creationDate": seqParam("Creation Date",
                                     "16/11/2019", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Yilong Chang", "", ""),
            "owner": seqParam("Owner", "PCP_1DCore", "", "default: PCP_Core"),
            "printSpd": seqParam("Printing Speed", "60", "", ""),
            "width": seqParam("Width", "10", "mm", "in y direction"),
            "length": seqParam("Length", "20", "mm", "in x direction"),
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
            width = self.dictParams.get("width").value
            length = self.dictParams.get("length").value
            toolOnValue = self.dictParams.get("toolOnVal").value
            cmds.append("tool.setValue(" + str(toolOnValue) + ")")

            self.cmdList.append("tool.engage()")
            cmds.append(("axes.move(\"G1 F" + str(printSpd)
                         + " X" + str(length) + "\\n" + "\")"))

            cmds.append(("axes.move(\"G1 F" + str(printSpd)
                         + " Y" + str(width) + "\\n" + "\")"))

            cmds.append(("axes.move(\"G1 F" + str(printSpd)
                         + " X-" + str(length) + "\\n" + "\")"))

            cmds.append(("axes.move(\"G1 F" + str(printSpd)
                         + " Y-" + str(width) + "\\n" + "\")"))

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
