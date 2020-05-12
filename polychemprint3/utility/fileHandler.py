# -*- coding: utf-8 -*-
"""Specifies interface for classes that will handle rw 'data' files.

| First created on Sun Oct 20 00:03:21 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""

from abc import ABC, abstractmethod
from colorama import Fore, Style
import logging
from itertools import islice


class fileHandler:
    """Base Class for objects that can read/write to file"""

    def __init__(self, fullFilePath=None, **kwargs):
        self.fullFilePath = fullFilePath
        super().__init__(**kwargs)

    ################### Helper Methods ###############################
    def testFileIO(self, modeString):
        """*Tests if file can be opened and closed*.

        Parameters
        ----------
        modeString : String
            mode with which to open file ("r,w,r+,a")

        Returns
        -------
        bool
            True/False if test passes/fails + errors

        """
        try:
            file = open(self.fullFilePath, modeString)
            # Close file
            file.close()
            return True
        except Exception as inst:
            print(Fore.LIGHTRED_EX + "Error Opening and Closing file\n"
                  + Style.RESET_ALL)
            logging.exception(inst)
            return False

            ################### File IO METHODS ###############################

    def overWriteToFile(self, outString):
        """*Completely overwrites file with new content from outString*.

        Parameters
        ----------
        outString : String
            the string to write to the file

        Returns
        -------
        bool
            True/False if writing passes/fails + errors
        """

        try:
            # Wipe file and open in writing mode
            file = open(self.fullFilePath, "w")

            # Write output to file
            file.write(outString)
            file.close()
            return True
        except Exception as inst:
            print(Fore.LIGHTRED_EX + "Error Overwriting to file\n"
                  + Style.RESET_ALL)
            logging.exception(inst)
            return False

    def appendToFile(self, outString):
        """*Appends to file with new content from outString*.

        Parameters
        ----------
            outString : String
                the string to write to the file

        Returns
        -------
            bool
                True/False if writing passes/fails + errors
        """
        if self.testFileIO("r+"):
            try:
                # Wipe file and open in writing mode
                file = open(self.fullFilePath, "w")

                # Write output to file
                file.write(outString)
                return True
            except Exception as inst:
                print(Fore.LIGHTRED_EX + "Error appending to file\n"
                      + Style.RESET_ALL)
                logging.exception(inst)
                return False
            finally:
                # Close file
                file.close()

    def readFullFile(self):
        """*Reads the entire file into memory as a list of strings*.

        Returns
        -------
            bool
                True/False if writing passes/fails + errors
            [lines]
                array of strings read in or ["Failed"]
        """
        if self.testFileIO("r"):
            try:
                # Open File for reading
                file = open(self.fullFilePath, "r")

                # Read in all as one text string, then split by newlines
                lines = file.read().split('\n')

                return True, lines
            except Exception as inst:
                print(Fore.LIGHTRED_EX + "Error reading from file\n"
                      + Style.RESET_ALL)
                logging.exception(inst)
                return False, ["Failed"]

            finally:
                # Close file
                file.close()

    def peekFile(self, numLines):
        """*Reads numLines from file and returns*.

        Parameters
        ----------
            numLines : int
                number of lines to read in from file

        Returns
        -------
            bool
                True/ False if read successful
            [lines]
                array of strings read in or ["Failed"]
        """
        if self.testFileIO("r"):
            try:
                # Open File for reading
                file = open(self.fullFilePath, "r")
                # Create generator
                lines = islice(file, numLines)
                outLines = []
                for line in lines:
                    outLines.append(line)
                    
                return True, outLines
            except Exception as inst:
                print(Fore.LIGHTRED_EX + "Error reading from file\n"
                      + Style.RESET_ALL)
                logging.exception(inst)
                return False, ["Failed"]
            finally:
                # Close file
                file.close()
