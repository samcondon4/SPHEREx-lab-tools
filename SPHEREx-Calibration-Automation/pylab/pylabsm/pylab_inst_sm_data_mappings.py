"""pylab_sm_inst_data_mapping:

    This module provides mappings between the data formats returned by instrument drivers and those present within the
    state machine.
"""

# monochromator mapping #########################################################
cs260_inst_to_sm_osf_map = {"1": "OSF1", "2": "OSF2", "3": "OSF3", "4": "No OSF"}
cs260_sm_to_inst_osf_map = {"OSF1": "1", "OSF2": "2", "OSF3": "3", "No OSF": "4", "Auto": "Auto"}
cs260_inst_to_sm_grating_map = {"1": "G1", "2": "G2", "3": "G3"}
cs260_sm_to_inst_grating_map = {"G1": "1", "G2": "2", "G3": 3, "Auto": "Auto"}

CS260_INST_TO_SM = {"wavelength": lambda w: float(w),
                    "grating": lambda g: float(g),
                    "order_sort_filter": lambda osf: cs260_inst_to_sm_osf_map[osf],
                    "shutter": lambda s: "Open" if s == "O" else "Close",
                    "units": lambda u: u}

CS260_SM_TO_INST = {"wavelength": lambda w: w,
                    "grating": lambda g: cs260_sm_to_inst_grating_map[g],
                    "order_sort_filter": lambda osf: cs260_sm_to_inst_osf_map[osf],
                    "shutter": lambda s: "O" if s == "Open" else "Close",
                    "units": lambda u: u}

# lockin mappings #################################################################
SR510_INST_TO_SM = {
    "sensitivity": lambda s: float(s),
    "time_constant": lambda tc: float(tc)
}

SR510_SM_TO_INST = {
    "sensitivity": lambda s: str(s),
    "time_constant": lambda tc: str(tc)
}

SR830_INST_TO_SM = {
    "sensitivity": lambda s: float(s),
    "time_constant": lambda tc: float(tc)
}

SR830_SM_TO_INST = {
    "sensitivity": lambda s: str(s),
    "time_constant": lambda tc: str(tc)
}

# ndf mapping ######################################################################
NDF_INST_TO_SM = {
    "position": lambda p: int(p),
    "error": lambda e: float(e)
}

NDF_SM_TO_INST = {
    "position": lambda p: str(p),
    "error": lambda e: str(e)
}

INST_SM_MAP = {"CS260": CS260_INST_TO_SM,
               "SR510": SR510_INST_TO_SM,
               "SR830": SR830_INST_TO_SM,
               "NDF": NDF_INST_TO_SM}

SM_INST_MAP = {"CS260": CS260_SM_TO_INST,
               "SR510": SR510_SM_TO_INST,
               "SR830": SR830_SM_TO_INST,
               "NDF": NDF_SM_TO_INST}

