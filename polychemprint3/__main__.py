# -*- coding: utf-8 -*-
"""Runs the command line interface and 'executes' the program.

| First created on Sat Oct 19 21:56:15 2019
| Revised: 30/11/2019 00:34:27
| Author: Bijal Patel

"""
# Import Statements ##########################################################
# General Imports
import copy
import sys
from datetime import datetime

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkfilebrowser import askopenfilenames
import logging
import os
import importlib
from pathlib import Path
from colorama import init, Fore, Style
import textwrap

# Internal PCP3 Imports
from polychemprint3.commandLineInterface.ioMenuSpec import ioMenuSpec
from polychemprint3.commandLineInterface.ioTextPanel import ioTextPanel
from polychemprint3.axes.nullAxes import nullAxes
from polychemprint3.recipes.recipe import recipe, recipeStub
from polychemprint3.sequence.sequenceSpec import sequenceSpec
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.utility.fileHandler import fileHandler


# Menu Classes ###############################################################
class ioMenu_0Main(ioMenuSpec):
    """The main menu is the root of the PCP3 command-line interface."""

    def __init__(self, **kwargs):
        """Initializes Main Menu Object."""
        kwargs = {'name': 'Main',
                  'menuTitle': 'Main Menu',
                  'menuDesc': 'the root of the PCP3 command-line interface.',
                  'menuItems':
                      {Fore.LIGHTRED_EX + "[q]": Fore.LIGHTRED_EX + "Quit",
                       Fore.LIGHTMAGENTA_EX + "[?]":
                           Fore.LIGHTMAGENTA_EX + "Repeat menu options",
                       Fore.WHITE + "[T] Test Code":
                           Fore.WHITE + "Run test code",
                       Fore.WHITE + "(1) Hardware Control Menu":
                           Fore.WHITE + "Send commands directly to hardware "
                                        "and execute active sequence/recipes",
                       Fore.WHITE + "(0) Configuration/About":
                           Fore.WHITE
                           + "Software setup, options, choose Tool/Axes",
                       Fore.WHITE + "(3) Recipe Menu":
                           Fore.WHITE
                           + "Configure/Activate multi-sequence recipes",
                       Fore.WHITE + "(2) Sequence Menu":
                           Fore.WHITE
                           + "Configure/Activate predefined command "
                             "sequences"}}
        super().__init__(**kwargs)

    def io_Operate(self):
        """Performs Menu operations - loops.

        Returns
        -------
            String
                title of next menu to call
        """
        global __savedInp__
        global __lastInp__
        # Menu Loop
        doQuitMenu = False

        while not doQuitMenu:
            try:
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()
                choiceString = io_Prompt("Enter Command:", validate=True,
                                         validResponse=["q", "?", "T",
                                                        "0", "1", "2", "3",
                                                        "/", ".", ","
                                                        ]).lower()

                if choiceString in ["/", ".", ","]:
                    choiceString = io_savedCmdOps(choiceString)
                else:
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                if choiceString == '?':
                    pass
                elif choiceString == 'q':
                    return 'quit'
                elif choiceString.lower() == 't':
                    io_TestCode()
                elif choiceString == '0':
                    return 'M1ConfigurationMenu'
                elif choiceString == '1':
                    return 'M1HardwareMenu'
                elif choiceString == '2':
                    return 'M1PrintSequence'
                elif choiceString == '3':
                    return 'M1PrintRecipe'
                else:
                    print("Received: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid choice, resetting menu..."
                          + Style.RESET_ALL)
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu...")


class ioMenu_1Configuration(ioMenuSpec):
    """Contains data and methods for implemented Configuration Menu."""

    def __init__(self, **kwargs):
        """Initializes Configuration Menu Object."""
        kwargs = {
            'name': 'ConfigurationMenu',
            'menuTitle': 'Configuration/About Menu',
            'menuItems': {
                Fore.LIGHTRED_EX + "[q]": Fore.LIGHTRED_EX + "Quit",
                Fore.LIGHTMAGENTA_EX + "[?]":
                    Fore.LIGHTMAGENTA_EX + "List Commands",
                Fore.WHITE + "(0) Info and License":
                    Fore.WHITE + "View Program Details and License Text",
                Fore.WHITE + "(1) Verbose":
                    Fore.WHITE + "Toggles level of output details",
                Fore.WHITE + "(2) Change Axes":
                    Fore.LIGHTYELLOW_EX + "Current Axes: " + axes.name,
                Fore.WHITE + "(3) Change Tool":
                    Fore.LIGHTYELLOW_EX + "Current Tool: " + tool.name}}
        super().__init__(**kwargs)

    def io_Operate(self):
        """Performs Menu operations - loops.

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

        while not doQuitMenu:
            try:
                self.__init__()
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()
                choiceString = io_Prompt("Enter Command:", validate=True,
                                         validResponse=["q", "?", "0",
                                                        "1", "2", "3", "/",
                                                        ".", ","]).lower()

                if choiceString in ["/", ".", ","]:
                    choiceString = io_savedCmdOps(choiceString)
                else:
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                if choiceString == '?':
                    pass
                elif choiceString == 'q':
                    return 'M0MainMenu'
                elif choiceString.lower() == '0':  # Show Log
                    print("\n\tPolyChemPrint3 v" + str(__version__)
                          + "\n\t" + str(__date__)
                          + "\n\tBy Bijal Patel bbpatel2@illinois.edu")

                    citationString = "Patel, B. B.; Chang, Y.; Park, S. K.; Wang, S.; Rosheck, J.; Patel, K.; Walsh, " \
                                     "D.; Guironnet, D.; Diao, Y. PolyChemPrint: A Hardware and Software Framework " \
                                     "for Benchtop Additive Manufacturing of Functional Polymeric Materials. Journal " \
                                     "of Polymer Science 2021. "
                    citationList = textwrap.wrap(citationString,width=70)
                    print("\n\tIf this program has been of value to your work, please cite the following:\n")
                    for line in citationList:
                        print("\t" + str(line))
                    print("\n\thttps://doi.org/10.1002/pol.20210086")
                    print("\n\tProvided under the University of Illinois"
                          "/NCSA\n\tOpen Source License\n")
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
                    for axesCode in sorted(__axesDict__):  # Prompt User
                        axesobj = __axesDict__.get(axesCode)
                        axesName = axesobj.name
                        print("\t\t(%-3s) %-10s" %
                              (axesCode, axesName))

                    subChoice = io_Prompt("Enter device to make active",
                                          validate=True,
                                          validResponse=[*__axesDict__, 'q'],
                                          caseSensitive=False)
                    # Make uppercase
                    subChoice = subChoice.upper()
                    newAxes = __axesDict__.get(subChoice)
                    oldAxes = axes
                    if not subChoice == 'Q':
                        try:
                            print("\t\tDeactivating old Axes...")
                            deactiv = oldAxes.deactivate()
                            print("\t\tActivating new Axes...")
                            axes = newAxes
                            activ = axes.activate()
                            if deactiv == 1 and activ == 1:
                                print(
                                    "\t\tAxes Changed and Activated "
                                    "Successfully!")
                                for seq in __seqDict__.values():
                                    seq.tool = tool
                                    seq.axes = axes

                            else:
                                print("\t\tError loading Axes, old Axes "
                                      "restored")
                                axes = oldAxes
                        except Exception as inst:
                            print("\t\tError loading new Axes, old Axes "
                                  "restored")
                            logging.exception(inst)
                            axes = oldAxes

                elif choiceString == '3':  # Change Tool
                    print("\t\tCurrently loaded Tools: ")
                    for toolCode in sorted(__toolDict__):  # Prompt User
                        toolobj = __toolDict__.get(toolCode)
                        toolName = toolobj.name
                        print("\t\t(%-3s) %-10s" % (toolCode, toolName))

                    subChoice = io_Prompt(
                        "Enter device to make active, q to quit",
                        validate=True,
                        validResponse=[*__toolDict__, 'q'],
                        caseSensitive=False)
                    # make uppercase
                    subChoice = subChoice.upper()
                    if not subChoice == 'Q':
                        newtool = __toolDict__.get(subChoice)
                        oldtool = tool
                        try:
                            print("\t\tDeactivating old Tool...")
                            oldtool.deactivate()
                            print("\t\tActivating new Tool...")
                            tool = newtool
                            if tool.activate():
                                print("\t\tTool changed and activated "
                                      "succesfully!")
                            else:
                                print("\t\tError loading new tool, old tool "
                                      "restored")
                                tool = oldtool

                        except Exception as inst:
                            print("\t\tError loading new tool, old tool "
                                  "restored")
                            logging.exception(inst)
                            tool = oldtool
                else:
                    print("Received: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")


class ioMenu_1Hardware(ioMenuSpec):
    """The hardware menu allows for direct control of hardware and for
    launching the active sequence or recipe."""

    def __init__(self, **kwargs):
        """Initializes Hardware Menu Object."""
        kwargs = {'name': 'HardwareMenu',
                  'menuTitle': 'Hardware Control Menu',
                  'menuDesc': "Allows for direct control of hardware and "
                              "launching the active sequence or recipe.",
                  'menuInstruc': Fore.WHITE + "Choose an execution option "
                                              "or directly enter a GCODE "
                                              "command for the axes. "
                                 + Fore.RED
                                 + '\n\tBe careful! There is '
                                   'limited error-checking!'
                                 + Style.RESET_ALL,
                  'menuItems': {
                      Fore.LIGHTRED_EX + "[q]":
                          Fore.LIGHTRED_EX + "Quit",
                      Fore.LIGHTMAGENTA_EX + "[?]":
                          Fore.LIGHTMAGENTA_EX + "List Commands",
                      Fore.WHITE + "[#SP, #SV, #SE, #SM]":
                          Fore.WHITE + "Prime, View, Execute, or Modify "
                                       "Active Sequence",
                      Fore.YELLOW + "a,d; r,f; s,w":
                          Fore.YELLOW + "Coarse Jog -,+ 1mm in X; Y; Z",
                      Fore.YELLOW + "x,z; c,v":
                          Fore.YELLOW + "Fine Jog in Z [-0.1, -0.01; +0.1, "
                                        "+ 0.01] mm",
                      Fore.WHITE + "(1) Clean Routine":
                          Fore.WHITE + "Lift up 20 mm, lower on cmd",
                      Fore.WHITE + "(2) Lift Tool":
                          Fore.WHITE + "Lift up 20 mm",
                      Fore.WHITE + "(3) Bring Bed Forward/Back":
                          Fore.WHITE + "Bring bed forward Y+50 mm, return on "
                                       "cmd",
                      Fore.GREEN + "Ton":
                          Fore.GREEN + "Engage Tool Dispense",
                      Fore.GREEN + "Toff":
                          Fore.GREEN + "Disengage Tool Dispense",
                      Fore.GREEN + "T[Value]":
                          Fore.GREEN + "Sets the tool value",
                      Fore.WHITE + "[#MS, #MR]":
                          Fore.WHITE + "Quick Switch to Sequence or Recipe "
                                       "Menus"
                  }}
        super().__init__(**kwargs)

    # ioMenuSpec METHODS #####################################################
    def io_Operate(self):
        """Performs menu operations and loops on user input.

        Returns
        -------
            str
                Title of next menu to call
        """
        # Pull in global values
        global __savedInp__
        global __lastInp__
        global __verbose__
        global tool
        global axes
        global __activeRecipe__
        global __activeSequence__

        # Menu Loop Variables
        doQuitMenu = False
        isSeqPrimed = False
        isRecPrimed = False

        # Loop until user wants to quit or a return is made
        while not doQuitMenu:
            try:
                # Initialize and display menu
                print('\tSetting Axes to relative positioning...')
                axes.setPosMode('relative')
                self.__init__()
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()
                # Prompt user for menu option and force to lowercase
                choiceString = io_Prompt("Enter Command:", validate=False,
                                         validResponse=[]).lower()
                # Operate based on user input
                # If action is based on saved command, pass to the saved
                # command helper function
                if choiceString in ["/", ".", ","]:
                    choiceString = io_savedCmdOps(choiceString)
                # Otherwise save this command as the last command.
                else:
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                # Check if it is a tool command
                if choiceString[:1] == 't':  # Tool command
                    # If it is the tool on, engage the tool
                    if choiceString == 'ton':
                        print("\tEngaging Tool")
                        print("\t" + tool.engage()[1])
                    # Else if it's tool off, disengage the tool
                    elif choiceString == 'toff':
                        print("\tDisengaging Tool")
                        print("\t" + tool.disengage()[1])
                    # Else pass the rest of the string as the tool value
                    else:
                        tool.setValue(choiceString[1:])
                # If the user wants to repeat the menu
                elif choiceString == '?':
                    pass
                # If the user wants to quit the menu
                elif choiceString == 'q':
                    return 'M0MainMenu'
                # If the user wants to do an operation on the active sequence
                elif choiceString in ['#sp', '#sv', '#se', '#sm']:
                    # If no active sequence, send back to the hardware menu
                    if __activeSequence__ is None:
                        print("\tNo active sequence, activate in the "
                              "sequence menu.")
                    # Prime Sequence [generate commands]
                    elif choiceString == '#sp':
                        print("\tGenerating print commands for the active "
                              "sequence...")
                        __activeSequence__.genSequence()
                        isSeqPrimed = True
                        print("\tCommands generated for the active sequence!")
                    # View Sequence [display commands]
                    elif choiceString == '#sv':
                        print("\tOutputting python commands for the active "
                              "sequence:")
                        if not isSeqPrimed:
                            __activeSequence__.genSequence()
                            isSeqPrimed = True
                        for line in __activeSequence__.cmdList:
                            print(Fore.LIGHTMAGENTA_EX + "\t" + repr(line))
                        print(Style.RESET_ALL, end='')
                    # Execute Sequence [display commands]
                    elif choiceString == '#se':
                        print("\tExecuting Print! Ctrl + C to Cancel")
                        if not isSeqPrimed:
                            __activeSequence__.genSequence()
                            isSeqPrimed = True
                        __activeSequence__.operateSeq()
                        print("\tSequence Complete!")
                    elif choiceString == '#sm':
                        isSeqPrimed = False
                        seqMen = ioMenu_2SequenceOptions(__activeSequence__)
                        seqMen.io_Operate()
                    else:  # Should never happen
                        pass
                # If the user wants to quick switch to another menu
                elif choiceString == '#ms':
                    return 'M1PrintSequence'
                elif choiceString == '#mr':
                    return 'M1PrintRecipe'
                # If the user wants to use one of the coarse or fine jog cmds.
                elif choiceString == 'a':
                    axes.move("G1 F500 X-1\n")
                elif choiceString == 'd':
                    axes.move("G1 F500 X1\n")
                elif choiceString == 'r':
                    axes.move("G1 F500 Y-1\n")
                elif choiceString == 'f':
                    axes.move("G1 F500 Y1\n")
                elif choiceString == 'w':
                    axes.move("G1 F500 Z1\n")
                elif choiceString == 's':
                    axes.move("G1 F500 Z-1\n")
                elif choiceString == 'x':
                    axes.move("G1 F100 Z-0.1\n")
                elif choiceString == 'z':
                    axes.move("G1 F60 Z-0.01\n")
                elif choiceString == 'c':
                    axes.move("G1 F100 Z0.1\n")
                elif choiceString == 'v':
                    axes.move("G1 F60 Z0.01\n")
                # If user accidently hits enter on nothing
                elif choiceString == '':
                    print("\t\tReceived empty string, no action performed.")
                # If user wants to use a convenient routine
                elif choiceString == '1':  # Clean Routine
                    print("\t\tRaising Tool by 20 mm...")
                    axes.move("G1 F2000 Z20\n")
                    # Prompt to Lower
                    choiceString = io_Prompt("\tLower 20 mm?(Y/N):",
                                             validate=True,
                                             validResponse=["Y", "N"]).lower()
                    if choiceString == 'y':
                        axes.move("G1 F2000 Z-15\n")
                        axes.move("G1 F500 Z-4\n")
                        axes.move("G1 F100 Z-1\n")
                elif choiceString == '2':  # Just Lift
                    print("\t\tRaising Tool by 20 mm...")
                    axes.move("G1 F2000 Z20\n")
                elif choiceString == '3':  # Bring Bed Forward
                    print("\t\tBringing Bed forward Y+50 mm...")
                    axes.move("G1 F2000 Y50\n")
                    # Prompt to return
                    choiceString = io_Prompt("\tReturn Y-50 mm? (Y/N):",
                                             validate=True,
                                             validResponse=["Y", "N"]).lower()
                    if choiceString == 'y':
                        axes.move("G1 F2000 Y-45\n")
                        axes.move("G1 F500 Y-4\n")
                        axes.move("G1 F100 Y-1\n")
                # If user wants to send input directly to axes
                else:  # Send to axes
                    print("\tReceived: " + choiceString)
                    axes.move(choiceString.upper() + "\n")
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")
                if tool.getState()[0]:
                    tool.disengage()
                print("\tTool Automatically Disengaged")
                return 'M1HardwareMenu'

    def ioMenu_printMenu(self):
        """Prints formatted menu options from menuItems dict."""
        # Print default menu name,description, params etc. from super()
        super().ioMenu_printMenu()

        # Get active sequence info
        if __activeSequence__ is None:
            seqName = "No Sequence Set"
        else:
            seqName = __activeSequence__.dictParams.get('name').value

        # Also print active recipe and sequence information
        print(Fore.LIGHTYELLOW_EX)
        print("\t%-35s|  %-25s" % ("Active Sequence:", seqName))
        print("\t%-35s|  %-25s" % ("Active Recipe:", __activeRecipe__.name))
        print(Style.RESET_ALL, end="")


class ioMenu_1PrintFile(ioMenuSpec):
    """Contains data and methods for implemented Print File Menu."""

    def __init__(self, **kwargs):
        """Initializes PrintFile Menu Object."""
        kwargs = {'name': 'PrintFileMenu',
                  'menuTitle': 'Print File Menu',
                  'menuItems': {
                      Fore.LIGHTRED_EX + "[q]": Fore.LIGHTRED_EX + "Quit",
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
        """Performs Menu operations - loops.

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
        """Initializes PrintFileOptions Menu Object."""
        kwargs = {'name': 'PrintFileOptionsMenu',
                  'menuTitle': 'Print File Options Menu',
                  'menuItems': {
                      Fore.LIGHTRED_EX + "[q]": Fore.LIGHTRED_EX + "Quit",
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
        """Performs Menu operations - loops.

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
        """Initializes Print Sequence Menu Object."""
        kwargs = {'name': 'PrintSequenceMenu',
                  'menuTitle': 'Print Sequence Menu',
                  'menuItems': {
                      Fore.LIGHTRED_EX + "[q]":
                          Fore.LIGHTRED_EX + "Quit",
                      Fore.LIGHTMAGENTA_EX + "[?]":
                          Fore.LIGHTMAGENTA_EX + "List Commands",
                      Fore.WHITE + "[H] Hardware":
                          Fore.WHITE + "Quick Switch to the Hardware Menu"}}
        super().__init__(**kwargs)

    def ioMenu_printMenu(self):
        """Prints formatted menu options from menuItems dict."""
        # Need to generate menu items and actions based on shapes loaded in
        # For now just 1 big list

        seqDictMenu = {}  # Contains name: filename pairs

        for seq in __seqDict__:
            fileName = __seqDict__.get(seq)
            seqDictMenu.update({seq: fileName})

        print(Style.RESET_ALL)
        print("-" * 150)
        print("###\t" + self.menuTitle)
        print("-" * 150)

        print(
            '\tSequences are pre-programmed, parameterized print routines '
            'stored as python files and loaded to RAM when the program '
            'launches.')
        print("\tChoose a sequence code to Edit/Execute:\n")

        print("\t(%-3s) %-35s| %-25s| %-55s" % (
            "Cmd", "Name", "Group", "Description"))
        for seqNum in __seqDict__:
            seqName = __seqDict__.get(seqNum).dictParams.get("name").value
            seqGrp = __seqDict__.get(seqNum).dictParams.get("owner").value
            seqDescription = __seqDict__.get(seqNum).dictParams.get(
                "description").value
            print("\t(%-3s) %-35s| %-25s| %-55s" % (
                seqNum, seqName, seqGrp, seqDescription))

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
        """Performs Menu operations - loops.

        Returns
        -------
            String
                title of next menu to call
        """
        global __savedInp__
        global __lastInp__

        # Push active axes and tool to all sequences
        for seq in __seqDict__.values():
            seq.axes = axes
            seq.tool = tool
            seq.updateParams()

        # Menu Loop
        doQuitMenu = False

        while not doQuitMenu:
            try:
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()
                # List of sequences as strings
                stringList = []
                for x in [*__seqDict__]:
                    stringList.append(str(x))

                choiceString = io_Prompt(
                    "Enter Command:", validate=True,
                    validResponse=(["q", "?", "h", "/", ".", ","]
                                   + stringList)).lower()

                if choiceString in ["/", ".", ","]:
                    choiceString = io_savedCmdOps(choiceString)
                else:
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)

                if choiceString == '?':
                    pass
                elif choiceString == 'q':
                    return 'M0MainMenu'
                elif choiceString.lower() == 'h':
                    return 'M1HardwareMenu'
                elif choiceString.upper() in stringList:
                    # Instantiate Sequence menu
                    seq = __seqDict__.get(choiceString.upper())
                    seqMen = ioMenu_2SequenceOptions(seq)
                    seqMen.io_Operate()
                else:
                    print("\tReceived: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")


class ioMenu_1PrintRecipe(ioMenuSpec):
    """Contains data and methods for implemented PrintRecipe Menu."""

    def __init__(self, **kwargs):
        """Initializes Print Recipe Menu Object."""
        kwargs = {'name': 'PrintRecipeMenu',
                  'menuTitle': 'Recipe Menu',
                  'menuItems': {
                      Fore.LIGHTRED_EX + "[q]":
                          Fore.LIGHTRED_EX + "Quit",
                      Fore.LIGHTMAGENTA_EX + "[?]":
                          Fore.LIGHTMAGENTA_EX + "List Commands",
                      Fore.WHITE + "(1) Browse/Load Stored Recipes":
                          Fore.WHITE + "Search through recipe folder for "
                                       "recipe to activate",
                      Fore.WHITE + "(2) Add to/Modify/Save Active Recipe":
                          Fore.WHITE + "Remove/Reorder sequences, change "
                                       "parameters, and save to yaml file",
                      Fore.WHITE + "(3) Create a New Recipe":
                          Fore.WHITE + "Start a new recipe from scratch",
                      # TODO Implement importing stored recipes and reusing
                      # Fore.WHITE + "(3) Reuse a stored recipe":
                      #    Fore.WHITE + "Import sequences from a stored
                      #    recipe to the active recipe",
                      Fore.LIGHTYELLOW_EX + "[PRIME]":
                          Fore.LIGHTYELLOW_EX + "Build active recipe into "
                                                "python code",
                      Fore.LIGHTYELLOW_EX + "[VIEW]":
                          Fore.LIGHTYELLOW_EX + "View active recipe details",
                      Fore.LIGHTGREEN_EX + "[GO]":
                          Fore.LIGHTGREEN_EX + "Begin recipe execution"
                  }}
        super().__init__(**kwargs)

    def ioMenu_printMenu(self):
        """Prints formatted menu options from menuItems dict."""

        print(Style.RESET_ALL)
        print("-" * 150)
        print("###\t" + self.menuTitle)
        print("-" * 150)
        print("\tRecipes are chains of sequences stored as yaml files and "
              "only loaded into RAM when active")
        print(Fore.YELLOW + "\tActive Recipe: " + str(
            __activeRecipe__.name) + "| "
              + str(__activeRecipe__.description) + "| " + str(
            __activeRecipe__.dateCreated))

        print(Fore.WHITE + "\tChoose an option from the list below:")
        print(Style.RESET_ALL, end="")
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
        """Performs Menu operations - loops.

        Returns
        -------
            String
                title of next menu to call
        """
        global __savedInp__
        global __lastInp__
        global __activeRecipe__  # pull global active recipe for modifying

        # Menu Loop
        doQuitMenu = False
        isPrimed = False
        while not doQuitMenu:
            try:
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()

                choiceString = io_Prompt(
                    "Enter Command:", validate=True,
                    validResponse=(["q", "?",
                                    "1", "2", "3",
                                    "/", ".", ",",
                                    "go", "view", "prime"]),
                    caseSensitive=False)

                if choiceString in ["/", ".", ","]:
                    choiceString = io_savedCmdOps(choiceString)
                else:
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)

                if choiceString == '?':
                    pass
                elif choiceString == 'q':
                    isPrimed = False
                    return 'M0MainMenu'
                elif choiceString == '1':
                    # Choose recipe from recipe stubs to activate
                    isPrimed = False
                    io_pollRecipes(silentMode=True)
                    print("\t Refreshing Recipe Stub List...")
                    # Print title line
                    print("\t| Code | %25s | %25s | %50s |" % (
                        str.center("Name", 25), str.center("Date Created", 25),
                        str.center("Description", 50)))
                    stubNum = 0
                    validOptions = ["q"]
                    for stub in __recipeStubList__:
                        stubNum = stubNum + 1
                        validOptions.append(str(stubNum))
                        print("\t| %-4s | %-25s | %-25s | %-50s |" % (
                            "(" + str(stubNum) + ")",
                            stub.name, stub.dateCreated, stub.description))

                    inpString = io_Prompt(
                        "Choose a recipe to activate, or q to cancel: ",
                        validate=True,
                        validResponse=validOptions, caseSensitive=False)

                    # Activate or quit
                    if inpString.lower() == 'q':
                        print("\tCanceling... no change made to active "
                              "sequence.")
                    else:
                        # Parse selection number
                        stubNum = int(inpString)

                        # Attempt to load new active recipe (with backup as
                        # an option)
                        backupActive = copy.copy(__activeRecipe__)
                        try:
                            io_loadRecipe(__recipeStubList__[stubNum - 1])
                        except Exception as inst:
                            logging.exception(inst)
                            __activeRecipe__ = backupActive
                            print(Fore.RED + "\tError activating sequence - "
                                             "reverting to previous active "
                                             "sequence.")
                elif choiceString == '2':  # Modify or save active recipe
                    isPrimed = False
                    # Check that there is an active recipe
                    if __activeRecipe__.name.lower() == \
                            'NoRecipeNameSet'.lower():
                        print(Fore.RED + "\tError: Cannot edit/save an active "
                                         "recipe that is empty or has this "
                                         "name." + Style.RESET_ALL)
                    else:
                        return "M2RecipeOptions"
                elif choiceString == '3':
                    # Create a new recipe and make active
                    isPrimed = False
                    nameinvalid = True
                    newName = None
                    while nameinvalid:
                        newName = io_Prompt("\tEnter new recipe name:")
                        # Check that name is unique
                        nameinvalid = False
                        for recStub in __recipeStubList__:
                            if newName.lower() == recStub.name.lower():
                                nameinvalid = True
                                print("\t\tError: Name already in use, "
                                      "try again.")
                    newDescription = io_Prompt(
                        "\tEnter new recipe description:")
                    newPath = None
                    # Backup active recipe
                    activeRecCopy = copy.copy(__activeRecipe__)
                    dateString = datetime.now().strftime(
                        "%I:%M%p on %B %d, %Y")
                    stubPassed = False
                    try:
                        newRecStub = recipeStub(name=newName,
                                                description=newDescription,
                                                dateCreated=dateString,
                                                fullFilePath=newPath)
                        __recipeStubList__.append(newRecStub)
                        stubPassed = True
                        __activeRecipe__ = recipe(name=newName,
                                                  description=newDescription,
                                                  dateCreated=dateString,
                                                  fullFilePath=newPath)
                        print("\tSuccessfully created new recipe!")
                    except Exception as inst:
                        print(
                            "\t\tError: Could not create new recipe, "
                            "reverting to previous condition.")
                        logging.exception(inst)
                        if stubPassed:
                            __recipeStubList__.pop()
                        __activeRecipe__ = activeRecCopy
                elif choiceString == '4':
                    # Import sequence from a stored recipe
                    isPrimed = False
                    # TODO Clone Modify recipe
                    pass
                elif choiceString.lower() == 'go':
                    if not isPrimed:
                        print(Fore.YELLOW + "\tError: must prime first"
                              + Style.RESET_ALL)
                    else:
                        logWriter = io_startLog()
                        __activeRecipe__.operateRecipe(axes, tool)
                        io_endLog(logWriter)
                elif choiceString.lower() == 'view':
                    for line in io_displayRecipe():
                        print("\t" + line)
                elif choiceString.lower() == 'prime':
                    __activeRecipe__.genRecipe()
                    isPrimed = True
                    pass
                else:
                    print("\tReceived: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")


class ioMenu_2SequenceOptions(ioMenuSpec):
    """Contains data and methods for print sequence options Menu."""

    def __init__(self, seq: sequenceSpec, **kwargs):
        """Initializes Print Sequence Options Menu Object.

        Parameters
        ----------
        seq: Sequence
            Refers to particular sequence object being modified by menu item
        """
        self.seq = seq
        self.paramsMenuDict = {}  # ParamID:  Param

        menuItems = {Fore.LIGHTRED_EX + "[q]": Fore.LIGHTRED_EX + "Quit",
                     Fore.LIGHTYELLOW_EX + "[PRIME]":
                         Fore.LIGHTYELLOW_EX + "Generate Print Commands",
                     Fore.LIGHTYELLOW_EX + "[VIEW]":
                         Fore.LIGHTYELLOW_EX + "View Print Commands",
                     Fore.YELLOW + "[Add]":
                         Fore.YELLOW + "Add/Insert sequence as configured "
                                       "into active recipe",
                     Fore.LIGHTGREEN_EX + "[ACTIVATE]":
                         Fore.LIGHTGREEN_EX + "Engage Print Sequence"}
        print(Style.RESET_ALL)

        kwargs = {'name': self.seq.dictParams.get("name").value,
                  'menuTitle': "Sequence: "
                               + self.seq.dictParams.get("name").value + ": "
                               + self.seq.dictParams.get("description").value,
                  'menuItems': menuItems}
        super().__init__(**kwargs)

    def ioMenu_printMenu(self):
        """Prints formatted menu options from menuItems dict."""
        print(Style.RESET_ALL)
        print("-" * 150)
        print("###\t" + self.menuTitle)
        print("-" * 150)

        print('\tFrom this menu you can directly modify the sequence '
              'parameters stored in RAM. Changes persist until the program '
              'is closed ')
        print("\tChoose a parameter number to modify, or one of the "
              "execution options:\n")

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
                "\t(%-3s) %-25s| %-45s| %-10s| %-50s"
                % (str(pNum), str(param.name)[:23], str(param.value)[:43],
                   str(param.unit)[:10],
                   str(param.helpString)))

        # Print param menu options
        print("\t(%-3s) %-25s| %-45s| %-10s| %-50s"
              % ("Cmd", "Parameter Name", "Parameter Value", "Units",
                 "Description"))
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
        """Performs Menu operations - loops.

        Returns
        -------
            String
                title of next menu to call
        """
        global __savedInp__
        global __lastInp__
        global __activeSequence__
        # Menu Loop
        doQuitMenu = False
        isPrimed = False

        while not doQuitMenu:
            try:
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()

                # List of param options as strings
                paramOptionList = []
                for x in [*self.paramsMenuDict]:
                    paramOptionList.append(str(x))

                choiceString = io_Prompt(
                    "Enter Command:",
                    validate=True,
                    validResponse=["q", "/", ".", ",",
                                   "PRIME", "VIEW", "ACTIVATE",
                                   "ADD"] + paramOptionList).lower()

                if choiceString in ["/", ".", ","]:
                    choiceString = io_savedCmdOps(choiceString)
                else:
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)

                if choiceString == 'q':
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
                elif choiceString.upper() == 'ACTIVATE':
                    __activeSequence__ = self.seq
                    print("\tSequence Activated, execute from the "
                          "hardware menu.")
                elif choiceString.upper() == "ADD":
                    # attempt to add to active recipe
                    if __activeRecipe__.name == 'NoRecipeNameSet':
                        print(Fore.RED + "\tError: No active recipe created"
                              + Style.RESET_ALL)
                    else:
                        print("\tCurrent state of Recipe: ")
                        for line in io_displayRecipe():
                            print("\t" + line)
                        newPos = io_Prompt(
                            "Enter index to be occupied by new sequence: ")
                        if newPos == 'q':
                            pass
                        else:
                            try:
                                __activeRecipe__.addSeq(int(newPos),
                                                        copy.deepcopy(
                                                            self.seq))
                            except Exception as inst:
                                logging.exception(inst)
                        print("\tNew state of Recipe: ")
                        for line in io_displayRecipe():
                            print("\t" + line)

                elif choiceString.upper() in paramOptionList:
                    isPrimed = False
                    # Modify corresponding parameter
                    paramNum = choiceString.upper()
                    param = self.paramsMenuDict.get(paramNum)
                    print("\tModifying parameter %s: %s"
                          % (paramNum, param.name))
                    newVal = io_Prompt(
                        "Enter new value (type File to choose a file):")
                    if newVal.lower() == "file":
                        print("\tChoose a file with the GUI window:")
                        tkWindow = tk.Tk()
                        newVal = \
                            askopenfilenames(parent=tkWindow, initialdir='/',
                                             initialfile='tmp',
                                             filetypes=[
                                                 ("GCode Files",
                                                  "*.gcode|*.txt"),
                                                 ("All files", "*")])[0]
                    oldVal = param.value
                    param.value = newVal
                    print("\tValue changed from %s to %s"
                          % (oldVal, param.value))
                else:
                    print("\tReceived: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu and "
                      "disengaging tool")
                tool.disengage()
                isPrimed = False


class ioMenu_2RecipeOptions(ioMenuSpec):
    """Contains data and methods for recipe edit options menu."""

    def __init__(self, **kwargs):
        """Initializes recipe edit options Menu Object.

        """

        menuItems = {Fore.LIGHTRED_EX + "[q]": Fore.LIGHTRED_EX + "Quit",
                     Fore.WHITE + "(0) Edit Recipe Parameters":
                         Fore.WHITE + "Edit Name, Description, Update Date",
                     Fore.WHITE + "(1) Add Sequence":
                         Fore.WHITE + "Inserts sequence at specified position",
                     Fore.WHITE + "(2) Edit Sequence":
                         Fore.WHITE + "Edit an existing sequence",
                     Fore.WHITE + "(3) Remove Sequence":
                         Fore.WHITE + "Removes one or more sequences",
                     Fore.WHITE + "(4) Reorder Sequences":
                         Fore.WHITE + "Change the order of sequence execution",
                     Fore.GREEN + "(SAVE) Save Recipe to File":
                         Fore.GREEN + "Writes to yaml file in recipe folder",
                     }  # TODO: IMPLEMENT SEQUENCE IMPORT from existing recipes
        print(Style.RESET_ALL)

        kwargs = {'name': "RecipeEditMenu",
                  'menuTitle': "Add to/Modify/Save Active Recipe: ",
                  'menuItems': menuItems}
        super().__init__(**kwargs)

    def ioMenu_printMenu(self):
        """Prints formatted menu options from menuItems dict."""
        print(Style.RESET_ALL)
        print("-" * 150)
        print("###\t" + self.menuTitle)
        print("-" * 150)

        print('\tFrom this menu you can modify the active recipe stored in '
              'RAM. Changes persist until the program is closed, unless '
              'saved to file ')
        print("\tChoose an edit/save operation:")
        print(Style.RESET_ALL, end="")
        # Print std menu options
        for key in sorted(self.menuItems):
            print("\t%-40s|  %-25s" % (key, self.menuItems.get(key)))
        print(Style.RESET_ALL)

    def io_Operate(self):
        """Performs Menu operations - loops.

        Returns
        -------
            String
                title of next menu to call
        """
        global __savedInp__
        global __lastInp__
        # Menu Loop
        doQuitMenu = False
        isPrimed = False

        while not doQuitMenu:
            try:
                self.ioMenu_printMenu()

                for line in io_displayRecipe():
                    print("\t" + line)

                choiceString = io_Prompt("Enter Command:", validate=True,
                                         validResponse=["q", "SAVE", "0", "1",
                                                        "2", "3", "4"])

                if choiceString == 'q':
                    return "M1PrintRecipe"
                elif choiceString.upper() == 'SAVE':
                    # First pull stub and active recipe
                    activeStub = None
                    for stub in __recipeStubList__:
                        if stub.name == __activeRecipe__.name:
                            activeStub = stub
                    try:
                        io_saveRecipe(activeStub)
                    except Exception as inst:
                        logging.exception(inst)
                elif choiceString == '0':  # Edit Recipe Parameters
                    inp = io_Prompt("Which parameter to edit? (P0-P2): ",
                                    validate=True,
                                    validResponse=["P0", "P1", "P2"])
                    if inp.lower() == 'p0':
                        isValid = False
                        newName = ''
                        # Pull active stub
                        activeStub = recipeStub()
                        for stub in __recipeStubList__:
                            if stub.name == __activeRecipe__.name:
                                activeStub = stub

                        while not isValid:
                            isValid = True
                            newName = io_Prompt(
                                "Enter new recipe name, q to cancel: ")
                            # Validate against existing names
                            for recStub in __recipeStubList__:
                                if recStub.name.lower() == newName.lower():
                                    isValid = False
                                    print(Fore.RED
                                          + "\tError, Name already in use"
                                          + Style.RESET_ALL)
                        if newName.lower() == 'q':
                            print("\tCancelling rename....")
                        else:
                            __activeRecipe__.name = newName
                            activeStub.name = newName

                    elif inp.lower() == 'p1':
                        __activeRecipe__.description = io_Prompt(
                            "Enter new description: ")
                    elif inp.lower() == 'p2':
                        isValid = False
                        newDate = ''
                        while not isValid:
                            isValid = True
                            newDate = io_Prompt("Enter new creation date in "
                                                "form hh:mmPM on Month dd, "
                                                "yyyy or enter \"NOW\" for "
                                                "current timestamp: ")
                            # Check for Now
                            if newDate.lower() == 'now':
                                newDate = datetime.now().strftime(
                                    "%I:%M%p on %B %d, %Y")
                                isValid = True
                                pass
                            # Check if length matches (excluding month)
                            elif (len(newDate[:11]) + len(newDate[-9:])) == 20:
                                isValid = True

                        __activeRecipe__.dateCreated = newDate
                    else:
                        print(Fore.RED + "\tError on input" + Style.RESET_ALL)
                elif choiceString == '1':  # Add Sequence
                    print("\tSending to Sequence Menu...")
                    return "M1PrintSequence"
                elif choiceString == '2':  # Edit Sequence
                    if __activeRecipe__.seqList == []:
                        print("Cannot edit an empty sequence list")
                    else:
                        indexList = []
                        index = -1
                        for seq in __activeRecipe__.seqList:
                            index = index + 1
                            indexList.append("S" + str(index))

                        indexNo = io_Prompt(
                            "Enter Index (S#) for Sequence to modify:",
                            validate=True,
                            validResponse=indexList)
                        seqIndex = int(indexNo[1:])
                        seqMen = ioMenu_2SequenceOptions(
                            __activeRecipe__.seqList[seqIndex])
                        seqMen.io_Operate()
                elif choiceString == '3':  # Remove Sequence
                    # Create list of sequence possibilities
                    numSeq = len(__activeRecipe__.seqList)
                    i = 0
                    validSeqIndex = ["q"]
                    while i < numSeq:
                        validSeqIndex.append("S" + str(i))
                        i = i + 1
                    seqRem = io_Prompt("Enter index of sequence to remove ("
                                       "S#), q to cancel: ",
                                       validate=True,
                                       validResponse=validSeqIndex)
                    if seqRem == 'q':
                        pass
                    else:
                        try:
                            seqRem = seqRem[1:]
                            __activeRecipe__.deleteSeq(int(seqRem))
                        except Exception as inst:
                            logging.exception(inst)
                elif choiceString == '4':  # Reorder Sequences
                    # Create list of sequence possibilities
                    numSeq = len(__activeRecipe__.seqList)
                    i = 0
                    validSeqIndex = ["q"]
                    while i < numSeq:
                        validSeqIndex.append("S" + str(i))
                        i = i + 1

                    doneReord = False
                    while not doneReord:
                        indexOld = io_Prompt("Enter index of sequence to "
                                             "move (S#), q to finish: ",
                                             validate=True,
                                             validResponse=validSeqIndex)
                        if indexOld == 'q':
                            doneReord = True
                        else:
                            try:
                                indexNew = \
                                    io_Prompt("Enter index you would like "
                                              "the sequence to occupy (S#), "
                                              "q to cancel: ",
                                              validate=True,
                                              validResponse=validSeqIndex)
                                if indexNew == 'q':
                                    pass
                                else:
                                    __activeRecipe__.reorderSeq(indexOld[1:],
                                                                indexNew[1:])
                                    print("\tNew state:")
                                    for line in io_displayRecipe():
                                        print("\t" + line)
                            except Exception as inst:
                                logging.exception(inst)
                else:
                    print("\tReceived: " + choiceString)
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")
                isPrimed = False


# CLI Initiation Methods #####################################################

def io_setupConsole():
    """Resizes console window."""
    osVers = sys.platform
    print("\tDetected OS: %s" % osVers)

    try:  # resizing window
        if sys.platform.startswith('win'):
            os.system("mode con cols=150 lines=2000")
        elif sys.platform.startswith('linux'):
            os.system("printf '\\e[8;40;150t'")
    except Exception as inst:
        print("\tFailed to resize terminal")
        logging.exception(inst)


def io_StartText():
    """Displays start screen."""
    print("=" * 150)
    print("\tPolyChemPrint3 - Version:" + str(__version__)
          + "\tRevised: " + __date__)
    print("=" * 150)


def io_preloadText():
    """Displays start screen."""
    print("#" * 150)
    print("\tStarting PolyChemPrint3 Load Sequence...")
    print("#" * 150)
    print("Step:" + " " * 55 + "| Syntax Checked | Loaded |")


# IO Helper METHODS ##########################################################

def io_TestCode():
    """Executes a block of test code from main menu."""
    print("\tBegin Test Code")
    print("\tEnd Test Code")


def io_Prompt(promptString: str, validate=False, validResponse=None,
              caseSensitive=False):
    """Prompts user for input and may validate against a list of options.

    Parameters
    ----------
    promptString: str
        text to display as a prompt to the user.
    validate: bool
        whether or not to validate input againt validResponse
    validResponse: list of str
        list of valid input strings, ignored if validate == false
    caseSensitive: bool
        whether validation should be made on a case sensitive basis

    Returns
    -------
    str
        inputString from user
    """
    if validResponse is None:
        validResponse = ['']
    global __lastInp__
    inString = input("\t" + promptString + '> ').rstrip()

    if validate:

        if not caseSensitive:
            # Convert all valid responses to lowercase
            validResponse = [item.lower() for item in validResponse]
            validString = inString.lower() in validResponse
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
    """Handles processing saved/ repeat commands for the CLI.

    Returns
    -------
    str
        the saved string to feed back into the menu loop
    """
    global __lastInp__
    global __savedInp__
    outString = ''

    if inString == '/':
        if __lastInp__ in ["/", ",", "."]:
            print("\tNo Valid Command to Repeat")
            __lastInp__ = ""
        else:
            outString = __lastInp__

    elif inString == '.':
        if __savedInp__ in ["/", "."]:
            print("\tNo Valid Command to Repeat")
            __savedInp__ = ""
        else:
            outString = __savedInp__
    elif inString == ',':
        __savedInp__ = io_Prompt("Enter Command to Save:")

    else:
        print("Error")

    return outString


def io_MenuManager(initialMenuString):
    """Presents appropriate Menu in CLI depending on menuString - loops.

    Parameters
    ----------
    initialMenuString: str
        telling which menu to begin on.

    Returns ------- menuFlag: str Str that falls through the switch case (
    doesn't match any menu or is quit)
    """
    # Instantiate Menu Objects, variable names match menu flags
    M0MainMenu = ioMenu_0Main()
    M1ConfigurationMenu = ioMenu_1Configuration()
    M1HardwareMenu = ioMenu_1Hardware()
    M1PrintFile = ioMenu_1PrintFile()
    M2PrintFileOptions = ioMenu_2PrintFileOptions()
    M1PrintSequence = ioMenu_1PrintSequence()
    M1PrintRecipe = ioMenu_1PrintRecipe()
    M2RecipeOptions = ioMenu_2RecipeOptions()

    # Loop to iterate through menu
    menuFlag = initialMenuString
    while not menuFlag == 'quit':
        # Switch based on menuflags
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
        elif menuFlag == 'M2PrintFileOptions':
            (M2PrintFileOptions.
             ioMenu_updateStoredCmds(__lastInp__, __savedInp__))
            menuFlag = M2PrintFileOptions.io_Operate()
        elif menuFlag == 'M1PrintSequence':
            M1PrintSequence.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M1PrintSequence.io_Operate()
        elif menuFlag == 'M1PrintRecipe':
            M1PrintSequence.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M1PrintRecipe.io_Operate()
        elif menuFlag == 'M2RecipeOptions':
            M1PrintSequence.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M2RecipeOptions.io_Operate()
        else:
            print(Fore.LIGHTRED_EX + "\tInternal CLI Error:"
                  + "Invalid flag returned from menu, resetting to main menu."
                  + Style.RESET_ALL)
            menuFlag = 'M0MainMenu'
    return menuFlag


# PCP Object Handling File IO METHODS ########################################
def io_loadPCP(objType):
    """Search for, instantiate, and load PCP objects into appropriate dict.

    Parameters
    ----------
    objType : Object
        Type of PCP object to load from python file
    """
    # Set type-specific values
    if objType == 'sequence':
        textCol = Fore.WHITE
        objDict = __seqDict__
        objCode = 'S'
        moduleDirString = "polychemprint3.sequence"
        objDir = __rootDir__ / 'sequence'
        print(textCol
              + "Loading sequences from Sequence Folder..." + "-" * 46)
    elif objType == 'tools':
        textCol = Fore.LIGHTCYAN_EX
        objDict = __toolDict__
        objCode = 'T'
        moduleDirString = "polychemprint3.tools"
        objDir = __rootDir__ / 'tools'
        print(textCol
              + "Loading tools from tools Folder..." + "-" * 53)
    elif objType == 'axes':
        textCol = Fore.LIGHTYELLOW_EX
        objCode = 'A'
        objDict = __axesDict__
        moduleDirString = "polychemprint3.axes"
        objDir = __rootDir__ / 'axes'
        print(textCol
              + "Loading axes from axes Folder " + "-" * 57)
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

    # Search folder for possible object files
    for name in filesInFolder:
        if (".py" in name[-3:]) and ("Spec" not in name) and (
                "init" not in name):
            pcpObjFiles.append(name)

    objNum = 1
    containsNull = 0
    for objFile in pcpObjFiles:

        # See if file will compile
        try:
            compile(open(objDir / objFile, 'r').read(), objFile, "exec")
            passCompile = 1
        except Exception as inst:
            passCompile = 0
            print(Fore.LIGHTRED_EX + '\t\t' + objFile
                  + "\tfailed syntax check" + textCol)
            logging.exception(inst)

        # See if file will load, if so assign it a number and add to the
        # objectDict
        if passCompile:
            try:
                # Load
                objName = str(objFile)[:-3]
                obj = getattr(
                    importlib.import_module(moduleDirString + "." + objName),
                    objName)
                # Depends on object type
                vars()[objName] = obj(__verbose__=__verbose__, name=objName)
                # If object name contains 'null' and null spot not already
                # taken, assign it object nubmer 0 so it stays at the top of
                # the list
                if objName.__contains__('null') and containsNull == 0:
                    thisNum = 0
                else:
                    thisNum = objNum
                    objNum += 1
                objDict.update({"%s%s" % (objCode, thisNum): vars()[objName]})
                passLoad = 1
            except Exception as inst:
                passLoad = 0
                logging.exception(inst)
        else:
            passLoad = 0

        # Print Status Line for this object
        print(textCol + "\t%-56s|" % objFile, end="")
        if passCompile == 1:
            print(Fore.LIGHTGREEN_EX + '      PASS      ' + textCol + "|",
                  end="")
        else:
            print(Fore.RED + '      FAIL      ' + textCol + "|", end="")
        if passLoad == 1:
            print(Fore.LIGHTGREEN_EX + '  PASS  ' + textCol + "|")
        else:
            print(Fore.RED + '  FAIL  ' + textCol + "|")

    if objType == 'sequence':
        print(textCol + "Finished Loading Sequence Files! " + "-" * 54
              + Style.RESET_ALL)
    elif objType == 'tools':
        print(textCol + "Finished Loading Tool Files! " + "-" * 58
              + Style.RESET_ALL)
    elif objType == 'axes':
        print(textCol + "Finished Loading Axes Files! " + "-" * 58
              + Style.RESET_ALL)


def io_reOrderSeq():
    """Reassigns sequence numbers in seqDict based on (1st) owner and (2nd)
    alphabetical order.
    """
    global __seqDict__
    # First, generate a list of owners
    ownersList = []
    for seqName in __seqDict__:
        seq = __seqDict__.get(seqName)
        thisOwner = seq.dictParams.get("owner").value
        if not ownersList.__contains__(thisOwner):
            ownersList.append(thisOwner)

    newSeqDict = {}
    seqNum = 1
    # Now, go through the old seqDict in order of owners,
    # then alphabetically, assign numbers and add to the new dict
    for owner in ownersList:
        for seqCode in sorted(__seqDict__):
            seq = __seqDict__.get(seqCode)
            thisOwner = seq.dictParams.get("owner").value
            newSeqCode = "S" + str(seqNum)
            if owner == thisOwner:
                newSeqDict[newSeqCode] = seq
                seqNum += 1
    # Overwrite the old dict with the new dict
    __seqDict__ = newSeqDict


def io_pollRecipes(silentMode=False):
    """Finds all recipe yaml files and loads recipe stubs into the
    recipeList.

    Parameters
    ----------
    silentMode: bool
        Whether or not to print log messages to terminal window.
    """
    global __recipeStubList__
    __recipeStubList__ = []

    textCol = Fore.GREEN
    recipeDir = __rootDir__ / 'recipes'
    if not silentMode:
        print(
            textCol + "Loading Recipe stub list from Recipes Folder..."
            + "-" * 40)
    # Read through all files in folder and load all yaml to a list
    filesInFolder = os.listdir(recipeDir)
    recipeNames = []

    # Search folder for possible recipe files
    for name in filesInFolder:
        if ".yaml" in name[-5:]:
            recipeNames.append(name)

    # For each of these, try to create a recipe stub by parsing first 3
    # lines and add to stublist
    if not silentMode:
        print("\tAttempting to load recipestubs...")
    for name in recipeNames:
        try:
            fullpath = recipeDir / name
            fileReader = fileHandler(fullpath)
            recipeekList = fileReader.peekFile(3)[1]

            newStub = recipeStub(name=recipeekList[0][8:].rstrip(),
                                 description=recipeekList[1][15:].rstrip(),
                                 dateCreated=recipeekList[2][16:].rstrip(),
                                 fullFilePath=fullpath)

            __recipeStubList__.append(newStub)
            if not silentMode:
                print("\tLoaded: " + newStub.name + ".yaml")
        except Exception as inst:
            logging.exception(inst)
    if not silentMode:
        print(textCol
              + "Finished Loading Recipe stub list from Recipes Folder!"
              + "-" * 33)
        print(Style.RESET_ALL, end="")


def io_loadRecipe(rStub: recipeStub):
    """Attempts to load selected recipeStub into the active Recipe, pulling
    extra info from yaml file.

    Parameters
    ----------
    rStub: recipeStub
        Summary object of the full recipe.
    """
    print(Style.RESET_ALL, end="")
    global __activeRecipe__

    # Backup current recipe
    backupActive = copy.copy(__activeRecipe__)
    try:
        print("\tAttempting to load full recipe from yaml file in recipe "
              "folder...")
        # Get path from stub
        fullpath = rStub.fullFilePath
        newRecipe = recipe(fullFilePath=fullpath)
        # Read in entire file and reject comment lines
        fullText = newRecipe.readFullFile()[1]
        # Remove comment lines
        del fullText[0:3]
        fullYaml = '\n'.join(fullText)
        newRecipe.loadLogSelf(fullYaml)
        # Overwrite stored file path with actual path
        newRecipe.fullFilePath = fullpath
        __activeRecipe__ = newRecipe
        print(Fore.GREEN + "\tNew recipe activated!" + Style.RESET_ALL)
    except Exception as inst:
        logging.exception(inst)
        __activeRecipe__ = backupActive
        print(
            Fore.RED + "\tError activating sequence - reverting to previous "
                       "active sequence." + Style.RESET_ALL)


def io_saveRecipe(activeStub: recipeStub):
    """Attempts to save active recipe to a yaml file.

    Parameters
    ----------
    activeStub: recipeStub
        The stub object for the currently active recipe.
    """
    global __activeRecipe__

    try:
        filePath = __rootDir__ / 'recipes' / (
                str(__activeRecipe__.name) + ".yaml")

        # Check if file already exists and whether user wants to overwrite
        fileExists = os.path.exists(filePath)
        doSave = True
        if fileExists:
            doSaveInp = io_Prompt(
                Fore.YELLOW + "\tA recipe with this filename already exists, "
                              "do you want to overwrite "
                              "it? (Y/N) If not, try renaming this recipe "
                              "first: ",
                validate=True,
                validResponse=["Y", "N"])
            if doSaveInp.lower() == 'n':
                doSave = False

        if doSave:

            __activeRecipe__.fullFilePath = filePath

            # Temporarily overwrite the cmd list
            cmdHolder = __activeRecipe__.cmdList
            __activeRecipe__.cmdList = []

            # Construct string to write
            outstring = "# Name: " + __activeRecipe__.name \
                        + "\n# Description: " \
                        + __activeRecipe__.description \
                        + "\n# Date Created: " \
                        + __activeRecipe__.dateCreated \
                        + "\n" + __activeRecipe__.writeLogSelf()
            __activeRecipe__.overWriteToFile(outstring)

            # Restore fullFilepath and cmd list
            __activeRecipe__.cmdList = cmdHolder

            print("\tSuccessfully saved recipe to file at: \n\t" + str(
                __activeRecipe__.fullFilePath))
        else:
            print("\t\tCancelling save operation...")
    except Exception as inst:
        logging.exception(inst)


def io_displayRecipe():
    """Prints recipe parameters and contents to screen. """
    global __activeRecipe__
    # Append parameter strings
    outStrings = [
        Fore.YELLOW + "(P0) Active Recipe Name: " + __activeRecipe__.name,
        Fore.YELLOW + "(P1) Description: " + __activeRecipe__.description,
        Fore.YELLOW + "(P2) Creation Date: " + __activeRecipe__.dateCreated,
        Fore.WHITE + "Full Path: " + str(__activeRecipe__.fullFilePath),
        Fore.WHITE + "Begin Sequence List " + "-" * 100,
        Fore.WHITE + "\t|  %5s  | %20s | %25s | %50s |" % (
            str.center("Index", 5),
            str.center("Sequence Name", 20),
            str.center("Sequence Type", 25),
            str.center("Description", 50))]

    # Present sequences
    if __activeRecipe__.seqList is None:
        outStrings.append(Fore.WHITE + "\tNo Sequences to display")
    else:
        index = - 1
        for seq in __activeRecipe__.seqList:
            index = index + 1
            outStrings.append(Fore.WHITE
                              + "\t| (%5s) | %20s | %25s | %50s|"
                              % (str.center("S" + str(index), 5),
                                 str.center(seq.dictParams.get("name").value,
                                            20),
                                 str.center(seq.dictParams.get("owner").value,
                                            25),
                                 str.center(
                                     seq.dictParams.get("description").value,
                                     50)))
    outStrings.append(Fore.WHITE + "End Sequence List " + "-" * 100)
    return outStrings


def io_startLog():
    """Creates a log file for the current recipe and writes pre-run
    parameters to it.

    """
    # TODO REVISIT LOGGING
    global __activeRecipe__
    # Append parameter strings
    try:
        print("\tAttempting to write log to file...")
        rootDir = Path(__file__).absolute().parent
        logDir = rootDir / 'Logs'
        now = datetime.now()
        strDate = str(now.year) + str(now.month) + str(now.day) + "_" \
                  + str(now.hour) + str(now.minute) \
                  + str(now.second)
        strName = str(input("\tEnter Log File Name:"))
        fileName = strDate + "_" + strName
        fileWriter = fileHandler(fullFilePath=str(logDir / fileName) + ".txt")
        outString = "-" * 50 + "\n" + "Log File Name: " + strName \
                    + "\nStarted at: " + strDate + "\n" + "-" * 50 \
                    + "\n" + __activeRecipe__.writeLogSelf()
        fileWriter.overWriteToFile(outString)
        return fileWriter
    except Exception as inst:
        print(Fore.RED + "\tError Writing Log File" + Style.RESET_ALL)
        logging.exception(inst)


def io_endLog(fileWriter: fileHandler):
    """Creates a log file for the current recipe and writes final
    parameters to it.

    Parameters
    ----------

    """
    # TODO: REVISIT LOGGING
    # Append End status
    try:
        now = datetime.now()
        strDate = str(now.year) + str(now.month) + str(now.day) + "_" + str(
            now.hour) + str(now.minute) + str(now.second)
        print("Recipe completed successfully at: " + strDate)
        finalText = io_Prompt(
            " Enter any text you'd like to add to the log (q for nothing): ")
        if finalText.lower() == 'q':
            finalText = ''

        fileWriter.appendToFile("-" * 50 + "Finished at: " + strDate + "\n")
        fileWriter.appendToFile("Final Comment: " + finalText)
        print("\tWriting log end to file...")
    except Exception as inst:
        print(Fore.RED + "\tError Writing Log File" + Style.RESET_ALL)
        logging.exception(inst)


# Global attributes ##########################################################

# Program Details
__version__ = 3.0
__date__ = "2020/10/23"
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
__seqDict__ = {}  # Empty dictionary to hold sequences
__toolDict__ = {}  # Empty dictionary to hold tools
__axesDict__ = {}  # Empty dictionary to hold axes
__recipeStubList__ = []  # Empty list to hold recipe stubs
__activeRecipe__ = recipe()  # Initialize a new (default) recipe object
__activeSequence__ = None  # No default sequence exists, so initialize as None

# Paths to text files that may need to be loaded.
__textDict__ = {'License': __rootDir__ / 'data' / 'TextPanels' / 'LICENSE.txt'}


# Main METHOD ################################################################
def main():
    """Runs program."""
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
    # Reorders sequences in the seqDict based on their type (owner)
    io_reOrderSeq()
    io_pollRecipes()
    # Interface Start Sequencea
    io_StartText()
    # make software connections

    doQuitProgram = False
    # prevent ctrl+c from closing program
    while not doQuitProgram:
        try:
            # menuManagerSequence - loop that handles menu driving
            menuFlag = io_MenuManager("M0MainMenu")
            # if we get here, menumanager should have received quit message
            # Double check with user if they want to exit
            if menuFlag == 'quit':
                inp = io_Prompt(
                    promptString=("Really quit (Y,q)?"
                                  " or return to main menu? (N): "),
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

            inp = io_Prompt(promptString="Restart the program? (Y/N): ",
                            validate=True, validResponse=["Y", "N"],
                            caseSensitive=False)
            if inp.lower() == 'y':
                main()
            else:
                print('\tExiting Program - Goodbye!')
                doQuitProgram = True

    # Exit program
    sys.exit()


# This code included so that the main method is only run when the python
# interpreter is executing this python file, i.e., so it doesn't run the
# main method on import.
if __name__ == "__main__":
    main()
