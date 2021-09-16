"""pylabsm_state_manual:

    This module provides the manual state class.

"""
import pymeasure.instruments.instrument

import pylabinst.pylabinst_instrument_base
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Manual(SmCustomState):

    def __init__(self, sm, identifier="manual"):
        super().__init__(sm, self, identifier)

    async def manual_action(self, action_arg):
        control_args = action_arg["Control"]
        instruments = action_arg["Instruments"]
        procedures = action_arg["Procedures"]
        command_dict = {}
        key1_list = list(control_args.keys())
        for key1 in control_args:
            key1_split = key1.split("_")
            # get the name of the instrument
            inst_key = key1_split[1].upper()
            # check if the dictionary specifies a new instrument state or measurement parameters
            state_or_measure = key1_split[2]

            # set new instrument state
            if state_or_measure == "state":
                for key2 in control_args[key1]:
                    # instrument state parameter data
                    inst_param_data = control_args[key1][key2]
                    # instrument state parameter name
                    inst_param_key = key2.replace("new_", "")
                    # update command dictionary
                    command_dict[inst_param_key] = inst_param_data
                # get the type of the instrument and call the appropriate parameter getter/setter for that type
                inst_type = type(instruments[inst_key])
                if issubclass(inst_type, pylabinst.pylabinst_instrument_base.Instrument):
                    await instruments[inst_key].set_parameters(command_dict)
                    inst_dict = await instruments[inst_key].get_parameters("All")
                elif issubclass(inst_type, pymeasure.instruments.instrument.Instrument):
                    print(command_dict)
                    instruments[inst_key].quick_properties = command_dict
                    inst_dict = instruments[inst_key].quick_properties
                else:
                    inst_dict = None

                """
                inst_dict2 = {}
                for key in inst_dict:
                    new_key = key.replace("current", "new")
                    inst_dict2[new_key] = inst_dict[key]
                """

                # place updated instrument parameter dictionary onto the Tx Queue for external processing
                print(inst_dict)
                action_arg["Tx Queue"][inst_key] = inst_dict

            # run a measurement
            elif state_or_measure == "measurement":
                measure_params = {}
                for key2 in control_args[key1]:
                    key2_split = key2.split("_")
                    measure_param_key = key2.replace(key2_split[0] + "_", "")
                    measure_params[measure_param_key] = control_args[key1][key2]
                # call the instrument measurement function
                measure_params[inst_key] = instruments[inst_key]
                await procedures[inst_key].run(measure_params)

        # remove instrument control parameters from the control dictionary so that we don't repeat the same thing we
        # just did.
        for key in key1_list:
            action_arg["Control"].pop(key)
