"""pylabsm_state_manual:

    This module provides the manual state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Manual(SmCustomState):

    def __init__(self, sm, identifier="manual"):
        super().__init__(sm, self, identifier)

    async def manual_action(self, action_arg):
        control_args = action_arg["Control"]
        command_dict = {}
        for key1 in control_args:
            inst_key = key1.replace("new ", "").upper()
            for key2 in control_args[key1]:
                inst_param_data = control_args[key1][key2]
                inst_param_key = key2.replace("new", "current")
                command_dict[inst_param_key] = inst_param_data
            print({inst_key: command_dict})
            await action_arg[inst_key].set_parameters(command_dict)
            inst_dict = await action_arg[inst_key].get_parameters("All")
            print(inst_dict)
            action_arg["Tx Queue"][inst_key] = inst_dict
