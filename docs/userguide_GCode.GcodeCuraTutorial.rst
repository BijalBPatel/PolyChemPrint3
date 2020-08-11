Cura 3D GCode Tutorial
======================
Cura is a free software that converts CAD files (commonly .STL) into GCode for FDM printers. We do not give an exhaustive tutorial of Cura here, but instead briefly outline the process and note the parameters you must select in order for PCP3 to properly import GCode.

Steo 0: Printer/ Program Settings

Either create a "Custom FFF Printer" or modify your 3D pritner's profile to reflect the following.

1. Delete any start or end Gcode.
2. Set the origin at center of the bed.
3. Select Marlin as the Gcode flavor.
4. Set the nozzle diameter to the diameter of the nozzle you are using (or feature size of LASER etch lines etc.)

Step 1: Import STL file

1.	Click File on the top bar and select Open Files
2.	Select the STL file you want to generate G-code from .
3.	Properly adjust orientation of your object. Make sure it is in contact with the bed.
4. In the print settings make the following changes: 
	
	a. Set the layer height to the height of your material under the desired printing conditions
	b. Set the print speed (for all parts) to be the desired printing speed.
	c. Turn off build plate adhesion tools like skirts or brims (unless you want them)

Step 2: Slice Object

1.	After done adjusting parameters, the bottom right corner will state “Ready to Slice”
2.	Please wait until it states “Ready to Save to File” and precede to step 3

Step 3: Generate G-code

1.	Click “Save to File” button on the bottom right corner
2.	Select the desired directory and click save 
3.	GCODE file is generated.

