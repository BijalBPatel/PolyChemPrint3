"""
The *ioElementSpec* Abstract Base Class specifies the interface for CLI menus/text/etc

| First created on Sun Oct 20 00:03:21 2019
| Revised: 6/11/2019 00:34:27
| Author: Bijal Patel

"""

from abc import ABC, abstractmethod

class ioElementSpec(ABC):
    #############################################################################
    ################### Construct/Destruct METHODS ##############################
    #############################################################################
        def __init__(self, name, **kwargs):
            """*Initializes Tool Object*
            | *Parameters* 
            |   menuItems, dictionary of menu options and text
            
            | *Returns*
            |   none 
            """
            self.name=name
    ############################# IO METHODS ################################
        def io_Prompt(self,promptString, validate=False, validResponse=[], caseSensitive=False):
            """*Prompts user for input and optionally validates against a list of options*
            | *Parameters* 
            |   promptString, String to display as prompt
            |   validate, Boolean for whether to validate input
            |   validResponse, list of valid input strings
            |   caseSensitive, whether prompt should be case sensitive
            
            | *Returns*
            |   inputString, inputString from user 
            """
            inString = input(promptString).rstrip()
            
            if validate:
                
                if not caseSensitive:
                    validString = inString.upper() in validResponse or inString.upper() in validResponse
                else:
                    validString = inString in validResponse
                        
                while not validString:
                    print("Not a valid response, try again.\n")
                    inString = input(promptString).rstrip()
                    
                    if not caseSensitive:
                        validString = inString.upper() in validResponse or inString.upper() in validResponse
                    else:
                        validString = inString in validResponse    
            return inString
            
    ############################# Operate METHODS ###########################
        @abstractmethod
        def io_Operate(self):
            """*Do the primary purpose of the CLI element*
            | *Parameters* 
            |   none
            
            | *Returns*
            |   none or flag, an optional string which reflects how operation terminated
            """
            pass
            