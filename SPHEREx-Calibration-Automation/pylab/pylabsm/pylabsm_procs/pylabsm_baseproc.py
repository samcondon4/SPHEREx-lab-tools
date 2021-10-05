"""pylabsm_baseproc:

    This provides a base procedure
"""

from pymeasure.experiment import Procedure, Worker, Results, FloatParameter

class SmBaseProc(Procedure):

    def __init__(self, lockin_instance):

        self._timestamp_method = lambda: str(datetime.datetime.now())

        super().__init__()