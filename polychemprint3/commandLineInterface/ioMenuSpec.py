# -*- coding: utf-8 -*-
"""Contains ioMenuSpec Abstract Base Class.

| First created on Sun Oct 20 00:03:21 2019
| Revised (dd/mm/yyyy): 20/12/2020 - BP
| Author: Bijal Patel

"""
# Imports ####################################################################
from abc import ABC, abstractmethod
from colorama import Fore, Style
from polychemprint3.commandLineInterface.ioElementSpec \
    import ioElementSpec


class ioMenuSpec(ioElementSpec, ABC):
    """Specifies the interface for CLI menus."""

    # Construct/Destruct Methods #############################################
    def __init__(self, menuTitle, menuItems, menuDesc="",
                 menuInstruc="Choose from the following menu items:",
                 lastCmd="", memCmd="", **kwargs):
        """Initializes Menu Object.

        Parameters
        ----------
        menuTitle: str
            name of the menu
        menuItems: dict of str
            menu options and text
        menuDesc: str
            description of the menu, to print in the menu header
        menuInstruc: str
            instructions for the user on how to use this menu
        lastCmd: str
            last command entered
        memCmd: str
            saved command entered
        """
        self.menuTitle = menuTitle
        self.menuItems = menuItems
        self.menuDesc = menuDesc
        self.menuInstruc = menuInstruc
        self.lastCmd = lastCmd
        self.memCmd = memCmd
        super().__init__(**kwargs)

    # ioElementSpec Methods ##################################################
    @abstractmethod
    def io_Operate(self):
        """Performs menu operations and loops on user input.
        Returns
        -------
            str
                Title of next menu to present.
        """

        pass

    def ioMenu_printMenu(self, showStoredCmds = True):
        """Prints formatted menu options from menuItems dict."""
        # Print Header
        print(Style.RESET_ALL + "-" * 150)
        print("###\t" + self.menuTitle + " - " + self.menuDesc)
        print("-" * 150)
        print(Fore.WHITE + '\t' + self.menuInstruc)

        # Print std menu options
        for key in sorted(self.menuItems):
            print("\t%-40s|  %-25s" % (key, self.menuItems.get(key)))
        print(Style.RESET_ALL)

        if showStoredCmds:
            storedCmds = {Fore.LIGHTCYAN_EX
                          + "[/] Repeat Last Command": self.lastCmd,
                          Fore.LIGHTCYAN_EX
                          + "[.] Repeat Saved Command": self.memCmd,
                          Fore.LIGHTCYAN_EX
                          + "[,] Store Saved Command": "Will Prompt for command"}
            for key in storedCmds:
                print("\t%-40s|  %-25s" % (key, storedCmds.get(key))
                      + Style.RESET_ALL)

    def ioMenu_updateStoredCmds(self, lastCmd, memCmd):
        """Updates stored commands local to this menu item from inputs.

        Parameters
        ----------
        lastCmd: str
            specifying the last command entered
        memCmd: str
            specifying the command saved to memory
        """
        self.lastCmd = lastCmd
        self.memCmd = memCmd
