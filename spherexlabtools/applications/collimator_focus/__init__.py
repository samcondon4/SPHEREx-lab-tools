"""
This application implements control over the collimator microscope and the first gimbal mount in the
focus calibration setup. Controllers are configured for each of these pieces of hardware. Procedures
are configured to retrieve and display live images from the microscope camera and to run an automated
collimator focus curve measurement. Focus curve data is written out to an HDF5 file.

"""

# import experiment configuration names ############
from .measure import RECORDERS, VIEWERS, PROCEDURES
from .hw import INSTRUMENT_SUITE
from .control import CONTROLLERS

# custom procedures #
from . import procedures


# TODO: Mono-8 and Mono-16 Camera settings, Image viewer levels based on camera settings

