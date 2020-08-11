Program Overview
================

PolyChemPrint3 (PCP3) is a command-line interface (CLI) Windows/Linux program that handles communication between the user and additive manufacturing(AM) hardware. In some ways, PCP3 offers overlapping functionality with 3D printer control software such as pronterface_ and 3D slicing programs such as slic3r_ or Cura_, but optimized for AM research with unconventional, non-FDM toolheads such as pneumatic (melt) extruders, LASERs, syringe pumps, etc.

.. _pronterface: https://www.pronterface.com/
.. _slic3r: https://slic3r.org/
.. _Cura: https://ultimaker.com/software/ultimaker-cura

.. image:: /images/overview.png

At the most basic level, users can directly send commands to the motion axes and toolhead to execute GCode move sequences and simple tool on/off/ power set commands. The next level up is to use parameterized, hardcoded 'sequences' to execute specific 2D and 3D patterns such as meanderlines, cuboids, electrode patterns, etc. For more complex 2D/3D patterns, GCode files created by slicers such as GCodeTools in Inkscape and Cura/ Slic3r can be imported as sequences. Finally, any combination of sequences can be chained together into 'Recipes', offering a 'code-free' way to build-up complex patterns. Automatic data-logging exports print parameters to text files to optimize parameter screening. 

Note: Even if you have identical hardware to the original developers, the software will need some initial setup - so pay careful attention to the "Installation and Setup" section. Best of luck!
