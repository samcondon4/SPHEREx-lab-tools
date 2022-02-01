import pyqtgraph as pg
from ..thread import QueueThread


class ImageViewer(pg.GraphicsLayoutWidget, QueueThread):
    """ Basic image viewer based on the pyqtgraph GraphicsLayoutWidget.
    """

    def __init__(self, q=None, **kwargs):
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
            viewers[cfg["instance_name"]] = ImageViewer(cfg)
    return viewers
