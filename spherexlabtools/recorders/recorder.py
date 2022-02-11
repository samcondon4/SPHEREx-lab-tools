import importlib
import pandas as pd
from ..thread import QueueThread


class HDF5Recorder(QueueThread):
    """ Base recorder class.
    """

    def __init__(self, cfg, **kwargs):
        """ Initialize a recorder.
        """
        super().__init__(**kwargs)
        self.filename = cfg["filename"]
        self.store = pd.HDFStore(self.filename)

    def handle(self, data, group=None, **kwargs):
        """ Generic recorder handle.
        """
        df = pd.DataFrame(data)
        self.store.append(group, df)


def create_recorders(exp_pkg):
    """ Create and return a set of recorder objects given the configuration dictionary.

    :param: exp_pkg: Experiment package module object.
    """
    rec_cfgs = exp_pkg.RECORDERS
    recorders = {}
    for cfg in rec_cfgs:
        name = cfg["instance_name"]

        # instantiate the recorder object. Search order for a recorder class is:
        # 1) User defined recorders in the provided experiment package.
        # 2) spherexlabtools core recorders.
        try:
            rec_class = getattr(exp_pkg.recorders, cfg["type"])
        except (AttributeError, ModuleNotFoundError):
            rec_mod = importlib.import_module(__name__)
            rec_class = getattr(rec_mod, cfg["type"])

        recorders[name] = rec_class(cfg)

    return recorders
