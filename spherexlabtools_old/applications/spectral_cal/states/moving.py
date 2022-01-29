"""pylabsm_state_moving:

    This module implements the moving state class.

"""
import os
import sys
import asyncio
from .sm_data_mappings import INST_SM_MAP
from spherexlabtools.state import SmCustomState
from spherexlabtools.instruments import PylabInstrument, PymeasureInstrumentSub


class Moving(SmCustomState):

    def __init__(self, sm, identifier="moving", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def moving_action(self, action_arg):
        """ Parse the control loop for arguments specific to the moving state, then execute moving control loop.
        """
        if action_arg["Control Loop Generate"]:
            try:
                control_loop = action_arg["Control"]["Loop"]
                cl_keys = list(control_loop.keys())
                instruments = action_arg["Instruments"]
                for key in instruments:
                    key = key.lower()
                    if key in cl_keys:
                        try:
                            move_list_getter = getattr(self, "{}_move_cl".format(key))
                        except AttributeError:
                            action_arg["Moving"][key.upper()] = control_loop[key.lower()]
                        else:
                            action_arg["Moving"][key.upper()] = move_list_getter(control_loop[key])

                await self.moving_control_loop(action_arg)
            except Exception as e:
                print(e)

    async def moving_control_loop(self, cl_dict):
        """ Execute the moving control loop
        """
        try:
            instruments = cl_dict["Instruments"]
            moving = cl_dict["Moving"]
            ser_index = cl_dict["Series Index"][0]
            seq_index = cl_dict["Sequence Index"][0]
            for key in moving:
                command_dict = moving[key][ser_index][seq_index]
                cmd_keys = list(command_dict.keys())
                # Try sending a command dictionary to each instrument. If a movement fails, enter the error state
                try:
                    if issubclass(type(instruments[key]), PylabInstrument):
                        cur_params = await instruments[key].get_parameters("All")
                        # remove set parameters if the instrument is already in that state
                        for cmd_key in cmd_keys:
                            inst_cmd = INST_SM_MAP[key][cmd_key](cur_params[cmd_key])
                            if command_dict[cmd_key] == inst_cmd:
                                command_dict.pop(cmd_key)
                        if command_dict != {}:
                            await instruments[key].set_parameters(command_dict)
                        inst_dict = await instruments[key].get_parameters("All")

                    elif issubclass(type(instruments[key]), PymeasureInstrumentSub):
                        cur_params = instruments[key].quick_properties
                        # remove set parameters if the instrument is already in that state
                        for cmd_key in cmd_keys:
                            if command_dict[cmd_key] == INST_SM_MAP[key][cmd_key](cur_params[cmd_key]):
                                command_dict.pop(cmd_key)
                        if command_dict != {}:
                            instruments[key].quick_properties = command_dict
                        inst_dict = instruments[key].quick_properties
                    else:
                        raise RuntimeError("Unknown instrument type provided!")

                    # place new instrument parameters on the tx queue for external processing
                    if type(self.DataQueueTx) is asyncio.Queue:
                        self.DataQueueTx.put_nowait({key: inst_dict})
                    elif type(self.DataQueueTx) is dict:
                        self.DataQueueTx[key] = inst_dict

                    # place instrument parameters on the global metadata dict for processing
                    metadata = self.parse_meta({key: inst_dict})
                    for new_key in metadata:
                        cl_dict["Metadata"][new_key] = metadata[new_key]

                except Exception as e:
                    self.error_flag = True
                    break

        except Exception as e:
            print(e)

    @staticmethod
    def s401c_move_cl(s401c_cl):
        s401c_cl_len = len(s401c_cl)
        out_list = [{} for _ in range(s401c_cl_len)]
        for i in range(s401c_cl_len):
            out_list[i] = [{"wavelength": cl["wavelength"]} for cl in s401c_cl[i]]
        return out_list

    def sr510_move_cl(self, lockin_cl):
        return self.lockin_move_cl(lockin_cl)

    def sr830_move_cl(self, lockin_cl):
        return self.lockin_move_cl(lockin_cl)

    @staticmethod
    def lockin_move_cl(lockin_cl):
        out_list = [{} for _ in range(len(lockin_cl))]
        for i in range(len(lockin_cl)):
            out_list[i] = [{"sensitivity": lockin_seq["sensitivity"],
                            "time_constant": lockin_seq["time_constant"]} for lockin_seq in lockin_cl[i]]
        return out_list

    @staticmethod
    def parse_meta(inst_dict):
        inst_key = list(inst_dict.keys())[0]
        meta_dict = {}
        new_keys = []
        for inst_param in inst_dict[inst_key]:
            nk = inst_key + " " + inst_param.upper()
            new_keys.append(nk)
            meta_dict[nk] = inst_dict[inst_key][inst_param]

        return meta_dict
