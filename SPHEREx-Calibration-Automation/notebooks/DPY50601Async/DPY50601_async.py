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
        'SET_ADDR_REG': '@{}~{}\r'
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
                if (ser.is_open):
                    ser.close()
            else:
                readval = ser.read(30)
                if (b'SMC60' in readval):
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
    def __init__(self, motor_id, encoder_motor_ratio=8, encoder_retries=10, step_range=20000):

        ##Instance Variables
        self.id = motor_id
        self.encoder_motor_ratio = encoder_motor_ratio
        self.encoder_retries = encoder_retries
        self.step_range = step_range
        self.com_est = 0  # communication established?
        self.pos = 0
        self.prev_pos = 0
        self.enc_pos = 0
        self.prev_enc_pos = 0
        self.err_code = 0
        self.task_running = {'get_err_async': 0,
                             'get_encoderpos_async': 0,
                             'home_async': 0,
                             'step_async': 0}

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
            DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_RETRIES', self.id, self.encoder_retries))
            # Read initial motor stage position
            self.pos = self.get_pos()
            self.prev_pos = self.pos
            self.enc_pos = self.get_encoderpos()
            self.prev_enc_pos = self.enc_pos
        else:
            print("DPY50601 Controller at ID {} not found...".format(self.id))

    #########################################################################################

    ##Instance Methods###################################################################################
    async def step_async(self, n, direction):
        '''step:

        Wrapper to step() to run success/failure check of step() operation in
        an asynio concurrent context.

        Parameters
            1) n: number of steps to move motor
            2) direction: 0 moves motor counter-clockwise, 1 moves motor clockwise

        Return
            success/failure code
        '''

        move_success = 1

        #Register step async task as running
        self.task_running['step_async'] = 1

        # Make sure a valid direction specifier was provided
        if not (direction == 0 or direction == 1):
            print("Please specify valid direction specifier: (0) for ccw, (1) for cw.")
            move_success = 0

        mult = (-2 * direction) + 1
        dest = self.enc_pos + 8 * (mult * n)
        if dest < 0 or dest > 8 * self.step_range:
            print("Step count leaves range")
            move_success = 0

        if move_success:  # Don't run the code that actually moves the motor if an error was previously detected
            # Create asyncio tasks
            if self.task_running['get_encoderpos_async'] == 0:
                postask = asyncio.create_task(self.get_encoderpos_async())
                self.task_running['get_encoderpos_async'] = 1

            if self.task_running['get_err_async'] == 0:
                errtask = asyncio.create_task(self.get_err_async(stop=True))
                self.task_running['get_err_async'] = 1

            if mult < 0:
                self.step(n, 1)
            else:
                self.step(n, 0)
            while self.enc_pos != dest:
                print("step async, error code: {}".format(self.err_code))
                await asyncio.wait([errtask, postask])
                if self.err_code != 0:
                    print("leaving step")
                    move_success = 0
                    break
                if self.prev_enc_pos == self.enc_pos:
                    n = (self.enc_pos - dest) // 8
                    if n < 0:
                        self.step(n, 0)
                    elif n > 0:
                        self.step(n, 1)
            # End periodic position and error message reading
            postask.cancel()
            self.task_running['get_encoderpos_async'] = 0
            errtask.cancel()
            self.task_running['get_err_async'] = 0

        print("step task complete")
        self.task_running['step_async'] = 0
        return move_success

    def step(self, n, direction):
        '''step:

        Sends command to move stepper motor 'n' steps in specified direction.

        Parameters
            1) n: number of steps to move motor
            2) direction: 0 moves motor counter-clockwise, 1 moves motor clockwise

        Return
            current None. Eventually this should return if the move was successful

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
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_N_STEPS', self.id, n))
            DPY50601._ser.write(DPY50601._get_cmd_bytes('GO_N_STEPS', self.id))

        return move_fail

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

    async def home_async(self):
        '''home:

            Wrapper to home() function to run success/failure check of home operation
            in an asyncio concurrent context

            Return
                Success/failure code
        '''

        #Register home_async task as running
        self.task_running['home_async'] = 1
        home_success = 1

        if self.task_running['get_encoderpos_async'] == 0:
            postask = asyncio.create_task(self.get_encoderpos_async())
            self.task_running['get_encoderpos_async'] = 1

        if self.task_running['get_err_async'] == 0:
            errtask = asyncio.create_task(self.get_err_async(stop=True))
            self.task_running['get_err_async'] = 1

        await self.step_async(2000, 0)
        self.home()
        while self.enc_pos != 0:
            await asyncio.wait([errtask, postask])
            if self.err_code != 0:
                home_success = 0
                break
            '''
            if self.enc_pos == self.prev_enc_pos:
                n = self.enc_pos // 8
                if n < 0:
                    self.step(n, 0)
                elif n > 0:
                    self.step(n, 1)
                else:
                    print("Home operation on unit {} complete".format(self.id))
                    self.set_pos(0)
                    self.reset_encoder()
            '''

            if self.enc_pos == self.prev_enc_pos:
                print("Home operation on unit {} complete".format(self.id))
                print(self.get_encoderpos())
                self.set_pos(0)
                self.reset_encoder()

        # End periodic position and error reading
        postask.cancel()
        self.task_running['get_encoderpos_async'] = 0
        errtask.cancel()
        self.task_running['get_err_async'] = 0

        self.task_running['home_async'] = 0
        return home_success

    def home(self):
        '''home:
            Send home command to motor controller
        '''
        DPY50601._ser.write(DPY50601._get_cmd_bytes('HOME', self.id, 1))

    async def get_pos_async(self, interval=0.5):
        '''get_pos_async:

            Wrapper for get_pos for use in periodic readings in asyncio context

            Parameter:
                1) interval: amount of time to sleep before next execution
            Return:
                None, position is returned through class instance attribute pos
        '''

        while 1:
            self.get_pos()
            await asyncio.sleep(interval)

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

    async def get_encoderpos_async(self, interval=0.5):
        '''get_encoderpos_async:

            Wrapper for get_encoderpos for use in asyncio context.

            Parameter
                1) interval: amount of time to sleep until next execution

            Return:
                 None, encoder position is returned through the class instance attribute enc_pos
        '''

        while 1:
            self.get_encoderpos()
            await asyncio.sleep(interval)

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

    async def get_err_async(self, stop=False, interval=0.5):
        '''get_err_async:

            Parameters
                1) stop: optional boolean that gives method permission to halt
                         any motion if an error is detected.

                2) interval: amount of time to sleep before next execution

            Read error register for use as asyncio task
        '''
        while 1:
            self.get_err(stop=stop)
            await asyncio.sleep(interval)

    def get_err(self, stop=False):
        DPY50601._ser.write(DPY50601._get_cmd_bytes('READ_ERR_REG', self.id))
        err = DPY50601._ser.read(30).decode('utf-8')
        print("get_err")
        print(err)
        err = err.split('\r')[0]
        print(err)
        self.err_code = int(err)
        print(self.err_code)
        if self.err_code != 0:
            print("Error {} received during motion on unit {}".format(self.err_code, self.id))
            if stop is True:
                self.stop()
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

        DPY50601._ser.write(DPY50601._get_cmd_bytes('ENCD_RST', self.id))
        self.prev_enc_pos = self.enc_pos
        self.enc_pos = 0
    ######################################################################################################
