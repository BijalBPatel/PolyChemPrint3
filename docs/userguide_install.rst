Installation and Setup
======================

Requirements/Supported OS
#########################

PCP3 is designed to run on Windows and Linux distributions with Python 3 on even very low spec hardware. At the end of the day, for just sending commands between hardware, there really isn't much you need in terms of specialized system specs. Just serial ports that can be connected to your desired hardware.

In our lab, we have run PCP3 on Debian 9/ Mint 19 Linux PCs and on Windows 10 using Ananconda as the python environment.

Installing Anaconda (optional)
##############################

To use polychemprint3, you need to have a python 3 environment set up. If you are on Linux, your distribution most likely has python 3 installed out of the box. If not, a simple way to set things up is to use Anaconda_, a free and open source python distribution comonly used in data science. 

.. _Anaconda: https://www.anaconda.com/products/individual.
   

After successfully installing Anaconda, open Anaconda Navigator and launch anaconda prompt. Boxed in red below:

.. image:: /images/AnacondaBoxRed.png

Installation PCP3 from PyPi via pip
###################################

After opening the appropriate terminal window (Anaconda Prompt/Terminal/Command Prompt), enter:

.. code-block:: none

	pip install --no-cache-dir --pre --upgrade polychemprint3

Press enter and polychemprint3 should install with any required dependencies automatically.

To run the program, just type 

.. code-block:: none

	polychemprint3

into the terminal window and the program should launch

.. image:: /images/Polychemprint.png


Run from Source (from Github)
#############################

TODO


Setting up new Hardware
#######################

TODO
