# -*- coding: utf-8 -*-
"""
While dispensing, moves axes a set distance in X,Y,Z at set speed

| First created on 13/11/2019 14:41:31
| Revised (dd/mm/yyyy): 17/12/2020 - BP
| Author: Bijal Patel

"""
from polychemprint3.axes.axes3DSpec import Axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class line(sequenceSpec):
    """Implemented print sequence for single lines."""

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
            "name": seqParam("name", "line", "", ""),
            "description": seqParam("Sequence Description",
                                    "A single line along a specified vector", "", "line.py"),
            "creationDate": seqParam("Creation Date",
                                     "16/11/2019", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Fundamentals", "", "default: PCP_Core"),
            "feedRate": seqParam("Axes Speed", "60", "mm/min", ""),
            "xMove": seqParam("X movement", "5", "mm",
                              "distance/location to move in X"),
            "yMove": seqParam("Y movement", "5", "mm",
                              "distance/location to move in Y"),
            "zMove": seqParam("Z movement", "5", "mm",
                              "distance/location to move in Z"),
            "toolOnVal": seqParam("Tool ON Value", "100", tool.units,
                                  "Depends on tool loaded"),
            "toolOffVal": seqParam("Tool OFF Value", "000", tool.units,
                                   "Depends on tool loaded")}

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

            # Pull values for brevity
            posMode = 'relative'
            feedRate = self.dictParams.get("feedRate").value
            xMove = self.dictParams.get("xMove").value
            yMove = self.dictParams.get("yMove").value
            zMove = self.dictParams.get("zMove").value
            toolOnValue = self.dictParams.get("toolOnVal").value
            toolOffValue = self.dictParams.get("toolOffVal").value

            # 0 Set positioning mode
            cmds.append("axes.setPosMode(\"" + posMode + "\")")

            # 1 Set Tool Value to On and engage
            cmds.append("tool.setValue(\"" + str(toolOnValue) + "\")")
            cmds.append("tool.engage()")

            # 2 Translate axis
            cmds.append(("axes.move(\"G1 F" + str(feedRate)
                         + " X" + str(xMove)
                         + " Y" + str(yMove)
                         + " Z" + str(zMove)
                         + "\\n" + "\")"))

            # 3 Set Tool Value to off and disengage
            cmds.append("tool.setValue(\"" + str(toolOffValue) + "\")")
            cmds.append("tool.disengage()")
            return True

        except KeyboardInterrupt:
            print("\tgenSequence Terminated by User....")
            return False
        except Exception as inst:
            print("\tgenSequence Terminated by Error....")
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
