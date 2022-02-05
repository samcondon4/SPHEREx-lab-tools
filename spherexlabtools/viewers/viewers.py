import pyqtgraph as pg
from ..thread import QueueThread


class Viewer(pg.GraphicsLayoutWidget, QueueThread):
    """ Base QueueThread viewer class.
    """

    def __init__(self):
        super(Viewer, self).__init__()

    def run(self):
        """ Open the gui and start queue processing.
        """
        self.show()
        while not self.should_stop():
            self.queue_process()

    def kill(self):
        """ Close the gui and stop queue processing.
        """
        self.close()
        self.stop()


class ImageViewer(Viewer):
    """ Basic image viewer based on the pyqtgraph GraphicsLayoutWidget.
    """

    def __init__(self, **kwargs):
        """ Initialize the image viewer.
        """
        super(ImageViewer, self).__init__()
        self.view = self.addViewBox()
        self.view.setAspectLocked(True)
        self.img = pg.ImageItem(border="w")
        self.view.addItem(self.img)

    def handle(self):
        """ Write image data to the view.
        """
        self.img.setImage(self.data)


def create_viewers(viewer_cfg):
    """ Return a set of viewers based on the configuration argument.
    """
    viewers = {}
    for cfg in viewer_cfg:
        if cfg["type"] == "ImageViewer":
            viewers[cfg["instance_name"]] = ImageViewer()
    return viewers
