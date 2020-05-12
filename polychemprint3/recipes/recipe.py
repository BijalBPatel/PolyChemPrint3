# -*- coding: utf-8 -*-
"""
Specifies modular recipe protocol to link series of sequences

| First created on Mon May 11 17:27:00 2020
| Revised:
| Author: Bijal Patel

"""
import logging
from time import sleep
from pathlib import Path
from polychemprint3.axes import axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence import sequenceSpec
from polychemprint3.utility.loggerSpec import loggerSpec
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
from polychemprint3.utility.fileHandler import fileHandler


class recipe(fileHandler, loggerSpec):
    """Class for recipes - a series of sequences joined together"""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self,
                 name: str = "NoRecipeNameSet",
                 description: str = "NoRecipeDescriptionSet",
                 dateCreated: str = "NoDateSet",
                 axes: axes3DSpec = nullAxes(),
                 tool: toolSpec = nullTool(),
                 seqList: list = None,
                 __verbose__: bool = 0, **kwargs):

        """*Initializes recipe object*.

        Parameters
        ----------
        name: String
        description: String
        dateCreated: String
        path: Path
        axes: axes3DSpec
        tool: toolSpec
        dictParams: dict
        __verbose__: bool
        """

        # Pass in active axes/tool, other params
        self.dateCreated = dateCreated
        self.description = description
        self.name = name
        self.axes = axes
        self.tool = tool
        self.__verbose__ = __verbose__
        self.seqList = seqList
        self.cmdList = []  # For storing generated commands
        super().__init__(**kwargs)

    ################### Sequence Manipulation ###########################
    def addSeq(self, beforeIndex: int, newSeq: sequenceSpec):
        """*Adds a copy of the provided sequence to the seqList*.
        Parameters
        ----------
        beforeIndex: int
        newSeq: sequenceSpec

        """
        # Step 1 Back up sequence list
        seqListBackup = self.seqList.copy()

        # Step 2 Attempt to add sequence, if fails revert seqList
        try:
            self.seqList.insert(beforeIndex, newSeq)
            seqListBackup = None  # Wipes backup label
            return [1, "Add successful"]
        except Exception as inst:
            print("\t\tError adding sequence to active recipe, restoring recipe to previous state.")
            logging.exception(inst)
            self.seqList = seqListBackup
            return [0, "Add failed"]

    def deleteSeq(self, index: int):
        """*Adds a copy of the provided sequence to the seqList*.
        Parameters
        ----------
        index: int

        """
        # Step 1 Back up sequence list
        seqListBackup = self.seqList.copy()

        # Step 2 Attempt to remove sequence, if fails revert seqList
        try:
            del self.seqList[index]
            seqListBackup = None  # Wipes backup label
            return [1, "Delete successful"]
        except Exception as inst:
            print("\t\tError removing sequence from active recipe, restoring recipe to previous state.")
            logging.exception(inst)
            self.seqList = seqListBackup
            return [0, "Remove failed"]

    def reorderSeq(self, currentIndex: int, newIndex: int):
        """*Moves sequence from currentIndex to newIndex in seqList*.
        Parameters
        ----------
        currentIndex: int
        newIndex: int

        """
        # Step 1 Back up sequence list
        seqListBackup = self.seqList.copy()

        # Step 2 Attempt to move sequence, if fails revert seqList
        try:
            seqTemp = self.seqList[currentIndex]
            del self.seqList[currentIndex]
            self.seqList.insert(newIndex, seqTemp)
            seqListBackup = None  # Wipes backup label
            return [True, "Sequence move successful"]
        except Exception as inst:
            print("\t\tError moving sequence within recipe, restoring recipe to previous state.")
            logging.exception(inst)
            self.seqList = seqListBackup
            return [False, "Sequence reordering failed"]

    ################### Recipe Actions ###################################
    def operateRecipe(self, axesIn, toolIn):
        """*Performs print sequence*.
        Returns
        -------
        bool
            Whether recipe successfully completed or not
        """
        axes = axesIn
        tool = toolIn

        try:
            for line in self.cmdList:
                eval(line)
            return True

        except KeyboardInterrupt:
            print("\tTerminated by User....")
            return False
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    def genRecipe(self):
        """*Loads print sequence into a list into cmdList attribute*.

        Returns
        -------
        bool
            whether successfully reached the end or not
        """
        try:
            for seq in self.seqList:
                seqCmds = seq.genSequence()
                self.cmdList = self.cmdList + seqCmds
            return True

        except KeyboardInterrupt:
            print("\tTerminated by User...")
            return False
        except Exception as inst:
            print("\tCould not convert sequences into python commands...")
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


class recipeStub(fileHandler):
    """Class for recipe stubs, just the name, description, path info"""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self,
                 name: str = "NoRecipeNameSet",
                 description: str = "NoRecipeDescriptionSet",
                 dateCreated: str = "NoDateSet",
                 **kwargs):
        """*Initializes recipe object*.

        Parameters
        ----------
        name: String
        description: String
        __verbose__: bool
        """

        # Pass in active axes/tool, other params
        self.description = description
        self.name = name
        self.dateCreated = dateCreated
        super().__init__(**kwargs)
