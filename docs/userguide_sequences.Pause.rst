Pause Sequence
==============

Pause Sequence lets axes to pause for a certain amount time before precede to next movements. Usually pause is used to create time gap between sequences in a recipe. Here is what the pause menu looks like:

.. image:: /images/pause.png

**P1** through **P5** inform users the basic information of the pause sequence. **P6**, pausetime, is the time to wait before next command is send. For example, when circle sequence and line sequence are written into recipe to be execute simultaneously, add pause sequence between them will allow axes to be stopped for certain time after completion of circle. **P7** gives user ability to control whether precede to next sequence after waiting time runs out. Typing Y in **P7** will let program ask for user prompt to resume when pause time expired,and typing N will have program automatically move on to next commands when pause time expired.

**Tool ON, Tool OFF, PRIME, VIEW, and GO commands have been described in user guide **6.1.1** and **6.1.2**. Please see them for more information
