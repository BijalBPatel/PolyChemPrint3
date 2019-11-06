# -*- coding: utf-8 -*-
"""
The *Shape* Class contains data and functions for modular pre-written motion and dispense sequences for common test prints.

| First created on Sun Oct 20 00:08:15 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""

class Shape:
    def __init__(self, name, creationDate,homeDirectory, verboseMode):
        self.name = name
        self.creationDate = creationDate
        self.homeDirectory = homeDirectory
        self.verboseMode = verboseMode
        