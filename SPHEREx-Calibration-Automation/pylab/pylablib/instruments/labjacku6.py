"""labjacku6.py:

    This module implements a wrapper around the Labjack provided U6 driver to fit into
    the SPHEREx Test/Calibration Automation Software Suite

Sam Condon, 07/05/2021
"""

import u6
import numpy as np
from pylablib.instruments.pylablib_instrument import Instrument


class Labjack(Instrument):

    def __init__(self):
        super().__init__("Labjack")

        # Configure open method ###########################
        self.set_open_method(self.open_u6_com)
        self.com = None
        ###################################################

        # Configure parameters #############################
        self.add_parameter("dio", self.get_dio, self.set_dio)
        ####################################################

    def open_u6_com(self):
        self.com = u6.U6()
        self.com.getCalibrationData()

    def get_dio(self, dios="All"):
        """get_dio:
            Return the current digital io port statuses

        :param: dios: int or list of ints specifying which dio pin status to return.
        :return: dictionary with keys corresponding to dio numbers and values corresponding to dio state.
        """
        dio_dict = {}
        ret = False
        if type(dios) is int:
            dio_dict[dios] = self.com.getDIOState(dios)
            ret = True
        elif type(dios) is list:
            for d in dios:
                dio_dict[d] = self.com.getDIOState(d)
                ret = True
        elif dios == "All":
            for d in np.arange(23):
                dio_dict[d] = self.com.getDIOState(int(d))
                ret = True

        if ret:
            return dio_dict
        else:
            return False

    def set_dio(self, dio_dict):
        """set_dio:
            Set the digital io ports on labjack to state specified in dio_dict

        :param: dio_dict: <dictionary> keys are dio pin numbers, values are desired dio states (0 or 1).
        """
        for d in dio_dict:
            if dio_dict[d] == 0 or dio_dict[d] == 1:
                self.com.setDOState(d, state=dio_dict[d])
            else:
                raise RuntimeError("Only 0 or 1 allowed as a DIO state on the LJU6!")

