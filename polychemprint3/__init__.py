import sys, os
import importlib
import pkgutil

sys.path.insert(0, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
import polychemprint3

from polychemprint3 import __main__
from polychemprint3 import tools, sequence, axes, commandLineInterface, user, utility
from polychemprint3.tools import *
from polychemprint3.sequence import *
from polychemprint3.axes import *
from polychemprint3.commandLineInterface import *
from polychemprint3.user import *
from polychemprint3.utility import *

def main():
    __main__.main()
if __name__ == "__main__":
    main()
