"""pylablibsm_test: This file provides an example of using the calibration automation state-machine API

    Sam Condon, 06/14/2021
"""
import numpy as np
from pylablibsm import SM


def init_action():
    print("This is the function that initializes communication interfaces with all instruments.")


def waiting_action():
    print("Here we are waiting for user input.")
    print("*Query instruments for lost connections*")


def thinking_action(wave_dict):
    """thinking_action: This funtion generates the control loop parameters based on the user input dictionary
                        of the following form:

                        {'start_wave': float, 'stop_wave': float, 'step_wave': float}
    """
    print("This is the thinking action that generates the control loop parameters based on user input")
    waves = np.arange(wave_dict['start_wave'], wave_dict['stop_wave'], wave_dict['step_wave'])
    print(waves)


# Create state-machine instance. Note that if any initialization action needs to be taken, this action must be passed
# in through the state machine constructor
state_machine = SM(init_action, 'Calibration automation initialization')

# Add all desired actions to the state-machine###########################
state_machine.add_action('Waiting', 'waiting_action_0', waiting_action)
state_machine.add_action('Thinking', 'cloop gen', thinking_action)

# After we have instantiated the state-machine and added all actions to the machine, invoke the first transition from
# Initializing to Waiting
state_machine.transition()

thinking_params = {'start_wave': 0.7, 'stop_wave': 3.5, 'step_wave': 0.1}
state_machine.add_params_to_queue('Thinking', 'cloop gen', thinking_params)

#Now transition to thinking
state_machine.transition()

#and so on and so forth........
