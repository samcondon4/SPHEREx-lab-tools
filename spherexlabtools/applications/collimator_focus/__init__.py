# import experiment configuration names ############
from .measure import RECORDERS, VIEWERS, PROCEDURES
from .hw import INSTRUMENT_SUITE
from .control import CONTROLLERS

# custom procedures #
from . import procedures


# TODO: figure out motor addressing for gimbal
# TODO: Turn off viewer auto-scale, Mono-8 and Mono-16 Camera settings, live streaming + moving average in viewer,
# TODO: save contents of any viewer, absolute position conversion

