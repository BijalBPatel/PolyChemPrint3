# -*- coding: utf-8 -*-
"""
Parameterized code for moving axes in X,Y,Z at a set rate

| First created on [dd/mm/yyyy 24h:min:sec]
| Revised: [DATE]
| Author: Bijal Patel

"""
from polychemprint3.axes import axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class basicMove(sequenceSpec):
    """[ DESCRIPTION]"""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes: axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """*Initializes [SEQUENCE NAME] object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """
        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "basicMove", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "Move Axes (relative or abs)", "", "basicMove.py"),
            "creationDate": seqParam("Creation Date",
                                     "05/05/2020", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_CoreUtilities", "", "default: PCP_Core"),
            "posMode": seqParam("Positioning Mode", "relative", "absolute/relative",
                                "Versus current position or absolute origin"),
            "feedRate": seqParam("Axes Speed", "60", "mm/min",  ""),
            "xMove": seqParam("X movement", "5", "mm",
                                "distance/location to move in X"),
            "yMove": seqParam("Y movement", "5", "mm",
                              "distance/location to move in Y"),
            "zMove": seqParam("Z movement", "5", "mm",
                              "distance/location to move in Z"),
        }

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

            # Pull values for brevity
            posMode = self.dictParams.get("posMode").value.lower()
            feedRate = self.dictParams.get("feedRate").value
            xMove = self.dictParams.get("xMove").value
            yMove = self.dictParams.get("yMove").value
            zMove = self.dictParams.get("zMove").value

            # Step by Step appending commands to list for execution

            # 0 Set positioning mode
            cmds.append("axes.setPosMode(\"" + posMode +  "\")")

            # 1 Move at feed rate in X Y and Z
            cmds.append(("axes.move(\"G1 F" + str(feedRate)
                         + " X" + str(xMove)
                         + " Y" + str(yMove)
                         + " Z" + str(zMove)
                         + "\\n" + "\")"))

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
