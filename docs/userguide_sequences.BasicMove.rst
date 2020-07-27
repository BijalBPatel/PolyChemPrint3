Basic Move Sequence
===================

**BasicMove** is a sequence that control axes to move in x, y and z direction. Its menu looks like the following:

.. image:: /images/basicmove.png

The top five commands (**P1** to **P5**) introduce the basic information of this sequence including the name, created date and etc. **P6** allows user to change the reference the command is execute from, whether relative to current position or the absolute reference, which is the origin. **P7** is the axes speed that controls how fast axes should move and the unit is in mm/min. **P8** through **P10** represent the distance axes is going to move move in x, y, and z direction. The unit is in mm. 

**PRIME,VIEW, and GO**

After modifying a parameter, **GO** command allows the execution of the sequence and corresponding Gcode command will be displayed on the terminal. It is highly recommended to do **PRIME** and **VIEW** command before engaging printing sequence. **PRIME** command will generate the print commands without actual execution done by hardware and **VIEW** will show those commands on terminal for user to review. Thus, it is best to do **PRIME** and **VIEW** to check on print commands in case there is errors that might break hardware



   


