"""lockinWindowHelper:

    This module provides a class, NDF, which contains helper methods for all NDF GuiWindows to use.

Sam Condon, 08/16/2021
"""

import json


class NDF:

    @classmethod
    def ndf_ini_dict_proc(cls, ndf_dict):
        output_dict = ndf_dict
        pos = output_dict["position transitions"]
        pos = pos.replace("'", '"')
        pos = json.loads(pos)
        new_pos = [0 for _ in pos]
        for i in range(len(pos)):
            transition = pos[i]
            new_trans = {"data": transition, "text": "wavelength = {}, position = {};".format(transition["wavelength"],
                                                                                            transition["position"])}
            new_pos[i] = new_trans
        output_dict["position transitions"] = new_pos

        return output_dict
