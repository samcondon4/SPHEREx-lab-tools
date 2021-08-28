"""pylabsm_state_initializing:

    This module provides the initialization state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Initializing(SmCustomState):

    def __init__(self, sm, identifier="initializing"):
        super().__init__(sm, self, identifier)

    def initialize_instruments(self, action_arg):
        print("Initializing instruments")
        print(action_arg)
        return True
