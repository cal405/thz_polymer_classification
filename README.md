# thz_polymer_classification

CONTENTS OF THIS FILE
---------------------
 * Introduction
 * Requirements
 * Installation
 * Configuration
 * Maintainers

INTRODUCTION
------------
This repository contains all the information used on the THz Polymer
Classification experiment as shown in the PDF documentation (in german). See
the documentation for a full explanation of the measurements, calculations and
modelling used.

The goal of this repository is to enable anyone to reproduce the results
obtained previously. The repository contains the following:

 * All of the raw data from the THz-TDS measurements.

 * All of the processed data used in the ML model training.

* The python code needed to extract the relevant features.

* The feature files for the training and test set.

* The MATLAB live script to train the SVMs for classification.


REQUIREMENTS
------------
Python 3.9.12 or later is required to run the .py files.

The following python modules are required to run the getData.py and
the functionalit.py files:

 * [numpy](https://numpy.org/) v. 1.23 or later
 * [pandas](https://pandas.pydata.org/) v. 1.5.1 or later
 * [natsort](https://pypi.org/project/natsort/) v. 8.2 or later
 * [matplotlib](https://matplotlib.org/) v. 3.6 or later
 * [scipy](https://scipy.org/) v. 1.9.3 or later

The refractive index and absorption extraction algorithm
are owned by [Elena Mavrona](https://scholar.google.com/citations?user=566uGpQAAAAJ&hl=en&oi=ao).

MATLAB 2020b or later is required to run the live script. 


INSTALLATION
------------
To install MATLAB visit: https://ch.mathworks.com/

Python can be found at: https://www.python.org/


CONFIGURATION
-------------

    1. To configure the MATLAB live script open it in the GUI.
    
    2. Specify the relative path to the feature file for the training
    and test set.
    
    3. Change parameters for the SVM template on the function to create
    and run the model.



MAINTAINERS
-----------

 * Nicklaus Cáceres - luis.caceres@empa.ch
 * Sofie Gnannt - sofie.gnannt@empa.ch

Supporting organization:

 * Empa - https://www.empa.ch/
