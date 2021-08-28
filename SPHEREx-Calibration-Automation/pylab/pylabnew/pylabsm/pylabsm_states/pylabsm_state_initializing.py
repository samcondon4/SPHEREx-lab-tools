"""pylabsm_state_initializing:

    This module provides the initialization state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState
from pylabinst.pylabinst_instrument_base import Instrument


class Initializing(SmCustomState):

    def __init__(self, sm, identifier="initializing"):
        super().__init__(sm, self, identifier)

    async def initialize_instruments(self, action_arg):
        print("Initializing instruments")
        inst_param_dict = {}
        for key in action_arg:
            if issubclass(type(action_arg[key]), Instrument):
                action_arg[key].open()
                inst_params = await action_arg[key].get_parameters("All")
                inst_param_dict[key] = inst_params
        action_arg["Tx Queue"].put_nowait(inst_param_dict)
        print("Initialization complete")
        return True
