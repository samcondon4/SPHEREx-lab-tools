import serial
from serial import rs485
from serial.tools import list_ports

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
        'HOME': '@{}H{}\r',
        'READ_ALL_INPUTS': '@{}IR\r',
        'READ_INPUT': '@{}I{}\r',
        'SET_MAX_SPEED': '@{}M{}\r',
        'SET_N_STEPS': '@{}N{}\r',
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
        ports = list_ports.comports()
        for p in ports:
            try:
                ser = serial.Serial(p.name, 38400, xonxoff=True, timeout=0.5, write_timeout=0.5)
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
                    break
                else:
                    ser.close()

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
    def __init__(self, motor_id):

        ##Instance Variables
        self.id = motor_id

        ##If DPY50601 serial COM port hasn't been opened, then open it. Otherwise, ping controller
        ##at specified ID through the open port.
        if (DPY50601._ser == None):
            DPY50601._open_serial()
        else:
            DPY50601._ser.write(DPY50601._get_cmd_bytes('READ_VERS_REG', self.id))
            readval = DPY50601._ser.read(30)
            if (b'SMC60' not in readval):
                print("DPY50601 Controller at ID {} not found...".format(self.id))

    #########################################################################################

    ##Instance Methods###################################################################################
    def step(self, n, direction):
        '''step:

        Sends command to move stepper motor 'n' steps in specified direction.

        Parameters
            1) n: number of steps to move motor
            2) direction: 0 moves motor clockwise, 1 moves motor counter-clockwise

        Return
            current None. Eventually this should return if the move was successful

        '''

        move_fail = 0
        if (direction == 0):
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_DIR_CW', self.id))
        elif (direction == 1):
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_DIR_CCW', self.id))
        else:
            print("Please specify a valid direction")
            move_fail = 1

        if (move_fail != 1):
            DPY50601._ser.write(DPY50601._get_cmd_bytes('SET_N_STEPS', self.id, n))
            DPY50601._ser.write(DPY50601._get_cmd_bytes('GO_N_STEPS', self.id))

        return move_fail

    def home(self):
        '''home:

            Return motor to home position
        '''

        home_fail = 0
        DPY50601._ser.write(DPY50601._get_cmd_bytes('HOME', self.id, 1))
        return home_fail

    def stop(self):
        '''stop:

            Stops all motion
        '''

        stop_fail = 0
        DPY50601._ser.write(DPY50601._get_cmd_bytes('STOP', self.id))
        return stop_fail

    '''set_basespeed:

        Sets basespeed of the motor controller. This is the speed that the motor will
        travel during home operations.

        Parameters
            1) speed: Speed value. Value specified here should be between 1-5000

        Return
            1) success code

    '''

    def set_basespeed(self, speed):
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
        ######################################################################################################






