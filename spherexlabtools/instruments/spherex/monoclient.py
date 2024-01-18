""" This module implements the client side of the monochromator control server in the class
    :class:`.MonoControlClient`

"""
import time
from ._mono_server import MonoControlServer
from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set


class MonoControlClient(Instrument):
    """ Client side of the monochromator control server.
    """

    HOST = MonoControlServer.HOST
    PORT = MonoControlServer.PORT

    _cmd_query_map = {
        "SHUTTER": "shutter",
        "UNITS": "units",
        "GRAT": "grating",
        "FILTER": "osf",
        "GOWAVE": "wavelength",
    }

    shutter = Instrument.control("SHUTTER?", "SHUTTER %s", """String property representing the current
    shutter setting. This property can be set.""",
                                 validator=strict_discrete_set,
                                 values=[0, 1])

    units = Instrument.control("UNITS?", "UNITS %s", """String property representing the current units of the
    wavelength setting. This property can be set with "NM" for nanometers and "UM" for microns.""",
                               validator=strict_discrete_set,
                               values=["NM", "UM"])

    grating = Instrument.control("GRAT?", "GRAT %s", """Integer property representing
    the current grating setting. This property can be set.""",
                                 validator=strict_discrete_set,
                                 values=[1, 2, 3, "Auto"])

    osf = Instrument.control("FILTER?", "FILTER %s", """Integer property representing the current
    order sort filter setting. This property can be set.""",
                             validator=strict_discrete_set,
                             values=[1, 2, 3, 4, 5, 6, "Auto"])

    wavelength = Instrument.control("WAVE?", "GOWAVE %s", """Float property representing
    the current wavelength setting in um. or nm. This property can be set.""")

    def __init__(self, resourceName, set_poll_interval=1, **kwargs):
        """ Initialize connection to :class:`.MonoControlServer`.

        :param resourceName: TCPIP socket resource name with syntax 'TCPIP::host::port:SOCKET'
        :param set_poll_interval: Number of seconds to wait between completion queries to the server after a
                                  set command is sent.
        """

        super().__init__(
            resourceName,
            "Monochromator Control Client",
            includeSCPI=False,
            write_termination="\r\n",
            read_termination="\r\n",
            **kwargs
        )

        self.set_poll_interval = set_poll_interval
        del self.adapter.connection.timeout

    def write(self, cmd):
        """ Override base write method to poll for completion after sending a set command.

        :param cmd: Command to send to instrument.
        """
        super().write(cmd)
        # if it is not a query, then pend for the attribute setting to complete. #
        if "?" not in cmd:
            self.read()

    def wait_for_completion(self):
        """ Query server for the completion of the attribute setting.
        """
        complete = False
        while not complete:
            self.read()
