"""pylabsm_state_auto:

    This module provides the auto state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Auto(SmCustomState):

    def __init__(self, sm, identifier="auto"):
        super().__init__(sm, self, identifier)

    def auto_action(self, action_arg):
        print("Run series")
