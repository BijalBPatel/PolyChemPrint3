Recipe Menu
===========

Recipe are a combination of sequences to be executed in series. The constituent sequences each can take on their own parameters and duplicates are allowed. This can be very useful for combinatorial screening, or even just for printing a batch of identical samples in one long run, without user intervention. It is also possible to include 'interrupt' sequences that prompt for user input, e.g. to confirm the nozzle is clean/ swap out substrates/ etc. between prints. Because recipes can become quite long, they are stored as text files (.yaml) and only one recipe is fully loaded into RAM at a time, the "active recipe". For convenience, basic details of all recipes can be seen from the loading screen. 

Note: Recipes are NOT meant to be created outside of PCP3. Although it is possible to edit .yaml files, it is not encouraged.

The recipe menu is shown below:

.. image:: /images/recipe.png

At program launch, no recipe is loaded and thus sequences cannot be added.

Creating a new Recipe
######################

To build a new recipe, type **3**, **Build a New Recipe**, in **Recipe Menu** and the program will ask for user input regarding the name and description of the new recipe. The newly created recipe will be empty of any sequences. Picture below shows the procedure on create a new recipe (commands entered are boxed by red). By default, the new recipe becomes the active recipe.

.. image:: /images/buildrecipe.png


Modifying/Saving Active Recipe
##############################

Type **2** in **Recipe Menu** to access the **Modify/Save Active Recipe** menu and users can adjust that recipe by remove/add sequences, change parameters, or saving to the yaml file. 

.. image:: /images/modifyrecipe.png

**Edit basic information**
  One bottom portion of **Modify/Save Active Recipe** menu, information about activated recipe is shown. Description information includes name, description,     creation date are shown. To modify these information, type **0** in terminal to edit text in P0 through P2(commands entered are boxed by red).

  .. image:: /images/editrecipe.png

**Add Sequence**
  To add a sequence, type **1** in the terminal and user will be brought to print sequence menu to choose a sequence to add. Type the code of the sequence user want   and the matching sequence menu will be displayed for user to edit parameters. (For more detailed information about sequences, please see sequence menu). After   finishing modifying parameters, type in **ADD** in terminal to add that sequence to sequence list, program will ask for user input about which index should the new   sequence be occupying. This decides on the executing order sequences. Pictures below reveals process of add line sequence to a recipe (commands entered are boxed by   red).

  1. Type in **1** to add sequence command

  .. image:: /images/addrecipe.png


  2.Select a sequence( in this example, select line sequence)

  .. image:: /images/selectsequence.png


  3. Modify line sequence parameter and type in command **add**

  .. image:: /images/addsequence.png


  4. Select the index to be occupied by new sequence

  .. image:: /images/selectindex.png

**Edit Sequence**
  To edit a sequence that is already in sequence list, type 2 in terminal under Modify/Save Active Recipe menu. The terminal will ask for user input of sequence code   (in the form of S#). Select the sequence wanted to be modified and the matching sequence menu will be brought up. Edit parameters and type in q to quit the sequence   menu. The editing process of sequence is complete. Following pictures shows a process of editing line sequence (commands entered are boxed by red).

  1.Select Edit Sequence

  .. image:: /images/editsequence.png


  2.Modify parameters

  .. image:: /images/modifyparameter.png


  3.Quit the sequence menu

  .. image:: /images/quitsequence.png

**Remove Sequence**
  To remove a sequence in sequence list, type **3**, **Remove sequence**, in terminal under **Modify/Save Active Recipe** menu and then type in the index of sequence   that needs to be removed. The following picture shows the removal of line sequence (commands entered are boxed by red).

  .. image:: /images/remove.png

**Recorder Sequence**
  To change the order of sequence in recipe, type **4**, **Recorder Sequence**, in terminal under **Modify/Save Active Recipe** menu and type the index of sequence   that need to be changed and then typed the index that sequence is going to occupy. A single re-order process is complete. This re-order procedure will be continued until user type **q** to quit the re-order sequence function. The following picture shows the change order process (commands entered are boxed by red).

  .. image:: /images/recorder.png

**Save Modifications**
  After finishing editing recipe, users must save the modified sequence list to yaml file in recipe folder. Otherwise, if the program is closed or reset, changes made will not no longer exist. To save a recipe, type **save** in terminal under **Modified/Save Active** menu. (Note, after adding a sequence and quit the Sequence Menu, program will not return to **Modified/Save Active** menu, please remember to return to **Main Menu**, and go to **Recipe Menu**, and go to **Modified/Save Active** Recipe menu in order to do save command)

**Quit Modify/Save Active Recipe Menu**
  To exit out of the Hardware Menu, type **q** in the command and you will be in the **Recipe Menu**.

Browse/Load Stored Recipes 
##########################

Type command **1** in the **Recipe Menu** will allow program to search through polychemprint3/recipe folder and display names, creation dates and descriptions of recipes stored locally. 

.. image:: /images/recipebrowse.png

By entering a recipe code(1,2,3,4,etc.), users can choose to activate a recipe in the program. The current active recipe name will also be shown in recipe menu (boxed in yellow). 

View Recipe Details
###################

To view information on activated recipe, type **view** under **Recipe Menu** and terminal will deliver information of name, description, and also the contents of  the active recipe.

Execute Recipe Menu
###################
To execute a recipe, first type **Prime** in terminal under **Recipe Menu** to convert active recipe into python code. Then type in **GO** to begin recipe execution. Before the recipe begins, it will prompt for a log file name to deposit full recipe details into. Logs are saved as text files in the polychemprint3/Logs folder.
