"""pylabsm_state_manual:

    This module provides the manual state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Manual(SmCustomState):

    def __init__(self, sm, identifier="manual"):
        super().__init__(sm, self, identifier)

    def manual_action(self, action_arg):
        print("move instruments manually")
