"""pylabsm_spectral:

    This module implements the spectral calibration specific state machine.

"""

import asyncio
from transitions.extensions.asyncio import AsyncMachine
# instrument drivers #######################
from pylabinst.CS260 import CS260
from pylabinst.labjacku6 import Labjack
from pylabinst.ndfwheel import NDF
from pymeasure.instruments.srs.sr510 import SR510
from pymeasure.instruments.srs.sr830 import SR830

# measurement procedures #####################################
from pylabsm.pylabsm_procs.sr830proc import Sr830Measurement
from pylabsm.pylabsm_procs.sr510proc import Sr510Measurement

# state classes ####################################################################################################
from pylabsm.pylabsm_states.pylabsm_statesimport import pylabsm_state_initializing, pylabsm_state_waiting, \
    pylabsm_state_manual, pylabsm_basestate, pylabsm_state_auto


class SpectralCalibrationMachine(AsyncMachine):

    def __init__(self, data_queue_tx=None, data_queue_rx=None):
        # Instantiate AsyncMachine base class #
        super().__init__(model=self)

        # Action argument attributes #######
        self.data_queue_tx = data_queue_tx
        self.data_queue_rx = data_queue_rx
        self.manual_or_auto = [""]
        self.control_args = {}

        # Instrument classes ##############
        self.inst_dict = {"CS260": CS260(),}
        """
         "LABJACK": Labjack(), "NDF": NDF(), "SR510": SR510("GPIB0::6::INSTR"),
                          "SR830": SR830("GPIB0::15::INSTR")}"""
        """
        self.inst_dict["SR510"].quick_properties_list = ["phase", "pre_time_constant", "sensitivity",
                                                         "reference_frequency"]
        self.inst_dict["SR830"].quick_properties_list = ["time_constant", "sensitivity"]
        """

        # Procedure classes ################
        self.proc_dict = {"SR830": Sr830Measurement(), "SR510": Sr510Measurement()}

        # Initialize action arguments ######################################################
        pylabsm_basestate.SmCustomState.set_global_args({"Tx Queue": self.data_queue_tx,
                                                         "Rx Queue": self.data_queue_rx})
        pylabsm_basestate.SmCustomState.set_global_args({"Manual or Auto": self.manual_or_auto})
        pylabsm_basestate.SmCustomState.set_global_args({"Instruments": self.inst_dict})
        pylabsm_basestate.SmCustomState.set_global_args({"Procedures": self.proc_dict})
        pylabsm_basestate.SmCustomState.set_global_args({"Control": self.control_args})

        # Configure states and state actions ###########################################################################
        self.init_state = pylabsm_state_initializing.Initializing(self, initial=True)
        self.init_state.add_action(self.init_state.initialize_instruments, args=["Tx Queue", "Instruments"])

        self.wait_state = pylabsm_state_waiting.Waiting(self)
        self.wait_state.add_action(self.wait_state.waiting_action, args=["Rx Queue", "Manual or Auto", "Control"])

        self.manual_state = pylabsm_state_manual.Manual(self)
        self.manual_state.add_action(self.manual_state.manual_action, args=["Control", "Tx Queue", "Instruments",
                                                                            "Procedures"])

        self.auto_state = pylabsm_state_auto.Auto(self)
        self.auto_state.add_action(self.auto_state.auto_sm_exec, args=["Control", "Tx Queue", "Instruments",
                                                                       "Procedures"])
        ################################################################################################################

        # Add states and transitions to the state machine #
        self.add_states([self.init_state, self.wait_state, self.manual_state, self.auto_state])
        self.init_state.add_transition(self.wait_state)
        self.wait_state.add_transition(self.manual_state, arg="Manual or Auto", arg_result=["manual"])
        self.wait_state.add_transition(self.auto_state, arg="Manual or Auto", arg_result=["auto"])
        self.manual_state.add_transition(self.wait_state)
        self.auto_state.add_transition(self.wait_state)

    async def run(self):
        if self.data_queue is None:
            self.data_queue = asyncio.Queue()
            pylabsm_basestate.SmCustomState.set_global_args({"Global Queue": self.data_queue})
        await self.start_machine()


if __name__ == "__main__":
    sm = SpectralCalibrationMachine()
    asyncio.run(sm.run())
