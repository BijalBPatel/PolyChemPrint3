SetToolStatus Sequence
======================

This sequence is typically implemented in a recipe between two sequences to change the status or the value of tool. Here is what it looks like:

.. image:: /images/toolstatus.png

P1 through P5 informs users the basic information of the line sequence. P6 lets user decide on tool status. There choices are available: change tool status to on, off, or not change. P7 controls the new tool value. For example, if circle sequence has juts been complete with a tool on value of 100, setting P7 to 200, will alter the tool on value of the next sequence to be 200.

**Not very certain what this sequence does**

**Tool ON**, **Tool OFF**, **PRIME**, **VIEW**, and **GO** commands have been described in user guide **6.1.1** and **6.1.2**. Please see them for more information



