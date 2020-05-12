# -*- coding: utf-8 -*-
"""Specifies interface for all classes to read/write themselves to string.

| First created on Sun Oct 20 00:03:21 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""
from abc import ABC, abstractmethod
import yaml


class loggerSpec(ABC):
    """Abstract Base Class for objects that can generate log strings."""

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    ### Logging METHODS

    def writeLogSelf(self):
        """*Generates yaml string containing dict to be written to log file*.

        Returns
        -------
        String
            log in yaml string format
        """
        return yaml.dump(self.__dict__)

    def loadLogSelf(self, yamlString):
        """*loads yaml log back into dict*.

        Parameters
        ----------
        yamlString: String
            yaml string to be loaded back in

        """
        self.__dict__ = yaml.load(yamlString)
