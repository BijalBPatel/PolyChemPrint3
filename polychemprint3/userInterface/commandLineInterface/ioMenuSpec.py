# -*- coding: utf-8 -*-
"""
The *ioMenuSpec* Abstract Base Class specifies the interface for CLI menus

| First created on Sun Oct 20 00:03:21 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""

from abc import ABC, abstractmethod
from polychemprint3.userInterface.commandLineInterface.ioElementSpec import ioElementSpec

class ioMenuSpec(ioElementSpec, ABC):

    #############################################################################
    ################### Construct/Destruct METHODS ##############################
    #############################################################################
        def __init__(self, menuTitle, menuItems, **kwargs):
            """*Initializes Tool Object*
            | *Parameters* 
            |   menuTitle, name of the menu
            |   menuItems, dictionary of menu options and text
            
            | *Returns*
            |   none 
            """
            self.menuTitle = menuTitle
            self.menuItems = menuItems
            super().__init__(**kwargs)
            
 
    #############################################################################
    ######################## UI_CLI_IOELement METHODS ###########################
    #############################################################################

        ######################### Operate METHOD #################################
        def io_Operate(self):
            """*Do the primary purpose of the CLI element*
            | *Parameters* 
            |   none
            
            | *Returns*
            |   none or flag, an optional string which reflects how operation terminated
            """
            self.UI_CLI_OperateMenu()
        
    #############################################################################
    ############################# Unique METHODS ################################
    #############################################################################

        ######################### Operation METHODS ############################# 
        def ioMenu_printMenu(self):
            """*Prints formatted menu options from menuItems dict*
            | *Parameters* 
            |   none
            
            | *Returns*
            |   none
            """
            print(self.menuTitle + "Menu: \n")
            for key in self.menuItems:
                print("\t%-25s|  %-25s\n" %(key,self.menuItems.get(key)))
                        
        @abstractmethod
        def ioMenu_Operate(self):
            """*Operate menu*
            | *Parameters* 
            |   none
        
            | *Returns*
            |   flag, String with title of next menu to call
            """
            self.UI_CLI_OperateMenu()
