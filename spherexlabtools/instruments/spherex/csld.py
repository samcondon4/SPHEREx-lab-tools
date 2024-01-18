""" This module implements the class, :class:`.CSLD` which represents the cold shutter/led controller used to control
    the cold shutter and led/bolometer sources inside of the SPHEREx small test cryostats.

v0.1: Sam Condon, 2022-05-23
"""

import logging
from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set


class CSLD(Instrument):
    """ Represents the warm electronics controller for the cold-shutter and led/bolometer sources inside
    of the SPHEREx small test cryostats.
    """

    led_channel = Instrument.setting(
        "UU011%i", """ Sets the state of the (single) CSLD led channel. """,
        validator=strict_discrete_set, values=[0, 1]
    )

    def __init__(self, adapter, **kwargs):
        super().__init__(adapter, "Cold Shutter Led Controller", **kwargs)

    def set_shutter_state(self, state):
        """ This function is used to send the shutter close/open command to CSLD.

        :param state: Integer 0 or 1 where 1 is to open the shutter, 0 is to close the shutter.
        """
        strict_discrete_set(state, [0, 1])
        self.write(f"UU001{state}")
