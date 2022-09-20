Step-by-Step Experiment Configuration
######################################

| This section utilizes the pymeasure SwissArmyFake class to work through each step of configuring SPHERExLabTools for
  a given experiment. The SwissArmyFake class generates mock data as if it were a real instrument, but does not require
  a connection to any real hardware.

| The dummy experiment is the monitoring of a "cryostat baseplate temperature" in response to some "voltage applied to a heater".
  Additionally, the thermal emission of the "heater" is monitored via an "IR camera". This tutorial walks through the steps required
  to configure the instruments in this experiment, write measurement scripts, view live temperature and camera data, and write
  data to output files for later analysis.

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
     - instruments/
     - procedures/
     -  __init__.py
     -  control.py
     -  hw.py
     -  measure.py

| Where the configuration dictionaries are defined for instruments in hw.py, for controllers in control.py, and viewers, recorders, and procedures
  in measure.py. The __init__.py file then defines the config variables as lists of the dictionaries defined in the other .py files. The instruments/
  and procedures/ directories are used for custom user procedure scripts and instrument drivers.

| Begin by cloning this configuration file structure with the following git command:

.. code-block:: bash

    git clone https://github.com/samcondon4/PyLabTools-Template.git

| We are now ready to populate the hw, control, and measure configuration files! In the following steps, do not worry too much about the
  contents of the configuration dictionaries that we define. The purpose of this tutorial is to get a big picture sense of how SPHERExLabTools
  is configured, not to understand all of the details of configuration dictionary syntax. These syntax details can be found at:
  :ref:`Configuration Dictionaries <user_guide/configuration:Configuration Dictionaries>`

1) Defining instruments
------------------------

| First, let's populate the hw.py file with the "instruments" in use. For this experiment, we are making use of a "temperature controller"
  with a single heater output and temperature input channel. We also are using an "IR camera".

| Add the following block to your hw.py file, which will configure each of these pieces of hardware:

.. code-block:: python

    TempController = {
        "instance_name": "temp_controller",
        "manufacturer": "custom_fakes",
        "instrument": "TemperatureController",
        "resource_name": 0.1,
    }


    Camera = {
        "instance_name": "camera",
        "manufacturer": "custom_fakes",
        "instrument": "Camera",
        "resource_name": 0.3
    }

| We have now defined a few hardware configuration dictionaries, but SPHERExLabTools will not be able to see that these exist if we do not add them to the
  **INSTRUMENT_SUITE** list. Back in the __init__.py file, add each dictionary to the **INSTRUMENT_SUITE** variable:

.. code-block:: python

    INSTRUMENT_SUITE = [hw.TempController, hw.Camera]


2) First instrument controller
-------------------------------

| Now, we can add a few controller configuration dictionaries to allow us to control the parameters of our newly added instruments with the SPHERExLabTools
  graphical interface!

| Add the following block to control.py:

.. code-block:: python

    CamCntrl = {
        "instance_name": "CameraCntrl",
        "type": "InstrumentController",
        "hw": "camera",
        "control_parameters": [
            {"name": "frame_width", "type": "int", "value": 2448},
            {"name": "frame_height", "type": "int", "value": 2048},
            {"name": "frame_format", "type": "list", "limits": ["mono_8", "mono_16"]},
            {"name": "gain", "type": "float", "value": 0.0}
        ],
        "status_parameters": [
            {"name": "frame_width", "type": "str"},
            {"name": "frame_height", "type": "str"},
            {"name": "frame_format", "type": "list", "limits": ["mono_8", "mono_16"]},
            {"name": "gain", "type": "float", "value": 0.0}
        ],
        "status_refresh": "after_set"
    }

    TCCntrl = {
        "instance_name": "TCCntrl",
        "type": "InstrumentController",
        "hw": "temp_controller",
        "control_parameters": [
            {"name": "heater_output", "type": "float", "value": 0.0}
        ],
        "status_parameters": [
            {"name": "plate_temperature", "type": "float", "value": 40}
        ],
        "status_refresh": 1000
    }

| And update the **CONTROLLERS** list with:

.. code-block:: python

    CONTROLLERS = [control.CamCntrl, control.TCCntrl]

| We can now start the SPHERExLabTools graphical interface. Start a python interactive session and run:

.. code-block:: python

    >>> import spherexlabtools as slt
    >>> import config
    >>> exp = slt.create_experiment(config)
    >>> exp.start()

| The following interface should now appear:

.. figure:: fig/first_controller_interface.png

    SPHERExLabTools interface with first instrument controllers.

| With this interface we can now set basic parameters of our instruments manually. The "Control" drop-down provides a carot drop-down
  for each parameter allowing parameters to be set individually, or all parameters can be set at once with the "Set All Parameters" button.
  The "Status" drop-down displays the current value of each parameter. The "Controller Select" selection allows one to switch between controllers.
  Switching to the "TCCntrl" controller reveals a simple interface for the temperature controller with the baseplate temperature being read and updated
  in the interface every second.

3) Creating a procedure
------------------------

| As discussed in :ref:`Fundamentals <user_guide/fundamentals/index:Fundamentals>`, **Procedures** are classes used to define scripts that run measurements.
  Let's write a procedure to run our basic measurement.

4) Connecting procedure records to viewers and recorders
---------------------------------------------------------

5) Running a measurement
-------------------------


