"""pylabsm_state_waiting:

    This module provides the waiting state class.

"""
import asyncio
import json
import numpy as np
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Waiting(SmCustomState):

    def __init__(self, sm, identifier="waiting"):
        super().__init__(sm, self, identifier)

        self.seq_waves = None
        self.seq_gen_later = []

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
            in_dict["Control"]["Loop"] = self.build_control_loop(gui_data)
        else:
            in_dict["Manual or Auto"][0] = "manual"
            in_dict["Control"].update(gui_data)

        return ret_code

    def build_control_loop(self, series):
        """Description: construct a control from a list of sequence parameters.

        :param series:
        :return: control loop
        """
        # initialize control loop dictionary #
        control_loop_dict = {}
        i = 0
        for sequence in series:
            for key in sequence:
                if key not in control_loop_dict:
                    control_loop_dict[key] = [self.build_sequence(key, sequence)]
                else:
                    control_loop_dict[key].extend([self.build_sequence(key, sequence)])
            for key in self.seq_gen_later:
                control_loop_dict[key][i] = self.build_sequence(key, sequence)

            self.seq_waves = None
            self.seq_gen_later = []
            i += 1

        return control_loop_dict

    def build_sequence(self, key, seq_params):
        """Description: route the seq params to the proper sequence generator function defined below.
        """
        ret_seq = None
        try:
            seq_gen_func = getattr(self, "{}_sequence".format(key))
        except AttributeError as e:
            pass
        else:
            ret_seq = seq_gen_func(seq_params[key])

        if ret_seq == "later":
            self.seq_gen_later.append(key)

        return ret_seq

    def cs260_sequence(self, cs260_params):
        """Description: construct a control loop list for the cs260 monochromator.

        :param cs260_params: (dict) CS260 sequence parameters dictionary
        :return: List of cs260 instrument command dictionaries.
        """

        # generate monochromator scan wavelengths
        waves = np.arange(float(cs260_params["start wavelength"]), float(cs260_params["end wavelength"]) +
                          float(cs260_params["step size"]),
                          float(cs260_params["step size"]))
        self.seq_waves = waves
        gratings = np.zeros_like(waves)
        filters = ["" for _ in range(len(waves))]
        # generate monochromator scan gratings
        i = 0
        for w in waves:
            if w <= float(cs260_params["g1 to g2 transition wavelength"]):
                gratings[i] = 1
            elif float(cs260_params["g1 to g2 transition wavelength"]) < w <= \
                 float(cs260_params["g2 to g3 transition wavelength"]):
                gratings[i] = 2
            elif float(cs260_params["g2 to g3 transition wavelength"]) < w:
                gratings[i] = 3
            i += 1

        # generate monochromator scan filters
        i = 0
        for w in waves:
            if w <= float(cs260_params["no osf to osf1 transition wavelength"]):
                filters[i] = "No OSF"
            elif float(cs260_params["no osf to osf1 transition wavelength"]) < w <= \
                 float(cs260_params["osf1 to osf2 transition wavelength"]):
                filters[i] = "OSF1"
            elif float(cs260_params["osf1 to osf2 transition wavelength"]) < w <= \
                    float(cs260_params["osf2 to osf3 transition wavelength"]):
                filters[i] = "OSF2"
            elif float(cs260_params["osf2 to osf3 transition wavelength"]) < w:
                filters[i] = "OSF3"
            i += 1

        cs260_seq = [{"current wavelength": waves[i], "current grating": gratings[i],
                               "current order sort filter": filters[i], "current shutter": cs260_params["shutter"]}
                     for i in range(len(waves))]

        return cs260_seq

    def ndf_sequence(self, ndf_params):
        """Description: construct a control loop list for the neutral density filter wheel.

        :param ndf_params: (dict) dictionary with ndf sequence parameters.
        :return: (list) list of ndf instrument command dictionaries.
        """
        if self.seq_waves is None:
            ndf_seq = "later"
        else:
            ndf_seq = [{"current position": 0} for _ in range(len(self.seq_waves))]
            ndf_transitions = json.loads(ndf_params["position transitions"].replace("'", '"'))
            transition_total = len(ndf_transitions)
            transi = 0
            seqi = 0
            position = 0
            for w in self.seq_waves:
                if w > float(ndf_transitions[transi]["wavelength"]):
                    position = int(ndf_transitions[transi]["position"])
                    if not transi == transition_total - 1:
                        transi += 1
                    ndf_seq[seqi]["current position"] = position
                else:
                    ndf_seq[seqi]["current position"] = position
                seqi += 1

        return ndf_seq

    def sr510_sequence(self, sr510_parmas):
        """ Description: Wrapper around self.lockin_sequence for the Sr510

        :param sr510_parmas: (dict) dictionary with sr830 sequence parameters.
        :return: (list) list of sr510 command dictionaries
        """
        return self.lockin_sequence(sr510_parmas)

    def sr830_sequence(self, sr830_parmas):
        """ Description: Wrapper around self.lockin_sequence for the Sr830

        :param sr830_parmas: (dict) dictionary with sr830 sequence parameters.
        :return: (list) list of sr830 command dictionaries
        """
        return self.lockin_sequence(sr830_parmas)

    def lockin_sequence(self, lockin_params):
        """ Description: Generate lockin control loop for both the sr830 and sr510 lockins.

        :param self:
        :param lockin_params: (dict) dictionary with lockin sequence parameters.
        :return: (list) list of lockin command dictionaries
        """
        if self.seq_waves is None:
            lockin_seq = "later"
        else:
            tc = float(lockin_params["time constant"])
            fs = float(lockin_params["sample frequency"])
            lockin_seq = [{"current sensitivity": 0.5, "current time constant": tc, "current sample rate": fs}
                          for _ in self.seq_waves]
            sens_transitions = json.loads(lockin_params["sensitivity transitions"].replace("'", '"'))
            transition_total = len(sens_transitions)
            transi = 0
            seqi = 0
            sens = 0.5
            for w in self.seq_waves:
                if w > float(sens_transitions[transi]["wavelength"]):
                    sens = float(sens_transitions[transi]["sensitivity"])
                    if not transi == transition_total - 1:
                        transi += 1
                    lockin_seq[seqi]["current sensitivity"] = sens
                else:
                    lockin_seq[seqi]["current sensitivity"] = sens
                seqi += 1

        return lockin_seq

