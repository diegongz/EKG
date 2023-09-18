To run this interface, you need to install the following packages: PyQt5, pyqtgraph, numpy, pandas, time.

Methods for loading/cutting a signal from an existing interface have been inherited. Several superclass methods require files from this folder to run, but only the mentioned two have been used in this project.

Methods related to R point detection, R-R intervals, and Heart Rate Variability have been created from scratch.

Methods related to my interface start from line 420; everything above that line is the inherited class.

In the "initUI" method, some lines from the inherited class have been retained, as the superclass needs these variables to run.

Buttons/Labels/LineEdit/Layouts needed for the new methods in my interface have been added starting from line 743 of this method.

In the "Signals" folder, there are .txt files to test the program; all these Electrocardiograms have a frequency f=512 Hz (value to enter as frequency).

You can find more information in the written documentation.

For any questions, contact: diego.ngzru@gmail.com
Diego Noguez Ruiz