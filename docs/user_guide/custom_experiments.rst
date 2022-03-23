###################
Custom Experiments
###################

Where SPHERExLabTools shines is in the ease and flexibility with which complex data-acquisition schemes
can be specified. Each of the core components (:ref:`Instruments <instrument-drivers>`, :ref:`controllers`,
:ref:`procedures`, :ref:`viewers`, and :ref:`recorders`) can be configured independently through the use of
configuration files. This section describes how a custom experiment package should be structured, as well as
the form that the configuration files for each component should take. Before continuing, it is a good idea to
familiarize oneself with the concept of a `Python Package`_. DESCRIBE PYTHON PACKAGES AND MODULE NAMESPACES A BIT HERE, AS WELL AS HOW THE EXPERIMENT CLASS
LOOKS FOR CONFIGURATION LISTS. Also, the MOCK EXPERIMENT TUTORIAL provides a start to finish example of creating a custom
experiment. To effectively learn how to use SPHERExLabTools, one should start with this tutorial, then use this section
as a quick reference after its completion.


Procedure Configuration
========================

To specify the procedures used to control the execution of a measurement, a list of :ref:`user_guide/custom_experiments:Procedure Configuration Dictionaries`
should be built and assigned to a variable called **PROCEDURES**. As described above, when the following code is executed::

    import spherexlabtools as slt
    import custom_experiment_package as cexp
    exp = slt.create_experiment(cexp)

The `create_experiment` function will look for the **PROCEDURES** variable in the experiment package namespace. Then,
a :ref:`Procedure object <api/procedures/procedures:Base Procedure>` is created for each configuration dictionary found
in this list.

Procedure Configuration Dictionaries
-------------------------------------
The form of a procedure configuration dictionary is as follows::

    proc_dict = {
        "instance_name": <string to name the instantiated procedure.>,
        "type": <string name of the procedure class.>,
        "hw": <string or list of strings of instance_name fields of the instruments used in the procedure>,
        "records": <dictionary with names of data objects as keys, and a map to the instance_name fields of the viewers
                    and recorders that this object will be sent to.>,
        "params": <`Optional` dictionary with an initial set of procedure parameters to set.>,
        "kwargs": <`Optional` dictionary with key-word arguments sent to the procedure initialization method.>
    }

The whole procedure configuration used in the :ref:`Collimator Focus Core Experiment <user_guide/core_experiments:Collimator Focus>`
is shown below::

    CameraView_Proc = {
        "instance_name": "CamViewProc",
        "type": "CamViewProc",
        "hw": "Microscope",
        "records": {
            "cam_latest_frame": {"viewer": "CamView"},
        },
        "params": {
            "frames_per_image": 100
        }
    }

    CollimatorFocus_Proc = {
        "instance_name": "CollimatorFocusProc",
        "type": "CollimatorFocusProc",
        "hw": "Microscope",
        "records": {
            "frame": {"viewer": "CamView"},
            "frame_avg": {"viewer": "CamViewAvg"},
            "image": {"recorder": "CollimatorFocusRecorder"},
            "sequence": {"recorder": "CollimatorFocusRecorder"}
        }
    }

    PROCEDURES = [CameraView_Proc, CollimatorFocus_Proc]



Controller Configuration
=========================
Controllers come in two flavors:

    - :ref:`Instrument Controllers <user_guide/custom_experiments:Instrument Controller Configuration Dictionaries>` are
      used for manual control over individual instruments.

    - :ref:`Procedure Controllers <user_guide/custom_experiments:Procedure Controller Configuration Dictionaries>` are
      used to set procedure parameters and execute individual procedures or sequences of several procedures.

Instrument Controller Configuration Dictionaries
-------------------------------------------------

Procedure Controller Configuration Dictionaries
-------------------------------------------------

The form of procedure controller config dictionaries is quite simple::

    proc_cntrl_dict = {
        "instance_name": <string name of the controller instance.>,
        "type": <string name of the controller class to instantiate.>
        "procedure": <instance_name field of the procedure to control.>,
        "params": <optional dictionary with a set of initial parameters. **NOTE**, while this field can be set just
                   as with the other components, it is not recommended to use this field for procedure controllers.>
        "kwargs": <optional dictionary of key-word arguments to send to the initialization method.>
    }

Valid key-word arguments that can be used in the optional `kwargs` field above are as follows:

    - sequencer: Boolean to indicate if a procedure sequencer interface should be generated. The default value is True.
    - records: Boolean to indicate if a record interaction interface should be generated. The default value is True.
    - place_params: Boolean to indicate if the default procedure controller layout should be set on initialization.
                    The default value is True.
    - connect: Boolean to indicate if the start and stop procedure buttons should be connected to the default methods.

The controller configuration used in the :ref:`Collimator Focus Core Experiment <user_guide/core_experiments:Collimator Focus>`
is shown below::

    MScope_Controller = {
        "instance_name": "MicroscopeCntrl",
        "type": "InstrumentController",
        "hw": "Microscope",
        "control_parameters": [
            {"name": "focuser_step_position", "type": "int"},
            {"name": "focuser_absolute_position", "type": "float"},
            {"name": "cam_gain_auto", "type": "list", "values": ["Off", "Once", "Continuous"]},
            {"name": "cam_gain", "type": "float"}
        ],
        "status_parameters": [
            {"name": "focuser_step_position", "type": "int"},
            {"name": "gauge_position", "type": "float"},
            {"name": "focuser_absolute_position", "type": "float"},
            {"name": "cam_gain", "type": "float"}
        ],
        "status_refresh": 2,
        "actions": [
            "focuser_stop", "focuser_reset_position"
        ]
    }

    Gimbal0_Controller = {
        "instance_name": "Gimbal0Cntrl",
        "type": "InstrumentController",
        "hw": "Gimbal0",
        "control_parameters": [
            {"name": "az_absolute_position", "type": "float"},
            {"name": "za_absolute_position", "type": "float"},
        ],
        "status_parameters": [
            {"name": "az_absolute_position", "type": "float"},
            {"name": "za_absolute_position", "type": "float"},
        ],
        "status_refresh": 2,
        "actions": [
            "az_stop", "za_stop", "az_home", "za_home", "az_reset_position", "za_reset_position"
        ]
    }

    LogProc_Controller = {
        "instance_name": "CamViewProcCntrl",
        "type": "LogProcController",
        "procedure": "CamViewProc",
    }

    CollimatorFocus_Controller = {
        "instance_name": "CollimatorFocusProcCntrl",
        "type": "ProcedureController",
        "procedure": "CollimatorFocusProc"
    }

    CONTROLLERS = [MScope_Controller, Gimbal0_Controller, LogProc_Controller, CollimatorFocus_Controller]


.. _`Python Package`: https://docs.python.org/3/tutorial/modules.html#packages

