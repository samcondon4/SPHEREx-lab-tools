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
        self.data = {'integration_time': None,
                     'storage_path': None,
                     'format': '.csv'
                     }

        self.metadata = {'cryo_temp': True,
                         'power_meter': True,
                         'ndf_wheel': True,
                         'grating': True,
                         'wavelength': True
                         }

        self.monochromator = {'start_wavelength': None,
                              'stop_wavelength': None,
                              'step_size': None,
                              'grating': None,
                              'shutter': None}

        self.lockin = {'time_constant': None,
                        'sensitivity': None,
                        'chop_frequency': None}

        self.labjack = {'sample_frequency': None,
                        'differential': None}

    def reset(self):
        self.integration_time = None
        self.data = {'storage-path': None,
                     'format': None}
        self.monochromator = {'start_wavelength': None,
                              'stop_wavelength': None,
                              'step_size': None,
                              'grating': None}
        self.lockin = {'time_constant': None,
                        'sensitivity': None,
                        'chop_frequency': None}
        self.labjack = {'sample_frequency': None,
                        'differential': False}

    def print_params(self):
        for ikey, idict in self.__dict__.items():
            print(ikey, idict)

#PRIVATE CLASSES: SHOULD NOT BE INSTANTIATED FROM EXTERNAL MODULES###################################################################
class _ControlStep:
    """_ControlStep: Class used to specify a single step of a control loop
    """
    def __init__(self):
        self.integration_time = None
        self.monochromator = {'wavelength': None,
                              'grating': None,
                              'shutter': None}
        self.lockin = {'time_constant': None,
                       'sensitivity': None}
        self.labjack = {'sample_frequency': None,
                        'sample_time': None}

    def print_step(self):
        
        ##PRINT STEP HERE TO ENSURE VALUES ARE POPULATED CORRECTLY!####################
        print("## Control step data #####################################################")
        print("Monochromator data:")
        print(self.monochromator)
        print("Lockin data:")
        print(self.lockin)
        print("Labjack data:")
        print(self.labjack)

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


    #PRIVATE METHODS: These should never be called by higher level software. State-machine code automatically calls these upon entry of each corresponding state#################################
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
        '''on_enter_Thinking: State function that is executed when the state machine enters the 'Thinking' state. This function expects that _next_state_data
                              has been set to a list of ControlLoopParams instances. The function populates the _control_loop attribute after building a 
                              list of _ControlStep instances based on the _next_state_data.

            Parameters:
                None

            Returns:
                None

        '''
        print("Thinking")
        
        self._control_loop.reset()

        for cloop_params in self._next_state_data:
            loop_shutters = None

            ##Get monochromator parameters from control loop params instance#####################
            start_wavelength = float(cloop_params.monochromator['start_wavelength'])
            stop_wavelength = float(cloop_params.monochromator['stop_wavelength'])
            step_size = float(cloop_params.monochromator['step_size'])*1e-3 #multiply by 1e-3 to convert to um.
            grating = float(cloop_params.monochromator['grating'])
            if start_wavelength == stop_wavelength:
                loop_waves = [start_wavelength]
                loop_shutters = [cloop_params.monochromator['shutter']]
            else:
                loop_waves = np.arange(start_wavelength, stop_wavelength + step_size, step_size)

            loop_gratings = grating*np.ones(len(loop_waves))
            ######################################################################################
            
            if loop_shutters == None:
                loop_shutters = ["Open" for w in loop_waves]
            
            cloop = [_ControlStep() for s in range(len(loop_waves))]
            ind = 0
            for step in cloop:
                step.monochromator['wavelength'] = loop_waves[ind]
                step.monochromator['grating'] = loop_gratings[ind]
                step.monochromator['shutter'] = loop_shutters[ind]
                ind += 1

            self._control_loop.loop = self._control_loop.loop + cloop        
        
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







