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

        # Configure parameters ####################################################
        self.add_get_parameter("dio", self.get_dio)
        self.add_parameter("dio config", self.get_dio_config, self.set_dio_config)
        self.add_parameter("dio state", self.get_dio_state, self.set_dio_state)
        ###########################################################################

    def open_u6_com(self):
        self.com = u6.U6()
        self.com.getCalibrationData()

    def get_dio(self, dios="All"):
        """get_dio:
            Get the dio configuration and state of the pins specified.

        :param: dios: int or list of ints specifying which dio pin configurations and states to return.
        :return: dictionary with keys corresponding to dio numbers and values corresponding to dictionaries with dio
                 states and configurations.
        """
        dio_dict = {}
        dio_config = self.get_dio_config(dios)
        dio_state = self.get_dio_state(dios)
        for d in dio_config:
            dio_dict[d] = {"Config": dio_config[d], "State": dio_state[d]}
        return dio_dict

    def get_dio_config(self, dios="All"):
        """get_dio_config:
            Get the i/o configuration of the dio pins specified

        :param: dios: int or list of ints specifying which dio pin configurations to return.
        :return: dictionary with keys corresponding to dio numbers and values corresponding to dio configurations.
        """
        dio_dict = {}
        ret = False
        if type(dios) is int:
            dio_dict[dios] = self.com.getFeedback(u6.BitDirRead(dios))[0]
            ret = True
        elif type(dios) is list:
            for d in dios:
                dio_dict[d] = self.com.getFeedback(u6.BitDirRead(d))[0]
            ret = True
        elif dios == "All":
            for d in np.arange(23):
                dio_dict[d] = self.com.getFeedback(u6.BitDirRead(int(d)))[0]
            ret = True

        if ret:
            for d in dio_dict:
                if dio_dict[d] == 0:
                    dio_dict[d] = "Input"
                else:
                    dio_dict[d] = "Output"
            return dio_dict
        else:
            return False

    def set_dio_config(self, dios_cfg_dict):
        """set_dio_config:
            Set the i/o configuration of the dio pins specified in dios_cfg_dict

        :param: dios_cfg_dict: dictionary with dio pin numbers as keys and dio pin configurations
                               as values.
        :return: None
        """
        for dio in dios_cfg_dict:
            write = False
            if dios_cfg_dict[dio] == "Output":
                write = 1
            elif dios_cfg_dict[dio] == "Input":
                write = 0
            if write is not False:
                self.com.getFeedback(u6.BitDirWrite(dio, write))

    def get_dio_state(self, dios="All"):
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

    def set_dio_state(self, dio_dict):
        """set_dio:
            Set the digital io ports on labjack to state specified in dio_dict. This command is only valid when the
            specified dio port(s) have been configured as outputs.

        :param: dio_dict: <dictionary> keys are dio pin numbers, values are desired dio states (0 or 1).
        """
        for d in dio_dict:
            dir = self.com.getFeedback(u6.BitDirRead(d))[0]
            if dir != 1:
                raise RuntimeError("DIO{} is configured as an input!".format(d))
            if dio_dict[d] == 0 or dio_dict[d] == 1:
                self.com.setDOState(d, state=dio_dict[d])
            else:
                raise RuntimeError("Only 0 or 1 allowed as a DIO state on the LJU6!")

