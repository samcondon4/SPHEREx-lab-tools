"""pylabsm_spectral:

    This module implements the spectral calibration specific state machine.

"""

# external packages ######################################
import asyncio
from transitions.extensions.asyncio import AsyncMachine
# instrument drivers #####################################
from ..pylabinst.CS260 import CS260
from ..pylabinst.ndfwheel import NDF
from ..pylabinst.labjacku6 import Labjack
from pymeasure.instruments.srs.sr510 import SR510
from pymeasure.instruments.srs.sr830 import SR830
from pymeasure.instruments.thorlabs.thorlabspm100usb import ThorlabsPM100USB

# measurement procedures #####################################
from .pylabsm_procs.lockinProc import LockinMeasurement
from .pylabsm_procs.pm100usbProc import PhotoDiodeMeasurement

# state classes ####################################################################################################
from .pylabsm_states.pylabsm_statesimport import Initializing, Waiting, Manual, Moving, Measuring, Archiving, \
    Indexing, SmCustomState

class SpectralCalibrationMachine(AsyncMachine):

    def __init__(self, data_queue_tx=None, data_queue_rx=None):
        # Instantiate AsyncMachine base class #
        super().__init__(model=self)

        # initialize the communication interface between external code and the states #
        SmCustomState.DataQueueRx = data_queue_rx
        SmCustomState.DataQueueTx = data_queue_tx

        # Action argument attributes #######
        self.meta_dict = {}
        self.ser_index = [0]
        self.seq_index = [0]
        self.moving_dict = {}
        self.control_args = {}
        self.measuring_dict = {}
        self.archiving_dict = {}
        self.manual_or_auto = [""]
        self.control_loop_generate = [True]
        self.control_loop_complete = [False]
        self.tables_dict = {}

        # Instrument classes ##############
        self.inst_dict = {"SR830": SR830(15), "SR510": SR510(6), "CS260": CS260(), "NDF": NDF(), "LABJACK": Labjack(),}
                          #"S401C": ThorlabsPM100USB("USB0::0x1313::0x8072::1912998 ::INSTR")}
        self.inst_dict.pop("LABJACK")
        #self.inst_dict["S401C"].quick_properties_list = ["wavelength"]
        self.inst_dict["SR830"].quick_properties_list = ["time_constant", "sensitivity"]
        self.inst_dict["SR510"].quick_properties_list = ["time_constant", "sensitivity"]

        # Procedure classes ################
        self.proc_dict = {"SR830": LockinMeasurement(self.inst_dict["SR830"]),
                          "SR510": LockinMeasurement(self.inst_dict["SR510"]),}
                          #"S401C": PhotoDiodeMeasurement(self.inst_dict["S401C"])}

        # Initialize action arguments ##########################################################################
        SmCustomState.set_global_args({"Moving": self.moving_dict})
        SmCustomState.set_global_args({"Metadata": self.meta_dict})
        SmCustomState.set_global_args({"Procedures": self.proc_dict})
        SmCustomState.set_global_args({"Control": self.control_args})
        SmCustomState.set_global_args({"Instruments": self.inst_dict})
        SmCustomState.set_global_args({"Series Index": self.ser_index})
        SmCustomState.set_global_args({"Measuring": self.measuring_dict})
        SmCustomState.set_global_args({"Tables": self.tables_dict})
        SmCustomState.set_global_args({"Archiving": self.archiving_dict})
        SmCustomState.set_global_args({"Sequence Index": self.seq_index})
        SmCustomState.set_global_args({"Manual or Auto": self.manual_or_auto})
        SmCustomState.set_global_args({"Control Loop Generate": self.control_loop_generate})
        SmCustomState.set_global_args({"Control Loop Complete": self.control_loop_complete})
        # Configure states and state actions #########################################################################
        # initial state
        self.init_state = Initializing(self, initial=True)
        self.init_state.add_action(self.init_state.initialize_instruments, args=["Instruments"])
        self.init_state.add_action(self.init_state.initialize_sql_server, args=["Tables"])

        self.manual_state = Manual(self)
        self.manual_state.add_action(self.manual_state.manual_action, args=["Control", "Instruments",
                                                                            "Procedures"])

        self.moving_state = Moving(self)
        self.moving_state.add_action(self.moving_state.moving_action, args=["Moving", "Metadata", "Instruments",
                                                                            "Series Index", "Sequence Index",
                                                                            "Control", "Control Loop Generate"])

        self.measuring_state = Measuring(self)
        self.measuring_state.add_action(self.measuring_state.measuring_action, args=["Measuring", "Instruments",
                                                                                     "Procedures", "Metadata",
                                                                                     "Series Index", "Sequence Index",
                                                                                     "Control", "Control Loop Generate",
                                                                                     "Archiving", "Tables"])

        self.archiving_state = Archiving(self)
        self.archiving_state.add_action(self.archiving_state.archiving_action, args=["Archiving", "Tables"])

        self.indexing_state = Indexing(self)
        self.indexing_state.add_action(self.indexing_state.indexing_action, args=["Control Loop Complete", "Moving",
                                                                                  "Series Index", "Sequence Index",
                                                                                  "Control", "Control Loop Generate"])

        # Add all states besides the idle state #################################################
        states = [self.init_state, self.manual_state, self.moving_state, self.measuring_state,
                  self.archiving_state, self.indexing_state]
        self.add_states(states)
        ##########################################################################################

        # Now create and add the idle state to the state machine #########################################
        self.wait_state = Waiting(self, idle=True)
        self.wait_state.add_action(self.wait_state.waiting_action, args=["Manual or Auto", "Control", "Series Index",
                                                                         "Sequence Index", "Moving", "Measuring",
                                                                         "Procedures", "Control Loop Generate",
                                                                         "Archiving", "Tables"])

        self.add_states([self.wait_state])
        ##################################################################################################

        ################################################################################################################

        # Add states and transitions to the state machine ########################################################
        self.init_state.add_transition(self.wait_state)
        self.wait_state.add_transition(self.moving_state, arg="Manual or Auto", arg_result=["auto"])
        self.wait_state.add_transition(self.manual_state, arg="Manual or Auto", arg_result=["manual"])
        self.manual_state.add_transition(self.wait_state)
        self.moving_state.add_transition(self.measuring_state)
        self.measuring_state.add_transition(self.indexing_state)
        self.indexing_state.add_transition(self.moving_state, arg="Control Loop Complete", arg_result=[False])
        self.indexing_state.add_transition(self.archiving_state, arg="Control Loop Complete", arg_result=[True])
        self.archiving_state.add_transition(self.wait_state)
        ###########################################################################################################

    # TODO: Re-write this function for standalone debugging of the state machine
    """
    async def run(self):
        if self.data_queue is None:
            self.data_queue = asyncio.Queue()
            pylabsm_basestate.SmCustomState.set_global_args({"Global Queue": self.data_queue})
        await self.start_machine()
    """


if __name__ == "__main__":
    sm = SpectralCalibrationMachine()
    asyncio.run(sm.run())
