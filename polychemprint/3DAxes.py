# -*- coding: utf-8 -*-
"""
The *3DAxes* Class contains data and operations for linear stages controlling bed and printhead motion.

| First created on Sat Oct 19 20:39:58 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel
  
Attributes
----------------
    :name: axes name
    :configuration: which axis? e.g., X, XY, XYZ
    :homeDirectory: directory for users data files on local pc
    :programSettings: catchall list for program settings (verbose etc.)

Methods
----------------
    :param: args
    :param: args
        
"""

class Axes3D:
    def __init__(self, name, creationDate,homeDirectory, verboseMode):
        self.name = name
        self.creationDate = creationDate
        self.homeDirectory = homeDirectory
        self.verboseMode = verboseMode
        