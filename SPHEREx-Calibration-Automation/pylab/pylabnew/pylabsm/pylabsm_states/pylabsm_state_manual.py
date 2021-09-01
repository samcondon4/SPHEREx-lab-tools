"""pylabsm_state_manual:

    This module provides the manual state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Manual(SmCustomState):

    def __init__(self, sm, identifier="manual"):
        super().__init__(sm, self, identifier)

    async def manual_action(self, action_arg):
        print("moving instruments manually...")
        control_args = action_arg["Control"]
        command_dict = {}
        print(control_args)
        key1_list = [0 for _ in range(len(control_args))]
        i = 0
        for key1 in control_args:
            inst_key = key1.split(" ")[1].upper()
            for key2 in control_args[key1]:
                inst_param_data = control_args[key1][key2]
                inst_param_key = key2.replace("new", "current")
                command_dict[inst_param_key] = inst_param_data
            await action_arg[inst_key].set_parameters(command_dict)
            inst_dict = await action_arg[inst_key].get_parameters("All")
            inst_dict2 = {}
            for key in inst_dict:
                new_key = key.replace("current", "new")
                inst_dict2[new_key] = inst_dict[key]
            key1_list[i] = key1
            action_arg["Tx Queue"][inst_key] = inst_dict
            action_arg["Tx Queue"][inst_key] = inst_dict

        #remove instrument control parameters from the control dictionary
        for key in key1_list:
            action_arg["Control"].pop(key)