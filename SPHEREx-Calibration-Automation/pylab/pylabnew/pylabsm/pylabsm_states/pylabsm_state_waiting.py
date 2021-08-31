"""pylabsm_state_waiting:

    This module provides the waiting state class.

"""
import asyncio
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Waiting(SmCustomState):

    def __init__(self, sm, identifier="waiting"):
        super().__init__(sm, self, identifier)

    async def waiting_action(self, in_dict):
        ret_code = True

        print("waiting for gui input... {}")
        data_queue = in_dict["Rx Queue"]
        gui_data = await data_queue.get()

        # Check the type of the gui input data. If the type is a list, then we know that a list of sequence parameters
        # has been sent and that a series should be run in the Auto state. Otherwise, enter the manual state.
        gui_input_type = type(gui_data)
        if gui_input_type is list:
            in_dict["Manual or Auto"][0] = "auto"
        else:
            in_dict["Manual or Auto"][0] = "manual"
            in_dict["Control"].update(gui_data)

        return ret_code
