# -*- coding: utf-8 -*-
"""
The *userSpec* Class holds data and operations relating to software users such as home directory and software preferences.

| First created on Sat Oct 19 20:39:58 2019
| Revised: 23/10/2019 14:06:59
| Author: Bijal Patel

"""
import sys
sys.path.append("../../")
class userSpec:
    def __init__(self, name="unset", creationDate="unset", homeDirectory="unset", programSettings="unset"):
        """*Initializes User object*

        | *Parameters* All default to "unset"
        |   name - user name (string)
        |   creationDate - date this user was first created
        |   homeDirectory - location of users data folder
        |   programSettings - array of UI options

        | *Returns*
        |   none
        """

        self.name = name
        self.creationDate = creationDate
        self.homeDirectory = homeDirectory
        self.programSettings = programSettings




