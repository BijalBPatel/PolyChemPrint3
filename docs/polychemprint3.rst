PCP3 Package Overview
=====================

PolyChemPrint3 is written as a (mostly) object-oriented program. The package is structured such that each "Type" of object is contained in its own folder/module in the root directory. Within each of these folders are the abstract base classes (if required) and classes that contain implementations for specific hardware/software/sequences/recipes etc.


Submodule/Folder Directory
--------------------------

.. toctree::
   :maxdepth: 1

   polychemprint3.commandLineInterface
   polychemprint3.data
   polychemprint3.axes
   polychemprint3.tools
   polychemprint3.recipes
   polychemprint3.sequence
   polychemprint3.user
   polychemprint3.utility
