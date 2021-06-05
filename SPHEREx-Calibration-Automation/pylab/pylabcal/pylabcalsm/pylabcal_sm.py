import sys
import os
import asyncio

from pylablib.pylablibsm import SM
from pylablib.utils.parameters import get_params_dict, write_config_file


class SpectralCalibrationMachine(SM):

    #STATE STATUS INDICATORS##########################
    STATE_IDLE = 0
    STATE_IN_PROGRESS = 1
    STATE_COMPLETE_SUCCESS = 2
    STATE_COMPLETE_FAILURE = 3
    ##################################################

    def __init__(self):
        """__init__: Class initialization. Implements logic of what would be the on_enter_Initializing function
                     but since Initializing is the initial state, on_enter_Initializing is not entered automatically
                     upon startup.
        """
        super().__init__()

        #Private attributes used in instance methods###################################
        self._task_list = []

        #Default value for next state data is None#####################################
        self._next_state_data = None
        ###############################################################################


        #Execute Initializing state function
        self.on_enter_Initializing()

    #PUBLIC FUNCTIONS#################################################################
    def next_state(self, next_state_data=None):
        """next_state: Trigger state-machine transition and update next_state_data
                       field with the passed in value.
        """
        self.kill_tasks()
        self._next_state_data = next_state_data
        self.transition()

    def get_state(self):
        """get_state: Return current state of the state machine

        """
        return self.current_state.identifier

    def get_state_status(self):
        """get_state_status: Return status of the current state

        """
        return SM.StateStatus 
    ##################################################################################


    #PRIVATE METHODS: These should never be called by higher level software. State-machine code automatically calls these###########################################
    def on_enter_Initializing(self):
        print("Initializing")
        SM.StateStatus = SpectralCalibrationMachine.STATE_IN_PROGRESS
        #Connect to all instruments
        SM.StateStatus = SpectralCalibrationMachine.STATE_COMPLETE_SUCCESS

    def on_enter_Waiting(self):
        """on_enter_Waiting: called upon entry of waiting state. Starts waiting asyncronous task.
        """
        print("Waiting")
        wait_task = asyncio.create_task(self.__waiting_async())
        self._task_list.append(wait_task)
        
    async def __waiting_async(self):
        """__waiting_async: asynchronous waiting task. Simply queries instruments to ensure everything is still connected then pends.

        """
        print(self._task_list)
        while(1):
            #Query instruments
            await asyncio.sleep(0.1)

    def on_enter_Thinking(self):
        print("Thinking")
        print(self._task_list)

    def on_enter_Moving(self):
        print("Moving")

    def on_enter_Measuring(self):
        print("Measuring")

    def on_enter_Checking(self):
        print("Checking")

    def on_enter_Compressing(self):
        print("Compressing")

    def on_enter_Writing(self):
        print("Writing")

    def on_enter_Resetting(self):
        print("Resetting")
        super().ControlLoopComplete = True

    def kill_tasks(self):
        """kill_tasks: Kill all running state tasks
        """
        if len(self._task_list) > 0:
            for task in self._task_list:
                task.cancel()
                self._task_list.remove(task)
    ####################################################################################################################################################################


    @staticmethod
    def get_parameters_from_file(config_path):
        # pdb.set_trace()
        params = get_params_dict(config_path)

        return params
