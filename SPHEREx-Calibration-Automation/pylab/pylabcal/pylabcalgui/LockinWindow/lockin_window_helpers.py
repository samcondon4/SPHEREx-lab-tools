from PyQt5 import QtCore


# CONSTANTS ####################################################################################
QtUNCHECKED = QtCore.Qt.Unchecked
QtCHECKED = QtCore.Qt.Checked
QtFULL_MATCH = QtCore.Qt.MatchExactly
SEQUENCE_ROLE = 0

LOCKIN_UNIT_SENSITIVITY_MAP = {"V.": 1, "mV.": 1e-3, "uV.": 1e-6, "nV.": 1e-9}
LOCKIN_UNIT_TC_MAP = {"ks.": 1e3, "s.": 1, "ms.": 1e-3, "us.": 1e-6}
LOCKIN_TC_MOD_MAP = {1: 0, 0: 3}
LOCKIN_TC_MULT_UNIT_MAP = {1e-6: ("x1", "us."), 1e-5: ("x10", "us."), 1e-4: ("x100", "us."),
                           1e-3: ("x1", "ms."), 1e-2: ("x10", "ms."), 1e-1: ("x100", "ms."),
                           1: ("x1", "s."), 1e1: ("x10", "s."), 1e2: ("x100", "s."),
                           1e3: ("x1", "ks.")}
LOCKIN_SENS_MOD_MAP = {0: 5, 1: 1, 2: 2}
LOCKIN_SENS_MULT_UNIT_MAP = {1e-9: ("x1", "nV."), 1e-8: ("x10", "nV."), 1e-7: ("x100", "nV."),
                             1e-6: ("x1", "uV."), 1e-5: ("x10", "uV."), 1e-4: ("x100", "uV."),
                             1e-3: ("x1", "mV."), 1e-2: ("x10", "mV."), 1e-1: ("x100", "mV."),
                             1: ("x1", "V.")}
LOCKIN_FS = [float(2**i) for i in range(-4, 10)]
################################################################################################
