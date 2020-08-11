GcodeFile3DSlicer Sequence
==========================

This sequence allows locally stored Gcode file obtained through InkScape software to be imported into polychemprint3.Here is what menu of this sequence looks like:

.. image:: /images/GCode3DMenu.png

**P1** through **P5** are basic information describing the sequence. **P6** gives users options to select the .gcode file. Users can either type in the full file path or type in "File" to opens up a GUI window and choose the matching file like follow:

**P7** - **P9** Allow the user to set the tool on, off, and travel values. Upon importing FDM Gcode, the program automatically converts from extruder positions to tool on/off triggers. 
