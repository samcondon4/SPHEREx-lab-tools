import sys
import os
import asyncio
import numpy as np

from pylablib.pylablibsm import SM
from pylablib.utils.parameters import get_params_dict, write_config_file


class ControlLoopParams:
    """ControlLoopParams: Class specifying all information used to build a control loop
    """
    def __init__(self):
        self.integration_time = None
        self.data = {'storage-path': None,
                     'format': None}
        self.monochromator = {'start-wavelength': None,
                              'stop-wavelength': None,
                              'step-size': None,
                              'grating': None}
        self.lock_in = {'time-constant': None,
                        'sensitivity': None,
                        'chop-frequency': None}
        self.labjack = {'sample-frequency': None,
                        'sample-time': None}

    def reset(self):
        self.integration_time = None
        self.data = {'storage-path': None,
                     'format': None}
        self.monochromator = {'start-wavelength': None,
                              'stop-wavelength': None,
                              'step-size': None,
                              'grating': None}
        self.lock_in = {'time-constant': None,
                        'sensitivity': None,
                        'chop-frequency': None}
        self.labjack = {'sample-frequency': None,
                        'sample-time': None}

    def print_params(self):
        print("# Control Loop Parameters ################################################################################################")
        print("Integration Time: {}".format(self.integration_time))
        print("Data: {}".format(self.data))
        print("Monochromator: {}".format(self.monochromator))
        print("Lock-In: {}".format(self.lock_in))
        print("LabJack: {}".format(self.labjack))
        print("##########################################################################################################################")

#PRIVATE CLASSES: SHOULD NOT BE INSTANTIATED FROM EXTERNAL MODULES###################################################################
class _ControlStep:
    """_ControlStep: Class used to specify a single step of a control loop
    """
    def __init__(self):
        self.integration_time = None
        self.monochromator = {'wavelength': None,
                              'grating': None}
        self.lockin = {'time-constant': None,
                       'sensitivity': None}
        self.labjack = {'sample-frequency': None,
                        'sample-time': None}

    def print_step(self):
        pass

class _ControlLoop:
    """ControlLoop: Class with attributes used to store every step of a control loop
    """
    def __init__(self):
        self.data = {'storage-path': None,
                     'format': None}
        self.loop = []

    def reset(self):
        self.data = {'storage-path': None,
                     'format': None}
        self.loop = []
########################################################################################################################################

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
        self._control_loop = _ControlLoop()

        #Default value for next state data is None
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

    def pause(self):
        """pause: pause the currently executing state and enter Waiting until resume is executed
        """
        pass 

    def resume(self):
        """resume: resume execution of paused state.
        """
        pass

    def stop(self):
        """stop: stop any currently executing state and reset state-machine
        """
        pass
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
        while(1):
            #Query instruments
            await asyncio.sleep(0.1)

    def on_enter_Thinking(self):
        print("Thinking")
        

        next_data_type = type(self._next_state_data)
        if(next_data_type is ControlLoopParams):
            
            self._next_state_data.print_params()

            #Populate control loop with monochromator control information
            if self._next_state_data.monochromator['start-wavelength'] == self._next_state_data.monochromator['stop-wavelength']:
                loop_waves = [self._next_state_data.monochromator['start-wavelength']]
            else:
                loop_waves = [np.arange(self._next_state_data.monochromator['start-wavelength'][i], self._next_state_data.monochromator['stop-wavelength'][i],
                                   self._next_state_data.monochromator['step-size'][i]) for i in range(len(self._next_state_data.monochromator['start-wavelength']))]

           
            loop_gratings = [self._next_state_data.monochromator['grating']]
            for i in range(len(loop_gratings)):
                loop_gratings[i] = loop_gratings[i]*np.ones(len(loop_waves))

            #Flatten all control arrays before populating control loops############
            loop_waves = np.array([wave for wave_list in loop_waves for wave in wave_list])
            loop_gratings = np.array([g for g_list in loop_gratings for g in g_list])

            #Initialize control loop
            self._control_loop.reset()
            loop_length = len(loop_waves)
            self._control_loop.loop = [_ControlStep() for step in range(loop_length)]

            ind = 0
            for step in self._control_loop.loop:
                step.monochromator['wavelength'] = loop_waves[ind]
                step.monochromator['grating'] = loop_gratings[ind]


            ##PRINT STEP HERE TO ENSURE VALUES ARE POPULATED CORRECTLY!####################


        else:
            raise TypeError("Control loop cannot be constructed with input of type {}".format(next_data_type))

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







