Hardware Menu
=============

This menu allows for the most basic communication to the hardware: line by line command entry and execution, along with some hotkeys for jogging the motion axes.

.. image:: /images/hardwaremenu.png

GCODE Entry
###########

Direct GCODE commands are accepted as input in Hardware Menu. For example, if the axes need to be moved in the positive x direction for 20 mm, Gcode command **“G0 X20”** can be typed in to perform such task, as shown below.

.. image:: /images/GcodeControl.png


Controlling Tools
#################

**Set Tool Value**
  Type in **T[value]** under **Hardware Menu** allows users to directly set tool values. For example, to set tool value to 100, users can type in **T100** in terminal and program will give an output indicting value is set like the following:

  .. image:: /images/toolvalue.png

**Turning Tool On and Off**
  Type in **Toff** or **Ton** to engage tool dispense or disengage tool dispense. It works just like a switch that turns the tool from off to on or on to off.

  .. image:: /images/ToolOnOff.png

  But if the current state of tool is off and a Toff command is executed, program will give a warning message saying that **“Dispense already off”**.  If the current state is on, Ton command is sent, program will also give error message saying **“Dispense already on”** These are handy for troubleshooting sequences/recipes, but are otherwise just for your information.

  .. image:: /images/ToolAlreadlyOn.png

Hotkeys for Jogging Axes
########################

For convenience, the following commands jog axes for small distance movement in all direction. (Note that these are not case sensitive)

  +----------+----------+----------+
  | Command  | Direction| Distance |
  +==========+==========+==========+
  |      a   |      -x  |    1mm   |
  +----------+----------+----------+
  |      d   |       x  |    1mm   |
  +----------+----------+----------+
  |      r   |      -y  |    1mm   |
  +----------+----------+----------+
  |      f   |       y  |    1mm   |
  +----------+----------+----------+
  |      s   |      -z  |    1mm   |
  +----------+----------+----------+
  |      w   |       z  |    1mm   |
  +----------+----------+----------+
  |      x   |      -z  |   0.1mm  |
  +----------+----------+----------+
  |      z   |      -z  |   0.01mm |
  +----------+----------+----------+
  
  .. image:: /images/MoveAxes.png
 
Clean and Raise Routines
########################

  Commands **1** and **0** provide convenient ways to lift the toolhead 20 mm. 
  If command **0** is chosen,the terminal will prompt on whether to lower 20mm or not. Type in **Y**, axes will be lowered for 20 mm in Z direction. Type in **N**, axes will stay still.

  .. image:: /images/CleanAxes.png


T ? , / . Commands 
##################

Functions of T ? , / and . have been described in user guide section **3.3**. Please see it for more information.


Quit Hardware Menu
##################

To exit out of the **Hardware Menu**, type **q** in the prompt and you will be returned to the **Main Menu**.
