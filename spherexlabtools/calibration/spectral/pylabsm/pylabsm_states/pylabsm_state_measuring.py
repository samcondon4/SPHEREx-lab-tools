"""pylabsm_state_measuring:

    This module implements the measuring state class.

"""

import asyncio
import datetime
import pdb

from .pylabsm_basestate import SmCustomState


class Measuring(SmCustomState):

    metadata_strings = ["CS260 WAVELENGTH", "CS260 GRATING", "CS260 ORDER_SORT_FILTER", "CS260 SHUTTER",
                        "NDF POSITION"]

    def __init__(self, sm, identifier="measuring", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def measuring_action(self, action_arg):
        try:
            control_loop = action_arg["Control"]["Loop"]
            cl_keys = list(control_loop.keys())
            instruments = action_arg["Instruments"]
            measure_args = control_loop["measure"]
            # Get instrument specific measurement parameters #########################################
            for seq in measure_args:
                for key in seq:
                    if (key.upper() in instruments) and seq[key] == "True":
                        try:
                            measure_list_getter = getattr(self, "{}_measure_cl".format(key))
                        except AttributeError:
                            action_arg["Measuring"][key] = control_loop[key.lower()]
                        else:
                            action_arg["Measuring"][key] = measure_list_getter(control_loop[key])
            ##########################################################################################

            # Get sequence measurement parameters ###########################################
            for key in action_arg["Measuring"]:
                i = 0
                for seq in action_arg["Measuring"][key]:
                    for mdict in seq:
                        mdict["sample_time"] = control_loop["measure"][i]["sample time"]
                        mdict["storage_path"] = control_loop["measure"][i]["storage path"]
                        mdict["sequence_name"] = control_loop["sequence info"][i]["sequence name"]
                    i += 1
            #################################################################################

            await self.measuring_control_loop(action_arg)

        except Exception as e:
            print(e)

    async def measuring_control_loop(self, measuring_dict):
        measure = measuring_dict["Measuring"]
        archive = measuring_dict["Archiving"]
        #pdb.set_trace()
        measure_coros = [None for _ in range(len(measure))]
        ser_index = measuring_dict["Series Index"][0]
        seq_index = measuring_dict["Sequence Index"][0]
        k = 0
        exception = None
        for key in measure:
            try:
                now = datetime.datetime.now()
                procedure = measuring_dict["Procedures"][key.upper()]
                measurement_params = measure[key][ser_index][seq_index]
                storage_path = measurement_params["storage_path"] + measurement_params["sequence_name"] + "_" + key + \
                               ".csv"
                measurement_params["storage_path"] = storage_path
                metadata = measuring_dict["Metadata"]
                meta_keys = list(metadata.keys())
                for mkey in meta_keys:
                    if mkey not in self.metadata_strings:
                        metadata.pop(mkey)
                procedure.metadata = metadata
                i = ser_index * len(archive[key]) + seq_index
                archive[key][i]["start_time"] = now.strftime('%Y-%m-%d %H:%M:%S')
                archive[key][i]["storage_path"] = storage_path.replace("C:", "/c").replace("\\", "/")
                #print(archive[key][i])
                #pdb.set_trace()
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

    @staticmethod
    def s401c_measure_cl(s401c_cl):
        s401c_cl_len = len(s401c_cl)
        out_list = [{} for _ in range(s401c_cl_len)]
        for i in range(s401c_cl_len):
            out_list[i] = [{"sample_rate": cl["sample_rate"]} for cl in s401c_cl[i]]
        return out_list

    def sr510_measure_cl(self, lockin_cl):
        return self.lockin_measure_cl(lockin_cl)

    def sr830_measure_cl(self, lockin_cl):
        return self.lockin_measure_cl(lockin_cl)

    @staticmethod
    def lockin_measure_cl(lockin_cl):
        out_list = [{} for _ in range(len(lockin_cl))]
        for i in range(len(lockin_cl)):
            out_list[i] = [{"sample_rate": lockin_seq["sample_rate"]} for lockin_seq in lockin_cl[i]]
        return out_list
