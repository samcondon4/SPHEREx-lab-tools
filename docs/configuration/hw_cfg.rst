#############################
Hardware Configuration Files
#############################

In a manner similar to Jonathon Hunacek's PyHk_, SpherexLabTools makes use of hardware configuration files in the json5 format to specify the instruments and sensors present in an experiment setup. The hardware configuration for a given experiment is used to create an instance of the :py:class:`spherexlabtools.calibration.focus.InstrumentSuite` object. This object serves as a top level container for all of the instruments in the setup. The format for a hardware configuration file is given below:

.. code:: javascript
        
        [
                {
                        "instance_name": (str),
                        "resource_name": (str), 
                        "manufacturer": (str),
                        "instrument": (str),
                        "kwargs": (dict),
                        "param": (param type)
                },
                ...
        ]

- **instance_name**: String identifying the name of the instrument instance to be created.
- **resource_name**: String identifying the name of the instrument communication channel seen by the computer. See :ref:`resource-name-id` for a quick tutorial on how to find an instrument's resource name. 
- **manufacturer**: String identifying the manufacturer of the instrument. This should match the name of the directory in pymeasure/instruments that the instrument class can be found in. 
- **instrument**: String identifying the instrument class within the pymeasure/instruments/<manufactururer>/ directory specified.
- **kwargs**: Dictionary containing keyword arguments to pass when initializing the instrument class.
              Note that some instrument classes have required initialization arguments. This arguments should be specified in this dictionary.
- **param**: Note that "param" should be substituted with the name of an instrument class property to be initialized with the value given here. As many initial values of instrument class properties as desired can be given here.  


Instruments in SpherexLabTools are implemented as subclasses of the :py:class:`pymeasure.instruments.instrument.Instrument` baseclass. As much as possible, SpherexLabTools instrument classes are developed and contributed to the `official pymeasure project`_.  Where our instrument classes fall out of scope for the official **pymeasure** project, we have created our own fork_ to implement these classes. The **spherex_test_cal** branch on the fork is used extensively within SpherexLabTools. 


.. _PyHk: http://docs.pyhk.net/en/beta/
.. _fork: https://github.com/samcondon4/pymeasure
.. _pyvisa: https://pyvisa.readthedocs.io/en/latest/
.. _`official pymeasure project`: https://pymeasure.readthedocs.io/en/latest/

