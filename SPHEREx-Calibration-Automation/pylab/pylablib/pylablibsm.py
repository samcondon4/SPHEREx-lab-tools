import asyncio
from inspect import signature
from transitions import Machine


class SM:
    states = ['Initializing', 'Waiting', 'Thinking', 'Moving', 'Measuring', 'Checking',
              'Compressing', 'Writing', 'Resetting', 'Troubleshooting']

    control_loop_states = ['Moving', 'Measuring', 'Checking', 'Compressing', 'Writing',
                           'Resetting']

    def __init__(self):

        self.machine = Machine(model=self, states=SM.states, initial='Initializing')

        # Define Transitions########################################################################
        # Core Transitions
        self.machine.add_transition(trigger='init_to_wait', source='Initializing', dest='Waiting')
        self.machine.add_transition('wait_to_think', 'Waiting', 'Thinking')

        # Control loop transition cycle #
        self.machine.add_transition('start_control_loop', 'Thinking', 'Moving')
        self.machine.add_transition('control_loop_next', 'Moving', 'Measuring')
        self.machine.add_transition('control_loop_next', 'Measuring', 'Checking')
        self.machine.add_transition('control_loop_next', 'Checking', 'Compressing')
        self.machine.add_transition('control_loop_next', 'Compressing', 'Writing')
        self.machine.add_transition('control_loop_next', 'Writing', 'Resetting')
        self.machine.add_transition('control_loop_next', 'Resetting', 'Moving')

        # Control loop complete transitions
        self.machine.add_transition('control_loop_complete', SM.control_loop_states, 'Waiting')

        # Error transitions
        self.machine.add_transition('to_trouble', '*', 'Troubleshooting')
        self.machine.add_transition('trouble_to_init', 'Troubleshooting', 'Initializing')
        self.machine.add_transition('trouble_to_wait', 'Troubleshooting', 'Waiting')
        self.machine.add_transition('trouble_to_think', 'Troubleshooting', 'Thinking')
        self.machine.add_transition('trouble_to_move', 'Troubleshooting', 'Moving')
        self.machine.add_transition('trouble_to_measure', 'Troubleshooting', 'Measuring')
        self.machine.add_transition('trouble_to_check', 'Troubleshooting', 'Checking')
        self.machine.add_transition('trouble_to_compress', 'Troubleshooting', 'Compressing')
        self.machine.add_transition('trouble_to_reset', 'Troubleshooting', 'Resetting')
        ##########################################################################################

        # STATE ACTION AND PARAMETER DICTIONARIES####################################################################
        # Actions#######################################
        # Action dictionaries take the following form:
        # key = <action name string>: {'action': <function>, 'takes_params': <boolean>, 'coro': <boolean>}
        self.state_actions = {'Initializing': {}, 'Waiting': {}, 'Thinking': {}, 'Moving': {},
                              'Measuring': {}, 'Checking': {}, 'Compressing': {}, 'Writing': {},
                              'Resetting': {}, 'Troubleshooting': {}}

        # Parameters#######################################
        # Parameter dictionaries take the following form:
        # key = <action name string>: <parameter dictionary>
        self.state_params = {'Initializing': {}, 'Waiting': {}, 'Thinking': {}, 'Moving': {},
                             'Measuring': {}, 'Checking': {}, 'Compressing': {}, 'Writing': {},
                             'Resetting': {}, 'Troubleshooting': {}}

        # Return data############################
        # Return data dictionaries take the following form:
        # key = <action name string>: <return data of varying type>
        self.state_ret_data = {'Initializing': {}, 'Waiting': {}, 'Thinking': {}, 'Moving': {},
                               'Measuring': {}, 'Checking': {}, 'Compressing': {}, 'Writing': {},
                               'Resetting': {}, 'Troubleshooting': {}}

        ###############################################################################################################

    def start_machine(self):
        """start_machine: Upon first instantiation, the state machine will not execute the Initializing state
                      function. This method is used to start the state machine by running the Initializing
                      state function.
        """
        if self.state == 'Initializing':
            self.on_enter_Initializing()
        else:
            raise RunTimeError(
                "Cannot execute Initializing state actions from state: {}".format(self.state))

    def add_action_to_state(self, state, action_name, action, coro=False):
        """add_action_to_state: Add a function that gets called in the specified state, 'state' when 'action_name'
                             is encountered in the state parameters dict.

            Parameters:
                state: command loop state where action should be run.
                action_name: name of the action to be run
                action: function pointer to be called when action should be run
                async_action: boolean to indicate if passed action is an asyncio coroutine
        """
        action_takes_params = len(signature(action).parameters) > 0
        action_dict = {'action': action, 'takes_params': action_takes_params, 'coro': coro}
        self.state_actions[state][action_name] = action_dict

    def remove_action_from_state(self, state, action_name):
        """remove_action_from_state: Remove previously added function from the control loop state, 'state' named 'action_name'

            Parameters:
                state: command loop state where action should be removed.
                action_name: name of previously added action to be removed.
        """
        self.state_actions[state][action_name].pop()

    def clear_actions(self, state='All'):
        """clear_cloop_actions: Clear all actions from a state, 'state.' Or if 'state' is set to 'All', clear all actions from all states.

            state: Specify which state actions should be cleared from. 'All' clears all actions from all states.
        """
        if state == 'All':
            for key in self.state_actions:
                self.state_actions[key] = {}
        else:
            self.state_actions[state] = {}

    def set_action_parameters(self, state, action_name, params_dict):
        """set_parameters_to_action: Add a parameters dictionary 'params_dict' to the queue to be passed to the action
                                      named 'action_name' which has been added to the appropriate state action dictionary.

                                      Adds a dictionary to the specified state parameters queue with the following form:
                                      {'action_name': action_name, 'params': params_dict}

            Params:
                state: state parameters dictionary to add params_dict to
                params_dict_name: name of dictionary. This will be the key of the dictionary that is added to the state
                                  parameters dictionary
                params_dict: dictionary of control loop parameters

            Returns:
                None
        """
        self.state_params[state][action_name] = params_dict

    def get_state_action_data(self, state):
        """get_state_action_data: Return the dictionary of data that has been returned from all actions executed within the specified state.
                                  After calling this function the state return data dictionary is reset.

            Params:
                state: state that the action return data dictionary should be returned from.

            Returns:
                Dictionary of state action return data. The returned dictionary is of the following form:
                    {<action name string>: <data>}
        """
        return self.state_ret_data[state]

    # STATE EXECUTION METHODS###############################################################

    def on_enter_Initializing(self):
        print("Initializing")
        asyncio.create_task(self._state_exec('Initializing'))

    def on_enter_Waiting(self):
        print("Waiting")
        asyncio.create_task(self._state_exec('Waiting'))

    def on_enter_Thinking(self):
        print("Thinking")
        asyncio.create_task(self._state_exec('Thinking'))

    def on_enter_Moving(self):
        print("Moving")
        asyncio.create_task(self._state_exec('Moving'))

    def on_enter_Measuring(self):
        print("Measuring")
        asyncio.create_task(self._state_exec('Measuring'))

    def on_enter_Checking(self):
        print("Checking")
        asyncio.create_task(self._state_exec('Checking'))

    def on_enter_Compressing(self):
        print("Compressing")
        asyncio.create_task(self._state_exec('Compressing'))

    def on_enter_Writing(self):
        print("Writing")
        asyncio.create_task(self._state_exec('Writing'))

    def on_enter_Resetting(self):
        print("Resetting")
        asyncio.create_task(self._state_exec('Resetting'))

    def on_enter_Troubleshooting(self):
        print("Troubleshooting")
        asyncio.create_task(self._state_exec('Troubleshooting'))

    async def _state_exec(self, state_id):

        for action_key in self.state_actions[state_id]:

            # Get next action
            action = self.state_actions[state_id][action_key]
            action_ret = None

            #Dictionary with state machine instance and action parameters
            act_dict = {'state_machine': self, 'params': None}

            if action['takes_params']:
                try:
                    act_dict['params'] = self.state_params[state_id][action_key]
                except KeyError:
                    pass

            # Execute action as either a coroutine or normal function
            if action['coro']:
                action_task = asyncio.create_task(action['action'](act_dict))
                await action_task
                action_ret = action_task.result()
            else:
                action_ret = action['action'](act_dict)

            # Save any returned action data
            self.state_ret_data[state_id][action_key] = action_ret
    #######################################################################################
