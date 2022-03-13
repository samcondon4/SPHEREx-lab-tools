import os
import logging
import numpy as np
import pyqtgraph as pg
from ..thread import QueueThread
from PyQt5 import QtCore, QtWidgets
from pyqtgraph.parametertree import Parameter, ParameterTree


pg.setConfigOption("imageAxisOrder", "row-major")
logger = logging.getLogger(__name__)


class Viewer(QueueThread, QtWidgets.QWidget):
    """ Base QueueThread viewer class.
    """

    startup_signal = QtCore.pyqtSignal()
    update_signal = QtCore.pyqtSignal(object)
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self, cfg, **kwargs):
        self.name = cfg["instance_name"]
        QueueThread.__init__(self, **kwargs)
        QtWidgets.QWidget.__init__(self, **kwargs)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.graphics_layout = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.graphics_layout)
        self.startup_signal.connect(self.show_view)
        self.shutdown_signal.connect(self.close_view)
        self.configuration_tree = ParameterTree()

    def set_cfg_parameters(self, params, **kwargs):
        """ Set the configuration parameters of the configuration parameters tree.
        """
        self.configuration_tree.setParameters(params, **kwargs)
        self.layout.addWidget(self.configuration_tree)

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

    def __init__(self, cfg, buf_size=10, **kwargs):
        """ Basic line viewer initialization.

        :param cfg: Configuration dictionary.
        :param buf_size: Size of the curve buffer.
        """
        if buf_size == 0:
            err_msg = "Error in initialization of viewer: %s: LineViewer cannot operate without a buffer!" \
                      % self.name
            logger.error(err_msg)
            raise BufferError(err_msg)
        # remove buf_size from kwargs so that two values aren't received #
        if "buf_size" in kwargs:
            kwargs.pop("buf_size")
        super().__init__(cfg, buf_size=buf_size, **kwargs)

        # create plot item #
        pkwargs = {} if "params" not in cfg.keys() else cfg["params"]
        self.plot_item = self.graphics_layout.addPlot(row=0, col=0, **pkwargs)
        self.plot = self.plot_item.plot(self.buffer)

        self.update_signal.connect(self.update_line)

    def update_line(self):
        """ Slot for the update signal. This is executed in the main thread and updates
            the data displayed in the plot item.
        """
        logger.debug("LineViewer updating plot data.")
        self.plot.setData(np.array(self.buffer))
        # print(self.buffer)

    def handle(self, record):
        """ Update the plot.
        """
        if not self.should_stop():
            self.update_signal.emit()


class ImageViewer(Viewer):
    """ Basic image viewer based on the pyqtgraph GraphicsLayoutWidget.
    """

    def __init__(self, cfg, levels_param_tree=True, show_hist_opt=True, export_opt=True, levels=None, **kwargs):
        """ Initialize the image viewer.

        :param cfg: Viewer configuration dictionary.
        :param levels_param_tree: Boolean to indicate if a parameter tree to set min/max pixel values should be
                                  provided.
        :param show_hist_opt: Boolean to indicate if an option to show a pixel histogram should be provided.
        :param export_opt: Boolean to indicate if an option to export contents of viewer should be provided.
        """
        super(ImageViewer, self).__init__(cfg)
        self.view = self.graphics_layout.addViewBox()
        self.view.setAspectLocked(True)
        self.img = pg.ImageItem(border="w")
        self.view.addItem(self.img)
        self.update_signal.connect(self.update_image_item)
        self.levels = levels
        self.histogram = None

        # configure levels parameter tree #
        params = []
        if levels_param_tree:
            self.levels_params = Parameter.create(name="Levels", type="group", children=[
                {"name": "Min", "type": "float"},
                {"name": "Max", "type": "float"},
                {"name": "Auto-scale", "type": "bool", "value": True}
            ])
            params.append(self.levels_params)

        # configure histogram #
        analysis_params = []
        if show_hist_opt:
            self.show_hist_opt = Parameter.create(name="Show Histogram", type="bool")
            analysis_params.append(self.show_hist_opt)
        if len(analysis_params) > 0:
            self.analysis_params = Parameter.create(name="Image Analysis", type="group", children=analysis_params)
            params.append(self.analysis_params)

        # configure data export #
        if export_opt:
            self.export_opt = Parameter.create(name="Export", type="group", children=[
                {"name": "Output Path", "type": "str", "value": os.getcwd()},
                {"name": "Filename", "type": "str", "value": self.name+"Img"},
                {"name": "Format", "type": "list", "limits": [".jpg", ".png"]},
                {"name": "Export", "type": "action"}
            ])
            params.append(self.export_opt)

        # create top level config parameter and call the set method #
        self.cfg_params = Parameter.create(name="Configuration Parameters", type="group", children=params)
        self.set_cfg_parameters(self.cfg_params, showTop=False)
        self.cfg_params.sigTreeStateChanged.connect(self.update_viewer_from_cfg)
        #self.cfg_params.monitorChildren()

    def update_viewer_from_cfg(self, changes):
        """ Update behavior of viewer after changes have occured in the Tree state.

        :param changes: Changes that occured in the cfg_params tree.
        """
        print(changes)

    def update_image_item(self, data):
        """ Slot for the update signal. This is executed in the main thread, and
            updates the currently displayed image data in the viewer.
        """
        logger.debug("ImageViewer updating image data")
        # if received data is a dictionary, grab the data key/value pair #
        kwargs = {}
        if self.levels is not None:
            kwargs.update({"levels": self.levels})
        self.img.setImage(data, **kwargs)

    def handle(self, record):
        """ Write image data to the view.
        """
        if not self.should_stop():
            self.update_signal.emit(record.data)

