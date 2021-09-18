"""pylabsm_state_auto:

    This module provides the auto state class.

"""

import asyncio
import pylabinst.pylabinst_instrument_base as pylabinst
from transitions.extensions.asyncio import AsyncMachine
import pymeasure.instruments.instrument as pymeasureinst
from pylabsm.pylab_inst_sm_data_mappings import INST_SM_MAP
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Moving(SmCustomState):
    meta_keys = ["CS260 WAVELENGTH", "CS260 GRATING", "CS260 ORDER_SORT_FILTER", "CS260 SHUTTER", "NDF POSITION"]

    def __init__(self, sm, identifier="moving", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def moving_action(self, move_dict):

        instruments = move_dict["Instruments"]
        moving = move_dict["Moving"]
        moving_key_list = list(moving.keys())
        for key in moving:
            command_dict = moving[key][self.sm.ser_index][self.sm.seq_index]
            cmd_keys = list(command_dict.keys())
            # Try sending a command dictionary to each instrument. If a movement fails, enter the error state
            try:
                if issubclass(type(instruments[key]), pylabinst.Instrument):
                    cur_params = await instruments[key].get_parameters("All")
                    # remove set parameters if the instrument is already in that state
                    for cmd_key in cmd_keys:
                        inst_cmd = INST_SM_MAP[key][cmd_key](cur_params[cmd_key])
                        if command_dict[cmd_key] == inst_cmd:
                            command_dict.pop(cmd_key)
                    if command_dict != {}:
                        await instruments[key].set_parameters(command_dict)
                    inst_dict = await instruments[key].get_parameters("All")

                elif issubclass(type(instruments[key]), pymeasureinst.Instrument):
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

                move_dict["Tx Queue"][key] = inst_dict
                metadata = self.parse_meta({key: inst_dict})
                for new_key in metadata:
                    if new_key in self.meta_keys:
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
            nk = inst_key + " " + inst_param.upper()
            new_keys.append(nk)
            meta_dict[nk] = inst_dict[inst_key][inst_param]

        return meta_dict


class Measuring(SmCustomState):

    def __init__(self, sm, identifier="measuring", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def measuring_action(self, measuring_dict):
        measure = measuring_dict["Measuring"]
        measure_coros = [None for _ in range(len(measure))]
        k = 0
        exception = None
        for key in measure:
            try:
                procedure = measuring_dict["Procedures"][key.upper()]
                measurement_params = measure[key][self.sm.ser_index][self.sm.seq_index]
                storage_path = measurement_params["storage_path"] + measurement_params["sequence_name"] + "_" + key + \
                               ".csv"
                measurement_params["storage_path"] = storage_path
                metadata = measuring_dict["Metadata"]
                procedure.metadata = metadata
                measure_coros[k] = asyncio.create_task(procedure.run(measurement_params, append_to_existing=True,
                                                                     hold=True))
            except Exception as e:
                print(e)
                self.error_flag = True
                break

            else:
                # iterate to next measurement
                k += 1

        # if no exception occured, run the measuring coroutines
        if exception is None:
            await asyncio.wait(measure_coros)


class Indexing(SmCustomState):

    def __init__(self, sm, identifier="indexing", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)
        self.sequence = None
        self.series = None

    def indexing_action(self, in_dict):
        print("## INDEX VALUES: series = {}, sequence = {}".format(self.sm.ser_index, self.sm.seq_index))
        in_dict["Control Loop Complete"][0] = False
        mdk_list = list(in_dict["Moving"].keys())

        # update the current sequence/series if necessary ######################
        if self.sequence is None:
            self.sequence = in_dict["Moving"][mdk_list[0]][self.sm.ser_index]
        if self.series is None:
            self.series = in_dict["Moving"][mdk_list[0]]

        # perform indexing using the lengths of the sequences/series ############
        if self.sm.seq_index < len(self.sequence) - 1:
            self.sm.seq_index += 1
        elif self.sm.ser_index < len(self.series) - 1:
            self.sequence = None
            self.sm.ser_index += 1
            self.sm.seq_index = 0
        else:
            self.sm.ser_index = 0
            self.sm.seq_index = 0
            self.sequence = None
            self.series = None
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
                                                                                     "Procedures", "Metadata"])

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
        try:
            control_loop = action_arg["Control"]["Loop"]
            cl_keys = list(control_loop.keys())
            instruments = action_arg["Instruments"]
            measure_args = control_loop["measure"]
            for key in instruments:
                key = key.lower()
                if key in cl_keys:
                    try:
                        move_list_getter = getattr(self, "{}_move_cl".format(key))
                    except AttributeError:
                        self.auto_sm.moving_dict[key.upper()] = control_loop[key]
                    else:
                        self.auto_sm.moving_dict[key.upper()] = move_list_getter(control_loop[key])

            # Get instrument specific measurement parameters #########################################
            for seq in measure_args:
                for key in seq:
                    if (key.upper() in instruments) and seq[key] == "True":
                        try:
                            measure_list_getter = getattr(self, "{}_measure_cl".format(key))
                        except AttributeError:
                            self.auto_sm.measuring_dict[key] = control_loop[key]
                        else:
                            self.auto_sm.measuring_dict[key] = measure_list_getter(control_loop[key])
            ##########################################################################################

            # Get sequence measurement parameters ###########################################
            for key in self.auto_sm.measuring_dict:
                i = 0
                for seq in self.auto_sm.measuring_dict[key]:
                    for mdict in seq:
                        mdict["sample_time"] = control_loop["measure"][i]["sample time"]
                        mdict["storage_path"] = control_loop["measure"][i]["storage path"]
                        mdict["sequence_name"] = control_loop["sequence info"][i]["sequence name"]
                    i += 1
            #################################################################################

            auto_sm_task = asyncio.create_task(self.auto_sm.to_moving())
            while not self.auto_sm.state == self.auto_sm.done_state.identifier:
                await asyncio.sleep(0)
            self.auto_sm.measuring_dict = {}
            self.auto_sm.done_state.hold_complete = True

        except Exception as e:
            print(e)

    def sr510_move_cl(self, lockin_cl):
        return self.lockin_move_cl(lockin_cl)

    def sr510_measure_cl(self, lockin_cl):
        return self.lockin_measure_cl(lockin_cl)

    def sr830_move_cl(self, lockin_cl):
        return self.lockin_move_cl(lockin_cl)

    def sr830_measure_cl(self, lockin_cl):
        return self.lockin_measure_cl(lockin_cl)

    @staticmethod
    def lockin_measure_cl(lockin_cl):
        out_list = [{} for _ in range(len(lockin_cl))]
        for i in range(len(lockin_cl)):
            out_list[i] = [{"sample_rate": lockin_seq["sample_rate"]} for lockin_seq in lockin_cl[i]]
        return out_list

    @staticmethod
    def lockin_move_cl(lockin_cl):
        out_list = [{} for _ in range(len(lockin_cl))]
        for i in range(len(lockin_cl)):
            out_list[i] = [{"sensitivity": lockin_seq["sensitivity"],
                            "time_constant": lockin_seq["time_constant"]} for lockin_seq in lockin_cl[i]]
        return out_list
