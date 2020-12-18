# -*- coding: utf-8 -*-
"""
Sequence for introducing a pause. The length of time can be set, or it can resume on user input.

| First created (dd/mm/yyyy): 05/05/2020
| Revised (dd/mm/yyyy): 17/12/2020 - BP
| Author: Bijal Patel

"""
from polychemprint3.axes.axes3DSpec import Axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class pause(sequenceSpec):
    """Sequence for introducing a pause. The length of time can be set, or it can resume on user input."""

    # Construct/Destruct METHODS ######################################################################################
    def __init__(self, axes: Axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """*Initializes pause object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """
        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "pause", "",
                             ""),
            "description": seqParam("Sequence Description",
                                    "Pause execution for a set duration, or until user confirms",
                                    "", "pause.py"),
            "creationDate": seqParam("Creation Date",
                                     "05/05/2020", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Fundamentals", "", ""),
            "pauseTime": seqParam("pauseTime", "1", "seconds", "time to wait before next cmd sent"),
            "doPrompt": seqParam("Prompt to Continue?", "N", "(Y/N)", "Will user be prompted to resume?")
        }

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
        self.cmdList = []  # empty the cmdLists
        cmds = self.cmdList  # rename for brevity
        try:

            # Pull values for brevity
            pauseTime = self.dictParams.get("pauseTime").value
            doPrompt = self.dictParams.get("doPrompt").value.upper()

            # Step by Step appending commands to list for execution

            # 0 Do mandated pause regardless of prompt
            cmds.append("print(\"\\tpausing...\", end =\" \")")
            cmds.append("sleep(" + str(pauseTime) + ")")
            cmds.append("print(\" pause ended!\")")

            # Prompt user to continue if needed
            if doPrompt == "Y":
                cmds.append("input(\"Press any key to continue: \")")

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
