from spherexlabtools.parameters import *
from spherexlabtools.procedures import BaseProcedure


class TestProc(BaseProcedure):

    frame_width = IntegerParameter("Frame Width", units="pixels", default=2448)
    frame_height = IntegerParameter("Frame Height", units="pixels", default=2048)
    heater_output = FloatParameter("Heater Output Voltage", units="V.", default=0)


