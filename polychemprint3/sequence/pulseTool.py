# -*- coding: utf-8 -*-
"""
Pulses Tool dispense at a set interval for a given number of times

| First created on 10/28/20
| Revised: -
| Author: Bijal Patel

"""
from polychemprint3.axes.axes3DSpec import Axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging


class pulseTool(sequenceSpec):
    """Implemented print sequence for pulseTool."""

    # Construct/Destruct METHODS ######################################################################################
    def __init__(self, axes: Axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """*Initializes pulseTool object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """
        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "pulseTool", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "Pulse Tool at a set value for a given number of cycles", "", "pulseTool.py"),
            "creationDate": seqParam("Creation Date",
                                     "28/10/2020", "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_Fundamentals", "", ""),

            "toolOn": seqParam("Tool on Value", "5", "", "Value to set the Tool for during ON time"),
            "toolOff": seqParam("Tool Off Value", "-1", "", "Value to set the Tool for during OFF time, -1 forces tool "
                                                            "disengage instead of Off Value"),
            "timeOn": seqParam("On Time", "1.00", "seconds", "Per cycle, how long should the tool be ON for (accepts "
                                                             "decimals)?"),
            "timeOff": seqParam("Off Time", "1.00", "seconds", "Per cycle, how long should the tool be OFF for?"),
            "numCycles": seqParam("Cycles", "1", "", "How many cycles to execute?"),
            "pauseFinal": seqParam("Include Final Pause?", "N", "(Y/N)", "Should the sequence end with a pause?")
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
        self.cmdList = []
        cmds = self.cmdList
        try:

            # Pull values for brevity
            toolOn = self.dictParams.get("toolOn").value
            toolOff = self.dictParams.get("toolOff").value
            timeOn = self.dictParams.get("timeOn").value
            timeOff = self.dictParams.get("timeOff").value
            numCycles = self.dictParams.get("numCycles").value
            pauseFinal = self.dictParams.get("pauseFinal").value.upper()

            # Initialize cycle count to 0
            count = 0

            # See if user wants tool to disengage or go to OffValue during off part of cycle
            doDisengage = toolOff == "-1"

            # Step by Step appending commands to list for execution
            while count < float(numCycles):
                # Set tool to On value, engage if necessary, and pause for On duration
                cmds.append("tool.setValue(\"" + str(toolOn) + "\")")
                if doDisengage or count == 0:
                    cmds.append("tool.engage()")
                cmds.append("time.sleep(float(\"" + str(timeOn) + "\"))")

                # Set tool to Off value OR disengage and pause for Off duration
                if doDisengage:
                    cmds.append("tool.disengage()")
                else:
                    cmds.append("tool.setValue(\"" + str(toolOff) + "\")")
                cmds.append("time.sleep(float(\"" + str(timeOff) + "\"))")

                # increment count
                count += 1

            # Add final disengage if missing
            if not doDisengage:
                cmds.append("tool.disengage()")

            # Remove final pause, if requested
            if pauseFinal == "N":
                cmds.pop()

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
