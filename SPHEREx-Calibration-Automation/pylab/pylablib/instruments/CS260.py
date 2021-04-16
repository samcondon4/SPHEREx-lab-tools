import subprocess as sp
from subprocess import *
import asyncio


async def async_sp_run(args, check=False):
    """async_sp_run: asynchronous equivalent of the subprocess run function that always captures
                     the process output.

    :return: completed process object
    """
    with sp.Popen(args, stdout=PIPE, stderr=PIPE, stdin=PIPE) as process:

        retcode = None
        #wait for process to complete
        while retcode is None:
            retcode = process.poll()
            await asyncio.sleep(0.001)

        stdout = process.stdout.read()
        stderr = process.stderr.read()

    if retcode != 0 and check:
        raise CalledProcessError(retcode, process.args,
                                 output=stdout, stderr=stderr)

    return sp.CompletedProcess(process.args, retcode, stdout, stderr)


class CS260:

    """CS260: Wrapper class to send and receive commands from the Oriel Cornerstone 260 monochromator.

                IMPORTANT: This class relies on the use of a pre-written executable file that provide an
                           interface to the Oriel USB drivers. Upon creating an instance of this class,
                           the path to this file must be specified!

              Create an instance of this class and use the various methods described below to interact
              with the monochromator. Each method returns a success/failure code. Return values can be
              decoded with the following key.

                  Communication errors:
                      -3: invalid parameters given to method.
                      -2: invalid parameters seen by executable. This typically should not be seen as the
                          class method should catch invalid parameters before sending them to the executable.
                          In this case a -3 is returned.
                      -1: USB communication error occurred. Check connections and ensure all drivers all installed!

                  Monochromator system errors:
                      1: miscellaneous system error
                      2: command not understood
                      3: bad parameter given
                      4: wavelength destination not allowed
                      7: accessory not present. This usually refers to the filter wheel.
                      8: accessory already in specified position.
                      9: could not home wavelength drive.
                      10: label too long

                  0: Success
    """

    def __init__(self, exe_path_, grat1_range_=(0.475, 1.400), grat2_range_=(0.925, 2.600), grat3_range_=(2.500, 12.0)):
        """ initialize instance of CS260 class

        :param exe_path_: Path to C++ executable DLL wrapper
               grat*_range: tuples with wavelength ranges for each grating present in monochromator. On initialization,
                            these values should be specified in microns
        """
        self.exe_path = exe_path_
        self.units = "UM"
        self.wavelength = None
        self.step_pos = None
        self.grating = None
        self.shutter_state = None
        self.filter = None
        self.slit1_microns = None
        self.slit2_microns = None
        self.slit3_microns = None
        self.bandpass = None
        self.out_port = None
        self.grat1_range = grat1_range_
        self.grat2_range = grat2_range_
        self.grat3_range = grat3_range_
        self.grating_ranges = [grat1_range_, grat2_range_, grat3_range_]
        self.open()
        # set default units to microns
        self.set_units("NM")
        #Get initial values for all parameters#########################
        self.get_units()
        self.get_wavelength()
        self.get_grating()
        self.get_shutter()
        self.get_filter()
        self.get_slit_microns(1)
        self.get_slit_microns(2)
        self.get_slit_microns(3)
        self.get_bandpass()
        #################################################################

    ##Wrapper functions##########################################################

    def set_units(self, units):
        """set_units: Set units that wavelength is expressed in. Valid units are
                      nano-meter ("NM"), micro-meter ("UM"), or wave-number ("WN")

        :param units: Should be a two character string. Valid options are given in
                      parenthesis above.
        :return: Success/failure code. Refer to return code comments given above
        """

        if (units == "NM") or (units == "UM") or (units == "WN"):
            if units != self.units:
                cp = self.write("UNITS {}".format(units))
                ret = cp.returncode
                if units == "UM" and self.units == "NM":
                    for i in range(3):
                        self.grating_ranges[i] = (self.grating_ranges[i][0] * (10**-3),
                                                  self.grating_ranges[i][1] * (10**-3))
                elif units == "UM" and self.units == "WN":
                    for i in range(3):
                        self.grating_ranges[i] = ((1/self.grating_ranges[i][1]) * (10**4),
                                                  (1/self.grating_ranges[i][0]) * (10**4))
                elif units == "NM" and self.units == "UM":
                    for i in range(3):
                        self.grating_ranges[i] = (self.grating_ranges[i][0] * (10**3),
                                                  self.grating_ranges[i][1] * (10**3))
                elif units == "NM" and self.units == "WN":
                    for i in range(3):
                        self.grating_ranges[i] = ((1/self.grating_ranges[i][1]) * (10**7),
                                                  (1/self.grating_ranges[i][0]) * (10**7))
                elif units == "WN" and self.units == "UM":
                    for i in range(3):
                        self.grating_ranges[i] = ((1/(self.grating_ranges[i][1] * 10**-4)),
                                                  (1/(self.grating_ranges[i][0] * 10**-4)))
                elif units == "WN" and self.units == "NM":
                    for i in range(3):
                        self.grating_ranges[i] = ((1/(self.grating_ranges[i][1] * 10**-7)),
                                                  (1/(self.grating_ranges[i][0] * 10**-7)))
                self.units = units
        else:
            raise ValueError("Please enter valid input argument. Valid arguments include {'NM', 'UM', 'WN'}")

    def get_units(self):
        """get_units: get units that wavelength is currently expressed in.

        :return: two character string indicating units. String values are the same as described in set_units
        """
        cp = self.ask('UNITS?')
        self.units = cp.stdout.decode('utf-8').upper()
        return self.units

    async def set_wavelength(self, wave, concurrent=False):
        """set_wavelength: move wavelength drive to step position closest
                           to specified wavelength parameter.

        :param concurrent: specify if this should be executed asynchronously
        :param wave: float wavelength value
        :return:
        """
        t = type(wave)
        if not (t == int or t == float):
            raise TypeError("Expected input of type int or float but type {} given.".format(t))
        write_task = asyncio.create_task(self.write_async("GOWAVE {}".format(wave)))
        await write_task
        cp = write_task.result()
        return cp.returncode

    def get_wavelength(self):
        """get_wavelength: returns exact wavelength output in current units.

        :return: Wavelength
        """
        cp = self.ask('WAVE?')
        self.wavelength = float(cp.stdout.decode('utf-8'))
        return self.wavelength

    async def step(self, n, concurrent=False):
        """ step: move wavelength drive an integer number of steps

        :param concurrent: specify if this should be run asynchronously
        :param n: integer number of steps to move wavelength drive. Can be positive or negative but must be integer
        :return: success/error code
        """

        t = type(n)
        if t != int:
            raise TypeError("Expected input of type int but {} given.".format(t))

        step_task = asyncio.create_task(self.write_async('STEP {}'.format(n)))
        await step_task
        cp = step_task.result()
        return cp.returncode

    def get_step(self):
        """get_step: return current wavelength drive step position

        :return: wavelength drive step position
        """
        cp = self.ask('STEP?')
        self.step_pos = int(cp.stdout.decode('utf-8'))
        return self.step_pos

    async def set_grating(self, g, concurrent=False):
        """set_grating: move wavelength drive to grating specified in integer parameter
                        g.

        :param: integer grating value 1, 2, or 3.
        :return: success code
        """
        task_run = 0
        t = type(g)
        if t != int:
            raise TypeError("Expected input of type int but type {} given.".format(t))

        if g in range(1, 4):
            sg_task = asyncio.create_task(self.write_async("GRAT {}".format(g)))
            await sg_task
            cp = sg_task.result()
            task_run = 1
        else:
            raise ValueError("Input should be integer values 1, 2, or 3")

        if task_run:
            return cp.returncode

    def get_grating(self):
        """get_grating: return current grating position

        :return: current integer grating position
        """
        cp = self.ask('GRAT?')
        self.grating = int(cp.stdout.split(b',')[0])
        return self.grating

    def abort(self):
        """abort: stop any motion on wavelength drive immediately

        :return: none
        """
        self.write('ABORT')

    def set_shutter(self, oc):
        """set_shutter: close or open shutter depending on input oc (open-close)

        :param concurrent: specify if this should be run asyncronously
        :param oc: open close: use "C" for close, "O" for open
        :return: success code
        """
        ret = 0
        if oc == "C":
            self.write('SHUTTER C')
        elif oc == "O":
            self.write('SHUTTER O')
        else:
            raise ValueError("Please specify valid value of shutter state parameter. Valid values are {'O', 'C'}")

    def get_shutter(self):
        """get_shutter: return current shutter state. 'O' indicates closed,
                        'C' indicates open

        :return: 'O' or 'C'
        """
        cp = self.ask('SHUTTER?')
        self.shutter_state = cp.stdout.decode('utf-8')
        return self.shutter_state

    async def set_filter(self, f):
        """set_filter: move filter wheel to position specified by integer f

        :param concurrent: specify if this should be run asynchronously
        :param f: integer filter wheel position
        :return: success code
        """
        task_run = 0
        t = type(f)
        if t != int:
            raise TypeError("Input type int expected but type {} was given.".format(t))
        if f in range(1, 7):
            sf_task = asyncio.create_task(self.write_async('FILTER {}'.format(f)))
            await sf_task
            cp = sf_task.result()
            task_run = 1
        else:
            raise ValueError("Filter wheel position should be integer between 1-6, but value {} was given.".format(f))

        if task_run:
            return cp.returncode

    def get_filter(self):
        """get_filter: return current filter wheel position

        :return:
        """
        cp = self.ask('FILTER?')
        self.filter = int(cp.stdout)
        return self.filter

    def set_slit_microns(self, slit, um):
        """set_slit_microns: Open slit 1 to size specified by integer parameter
                              in microns. Valid range is 6-2000 at 6 micron resolution

        :param: um: integer micron parameter. Input is rounded up to nearest 6th
        :param: slit: integer number specifying slit to open
        :return: success code
        """
        #check input types
        slit_type = type(slit)
        um_type = type(um)
        if slit_type != int:
            raise TypeError("slit argument should be of type int but type {} was given.".format(slit_type))
        elif um_type != int:
            raise TypeError("microns argument should be of type int but type {} was given.".format(um_type))

        #round input to nearest 6th
        um = um + (um % 6)
        if um in range(6, 2001):
            if slit in range(1, 4):
                self.write('SLIT{}MICRONS {}'.format(slit, um + 6 - (um % 6)))
            else:
                raise ValueError("Please enter valid slit parameter. Valid values include {1, 2, 3}")
        else:
            raise ValueError("Please enter valid microns parameter. Valid values must fall within range 6-2000")

    def get_slit_microns(self, slit):
        """get_slit_microns: gets current slit opening width for specified slit.

        :return: slit width in microns
        """
        slit_type = type(slit)
        if slit_type != int:
            raise TypeError("Expected slit parameter to be of type int but type {} given.".format(slit_type))
        if slit in range(1, 3):
            cp = self.ask('SLIT{}MICRONS?'.format(slit))
        elif slit == 3:
            cp = self.ask('SLIT3MICRONS?')
        else:
            raise ValueError("Invalid value specified for ")

    def get_bandpass(self):
        """get_bandpass: gets current bandpass parameter. This floating point parameter
                         specifies the wavelength resolution to automatically adjust
                         slits for.

        :return: floating point bandpass parameter
        """
        cp = self.ask('BANDPASS?')
        self.bandpass = float(cp.stdout.decode('utf-8'))
        return self.bandpass

    def get_error(self):
        """get_error: check for monochromator error state and return error code.

        :return: Error code or 0 if no error state encountered.
        """
        cp = self.ask('STB?')
        err_code = int(cp.stdout.decode('utf-8'))
        if err_code == 20:
            cp = self.ask('ERROR?')
            err_code = int(cp.stdout.decode('utf-8'))
            raise RuntimeError("Error state {} seen on CS260".format(err_code))
        return err_code
    ############################################################################

    ##C++ EXE Functions#################################################################
    def open(self):
        cp = sp.run([self.exe_path, 'open'], capture_output=True, check=True)
        return cp

    def close(self):
        cp = sp.run([self.exe_path, 'close'], capture_output=True, check=True)
        return cp

    def list(self):
        cp = sp.run([self.exe_path, 'list'], capture_output=True, check=True)
        return cp

    def write(self, cmd):
        args = [self.exe_path, 'write', cmd]
        cp = sp.run(args, capture_output=True, check=True)
        return cp

    async def write_async(self, cmd):
        args = [self.exe_path, 'write', cmd]
        sp_run_task = asyncio.create_task(async_sp_run(args, check=True))
        await sp_run_task
        cp = sp_run_task.result()
        return cp

    def ask(self, query):
        cp = sp.run([self.exe_path, 'ask', query], capture_output=True, check=True)
        return cp

    ########################################################################################
