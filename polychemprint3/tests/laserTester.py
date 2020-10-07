from polychemprint3.tools import *
from polychemprint3.tools.laser6W import laser6W

las = laser6W()
print(las.activate())
print(las.deactivate())