

class Recorder:
    """ Base recorder class.
    """

    def __init__(self, recorder_cfg):
        pass


def create_recorders(recorder_cfg):
    """ Create and return a recorder object given the configuration dictionary.
    """
    return Recorder(recorder_cfg)
