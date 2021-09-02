"""pylabsm_state_auto:

    This module provides the auto state class.

"""

import asyncio
from transitions.extensions.asyncio import AsyncMachine
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Moving(SmCustomState):

    def __init__(self, sm, identifier="moving", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def moving_action(self, move_dict):
        print("Moving instruments in control loop with: {}".format(move_dict))


class AutoDone(SmCustomState):

    def __init__(self, sm, identifier="done", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)


class AutoStateMachine(AsyncMachine):

    def __init__(self):
        super().__init__(model=self)
        # Action argument attributes #
        self.moving_dict = {}
        ##############################

        #Initialize sub state machine action arguments ####
        SmCustomState.set_global_args({"Moving": self.moving_dict})
        ###################################################

        # Configure states and state actions #############################################
        self.moving_state = Moving(self, initial=True)
        self.moving_state.add_action(self.moving_state.moving_action, args=["Moving"])

        self.done_state = AutoDone(self, hold_on_complete=True)
        ##################################################################################

        # Add states and transitions to the auto sub state machine ########
        self.add_states([self.moving_state, self.done_state])
        self.moving_state.add_transition(self.done_state)
        ###################################################################


class Auto(SmCustomState):

    def __init__(self, sm, identifier="auto"):
        super().__init__(sm, self, identifier)

        self.auto_sm = AutoStateMachine()

    async def auto_sm_exec(self, action_arg):
        """Description: pass control loop parameters to the proper states, then wait until the done state is reached
                        before returning

        :param action_arg: (list) input control loop
        :return: None
        """
        control_loop = action_arg["Control"]
        instruments = action_arg["Instruments"]
        auto_sm_task = asyncio.create_task(self.auto_sm.to_moving())
        while not self.auto_sm.state == self.auto_sm.done_state.identifier:
            await asyncio.sleep(0)
        self.auto_sm.done_state.hold_complete = True
