# -*- coding: utf-8 -*-
""" user-specific preferences like directory and software options preferences.

| First created on Sat Oct 19 20:39:58 2019
| Revised: 05/17/2020 22:25:00
| Author: Bijal Patel

"""
from polychemprint3.utility.fileHandler import fileHandler
from polychemprint3.utility.loggerSpec import loggerSpec


class user(loggerSpec):
    def __init__(self,
                 name="unset",
                 creationDate="unset",
                 homeDirectory="unset",
                 filePath=None,
                 programSettings=None,
                 **kwargs):
        """*Initializes User object*

        | *Parameters* All default to "unset"
        |   name - user name (string)
        |   creationDate - date this user was first created
        |   homeDirectory - location of users data folder
        |   filePath - path to this user file
        |   programSettings - array of UI options

        | *Returns*
        |   none
        """
        self.name = name
        self.creationDate = creationDate
        self.homeDirectory = homeDirectory
        self.programSettings = programSettings
        self.filePath = filePath
        if programSettings is None:
            self.programSettings = {}
        super().__init__(**kwargs)




