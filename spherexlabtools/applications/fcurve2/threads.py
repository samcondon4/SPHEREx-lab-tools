import time
import threading


class BaseThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self._kill = False

    def kill(self):
        """ Thread kill signal.
        """
        self._kill = True

    def execution_loop(self):
        """ Thread activity that is looped until the kill signal is set.
        """
        raise NotImplementedError("execution_loop() must be overridden in a subclass!")

    def run(self):
        """ run thread.
        """
        print("thread {} running".format(self))
        while not self._kill:
            self.execution_loop()
        self._kill = False
        print("\nthread {} ending".format(self))


class ImageWriteThread(BaseThread):

    def __init__(self):
        super().__init__()

    def execution_loop(self):
        x = 2


class ImageDisplayThread(BaseThread):

    def __init__(self):
        super().__init__()

    def execution_loop(self):
        y = 3


class ProcedureThread(BaseThread):

    def __init__(self):
        super().__init__()

    def execution_loop(self):
        z = 6


