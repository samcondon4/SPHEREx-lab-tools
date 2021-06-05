import sys
from statemachine import State, StateMachine


class SM(StateMachine):
    """SM: This class defines the state-machine framework used for the SPHEREx Test and Calibration Lab control
           software
    """
    # Define States##########################################
    Initializing = State('Initializing', initial=True)
    Waiting = State('Waiting')
    Thinking = State('Thinking')
    Moving = State('Moving')
    Measuring = State('Measuring')
    Checking = State('Checking')
    Compressing = State('Compressing')
    Writing = State('Writing')
    Resetting = State('Resetting')
    Troubleshooting = State('Troubleshooting')
    ##########################################################
    
    #STATE STATUS INDICATORS##########################
    STATE_IDLE = 0
    STATE_IN_PROGRESS = 1
    STATE_COMPLETE_SUCCESS = 2
    STATE_COMPLETE_FAILURE = 3
    ##################################################

    # Flag to indicate successful completion of a state#######
    StateStatus = STATE_IDLE
    ##########################################################

    # Define Control Loop states##############################################################
    ControlLoop = ['Moving', 'Measuring', 'Checking', 'Compressing', 'Writing', 'Resetting']
    ##########################################################################################

    # Flag to indicate completion of control loop###
    ControlLoopComplete = False
    ################################################

    # State identifier to keep record of previous state##########################
    PrevState = None
    #############################################################################

    # Define Transitions###############################################################################################
    # Core transitions:
    init_to_wait = Initializing.to(Waiting)
    wait_to_think = Waiting.to(Thinking)
    think_to_move = Thinking.to(Moving)

    # Control loop transition cycle:
    control_loop_next = Moving.to(Measuring) | Measuring.to(Checking) | Checking.to(Compressing) | \
                        Compressing.to(Writing) | Writing.to(Resetting) | Resetting.to(Moving)

    # Control loop complete transitions:
    control_loop_complete = Moving.to(Waiting) | Measuring.to(Waiting) | Checking.to(Waiting) | \
                            Compressing.to(Waiting) | Writing.to(Waiting) | Resetting.to(Waiting)

    # Error transitions:
    init_to_trouble = Initializing.to(Troubleshooting)
    trouble_to_init = Troubleshooting.to(Initializing)

    wait_to_trouble = Waiting.to(Troubleshooting)
    trouble_to_wait = Troubleshooting.to(Waiting)

    think_to_trouble = Thinking.to(Troubleshooting)
    trouble_to_think = Troubleshooting.to(Thinking)

    control_loop_to_trouble = Moving.to(Troubleshooting) | Measuring.to(Troubleshooting) | Checking.to(Troubleshooting) \
                              | Compressing.to(Troubleshooting) | Writing.to(Troubleshooting) | \
                              Resetting.to(Troubleshooting)

    trouble_to_move = Troubleshooting.to(Moving)
    trouble_to_measure = Troubleshooting.to(Measuring)
    trouble_to_check = Troubleshooting.to(Checking)
    trouble_to_compress = Troubleshooting.to(Compressing)
    trouble_to_reset = Troubleshooting.to(Resetting)
    ####################################################################################################################

    def ret_state(self):
        return self.current_state

    def transition(self):
        """transition: implements next state transition logic

        :return: None
        """
        cur_state_id = self.current_state.identifier
        SM.PrevState = cur_state_id
        if cur_state_id == 'Initializing' and self.StateStatus == SM.STATE_COMPLETE_SUCCESS:
            self.init_to_wait()

        elif cur_state_id == 'Initializing' and self.StateStatus is False:
            self.init_to_trouble()

        elif cur_state_id == 'Waiting' and self.StateStatus == SM.STATE_COMPLETE_SUCCESS:
            self.wait_to_think()

        elif cur_state_id == 'Waiting' and self.StateStatus is False:
            self.wait_to_trouble()

        elif cur_state_id == 'Thinking' and self.StateStatus == SM.STATE_COMPLETE_SUCCESS:
            self.think_to_move()

        elif cur_state_id in self.ControlLoop and self.StateStatus == SM.STATE_COMPLETE_SUCCESS and self.ControlLoopComplete is False:
            self.control_loop_next()

        elif cur_state_id in self.ControlLoop and self.StateStatus == SM.STATE_COMPLETE_SUCCESS and self.ControlLoopComplete == SM.STATE_COMPLETE_SUCCESS:
            self.control_loop_complete()

        elif cur_state_id in self.ControlLoop and self.StateStatus is False:
            self.control_loop_to_trouble()


