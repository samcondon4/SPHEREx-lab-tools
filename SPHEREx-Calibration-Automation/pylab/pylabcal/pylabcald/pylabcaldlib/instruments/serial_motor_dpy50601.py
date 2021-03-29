import serial
from serial import rs485
import serial
from serial import rs485
from serial.tools import list_ports
import asyncio


class DPY50601:
    ##CLASS VARIABLES, SHARED BETWEEN ALL INSTANCES#######################################
    '''_cmd_dict:
        Dictionary of ASCII commands to send to motor controller.
        Intended for use inside methods in conjunction w/ _get_cmd_bytes.

        Example: To update motor's maximum speed inside of a method use:

        DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_MAX_SPEED', id, speed))

        NOT INTENDED FOR USE BY EXTERNAL USER OF THIS CLASS
    '''
    _cmd_dict = {
        'SET_ACCELERATION': '@{}A{}\r',
        'SET_BASE_SPEED': '@{}B{}\r',
        'GO_N_STEPS': '@{}G\r',
        'MOVE_TO': '@{}P{}\r',
        'SET_N_STEPS': '@{}N{}\r',
        'HOME': '@{}H{}\r',
        'ENCD_AUTO': '@{}EA{}\r',
        'ENCD_DELAY': '@{}ED{}\r',
        'ENCD_MOT_RATIO': '@{}EM{}\r',
        'ENCD_RETRIES': '@{}ER{}\r',
        'ENCD_RST': '@{}ET\r',
        'ENCD_WINDOW': '@{}EW{}\r',
        'READ_ALL_INPUTS': '@{}IR\r',
        'READ_INPUT': '@{}I{}\r',
        'SET_MAX_SPEED': '@{}M{}\r',
        'SLEW': '@{}S\r',
        'VERIFY': '@{}V{}\r',
        'SET_POS': '@{}Z{}\r',
        'READ_ERR_REG': '@{}!\r',
        'READ_VERS_REG': '@{}$\r',
        'READ_ADDR_REG': '@{}%\r',
        'SET_DIR_CW': '@{}+\r',
        'SET_DIR_CCW': '@{}-\r',
        'STOP': '@{}.\r',
        'SET_ADDR_REG': '@{}~{}\r',
        'SET_OUTPUT': '@{}OR{}\r'
    }

    '''_ser:
       Serial COM port to be shared between multiple instances of the DPY50601 class. 

       NOT INTENDED FOR USE BY EXTERNAL USER OF THIS CLASS
    '''
    _ser = None

    #######################################################################################

    ##CLASS METHODS#############################################################################################

    @classmethod
    def _open_serial(cls):
        '''_open_serial:

            This method is intended to be used internally when the first DPY50601 instance is created. It iterates
            through the list of available COM ports and finds the port associated the motor id 0. If this port is
            located successfully, then this method sets the '_ser' class variable. This variable is shared between
            all instances of this class so each motor controller instance can be accessed through the same serial
            COM port

            NOT INTENDED FOR USE BY EXTERNAL USER OF THIS CLASS
        '''
        readval = 0
        com_est = 0  # communication established?
        ports = list_ports.comports()
        for p in ports:
            try:
                ser = serial.Serial(p.name, 38400, xonxoff=True, timeout=0.2, write_timeout=0.5)
                ser.rs485_mode = serial.rs485.RS485Settings()
                ser.write(cls._get_cmd_bytes('READ_VERS_REG', 0))

            except Exception as e:
                print("Exception on {}: {}".format(p.name, e))
                if ser.is_open:
                    ser.close()
            else:
                readval = ser.read(30)
                if b'SMC60' in readval:
                    print('Found DPY50601 COM at: {}'.format(p.name))
                    cls._ser = ser
                    com_est = 1
                    break
                else:
                    ser.close()

        return com_est

    @classmethod
    def _get_cmd_bytes(cls, cmdstr, cid, value=None):
        '''_get_cmd_bytes:

            This method returns the ASCII byte string to be sent to the DPY50601 motor controller.

            Parameters
                1) cmdstr: String specifying which command should be executed. This should be a key
                           to the _cmd_dict dictionary.

                2) cid: ID of the motor controller that the command should be addressed to.

                3) value: Associated value to send with command. This is only valid for controller
                          commands that take an argument. For instance, with the 'MAX_SPEED' command,
                          a value specifying the maximum speed value should be sent. On the contrary,
                          the 'READ_ERR_REG' command takes no arguments, so 'value' should not be set.

            Returns
                byte string that can be directly sent through the open COM port to the motor controller(s)


            NOT INTENDED FOR USE BY EXTERNAL USER OF THIS CLASS
        '''

        return bytes(cls._cmd_dict[cmdstr].format(cid, value), 'utf-8')

    ###########################################################################################################

    ##CONSTRUCTOR###########################################################################
    def __init__(self, motor_id, encoder_motor_ratio=8):

        ##Instance Variables
        self.id = motor_id
        self.encoder_delay = 500
        self.encoder_motor_ratio = encoder_motor_ratio #check this
        self.encoder_retries = 5
        self.encoder_window = self.encoder_motor_ratio
        self.com_est = 0  # communication established?
        self.pos = 0
        self.prev_pos = 0
        self.enc_pos = 0
        self.prev_enc_pos = 0
        self.err_code = 0


        ##If DPY50601 serial COM port hasn't been opened, then open it. Otherwise, ping controller
        ##at specified ID through the open port.
        if DPY50601._ser is None:
            self.com_est = DPY50601._open_serial()
        else:
            DPY50601._ser.write(DPY50601._get_cmd_bytes('READ_VERS_REG', self.id))
            readval = DPY50601._ser.read(30)
            if b'SMC60' in readval:
                self.com_est = 1

        # Check if communication has been successfully established, perform other initializations if so
        if self.com_est == 1:
            print('DPY50601-{} communication established at {}'.format(self.id, DPY50601._ser.name))
            DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_MOT_RATIO', self.id, self.encoder_motor_ratio))
            DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_DELAY', self.id, self.encoder_delay))
            DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_RETRIES', self.id, self.encoder_retries))
            DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_WINDOW', self.id, self.encoder_window))
            #encoder auto correct disabled by default
            DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_AUTO', self.id, 0))
            # Read initial motor stage position
            self.pos = self.get_pos()
            self.prev_pos = self.pos
            self.enc_pos = self.get_encoderpos()
            self.prev_enc_pos = self.enc_pos
            # Pull all controller outputs to ground by default
            self.set_output(255)
        else:
            print("DPY50601 Controller at ID {} not found...".format(self.id))

    #########################################################################################

    ##Instance Methods###################################################################################

    def move_to(self, pos, auto_cor=False):
        '''move_to: move to specified absolute position. For defined results, this should only be called
                    after an appropriate homing operation has been performed.

        :param pos: Position to move to. Range is -8388607 - +8388607
               auto_cor: (optional) enable encoder auto correct functionality
        :return: success/failure code
        '''

        move_success = 0
        if auto_cor:
            DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_AUTO', self.id, 1))
            print("Auto-correct enabled")
        else:
            DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_AUTO', self.id, 0))
        #Switch to home- input
        self.set_output(4)
        DPY50601._ser.write(DPY50601._get_cmd_bytes('MOVE_TO', self.id, pos))
        DPY50601._ser.write(DPY50601._get_cmd_bytes('GO_N_STEPS', self.id))

    async def step_async(self, n, direction, interval=0.5, timeout=5):
        '''step:

        Wrapper to step() to run success/failure check of step() operation in
        an asynio concurrent context.

        Parameters
            1) n: number of steps to move motor
            2) direction: 0 moves motor counter-clockwise, 1 moves motor clockwise
            3) interval: amount of time in between successive controller status reads
            4) timeout: number of idle controller status reads to detect before timing out

        Return
            success/failure code. 1 indicates a successful step operation, 0 indicates
            failed step operation.
        '''

        move_success = 1
        timeout_cnt = 0

        # Make sure a valid direction specifier was provided
        if not (direction == 0 or direction == 1):
            print("Please specify valid direction specifier: (0) for ccw, (1) for cw.")
            move_success = 0

        #Calculate destination in encoder counts and make sure we are within allowable movement range#################
        mult = (-2 * direction) + 1
        dest = self.enc_pos + (self.encoder_motor_ratio*mult* n)
        ##############################################################################################################

        if mult < 0:
            self.step(n, 1)
        else:
            self.step(n, 0)

        while abs(self.enc_pos - dest) >= self.encoder_motor_ratio:
            self.get_encoderpos()
            self.get_err(stop=True)
            if self.err_code != 0:
                move_success = 0
                break
            if self.prev_enc_pos == self.enc_pos:
                timeout_cnt += 1
                if timeout_cnt == timeout:
                    raise TimeoutError('Controller timeout. Limit switch pressed?')
                    move_success = 0
                    break
                n = (self.enc_pos - dest) // self.encoder_motor_ratio
                print("Stage correction value = {}".format(n))
                print(self.enc_pos - dest)
                if n < 0:
                    self.step(-1*n, 0)
                elif n > 0:
                    self.step(n, 1)
            await asyncio.sleep(interval)
        #########################################################################################################

        return move_success

    def step(self, n, direction):
        '''step:

        Sends command to move stepper motor 'n' steps in specified direction.

        Parameters
            1) n: number of steps to move motor
            2) direction: 0 moves motor counter-clockwise, 1 moves motor clockwise

        Return
            success/failure code
        '''

        move_fail = 0
        if direction == 0:
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_DIR_CCW', self.id))
        elif direction == 1:
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_DIR_CW', self.id))
        else:
            print("Please specify a valid direction")
            move_fail = 1

        if move_fail != 1:
        #    self.set_output(4)
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_N_STEPS', self.id, n))
            DPY50601._ser.write(DPY50601._get_cmd_bytes('GO_N_STEPS', self.id))

        return move_fail

    async def slew_async(self, direction, interval=0.5, timeout=5):
        '''slew_async:

        Wrapper to slew() to run periodic controller status reads in an asyncio concurrent context.

        :param direction: direction to move motor. 0 for ccw, 1 for cw.
        :param interval: (optional) specify interval between successive controller status reads
        :param timeout: (optional) specify number of idle controller status reads before raising timeout exception.
        :return: success code. 0 for failed slew, 1 for successful slew
        '''

        slew_success = 1
        timeout_cnt = 0

        if not (direction == 0 or direction == 1):
            print("Please specify valid direction specifier: (0) for ccw, (1) for cw.")
            slew_success = 0

        if slew_success:
            self.slew(direction)

    def slew(self, direction):
        '''slew():
            Description: Set motor spinning with no specified number of steps. Motor will keep spinning until
                         self.stop() is executed.

            Parameter
                direction: Direction that the motor should spin. 0 for ccw, 1 for cw

            Return:
                 Success/error code
        '''

        move_fail = 0
        if direction == 0:
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_DIR_CCW', self.id))
        elif direction == 1:
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_DIR_CW', self.id))
        else:
            print("Please specify a valid direction")
            move_fail = 1

        if move_fail != 1:
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SLEW', self.id))

        return move_fail

    async def home_async(self, initial=True, interval=0.5, timeout=5):
        '''home:

            Wrapper to home() function to run success/failure check of home operation
            in an asyncio concurrent context

            Parameter
                1) (optional) initial: this parameter specifies if this is the first homing
                                       operation. Initial homing operations implement slightly
                                       different logic.

                2) (optional) interval: specifies the amount of time between successive controller
                                        status checks.

                3) (optional) timeout: specifies number of idle controller status reads before timing
                                       out.

            Return
                Success/failure code
        '''

        timeout_cnt = 0
        home_success = 1

        #Run homing operation#######################################
        self.home()
        complete = 0
        while complete == 0:
            self.get_err(stop=True)
            self.get_encoderpos()
            if self.err_code != 0:
                home_success = 0
                break
            if self.enc_pos == self.prev_enc_pos:
                timeout_cnt += 1
                if timeout_cnt == timeout:
                    raise TimeoutError('Controller timeout. Limit switch pressed?')
                    home_success = 0
                    break
                if not initial:
                    n = self.enc_pos // self.encoder_motor_ratio
                    if n < 0:
                        self.step(-1*n, 0)
                    elif n > 0:
                        self.step(n, 1)
                    else:
                        complete = 1
                else:
                    complete = 1

            #yield control to event loop. We don't want to block GUI code execution
            await asyncio.sleep(0.5)
        ###################################################################################

        self.set_pos(0)
        self.reset_encoder()
        #Send final stop command for safety
        self.stop()
        return home_success

    def home(self):
        '''home:
            Send home command to motor controller
        '''
        #self.set_output(4)
        DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_DIR_CCW', self.id))
        DPY50601._ser.write(DPY50601._get_cmd_bytes('HOME', self.id, 1))

    def get_pos(self):
        '''get_position:

            Read position of stage as recorded by motor controller.
        '''
        self.prev_pos = self.pos
        DPY50601._ser.write(DPY50601._get_cmd_bytes('VERIFY', self.id, 'Z'))
        pos = DPY50601._ser.read(30).decode('utf-8')
        pos = pos.split('\r')[0]
        self.pos = int(pos)
        return self.pos

    def get_encoderpos(self):
        '''get_encoderpos:

            Get position of stage as read by encoder
        '''
        self.prev_enc_pos = self.enc_pos
        DPY50601._ser.write(DPY50601._get_cmd_bytes('VERIFY', self.id, 'EP'))
        enc_pos = DPY50601._ser.read(30).decode('utf-8')
        enc_pos = enc_pos.split('\r')[0]
        self.enc_pos = int(enc_pos)
        return self.enc_pos

    def get_err(self, stop=False):
        DPY50601._ser.write(DPY50601._get_cmd_bytes('READ_ERR_REG', self.id))
        err = DPY50601._ser.read(30).decode('utf-8')
        err = err.split('\r')[0]
        self.err_code = int(err)
        if self.err_code != 0:
            if stop is True:
                self.stop()
            raise RuntimeError('Error code {} received on controller {}'.format(self.err_code, self.id))
        return self.err_code

    def stop(self):
        '''stop:

            Stops all motion
        '''

        stop_fail = 0
        DPY50601._ser.write(DPY50601._get_cmd_bytes('STOP', self.id))
        return stop_fail

    def set_basespeed(self, speed):
        '''set_basespeed:

        Sets basespeed of the motor controller. This is the speed that the motor will
        travel during home operations.

        Parameters
            1) speed: Speed value. Value specified here should be between 1-5000

        Return
            1) success code

        '''
        set_fail = 0
        DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_BASE_SPEED', self.id, speed))
        DPY50601._ser.write(DPY50601._get_cmd_bytes('VERIFY', self.id, 'B'))
        basespeed = DPY50601._ser.read(30)
        if (basespeed != speed):
            set_fail = 1
        return set_fail

    def get_basespeed(self):
        '''get_basespeed:

            Returns current basespeed value
        '''

        DPY50601._ser.write(DPY50601._get_cmd_bytes('VERIFY', self.id, 'B'))
        basespeed = DPY50601._ser.read(30)
        return basespeed

    def set_maxspeed(self, speed):
        '''set_maxspeed:

            Sets maxspeed of the motor controller. This is the speed that the motor will
            travel during step operations.

            Parameters
                1) speed: Speed value. Value specified here should be between 1-50000

            Return
                1) success code

        '''

        set_fail = 0
        DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_MAX_SPEED', self.id, speed))
        DPY50601._ser.write(DPY50601._get_cmd_bytes('VERIFY', self.id, 'M'))
        maxspeed = DPY50601._ser.read(30)
        if (maxspeed != speed):
            set_fail = 1
        return set_fail

    def get_maxspeed(self):
        '''get_maxspeed:

            Returns current maxspeed value
        '''

        DPY50601._ser.write(DPY50601._get_cmd_bytes('VERIFY', self.id, 'M'))
        maxspeed = DPY50601._ser.read(30)
        return maxspeed

    def set_pos(self, pos):
        '''set_position:

            Set internal position counter for relative motion
        '''

        DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_POS', self.id, pos))
        self.prev_pos = self.pos
        self.pos = 0

    def reset_encoder(self):
        '''reset_encoder:

            Reset internal encoder count register to 0
        '''
        print("Resetting encoder")
        DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_RST', self.id))
        self.prev_enc_pos = self.enc_pos
        self.enc_pos = 0

    def set_output(self, val):
        '''Write to the controller output register.

        :param val: Value to write to output register. Should be within range 0-255
        :return: None
        '''
        DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_OUTPUT', self.id, val))
    ######################################################################################################
