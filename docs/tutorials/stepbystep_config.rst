Step-by-Step Experiment Configuration
######################################

| This section utilizes the pymeasure SwissArmyFake class to work through each step of configuring SPHERExLabTools for
  a given experiment. The SwissArmyFake class generates mock data as if it were a real instrument, but does not require
  a connection to any real hardware.

0) Setting up the configuration file structure
-----------------------------------------------

| As discussed in :ref:`Fundamentals <user_guide/fundamentals:Fundamentals>`, SPHERExLabTools reads user defined :ref:`Experiment Control Packages <user_guide/fundamentals:Experiment Control Packages>`
  to configure control software for a given experiment. Experiment control packages define the 5 configuration variables:

    - INSTRUMENT_SUITE: python list of hardware configuration dictionaries.
    - CONTROLLERS: list of controller configuration dictionaries.
    - PROCEDURES: list of procedure configuration dictionaries.
    - VIEWERS: list of viewer configuration dictionaries.
    - RECORDERS: list of recorder configuration dictionaries.

| The file structure of the experiment control package can be in whatever manner the user desires, though the standard structure is as follows:

    config/
     -  __init__.py
     -  hw.py
     -  control.py
     -  measure.py

| Where the configuration dictionaries are defined for instruments in hw.py, for controllers in control.py, and viewers, recorders, and procedures
  in measure.py. The __init__.py file then defines the config variables as lists of the dictionaries defined in the other .py files.

1) Defining instruments
------------------------

| First let's populate the hw.py file with the "instruments" in use.

2) First instrument controller
-------------------------------

3) Creating a procedure
------------------------

4) Connecting procedure records to viewers and recorders
---------------------------------------------------------

5) Running a measurement
-------------------------


