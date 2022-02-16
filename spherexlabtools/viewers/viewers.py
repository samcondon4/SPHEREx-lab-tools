import logging
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

    def __init__(self, cfg, **kwargs):
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


class ImageViewer(Viewer):
    """ Basic image viewer based on the pyqtgraph GraphicsLayoutWidget.
    """

    def __init__(self, cfg, **kwargs):
        """ Initialize the image viewer.
        """
        super(ImageViewer, self).__init__(cfg)
        self.view = self.addViewBox()
        self.view.setAspectLocked(True)
        self.img = pg.ImageItem(border="w")
        self.view.addItem(self.img)
        self.update_signal.connect(self.update_image_item)

    def update_image_item(self, data):
        """ Slot for the update signal. This is executed in the main thread, and
            updates the currently displayed image data in the viewer.
        """
        logger.debug("ImageViewer updating image data")
        # if received data is a dictionary, grab the data key/value pair #
        self.img.setImage(data)

    def handle(self, record):
        """ Write image data to the view.
        """
        if not self.should_stop():
            self.update_signal.emit(record.data)

