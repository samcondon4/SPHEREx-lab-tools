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

    def __init__(self, cfg, exp, **kwargs):
        self.name = cfg["instance_name"]
        self.exp = exp
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

    def __init__(self, cfg, exp, **kwargs):
        """ Basic line viewer initialization.

        :param cfg: Configuration dictionary.
        :param buf_size: Size of the curve buffer.
        :param channels: Integer number of lines to plot in the view, or list with
                         string labels of different channels to plot.
        """
        super().__init__(cfg, exp, **kwargs)

        # create plot item #
        pkwargs = {} if "params" not in cfg.keys() else cfg["params"]
        self.plot_item = self.graphics_layout.addPlot(row=0, col=0, **pkwargs)
        self.plot = self.plot_item.plot(self.buffer)

        self.update_signal.connect(self.update_line)

    def update_line(self, buf):
        """ Slot for the update signal. This is executed in the main thread and updates
            the data displayed in the plot item.
        """
        logger.debug("LineViewer updating plot data.")
        self.plot.setData(np.array(buf))

    def handle(self, record):
        """ Update the plot.
        """
        if not self.should_stop():
            self.update_signal.emit(record.buffer)


class ImageViewer(Viewer):
    """ Basic image viewer based on the pyqtgraph GraphicsLayoutWidget.
    """

    default_levels = (0, 255)

    def __init__(self, cfg, exp, levels=None, levels_param_tree=True, auto_scale=False, **kwargs):
        """ Initialize the image viewer.

        :param cfg: Viewer configuration dictionary.
        :param exp: Experiment object.
        :param levels: Initial min/max levels of the display
        :param levels_param_tree: Boolean to indicate if a parameter tree to set min/max pixel values should be
                                  provided.
        :param auto_scale: Boolean to determine if auto-scaling is initially on or off.
        """
        super(ImageViewer, self).__init__(cfg, exp)
        # explicitly adding the ViewBox class may be unnecessary here? #
        self.view = self.graphics_layout.addViewBox()
        self.view.setAspectLocked(True)
        self.img = pg.ImageItem(border="w")
        self.view.addItem(self.img)

        # histogram
        self.hist_plot = None
        self.hist_plot_data = None

        self.update_signal.connect(self.update_display)
        self.levels = levels if levels is not None else self.default_levels
        self.auto_scale = auto_scale

        # configure levels parameter tree #
        params = []
        if levels_param_tree:
            self.levels_params = Parameter.create(name="Levels", type="group", children=[
                {"name": "Min", "type": "float", "value": self.levels[0]},
                {"name": "Max", "type": "float", "value": self.levels[1]},
                {"name": "Auto_scale", "type": "bool", "value": True}
            ])
            params.append(self.levels_params)
            self.levels_params.sigTreeStateChanged.connect(self.update_levels)

        # create top level config parameter and call the set method #
        self.cfg_params = Parameter.create(name="Configuration Parameters", type="group", children=params)
        self.set_cfg_parameters(self.cfg_params, showTop=False)

    def update_levels(self, param, changes):
        """ Update the levels attribute when an interface value changes.
        """
        changed_param = changes[0][0]
        name = changed_param.name()
        val = changed_param.value()
        if name == "Min" and val < self.levels[1]:
            self.levels[0] = val
        elif name == "Max" and val > self.levels[0]:
            self.levels[1] = val
        elif name == "Auto_scale":
            self.auto_scale = val
        else:
            logger.error("Invalid viewer settings specified. Changes have not been set in the viewer!")

    def update_display(self, record):
        """ Slot for the update signal. This is executed in the main thread, and
            updates the currently displayed image data in the viewer.
        """
        logger.debug("ImageViewer updating image data")
        # update image item ########################################
        data = record.data
        kwargs = {}
        if self.auto_scale is False:
            kwargs.update({"levels": self.levels})
        self.img.setImage(data, **kwargs)

        # update histogram plot item ################################
        hist = record.ancillary.get("histogram", None)
        # graphics layout update
        if hist is not None and self.hist_plot is None:
            self.hist_plot = self.graphics_layout.addPlot()
        elif hist is None and self.hist_plot is not None:
            self.graphics_layout.removeItem(self.hist_plot)
            self.hist_plot = None
        # hist plot data update
        if hist is not None and self.hist_plot_data is None:
            self.hist_plot_data = self.hist_plot.plot(hist[1], hist[0], stepMode="center", fillLevel=0,
                                                      fillOutline=True, brush=(0, 0, 255, 100))
        elif hist is not None and self.hist_plot_data is not None:
            self.hist_plot_data.setData(hist[1], hist[0])

    def handle(self, record):
        """ Write image data to the view.
        """
        if not self.should_stop():
            self.update_signal.emit(record)

