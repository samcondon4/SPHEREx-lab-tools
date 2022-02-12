""" This module implements a set of ubiquitous procedure classes for measurement execution. These
    classes include:

        - :class:`.BasicProc`

Sam Condon, 01/31/2022
"""
import time
import logging
import inspect
import importlib
from copy import deepcopy
from pymeasure.experiment import Parameter, FloatParameter

from ..thread import StoppableReusableThread


logger = logging.getLogger(__name__)


class BaseProcedure(StoppableReusableThread):
    """ Thread to execute a measurement. Largely based on the pymeasure procedure class.
    """

    DATA_COLUMNS = []
    MEASURE = {}
    FINISHED, FAILED, ABORTED, QUEUED, RUNNING = 0, 1, 2, 3, 4
    STATUS_STRINGS = {
        FINISHED: 'Finished', FAILED: 'Failed',
        ABORTED: 'Aborted', QUEUED: 'Queued',
        RUNNING: 'Running'
    }

    _parameters = {}

    def __init__(self, cfg, hw=None, viewers=None, recorders=None, **kwargs):
        """ Initialize a bare procedure instance.

        :param hw: :class:`..instruments.InstrumentSuite` object.
        :param records: Dictionary containing lists of queues to which data should be posted on
                         calls to emit().
        :param viewers: Dictionary of Viewer objects.
        :param recorders: Dictionary of recorder objects.
        :param kwargs: Key-word arguments to set the procedure parameters.
        """
        super().__init__()
        self.hw = getattr(hw, cfg["hw"])
        qdict = {}
        for key, val in cfg["records"].items():
            qdict_val = [{"viewer": viewers, "recorder": recorders}[k][v].queue for k, v in val.items()]
            qdict[key] = qdict_val
        self.records = qdict
        self.status = BaseProcedure.QUEUED
        self._update_parameters()
        for key in kwargs:
            if key in self._parameters.keys():
                setattr(self, key, kwargs[key])

    def startup(self):
        """ Check that all procedure parameters have been set.
        """
        self.check_parameters()

    def emit(self, record_name, record_data, **kwargs):
        """ Post a record to the appropriate queues.
        """
        if len(kwargs) > 0:
            record_data = {"data": record_data, "handle_kwargs": kwargs}
        for q in self.records[record_name]:
            q.put(record_data)

    def _update_parameters(self):
        """ Collects all the Parameter objects for the procedure and stores
        them in a meta dictionary so that the actual values can be set in
        their stead
        """
        if not self._parameters:
            self._parameters = {}
        for item, parameter in inspect.getmembers(self.__class__):
            if isinstance(parameter, Parameter):
                self._parameters[item] = deepcopy(parameter)
                if parameter.is_set():
                    setattr(self, item, parameter.value)
                else:
                    setattr(self, item, None)

    def parameters_are_set(self):
        """ Returns True if all parameters are set """
        for name, parameter in self._parameters.items():
            if getattr(self, name) is None:
                return False
        return True

    def check_parameters(self):
        """ Raises an exception if any parameter is missing before calling
        the associated function. Ensures that each value can be set and
        got, which should cast it into the right format. Used as a decorator
        @check_parameters on the startup method
        """
        for name, parameter in self._parameters.items():
            value = getattr(self, name)
            if value is None:
                raise NameError("Missing {} '{}' in {}".format(
                    parameter.__class__, name, self.__class__))

    def parameter_values(self):
        """ Returns a dictionary of all the Parameter values and grabs any
        current values that are not in the default definitions
        """
        result = {}
        for name, parameter in self._parameters.items():
            value = getattr(self, name)
            if value is not None:
                parameter.value = value
                setattr(self, name, parameter.value)
                result[name] = parameter.value
            else:
                result[name] = None
        return result

    def parameter_objects(self):
        """ Returns a dictionary of all the Parameter objects and grabs any
        current values that are not in the default definitions
        """
        result = {}
        for name, parameter in self._parameters.items():
            value = getattr(self, name)
            if value is not None:
                parameter.value = value
                setattr(self, name, parameter.value)
            result[name] = parameter
        return result

    def refresh_parameters(self):
        """ Enforces that all the parameters are re-cast and updated in the meta
        dictionary
        """
        for name, parameter in self._parameters.items():
            value = getattr(self, name)
            parameter.value = value
            setattr(self, name, parameter.value)

    def set_parameters(self, parameters, except_missing=True):
        """ Sets a dictionary of parameters and raises an exception if additional
        parameters are present if except_missing is True
        """
        for name, value in parameters.items():
            if name in self._parameters:
                self._parameters[name].value = value
                setattr(self, name, self._parameters[name].value)
            else:
                if except_missing:
                    raise NameError("Parameter '{}' does not belong to '{}'".format(
                        name, repr(self)))


class LogProc(BaseProcedure):
    """ Basic procedure that continuously records a parameter at a defined refresh rate and
        sends it to a :class:`..recorders.Recorder`, a :class:`..viewers.Viewer`, or both
        with calls to :meth:`BaseProcedure.emit()`.
    """

    refresh_rate = FloatParameter("Log Rate", units="Hz.", default=1)

    def __init__(self, cfg, **kwargs):
        """ Initialize a basic procedure that will record data from the prop argument.

        :param cfg: List of procedure configurations.
        :param kwargs: Key-word arguments for :class:`.BaseProcedure`
        """
        super().__init__(cfg, **kwargs)
        self.DATA_COLUMNS = list(self.records.keys())

    def execute(self):
        """ Procedure execution method. Calls get_properties() to start recording props at a fixed interval.
        """
        while not self.thread.should_stop():
            self.get_properties()
            time.sleep(1/self.refresh_rate)

    def get_properties(self):
        """ Retrieve all properties given in the DATA_COLUMNS list and emit results.
        """
        for p in self.DATA_COLUMNS:
            data = getattr(self.hw, p)
            self.emit(p, data)


def create_procedures(exp_pkg, hw, viewers=None, recorders=None):
    """ Create a set of procedures.

    :param: exp_pkg: User experiment configuration package.
    :param: hw: InstrumentSuite object.
    :param: viewers: Dictionary of instantiated viewers.
    :param: recorders: Dictionary of instantiated recorders.
    """
    proc_cfgs = exp_pkg.PROCEDURES
    procedures = {}
    for cfg in proc_cfgs:
        # get hardware object #
        hw_obj = getattr(hw, cfg["hw"])

        # get recorder and viewer queues to pass to the procedure base #
        records = cfg["records"]
        qdict = {}
        for key, val in records.items():
            qdict_val = [{"viewer": viewers, "recorder": recorders}[k][v].queue for k, v in val.items()]
            qdict[key] = qdict_val

        # instantiate the procedure object. Search order for a procedure class definition is:
        # 1) User defined procedures in the experiment package.
        # 2) spherexlabtools core procedures.
        try:
            proc_class = getattr(exp_pkg.procedures, cfg["type"])
        except (AttributeError, ModuleNotFoundError):
            proc_mod = importlib.import_module(__name__)
            proc_class = getattr(proc_mod, cfg["type"])

        # place instantiated procedure in the returned dictionary
        procedures[cfg["instance_name"]] = proc_class(hw_obj, records=qdict)

    return procedures
