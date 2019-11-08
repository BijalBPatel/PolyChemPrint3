# -*- coding: utf-8 -*-
"""
| The *mainMethod* module runs the command line interface for PolyChemPrint and 'executes' the program.

| First created on Sat Oct 19 21:56:15 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""
#############################################################################
################### Import Statements #######################################
#############################################################################
from colorama import init, Fore, Back, Style 
from polychemprint3.userInterface.commandLineInterface.ioMenuSpec import ioMenuSpec

#############################################################################
################### Main METHOD ##############################
#############################################################################
def main():
    
    try:
         init(convert=True)
         verbose = 1
         print("Hello World!")
         while True:
             print("looping")
    except KeyboardInterrupt:
        print("Interrupted")

#if __name__ == "__main__":
 #   main()

#############################################################################
############################ Menu Classes ###################################
#############################################################################
class ioMenu_Main(ioMenuSpec):
    
    ################### Construct/Destruct METHODS ###########################
        def __init__(self, **kwargs):
            """*Initializes Tool Object*
            | *Parameters* 
            |   none
            
            | *Returns*
            |   none 
            """
            kwargs = {'name': 'Test',
                      'menuTitle':'Test', 
                      'menuItems':{'a':'b'}}
            super().__init__(**kwargs)

    ################### ioMenuSpec METHODS ###########################
        def ioMenuSpec(self):
            """*Operate menu*
            | *Parameters* 
            |   none
        
            | *Returns*
            |   flag, String with title of next menu to call
            """
           