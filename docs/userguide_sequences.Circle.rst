Circle Sequence
===============

Circle is a sequence that lets axes moves in a circle with radius set by user. Below is the menu of circle:

.. image:: /images/Circle.png
   
**P1** through **P5** inform users the basic information of this sequence. **P6** controls the speed of the axes movement and unit is in mm/min. **P7** command controls the radius of the circle. Since hardware like 3D printer is limited to straight move only, axes have to move step by step in x and y direction to create roughly round object. That is where **P8** comes from. It represents the step axes moves in x and y. A smaller **P8** value lead to a more circular shape. 

**Tool ON and OFF Value**

**P9** and **P10** control the on and off tool value. For example, when trying to do laser cutting, the energy of laser when print, on value, will be like 100 watts, and off value will be 0. Users should adjust the P8 and P9 based on the tool they are using.




