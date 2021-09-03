"""pylabsm_state_initializing:

    This module provides the initialization state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState
from pylabinst.pylabinst_instrument_base import Instrument


class Initializing(SmCustomState):

    def __init__(self, sm, identifier="initializing", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def initialize_instruments(self, action_arg):
        print("initializing instruments...")
        instruments = action_arg["Instruments"]
        for key in instruments:
            try:
                await instruments[key].open()
            except Exception as e:
                self.error_flag = True
                break
            else:
                inst_params = await instruments[key].get_parameters("All")
                action_arg["Tx Queue"][key] = inst_params
        action_arg["Tx Queue"]["Instrument Initialization"] = True
        print("initialization complete")
