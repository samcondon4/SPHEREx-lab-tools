"""pylabsm_proc_base:

    This module implements a base class for all measurement procedures.
"""


import asyncio
from pymeasure.experiment import Procedure, Worker, Results


class LockinMeasurement(Procedure):

    DATA_COLUMNS = ["Time Stamp", "X Channel Voltage (V.)", "Y Channel Voltage (V.)", "Lia Status Register",
                    "Error Status Register"]

    def __init__(self, lockin):
        self.lockin_instance = lockin
        self.running = False
