Core Experiments
=================

SPHERExLabTools ships with the following preconfigured experiments:

.. toctree::
        :maxdepth: 1

        core_exp_docs/spectral_cal
        core_exp_docs/thermal_surrogate

To run the control software associated with each of these experiments, perform the following steps:

    1. Open the **Anaconda Prompt** application (on windows type anaconda prompt in the search bar)
    2. Activate the **spherexlabtools** Anaconda environment::

        conda activate spherexlabtools

    3. Navigate to the directory where you would like all output data files to be saved.
    4. Start a python interpreter by typing **python** into the terminal.
    5. Import the **spherexlabtools** package::

        import spherexlabtools as slt

    6. Import the desired core experiment configuration package::

        from spherexlabtools.applications import <name of core experiment> as <core_exp_alias>

       The specific form of this line varies depending on which core experiment is being used. See the documentation
       specific to each core experiment provided at the links above.
    7. Create the :ref:`Experiment Object <user_guide/fundamentals:Experiment Class>` with the core experiment
       configuration::

        exp = slt.create_experiment(<core_exp_alias>)

The variable **exp** now contains all of the :ref:`user_guide/fundamentals:Instrument Drivers`,
:ref:`user_guide/fundamentals:Procedures`, :ref:`user_guide/fundamentals:Controllers`, :ref:`user_guide/fundamentals:Viewers`,
and :ref:`user_guide/fundamentals:Recorders` that are specified by the core experiment configuration package. To start each
of these components use::

    exp.start_controller("NameOfController")
    exp.start_viewer("NameOfViewer")
    exp.start_recorder("NameOfRecorder")

To stop each of these components use::

    exp.stop_controller("NameOfController")
    exp.stop_viewer("NameOfViewer")
    exp.stop_recorder("NameOfRecorder")

Refer to the documentation specific to each core experiment provided at the links above to see the list of controller,
viewer, and recorder names, as well as the function of each component.

