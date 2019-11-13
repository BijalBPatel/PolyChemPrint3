# -*- coding: utf-8 -*-
"""
Specifies modular pre-written motion and dispense sequences for common prints.

| First created on Sun Oct 20 00:08:15 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

"""
import sys
sys.path.append("../../")
class sequenceSpec:
    def __init__(self, name, creationDate,homeDirectory, verboseMode):
        self.name = name
        self.creationDate = creationDate
        self.homeDirectory = homeDirectory
        self.verboseMode = verboseMode