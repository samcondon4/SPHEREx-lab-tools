"""state:

    This module provides a base class for a finite state machine state.

"""

import asyncio
from transitions.extensions.asyncio import AsyncState


# MOVE ACTION BACK TO A DICTIONARY IMPLEMENTATION INSIDE OF THE SMCUSTOMSTATE CLASS ###########################


class Action:
    """
    class to implement state machine actions.
    """
    def __init__(self, func, arg_getter=None, err_flag_setter=None, coro=False):
        """ Description: Initialization for the Action class

        :param func: function object to execute
        :param arg_getter: function object to retrieve arguments to pass to func
        :param err_flag_setter: function to set the error flag of state class
        :param coro: flag to indicate if func is a coroutine
        """
        self.func = func
        self.arg_getter = arg_getter
        self.err_flag_setter = err_flag_setter
        self.coro = coro

    def exec(self):
        """ Description: execute func with the specified arguments
        :return: return value from the action function
        """
        if self.arg_getter is None:
            ret = self.func()
        else:
            func_args = self.arg_getter()
            ret = self.func(func_args)

        if ret is False and self.err_flag_setter is not None:
            self.err_flag_setter()

    async def async_exec(self):
        """ Description: same as exec except func is awaited as a coroutine
        :return: return value from the action function
        """
        if self.arg_getter is None:
            ret = await self.func()
        else:
            func_args = self.arg_getter()
            ret = await self.func(func_args)

        if ret is False and self.err_flag_setter is not None:
            self.err_flag_setter()


class SmCustomState(AsyncState):

    sm = None
    _sm_global_args = {}

    @classmethod
    def set_global_args(cls, arg_dict):
        """ Description: set key/value pairs in the sm_global_args dictionary.

        :param arg_dict: dictionary with key/value pairs to set in the sm_global_args dictionary.
        :return: None
        """
        if cls is SmCustomState:
            for key in arg_dict:
                cls._sm_global_args[key] = arg_dict[key]
        else:
            raise RuntimeError("state global args can only be set at the class level!")

    @classmethod
    def get_global_args(cls, args):
        """ Description: return the value from the arg_name key in sm_global_args

        :param args: key(s) into the sm_global_args dictionary
        :return: dictionary containing all key/value pairs specified by the args parameter.
        """
        if cls is SmCustomState:
            ret = {}
            if args == "All":
                ret = cls._sm_global_args
            elif type(args) is list:
                for key in args:
                    ret[key] = cls._sm_global_args[key]
            elif type(args) is str:
                ret = cls._sm_global_args[args]
        else:
            raise RuntimeError("state global args can only be retrieved at the class level!")

        return ret

    def __init__(self, sm, child, identifier, **kwargs):
        """ Description: initialization for the state base class.

        :param sm: State machine instance that the state is a member of.
        :param child: Subclass instance.
        :param identifier: String used to identify the state within the state machine class.
        """
        if SmCustomState.sm is None:
            SmCustomState.sm = sm
            SmCustomState.sm.add_transition("start_machine", source="initial", dest=identifier)
        self.child = child
        self.identifier = identifier
        super().__init__(identifier, **kwargs)
        self.error_flag = False
        self.error_message = None
        self.coro_actions = {}
        self.actions = {}
        self.transitions = {}

        self.sm.add_transition("error", self.identifier, None, after="error")
        self.add_callback("enter", self.state_exec)

    async def state_exec(self):
        """ Description: Execute all actions that have been added to the state. Transition to the error handler if
                         an error is encountered, otherwise move to the next state.

        :return: None
        """
        self.error_flag = False

        # Execute all state actions #
        await asyncio.create_task(self.action_exec())

        # Enter error handler if an action raised the error_flag else move to next state #
        transition = None
        if self.error_flag:
            transition = self.sm.error
        else:
            for key in self.transitions:
                trans = self.transitions[key]
                if trans["arg"] is None:
                    transition = getattr(self.sm, key)
                else:
                    action_results = SmCustomState.get_global_args(trans["arg"])
                    if action_results == trans["arg_result"]:
                        transition = getattr(self.sm, key)

        if transition is not None:
            await transition()
        else:
            raise RuntimeError("No valid state transition found. State machine stuck!")
        #################################################################################

    async def action_exec(self):
        """Description: Execute the action specified in the actions dictionary with key = action_key.

        :param action_key: (str) key into state actions dictionary
        :return: None
        """
        # Run all coroutines actions ###################################################################################
        coro_args = dict([(key, SmCustomState.get_global_args(self.coro_actions[key]["args"]))
                          for key in self.coro_actions])
        coro_tasks = [asyncio.create_task(self.coro_actions[key]["func"](coro_args[key])) for key in self.coro_actions]
        if len(coro_tasks) > 0:
            await asyncio.wait(coro_tasks)

        # Run all function actions ####################################################################################
        func_args = dict([(key, SmCustomState.get_global_args(self.actions[key]["args"])) for key in self.actions])
        for key in self.actions:
            self.actions[key]["func"](func_args)

    def add_transition(self, next_state, arg=None, arg_result=None, identifier=None):
        """ Description: add a custom state transition to the state machine.

        :param next_state: (SMCustomState) SMCustomState instance to transition to.
        :param arg: (str, list of str) sm_global_args key to base transition logic off. None indicates that this is
                                       an unconditional transition.
        :param arg_result: (varying type) if sm_global_args[arg] == arg_result, then execute the transition.
        :param identifier: (str) string to identify the transition.
        :return:
        """
        if identifier is None:
            trans_key = self.identifier + "_to_" + next_state.identifier
        else:
            trans_key = identifier

        trans_dict = {"next_state": next_state,
                      "arg": arg,
                      "arg_result": arg_result}

        self.sm.add_transition(trans_key, self.identifier, next_state.identifier)
        self.transitions[trans_key] = trans_dict

    def add_action(self, func, identifier=None, args=None):
        """ Description: Add an action dictionary to the state actions dictionary.

        :param func: (function) function object for the action instance.
        :param args: (str, list) string or list of strings identifying which arguments func should take from the
                                 sm_global_args dictionary.
        :param identifier: (str) string to identify the action within the action dictionary.
        :return: None
        """
        if identifier is None:
            identifier = func.__name__
        action_dict = {"func": func, "args": args}
        if asyncio.iscoroutinefunction(func):
            self.coro_actions[identifier] = action_dict
        else:
            self.actions[identifier] = action_dict

    def error(self):
        """ Description: Function that executes either generic error handler, or the handler provided by the child
                         class.
        :return: Whatever the error handler returns
        """
        try:
            self.child.error_handler()
        except AttributeError:
            pass
        else:
            self.error_handler()

    def error_handler(self):
        """ Description: generic error handler for a state machine state.
        """
        print("State {} execution failed!".format(self.identifier))
