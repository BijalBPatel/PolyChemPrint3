# -*- coding: utf-8 -*-
"""Contains ioMenu Abstract Base Class.

| First created on Sun Oct 20 00:03:21 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""
from abc import ABC, abstractmethod
from colorama import Fore, Style
from polychemprint3.commandLineInterface.ioElementSpec \
    import ioElementSpec


class ioMenuSpec(ioElementSpec, ABC):
    """Specifies the interface for CLI menus."""

    #####################################################################
    ### Construct/Destruct METHODS
    #####################################################################
    def __init__(self, menuTitle, menuItems, lastCmd="", memCmd="", **kwargs):
        """*Initializes Menu Object*.

        Parameters
        ----------
        menuTitle: string
            name of the menu
        menuItems: Dict of strings
            menu options and text
        lastCmd: string
            last command entered
        memCmd: String
            saved command entered
        """
        self.menuTitle = menuTitle
        self.menuItems = menuItems
        self.lastCmd = lastCmd
        self.memCmd = memCmd
        super().__init__(**kwargs)

    #####################################################################
    ### UI_CLI_IOELement METHODS
    #####################################################################

    @abstractmethod
    def io_Operate(self):
        pass

    def ioMenu_printMenu(self):
        """*Prints formatted menu options from menuItems dict*."""
        print("-" * 120)
        print("###\t" + self.menuTitle)
        print("-" * 120)
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

    def ioMenu_updateStoredCmds(self, lastCmd, memCmd):
        """*Updates stored commands local to this menu item from inputs*.

        Parameters
        ----------
        lastCmd: String
            specifying the last command entered
        memCmd: String
            specifying the command saved to memory
        """
        self.lastCmd = lastCmd
        self.memCmd = memCmd
