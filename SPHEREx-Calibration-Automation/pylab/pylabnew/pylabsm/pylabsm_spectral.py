"""pylabsm_spectral:

    This module implements the spectral calibration specific state machine.

"""

import asyncio
from transitions.extensions.asyncio import AsyncMachine
from pylabsm.pylabsm_states.pylabsm_statesimport import pylabsm_state_initializing, pylabsm_state_waiting, \
                                                        pylabsm_state_manual, pylabsm_basestate


class SpectralCalibrationMachine(AsyncMachine):

    def __init__(self, data_queue=None):
        # Instantiate AsyncMachine base class #
        super().__init__(model=self)

        # Action argument attributes #######
        self.data_queue = data_queue
        self.manual_or_auto = None

        # Initialize action arguments ######################################################
        pylabsm_basestate.SmCustomState.set_global_args({"Global Queue": self.data_queue})
        pylabsm_basestate.SmCustomState.set_global_args({"Manual or Auto": property(self.get_manual_or_auto,
                                                                                    self.set_manual_or_auto)})

        # Configure states and state actions #########################################
        self.init_state = pylabsm_state_initializing.Initializing(self)
        self.init_state.add_action(self.init_state.initialize_instruments)

        self.wait_state = pylabsm_state_waiting.Waiting(self)
        self.wait_state.add_action(self.wait_state.waiting_action, args="All")

        self.manual_state = pylabsm_state_manual.Manual(self)
        self.manual_state.add_action(self.manual_state.manual_action)

        # Add states to state machine and create state transitions
        # SHOULD ADDITION OF STATES BE MOVED TO STATE BASE CLASS INSTANTIATION? #
        self.add_states([self.init_state, self.wait_state, self.manual_state])
        self.init_state.add_transition(self.wait_state)
        self.wait_state.add_transition(self.manual_state, arg="Manual or Auto", arg_result="manual")
        self.manual_state.add_transition(self.wait_state)

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
