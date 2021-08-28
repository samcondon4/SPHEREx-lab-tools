"""pylabsm_spectral:

    This module implements the spectral calibration specific state machine.

"""

import asyncio
from pylabinst.CS260 import CS260
from pylabinst.labjacku6 import Labjack
from pylabinst.ndfwheel import NDF
from pylabinst.SR830 import SR830
from transitions.extensions.asyncio import AsyncMachine
from pylabsm.pylabsm_states.pylabsm_statesimport import pylabsm_state_initializing, pylabsm_state_waiting, \
                                                        pylabsm_state_manual, pylabsm_basestate, pylabsm_state_auto


class SpectralCalibrationMachine(AsyncMachine):

    def __init__(self, data_queue_tx=None, data_queue_rx=None):
        # Instantiate AsyncMachine base class #
        super().__init__(model=self)

        # Action argument attributes #######
        self.data_queue_tx = data_queue_tx
        self.data_queue_rx = data_queue_rx
        self.manual_or_auto = None

        # Instrument classes ##############
        self.inst_dict = {"Cs260": CS260(), "Labjack": Labjack(), "NDF": NDF(), "Sr830": SR830()}

        # Initialize action arguments ######################################################
        pylabsm_basestate.SmCustomState.set_global_args({"Tx Queue": self.data_queue_tx,
                                                         "Rx Queue": self.data_queue_rx})
        pylabsm_basestate.SmCustomState.set_global_args({"Manual or Auto": property(self.get_manual_or_auto,
                                                                                    self.set_manual_or_auto)})
        pylabsm_basestate.SmCustomState.set_global_args(self.inst_dict)

        # Configure states and state actions #########################################
        self.init_state = pylabsm_state_initializing.Initializing(self)
        self.init_state.add_action(self.init_state.initialize_instruments, args=list(self.inst_dict.keys()))
        ##############################################################################

        # Add states to the state machine #
        self.add_states(self.init_state)

    def set_manual_or_auto(self, set_str):
        self.manual_or_auto = set_str

    def get_manual_or_auto(self):
        return self.manual_or_auto

    async def run(self):
        if self.data_queue is None:
            self.data_queue = asyncio.Queue()
            pylabsm_basestate.SmCustomState.set_global_args({"Global Queue": self.data_queue})
        await self.start_machine()


if __name__ == "__main__":
    sm = SpectralCalibrationMachine()
    asyncio.run(sm.run())
