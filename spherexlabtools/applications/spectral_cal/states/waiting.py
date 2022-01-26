"""pylabsm_state_waiting:

    This module implements the waiting state class.

"""
import json
import datetime
import numpy as np
from spherexlabtools.state import SmCustomState


class Waiting(SmCustomState):

    def __init__(self, sm, identifier="waiting", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

        self.seq_waves = None
        self.seq_gen_later = []

    async def waiting_action(self, in_dict):
        ret_code = True
        # set flag so that other states to generate their state specific control loop
        in_dict["Control Loop Generate"][0] = True
        # kill any workers that may still be running from the measuring state #
        for proc_key in in_dict["Procedures"]:
            proc = in_dict["Procedures"][proc_key]
            if proc.running:
                print("Killing worker on procedure {}".format(proc_key))
                proc.worker.stop()
                proc.running = False

        print("waiting for gui input...")
        gui_data = await self.pend_for_data()

        # reset the control loop before updating it with new data
        self.reset_control_loop(in_dict)
        # Check the type of the gui input data. If the type is a list, then we know that a list of sequence parameters
        # has been sent and that a series should be run in the Auto state. Otherwise, enter the manual state.
        gui_input_type = type(gui_data)
        if gui_input_type is list:
            in_dict["Manual or Auto"][0] = "auto"
            in_dict["Control"]["Loop"] = self.build_control_loop(gui_data)
            # Add exposure ids to dicts
            in_dict["Archiving"] = self.assign_exposure_ids(in_dict["Archiving"], in_dict["Control"]["Loop"], in_dict["Tables"])
        else:
            in_dict["Manual or Auto"][0] = "manual"
            in_dict["Control"].update(gui_data)
            # Add exposure ids to dicts
            in_dict["Archiving"] = self.assign_exposure_ids(in_dict["Archiving"], [[in_dict["Control"]]], in_dict["Tables"])

        return ret_code

    def assign_exposure_ids(self, archive_dict, control_loop, tables_dict):
        timestamp_prefix = "_".join((SmCustomState.get_prefix_datestamp(), SmCustomState.get_prefix_timestamp()))
        now = datetime.datetime.now()
        #timestamp = SmCustomState.
        # archive_dict = {} # Contains subset of control_dict, with the exposure_id.
        # E.g.;
        # archive_dict = {"cs260": [{"exp_id": "20211215_1031_0", "wavelength": 500, "bandwidth": 10, "grating": 2, ...},
        #                           {"exp_id": "20211215_1031_1", "wavelength": 510, "bandwidth": 10, "grating": 2, ...},
        #                           ...],
        #                 "sr510: [{"exp_id": "20211215_1031_0", "sample_rate": 1, "time_constant": 1, "sensitivity":10},
        #                          {"exp_id": "20211215_1031_1", "sample_rate": 1, "time_constant": 1, "sensitivity":10},
        #                           ...],
        #                 ...}
        key0 = list(control_loop.keys())[0]  # Used only to get lengths of sequences
        control_loop['control_software'] = []  # Add empty control_software list which gets populated below
        for key in control_loop:
            i = 0
            if key in tables_dict:
                series = control_loop[key]  # A list of dicts []

                #  Populate control_software table here
                if key == 'control_software':
                    for j, jseries in enumerate(control_loop[key0]):
                        control_loop_list = []
                        for jsequence in range(len(jseries)):
                            control_loop_dict = {'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                                                 'date': now.strftime('%Y-%m-%d'),
                                                 'sequence': control_loop['sequence info'][j]['sequence name']}
                            control_loop_list.extend([control_loop_dict])
                        series.extend([control_loop_list])
                        #pdb.set_trace()

                for ilist, sequence_list in enumerate(series):
                    for exposure_settings_dict in sequence_list:
                        archive_settings_dict = {}  # To store settings for archiving
                        for isetting in exposure_settings_dict:
                            #print(isetting)
                            if isetting in tables_dict[key]:
                                if "exp_id" not in archive_settings_dict:
                                    i += 1
                                    archive_settings_dict["exp_id"] = "_".join([timestamp_prefix, str(i)])

                                archive_settings_dict[isetting] = exposure_settings_dict[isetting]
                        #pdb.set_trace()
                        # Add dict to list
                        if key not in archive_dict:
                            archive_dict[key] = [archive_settings_dict]
                        else:
                            archive_dict[key].extend([archive_settings_dict])
        #print(archive_dict)
        #pdb.set_trace()
        return archive_dict

    def reset_control_loop(self, in_dict):
        """ Method that clears the control argument dictionary and all of the control loop parameters depending on the
            status of the state machine
        """
        # clear out control loop, moving, and measuring dictionaries #
        cl_keys = list(in_dict["Control"].keys())
        for key in cl_keys:
            in_dict["Control"].pop(key)

        move_keys = list(in_dict["Moving"].keys())
        for key in move_keys:
            in_dict["Moving"].pop(key)

        measure_keys = list(in_dict["Measuring"].keys())
        for key in measure_keys:
            in_dict["Measuring"].pop(key)

        archive_keys = list(in_dict["Archiving"].keys())
        for key in archive_keys:
            in_dict["Archiving"].pop(key)
        ###############################################################

        # Reset the series and sequence index if the machine is aborting from a running series
        if self.abort:
            in_dict["Series Index"][0] = 0
            in_dict["Sequence Index"][0] = 0
            SmCustomState.abort = False

        SmCustomState.paused = False

    def build_control_loop(self, series):
        """Description: construct a control loop from a list of sequence parameters.

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
        # look for a sequence generator function, if one doesn't exist then just return the sequence as is ###########
        try:
            seq_gen_func = getattr(self, "{}_sequence".format(key))
        except AttributeError as e:
            ret_seq = seq_params[key]
        else:
            ret_seq = seq_gen_func(seq_params[key])

        if ret_seq == "later":
            self.seq_gen_later.append(key)
        ###############################################################################################################

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
        grating_transitions = json.loads(cs260_params["grating transitions"].replace("'", '"'))
        grating_total = len(grating_transitions)
        filters = ["" for _ in range(len(waves))]
        filter_transitions = json.loads(cs260_params["osf transitions"].replace("'", '"'))
        filter_total = len(filter_transitions)
        # generate monochromator scan gratings
        gtransi = 0
        ftransi = 0
        seqi = 0
        grat = 1
        filt = 1
        for w in waves:
            # get the appropriate grating #
            while gtransi < grating_total and w > float(grating_transitions[gtransi]["wavelength"]):
                grat = int(grating_transitions[gtransi]["grating"])
                gtransi += 1
            gratings[seqi] = grat
            # get the appropriate order sort filter #
            while ftransi < filter_total and w > float(filter_transitions[ftransi]["wavelength"]):
                filt = int(filter_transitions[ftransi]["osf"])
                ftransi += 1
            filters[seqi] = "OSF%i" % filt
            seqi += 1

        cs260_seq = [{"wavelength": waves[i], "grating": gratings[i],
                      "order_sort_filter": filters[i], "shutter": cs260_params["shutter"]}
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
            ndf_seq = [{"position": 0} for _ in range(len(self.seq_waves))]
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
                    ndf_seq[seqi]["position"] = position
                else:
                    ndf_seq[seqi]["position"] = position
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
            fs = float(lockin_params["sample rate"])
            lockin_seq = [{"sensitivity": 0.5, "time_constant": tc, "sample_rate": fs}
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
                    lockin_seq[seqi]["sensitivity"] = sens
                else:
                    lockin_seq[seqi]["sensitivity"] = sens
                seqi += 1

        return lockin_seq

    def s401c_sequence(self, params):
        """ Generate the control loop for the s401c thermal detector.

        :param params: (dict) dictionary with s401c sequence parameters. Currently this is actually just an empty
                       dictionary as the only sequence parameters for this detector are the monochromator wavelength.
        """
        sample_rate = params["sample rate"]
        if self.seq_waves is None:
            s401_seq = "later"
        else:
            s401_seq = [{"wavelength": w*1e3, "sample_rate": float(sample_rate)} for w in self.seq_waves]

        return s401_seq

