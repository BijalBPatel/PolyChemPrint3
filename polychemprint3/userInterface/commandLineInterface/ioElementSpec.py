# -*- coding: utf-8 -*-
"""Contains ioElementSpec Abstract Base Class.

| First created on Sun Oct 20 00:03:21 2019
| Revised: 6/11/2019 00:34:27
| Author: Bijal Patel


"""
import sys
sys.path.append("../../../")
from abc import ABC, abstractmethod


class ioElementSpec(ABC):
    """Specifies the interface for CLI menus/text/etc."""

    ###########################################################################
    ### Construct/Destruct METHODS
    ###########################################################################
    def __init__(self, name, **kwargs):
        """*Initializes command line interface element*.

        | *Parameters*
        |   name, the name of CLI element

        | *Returns*
        |   none
        """
        self.name = name

    ###########################################################################
    ### Operation METHODS
    ###########################################################################
    @abstractmethod
    def io_Operate(self):
        """*Do the primary purpose of the CLI element*.

        | *Parameters*
        |   none

        | *Returns*
        |   flag, an optional string which reflects how operation terminated
        """
        pass
