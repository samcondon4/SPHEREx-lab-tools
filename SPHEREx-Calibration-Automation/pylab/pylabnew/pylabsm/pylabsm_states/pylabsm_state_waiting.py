"""pylabsm_state_waiting:

    This module provides the waiting state class.

"""
import asyncio
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Waiting(SmCustomState):

    def __init__(self, sm, identifier="waiting"):
        super().__init__(sm, self, identifier)

    async def waiting_action(self, in_dict):
        print("waiting for gui input... {}".format(in_dict))
        data_queue = in_dict["Global Queue"]
        gui_data = await data_queue.get()
        gui_input_type = type(gui_data)
        if gui_input_type is list:
            in_dict["Manual or Auto"][0] = "auto"
        else:
            in_dict["Manual or Auto"][0] = "manual"
        print(gui_data)
