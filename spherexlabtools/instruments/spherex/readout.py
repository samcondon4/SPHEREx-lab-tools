""" This module implements a wrapper around the client side of the SPHEREx detector readout control server, as
    well as an http server that the readout control sends detector data acquisition complete messages to.
"""

import json
import queue
import logging
import time

import requests
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

from spherexlabtools.thread import StoppableReusableThread

logger = logging.getLogger(__name__)


class DaqCompleteHandler(BaseHTTPRequestHandler):
    """ Handler subclass to handle data acquisition complete messages.
    """

    daq_response = None

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        """ Handle POST requests.
        """
        # self._set_headers()
        data_string = self.rfile.read(int(self.headers["Content-Length"]))
        self.daq_response = json.loads(data_string)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(data_string)
        self.server.daq_complete_q.put(self.daq_response)


class DaqCompleteServer(HTTPServer):
    """ Subclass of the basic HTTPServer to implement a queue, onto which the handler will place data sent from
        post requests.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daq_complete_q = queue.Queue()


class DetectorCom:
    """ Class implementing control of the detector data acquisition.
    """

    # http communication names #
    readout_hostname_start = "http://131.215.196.228:8555/test"
    readout_hostname_done = "http://131.215.196.228:8555/done"
    control_hostname = "131.215.200.125"
    control_port = 8000

    # this dictionary should be sent over http to trigger an exposure #
    _exp_cmd_dict = {
        "detid": "00",
        "detsn": "18831",
        "start": "rob1",
        "surcnt": 393,
        'surlim': 400,
    }

    # - this dictionary is used to check if the exposure has completed - #
    _exp_done_dict = {
        "fileid": None
    }

    def __init__(self, rec_name, exp=None, **kwargs):
        """ Start the data-acquisition pend server.
        """
        pass

    def start_exposure(self, exposure_time=30, comment="", detsn=None, detid=None, pend_for_complete=False, nofits=0,
                       timestamp=None, surcnt=None, surlim=None):
        """ Send the http command to start an exposure.

        :param exposure_time: Exposure time in seconds.
        :param comment: String with comment that should accompany the exposure fits file.
        :param pend_for_complete: Boolean to indicate if this method should block until the daq
                                  completion flag is received from the readout server.
        :param nofits: Setting this to 1 means that fits files will not be generated for this exposure.
        """
        assert exposure_time > 0, "Exposure duration must be > 0"

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") if timestamp is None else timestamp
        self._exp_cmd_dict.update({"exposure": exposure_time, "comment": str(comment), "nobin": nofits,
                                   "timestamp": timestamp})
        key_list = list(self._exp_cmd_dict.keys())
        if surcnt is not None:
            self._exp_cmd_dict.update({'surcnt': surcnt})
        elif 'surcnt' in key_list:
            self._exp_cmd_dict.pop('surcnt')

        if surlim is not None:
            self._exp_cmd_dict.update({'surlim': surlim})
        elif 'surlim' in key_list:
            self._exp_cmd_dict.pop('surlim')

        if detsn is not None:
            self._exp_cmd_dict['detsn'] = detsn
        if detid is not None:
            self._exp_cmd_dict['detid'] = detid

        # - change surcnt to surcn (changed on 2023-11-17 to match Hiro's new command) - #
        key_list = list(self._exp_cmd_dict.keys())
        if 'surcnt' in key_list:
            surcn = self._exp_cmd_dict.pop('surcnt')
            self._exp_cmd_dict['surcn'] = surcn
        # - change nofits to nobin (changed on 2023-11-17 to match Hiro's new command) - #
        if 'nofits' in key_list:
            nobin = self._exp_cmd_dict.pop('nofits')
            self._exp_cmd_dict['nobin'] = nobin

        logger.info(f"starting DETECTOR EXPOSURE with EXPOSURE PARAMETERS: \n {self._exp_cmd_dict}")
        r0 = requests.post(self.readout_hostname_start, json=self._exp_cmd_dict)
        r0_json = r0.json()
        file_id = r0_json["testcom"]["fileid"]

        if pend_for_complete:
            time.sleep(exposure_time)
            ret = {"done": False}
            self._exp_done_dict.update({"fileid": file_id})
            while not ret["done"]:
                ret = requests.post(self.readout_hostname_done, json=self._exp_done_dict).json()
                time.sleep(1)

        return r0_json
