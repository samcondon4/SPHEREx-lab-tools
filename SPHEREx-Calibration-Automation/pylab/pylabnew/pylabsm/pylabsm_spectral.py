"""pylabsm_spectral:

    This module implements the spectral calibration specific state machine.

"""

import asyncio
from transitions.extensions.asyncio import AsyncMachine
from pylabsm.pylabsm_states.pylabsm_statesimport import pylabsm_state_initializing, pylabsm_state_waiting, \
                                                        pylabsm_state_manual, pylabsm_basestate


class SpectralCalibrationMachine(AsyncMachine):

    def __init__(self, data_queue=None):
        # Configure global data queue for interfacing w/ external software or internal testing #
        if data_queue is None:
            queue = asyncio.Queue()
        else:
            queue = data_queue
        pylabsm_basestate.SmCustomState.set_global_args({"Global Queue": queue})
        pylabsm_basestate.SmCustomState.set_global_args({"Manual or Auto": [""]})

        # Instantiate AsyncMachine base class #
        super().__init__(model=self)

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
        self.wait_state.add_transition(self.manual_state, arg="Manual or Auto", arg_result=["manual"])
        self.manual_state.add_transition(self.wait_state)


async def main(sm):
    await sm.start_machine()

if __name__ == "__main__":
    sm = SpectralCalibrationMachine()
    asyncio.run(main(sm))
