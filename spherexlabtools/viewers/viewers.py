import logging
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from ..thread import QueueThread


pg.setConfigOption("imageAxisOrder", "row-major")
logger = logging.getLogger(__name__)


class Viewer(QueueThread, pg.GraphicsLayoutWidget):
    """ Base QueueThread viewer class.
    """

    startup_signal = QtCore.pyqtSignal()
    update_signal = QtCore.pyqtSignal(object)
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self, cfg, exp, **kwargs):
        self.name = cfg["instance_name"]
        self.exp = exp
        QueueThread.__init__(self, **kwargs)
        pg.GraphicsLayoutWidget.__init__(self)
        self.startup_signal.connect(self.show_view)
        self.shutdown_signal.connect(self.close_view)

    def show_view(self):
        """ Slot for the qt startup signal. This is executed in the main thread.
        """
        self.setVisible(True)

    def close_view(self):
        """ Slot for the qt shutdown signal. This is executed in the main thread.
        """
        self.setVisible(False)

    def startup(self):
        """ Open the gui.
        """
        self.startup_signal.emit()

    def shutdown(self):
        """ Close the gui.
        """
        self.shutdown_signal.emit()


class LineViewer(Viewer):
    """ Basic line viewer.
    """

    # this viewer operates on buffered data, so override update_signal to take no arguments on emit() #
    update_signal = QtCore.pyqtSignal()

    def __init__(self, cfg, exp, buf_size=10, channels=1, **kwargs):
        """ Basic line viewer initialization.

        :param cfg: Configuration dictionary.
        :param buf_size: Size of the curve buffer.
        :param channels: Integer number of lines to plot in the view, or list with
                         string labels of different channels to plot.
        """
        if buf_size == 0:
            err_msg = "Error in initialization of viewer: %s: LineViewer cannot operate without a buffer!" \
                      % self.name
            logger.error(err_msg)
            raise BufferError(err_msg)
        # remove buf_size from kwargs so that two values aren't received #
        if "buf_size" in kwargs:
            kwargs.pop("buf_size")
        super().__init__(cfg, exp, buf_size=buf_size, **kwargs)

        # create plot item #
        pkwargs = {} if "params" not in cfg.keys() else cfg["params"]
        self.plot_item = self.addPlot(row=0, col=0, **pkwargs)
        self.plot = self.plot_item.plot(self.buffer)

        self.update_signal.connect(self.update_line)

    def update_line(self):
        """ Slot for the update signal. This is executed in the main thread and updates
            the data displayed in the plot item.
        """
        logger.debug("LineViewer updating plot data.")
        self.plot.setData(np.array(self.buffer))

    def handle(self, record):
        """ Update the plot.
        """
        if not self.should_stop():
            self.update_signal.emit()


class ImageViewer(Viewer):
    """ Basic image viewer based on the pyqtgraph GraphicsLayoutWidget.
    """

    def __init__(self, cfg, exp, **kwargs):
        """ Initialize the image viewer.
        """
        super(ImageViewer, self).__init__(cfg, exp)
        self.view = self.addViewBox()
        self.view.setAspectLocked(True)
        self.img = pg.ImageItem(border="w")
        self.view.addItem(self.img)
        self.update_signal.connect(self.update_image_item)

    def update_image_item(self, data, auto_levels=True):
        """ Slot for the update signal. This is executed in the main thread, and
            updates the currently displayed image data in the viewer.
        """
        logger.debug("ImageViewer updating image data")
        # if received data is a dictionary, grab the data key/value pair #
        self.img.setImage(data, autoLevels=auto_levels)

    def handle(self, record):
        """ Write image data to the view.
        """
        if not self.should_stop():
            self.update_signal.emit(record.data)

