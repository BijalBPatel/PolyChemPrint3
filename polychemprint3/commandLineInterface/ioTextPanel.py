# -*- coding: utf-8 -*-
"""Contains ioTextPanelSpec Abstract Base Class.

| First created on Sun Oct 20 00:03:21 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""
from colorama import Fore, Style
import logging
from polychemprint3.commandLineInterface.ioElementSpec \
    import ioElementSpec
from polychemprint3.utility.fileHandler import fileHandler


class ioTextPanel(fileHandler, ioElementSpec):
    """Specifies the interface for CLI menus."""

    def __init__(self, panelTitle, fullFilePath, **kwargs):
        """*Initializes Tool Object*.

        Parameters
        ----------
        fullFilePath: Path object
            referring to file to open
        panelTitle: String
        """
        self.panelTitle = panelTitle
        kwargs = {'fullFilePath': fullFilePath,
                  'name': panelTitle}
        super().__init__(**kwargs)

    def io_Operate(self):
        """*Prints formatted text from file*."""
        # load from file then print
        try:
            readStatus, readData = self.readFullFile()
            if readStatus:
                for read in readData:
                    print("\t%s" % read)
        except Exception as inst:
            print(Fore.LIGHTRED_EX + '\t\tfailed to open file')
            logging.exception(inst)
