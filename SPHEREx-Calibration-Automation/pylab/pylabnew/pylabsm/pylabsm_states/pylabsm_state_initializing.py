"""pylabsm_state_initializing:

    This module provides the initialization state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState
from pylabinst.pylabinst_instrument_base import Instrument


class Initializing(SmCustomState):

    def __init__(self, sm, identifier="initializing"):
        super().__init__(sm, self, identifier)

    async def initialize_instruments(self, action_arg):
        print("initializing instruments...")
        for key in action_arg:
            if issubclass(type(action_arg[key]), Instrument):
                await action_arg[key].open()
                inst_params = await action_arg[key].get_parameters("All")
                action_arg["Tx Queue"][key] = inst_params
                print(inst_params)
        action_arg["Tx Queue"]["Instrument Initialization"] = True
        print("initialization complete")
        return True
