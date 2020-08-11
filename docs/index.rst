.. PolyChemPrint3 documentation master file, created by
   sphinx-quickstart on Thu May 28 00:15:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PolyChemPrint3's User Guide and Software Documentation!
==================================================================

PolyChemPrint3 is an `open source`_ benchtop additive manufacturing software developed at the University of Illinois by Bijal Patel and Dr. Ying Diao. For more information, please visit the `project homepage`_ and `Diao Research Group homepage`_.

.. _open source: https://github.com/BijalBPatel/PolyChemPrint3/blob/master/LICENSE.txt
.. _project homepage: https://publish.illinois.edu/polychemprint3
.. _Diao Research Group homepage: http://diao.scs.illinois.edu/Diao_Lab/Home.html

This readthedocs.io page contains: 
	A 'user guide' with instructions on setting up and operating the program. 
	
	A 'software guide' intended as a programming aid that contains the organized python docstrings for the modules, classes, and methods of this object-oriented program.
	
Note: If you use this software/code, please cite the `original paper`_ listed on the project homepage! It really helps!

.. _original paper: https://publish.illinois.edu/polychemprint3/


.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: User Guide
   
   userguide_overview
   userguide_install
   userguide_navigation
   userguide_configuration
   userguide_HardwareDirectControl
   userguide_sequences
   userguide_GCode
   userguide_recipes
   userguide_userprofiles
   userguide_logging
   
   
.. toctree::
   :maxdepth: 1
   :caption: Software Guide

   polychemprint3
   polychemprint3.commandLineInterface
   polychemprint3.data
   polychemprint3.axes
   polychemprint3.tools
   polychemprint3.recipes
   polychemprint3.sequence
   polychemprint3.user
   polychemprint3.utility
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
