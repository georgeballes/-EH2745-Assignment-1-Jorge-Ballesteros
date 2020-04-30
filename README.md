# -EH2745-Assignment-1-Jorge-Ballesteros
The purpose of Assignment 1 is to combine Python programming, CIM-XML modelling and parsing and finally model building using Pandapower. 

This repository is composed by:
- Assignment1: this is the main file with the code which parse the CIM-XML data, there are several algorithms to retrieve the desired xml data and to create each specific element in pandapower and finally create a plot. Note that when running the main file, the way of showing the plot is creating automatically an html file in the same folder.
- GUI: Here I created an user interface where when you run it gives you the option to introduce 2 files, here you have to introduce Assignment_EQ_reduced.xml and Assignment_SSH_reduced.xml, or if you want to display the extended system, MicroGridTestConfiguration_T1_BE_EQ_V2 and MicroGridTestConfiguration_T1_BE_SSH_V2 and press execute.
- Classes:A internal data structure to describe the model need to be created, to do so I have written classes for each specific component (buses, connectivity nodes, generators terminal, etc).

