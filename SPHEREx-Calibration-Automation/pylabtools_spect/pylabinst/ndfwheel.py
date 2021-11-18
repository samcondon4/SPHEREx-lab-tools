"""ndfwheel:

    This module implements a python wrapper for control of the neutral density filter wheel

Sam Condon, 07/02/2021
"""
import asyncio
from pylabinst.pylabinst_instrument_base import Instrument
import clr
import sys
sys.path.append("pylabinst\\NDFWheel_DLLs\\")
sys.path.append(".\\NDFWheel_DLLs\\")
clr.AddReference("OptecHID_FilterWheelAPI")
from OptecHID_FilterWheelAPI import FilterWheels
from OptecHID_FilterWheelAPI import FilterWheel


class NDF(Instrument):

    def __init__(self):
        super().__init__("NDF")

        self.HSFW = None
        self.err_state = None

        # Configure open method ##########################
        self.set_open_method(self.open_com)
        ##################################################

        # Configure parameters ################################
        self.add_get_parameter("position", self.get_position)
        self.add_set_parameter("position", self.set_position)
        self.add_get_parameter("error", self.get_error)
        self.add_set_parameter("error", self.clear_error)
        self.add_set_parameter("home", self.home)
        ########################################################

    def open_com(self):
        self.HSFW = FilterWheels().FilterWheelList[0]
        self.home()
        self.clear_error()
        pass

    def get_position(self):
        return str(self.HSFW.CurrentPosition)

    def set_position(self, position):
        if position == 0:
            self.home()
        else:
            self.HSFW.CurrentPosition = position
        self.get_error()
        if self.err_state != 0:
            raise RuntimeError("Error {} occurred during movement of NDF!".format(self.err_state))

    def get_error(self):
        self.err_state = self.HSFW.ErrorState
        return self.err_state

    def clear_error(self):
        self.HSFW.ClearErrorState()

    def home(self):
        self.HSFW.HomeDevice()
        self.get_error()
        if self.err_state != 0:
            raise RuntimeError("Error {} occurred during homing of NDF!".format(self.err_state))

