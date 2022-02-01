import queue


class Recorder:
    """ Base recorder class.
    """

    def __init__(self, q=None):
        """ Initialize a recorder.

        :param: q: All Recorder subclasses listen for data on a queue.
        """
        self.recorder_queue = q if q is not None else queue.Queue()


def create_recorders(recorder_cfg):
    """ Create and return a recorder object given the configuration dictionary.
    """
    return None
