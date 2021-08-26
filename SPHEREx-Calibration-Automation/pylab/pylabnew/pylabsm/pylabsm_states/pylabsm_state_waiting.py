"""pylabsm_state_waiting:

    This module provides the waiting state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Waiting(SmCustomState):

    def __init__(self, sm, identifier="waiting"):
        super().__init__(sm, self, identifier)

    async def waiting_action(self, in_dict):
        data_queue = in_dict["Global Queue"]
        gui_data = await data_queue.get()
