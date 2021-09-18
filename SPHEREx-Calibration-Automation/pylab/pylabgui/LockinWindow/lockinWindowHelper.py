"""lockinWindowHelper:

    This module provides a class, Lockin, which contains helper methods for all Lockin GuiWindows to use.

Sam Condon, 08/16/2021
"""

import json
import numpy as np


class Lockin:
    # HELPER DICTIONARIES ###############################################################################
    UNIT_SENSITIVITY_MAP = {"V.": 1, "mV.": 1e-3, "uV.": 1e-6, "nV.": 1e-9}
    UNIT_TC_MAP = {"ks.": 1e3, "s.": 1, "ms.": 1e-3, "us.": 1e-6}
    TC_MOD_MAP = {1: 0, 0: 3}
    TC_MULT_UNIT_MAP = {1e-6: ("x1", "us."), 1e-5: ("x10", "us."), 1e-4: ("x100", "us."),
                               1e-3: ("x1", "ms."), 1e-2: ("x10", "ms."), 1e-1: ("x100", "ms."),
                               1: ("x1", "s."), 1e1: ("x10", "s."), 1e2: ("x100", "s."),
                               1e3: ("x1", "ks.")}
    SENS_MOD_MAP = {0: 5, 1: 1, 2: 2}
    SENS_MULT_UNIT_MAP = {1e-9: ("x1", "nV."), 1e-8: ("x10", "nV."), 1e-7: ("x100", "nV."),
                                 1e-6: ("x1", "uV."), 1e-5: ("x10", "uV."), 1e-4: ("x100", "uV."),
                                 1e-3: ("x1", "mV."), 1e-2: ("x10", "mV."), 1e-1: ("x100", "mV."),
                                 1: ("x1", "V.")}
    FS = [float(2 ** i) for i in range(-4, 10)]
    ######################################################################################################

    @classmethod
    def get_tc(cls, tc_dict):
        value = float(tc_dict["value"])
        multiplier = float(tc_dict["multiplier"].split("x")[-1])
        unit_multiplier = float(cls.UNIT_TC_MAP[tc_dict["units"]])
        tc = value * multiplier * unit_multiplier
        return tc

    @classmethod
    def set_tc(cls, tc):
        if type(tc) is str:
            tc = float(tc)
        tc_mod = tc % 3
        tc_value = tc_mod + cls.TC_MOD_MAP[tc_mod]
        tc_mult, tc_units = cls.TC_MULT_UNIT_MAP[tc/tc_value]
        return {"time constant value": str(tc_value), "time constant multiplier": tc_mult, "time constant units": tc_units}

    @classmethod
    def get_sensitivity(cls, sens_dict):
        value = float(sens_dict["value"])
        multiplier = float(sens_dict["multiplier"].split("x")[-1])
        unit_multiplier = float(cls.UNIT_SENSITIVITY_MAP[sens_dict["units"]])
        total_mult = multiplier*unit_multiplier
        round_off = abs(int(np.log10(total_mult)))
        sensitivity = round(value * multiplier * unit_multiplier, round_off)
        sens_dict = {"sensitivity": sensitivity, "value": value, "multiplier": multiplier,
                     "unit_multiplier": unit_multiplier}
        return sens_dict

    @classmethod
    def lockin_ini_dict_proc(cls, lockin_dict):
        output_dict = lockin_dict
        sens = lockin_dict["sensitivity transitions"]
        sens = sens.replace("'", '"')
        sens = json.loads(sens)
        new_sens = [0 for _ in sens]
        for i in range(len(sens)):
            transition = sens[i]
            new_trans = {"data": transition, "text": "wavelength = {}, sensitivity = {};".format(
                transition["wavelength"], transition["sensitivity"])}
            new_sens[i] = new_trans
        output_dict["sensitivity transitions"] = new_sens

        tc = cls.set_tc(lockin_dict["time constant"])
        output_dict.pop("time constant")
        for key in tc:
            output_dict[key] = tc[key]

        return output_dict
