import pyqtgraph as pg
from ..thread import QueueThread


pg.setConfigOption("imageAxisOrder", "row-major")


class Viewer(pg.GraphicsLayoutWidget, QueueThread):
    """ Base QueueThread viewer class.
    """

    def __init__(self, **kwargs):
        super(Viewer, self).__init__(**kwargs)

    def startup(self):
        """ Open the gui.
        """
        self.setVisible(True)

    def shutdown(self):
        """ Close the gui.
        """
        self.setVisible(False)


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

    def handle(self, data, **kwargs):
        """ Write image data to the view.
        """
        if not self.should_stop():
            self.img.setImage(data)


def create_viewers(exp_pkg):
    """ Return a set of viewers based on the configuration argument.

    :param: exp_pkg: User experiment configuration package.
    """
    viewer_cfg = exp_pkg.VIEWERS
    viewers = {}
    for cfg in viewer_cfg:
        if cfg["type"] == "ImageViewer":
            viewers[cfg["instance_name"]] = ImageViewer()
    return viewers
