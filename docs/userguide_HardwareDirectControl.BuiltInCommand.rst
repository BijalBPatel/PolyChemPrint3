Built-in Commands to Control Hareware
=====================================

**Set Tool Value**
  Type in **T[value]** under **Hardware Menu** allows users to directly set tool values. For example, to set tool value to 100, users can type in **T100** in terminal and program will give an output indicting value is set like the following:

  .. image:: /images/toolvalue.png

**Turning Tool On and Off**
  Type in **Toff** or **Ton** to engage tool dispense or disengage tool dispense. It works juts like a switch that turns the tool from off to on or on to off.

  .. image:: /images/ToolOnOff.png

  But if the current state of tool is off and a Toff command is executed, program will give an error output saying that **“Dispense already off”**.  If the current state is on, Ton command is sent, program will also give error message saying **“Dispense already on”**

  .. image:: /images/ToolAlreadlyOn.png

**Move Axes**
  Since Gcode command is a bit long to type in every time there is a need for moving axes, especially for moving multiple small distances. Built in commands to jog axes for small distance movement in all direction are available. (Note polychemprint3 is not case sensitive))

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

  To lift axes for a long distance, command **1** and **0** both can perform the task. However, command **0** gives choice to lower the axes after lift.
  By type in command **0**, axes will be lifted in positive z direction for 20 mm, and terminal will require a user prompt whether to lower 20mm or not. Type in **Y**, axes will be lowered for 20 mm in Z direction. Type in **N**, axes will stay still.

  .. image:: /images/CleanAxes.png

