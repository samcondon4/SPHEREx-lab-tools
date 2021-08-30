"""CS260: This module implements a getter/setter based control wrapper for the Oriel CS260 monochromator

Sam Condon 07/01/2021
"""
import sys
import subprocess as sp
from subprocess import *
import asyncio

sys.path.append("..\\..\\")
from pylabinst.pylabinst_instrument_base import Instrument


class CS260(Instrument):

    def __init__(self, exe_path="pylabinst\\CS260_DLLs\\C++EXE.exe"):
        super().__init__("CS260")
        self.exe_path = exe_path

        # Configure open method###################
        self.set_open_method(self.cs260_open)
        ##########################################

        # Configure parameters ###############################################################
        self.add_parameter("current wavelength", self.get_wavelength, self.set_wavelength, coro=True)
        self.add_parameter("current grating", self.get_grating, self.set_grating, coro=True)
        self.add_parameter("current order sort filter", self.get_osf, self.set_osf, coro=True)
        self.add_parameter("current shutter", self.get_shutter_state, self.set_shutter_state, coro=True)
        self.add_get_parameter("current units", self.get_units, coro=True)
        self.add_set_parameter("current units", self.set_units, coro=False)
        #######################################################################################

    # PARAMETER GETTER/SETTERS ##########################################################
    async def get_wavelength(self):
        """get_wavelength: returns exact wavelength output in current units.

        :return: Wavelength
        """
        ask_task = asyncio.create_task(self.ask("WAVE?"))
        await ask_task
        cp = ask_task.result()
        return cp.stdout.decode('utf-8')

    async def set_wavelength(self, wavelength):
        """set_wavelength: move wavelength drive to step position closest
                           to specified wavelength parameter.

        :param wavelength: <float> wavelength value
        :return:
        """
        t = type(wavelength)
        if not (t == int or t == float):
            raise TypeError("Expected input of type int or float but type {} given.".format(t))
        write_task = asyncio.create_task(self.write_async("GOWAVE {}".format(wavelength)))
        await write_task
        await asyncio.create_task(self.async_pend("wave", arg=wavelength))
        cp = write_task.result()
        return cp.returncode

    async def get_grating(self):
        """get_grating: return current grating position

        :return: current integer grating position
        """
        ask_task = asyncio.create_task(self.ask("GRAT?"))
        await ask_task
        cp = ask_task.result()
        return (cp.stdout.split(b',')[0]).decode("utf-8")

    async def set_grating(self, grating):
        """set_grating: move wavelength drive to grating specified in integer parameter
                        grating.

        :param: grating: integer grating value 1, 2, or 3.
        :return: success code
        """
        task_run = 0
        t = type(grating)
        if t != int:
            raise TypeError("Expected input of type int but type {} given.".format(t))

        if grating in range(1, 4):
            sg_task = asyncio.create_task(self.write_async("GRAT {}".format(grating)))
            await sg_task
            await asyncio.create_task(self.async_pend("grating", arg=grating))
            cp = sg_task.result()
            task_run = 1
        else:
            raise ValueError("Input should be integer values 1, 2, or 3")

        if task_run:
            return cp.returncode

    async def get_osf(self):
        """get_filter: return current filter wheel position

        :return:
        """
        ask_task = asyncio.create_task(self.ask("FILTER?"))
        await ask_task
        cp = ask_task.result()
        return cp.stdout.decode("utf-8")

    async def set_osf(self, osf):
        """set_filter: move filter wheel to position specified by integer f

        :param osf: integer filter wheel position
        :return: success code
        """
        task_run = 0
        t = type(osf)
        if t != int:
            raise TypeError("Input type int expected but type {} was given.".format(t))
        if osf in range(1, 7):
            sf_task = asyncio.create_task(self.write_async('FILTER {}'.format(osf)))
            await sf_task
            await asyncio.create_task(self.async_pend("osf", arg=osf))
            cp = sf_task.result()
            task_run = 1
        else:
            raise ValueError("Filter wheel position should be integer between 1-6, but value {} was given.".format(osf))

        if task_run:
            return cp.returncode

    async def get_shutter_state(self):
        """get_shutter: return current shutter state. 'O' indicates closed,
                        'C' indicates open

        :return: 'O' or 'C'
        """
        ask_task = asyncio.create_task(self.ask("SHUTTER?"))
        await ask_task
        cp = ask_task.result()
        return cp.stdout.decode('utf-8')

    async def set_shutter_state(self, shutter_state):
        """set_shutter: close or open shutter depending on input oc (open-close)

        :param shutter_state: open close: use "C" for close, "O" for open
        :return: success code
        """
        ret = 0
        if shutter_state == "C":
            self.write('SHUTTER C')
        elif shutter_state == "O":
            self.write('SHUTTER O')
        else:
            raise ValueError("Please specify valid value of shutter state parameter. Valid values are {'Open', 'Close'}")

    async def get_units(self):
        """get_units: get units that wavelength is currently expressed in.

        :return: two character string indicating units. String values are the same as described in set_units
        """
        ask_task = asyncio.create_task(self.ask("UNITS?"))
        await ask_task
        cp = ask_task.result()
        return cp.stdout.decode('utf-8').upper()

    def set_units(self, units):
        """set_units: Set units that wavelength is expressed in. Valid units are
                      nano-meter ("NM"), micro-meter ("UM"), or wave-number ("WN")

        :param units: Should be a two character string. Valid options are given in
                      parenthesis above.
        :return: Success/failure code. Refer to return code comments given above
        """
        ret = None

        if (units == "NM") or (units == "UM") or (units == "WN"):
            cp = self.write("UNITS {}".format(units))
        else:
            raise ValueError("Please enter valid input argument. Valid arguments include {'NM', 'UM', 'WN'}")

        if ret is not None:
            return ret
    #####################################################################################

    # C++ EXE Methods ###################################################################
    def cs260_open(self):
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
        sp_run_task = asyncio.create_task(self.async_sp_run(args, check=True))
        await sp_run_task
        cp = sp_run_task.result()
        return cp

    async def ask(self, query):
        sp_task = asyncio.create_task(self.async_sp_run([self.exe_path, 'ask', query], check=True))
        await sp_task
        cp = sp_task.result()
        return cp

    #####################################################################################

    # OTHER SUPPORT METHODS #########################################################################################
    async def async_pend(self, pend_task, arg=None, pend_time=0.5):
        """async_pend: additional layer of pending. Sometimes the low-level "blocking" cs260 communication
                       functions exit before their action is actually complete. This function waits until
                       a valid return has been read from the cs260 before leaving. Also can serve as a check
                       for if the monochromator responded properly by comparing the queried value against
                       arg.

            Parameters:
                pend_task: which of the above async tasks should be pended? Valid inputs are "osf", "grating",
                           "step", or "wave"
                arg: Argument that was passed in higher level calling function. Compare cs260 query with this
                     value to check if device responded properly. Default value is None, which indicates that
                     no check should be performed.
                pend_time: interval (seconds) between queries
        """
        # Set proper query function based on input argument
        query_func = None
        if pend_task == "wave":
            query_func = self.get_wavelength
        elif pend_task == "grating":
            query_func = self.get_grating
        elif pend_task == "osf":
            query_func = self.get_osf
        else:
            raise ValueError("Invalid pend_task argument provided. Valid values are {'wave', 'osf', 'grating'}")

        complete = False
        val = 0
        while not complete:
            try:
                query_task = asyncio.create_task(query_func())
                await query_task
                val = query_task.result()
            except ValueError as e:
                await asyncio.sleep(pend_time)
            else:
                complete = True

        # Check if monochromator queried value matches desired value. Raise exception if it doesn't
        if (arg is not None) and (not (abs(val - arg) < 0.2)):
            raise RuntimeError("Monochromator {} task set unspecified value {} instead of {}".format(pend_task, val, arg))
        else:
            return val

    @staticmethod
    async def async_sp_run(args, check=False):
        """async_sp_run: asynchronous equivalent of the subprocess run function that always captures
                         the process output.

        :return: completed process object
        """
        with sp.Popen(args, stdout=PIPE, stderr=PIPE, stdin=PIPE) as process:

            retcode = None
            # wait for process to complete
            while retcode is None:
                retcode = process.poll()
                await asyncio.sleep(0.001)

            stdout = process.stdout.read()
            stderr = process.stderr.read()

        if retcode != 0 and check:
            raise CalledProcessError(retcode, process.args,
                                     output=stdout, stderr=stderr)

        return sp.CompletedProcess(process.args, retcode, stdout, stderr)
    ################################################################################################################