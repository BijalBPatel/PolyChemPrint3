# -*- coding: utf-8 -*-
"""Contains ioElementSpec Abstract Base Class.

| First created on Sun Oct 20 00:03:21 2019
| Revised (dd/mm/yyyy): 20/12/2020 - BP
| Author: Bijal Patel

"""
# Imports ####################################################################
from abc import ABC, abstractmethod


class ioElementSpec(ABC):
    """Specifies the interface for CLI menus/text/etc."""

    # Construct/Destruct METHODS ##############################################
    def __init__(self, name, **kwargs):
        """Initializes command line interface element.

        Parameters
        ----------
        name: str
            the name of CLI element
        """
        self.name = name

    # Operation METHODS #######################################################
    @abstractmethod
    def io_Operate(self):
        """*Do the primary purpose of the CLI element*.

        Returns
        -------
        str
            an optional flag which either reflects how operation went,
            or is direction for future CLI operations.
        """
        pass
