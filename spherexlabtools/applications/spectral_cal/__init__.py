"""
.. automodule:: spherexlabtools.applications.spectral_cal.hw
    :members:

To initialize the spectral calibration software, run the following code on the control computer:

    import spherexlabtools as slt
    from spherexlabtools.applications import spectral_cal as sc

    exp = slt.create_experiment(sc)

The variable **exp** now contains the :ref:`user_guide/fundamentals:Instrument Drivers`,
:ref:`user_guide/fundamentals:Procedures`, :ref:`user_guide/fundamentals:Controllers`,
:ref:`user_guide/fundamentals:Viewers`, and :ref:`user_guide/fundamentals:Recorders` described below. As an example
of starting a controller, the following code will start the manual monochromator control gui::

    exp.start_controller("MonoCntrl")

.. automodule:: spherexlabtools.applications.spectral_cal.measure
    :members:

.. automodule:: spherexlabtools.applications.spectral_cal.control
    :members:

"""

from .hw import INSTRUMENT_SUITE
from .control import CONTROLLERS
from .measure import VIEWERS, PROCEDURES, RECORDERS
from . import procedures


