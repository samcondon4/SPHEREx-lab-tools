""" This module implements the class, :class:`.MonoControlServer`, which acts as a wrapper around the
    existing monochromator driver, :class:`..newport.CS260`.
"""
import os
import time
import socket
import logging
from ..newport import CS260
from spherexlabtools.thread import StoppableReusableThread


logger = logging.getLogger(__name__)


class MonoControlServer:
    """ Wraps the existing :class:`..newport.CS260` monochromator driver with a TCPIP interface
        allowing remote command and control of the monochromator.
    """

    HOST = "131.215.200.118"
    PORT = 6550
    _cmd_sep = " "
    _cmd_terminator = "\r\n"

    query_prop_map = {
        "SHUTTER?": "shutter",
        "UNITS?": "units",
        "GRAT?": "grating",
        "FILTER?": "osf",
        "WAVE?": "wavelength"
    }

    cmd_prop_map = {
        "SHUTTER": "shutter",
        "UNITS": "units",
        "GRAT": "grating",
        "FILTER": "osf",
        "GOWAVE": "wavelength"
    }

    IDLE, SETTING, GETTING = 0, 1, 2

    def __init__(self, resource_name=None, setter_post_interval=1, **kwargs):
        """ Initialize the local monochromator control driver.
        """
        if resource_name is None:
            slt_path = os.environ["SPHEREXLABTOOLS"]
            resource_name = os.path.join(slt_path, "spherexlabtools", "instruments", "newport", "CS260_DLLs",
                                         "C++EXE.exe")
        self.cs260 = CS260(resource_name, **kwargs)
        self.state = self.IDLE
        self.setter_thread = StoppableReusableThread()
        self.setter_thread.execute = self.setter_thread_target
        self.setter_post_interval = setter_post_interval
        self.conn = None

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Monochromator control server started.")
            print("Waiting for connection...")
            s.bind((self.HOST, self.PORT))
            s.listen()
            self.conn, addr = s.accept()
            log_msg = f"MonoControlServer connected to {addr}"
            logger.info(log_msg)
            print(log_msg)
            # main command control loop #
            while True:
                cmd, val = self.get_command_val()
                if not cmd:
                    break
                if "?" in cmd and cmd in self.query_prop_map.keys():
                    self.state = self.GETTING
                    prop = self.query_prop_map[cmd]
                    resp = str(getattr(self.cs260, prop)) + self._cmd_terminator
                    log_msg = f"MonoControlServer query for {prop} received {resp}"
                    print(log_msg)
                    self.conn.sendall(bytes(str(resp), "utf-8"))
                    self.state = self.IDLE
                elif cmd in self.cmd_prop_map.keys():
                    self.state = self.SETTING
                    cmd = self.cmd_prop_map[cmd]
                    log_msg = f"MonoControlServer setting {cmd} with {val}"
                    print(log_msg)
                    setattr(self.cs260, cmd, val)
                    complete = "SETTER_COMPLETE" + self._cmd_terminator
                    self.conn.sendall(bytes(complete, "utf-8"))
                    logger.debug("sent complete flag.")
                    self.state = self.IDLE

            self.conn.close()

    def setter_thread_target(self):
        """ Target for the setter :class:`.StoppableReusableThread`
        """
        while self.state == self.SETTING:
            logger.debug("setter_thread_target sending incomplete flag.")
            cmd, val = self.get_command_val()
            if cmd == "SETCOMPLETE?":
                self.conn.sendall(bytes(f"False{self._cmd_terminator}", "utf-8"))
        cmd, val = self.get_command_val()
        if cmd == "SETCOMPLETE?":
            logger.debug("setter_thread_target sending complete flag.")
            self.conn.sendall(bytes(f"True{self._cmd_terminator}", "utf-8"))

    def get_command_val(self):
        data = self.conn.recv(1024)
        data = data.decode("utf-8").split(self._cmd_terminator)[0]
        if not data or data == "CLOSE":
            return False
        data_cmd_split = data.split(self._cmd_sep)
        cmd = data_cmd_split[0]
        if len(data_cmd_split) > 1:
            ret = (cmd, data_cmd_split[1])
        else:
            ret = (cmd, None)
        return ret

