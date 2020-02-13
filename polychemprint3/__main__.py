# -*- coding: utf-8 -*-
"""Runs the command line interface and 'executes' the program.

| First created on Sat Oct 19 21:56:15 2019
| Revised: 30/11/2019 00:34:27
| Author: Bijal Patel

"""
#############################################################################
### Import Statements
#############################################################################
import sys
from polychemprint3.commandLineInterface.ioMenuSpec import ioMenuSpec
from polychemprint3.commandLineInterface.ioTextPanel import ioTextPanel
from polychemprint3.axes.nullAxes import nullAxes
from polychemprint3.tools.nullTool import nullTool
import logging
import os
import importlib
# import time
from pathlib import Path
from colorama import init, Fore, Style


#############################################################################
### Menu Classes
#############################################################################
class ioMenu_0Main(ioMenuSpec):
    """Contains data and methods for implemented Main Menu."""

    def __init__(self, **kwargs):
        """*Initializes Main Menu Object*."""
        kwargs = {'name': 'Main',
                  'menuTitle': 'Main Menu', 'menuItems':
                      {Fore.LIGHTRED_EX + "[q]": Fore.LIGHTRED_EX + "Quit",
                       Fore.LIGHTMAGENTA_EX + "[?]":
                           Fore.LIGHTMAGENTA_EX + "List Commands",
                       Fore.WHITE + "[T] Test Code":
                           Fore.WHITE + "Run Test Code",
                       Fore.WHITE + "(2) GCode File Menu":
                           Fore.WHITE + "Generate sequence from a GCODE file",
                       Fore.WHITE + "(1) Hardware Control Menu":
                           Fore.WHITE + "Directly control hardware",
                       Fore.WHITE + "(0) Configuration/About":
                           Fore.WHITE
                           + "Software setup, options, Tool/Axes",
                       Fore.WHITE + "(4) Recipe Menu":
                           Fore.WHITE
                           + "Build/Execute Multi-Sequence Programs",
                       Fore.WHITE + "(3) Sequence Menu":
                           Fore.WHITE
                           + "Print/Configure pre-defined commands"}}
        super().__init__(**kwargs)

    def io_Operate(self):
        """*Performs Menu operations - loops*.

        Returns
        -------
            String
                title of next menu to call
        """
        global __savedInp__
        global __lastInp__
        # Menu Loop
        doQuitMenu = False
        promptIn = True

        while not doQuitMenu:
            try:
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()
                if promptIn:
                    choiceString = io_Prompt("Enter Command:", validate=True,
                                             validResponse=["q",
                                                            "?",
                                                            "T",
                                                            "0",
                                                            "1",
                                                            "2",
                                                            "3",
                                                            "4",
                                                            "/",
                                                            ".",
                                                            ","]).lower()

                if not (choiceString in ["/", ".", ","]):
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)

                if choiceString in ["/", ".", ","]:
                    (choiceString, promptIn) = io_savedCmdOps(choiceString)
                elif choiceString == '?':
                    pass
                elif choiceString == 'q':
                    return 'quit'
                elif choiceString.lower() == 't':
                    io_TestCode()
                    promptIn = True
                elif choiceString == '0':
                    return 'M1ConfigurationMenu'
                elif choiceString == '1':
                    return 'M1HardwareMenu'
                elif choiceString == '2':
                    return 'M1PrintFile'
                elif choiceString == '3':
                    return 'M1PrintSequence'
                elif choiceString == '4':
                    return 'M1PrintRecipe'

                else:
                    print("Received: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
                    promptIn = True
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")


class ioMenu_1Configuration(ioMenuSpec):
    """Contains data and methods for implemented Configuration Menu."""

    def __init__(self, **kwargs):
        """*Initializes Configuration Menu Object*."""
        kwargs = {'name': 'ConfigurationMenu',
                  'menuTitle': 'Configuration/About Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                Fore.WHITE + "(0) Info and License":
                                    Fore.WHITE
                                    + "View Program Details and License Text",
                                Fore.WHITE + "(1) Verbose":
                                    Fore.WHITE
                                    + "Toggles level of output details",
                                Fore.WHITE + "(2) Change Axes":
                                    Fore.LIGHTYELLOW_EX
                                    + "Current Axes: " + axes.name,
                                Fore.WHITE + "(3) Change Tool":
                                    Fore.LIGHTYELLOW_EX
                                    + "Current Tool: " + tool.name}}
        super().__init__(**kwargs)

    def io_Operate(self):
        """*Performs Menu operations - loops*.

        Returns
        -------
            String
                title of next menu to call
        """
        global __savedInp__
        global __lastInp__
        global __verbose__
        global tool
        global axes

        # Menu Loop
        doQuitMenu = False
        promptIn = True

        while not doQuitMenu:
            try:
                self.__init__()
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()
                if promptIn:
                    choiceString = io_Prompt("Enter Command:", validate=True,
                                             validResponse=["q", "?", "0",
                                                            "1", "2", "3", "/",
                                                            ".", ","]).lower()

                if not (choiceString in ["/", ".", ","]):
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)

                if choiceString in ["/", ".", ","]:
                    (choiceString, promptIn) = io_savedCmdOps(choiceString)
                elif choiceString == '?':
                    pass
                elif choiceString == 'q':
                    return 'M0MainMenu'
                elif choiceString.lower() == '0':  # Show Log
                    print("\t\tPolyChemPrint3 v" + str(__version__)
                          + "\n\t\t" + str(__date__)
                          + "\n\t\tBy Bijal Patel bbpatel2@illinois.edu")
                    print("\n\t\tProvided under the University of Illinois"
                          "/NCSA\nOpen Source License\n")
                    panelTitle = 'License'
                    filePath = __textDict__.get(panelTitle)
                    licensePanel = ioTextPanel(panelTitle, filePath)
                    licensePanel.io_Operate()
                elif choiceString == '1':
                    __verbose__ = 1 - __verbose__
                    if __verbose__:
                        print("\tMore Details will be displayed.")
                    else:
                        print("\tFewer Details will be displayed.")
                elif choiceString == '2':  # Change Axes
                    print("\t\tCurrently loaded Axes: ")
                    for axesCode in __axesDict__:  # Prompt User
                        axesobj = __axesDict__.get(axesCode)
                        axesName = axesobj.name
                        print("\t\t(%-3s) %-10s" %
                              (axesCode, axesName))

                    subChoice = io_Prompt("Enter device to make active",
                                          validate=True,
                                          validResponse=[*__axesDict__])
                    newAxes = __axesDict__.get(subChoice)
                    oldAxes = axes
                    try:
                        print("\t\tDeactivating old Axes...")
                        deactiv = oldAxes.deactivate()
                        print("\t\tActivating new Axes...")
                        axes = newAxes
                        activ = axes.activate()
                        if deactiv == 1 and activ == 1:
                            print("\t\tAxes Changed and activated Succesfully")
                        else:
                            print("\t\tError loading Axes, old Axes restored")
                            axes = oldAxes
                    except Exception as inst:
                        print("\t\tError loading new Axes, old Axes restored")
                        logging.exception(inst)
                        axes = oldAxes

                elif choiceString == '3':  # Change Tool
                    print("\t\tCurrently loaded Tools: ")
                    for toolCode in __toolDict__:  # Prompt User
                        toolobj = __toolDict__.get(toolCode)
                        toolName = toolobj.name
                        print("\t\t(%-3s) %-10s" % (toolCode, toolName))

                    subChoice = io_Prompt("Enter device to make active",
                                          validate=True,
                                          validResponse=[*__toolDict__])
                    newtool = __toolDict__.get(subChoice)
                    oldtool = tool
                    try:  # TODO Implement validation of tool working here
                        print("\t\tDeactivating old Tool...")
                        oldtool.deactivate()
                        print("\t\tActivating new Tool...")
                        tool = newtool
                        tool.activate()
                        print("\t\tTool Changed and activated Succesfully")
                    except Exception as inst:
                        print("\t\tError loading new tool, old tool restored")
                        logging.exception(inst)
                        tool = oldtool
                else:
                    print("Received: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
                    promptIn = True
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")


class ioMenu_1Hardware(ioMenuSpec):
    """Contains data and methods for implemented Hardware Menu."""

    def __init__(self, **kwargs):
        """*Initializes Hardware Menu Object*."""
        kwargs = {'name': 'HardwareMenu',
                  'menuTitle': 'Hardware Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                Fore.LIGHTRED_EX + "STOP":
                                    Fore.LIGHTRED_EX + "Emergency STOP",
                                Fore.WHITE + "a,d;r,f;s,w;x,z":
                                    Fore.WHITE
                                    + "Jog -+ 1mm (X; Y; Z; Z-0.1,-.01)",
                                Fore.WHITE + "(0) Clean Routine":
                                    Fore.WHITE + "Lift up 20 mm, lower on cmd",
                                Fore.WHITE + "(1) Lift Tool":
                                    Fore.WHITE + "Lift up 20 mm",
                                Fore.WHITE + "(2) Ext":
                                    Fore.WHITE + "Send commands to Tool",
                                Fore.WHITE + "(3) Sequences":
                                    Fore.WHITE + "Go to sequences menu",
                                Fore.WHITE + "(4) PrintFile":
                                    Fore.WHITE + "Go to printFile menu"}}
        super().__init__(**kwargs)

    ### ioMenuSpec METHODS
    def io_Operate(self):
        """*Performs Menu operations - loops*.

        Returns
        -------
            String
                title of next menu to call
        """
        io_Prompt("This is filler, enter any key to go back to main menu")
        return 'M0MainMenu'


class ioMenu_1PrintFile(ioMenuSpec):
    """Contains data and methods for implemented Print File Menu."""

    def __init__(self, **kwargs):
        """*Initializes PrintFile Menu Object*."""
        kwargs = {'name': 'PrintFileMenu',
                  'menuTitle': 'Print File Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                "STOP": "Emergency STOP",
                                "a,d;r,f;w,s;x,z": "Jog (X; Y; Z; Zsmall)",
                                "(0) SetZero": "Perform Origin set sequence",
                                "(1) PickFile": "Pick a GCODE file",
                                "(2) PrintFile": "Execute print sequence",
                                "(3) FileText": "Display GCODE file"}}

        super().__init__(**kwargs)

    def io_Operate(self):
        """*Performs Menu operations - loops*.

        Returns
        -------
            String
                title of next menu to call
        """
        io_Prompt("This is filler, enter any key to go back to main menu")
        return 'M0MainMenu'


class ioMenu_2AxesOrigin(ioMenuSpec):
    """Contains data and methods for implemented AxesOrigin Menu."""

    def __init__(self, **kwargs):
        """*Initializes PrintFile Menu Object*.

        Performs Menu operations - loops*.

        Returns
        -------
            String
                title of next menu to call
        """
        kwargs = {'name': 'AxesOriginSet',
                  'menuTitle': 'Axes Origin Set Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                "STOP": "Emergency STOP",
                                "a,d;r,f;w,s;x,z": "Jog (X; Y; Z; Zsmall)",
                                "Done": "Tip is at 0,0,0"}}
        super().__init__(**kwargs)

    def io_Operate(self):
        """*Performs Menu operations - loops*.

        Returns
        -------
            String
                title of next menu to call
        """
        io_Prompt("This is filler, enter any key to go back to main menu")
        return 'M0MainMenu'


class ioMenu_2PrintFileOptions(ioMenuSpec):
    """Contains data and methods for implemented PrintFileOptions Menu."""

    def __init__(self, **kwargs):
        """*Initializes PrintFileOptions Menu Object*."""
        kwargs = {'name': 'PrintFileOptionsMenu',
                  'menuTitle': 'Print File Options Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                "L": "Advanced Log Options",
                                "(9) Execute": "Start print sequence",
                                "(6) GenCmds": "Generate command arrays",
                                "(8) DispCode": "Display printing code",
                                "(7) DispCmds": "Display current commands",
                                "(0) Clean": "raise/lower 20mm",
                                "(1) Hardware": "Go to hardware menu",
                                "(2) Plot":
                                    "Select Plotter Mode (No Extruder))",
                                "(3) ConstPres":
                                    "Select Constant Dispense Pressure Mode",
                                "(4) VarPres":
                                    "Select Variable Dispense Pressure Mode"}}
        super().__init__(**kwargs)

    def io_Operate(self):
        """*Performs Menu operations - loops*.

        Returns
        -------
        String
            title of next menu to call
        """
        io_Prompt("This is filler text, enter any key to go back to main menu")
        return 'M0MainMenu'


class ioMenu_1PrintSequence(ioMenuSpec):
    """Contains data and methods for implemented PrintSequence Menu."""

    def __init__(self, **kwargs):
        """*Initializes Print Sequence Menu Object*."""
        kwargs = {'name': 'PrintSequenceMenu',
                  'menuTitle': 'Print Sequence Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                Fore.WHITE + "L": "Advanced Log Options",
                                Fore.WHITE + "(1) hardware":
                                    "Go to hardware menu"
                                }}
        super().__init__(**kwargs)

    def ioMenu_printMenu(self):
        """*Prints formatted menu options from menuItems dict*."""
        # Need to generate menu items and actions based on shapes loaded in
        # For now just 1 big list

        seqDictMenu = {}  # Contains name: filename pairs

        for seq in __seqDict__:
            fileName = __seqDict__.get(seq)
            seqDictMenu.update({seq: fileName})

        print(Style.RESET_ALL)
        print("-" * 100)
        print("###\t" + self.menuTitle)
        print("-" * 100)

        # Print sequences
        print(Fore.LIGHTGREEN_EX + "\n\tLoaded Sequences:")
        for seqNum in __seqDict__:
            seqName = __seqDict__.get(seqNum).nameString
            seqDescription = __seqDict__.get(seqNum).descrip
            print("\t(%s) %-10s|  %-55s" % (seqNum, seqName, seqDescription))

        print(Style.RESET_ALL)
        # Print std menu options
        for key in sorted(self.menuItems):
            print("\t%-40s|  %-25s" % (key, self.menuItems.get(key)))
        print(Style.RESET_ALL)

        storedCmds = {Fore.LIGHTCYAN_EX
                      + "[/] Repeat Last Command": self.lastCmd,
                      Fore.LIGHTCYAN_EX
                      + "[.] Repeat Saved Command": self.memCmd,
                      Fore.LIGHTCYAN_EX
                      + "[,] Store Saved Command": "Will Prompt for command"}

        for key in storedCmds:
            print("\t%-40s|  %-25s" % (key, storedCmds.get(key)))
        print(Style.RESET_ALL)

    def io_Operate(self):
        """*Performs Menu operations - loops*.

        Returns
        -------
            String
                title of next menu to call
        """
        global __savedInp__
        global __lastInp__
        # Menu Loop
        doQuitMenu = False
        promptIn = True

        while not doQuitMenu:
            try:
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()
                # List of sequences as strings
                stringList = []
                for x in [*__seqDict__]:
                    stringList.append(str(x))

                if promptIn:
                    choiceString = io_Prompt(
                        "Enter Command:", validate=True,
                        validResponse=(["q", "?", "1", "/", ".", ","]
                                       + stringList)).lower()

                if not (choiceString in ["/", ".", ","]):
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)

                if choiceString in ["/", ".", ","]:
                    (choiceString, promptIn) = io_savedCmdOps(choiceString)
                elif choiceString == '?':
                    pass
                elif choiceString == 'q':
                    return 'M0MainMenu'
                elif choiceString == '1':
                    return 'M1HardwareMenu'
                elif choiceString.upper() in stringList:
                    # Instantiate Sequence menu
                    seqMen = ioMenu_2SequenceOptions(choiceString.upper())
                    seqMen.io_Operate()
                else:
                    print("\tReceived: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
                    promptIn = True
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")


class ioMenu_2SequenceOptions(ioMenuSpec):
    """Contains data and methods for print sequence options Menu."""

    def __init__(self, seqNum, **kwargs):
        """*Initializes Print Sequence Options Menu Object*.

        Parameters
        ----------
        seqNum: String
            Refers to particular sequence object being modified by menu item
        """
        self.seqNum = seqNum
        self.seq = __seqDict__.get(seqNum)
        self.paramsMenuDict = {}  # ParamID:  Param

        menuItems = {Fore.LIGHTRED_EX + "[q]": Fore.LIGHTRED_EX + "Quit",
                     Fore.LIGHTYELLOW_EX + "[PRIME]":
                         Fore.LIGHTYELLOW_EX + "Generate Print Commands",
                     Fore.LIGHTYELLOW_EX + "[VIEW]":
                         Fore.LIGHTYELLOW_EX + "View Print Commands",
                     Fore.LIGHTGREEN_EX + "[GO]":
                         Fore.LIGHTGREEN_EX + "Engage Print Sequence"}
        print(Style.RESET_ALL)

        kwargs = {'name': self.seq.dictParams.get("name").value,
                  'menuTitle': "Sequence: "
                  + self.seq.dictParams.get("name").value,
                  'menuItems': menuItems}
        super().__init__(**kwargs)

    def ioMenu_printMenu(self):
        """*Prints formatted menu options from menuItems dict*."""
        print(Style.RESET_ALL)
        print("-" * 100)
        print("###\t" + self.menuTitle)
        print("-" * 100)

        self.paramsMenuDict = {}  # reset params menu dict
        # First map params onto param number for menu
        paramNum = 1
        for paramName in self.seq.dictParams:
            param = self.seq.dictParams.get(paramName)
            self.paramsMenuDict.update({"P" + str(paramNum): param})
            paramNum += 1

        paramStrings = []
        # Then create formatted menu strings
        for pNum in self.paramsMenuDict:
            param = self.paramsMenuDict.get(pNum)
            paramStrings.append(
                "\t(%-3s) %-20s| %-15s| %-7s| %-30s"
                % (str(pNum), param.name, param.value, param.unit,
                   param.helpString))

        # Print param menu options
        print("\tEnter Parameter number to modify:")
        for outString in paramStrings:
            print(outString)

        print(Style.RESET_ALL)
        # Print std menu options
        for key in sorted(self.menuItems):
            print("\t%-40s|  %-25s" % (key, self.menuItems.get(key)))
        print(Style.RESET_ALL)

        storedCmds = {Fore.LIGHTCYAN_EX
                      + "[/] Repeat Last Command": self.lastCmd,
                      Fore.LIGHTCYAN_EX
                      + "[.] Repeat Saved Command": self.memCmd,
                      Fore.LIGHTCYAN_EX
                      + "[,] Store Saved Command": "Will Prompt for command"}

        for key in storedCmds:
            print("\t%-40s|  %-25s" % (key, storedCmds.get(key)))
        print(Style.RESET_ALL)

    def io_Operate(self):
        """*Performs Menu operations - loops*.

        Returns
        -------
            String
                title of next menu to call
        """
        global __savedInp__
        global __lastInp__
        # Menu Loop
        doQuitMenu = False
        promptIn = True
        isPrimed = False

        while not doQuitMenu:
            try:
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()

                # List of param options as strings
                paramOptionList = []
                for x in [*self.paramsMenuDict]:
                    paramOptionList.append(str(x))

                if promptIn:
                    choiceString = io_Prompt(
                        "Enter Command:",
                        validate=True,
                        validResponse=["q", "/", ".", ",",
                                       "PRIME", "VIEW", "GO"]
                        + paramOptionList).lower()

                if not (choiceString in ["/", ".", ","]):
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)

                if choiceString in ["/", ".", ","]:
                    (choiceString, promptIn) = io_savedCmdOps(choiceString)
                elif choiceString == 'q':
                    return "M1PrintSequence"
                elif choiceString.upper() == 'PRIME':
                    # Prime [generate commands]
                    print("\tGenerating Print Commands...")
                    self.seq.genSequence()
                    isPrimed = True
                    print("\tCommands Generated!")
                elif choiceString.upper() == 'VIEW':
                    print("\tOutputting Python Commands:")
                    for line in self.seq.cmdList:
                        print(Fore.LIGHTMAGENTA_EX + "\t" + repr(line))
                    print(Style.RESET_ALL, end='')
                elif choiceString.upper() == 'GO':
                    if isPrimed:
                        print("\tExecuting Print! Ctrl + C to Cancel")
                        self.seq.operateSeq(tool, axes)
                        print("\tSequence Complete!")
                    else:
                        self.seq.genSequence()
                        isPrimed = True
                        print("\tCommands Generated!")
                        print("\tExecuting Print! Ctrl + C to Cancel")
                        self.seq.operateSeq(tool, axes)
                        print("\tSequence Complete!")
                elif choiceString.upper() in paramOptionList:
                    isPrimed = False
                    # Modify corresponding parameter
                    paramNum = choiceString.upper()
                    param = self.paramsMenuDict.get(paramNum)
                    print("\tModifying parameter %s: %s"
                          % (paramNum, param.name))
                    newVal = io_Prompt("Enter new value")
                    oldVal = param.value
                    param.value = newVal
                    print("Value changed from %s to %s"
                          % (oldVal, param.value))
                else:
                    print("\tReceived: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
                    promptIn = True
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")
                isPrimed = False

#############################################################################
### Start Sequence Methods
#############################################################################


def io_setupConsole():
    """*Resizes console window*."""
    osVers = sys.platform
    print("\tDetected OS: %s" % osVers)

    try:  # resizing window
        if sys.platform.startswith('win'):
            os.system("mode con cols=100 lines=2000")
        elif sys.platform.startswith('linux'):
            os.system("printf '\\e[8;40;100t'")
    except Exception:
        print("\tFailed to resize terminal")


def io_StartText():
    """*Displays start screen*."""
    print(("#" * 100) + "\n" + ("#" * 100))
    print("\tPolyChemPrint3 - Version:" + str(__version__)
          + "\tRevised: " + __date__)
    print(("#" * 100) + "\n" + ("#" * 100))


def io_preloadText():
    """*Displays start screen*."""
    print("#" * 100)
    print("\tStarting PolyChemPrint3 Load Sequence...")
    print("#" * 100)

#########################################################################
### IO Helper METHODS
#########################################################################


def io_TestCode():
    """*Executes a block of test code from main menu*."""
    print("\tBegin Test Code")
    print("\tEnd Test Code")


def io_Prompt(promptString, validate=False,
              validResponse=[''], caseSensitive=False):
    """*Prompts user for input and may validate against a list of options*.

    Parameters
    ----------
    promptString: String
        to display as prompt
    validate: Boolean
        for whether to validate input
    validResponse: list of strings
        valid input strings
    caseSensitive: Boolean
        whether prompt should be case sensitive

    Returns
    -------
    String
        inputString from user
    """
    global __lastInp__
    inString = input("\t" + promptString + '> ').rstrip()

    if validate:

        if not caseSensitive:
            validString = (inString.upper() in validResponse
                           or inString.lower() in validResponse)
        else:
            validString = inString in validResponse

        if not validString:
            print(Fore.LIGHTRED_EX + "\tNot a valid response, try again.\n"
                  + Style.RESET_ALL)
            inString = io_Prompt(promptString, validate, validResponse,
                                 caseSensitive)
        else:
            if not (inString in ["/"]):
                __lastInp__ = inString
    else:
        if not (inString in ["/"]):
            __lastInp__ = inString

    return inString


def io_savedCmdOps(inString):
    """*Executes a block of test code from main menu*.

    Returns
    -------
    String
        the String to feed back into the menu loop
    Boolean
        whether menu should prompt for input this cycle
    """
    global __lastInp__
    global __savedInp__
    promptIn = True
    outString = ''

    if inString == '/':
        if __lastInp__ in ["/", ",", "."]:
            print("\tNo Valid Command to Repeat")
            __lastInp__ = ""
        else:
            outString = __lastInp__
            promptIn = False

    elif inString == '.':
        if __savedInp__ in ["/", "."]:
            print("\tNo Valid Command to Repeat")
            __savedInp__ = ""
        else:
            inString = __savedInp__
            promptIn = False
    elif inString == ',':
        __savedInp__ = io_Prompt("Enter Command to Save:")

    else:
        print("Error")

    return outString, promptIn


def io_MenuManager(initialMenuString):
    """*Presents appropriate Menu in CLI depending on menuString - loops*.

    Parameters
    ----------
    initialMenuString: String
        telling which menu to begin on

    Returns
    -------
    menuFlag: String
        For quitting program
    """
    M0MainMenu = ioMenu_0Main()
    M1ConfigurationMenu = ioMenu_1Configuration()
    M1HardwareMenu = ioMenu_1Hardware()
    M1PrintFile = ioMenu_1PrintFile()
    M2AxesOrigin = ioMenu_2AxesOrigin()
    M2PrintFileOptions = ioMenu_2PrintFileOptions()
    M1PrintSequence = ioMenu_1PrintSequence()

    menuFlag = initialMenuString
    while not menuFlag == 'quit':
        # Switch on menuflags
        if menuFlag == 'M0MainMenu':
            M0MainMenu.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M0MainMenu.io_Operate()
        elif menuFlag == 'M1ConfigurationMenu':
            M1ConfigurationMenu.ioMenu_updateStoredCmds(__lastInp__,
                                                        __savedInp__)
            menuFlag = M1ConfigurationMenu.io_Operate()
        elif menuFlag == 'M1HardwareMenu':
            M1HardwareMenu.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M1HardwareMenu.io_Operate()
        elif menuFlag == 'M1PrintFile':
            M1PrintFile.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M1PrintFile.io_Operate()
        elif menuFlag == 'M2AxesOrigin':
            M2AxesOrigin.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M2AxesOrigin.io_Operate()
        elif menuFlag == 'M2PrintFileOptions':
            (M2PrintFileOptions.
             ioMenu_updateStoredCmds(__lastInp__, __savedInp__))
            menuFlag = M2PrintFileOptions.io_Operate()
        elif menuFlag == 'M1PrintSequence':
            M1PrintSequence.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M1PrintSequence.io_Operate()
        else:
            print(Fore.LIGHTRED_EX + "\tInternal CLI Error:"
                  + "Invalid flag returned from menu, resetting to main"
                  + Style.RESET_ALL)
            menuFlag = 'M0MainMenu'

    return menuFlag


def io_loadPCP(objType):
    """*Search for, instantiate, and load PCP objects into appropriate dict*.

    Parameters
    ----------
    objDir : Path
        Path object referring to directory where obj scripts are located
    """
    # Set type-specific values
    if objType == 'sequence':
        textCol = Fore.LIGHTGREEN_EX
        objDict = __seqDict__
        objCode = 'S'
        moduleDirString = "polychemprint3.sequence"
        objDir = __rootDir__ / 'sequence'
        print(textCol
              + "\tAttempting to load sequences from Sequence Folder...")
    elif objType == 'tools':
        textCol = Fore.LIGHTCYAN_EX
        objDict = __toolDict__
        objCode = 'T'
        moduleDirString = "polychemprint3.tools"
        objDir = __rootDir__ / 'tools'
        print(textCol
              + "\tAttempting to load tools from tools Folder...")
    elif objType == 'axes':
        textCol = Fore.LIGHTYELLOW_EX
        objCode = 'A'
        objDict = __axesDict__
        moduleDirString = "polychemprint3.axes"
        objDir = __rootDir__ / 'axes'
        print(textCol
              + "\tAttempting to load axes from axes Folder...")
    elif objType == 'user':
        textCol = Fore.LIGHTMAGENTA_EX
        objCode = 'U'
        objDict = __userDict__
        moduleDirString = "polychemprint3.user"
        objDir = __rootDir__ / 'user'
        print(textCol
              + "\tAttempting to load user profiles from user Folder...")
    else:
        textCol = Fore.WHITE
        objType = 'invalid'
        objCode = ''
        objDict = {}
        objDir = ''
        moduleDirString = ""
        print("\tInternal load error, invalid PCP type")

    filesInFolder = os.listdir(objDir)
    pcpObjFiles = []

    for name in filesInFolder:
        if (".py" in name[-3:]) and ("Spec"
                                     not in name) and ("init" not in name):
            pcpObjFiles.append(name)

    objValidDict = {}
    for objFile in pcpObjFiles:
        try:
            compile(open(objDir / objFile, 'r').read(), objFile, "exec")
            print('\t\t%-25s passes compile-time syntax check' % objFile)
            objValidDict.update({objFile[:-3]: objDir / objFile})
        except Exception:
            print(Fore.LIGHTRED_EX + '\t\t' + objFile
                  + "\tfailed syntax check" + textCol)

    # Instantiate all valid objects
    # Goal: Create object with variable name = class name and add to objList
    objNum = 1
    for objName in objValidDict:
        try:
            obj = getattr(importlib.import_module(moduleDirString + "."
                                                  + objName), objName)
            # Depends on object type
            vars()[objName] = obj(__verbose__=__verbose__, name=objName)
            objDict.update({"%s%s" % (objCode, objNum): vars()[objName]})
            objNum += 1
            print('\t\t%-25s loaded successfully' % (objName + ".py"))
        except Exception as inst:
            print(Fore.LIGHTRED_EX + '\t\t' + objName + "\tfailed to load"
                  + textCol)
            logging.exception(inst)

    if objType == 'sequence':
        print(Fore.LIGHTGREEN_EX + "\tFinished Loading Sequence Files..."
              + Style.RESET_ALL)
    elif objType == 'tools':
        print(Fore.LIGHTCYAN_EX + "\tFinished Loading Tool Files..."
              + Style.RESET_ALL)
    elif objType == 'axes':
        print(Fore.LIGHTYELLOW_EX + "\tFinished Loading Axes Files..."
              + Style.RESET_ALL)
    elif objType == 'user':
        print(Fore.LIGHTMAGENTA_EX + "\tFinished Loading User Files..."
              + Style.RESET_ALL)


#############################################################################
### Global attributes
#############################################################################

# Program Details
__version__ = 3.0
__date__ = "2019/11/30"
__verbose__ = 1  # reflects how many status messages are shown
__rootDir__ = Path(__file__).absolute().parent

# User Input helper variables
__input__ = ""
__lastInp__ = ""
__savedInp__ = ""

# Instantiated Hardware
axes = nullAxes()
tool = nullTool()

# Instantiated Objects
__seqDict__ = {}
__toolDict__ = {}
__axesDict__ = {}
__userDict__ = {}

# Instantiated menus
M0MainMenu = ioMenu_0Main()
M1ConfigurationMenu = ioMenu_1Configuration()
M1HardwareMenu = ioMenu_1Hardware()
M1PrintFile = ioMenu_1PrintFile()
M2AxesOrigin = ioMenu_2AxesOrigin()
M2PrintFileOptions = ioMenu_2PrintFileOptions()
M1PrintSequence = ioMenu_1PrintSequence()
# Relative paths to text panels


__textDict__ = {'License': __rootDir__ / 'data' / 'TextPanels'
                / 'License.txt'}

#############################################################################
### Main METHOD
#############################################################################


def main():
    """*Runs program*."""
    logging.basicConfig(level=logging.DEBUG)  # logging
    init(convert=None)  # colorama

    # Perfom os-dependent terminal window resizing
    io_setupConsole()
    # Display pre-load text
    io_preloadText()
    # Load PCP Modules
    io_loadPCP('axes')
    io_loadPCP('tools')
    io_loadPCP('sequence')
    io_loadPCP('user')
    # Interface Start Sequencea
    io_StartText()
    # make software connections

    doQuitProgram = False
    # prevent ctrl+c from closing program
    while not doQuitProgram:

        try:

            # menuManagerSequence - loop that handles menu driving
            menuFlag = io_MenuManager(M0MainMenu.io_Operate())

            # if we get here, menumanager should have received quit message
            # Double check with user if they want to exit
            if menuFlag == 'quit':
                inp = io_Prompt(
                    promptString=("Really quit (Y,q)?"
                                  " or internal reset? (N): "),
                    validate=True, validResponse=["Y", "N", "q"],
                    caseSensitive=False)
                if inp.lower() == 'n':
                    main()
                else:
                    print('\tExiting Program - Goodbye!')
                    doQuitProgram = True

        except KeyboardInterrupt:
            print("\n Ctrl+C To exit program disabled."
                  "Enter q to close program\n")
        except Exception as inst:
            print("Error from Main Method\n")
            logging.exception(inst)

            inp = io_Prompt(promptString="Try an internal reset? (Y/N): ",
                            validate=True, validResponse=["Y", "N"],
                            caseSensitive=False)
            if inp.lower() == 'y':
                main()
            else:
                print('\tExiting Program - Goodbye!')
                doQuitProgram = True

    # Exit Sequence
    sys.exit()


if __name__ == "__main__":
    main()
