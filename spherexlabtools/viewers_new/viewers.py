import logging
import pyqtgraph as pg
from ..thread import QueueThread
from PyQt5 import QtCore, QtWidgets
from pyqtgraph.parametertree import Parameter, ParameterTree
import spherexlabtools.log as slt_log

pg.setConfigOption("imageAxisOrder", "row-major")
logger = logging.getLogger(f"{slt_log.LOGGER_NAME}.{__name__}")


class Viewer(QueueThread, QtWidgets.QWidget):

    pass


class LineViewer:

    pass


class ImageViewer:

    pass

