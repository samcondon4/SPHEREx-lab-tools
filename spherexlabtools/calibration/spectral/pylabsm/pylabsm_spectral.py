"""pylabsm_spectral:

    This module implements the spectral calibration specific state machine.

"""

# external packages ######################################
import asyncio
from transitions.extensions.asyncio import AsyncMachine
# instrument drivers #####################################
from pylabinst.CS260 import CS260
from pylabinst.ndfwheel import NDF
from pylabinst.labjacku6 import Labjack
from pymeasure.instruments.srs.sr510 import SR510
from pymeasure.instruments.srs.sr830 import SR830
from pymeasure.instruments.thorlabs.thorlabspm100usb import ThorlabsPM100USB

# measurement procedures #####################################
from pylabsm.pylabsm_procs.lockinProc import LockinMeasurement
from pylabsm.pylabsm_procs.pm100usbProc import PhotoDiodeMeasurement

# state classes ####################################################################################################
from pylabsm.pylabsm_states.pylabsm_statesimport import pylabsm_state_initializing, pylabsm_state_waiting, \
    pylabsm_state_manual, pylabsm_state_moving, pylabsm_state_measuring, pylabsm_state_indexing, pylabsm_basestate


class SpectralCalibrationMachine(AsyncMachine):

    def __init__(self, data_queue_tx=None, data_queue_rx=None):
        # Instantiate AsyncMachine base class #
        super().__init__(model=self)

        # initialize the communication interface between external code and the states #
        pylabsm_basestate.SmCustomState.DataQueueRx = data_queue_rx
        pylabsm_basestate.SmCustomState.DataQueueTx = data_queue_tx

        # Action argument attributes #######
        self.meta_dict = {}
        self.ser_index = [0]
        self.seq_index = [0]
        self.moving_dict = {}
        self.control_args = {}
        self.measuring_dict = {}
        self.manual_or_auto = [""]
        self.control_loop_generate = [True]
        self.control_loop_complete = [False]

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
        pylabsm_basestate.SmCustomState.set_global_args({"Moving": self.moving_dict})
        pylabsm_basestate.SmCustomState.set_global_args({"Metadata": self.meta_dict})
        pylabsm_basestate.SmCustomState.set_global_args({"Procedures": self.proc_dict})
        pylabsm_basestate.SmCustomState.set_global_args({"Control": self.control_args})
        pylabsm_basestate.SmCustomState.set_global_args({"Instruments": self.inst_dict})
        pylabsm_basestate.SmCustomState.set_global_args({"Series Index": self.ser_index})
        pylabsm_basestate.SmCustomState.set_global_args({"Measuring": self.measuring_dict})
        pylabsm_basestate.SmCustomState.set_global_args({"Sequence Index": self.seq_index})
        pylabsm_basestate.SmCustomState.set_global_args({"Manual or Auto": self.manual_or_auto})
        pylabsm_basestate.SmCustomState.set_global_args({"Control Loop Generate": self.control_loop_generate})
        pylabsm_basestate.SmCustomState.set_global_args({"Control Loop Complete": self.control_loop_complete})
        # Configure states and state actions #########################################################################
        # initial state
        self.init_state = pylabsm_state_initializing.Initializing(self, initial=True)
        self.init_state.add_action(self.init_state.initialize_instruments, args=["Instruments"])

        self.manual_state = pylabsm_state_manual.Manual(self)
        self.manual_state.add_action(self.manual_state.manual_action, args=["Control", "Instruments",
                                                                            "Procedures"])

        self.moving_state = pylabsm_state_moving.Moving(self)
        self.moving_state.add_action(self.moving_state.moving_action, args=["Moving", "Metadata", "Instruments",
                                                                            "Series Index", "Sequence Index",
                                                                            "Control", "Control Loop Generate"])

        self.measuring_state = pylabsm_state_measuring.Measuring(self)
        self.measuring_state.add_action(self.measuring_state.measuring_action, args=["Measuring", "Instruments",
                                                                                     "Procedures", "Metadata",
                                                                                     "Series Index", "Sequence Index",
                                                                                     "Control", "Control Loop Generate"
                                                                                     ])

        self.indexing_state = pylabsm_state_indexing.Indexing(self)
        self.indexing_state.add_action(self.indexing_state.indexing_action, args=["Control Loop Complete", "Moving",
                                                                                  "Series Index", "Sequence Index",
                                                                                  "Control", "Control Loop Generate"])

        # Add all states besides the idle state #################################################
        states = [self.init_state, self.manual_state, self.moving_state, self.measuring_state,
                  self.indexing_state]
        self.add_states(states)
        ##########################################################################################

        # Now create and add the idle state to the state machine #########################################
        self.wait_state = pylabsm_state_waiting.Waiting(self, idle=True)
        self.wait_state.add_action(self.wait_state.waiting_action, args=["Manual or Auto", "Control", "Series Index",
                                                                         "Sequence Index", "Moving", "Measuring",
                                                                         "Procedures", "Control Loop Generate"])

        self.add_states([self.wait_state])
        ##################################################################################################

        ################################################################################################################

        # Add states and transitions to the state machine ########################################################
        self.init_state.add_transition(self.wait_state)
        #self.wait_state.add_transition(self.moving_state, arg="Manual or Auto", arg_result=["auto"])
        #self.wait_state.add_transition(self.manual_state, arg="Manual or Auto", arg_result=["manual"])
        #self.manual_state.add_transition(self.wait_state)
        #self.moving_state.add_transition(self.measuring_state)
        #self.measuring_state.add_transition(self.indexing_state)
        #self.indexing_state.add_transition(self.wait_state, arg="Control Loop Complete", arg_result=[True])
        #self.indexing_state.add_transition(self.moving_state, arg="Control Loop Complete", arg_result=[False])
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
