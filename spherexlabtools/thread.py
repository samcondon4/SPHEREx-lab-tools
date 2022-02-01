""" thread:

        Simple module to implement a stoppable thread that listens for data over a queue
        and performs some action when data is received.
"""
import queue
from pymeasure.thread import StoppableThread


class QueueThread(StoppableThread):

    def __init__(self, q=None, timeout=None):
        """ Initialize a new queue thread.

        :param: q: Queue object
        :param: timeout: queue get timeout.
        """
        super().__init__()
        self.queue = q if q is not None else queue.Queue()
        self.timeout = timeout
        self.data = None

    def run(self):
        """ Method that executes when thread is started.
        """
        while not self.should_stop():
            self.data = self.queue.get(self.timeout)
            self.handle()

    def handle(self):
        """ Method called after data is received in the queue.
        """
        raise NotImplementedError("handle() must be implemented in subclasses!")
