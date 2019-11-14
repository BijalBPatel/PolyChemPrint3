# -*- coding: utf-8 -*-
"""Runs the command line interface and 'executes' the program.

| First created on Sat Oct 19 21:56:15 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""
#############################################################################
### Import Statements
#############################################################################
import sys
sys.path.append("../")
from polychemprint3.userInterface.commandLineInterface.ioMenuSpec \
    import ioMenuSpec
from polychemprint3.axes.Axes3D import axes3D
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.tools.ultimusExtruder import ultimusExtruder

import logging
import os
from pathlib import Path
from colorama import init, Fore, Back, Style


#############################################################################
### Menu Classes
#############################################################################
class ioMenu_0Main(ioMenuSpec):
    """Contains data and methods for implemented Main Menu."""

    ### Construct/Destruct METHODS
    def __init__(self, **kwargs):
        """*Initializes Main Menu Object*.

        | *Parameters*
        |   none

        | *Returns*
        |   none
        ""

        ''' Param to pass into parent class
        |   name, name of the menu
        |   menuTitle, name of the menu
        |   menuItems, dictionary of menu options and text
        """
        kwargs = {'name': 'Main',
                  'menuTitle': 'Main Menu', 'menuItems':
                      {Fore.LIGHTRED_EX + "[q]": Fore.LIGHTRED_EX + "Quit",
                       Fore.LIGHTMAGENTA_EX + "[?]":
                           Fore.LIGHTMAGENTA_EX + "List Commands",
                       Fore.WHITE + "(2) printFile":
                           Fore.WHITE + "Print from a GCODE file",
                       Fore.WHITE + "(1) hardware":
                           Fore.WHITE + "Manually control hardware",
                       Fore.WHITE + "(0) settings":
                           Fore.WHITE + "Program options",
                       Fore.WHITE + "(4) test":
                           Fore.WHITE + "Run Test Code",
                       Fore.WHITE + "(3) printSequences":
                           Fore.WHITE + "Print pre-defined sequences"}}
        super().__init__(**kwargs)

    ### ioMenuSpec METHODS
    def ioMenu_Operate(self):
        """*Performs Menu operations - loops*.

        | *Parameters*
        |   none

        | *Returns*
        |   menuFlag, String with title of next menu to call
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
                                             validResponse=["q", "?", "0", "1",
                                                            "2", "3", "4", "/",
                                                            ".", ","]).lower()

                if not (choiceString in ["/", ".", ","]):
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)

                if choiceString in ["/", ".", ","]:
                    (choiceString, promptIn) = io_savedCmdOps(choiceString)
                elif choiceString == '?':
                    pass
                elif choiceString == 'q':
                    return 'quit'
                elif choiceString == '0':
                    return 'M1SettingsMenu'
                elif choiceString == '1':
                    return 'M1HardwareMenu'
                elif choiceString == '2':
                    return 'M1PrintFile'
                elif choiceString == '3':
                    return 'M1PrintSequence'
                elif choiceString == '4':
                    io_TestCode()
                    promptIn = True
                else:
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
                    promptIn = True
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")


class ioMenu_1Settings(ioMenuSpec):
    """Contains data and methods for implemented Settings Menu."""

    ### Construct/Destruct METHODS
    def __init__(self, **kwargs):
        """*Initializes Settings Menu Object*.

        | *Parameters*
        |   none

        | *Returns*
        |   none
        ""

        ''' Param to pass into parent class
        |   name, name of the menu
        |   menuTitle, name of the menu
        |   menuItems, dictionary of menu options and text
        """
        kwargs = {'name': 'SettingsMenu',
                  'menuTitle': 'Settings Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                Fore.WHITE + "(0) info":
                                    Fore.WHITE + "Program Info",
                                Fore.WHITE + "(1) out":
                                    Fore.WHITE
                                    + "Toggles level of output details"}}
        super().__init__(**kwargs)

    ### ioMenuSpec METHODS
    def ioMenu_Operate(self):
        """*Performs Menu operations - loops*.

        | *Parameters*
        |   none

        | *Returns*
        |   flag, String with title of next menu to call
        """
        global __savedInp__
        global __lastInp__
        global __verbose__
        # Menu Loop
        doQuitMenu = False
        promptIn = True

        while not doQuitMenu:
            try:
                self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
                self.ioMenu_printMenu()
                if promptIn:
                    choiceString = io_Prompt("Enter Command:", validate=True,
                                             validResponse=["q", "?", "0",
                                                            "1", "/",
                                                            ".", ","]).lower()

                if not (choiceString in ["/", ".", ","]):
                    self.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)

                if choiceString in ["/", ".", ","]:
                    (choiceString, promptIn) = io_savedCmdOps(choiceString)
                elif choiceString == '?':
                    pass
                elif choiceString == 'q':
                    return 'M0MainMenu'
                elif choiceString == '0':
                    return 'M1SettingsMenu'
                elif choiceString == '0':
                    print("PolyChemPrintv" + __version__ + " " + __date__
                          + " By Bijal Patel bbpatel2@illinois.edu")
                elif choiceString == '1':
                    __verbose__ = 1 - __verbose__
                    if __verbose__:
                        print("\tMore Details will be displayed.")
                    else:
                        print("\tFewer Details will be displayed.")
                else:
                    print(Fore.LIGHTRED_EX
                          + "\tInvalid Choice, resetting menu"
                          + Style.RESET_ALL)
                    promptIn = True
            except KeyboardInterrupt:
                print("\n\tKeyboardInterrupt received, resetting menu")


class ioMenu_1Hardware(ioMenuSpec):
    """Contains data and methods for implemented Hardware Menu."""

    ### Construct/Destruct METHODS

    def __init__(self, **kwargs):
        """*Initializes Hardware Menu Object*.

        | *Parameters*
        |   none

        | *Returns*
        |   none
        ""

        ''' Param to pass into parent class
        |   name, name of the menu
        |   menuTitle, name of the menu
        |   menuItems, dictionary of menu options and text
        """
        kwargs = {'name': 'HardwareMenu',
                  'menuTitle': 'Hardware Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                Fore.LIGHTRED_EX + "STOP":
                                    Fore.LIGHTRED_EX + "Emergency STOP",
                                Fore.WHITE + "a,d;r,f;w,s;x,z":
                                    Fore.WHITE + "Jog (X; Y; Z; Zsmall)",
                                Fore.WHITE + "(0) clean":
                                    Fore.WHITE + "Lift up 20 mm, lower on cmd",
                                Fore.WHITE + "(1) lift":
                                    Fore.WHITE + "Lift up 20 mm",
                                Fore.WHITE + "(2) ext":
                                    Fore.WHITE + "Send cmd to extruder",
                                Fore.WHITE + "(3) sequences":
                                    Fore.WHITE + "Go to sequences menu",
                                Fore.WHITE + "(4) printFile":
                                    Fore.WHITE + "Go to printFile menu"}}
        super().__init__(**kwargs)

    ### ioMenuSpec METHODS
    def ioMenu_Operate(self):
        """*Performs Menu operations - loops*.

        | *Parameters*
        |   none

        | *Returns*
        |   flag, String with title of next menu to call
        """
        io_Prompt("This is filler, enter any key to go back to main menu")
        return 'M0MainMenu'


class ioMenu_1PrintFile(ioMenuSpec):
    """Contains data and methods for implemented Print File Menu."""

    ### Construct/Destruct METHODS

    def __init__(self, **kwargs):
        """*Initializes PrintFile Menu Object*.

        | *Parameters*
        |   none

        | *Returns*
        |   none
        ""

        ''' Param to pass into parent class
        |   name, name of the menu
        |   menuTitle, name of the menu
        |   menuItems, dictionary of menu options and text
        """
        kwargs = {'name': 'PrintFileMenu',
                  'menuTitle': 'Print File Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                "STOP": "Emergency STOP",
                                "a,d;r,f;w,s;x,z": "Jog (X; Y; Z; Zsmall)",
                                "(0) setZero": "Perform Origin set sequence",
                                "(1) pickFile": "Pick a GCODE file",
                                "(2) printFile": "Execute print sequence",
                                "(3) fileText": "Display GCODE file"}}

        super().__init__(**kwargs)

    ### ioMenuSpec METHODS
    def ioMenu_Operate(self):
        """*Performs Menu operations - loops*.

        | *Parameters*
        |   none

        | *Returns*
        |   flag, String with title of next menu to call
        """
        io_Prompt("This is filler, enter any key to go back to main menu")
        return 'M0MainMenu'


class ioMenu_2AxesOrigin(ioMenuSpec):
    """Contains data and methods for implemented AxesOrigin Menu."""

    ### Construct/Destruct METHODS

    def __init__(self, **kwargs):
        """*Initializes PrintFile Menu Object*.

        | *Parameters*
        |   none

        | *Returns*
        |   none
        ""

        ''' Param to pass into parent class
        |   name, name of the menu
        |   menuTitle, name of the menu
        |   menuItems, dictionary of menu options and text
        """
        kwargs = {'name': 'AxesOriginSet',
                  'menuTitle': 'Axes Origin Set Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                "STOP": "Emergency STOP",
                                "a,d;r,f;w,s;x,z": "Jog (X; Y; Z; Zsmall)",
                                "done": "Tip is at 0,0,0"}}
        super().__init__(**kwargs)

    ### ioMenuSpec METHODS
    def ioMenu_Operate(self):
        """*Performs Menu operations - loops*.

        | *Parameters*
        |   none

        | *Returns*
        |   flag, String with title of next menu to call
        """
        io_Prompt("This is filler, enter any key to go back to main menu")
        return 'M0MainMenu'


class ioMenu_2PrintFileOptions(ioMenuSpec):
    """Contains data and methods for implemented PrintFileOptions Menu."""

    ### Construct/Destruct METHODS

    def __init__(self, **kwargs):
        """*Initializes PrintFileOptions Menu Object*.

        | *Parameters*
        |   none

        | *Returns*
        |   none
        ""

        ''' Param to pass into parent class
        |   name, name of the menu
        |   menuTitle, name of the menu
        |   menuItems, dictionary of menu options and text
        """
        kwargs = {'name': 'PrintFileOptionsMenu',
                  'menuTitle': 'Print File Options Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                "L": "Advanced Log Options",
                                "(9) execute": "Start print sequence",
                                "(6) genCmds": "Generate command arrays",
                                "(8) dispCode": "Display printing code",
                                "(7) dispCmds": "Display current commands",
                                "(0) clean": "raise/lower 20mm",
                                "(1) hardware": "Go to hardware menu",
                                "(2) plot":
                                    "Select Plotter Mode (No Extruder))",
                                "(3) constPres":
                                    "Select Constant Dispense Pressure Mode",
                                "(4) varPres":
                                    "Select Variable Dispense Pressure Mode"}}
        super().__init__(**kwargs)

    ### ioMenuSpec METHODS
    def ioMenu_Operate(self):
        """*Performs Menu operations - loops*.

        | *Parameters*
        |   none

        | *Returns*
        |   flag, String with title of next menu to call
        """
        io_Prompt("This is filler text, enter any key to go back to main menu")
        return 'M0MainMenu'


class ioMenu_1PrintSequence(ioMenuSpec):
    """Contains data and methods for implemented PrintSequence Menu."""

    ### Construct/Destruct METHODS

    def __init__(self, **kwargs):
        """*Initializes Print Sequence Menu Object*.

        | *Parameters*
        |   none

        | *Returns*
        |   none
        ""

        ''' Param to pass into parent class
        |   name, name of the menu
        |   menuTitle, name of the menu
        |   menuItems, dictionary of menu options and text
        """
        kwargs = {'name': 'PrintSequenceMenu',
                  'menuTitle': 'Print Sequence Menu',
                  'menuItems': {Fore.LIGHTRED_EX + "[q]":
                                Fore.LIGHTRED_EX + "Quit",
                                Fore.LIGHTMAGENTA_EX + "[?]":
                                Fore.LIGHTMAGENTA_EX + "List Commands",
                                "STOP": "Emergency STOP",
                                "L": "Advanced Log Options",
                                "(0) clean": "raise/lower 20mm",
                                "(1) hardware": "Go to hardware menu",
                                "(2) plate": "Print plate",
                                "(3) gapLine": "Print Broken Line",
                                "(4) cuboid": "Print cuboid",
                                "(5) electrode1": "Print electrode1",
                                "(6) Line": "Print Simple Line +Reset",
                                "(7) hydroGrid": "Print Hydrogel Grid Pattern"
                                }}
        super().__init__(**kwargs)

### ioMenuSpec METHODS
    def ioMenu_Operate(self):
        """*Performs Menu operations - loops*.

        | *Parameters*
        |   none

        | *Returns*
        |   flag, String with title of next menu to call
        """
        io_Prompt("This is filler text, enter any key to go back to main menu")
        return 'M0MainMenu'

#############################################################################
### Start Sequence Methods
#############################################################################


def io_StartText():
    """*Displays start screen*.

    | *Parameters*
    |   none

    | *Returns*
    |   none
    """
    print(("#" * 80) + "\n" + ("#" * 80) + "\n\n")
    print("\tPolyChemPrintBP - Version:" + str(__version__)
          + "\tRevised: " + __date__ + "\n\n")
    print(("#" * 80) + "\n" + ("#" * 80) + "\n")


#########################################################################
### IO Helper METHODS
#########################################################################

def io_TestCode():
    """*Executes a block of test code from main menu*.

    | *Parameters*
    |   none

    | *Returns*
    |   none
    """
    print("Begin Test Code")
    print("End Test Code")


def io_Prompt(promptString, validate=False,
              validResponse=[''], caseSensitive=False):
    """*Prompts user for input and may validate against a list of options*.

    | *Parameters*
    |   promptString, String to display as prompt
    |   validate, Boolean for whether to validate input
    |   validResponse, list of valid input strings
    |   caseSensitive, whether prompt should be case sensitive

    | *Returns*
    |   inputString, inputString from user
    """
    global __lastInp__
    inString = input("\t" + promptString + '>').rstrip()

    if validate:

        if not caseSensitive:
            validString = (inString.upper() in validResponse
                           or inString.lower() in validResponse)
        else:
            validString = inString in validResponse

        if not validString:
            print(Fore.LIGHTRED_EX + "\tNot a valid response, try again.\n"
                  + Style.RESET_ALL)
            io_Prompt(promptString, validate, validResponse, caseSensitive)
        else:
            if not (inString in ["/"]):
                __lastInp__ = inString
    else:
        if not (inString in ["/"]):
            __lastInp__ = inString


    return inString


def io_savedCmdOps(inString):
    """*Executes a block of test code from main menu*.

    | *Parameters*
    |   none

    | *Returns*
    |   outString, the String to feed back into the menu loop
    |   promptIn, whether menu should prompt for input this cycle
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

    | *Parameters*
    |   initialMenuString, String telling which menu to begin on

    | *Returns*
    |   menuFlag, menuFlag for quitting program
    """
    menuFlag = initialMenuString
    while not menuFlag == 'quit':
        # Switch on menuflags
        if menuFlag == 'M0MainMenu':
            M0MainMenu.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M0MainMenu.ioMenu_Operate()
        elif menuFlag == 'M1SettingsMenu':
            M1SettingsMenu.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M1SettingsMenu.ioMenu_Operate()
        elif menuFlag == 'M1HardwareMenu':
            M1HardwareMenu.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M1HardwareMenu.ioMenu_Operate()
        elif menuFlag == 'M1PrintFile':
            M1PrintFile.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M1PrintFile.ioMenu_Operate()
        elif menuFlag == 'M2AxesOrigin':
            M2AxesOrigin.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M2AxesOrigin.ioMenu_Operate()
        elif menuFlag == 'M2PrintFileOptions':
            (M2PrintFileOptions.
             ioMenu_updateStoredCmds(__lastInp__, __savedInp__))
            menuFlag = M2PrintFileOptions.ioMenu_Operate()
        elif menuFlag == 'M1PrintSequence':
            M1PrintSequence.ioMenu_updateStoredCmds(__lastInp__, __savedInp__)
            menuFlag = M1PrintSequence.ioMenu_Operate()
        else:
            print("Internal CLI Error:"
                  + "Invalid flag returned from menu, resetting to main")
            menuFlag = 'M0MainMenu'

    return menuFlag


def io_loadSeq(seqDir):
    """*Search for, instantiate, and load sequence objects into seqDict*.

    Parameters
    ----------
    seqDir : Path
        Path object referring to directory where path scripts are located

    Returns
    list of Strings
        list of names of loaded sequence files

    """
    global __seqDict__
    print(Fore.LIGHTGREEN_EX
          + "Attempting to load sequences from root/sequence...")
    filesInFolder = os.listdir(seqDir)
    pySeq = []

    for name in filesInFolder:
        if (".py" in name[-3:]) and ("Spec" not in name):
            pySeq.append(name)

    syntaxValidSeq = []
    for seq in pySeq:
        try:
            compile(open(seqDir / seq, 'r').read(), seq, "exec")
            syntaxValidSeq.append(seq)
            print('\t' + seq + "\tpasses syntax check")
        except Exception as inst:
            print(Fore.LIGHTRED_EX+ '\t' + seq + "\tfailed syntax check")
        __seqDict__.update({seq[:-3]: seqDir / seq})

    print(Fore.LIGHTGREEN_EX + "Finished Loading Sequence Files..."
          + Style.RESET_ALL)






#############################################################################
### Global attributes
#############################################################################
# Program Details
__version__ = 3.0
__date__ = "2019/02/15"
__verbose__ = 1  # reflects how many status messages are shown
__rootDir__ = Path.cwd().parent / 'polychemprint3'

# User Input helper variables
__input__ = ""
__lastInp__ = ""
__savedInp__ = ""

# Instantiated menus
M0MainMenu = ioMenu_0Main()
M1SettingsMenu = ioMenu_1Settings()
M1HardwareMenu = ioMenu_1Hardware()
M1PrintFile = ioMenu_1PrintFile()
M2AxesOrigin = ioMenu_2AxesOrigin()
M2PrintFileOptions = ioMenu_2PrintFileOptions()
M1PrintSequence = ioMenu_1PrintSequence()

# Instantiated Hardware
axes = axes3D()
tool = nullTool()

# Instantiated Shapes
__seqDict__ = {}
io_loadSeq(__rootDir__ / 'sequence')

#############################################################################
### Main METHOD
#############################################################################


def main():
    """*Runs program*."""
    # Interface Start Sequencea
    io_StartText()
    logging.basicConfig(level=logging.DEBUG)  # logging
    init(convert=True)  # colorama


    # make software connections

    doQuitProgram = False
    # prevent ctrl+c from closing program
    while not doQuitProgram:

        try:

            # menuManagerSequence - loop that handles menu driving
            menuFlag = io_MenuManager(M0MainMenu.ioMenu_Operate())

            # if we get here, menumanager should have received quit message
            # Double check with user if they want to exit
            if menuFlag == 'quit':
                inp = io_Prompt(
                    promptString=("Really quit?"
                                  " or try an internal reset? (Y/N): "),
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
