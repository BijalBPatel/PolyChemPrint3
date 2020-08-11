Inkscape 2D GCODE Tutorial
==========================
Inkscape is powerful, free, and high-quality drawing software often used to create attractive logos, diagrams, and more. Besides its functionality in drawing, it also has a default extension, GCodeTools, that allows user to generate Gcode from their 2D drawing.


Step 1: Set Properties of Document

a)	Open InkScape
b)	Click File on the top left corner
c)	Click Document Properties and a window will pop up for you to modify page size and units. (Note: the bottom left corner is the (0,0) coordinate)

Step 2: Draw Pattern (ex: text)

a)	Click text tool icon A on the left vertical bar to write text on the page
b)	Text style and size can be adjusted use top horizontal tool bar
c)	Make sure that your text is on the same layer

Step 3: Convert to Path

a)	Make sure that you have selected your text
b)	Click Path tab on top of Inkscape software and select Object to path
c)	Select your text again and click Path tab and select Dynamic Offset

Step 4: GCODE Tools

a)	Click Extension tab on the top of Inkscape software and select GcodeTools
b)	Then click Tools library and a window will pop up
c)	Now, you can select the correct tool type you want to use for the design and click Apply
d)	A green window will appear for you to modify tool parameter. You must first click text icon A in order to edit those parameters.
e)	Set feed to 9999, set the passing feed to 1000, and set the penetration speed to 9998 

Step 5: Set Orientation Points

a)	From the extension tab on the navigation panel, select GCodetools, and then select Orientation Points
b)	A window will pop up and you can select the desired orientation type. For Orientation type, choose 2-points mode. Set Z surface to 0.000 and Z-depth to -1
c)	Click Apply when you are done and you should see two coordinates point appearing on your drawing sheet. One on the bottom left corner with coordinates of (0,0; 0,0; 0,0). The other one on the on the bottom margin of drawing sheet with coordinates of (100.0; 0.0; -1.0)

Step 6: Generate GCODE

a)	Click Extension tap on the top and select Gcodetools
b)	Click Path to Gcode and a window with four tabs will appear
c)	Under the Preference tap, you can edit file name and the directory of the file. Remember to set Z safe height to 3
d)	Other tabs allow to further edit Gcode information such as maximum splitting depth and cutting order
e)	After done editing parameters, click Path to Gcode tab on top of this window and make sure to check sort path to reduse rapid distance
f)	Click Apply and Gcode file is generated. You should see arrows cover the margin of your drawing 

Convert image to Gcode file (only for 2D)

a)	Import image into Inkscape. 
b)	Click Path tab on top of the software and select Trace Bitmap
c)	A window will pop up and you can select proper scan mode to trace the edge of image 
d)	Click OK after selecting the correct mode
e)	Follow step 3, 4, 5, 6 in Convert Drawing Text to Gcode to generate Gcode file

