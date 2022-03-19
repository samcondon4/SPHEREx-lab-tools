""" cam_view:

    Module implementing the procedures camera viewer for the collimator focus measurement.
"""
import logging
from spherexlabtools.viewers import ImageViewer


logger = logging.getLogger(__name__)


class CamViewer(ImageViewer):
    """ Subclass of the basic image viewer that overrides the update_display() method to remove
        the value from the image histogram that has the most occurences. Not totally clear if this
        is necessary yet...
    """

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)
