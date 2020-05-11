# -*- coding: utf-8 -*-
"""
[DESCRIPTION: Predefined print sequence for simple lines.]

| First created on [dd/mm/yyyy 24h:min:sec]
| Revised: [DATE]
| Author: [NAME]

"""
from polychemprint3.axes import axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class setToolState(sequenceSpec):
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
            "name": seqParam("name", "setToolState", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "Set Tool Value or Dispense State", "", "setToolState.py"),
            "creationDate": seqParam("Creation Date",
                                     "05/05/2020", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_CoreUtilities", "", "default: PCP_Core"),
            "dispenseState": seqParam("dispenseState", "NoChange", "On/Off/NoChange",
                                "Engage/Disengage/No Change"),
            "newVal": seqParam("newVal", "NoChange", "New value to set: Number or NoChange",
                                "New Tool Value to Set"),
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
            dispenseState = self.dictParams.get("dispenseState").value.lower()
            newVal = self.dictParams.get("newVal").value

            # Step by Step appending commands to list for execution

            # 0 Set dispense mode
            if dispenseState == "on":
                cmds.append("tool.engage()")
            elif dispenseState == "off":
                cmds.append("tool.disengage()")

            # 1 Set new value
            if newVal.lower() != "nochange":
                cmds.append("tool.setValue(" + str(newVal) + ")")

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
