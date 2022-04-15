"""
The thermal surrogate control software configuration is imported with the following code::

        from spherexlabtools.applications import thermal_surrogate as ts

This configuration specifies the following components:

.. automodule:: spherexlabtools.applications.thermal_surrogate.hw
    :members:

.. automodule:: spherexlabtools.applications.thermal_surrogate.measure
    :members:

.. automodule:: spherexlabtools.applications.thermal_surrogate.control
    :members:
"""

from .hw import INSTRUMENT_SUITE
from .control import CONTROLLERS
from .measure import VIEWERS, PROCEDURES, RECORDERS
from . import procedures


