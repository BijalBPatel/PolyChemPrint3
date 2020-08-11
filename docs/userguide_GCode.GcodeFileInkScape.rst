GcodeFileInkScape Sequence
==========================

This sequence allows locally stored Gcode file obtained through InkScape software to be imported into polychemprint3.Here is what menu of this sequence looks like:

.. image:: /images/inkscapemenu.png

**P1** through **P5** inform user the basic information of the GcodeFileInkScape sequence. **P6** gives users options to select the objective file. Users can either type in the full file path or just type in File to opens up a GUI window and choose the matching file like follow:

.. image:: /images/inkscapeopenfile.png

**P7** controls moving speed of axes in x and y direction when printing and **P8** represents the speed of axes when tool is not print but sequence is still running. **P9** is the speed of axes when traveling in z direction. The unit regarding speed is in mm/min. **P10, Z hop height**, controls the distance axes moves in positive z direction when two lines are crossed. Axes need to be move up to avoid collision of material, thus called hop height. The unit is in mm.


