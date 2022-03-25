#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2022 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging

from time import sleep, time

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class LakeShore218(Instrument):

    temperature_all = Instrument.measurement(
        "KRDG? 0", """ Query the temperature of all sensors. """
    )

    temperature1 = Instrument.measurement(
        "KRDG? 1", """ Query the temperature of the channel 1 sensor. """
    )

    temperature2 = Instrument.measurement(
        "KRDG? 2", """ Query the temperature of the channel 2 sensor. """
    )

    temperature3 = Instrument.measurement(
        "KRDG? 3", """ Query the temperature of the channel 3 sensor. """
    )

    temperature4 = Instrument.measurement(
        "KRDG? 4", """ Query the temperature of the channel 4 sensor. """
    )
    temperature5 = Instrument.measurement(
        "KRDG? 5", """ Query the temperature of the channel 5 sensor. """
    )
    temperature6 = Instrument.measurement(
        "KRDG? 6", """ Query the temperature of the channel 6 sensor. """
    )
    temperature7 = Instrument.measurement(
        "KRDG? 7", """ Query the temperature of the channel 7 sensor. """
    )

    temperature8 = Instrument.measurement(
        "KRDG? 8", """ Query the temperature of the channel 8 sensor. """
    )

    status = Instrument.measurement(
        "QSTB?", """ Query the status byte. """
    )

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter,
            "Lake Shore 218 Temperature Controller",
            **kwargs
        )

