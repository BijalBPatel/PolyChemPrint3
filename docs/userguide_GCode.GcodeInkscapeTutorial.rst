Inkscape 2D GCODE Tutorial
==========================
The free and open source vector image software `Inkscape <Inkscape.org>`__ can be used to generate G-code for complex 2D patterns that can then be imported into polychemprint3. We will be using the plugin `GCodeTools <https://github.com/cnc-club/gcodetools>`__ (included by default with Inkscape).

Below is a step-by-step tutorial for creating a vector image and generating PCP3-compatible GCode.

**Step 1: Set Canvas Dimensions**

a)	Open InkScape
b)	Click File -> Document Properties
c)  In the window that appears, set the page size and units. Note: the bottom left corner is the (0,0) coordinate.

**Step 2: Draw your pattern** (ex: text, shapes, and bezier curves)

a)	Create a layer for your pattern (shift + ctrl + L) to open the layer window.
b)  From the tools panel at left, choose either the text tool or one of the drawing tools and draw your pattern.
c)	For complex patterns, it can be helpful to paste a picture into a layer below your working layer, set it to ~60% opacity, lock it, and then 'trace' a pattern on your working layer with bezier curves.
d)  Note: There is technically a way to auto-generate paths from non-vector drawings, but I have not been able to get it to work. After import an image into Inkscape, you can click Path-> Trace Bitmap. In the window that appears, choose a tracing mode and your path will be generated. Unfortunately, all modes generate 'double-paths' except centerline tracing, which just crashes (as of 12/17/20).

**Step 3: Convert to Path**

a)	Select all of your 'artwork' in the working layer.
b)	From the top toolbar, choose Path -> Object to path
c)  Before you proceed, go to node view (n) and try to simplify the nodes as much as you can while maintaining pattern fidelity. Having a huge number of nodes will lead to having many many tiny steps that the printer will execute, increasing pritn time and reducing stability. If you have overlapping nodes (e.g., two lines coming to a point), use the 'join nodes' tool to combine them.
d)  At this stage, your artwork is complete. Clone this layer to a new layer above this one and hide and lock all sublayers.

**Step 4: Setup Orientation Points**

a)	From the top toolbar, choose Extensions -> GCodeTools -> Orientation Points.
b)  In the window that appears:

    * Choose 2-points mode
    * Set Z surface to 0.000
    * Set Z-depth to -1.

c)  Click Apply when you are done and you should see two coordinates point appearing on your drawing sheet. One on the bottom left corner with coordinates of (0,0; 0,0; 0,0). The other one on the on the bottom margin of drawing sheet with coordinates of (100.0; 0.0; -1.0)

**Step 5: Setup the Tool**

a)  From the top toolbar, choose Extensions -> GCodeTools -> Tools Library.
b)	In the window that appears, select  the 'default' tool and press Apply.
c)	A text panel will appear on top of your drawing. Move it to the side with the selection tool (S) and then select the text editing tool (T).
d)  Edit the following parameters in the text panel.
    * Set diameter to your tool diameter (optional).
    * Set feed to 9999.
    * Set penetration feed to 9998.
    * Set passing feed to 1000.

**Step 6: Enter G-code processing parameters**

a)	From the top toolbar, choose Extensions -> GCodeTools -> Path-to-Gcode. A window with 4 tabs will appear.
b)	In the "Path to GCode" tab, set the cutting order to "pass by pass".
c)  In the "Options" tab, set the 'Offset along Z axis' to 1.00. Also, check the "Select all paths if nothing is selected" checkbox.
d)	In the "Preferences" tab:

    * Enter the filename for your exported G-code file.
    * Enter the full path to the export directory in the 'directory' field.
    * Set 'Z safe height for G00 move over blank' to 2.00'

e)  Generate log files if you would like.
f) At this stage, everything is ready to generate a gcode file. Clone the layer above your current layer and lock/hide all previous layers.

**Step 7: Generate and export G-code File**

a)  With the "Path-to-Gcode" tab of the "Path-to-Gcode" panel open, click apply.
b)  If a warning appears that no paths were selected, just press ok and GCodeTools will attempt to use all paths.

**Step 8: Validate GCode File** [Strongly recommended]

a)  Open the G-code file that you have generated and look through it for obvious errors such as:

    * No/ very few commands -> Likely the plugin didnt select your drawing, or your drawing wasnt in the top layer.
    * Printing steps aren't at Z0, travel steps arent at Z3. -> you have made a mistake in steps 4 or 6.

b)  Use a program like `CAMotics <camotics.org>`__ or `NC Viewer <https://ncviewer.com/>`__ to visually inspect the toolpath BEFORE you try it on the printer.