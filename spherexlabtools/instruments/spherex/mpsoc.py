""" This module implements the class, :class:`.MPSOC` which represents the Xilinx MPSOC devices configured for general
lab use.
"""

import logging
from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set


class MPSOC(Instrument):

    pwm_on_time = Instrument.setting(
        'UU000000000D%010i', """ Sets the pwm on time for a single pwm channel. """
    )
    pwm_period = Instrument.setting(
        'UU000000000P%010i', """ Set the pwm period for a single pwm channel. """
    )
    pwm_status = Instrument.setting(
        'UU000000000S%010i', """ Sets the On/Off status for a single pwm channel """,
        validator=strict_discrete_set, values=[0, 1]
    )

    def __init__(self, adapter, **kwargs):
        super().__init__(adapter, 'Lab configured MPSOC', **kwargs)
