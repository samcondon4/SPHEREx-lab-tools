"""pylabsm_basestate:

    This module provides a base class for a state within a pytransitions Async finite state machine.

    Note that the mechanism to pass data into a state is via the DataQueueRx name. Data that is placed on this queue
    falls within two categories:

        1) control message strings:
            "pause": when this string is seen on the queue, the running state will pause until "resume" or "abort"
                    is received.
            "resume": resume a paused state.
            "abort": end state execution

        2) control data:
            Any data placed on the DataQueueRx name which is not one of the control message strings is treated as
            control data. The control data that is expected within various states depends on the specific actions executed
            within them.
"""

import asyncio
from transitions.extensions.asyncio import AsyncState


class SmCustomState(AsyncState):

    #SM = None
    DataQueueRx = asyncio.Queue()
    # DataQueueTx may be replaced by an alternative interface by higher level sw.
    DataQueueTx = asyncio.Queue()
    # flag to break from a pend_for_message or pend_for_data call
    ControlMsgStrings = ["pause", "resume", "abort"]

    # reference to idle state
    _idle_id = None

    # private class names
    _sm_global_args = {}
    _running_coros = None
    _initial_state = None


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

    def __init__(self, sm, child, identifier, hold_on_complete=False, initial=False, idle=False, **kwargs):
        """ Description: initialization for the state base class.

        :param sm: State machine instance that the state is a member of.
        :param child: Subclass instance.
        :param identifier: String used to identify the state within the state machine class.
        """
        self.SM = sm
        if initial:
            self.SM.add_transition("start_machine", source="initial", dest=identifier)
        if idle:
            SmCustomState._idle_id = identifier
        self.child = child
        self.identifier = identifier
        kewargs = {}
        for key in kwargs:
            kewargs[key] = kwargs[key]
        if "model" in kewargs:
            kewargs.pop("model")
        super().__init__(identifier, kewargs)
        self.error_flag = False
        self.error_message = None
        self.coro_actions = {}
        self.actions = {}
        self.transitions = {}
        # flags to create a mechanism allowing states to pend at the end of action execution until external software
        # sets the complete flag
        self.hold_complete = hold_on_complete
        self.complete = False

        # boolean to indicate used in conjunction with the pend_for_message and pend_for_data methods
        self.quit_pend = False

        self.SM.add_transition("error", self.identifier, None, after="error")
        self.add_callback("enter", self.state_exec)

    async def pend_for_message(self):
        """ Pend for a control message string to be received on the DataQueueRx name. If control data is seen, then place
            it back on the queue.
        """
        self.quit_pend = False
        msg_rec = False
        msg = None
        while not msg_rec:
            if self.quit_pend:
                msg = None
                break
            if not self.DataQueueRx.empty():
                msg = self.DataQueueRx.get_nowait()
                if msg not in self.ControlMsgStrings:
                    self.DataQueueRx.put_nowait(msg)
                else:
                    msg_rec = True

            await asyncio.sleep(0)

        return msg

    async def pend_for_data(self):
        """ Pend for control data to be received on the DataQueueRx name. If a control message string is seen, then
            place it back on the queue.
        """
        self.quit_pend = False
        data_rec = False
        data = None
        while not data_rec:
            if self.quit_pend:
                data = None
                break
            if not self.DataQueueRx.empty():
                data = self.DataQueueRx.get_nowait()
                if data in self.ControlMsgStrings:
                    self.DataQueueRx.put_nowait(data)
                else:
                    data_rec = True

            await asyncio.sleep(0)

        return data

    async def state_exec(self):
        """ Description: Execute all actions that have been added to the state. Transition to the error handler if
                         an error is encountered, otherwise move to the next state.

        :return: None
        """
        self.error_flag = False

        # Execute all state actions #################################
        print("## START {} ##".format(self.identifier.upper()))
        asyncio.create_task(self.action_exec())
        # pend for an abort or pause message to be received, or for the actions to complete execution
        msg = await self.pend_for_message()
        print("MESSAGE RECEIVED = {}".format(msg))
        # Enter error handler if an action raised the error_flag else move to next state #
        if msg is None:
            transition = None
            if self.error_flag:
                transition = self.SM.error
            else:
                for key in self.transitions:
                    trans = self.transitions[key]
                    if trans["arg"] is None:
                        transition = getattr(self.SM, key)
                    else:
                        action_results = SmCustomState.get_global_args(trans["arg"])
                        if action_results == trans["arg_result"]:
                            transition = getattr(self.SM, key)

            print("## END {} ##".format(self.identifier.upper()))
            if transition is not None:
                await transition()
            elif self.hold_complete:
                while not self.complete:
                    await asyncio.sleep(0)
            else:
                raise RuntimeError("No valid state transition found. State machine stuck!")
            #################################################################################

        # kill all running coroutines and threads and transition to the idle state
        # TODO: log and kill all threads
        elif msg == "abort":
            print("Abort message received!")
            try:
                for coro in self._running_coros:
                    coro.cancel()
                await self.SM.enter_idle()
            except Exception as e:
                print(e)

    async def action_exec(self):
        """Description: Execute the action specified in the actions dictionary with key = action_key.

        :return: None
        """
        # Run all coroutines actions ###################################################################################
        coro_args = dict([(key, SmCustomState.get_global_args(self.coro_actions[key]["args"]))
                          for key in self.coro_actions])
        self._running_coros = [asyncio.create_task(self.coro_actions[key]["func"](coro_args[key]))
                            for key in self.coro_actions]
        if len(self._running_coros) > 0:
            await asyncio.wait(self._running_coros)

        # Run all function actions ####################################################################################
        func_args = dict([(key, SmCustomState.get_global_args(self.actions[key]["args"])) for key in self.actions])
        for key in self.actions:
            self.actions[key]["func"](func_args[key])

        # clear the quit pend flag so that the state_exec message pend will move on
        self.quit_pend = True

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

        self.SM.add_transition(trans_key, self.identifier, next_state.identifier)
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

    def set_as_idle(self):
        """Set this state instance as the idle state of the state machine.
        """
        self.SM.add_transition("enter_idle", "*", self.identifier)

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
