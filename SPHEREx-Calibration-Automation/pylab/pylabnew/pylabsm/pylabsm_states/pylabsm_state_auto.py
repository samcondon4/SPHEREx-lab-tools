"""pylabsm_state_auto:

    This module provides the auto state class.

"""

import asyncio
from transitions.extensions.asyncio import AsyncMachine
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Moving(SmCustomState):

    def __init__(self, sm, identifier="moving", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def moving_action(self, move_dict):
        meta_keys = ["CS260 WAVELENGTH", "CS260 GRATING", "CS260 ORDER SORT FILTER",
                     "CS260 SHUTTER", "NDF POSITION", "SR830 SENSITIVITY", "SR830 TIME CONSTANT"]

        instruments = move_dict["Instruments"]
        moving = move_dict["Moving"]
        moving_key_list = list(moving.keys())

        for key in moving:
            command_dict = moving[key][self.sm.ser_index][self.sm.seq_index]
            # Try sending a command dictionary to each instrument. If a movement fails, enter the error state
            try:
                await instruments[key].set_parameters(command_dict)
                inst_dict = await instruments[key].get_parameters("All")
                move_dict["Tx Queue"][key] = inst_dict
                metadata = self.parse_meta({key: inst_dict})
                for new_key in metadata:
                    if new_key in meta_keys:
                        move_dict["Metadata"][new_key] = metadata[new_key]
            except Exception as e:
                print(e)
                self.error_flag = True
                break

    @staticmethod
    def parse_meta(inst_dict):
        inst_key = list(inst_dict.keys())[0]
        meta_dict = {}
        new_keys = []
        for inst_param in inst_dict[inst_key]:
            nk = inst_param.replace("current", inst_key).upper()
            new_keys.append(nk)
            meta_dict[nk] = inst_dict[inst_key][inst_param]

        return meta_dict

class Measuring(SmCustomState):

    def __init__(self, sm, identifier="measuring", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def measuring_action(self, measuring_dict):
        measure = measuring_dict["Measuring"]
        for key in measure:
            try:
                measurement_params = measure[key][self.sm.ser_index][self.sm.seq_index]
                measurement_params["storage path"] += key + ".csv"
                metadata = measuring_dict["Metadata"]
                await measuring_dict["Instruments"][key.upper()].start_measurement(measurement_params, metadata=metadata,
                                                                                   append_to_existing=True, hold=True)
            except Exception as e:
                self.error_flag = True


class Indexing(SmCustomState):

    def __init__(self, sm, identifier="indexing", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    def indexing_action(self, in_dict):
        print("## INDEX VALUES: series = {}, sequence = {}".format(self.sm.ser_index, self.sm.seq_index))
        in_dict["Control Loop Complete"][0] = False
        mdk_list = list(in_dict["Moving"].keys())
        if self.sm.seq_index < len(in_dict["Moving"][mdk_list[self.sm.ser_index]][0]):
            self.sm.seq_index += 1
        elif self.sm.ser_index < len(in_dict["Moving"][mdk_list[self.sm.ser_index]]):
            self.sm.ser_index += 1
            self.sm.seq_index = 0
        else:
            self.sm.ser_index = 0
            self.sm.seq_index = 0
            in_dict["Control Loop Complete"][0] = True


class AutoDone(SmCustomState):

    def __init__(self, sm, identifier="done", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)


class AutoStateMachine(AsyncMachine):

    def __init__(self):
        super().__init__(model=self)
        # Action argument attributes #
        self.moving_dict = {}
        self.meta_dict = {}
        self.measuring_dict = {}
        self.control_loop_complete = [False]
        self.ser_index = 0
        self.seq_index = 0
        ##############################

        # Initialize sub state machine action arguments ########################################
        SmCustomState.set_global_args({"Moving": self.moving_dict})
        SmCustomState.set_global_args({"Metadata": self.meta_dict})
        SmCustomState.set_global_args({"Measuring": self.measuring_dict})
        SmCustomState.set_global_args({"Control Loop Complete": self.control_loop_complete})
        ########################################################################################

        # Configure states and state actions #####################################################################
        self.moving_state = Moving(self, initial=True)
        self.moving_state.add_action(self.moving_state.moving_action, args=["Moving", "Metadata",
                                                                            "Instruments", "Tx Queue"])

        self.measuring_state = Measuring(self)
        self.measuring_state.add_action(self.measuring_state.measuring_action, args=["Measuring", "Instruments",
                                                                                     "Metadata"])

        self.indexing_state = Indexing(self)
        self.indexing_state.add_action(self.indexing_state.indexing_action, args=["Control Loop Complete", "Moving"])

        self.done_state = AutoDone(self, hold_on_complete=True)
        ##########################################################################################################

        # Add states and transitions to the auto sub state machine ###############################################
        self.add_states([self.moving_state, self.measuring_state, self.indexing_state, self.done_state])
        self.moving_state.add_transition(self.measuring_state)
        self.measuring_state.add_transition(self.indexing_state)
        self.indexing_state.add_transition(self.moving_state, arg="Control Loop Complete", arg_result=[False])
        self.indexing_state.add_transition(self.done_state, arg="Control Loop Complete", arg_result=[True])
        #########################################################################################################


class Auto(SmCustomState):

    def __init__(self, sm, identifier="auto"):
        super().__init__(sm, self, identifier)

        self.auto_sm = AutoStateMachine()

    async def auto_sm_exec(self, action_arg):
        """Description: pass control loop parameters to the proper states, then wait until the done state is reached
                        before returning

        :param action_arg: (list) input control loop
        :return: None
        """
        control_loop = action_arg["Control"]["Loop"]
        cl_keys = list(control_loop.keys())
        instruments = action_arg["Instruments"]
        measure_args = control_loop["measure"]
        for key in instruments:
            key = key.lower()
            if key in cl_keys:
                self.auto_sm.moving_dict[key.upper()] = control_loop[key]

        # Get instrument specific measurement parameters #########################################
        for seq in measure_args:
            for key in seq:
                if (key.upper() in instruments) and seq[key]:
                    measure_list_getter = getattr(self, "{}_measure_dict".format(key))
                    if self.auto_sm.measuring_dict == {}:
                        self.auto_sm.measuring_dict[key] = measure_list_getter(control_loop[key])
        ##########################################################################################

        # Get sequence measurement parameters ###########################################
        for key in self.auto_sm.measuring_dict:
            i = 0
            for seq in self.auto_sm.measuring_dict[key]:
                for mdict in seq:
                    mdict["sample time"] = control_loop["measure"][i]["sample time"]
                    mdict["storage path"] = control_loop["measure"][i]["storage path"]
                i += 1
        #################################################################################

        auto_sm_task = asyncio.create_task(self.auto_sm.to_moving())
        while not self.auto_sm.state == self.auto_sm.done_state.identifier:
            await asyncio.sleep(0)
        self.auto_sm.measuring_dict = []
        self.auto_sm.done_state.hold_complete = True

    @staticmethod
    def sr830_measure_dict(lockin_cl):
        out_list = [{} for _ in range(len(lockin_cl))]
        for i in range(len(lockin_cl)):
            out_list[i] = [{"sample rate": lockin_seq["current sample rate"]} for lockin_seq in lockin_cl[i]]
        return out_list
